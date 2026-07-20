import "./styles/base.css";
import "./styles/layout.css";
import "./styles/components.css";
import "./styles/viewer.css";

import { canonicalCurveFixture, curvePresets, frameAt, presetById, type CurveFrame, type CurvePreset } from "./math/curves";
import { formatVec3 } from "./math/map";
import { DualSpaceViewer } from "./viewer/dual-space-viewer";

function required<T extends Element>(selector: string): T {
  const element = document.querySelector<T>(selector);
  if (!element) throw new Error(`Missing required element: ${selector}`);
  return element;
}

const select = required<HTMLSelectElement>("#curve-select");
const progress = required<HTMLInputElement>("#curve-progress");
const playButton = required<HTMLButtonElement>("#play-curve");
const parameterOutput = required<HTMLOutputElement>("#curve-parameter");
const title = required<HTMLElement>("#curve-title");
const description = required<HTMLElement>("#curve-description");
const reading = required<HTMLElement>("#curve-reading");
const rows = required<HTMLTableSectionElement>("#coordinate-rows");
const zoom = required<HTMLInputElement>("#view-zoom");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

for (const preset of curvePresets) {
  const option = document.createElement("option");
  option.value = preset.id;
  option.textContent = preset.shortTitle;
  select.append(option);
}

const query = new URLSearchParams(window.location.search);
let activePreset: CurvePreset = presetById(query.get("curve") ?? "collision");
let normalizedProgress = Math.min(1, Math.max(0, Number(query.get("p") ?? 0) || 0));
let viewer: DualSpaceViewer | undefined;
let playing = false;
let animationFrame = 0;
let lastTime = 0;

try {
  viewer = new DualSpaceViewer(
    required<HTMLElement>("#source-plot"),
    required<HTMLElement>("#target-plot"),
  );
} catch (error) {
  required<HTMLElement>("#webgl-fallback").hidden = false;
  document.querySelectorAll<HTMLElement>(".plot").forEach((plot) => plot.classList.add("plot-unavailable"));
  console.info("3D viewer unavailable; using the coordinate fallback.", error);
}

function colorCss(color: number): string {
  return `#${color.toString(16).padStart(6, "0")}`;
}

function updateTable(frame: CurveFrame): void {
  const newRows = frame.tracks.map((track) => {
    const row = document.createElement("tr");
    const heading = document.createElement("th");
    heading.scope = "row";
    heading.style.color = colorCss(track.color);
    const swatch = document.createElement("span");
    swatch.className = "branch-swatch";
    swatch.setAttribute("aria-hidden", "true");
    heading.append(swatch, document.createTextNode(track.label));
    const source = document.createElement("td");
    source.textContent = formatVec3(track.source);
    const target = document.createElement("td");
    target.textContent = formatVec3(track.target);
    row.append(heading, source, target);
    return row;
  });
  rows.replaceChildren(...newRows);
}

function writePermalink(): void {
  const url = new URL(window.location.href);
  url.searchParams.set("curve", activePreset.id);
  url.searchParams.set("p", normalizedProgress.toFixed(3));
  window.history.replaceState({}, "", url);
}

function updateFrame(updateUrl = true): void {
  const frame = frameAt(activePreset, normalizedProgress);
  progress.value = String(Math.round(normalizedProgress * 1000));
  parameterOutput.textContent = frame.parameterText;
  viewer?.setFrame(frame);
  updateTable(frame);
  if (updateUrl) writePermalink();
}

function stopPlaying(): void {
  playing = false;
  playButton.textContent = reduceMotion.matches ? "Next step" : "Play";
  playButton.setAttribute("aria-pressed", "false");
  cancelAnimationFrame(animationFrame);
  animationFrame = 0;
  lastTime = 0;
  writePermalink();
}

function animationTick(time: number): void {
  if (!playing) return;
  if (!lastTime) lastTime = time;
  normalizedProgress += (time - lastTime) / 9000;
  lastTime = time;
  if (normalizedProgress >= 1) {
    normalizedProgress = 1;
    updateFrame(false);
    stopPlaying();
    return;
  }
  updateFrame(false);
  animationFrame = requestAnimationFrame(animationTick);
}

function setPreset(next: CurvePreset): void {
  stopPlaying();
  activePreset = next;
  normalizedProgress = 0;
  select.value = next.id;
  title.textContent = next.title;
  description.textContent = next.description;
  reading.textContent = next.reading;
  const isStatic = next.id === "collision";
  progress.disabled = isStatic;
  playButton.disabled = isStatic;
  viewer?.setPreset(next);
  updateFrame();
}

select.addEventListener("change", () => setPreset(presetById(select.value)));
progress.addEventListener("input", () => {
  stopPlaying();
  normalizedProgress = Number(progress.value) / 1000;
  updateFrame();
});

playButton.addEventListener("click", () => {
  if (reduceMotion.matches) {
    normalizedProgress = normalizedProgress >= 1 ? 0 : Math.min(1, normalizedProgress + 0.1);
    updateFrame();
    return;
  }
  if (playing) {
    stopPlaying();
    return;
  }
  if (normalizedProgress >= 1) normalizedProgress = 0;
  playing = true;
  playButton.textContent = "Pause";
  playButton.setAttribute("aria-pressed", "true");
  animationFrame = requestAnimationFrame(animationTick);
});

reduceMotion.addEventListener("change", () => {
  stopPlaying();
  playButton.textContent = reduceMotion.matches ? "Next step" : "Play";
});

zoom.addEventListener("input", () => viewer?.setZoom(Number(zoom.value) / 100));
required<HTMLButtonElement>("#reset-view").addEventListener("click", () => {
  zoom.value = "100";
  viewer?.resetView();
});

const rotations: Record<string, readonly [number, number]> = {
  left: [-0.14, 0],
  right: [0.14, 0],
  up: [0, 0.12],
  down: [0, -0.12],
};
document.querySelectorAll<HTMLButtonElement>("[data-rotate]").forEach((button) => {
  button.addEventListener("click", () => {
    const delta = rotations[button.dataset.rotate ?? ""];
    if (delta) viewer?.rotate(delta[0], delta[1]);
  });
});

required<HTMLButtonElement>("#copy-view").addEventListener("click", async (event) => {
  writePermalink();
  const button = event.currentTarget as HTMLButtonElement;
  try {
    await navigator.clipboard.writeText(window.location.href);
    button.textContent = "Link copied";
  } catch {
    button.textContent = "Copy the address bar";
  }
  window.setTimeout(() => { button.textContent = "Copy this view"; }, 1800);
});

required<HTMLButtonElement>("#download-data").addEventListener("click", () => {
  const payload = JSON.stringify(canonicalCurveFixture, null, 2);
  const link = document.createElement("a");
  link.href = URL.createObjectURL(new Blob([payload], { type: "application/json" }));
  link.download = "marked-root-curve-fixtures.json";
  link.click();
  window.setTimeout(() => URL.revokeObjectURL(link.href), 0);
});

select.value = activePreset.id;
title.textContent = activePreset.title;
description.textContent = activePreset.description;
reading.textContent = activePreset.reading;
viewer?.setPreset(activePreset);
progress.disabled = activePreset.id === "collision";
playButton.disabled = activePreset.id === "collision";
playButton.textContent = reduceMotion.matches ? "Next step" : "Play";
updateFrame(false);
