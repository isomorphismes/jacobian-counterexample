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


async function inspectCharcoal(page, label) {
  const result = await page.evaluate(() => {
    const rgb = (text) => {
      const values = text.match(/[0-9.]+/g)?.map(Number);
      if (!values || values.length < 3) throw new Error("Unparsed CSS color: " + text);
      return [values[0], values[1], values[2], values[3] ?? 1];
    };
    const luminance = (color) => color.slice(0, 3).map((v) => {
      const c = v / 255;
      return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
    }).reduce((sum, v, i) => sum + v * [0.2126, 0.7152, 0.0722][i], 0);
    const ratio = (a, b) => {
      const x = luminance(a), y = luminance(b);
      return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
    };
    const background = (element) => {
      const chain = [];
      for (let e = element; e; e = e.parentElement) chain.unshift(e);
      let color = [33, 33, 33, 1];
      for (const e of chain) {
        const next = rgb(getComputedStyle(e).backgroundColor);
        color = next.slice(0, 3).map((v, i) => v * next[3] + color[i] * (1 - next[3]));
        color.push(1);
      }
      return color;
    };
    const surfaces = [
      ["body", 33], [".section-light", 47], [".film-section", 33],
      [".formula-section", 33], [".proof-section", 33],
      [".viewer-section", 33], [".viewer-shell", 47],
      [".viewer-toolbar", 47], [".viewer-toolbar select", 56],
      [".button-primary", 56], [".button-small", 56],
    ].map(([selector, value]) => {
      const elements = [...document.querySelectorAll(selector)];
      if (!elements.length) throw new Error("Missing theme surface " + selector);
      for (const element of elements) {
        const actual = rgb(getComputedStyle(element).backgroundColor);
        if (actual.some((v, i) => i < 3 && v !== value) || actual[3] !== 1) {
          throw new Error("Charcoal role mismatch " + selector + ": " + actual);
        }
      }
      return { selector, value, count: elements.length };
    });
    const failures = [];
    let textCount = 0, lowest = 100;
    for (const element of document.querySelectorAll("body *")) {
      // Scientific SVG/canvas colors, video, and the existing image overlay stay intact.
      if (element.closest("svg, .plot, .hero, .site-header, .map-arrow")) continue;
      if (!element.getClientRects().length || element.matches(":disabled")) continue;
      if (![...element.childNodes].some((n) => n.nodeType === Node.TEXT_NODE && n.textContent.trim())) continue;
      const style = getComputedStyle(element);
      if (style.visibility !== "visible" || Number(style.opacity) === 0) continue;
      const bg = background(element), fg = rgb(style.color);
      const composite = fg.slice(0, 3).map((v, i) => v * fg[3] + bg[i] * (1 - fg[3]));
      const actual = ratio(composite, bg);
      textCount++;
      lowest = Math.min(lowest, actual);
      if (actual < 4.5) failures.push({ element: element.tagName + "." + element.className, actual, color: style.color, bg });
    }
    if (textCount < 100) throw new Error("Insufficient actual interface text observed: " + textCount);
    if (failures.length) throw new Error("AA text failures: " + JSON.stringify(failures));
    return { surfaces, textCount, lowestContrast: lowest, exceptions: ["scientific SVG and plot colors", "video and original hero image overlay"] };
  });
  return { label, ...result };
}

