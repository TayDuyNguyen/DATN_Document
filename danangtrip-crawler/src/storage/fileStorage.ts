import { mkdir, writeFile } from "node:fs/promises";
import { dirname } from "node:path";
import type { NormalizedCrawlItem } from "../contracts/crawler.js";

export async function writeItemsToJsonFile(filePath: string, items: NormalizedCrawlItem[]) {
  await mkdir(dirname(filePath), { recursive: true });
  await writeFile(filePath, `${JSON.stringify(items, null, 2)}\n`, "utf8");
}

