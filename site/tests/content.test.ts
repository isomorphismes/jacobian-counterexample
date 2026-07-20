import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const html = readFileSync(resolve(import.meta.dirname, "../index.html"), "utf8");
const componentsCss = readFileSync(
  resolve(import.meta.dirname, "../src/styles/components.css"),
  "utf8",
);

describe("publication content", () => {
  it("resolves every in-page navigation target", () => {
    const targets = [...html.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]!);
    for (const target of targets) expect(html).toContain(`id="${target}"`);
  });

  it("links and distinguishes all primary contributions", () => {
    expect(html).toContain("https://x.com/__alpoge__/status/2079028340955197566");
    expect(html).toContain("https://x.com/davikrehalt/status/2079175065695035442");
    expect(html).toContain("https://aaronlou.com/jacobian_counterexample_derivation.pdf");
    expect(html).toMatch(/Bartosz Naskrecki[\s\S]*does not claim discovery/);
    expect(html).toContain("earliest formula post located by this audit");
    expect(html).toContain('datetime="2026-07-21">21 Jul 2026 · repository release');
  });

  it("states the visualization and dimension-two limits", () => {
    expect(html).toContain("six real dimensions");
    expect(html.toLowerCase()).toContain("dimension 2");
    expect(html).toContain("remains open");
  });

  it("uses the canonical assembled paper name", () => {
    expect(html).toContain("./paper/one-map-three-descriptions.pdf");
    expect(html).not.toContain("distinguished-root-map.pdf");
    expect(html).toContain(
      'property="og:image" content="https://nasqret.github.io/jacobian-counterexample/assets/hero-marked-roots.png"',
    );
  });

  it("publishes the complete canonical transcript and honest draft-voice status", () => {
    const segmentIds = [...html.matchAll(/data-segment-id="([^"]+)"/g)].map(
      (match) => match[1],
    );
    expect(segmentIds).toEqual([
      "credits",
      "local_global",
      "formula",
      "three_points",
      "mark_roots",
      "projective_map",
      "delete_ramification",
      "affine_slice",
      "factorization",
      "resultant",
      "unified",
      "real_curves",
      "escaping_sheets",
      "proof_scope",
    ]);
    expect(html).toContain("Read the exact narration transcript");
    expect(html).toContain("reproducibly configured offline Piper draft");
    expect(html).toContain("en_US-libritts-high");
    expect(html).toContain("speaker 0");
    expect(html).toContain("A human-recorded final narration is planned");
    expect(html).toContain("marked-root-explainer-transcript.md");
    expect(html).toContain("marked-root-explainer.mp4");
    expect(html).toContain('kind="captions"');
    expect(html).toContain('label="English" default');
    expect(html).not.toContain("marked-root-explainer.webm");
    expect(html).not.toContain("being prepared for this public release");
  });

  it("constrains and stacks the mobile hero instead of clipping it", () => {
    const mobile = componentsCss.slice(componentsCss.indexOf("@media (max-width: 620px)"));
    expect(mobile).toContain("max-width: calc(100% - 2.25rem)");
    expect(mobile).toContain("overflow-wrap: break-word");
    expect(mobile).toContain("flex-direction: column");
    expect(mobile).toMatch(/\.hero-actions \.button\s*{[\s\S]*?width: 100%/);
    expect(html).toContain("derivative is invertible everywhere");
    expect(html).not.toContain("same nonzero local volume scale");
  });
});
