import { cp, mkdir, stat } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const siteRoot = resolve(here, "..");
const repoRoot = resolve(siteRoot, "..");
const dist = resolve(siteRoot, "dist");

async function exists(path) {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

await mkdir(resolve(dist, "paper"), { recursive: true });
await mkdir(resolve(dist, "legal"), { recursive: true });
await mkdir(resolve(dist, "media"), { recursive: true });

const canonicalPaper = resolve(repoRoot, "output/pdf/one_map_three_descriptions.pdf");
const currentPaper = resolve(repoRoot, "output/pdf/marked_root_binary_cubic.pdf");
const paper = (await exists(canonicalPaper)) ? canonicalPaper : currentPaper;
if (await exists(paper)) {
  await cp(paper, resolve(dist, "paper/one-map-three-descriptions.pdf"));
}

const book = resolve(repoRoot, "knowledge/_build/html");
if (await exists(book)) {
  await cp(book, resolve(dist, "book"), { recursive: true });
}

const source = resolve(repoRoot, "src/distinguished_root_map.tex");
if (await exists(source)) {
  await cp(source, resolve(dist, "paper/one-map-three-descriptions.tex"));
}

const transcript = resolve(repoRoot, "animations/transcript.md");
if (await exists(transcript)) {
  await cp(transcript, resolve(dist, "media/marked-root-explainer-transcript.md"));
}

const legalDocuments = new Map([
  ["LICENSE-CODE", "license-code.txt"],
  ["LICENSE-CONTENT", "license-content.txt"],
  ["THIRD_PARTY_NOTICES.md", "third-party-notices.md"],
]);
for (const [sourceName, targetName] of legalDocuments) {
  const legalSource = resolve(repoRoot, sourceName);
  if (await exists(legalSource)) {
    await cp(legalSource, resolve(dist, "legal", targetName));
  }
}
