import * as THREE from "three";
import type { CurveFrame, CurvePreset } from "../math/curves";
import {
  asVector,
  boundsForPreset,
  disposeObject,
  lineObject,
  pointsForTrack,
  surfaceGeometry,
  surfaceGridGeometry,
  trackPoint,
  type Space,
  type ViewBounds,
} from "./geometry";

type Panel = {
  space: Space;
  host: HTMLElement;
  scene: THREE.Scene;
  camera: THREE.PerspectiveCamera;
  renderer: THREE.WebGLRenderer;
  surfaces: THREE.Group;
  curves: THREE.Group;
  markers: THREE.Group;
  grid: THREE.GridHelper;
  axes: THREE.AxesHelper;
  bounds: ViewBounds;
  resizeObserver: ResizeObserver;
};

const neutralTarget = 0xe8edf7;
const defaultView = { yaw: -0.72, pitch: 0.47 } as const;
const maxCanvasPixels = 1_350_000;

export class DualSpaceViewer {
  private panels: readonly [Panel, Panel];
  private preset: CurvePreset | undefined;
  private yaw: number = defaultView.yaw;
  private pitch: number = defaultView.pitch;
  private zoom = 1;
  private dirty = false;
  private frameRequest = 0;
  private readonly cameraDirection = new THREE.Vector3();

  constructor(sourceHost: HTMLElement, targetHost: HTMLElement) {
    if (!window.WebGLRenderingContext) throw new Error("WebGL is unavailable.");
    this.panels = [this.makePanel(sourceHost, "source"), this.makePanel(targetHost, "target")];
    this.bindPointer(this.panels[0]);
    this.bindPointer(this.panels[1]);
    this.renderSoon();
  }

  setPreset(preset: CurvePreset): void {
    this.preset = preset;
    this.yaw = preset.camera?.yaw ?? defaultView.yaw;
    this.pitch = preset.camera?.pitch ?? defaultView.pitch;
    this.zoom = 1;
    for (const panel of this.panels) {
      this.clear(panel.surfaces);
      this.clear(panel.curves);
      this.clear(panel.markers);
      panel.bounds = boundsForPreset(preset, panel.space);
      const guideScale = Math.max(1, panel.bounds.radius / 4);
      panel.grid.scale.setScalar(guideScale);
      const gridZ = panel.bounds.min.z <= 0 && panel.bounds.max.z >= 0
        ? 0
        : panel.bounds.min.z;
      panel.grid.position.set(panel.bounds.center.x, panel.bounds.center.y, gridZ);
      panel.axes.scale.setScalar(guideScale);
      panel.scene.fog = new THREE.Fog(
        0x07101d,
        panel.bounds.radius * 2.5,
        panel.bounds.radius * 6.4,
      );

      for (const surface of preset.surfaces ?? []) {
        const fill = new THREE.Mesh(
          surfaceGeometry(surface, panel.space),
          new THREE.MeshStandardMaterial({
            color: surface.color,
            transparent: true,
            opacity: surface.opacity,
            depthWrite: false,
            side: THREE.DoubleSide,
            roughness: 0.38,
            metalness: 0.08,
          }),
        );
        fill.name = `${surface.id}-fill`;
        fill.renderOrder = 1;
        const grid = new THREE.LineSegments(
          surfaceGridGeometry(surface, panel.space),
          new THREE.LineBasicMaterial({
            color: surface.color,
            transparent: true,
            opacity: 0.58,
            depthWrite: false,
            toneMapped: false,
          }),
        );
        grid.name = `${surface.id}-grid`;
        grid.renderOrder = 2;
        panel.surfaces.add(fill, grid);
      }

      const firstFrame = preset.samples[0]!;
      const allTargetsCoincide = panel.space === "target" && firstFrame.tracks.length > 1 && preset.samples.every((frame) => {
        const first = frame.tracks[0]?.target;
        return first && frame.tracks.every((track) => track.target.every((v, i) => Math.abs(v - first[i]!) < 1e-9));
      });

      firstFrame.tracks.forEach((track, index) => {
        if (!(allTargetsCoincide && index > 0)) {
          const path = pointsForTrack(preset, track.id, panel.space);
          const line = lineObject(
            path,
            allTargetsCoincide ? neutralTarget : track.color,
            panel.bounds.radius,
          );
          panel.curves.add(line);
        }

        const markerRadius = Math.max(0.04, panel.bounds.radius * 0.021);
        const marker = new THREE.Group();
        marker.name = track.id;
        const scale = allTargetsCoincide ? 1 + index * 0.62 : 1;
        const core = new THREE.Mesh(
          allTargetsCoincide
            ? new THREE.IcosahedronGeometry(markerRadius * scale, 2)
            : new THREE.SphereGeometry(markerRadius, 18, 12),
          new THREE.MeshBasicMaterial({
            color: track.color,
            wireframe: allTargetsCoincide,
            toneMapped: false,
          }),
        );
        core.renderOrder = 6;
        marker.add(core);
        if (!allTargetsCoincide) {
          const halo = new THREE.Mesh(
            new THREE.IcosahedronGeometry(markerRadius * 1.72, 1),
            new THREE.MeshBasicMaterial({
              color: track.color,
              wireframe: true,
              transparent: true,
              opacity: 0.35,
              depthWrite: false,
              blending: THREE.AdditiveBlending,
              toneMapped: false,
            }),
          );
          halo.renderOrder = 5;
          marker.add(halo);
        }
        panel.markers.add(marker);
      });
      panel.host.dataset.surfaceVertices = String(
        (preset.surfaces ?? []).reduce((total, surface) => total + surface.source.length, 0),
      );
      panel.host.dataset.curveTracks = String(firstFrame.tracks.length);
    }
    this.setFrame(preset.samples[0]!);
  }

