import { describe, expect, it } from "vitest";
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
});