async function inspectViewport(browser, label, viewport, reducedMotion = "no-preference", colorScheme = "dark") {
  const context = await browser.newContext({ viewport, reducedMotion, colorScheme });
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

  report.charcoal ??= {};
  report.charcoal[label] = await inspectCharcoal(page, label);
  const whiteRoot = await page.addStyleTag({ content: "body { background: #FFFFFF !important; }" });
  await page.waitForFunction(() => getComputedStyle(document.body).backgroundColor === "rgb(255, 255, 255)");
  await assert.rejects(() => inspectCharcoal(page, label), /Charcoal role mismatch body/);
  await whiteRoot.evaluate((element) => element.remove());
  await page.waitForFunction(() => getComputedStyle(document.body).backgroundColor === "rgb(33, 33, 33)");
  await inspectCharcoal(page, label);
  report.charcoal[label].whiteRootNegative = "REJECTED";
  await page.locator(".hero-actions .button").first().focus();
  await page.keyboard.press("Tab");
  await page.keyboard.press("Shift+Tab");
  await page.waitForFunction(() => {
    const element = document.querySelector(".hero-actions .button");
    const style = getComputedStyle(element);
    return document.activeElement === element && element.matches(":focus-visible")
      && style.outlineColor === "rgb(180, 180, 180)" && style.outlineWidth === "3px";
  });
  const focus = await page.locator(".hero-actions .button").first().evaluate((element) => {
    const style = getComputedStyle(element);
    return { color: style.outlineColor, width: style.outlineWidth, style: style.outlineStyle };
  });
  assert.deepEqual(focus, { color: "rgb(180, 180, 180)", width: "3px", style: "solid" });
  report.charcoal[label].keyboardFocus = "PASS";

  await page.locator(".hero").screenshot({ path: resolve(outputDir, `${label}-hero.png`) });
  await page.screenshot({ path: resolve(outputDir, `${label}-full.png`), fullPage: true });
  report.viewports[label] = geometry;

  if (label.startsWith("desktop")) {
    assert.equal(await page.locator("#curve-select option").count(), 5);
    assert.equal(await page.locator("#curve-select").inputValue(), "pencil");
    assert.equal(await page.locator("#coordinate-rows tr").count(), 11);
    await page.locator("[data-viewer]").scrollIntoViewIfNeeded();
    await page.locator("#source-plot canvas").waitFor();
    assert.equal(await page.locator("#source-plot canvas").count(), 1);
    assert.equal(await page.locator("#target-plot canvas").count(), 1);
    assert.equal(await page.locator("#source-plot").getAttribute("data-curve-tracks"), "11");
    const pixelRatio = Number(await page.locator("#source-plot").getAttribute("data-pixel-ratio"));
    assert.ok(pixelRatio >= 1 && pixelRatio <= 1.8, `viewer DPR ${pixelRatio} exceeds its cap`);
    await page.locator("[data-viewer]").screenshot({ path: resolve(outputDir, `${label}-viewer-pencil.png`) });

    await page.locator("#curve-select").selectOption("surface");
    assert.equal(await page.locator("#source-plot").getAttribute("data-surface-vertices"), "775");
    assert.equal(await page.locator("#coordinate-rows tr").count(), 3);
    await page.locator("[data-viewer]").screenshot({ path: resolve(outputDir, `${label}-viewer-surface.png`) });

    const sections = [
      ["infographic", ".root-infographic"],
      ["viewer", "[data-viewer]"],
      ["lenses", "#lenses"],
      ["film", "#film"],
      ["provenance", "#provenance"],
    ];
    for (const [name, selector] of sections) {
      await page.locator(selector).screenshot({ path: resolve(outputDir, `${label}-${name}.png`) });
    }
    await transcript.screenshot({ path: resolve(outputDir, `${label}-film-transcript.png`) });
    report.interaction = {
      presets: 5,
      pencilRows: 11,
      surfaceVertices: 775,
      pixelRatio,
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
  for (const scheme of ["dark", "light"]) {
    await inspectViewport(browser, "desktop-" + scheme, { width: 1440, height: 1000 }, "no-preference", scheme);
    await inspectViewport(browser, "mobile-" + scheme, { width: 390, height: 844 }, "no-preference", scheme);
    await inspectViewport(browser, "reduced-" + scheme, { width: 1024, height: 768 }, "reduce", scheme);
  }
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
  report.fallback = { visible: true, coordinateRows: 11, charcoal: await inspectCharcoal(page, "fallback") };
  await context.close();
} finally {
  await fallbackBrowser.close();
}

assert.deepEqual(browserErrors, [], `browser console errors:\n${browserErrors.join("\n")}`);
assert.deepEqual(failedRequests, [], `failed requests:\n${failedRequests.join("\n")}`);
await writeFile(resolve(outputDir, "report.json"), `${JSON.stringify(report, null, 2)}\n`);
process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
