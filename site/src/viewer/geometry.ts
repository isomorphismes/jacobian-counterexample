import * as THREE from "three";
import type { CurvePreset, SurfaceMesh, Track } from "../math/curves";
import type { Vec3 } from "../math/map";

export type Space = "source" | "target";

export type ViewBounds = {
  center: THREE.Vector3;
  radius: number;
  min: THREE.Vector3;
  max: THREE.Vector3;
};

export function asVector([x, y, z]: Vec3): THREE.Vector3 {
  return new THREE.Vector3(x, y, z);
}

export function trackPoint(track: Track, space: Space): Vec3 {
  return space === "source" ? track.source : track.target;
}

export function pointsForTrack(preset: CurvePreset, trackId: string, space: Space): THREE.Vector3[] {
  return preset.samples.flatMap((frame) => {
    const track = frame.tracks.find((candidate) => candidate.id === trackId);
    return track ? [asVector(trackPoint(track, space))] : [];
  });
}

export function boundsForPreset(preset: CurvePreset, space: Space): ViewBounds {
  const box = new THREE.Box3();
  for (const frame of preset.samples) {
    for (const track of frame.tracks) box.expandByPoint(asVector(trackPoint(track, space)));
  }
  for (const surface of preset.surfaces ?? []) {
    const points = space === "source" ? surface.source : surface.target;
    for (const point of points) box.expandByPoint(asVector(point));
  }
  if (box.isEmpty()) {
    return {
      center: new THREE.Vector3(),
      radius: 2,
      min: new THREE.Vector3(-1, -1, -1),
      max: new THREE.Vector3(1, 1, 1),
    };
  }
  const center = box.getCenter(new THREE.Vector3());
  const size = box.getSize(new THREE.Vector3());
  return {
    center,
    radius: Math.max(1.1, size.length() * 0.54),
    min: box.min.clone(),
    max: box.max.clone(),
  };
}

function polylinePath(points: readonly THREE.Vector3[]): THREE.CurvePath<THREE.Vector3> {
  const path = new THREE.CurvePath<THREE.Vector3>();
  for (let index = 1; index < points.length; index += 1) {
    path.add(new THREE.LineCurve3(points[index - 1]!.clone(), points[index]!.clone()));
  }
  return path;
}

/** A luminous tube remains legible at high-density and high-DPI viewports. */
export function lineObject(
  points: readonly THREE.Vector3[],
  color: number,
  sceneRadius: number,
): THREE.Group {
  const group = new THREE.Group();
  if (points.length < 2 || points.every((point) => point.distanceToSquared(points[0]!) < 1e-18)) {
    return group;
  }

  const path = polylinePath(points);
  const tubularSegments = Math.min(144, Math.max(12, points.length - 1));
  const coreRadius = Math.max(sceneRadius * 0.0085, 0.012);
  const haloRadius = coreRadius * 2.35;
  const halo = new THREE.Mesh(
    new THREE.TubeGeometry(path, tubularSegments, haloRadius, 5, false),
    new THREE.MeshBasicMaterial({
      color,
      transparent: true,
      opacity: 0.14,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      toneMapped: false,
    }),
  );
  halo.renderOrder = 3;

  const core = new THREE.Mesh(
    new THREE.TubeGeometry(path, tubularSegments, coreRadius, 6, false),
    new THREE.MeshBasicMaterial({ color, toneMapped: false }),
  );
  core.renderOrder = 4;
  group.add(halo, core);
  return group;
}

function pointsForSurface(surface: SurfaceMesh, space: Space): readonly Vec3[] {
  return space === "source" ? surface.source : surface.target;
}

export function surfaceGeometry(surface: SurfaceMesh, space: Space): THREE.BufferGeometry {
  const points = pointsForSurface(surface, space);
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute(
    "position",
    new THREE.Float32BufferAttribute(points.flatMap((point) => [...point]), 3),
  );

  const indices: number[] = [];
  for (let row = 0; row < surface.rows - 1; row += 1) {
    for (let column = 0; column < surface.columns - 1; column += 1) {
      const topLeft = row * surface.columns + column;
      const topRight = topLeft + 1;
      const bottomLeft = topLeft + surface.columns;
      const bottomRight = bottomLeft + 1;
      indices.push(topLeft, bottomLeft, topRight, topRight, bottomLeft, bottomRight);
    }
  }
  geometry.setIndex(indices);
  geometry.computeVertexNormals();
  geometry.computeBoundingSphere();
  return geometry;
}

export function surfaceGridGeometry(surface: SurfaceMesh, space: Space): THREE.BufferGeometry {
  const points = pointsForSurface(surface, space);
  const segments: number[] = [];
  const append = (first: Vec3, second: Vec3) => segments.push(...first, ...second);
  for (let row = 0; row < surface.rows; row += 1) {
    for (let column = 1; column < surface.columns; column += 1) {
      append(points[row * surface.columns + column - 1]!, points[row * surface.columns + column]!);
    }
  }
  for (let column = 0; column < surface.columns; column += 1) {
    for (let row = 1; row < surface.rows; row += 1) {
      append(points[(row - 1) * surface.columns + column]!, points[row * surface.columns + column]!);
    }
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.Float32BufferAttribute(segments, 3));
  return geometry;
}

export function disposeObject(object: THREE.Object3D): void {
  object.traverse((child) => {
    if (!(child instanceof THREE.Mesh || child instanceof THREE.Line)) return;
    child.geometry.dispose();
    const materials = Array.isArray(child.material) ? child.material : [child.material];
    materials.forEach((material) => material.dispose());
  });
}
