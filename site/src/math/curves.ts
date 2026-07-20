import curveFixtureJson from "../../../shared/curve-fixtures.json";
import { markedRootMap, type Vec3 } from "./map";

type FixtureSample = { parameter: number; point: number[] };
type ElementaryFixture = {
  id: string;
  domain: number[];
  source: FixtureSample[];
  target: FixtureSample[];
};
type CurveFixture = {
  schema_version: number;
  space_note: string;
  map_formula: string[];
  elementary_curves: ElementaryFixture[];
  sheet_family: {
    polynomial: string;
    domain: number[];
    target: FixtureSample[];
    branches: Record<string, FixtureSample[]>;
  };
  three_point_fiber: { source: number[][]; target: number[] };
};

export type Track = {
  id: string;
  label: string;
  color: number;
  source: Vec3;
  target: Vec3;
};

export type CurveFrame = {
  parameter: number;
  parameterText: string;
  tracks: readonly Track[];
};

export type CurvePreset = {
  id: string;
  title: string;
  shortTitle: string;
  description: string;
  reading: string;
  samples: readonly CurveFrame[];
};

export const canonicalCurveFixture = curveFixtureJson as CurveFixture;

const colors = [0xffb45e, 0x65e4ca, 0xa99bff] as const;

function linspace(start: number, end: number, count = 121): number[] {
  return Array.from({ length: count }, (_, index) =>
    start + (end - start) * (index / (count - 1)),
  );
}

function fixtureVec(point: readonly number[]): Vec3 {
  if (point.length !== 3) throw new Error("Curve fixture points must have three coordinates.");
  return [point[0]!, point[1]!, point[2]!];
}

function mappedTrack(id: string, label: string, color: number, source: Vec3): Track {
  return { id, label, color, source, target: markedRootMap(source) };
}

const collisionPoints = canonicalCurveFixture.three_point_fiber.source.map(fixtureVec);
const collisionTarget = fixtureVec(canonicalCurveFixture.three_point_fiber.target);

const collision: CurvePreset = {
  id: "collision",
  title: "The certified three-point fiber",
  shortTitle: "Three points, one image",
  description:
    "Three distinct source points (left) land on exactly the same target point (right). This is the shortest certificate that the map is not injective.",
  reading: "The three colored target markers coincide at (−¼, 0, 0).",
  samples: linspace(0, 1, 2).map((parameter) => ({
    parameter,
    parameterText: "fixed fiber",
    tracks: collisionPoints.map((source, index) => ({
      id: `point-${index}`,
      label: `preimage ${index + 1}`,
      color: colors[index]!,
      source,
      target: collisionTarget,
    })),
  })),
};

const axisNames: Record<string, string> = {
  x_axis: "x-axis",
  y_axis: "y-axis",
  z_axis: "z-axis",
};
const elementarySampleCount = canonicalCurveFixture.elementary_curves[0]?.source.length ?? 0;
const elementaryFrames: CurveFrame[] = Array.from({ length: elementarySampleCount }, (_, index) => ({
  parameter: index,
  parameterText: canonicalCurveFixture.elementary_curves
    .map((curve) => `${axisNames[curve.id] ?? curve.id}: ${curve.source[index]!.parameter.toFixed(2)}`)
    .join(" · "),
  tracks: canonicalCurveFixture.elementary_curves.map((curve, curveIndex) => ({
    id: curve.id,
    label: axisNames[curve.id] ?? curve.id,
    color: colors[curveIndex]!,
    source: fixtureVec(curve.source[index]!.point),
    target: fixtureVec(curve.target[index]!.point),
  })),
}));

const elementary: CurvePreset = {
  id: "elementary",
  title: "Three coordinate axes under the map",
  shortTitle: "Elementary curves",
  description:
    "The x-axis maps to (0,0,2t), the y-axis to (4t²,t,0), and the z-axis to (t,0,0). The middle image bends into a parabola; the other two remain lines.",
  reading: "These deterministic samples are shared verbatim with the Manim animation.",
  samples: elementaryFrames,
};

const sheetTargets = canonicalCurveFixture.sheet_family.target;
const sheetBranches = ["zero", "moving", "remaining"] as const;
const sheetFrames: CurveFrame[] = [...sheetTargets].reverse().map((targetSample, reverseIndex) => {
  const originalIndex = sheetTargets.length - 1 - reverseIndex;
  const s = targetSample.parameter;
  const target = fixtureVec(targetSample.point);
  return {
    parameter: s,
    parameterText: `s = ${s.toFixed(3)} · roots 0, ${s.toFixed(3)}, ${(1 - s).toFixed(3)}`,
    tracks: sheetBranches.map((branch, index) => ({
      id: `root-${index}`,
      label: `marked root ${branch === "zero" ? "0" : branch === "moving" ? "s" : "1−s"}`,
      color: colors[index]!,
      source: fixtureVec(canonicalCurveFixture.sheet_family.branches[branch]![originalIndex]!.point),
      target,
    })),
  };
});

const threeSheets: CurvePreset = {
  id: "sheets",
  title: "Three sheets over one target curve",
  shortTitle: "Three inverse sheets",
  description:
    "The target cubic 2T(T−s)(T−(1−s)) has roots 0, s, and 1−s. Marking each root gives one colored source curve; forgetting the mark makes all three land on the same target curve.",
  reading:
    "Three moving source points correspond to one moving target point. As s tends to 0, the first two roots collide and their marked branches escape.",
  samples: sheetFrames,
};

const escape: CurvePreset = {
  id: "escape",
  title: "A missing inverse branch escapes to infinity",
  shortTitle: "Escape to infinity",
  description:
    "As s grows, (s,−1/s,5/s²) runs away in the source while its image (0,2/s,0) approaches the finite target (0,0,0). This is nonproperness made visible.",
  reading: "Each camera rescales to fit its curve; the coordinates below report the true values.",
  samples: linspace(1, 20).map((s) => {
    const source: Vec3 = [s, -1 / s, 5 / s ** 2];
    return {
      parameter: s,
      parameterText: `s = ${s.toFixed(2)}`,
      tracks: [mappedTrack("escape", "escaping branch", colors[1], source)],
    };
  }),
};

export const curvePresets: readonly CurvePreset[] = [collision, elementary, threeSheets, escape];

export function presetById(id: string): CurvePreset {
  return curvePresets.find((preset) => preset.id === id) ?? curvePresets[0]!;
}

export function frameAt(preset: CurvePreset, progress: number): CurveFrame {
  const clamped = Math.min(1, Math.max(0, progress));
  const index = Math.round(clamped * (preset.samples.length - 1));
  return preset.samples[index]!;
}
