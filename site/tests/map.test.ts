import { describe, expect, it } from "vitest";
import * as THREE from "three";
import {
  binaryCubic,
  cubicAt,
  distance,
  inverseAtFiniteRoot,
  markedRootMap,
  threeRootTarget,
  type Vec3,
} from "../src/math/map";
import { curvePresets } from "../src/math/curves";
import {
  boundsForPreset,
  disposeObject,
  lineObject,
  pointsForTrack,
  surfaceGeometry,
  surfaceGridGeometry,
} from "../src/viewer/geometry";

const closeVec = (actual: Vec3, expected: Vec3, digits = 10) => {
  expected.forEach((value, index) => expect(actual[index]).toBeCloseTo(value, digits));
};

describe("displayed polynomial map", () => {
  it("maps all three certificate points to the same target", () => {
    const points: Vec3[] = [
      [0, 0, -1 / 4],
      [1, -3 / 2, 13 / 2],
      [-1, 3 / 2, 13 / 2],
    ];
    points.forEach((point) => closeVec(markedRootMap(point), [-1 / 4, 0, 0]));
  });

  it("satisfies the normalized marked-root identities", () => {
    const points: Vec3[] = [
      [0.3, -0.7, 1.2],
      [-1.1, 0.4, -0.2],
      [0, 2, 3],
    ];
    for (const [x, y, z] of points) {
      const target = markedRootMap([x, y, z]);
      expect(binaryCubic(target, 1 + x * y, x)).toBeCloseTo(0, 9);
    }
  });

  it("inverts a target at each selected simple root", () => {
    for (const q of [0.8, 1.2, 2.1]) {
      const target = threeRootTarget(q);
      for (const root of [q - 1, q, q + 1]) {
        expect(cubicAt(target, root)).toBeCloseTo(0, 11);
        closeVec(markedRootMap(inverseAtFiniteRoot(target, root)), target, 9);
      }
    }
  });
});

describe("viewer fixtures", () => {
  it("omits the unreadable inverse-sheets preset", () => {
    expect(curvePresets).toHaveLength(5);
    expect(curvePresets.map((preset) => preset.id)).not.toContain("sheets");
  });

  it("opens on an eleven-line pencil through the origin", () => {
    const pencil = curvePresets[0]!;
    expect(pencil.id).toBe("pencil");
    expect(pencil.samples[0]!.tracks).toHaveLength(11);
    const center = pencil.samples[Math.floor(pencil.samples.length / 2)]!;
    center.tracks.forEach((track) => closeVec(track.source, [0, 0, 0], 12));

    for (let trackIndex = 0; trackIndex < 11; trackIndex += 1) {
      const first = pencil.samples[0]!.tracks[trackIndex]!.source;
      const slope = first[1] / first[0];
      for (const frame of pencil.samples) {
        const [x, y, z] = frame.tracks[trackIndex]!.source;
        expect(z).toBe(0);
        expect(y).toBeCloseTo(slope * x, 12);
      }
    }
  });

  it("draws only honest source/image pairs", () => {
    for (const preset of curvePresets) {
      for (const frame of preset.samples) {
        for (const track of frame.tracks) {
          expect(distance(markedRootMap(track.source), track.target)).toBeLessThan(1e-7);
        }
      }
    }
  });

  it("sends the escaping source curve toward a finite target", () => {
    const escape = curvePresets.find((preset) => preset.id === "escape")!;
    const first = escape.samples[0]!.tracks[0]!;
    const last = escape.samples.at(-1)!.tracks[0]!;
    expect(Math.hypot(...last.source)).toBeGreaterThan(Math.hypot(...first.source));
    expect(Math.hypot(...last.target)).toBeLessThan(Math.hypot(...first.target));
    expect(last.target[1]).toBeCloseTo(0.1, 12);
  });

  it("triangulates a directly evaluated mapped surface within the render budget", () => {
    const preset = curvePresets.find((candidate) => candidate.id === "surface")!;
    const surface = preset.surfaces?.[0]!;
    expect(surface.rows).toBe(25);
    expect(surface.columns).toBe(31);
    expect(surface.source).toHaveLength(surface.rows * surface.columns);
    expect(surface.target).toHaveLength(surface.source.length);
    surface.source.forEach((source, index) => {
      const [x, y, z] = source;
      expect(y).toBe(0);
      closeVec(surface.target[index]!, [z, 3 * x * z, 2 * x - x ** 3 * z], 9);
      closeVec(markedRootMap(source), surface.target[index]!, 9);
    });

    const fill = surfaceGeometry(surface, "target");
    const grid = surfaceGridGeometry(surface, "target");
    expect(fill.getAttribute("position").count).toBe(775);
    expect(fill.index?.count).toBe((surface.rows - 1) * (surface.columns - 1) * 6);
    expect(grid.getAttribute("position").count).toBe(
      2 * (surface.rows * (surface.columns - 1) + surface.columns * (surface.rows - 1)),
    );
    expect(surface.source.length).toBeLessThan(1_000);

    for (let trackIndex = 0; trackIndex < 3; trackIndex += 1) {
      const fixedX = preset.samples[0]!.tracks[trackIndex]!.source[0];
      for (const frame of preset.samples) {
        const track = frame.tracks[trackIndex]!;
        const [x, y, z] = track.source;
        expect(x).toBe(fixedX);
        expect(y).toBe(0);
        closeVec(track.target, [z, 3 * fixedX * z, 2 * fixedX - fixedX ** 3 * z], 9);
      }
    }

    fill.dispose();
    grid.dispose();
  });

  it("keeps the retina pencil geometry inside an interactive triangle budget", () => {
    const pencil = curvePresets[0]!;
    let triangleCount = 0;
    for (const space of ["source", "target"] as const) {
      const bounds = boundsForPreset(pencil, space);
      for (const track of pencil.samples[0]!.tracks) {
        const object = lineObject(
          pointsForTrack(pencil, track.id, space),
          track.color,
          bounds.radius,
        );
        object.traverse((child) => {
          if (!(child instanceof THREE.Mesh)) return;
          triangleCount += (child.geometry.index?.count ?? 0) / 3;
        });
        disposeObject(object);
      }
    }
    expect(triangleCount).toBe(58_080);
    expect(triangleCount).toBeLessThan(70_000);
  });
});
