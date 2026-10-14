/**
 * Re-parse crafting workbook → crafting-recipes.json.
 * Delegates to fill-crafting-components.mjs (quantity parse, Aethel remaps, needsReview).
 *
 * Usage: node scripts/reparse-crafting.mjs
 */
import { spawnSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const fill = path.join(__dirname, "fill-crafting-components.mjs");
const result = spawnSync(process.execPath, [fill], { stdio: "inherit" });
process.exit(result.status ?? 1);
