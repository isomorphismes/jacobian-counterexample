import * as THREE from "three";
import type { CurveFrame, CurvePreset } from "../math/curves";
import {
  asVector,
  boundsForPreset,
  disposeObject,
  lineObject,
  pointsForTrack,
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
  curves: THREE.Group;
  markers: THREE.Group;
  grid: THREE.GridHelper;
  axes: THREE.AxesHelper;
  bounds: ViewBounds;
  resizeObserver: ResizeObserver;
};

const neutralTarget = 0xe8edf7;

export class DualSpaceViewer {
  private panels: readonly [Panel, Panel];
  private preset: CurvePreset | undefined;
  private yaw = -0.72;
  private pitch = 0.47;
  private zoom = 1;
  private dirty = false;
  private frameRequest = 0;

  constructor(sourceHost: HTMLElement, targetHost: HTMLElement) {
    if (!window.WebGLRenderingContext) throw new Error("WebGL is unavailable.");
    this.panels = [this.makePanel(sourceHost, "source"), this.makePanel(targetHost, "target")];
    this.bindPointer(this.panels[0]);
    this.bindPointer(this.panels[1]);
    this.renderSoon();
  }

  setPreset(preset: CurvePreset): void {
    this.preset = preset;
    this.zoom = 1;
    for (const panel of this.panels) {
      this.clear(panel.curves);
      this.clear(panel.markers);
      panel.bounds = boundsForPreset(preset, panel.space);
      const guideScale = Math.max(1, panel.bounds.radius / 4);
      panel.grid.scale.setScalar(guideScale);
      panel.axes.scale.setScalar(guideScale);
      const firstFrame = preset.samples[0]!;
      const allTargetsCoincide = panel.space === "target" && firstFrame.tracks.length > 1 && preset.samples.every((frame) => {
        const first = frame.tracks[0]?.target;
        return first && frame.tracks.every((track) => track.target.every((v, i) => Math.abs(v - first[i]!) < 1e-9));
      });

      firstFrame.tracks.forEach((track, index) => {
        if (!(allTargetsCoincide && index > 0)) {
          const path = pointsForTrack(preset, track.id, panel.space);
          const line = lineObject(path, allTargetsCoincide ? neutralTarget : track.color);
          panel.curves.add(line);
        }

        const markerRadius = Math.max(0.045, panel.bounds.radius * 0.018);
        const marker = new THREE.Mesh(
          new THREE.SphereGeometry(markerRadius, 20, 14),
          new THREE.MeshBasicMaterial({
            color: track.color,
            wireframe: allTargetsCoincide,
            transparent: true,
            opacity: 0.98,
          }),
        );
        marker.name = track.id;
        if (allTargetsCoincide) marker.scale.setScalar(1 + index * 0.55);
        panel.markers.add(marker);
      });
    }
    this.setFrame(preset.samples[0]!);
  }

  setFrame(frame: CurveFrame): void {
    for (const panel of this.panels) {
      for (const track of frame.tracks) {
        const marker = panel.markers.getObjectByName(track.id);
        marker?.position.copy(asVector(trackPoint(track, panel.space)));
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
    this.yaw = -0.72;
    this.pitch = 0.47;
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

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0);
    renderer.outputColorSpace = THREE.SRGBColorSpace;

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x090d19, 0.012);
    const camera = new THREE.PerspectiveCamera(36, 1, 0.01, 5000);

    const grid = new THREE.GridHelper(12, 12, 0x46506a, 0x252d40);
    grid.rotation.x = Math.PI / 2;
    grid.material.transparent = true;
    grid.material.opacity = 0.42;
    scene.add(grid);

    const axes = new THREE.AxesHelper(3.3);
    axes.material.transparent = true;
    axes.material.opacity = 0.68;
    scene.add(axes);

    const curves = new THREE.Group();
    const markers = new THREE.Group();
    scene.add(curves, markers);

    let panel!: Panel;
    const resizeObserver = new ResizeObserver(() => {
      const rect = host.getBoundingClientRect();
      const width = Math.max(1, Math.round(rect.width));
      const height = Math.max(1, Math.round(rect.height));
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      this.renderSoon();
    });

    panel = {
      space,
      host,
      scene,
      camera,
      renderer,
      curves,
      markers,
      grid,
      axes,
      bounds: { center: new THREE.Vector3(), radius: 2 },
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
    const direction = new THREE.Vector3(
      Math.cos(this.pitch) * Math.cos(this.yaw),
      Math.cos(this.pitch) * Math.sin(this.yaw),
      Math.sin(this.pitch),
    );
    const distance = (panel.bounds.radius * 3.35) / this.zoom;
    panel.camera.position.copy(panel.bounds.center).addScaledVector(direction, distance);
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
