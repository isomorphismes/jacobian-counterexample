import * as THREE from "three";
import type { CurvePreset, Track } from "../math/curves";
import type { Vec3 } from "../math/map";

export type Space = "source" | "target";

export type ViewBounds = {
  center: THREE.Vector3;
  radius: number;
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
  if (box.isEmpty()) return { center: new THREE.Vector3(), radius: 2 };
  const center = box.getCenter(new THREE.Vector3());
  const size = box.getSize(new THREE.Vector3());
  return { center, radius: Math.max(1.25, size.length() / 2) };
}

export function lineObject(points: readonly THREE.Vector3[], color: number): THREE.Line {
  const geometry = new THREE.BufferGeometry().setFromPoints([...points]);
  const material = new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.9 });
  return new THREE.Line(geometry, material);
}

export function disposeObject(object: THREE.Object3D): void {
  object.traverse((child) => {
    if (!(child instanceof THREE.Mesh || child instanceof THREE.Line)) return;
    child.geometry.dispose();
    const materials = Array.isArray(child.material) ? child.material : [child.material];
    materials.forEach((material) => material.dispose());
  });
}