  setFrame(frame: CurveFrame): void {
    for (const panel of this.panels) {
      for (const track of frame.tracks) {
        const marker = panel.markers.getObjectByName(track.id);
        const point = trackPoint(track, panel.space);
        marker?.position.set(point[0], point[1], point[2]);
      }
    }
    this.renderSoon();
  }

  rotate(deltaYaw: number, deltaPitch: number): void {
    this.yaw += deltaYaw;
    this.pitch = THREE.MathUtils.clamp(this.pitch + deltaPitch, -1.2, 1.2);
    this.renderSoon();
  }

  setZoom(next: number): void {
    this.zoom = THREE.MathUtils.clamp(next, 0.65, 2.8);
    this.renderSoon();
  }

  resetView(): void {
    this.yaw = this.preset?.camera?.yaw ?? defaultView.yaw;
    this.pitch = this.preset?.camera?.pitch ?? defaultView.pitch;
    this.zoom = 1;
    this.renderSoon();
  }

  private makePanel(host: HTMLElement, space: Space): Panel {
    const canvas = document.createElement("canvas");
    canvas.setAttribute("role", "img");
    canvas.setAttribute(
      "aria-label",
      `${space === "source" ? "Source" : "Target"} three-dimensional curve plot. Coordinates are repeated in the accessible table below.`,
    );
    host.append(canvas);

    const renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: false,
      powerPreference: "high-performance",
    });
    renderer.setPixelRatio(1);
    renderer.setClearColor(0x07101d, 1);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.14;

    const scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x07101d, 5, 18);
    const camera = new THREE.PerspectiveCamera(34, 1, 0.01, 5000);

    const hemisphere = new THREE.HemisphereLight(0xb9ddff, 0x090b17, 2.1);
    const key = new THREE.DirectionalLight(0xffffff, 2.35);
    key.position.set(4, -5, 7);
    const rim = new THREE.DirectionalLight(0x61f0dc, 1.5);
    rim.position.set(-5, 3, 2);
    scene.add(hemisphere, key, rim);

    const grid = new THREE.GridHelper(12, 12, 0x46506a, 0x252d40);
    grid.rotation.x = Math.PI / 2;
    grid.material.transparent = true;
    grid.material.opacity = 0.3;
    scene.add(grid);

    const axes = new THREE.AxesHelper(3.3);
    axes.material.transparent = true;
    axes.material.opacity = 0.78;
    scene.add(axes);

    const surfaces = new THREE.Group();
    const curves = new THREE.Group();
    const markers = new THREE.Group();
    scene.add(surfaces, curves, markers);

    let panel!: Panel;
    const resizeObserver = new ResizeObserver(() => {
      const rect = host.getBoundingClientRect();
      const width = Math.max(1, Math.round(rect.width));
      const height = Math.max(1, Math.round(rect.height));
      const pixelRatio = Math.min(
        window.devicePixelRatio || 1,
        1.8,
        Math.sqrt(maxCanvasPixels / (width * height)),
      );
      renderer.setPixelRatio(Math.max(1, pixelRatio));
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      host.dataset.pixelRatio = renderer.getPixelRatio().toFixed(2);
      this.renderSoon();
    });

    panel = {
      space,
      host,
      scene,
      camera,
      renderer,
      surfaces,
      curves,
      markers,
      grid,
      axes,
      bounds: {
        center: new THREE.Vector3(),
        radius: 2,
        min: new THREE.Vector3(-1, -1, -1),
        max: new THREE.Vector3(1, 1, 1),
      },
      resizeObserver,
    };
    resizeObserver.observe(host);
    return panel;
  }

  private bindPointer(panel: Panel): void {
    const canvas = panel.renderer.domElement;
    let pointer: { id: number; x: number; y: number } | undefined;

    canvas.addEventListener("pointerdown", (event) => {
      pointer = { id: event.pointerId, x: event.clientX, y: event.clientY };
      canvas.setPointerCapture(event.pointerId);
    });
    canvas.addEventListener("pointermove", (event) => {
      if (!pointer || pointer.id !== event.pointerId) return;
      this.rotate((event.clientX - pointer.x) * 0.008, (event.clientY - pointer.y) * 0.008);
      pointer.x = event.clientX;
      pointer.y = event.clientY;
    });
    canvas.addEventListener("pointerup", () => { pointer = undefined; });
    canvas.addEventListener("pointercancel", () => { pointer = undefined; });
    canvas.addEventListener("wheel", (event) => {
      event.preventDefault();
      this.setZoom(this.zoom * Math.exp(-event.deltaY * 0.001));
    }, { passive: false });
  }

  private updateCamera(panel: Panel): void {
    this.cameraDirection.set(
      Math.cos(this.pitch) * Math.cos(this.yaw),
      Math.cos(this.pitch) * Math.sin(this.yaw),
      Math.sin(this.pitch),
    );
    const distance = (panel.bounds.radius * 3.28) / this.zoom;
    panel.camera.position.copy(panel.bounds.center).addScaledVector(this.cameraDirection, distance);
    panel.camera.up.set(0, 0, 1);
    panel.camera.lookAt(panel.bounds.center);
    panel.camera.near = Math.max(0.005, distance / 200);
    panel.camera.far = Math.max(100, distance * 20);
    panel.camera.updateProjectionMatrix();
  }

  private clear(group: THREE.Group): void {
    for (const child of [...group.children]) {
      group.remove(child);
      disposeObject(child);
    }
  }

  private renderSoon(): void {
    this.dirty = true;
    if (this.frameRequest) return;
    this.frameRequest = requestAnimationFrame(() => {
      this.frameRequest = 0;
      if (!this.dirty) return;
      this.dirty = false;
      for (const panel of this.panels) {
        this.updateCamera(panel);
        panel.renderer.render(panel.scene, panel.camera);
      }
    });
  }
}
