import assert from "node:assert/strict";
import { mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { chromium } from "playwright-core";

const siteUrl = process.env.SITE_URL ?? "http://127.0.0.1:4174/";
const chromePath = process.env.CHROME_PATH
  ?? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const outputDir = resolve(process.env.BROWSER_QA_OUTPUT ?? "/tmp/jacobian-browser-qa");

await mkdir(outputDir, { recursive: true });

const browserErrors = [];
const failedRequests = [];
const report = { siteUrl, viewports: {}, interaction: {}, fallback: {} };

function monitor(page, label, { allowWebglErrors = false } = {}) {
  page.on("console", (message) => {
    if (message.type() !== "error") return;
    const text = message.text();
    if (allowWebglErrors && /WebGL context|Error creating WebGL/i.test(text)) return;
    browserErrors.push(`${label}: ${text}`);
  });
  page.on("pageerror", (error) => browserErrors.push(`${label}: ${error.message}`));
  page.on("requestfailed", (request) => {
    failedRequests.push(`${label}: ${request.url()} — ${request.failure()?.errorText ?? "failed"}`);
  });
}

async function inspectViewport(browser, label, viewport, reducedMotion = "no-preference") {
  const context = await browser.newContext({ viewport, reducedMotion });
  const page = await context.newPage();
  monitor(page, label);
  await page.goto(siteUrl, { waitUntil: "networkidle" });
  await page.locator("main").waitFor();
  await page.waitForTimeout(600);

  const geometry = await page.evaluate(() => ({
    innerWidth: window.innerWidth,
    innerHeight: window.innerHeight,
    scrollWidth: document.documentElement.scrollWidth,
    scrollHeight: document.documentElement.scrollHeight,
    heroRight: document.querySelector(".hero-copy")?.getBoundingClientRect().right,
    heroButtonRights: [...document.querySelectorAll(".hero-actions .button")]
      .map((element) => element.getBoundingClientRect().right),
  }));
  assert.equal(geometry.innerWidth, viewport.width, `${label}: viewport emulation failed`);
  assert.ok(
    geometry.scrollWidth <= geometry.innerWidth + 1,
    `${label}: horizontal overflow ${geometry.scrollWidth}px > ${geometry.innerWidth}px`,
  );
  assert.ok(
    geometry.heroButtonRights.every((right) => right <= geometry.innerWidth + 1),
    `${label}: a hero action leaves the viewport`,
  );
  assert.ok((geometry.heroRight ?? 0) <= geometry.innerWidth + 1, `${label}: hero copy overflows`);

  const transcript = page.locator("#film-transcript");
  await transcript.locator("summary").click();
  assert.equal(await transcript.locator("[data-segment-id]").count(), 14);
  assert.ok(await page.locator("#film .transcript-download a").isVisible());
  assert.equal(await page.locator("#film video source").count(), 1);
  assert.equal(
    await page.locator("#film video source").getAttribute("type"),
    "video/mp4",
  );
  assert.equal(await page.locator("#film video track[kind='captions'][default]").count(), 1);
  const openScrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
  assert.ok(
    openScrollWidth <= geometry.innerWidth + 1,
    `${label}: the open transcript causes horizontal overflow`,
  );

  await page.locator(".hero").screenshot({ path: resolve(outputDir, `${label}-hero.png`) });
  await page.screenshot({ path: resolve(outputDir, `${label}-full.png`), fullPage: true });
  report.viewports[label] = geometry;

  if (label === "desktop") {
    assert.equal(await page.locator("#curve-select option").count(), 6);
    assert.equal(await page.locator("#curve-select").inputValue(), "pencil");
    assert.equal(await page.locator("#coordinate-rows tr").count(), 11);
    await page.locator("[data-viewer]").scrollIntoViewIfNeeded();
    await page.locator("#source-plot canvas").waitFor();
    assert.equal(await page.locator("#source-plot canvas").count(), 1);
    assert.equal(await page.locator("#target-plot canvas").count(), 1);
    assert.equal(await page.locator("#source-plot").getAttribute("data-curve-tracks"), "11");
    const pixelRatio = Number(await page.locator("#source-plot").getAttribute("data-pixel-ratio"));
    assert.ok(pixelRatio >= 1 && pixelRatio <= 1.8, `viewer DPR ${pixelRatio} exceeds its cap`);
    await page.locator("[data-viewer]").screenshot({ path: resolve(outputDir, "desktop-viewer-pencil.png") });

    await page.locator("#curve-select").selectOption("surface");
    assert.equal(await page.locator("#source-plot").getAttribute("data-surface-vertices"), "775");
    assert.equal(await page.locator("#coordinate-rows tr").count(), 3);
    await page.locator("[data-viewer]").screenshot({ path: resolve(outputDir, "desktop-viewer-surface.png") });

    await page.locator("#curve-select").selectOption("sheets");
    assert.equal(await page.locator("#coordinate-rows tr").count(), 3);
    await page.locator("#curve-progress").evaluate((element) => {
      element.value = "800";
      element.dispatchEvent(new Event("input", { bubbles: true }));
    });
    const targets = await page.locator("#coordinate-rows td:last-child").allTextContents();
    assert.equal(new Set(targets).size, 1, "three marked-root sheets must share one target");

    const sections = [
      ["infographic", ".root-infographic"],
      ["viewer", "[data-viewer]"],
      ["lenses", "#lenses"],
      ["film", "#film"],
      ["provenance", "#provenance"],
    ];
    for (const [name, selector] of sections) {
      await page.locator(selector).screenshot({ path: resolve(outputDir, `desktop-${name}.png`) });
    }
    await transcript.screenshot({ path: resolve(outputDir, "desktop-film-transcript.png") });
    report.interaction = {
      presets: 6,
      pencilRows: 11,
      surfaceVertices: 775,
      pixelRatio,
      sheetRows: 3,
      coincidentTarget: targets[0],
      transcriptSegments: 14,
      captionTrack: true,
      videoFormat: "video/mp4",
    };
  }

  if (reducedMotion === "reduce") {
    await page.locator("#curve-select").selectOption("elementary");
    assert.equal(await page.locator("#play-curve").textContent(), "Next step");
    await page.locator("#play-curve").click();
    assert.equal(await page.locator("#curve-progress").inputValue(), "100");
    assert.equal(await page.locator("#play-curve").getAttribute("aria-pressed"), "false");
    report.interaction.reducedMotionStep = true;
  }

  await context.close();
}

const browser = await chromium.launch({
  executablePath: chromePath,
  headless: true,
  args: ["--disable-background-networking", "--disable-sync", "--no-first-run"],
});

try {
  await inspectViewport(browser, "desktop", { width: 1440, height: 1000 });
  await inspectViewport(browser, "mobile", { width: 390, height: 844 });
  await inspectViewport(browser, "reduced", { width: 1024, height: 768 }, "reduce");
} finally {
  await browser.close();
}

const fallbackBrowser = await chromium.launch({
  executablePath: chromePath,
  headless: true,
  args: ["--disable-webgl", "--disable-gpu", "--no-first-run"],
});
try {
  const context = await fallbackBrowser.newContext({ viewport: { width: 1024, height: 768 } });
  const page = await context.newPage();
  monitor(page, "fallback", { allowWebglErrors: true });
  await page.goto(siteUrl, { waitUntil: "networkidle" });
  await page.locator("[data-viewer]").scrollIntoViewIfNeeded();
  await page.locator("#webgl-fallback").waitFor({ state: "visible" });
  assert.equal(await page.locator("#coordinate-rows tr").count(), 11);
  await page.locator("[data-viewer]").screenshot({ path: resolve(outputDir, "webgl-fallback.png") });
  report.fallback = { visible: true, coordinateRows: 11 };
  await context.close();
} finally {
  await fallbackBrowser.close();
}

assert.deepEqual(browserErrors, [], `browser console errors:\n${browserErrors.join("\n")}`);
assert.deepEqual(failedRequests, [], `failed requests:\n${failedRequests.join("\n")}`);
await writeFile(resolve(outputDir, "report.json"), `${JSON.stringify(report, null, 2)}\n`);
process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
