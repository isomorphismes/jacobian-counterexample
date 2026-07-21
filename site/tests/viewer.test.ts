import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const read = (path: string) => readFileSync(resolve(import.meta.dirname, "..", path), "utf8");
const mainSource = read("src/main.ts");
const viewerSource = read("src/viewer/dual-space-viewer.ts");
const geometrySource = read("src/viewer/geometry.ts");

describe("viewer performance contract", () => {
  it("loads the Three.js viewer only when its section approaches the viewport", () => {
    expect(mainSource).toContain('import type { DualSpaceViewer as DualSpaceViewerInstance }');
    expect(mainSource).toContain('import("./viewer/dual-space-viewer")');
    expect(mainSource).toContain("IntersectionObserver");
    expect(mainSource).toContain('rootMargin: "700px 0px"');
  });

  it("does not repeat canvas and table work for the same sampled frame", () => {
    expect(mainSource).toContain("let renderedFrame: CurveFrame | undefined");
    expect(mainSource).toContain("if (frame !== renderedFrame)");
    expect(mainSource).toContain('zoom.value = "100"');
  });

  it("caps retina render cost while retaining bright geometric strokes", () => {
    expect(viewerSource).toContain("const maxCanvasPixels = 1_350_000");
    expect(viewerSource).toContain("Math.sqrt(maxCanvasPixels / (width * height))");
    expect(viewerSource).toContain("renderer.setPixelRatio(Math.max(1, pixelRatio))");
    expect(geometrySource).toContain("new THREE.TubeGeometry");
    expect(geometrySource).toContain("THREE.AdditiveBlending");
  });
});
