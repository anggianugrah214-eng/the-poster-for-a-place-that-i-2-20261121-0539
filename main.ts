// Entry point for the-poster-for-a-place-that-i-2-20261121-0539.
//
// The repository holds the finished poster (entry.png, drawn in code by
// draw_image.py). This program copies it into the output directory as
// entry.png, so every run writes the same bytes. No network is used.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
// Fail loudly instead of shipping a truncated copy: the output must be
// byte for byte the image the repository holds.
if (statSync(src).size !== statSync(dst).size) {
  throw new Error("entry.png copy is incomplete");
}
