/** Exact formulas used by the page. Numbers are floating-point only for drawing. */
export type Vec3 = readonly [x: number, y: number, z: number];

export function markedRootMap([x, y, z]: Vec3): Vec3 {
  const u = 1 + x * y;
  return [
    u ** 3 * z + y ** 2 * u * (4 + 3 * x * y),
    y + 3 * x * u ** 2 * z + 3 * x * y ** 2 * (4 + 3 * x * y),
    2 * x - 3 * x ** 2 * y - x ** 3 * z,
  ];
}

/** Q(U,V)=cU^3-2U^2V+bUV^2-2aV^3. */
export function binaryCubic([a, b, c]: Vec3, u: number, v: number): number {
  return c * u ** 3 - 2 * u ** 2 * v + b * u * v ** 2 - 2 * a * v ** 3;
}

/** p(t)=Q(t,1), for a finite projective root [t:1]. */
export function cubicAt([a, b, c]: Vec3, t: number): number {
  return c * t ** 3 - 2 * t ** 2 + b * t - 2 * a;
}

export function cubicDerivative([, b, c]: Vec3, t: number): number {
  return 3 * c * t ** 2 - 4 * t + b;
}

/** Recover the unique source point associated with a simple finite root. */
export function inverseAtFiniteRoot(target: Vec3, root: number): Vec3 {
  const [, , c] = target;
  const rho = cubicDerivative(target, root);
  if (Math.abs(rho) < 1e-12) {
    throw new RangeError("The selected root is not simple.");
  }
  const x = 2 / rho;
  const y = root - rho / 2;
  const z = (5 * rho ** 2) / 4 - (3 * root * rho) / 2 - (c * rho ** 3) / 8;
  return [x, y, z];
}

/** The normalized cubic whose three real roots are q-1, q, q+1. */
export function threeRootTarget(q: number): Vec3 {
  if (Math.abs(q) < 1e-12) {
    throw new RangeError("q=0 is outside this affine chart.");
  }
  const c = 2 / (3 * q);
  const a = (c * (q ** 3 - q)) / 2;
  const b = c * (3 * q ** 2 - 1);
  return [a, b, c];
}

/** Coefficients for 2t(t-s)(t-(1-s)), with roots 0, s, and 1-s. */
export function coalescingRootTarget(s: number): Vec3 {
  return [0, 2 * s * (1 - s), 2];
}

export function distance(a: Vec3, b: Vec3): number {
  return Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
}

export function formatCoordinate(value: number): string {
  if (Math.abs(value) < 5e-10) return "0";
  const magnitude = Math.abs(value);
  if (magnitude >= 1e4 || magnitude < 1e-3) return value.toExponential(2);
  return Number(value.toFixed(3)).toString();
}

export function formatVec3(value: Vec3): string {
  return `(${value.map(formatCoordinate).join(", ")})`;
}
