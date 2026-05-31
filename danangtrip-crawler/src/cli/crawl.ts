import { env } from "../config/env.js";
import { normalizeLocationItems } from "../pipelines/locationPipeline.js";
import { CuratedDanangLocationsSource } from "../sources/curatedDanangLocationsSource.js";
import { MockPlacesSource } from "../sources/mockPlacesSource.js";
import { OverpassDanangPoisSource } from "../sources/overpassDanangPoisSource.js";
import { writeItemsToJsonFile } from "../storage/fileStorage.js";
import { logger } from "../utils/logger.js";

async function main() {
  const sourceArg = getArgValue("--source") ?? "mock-places";
  const outputFile = getArgValue("--output") ?? env.CRAWLER_OUTPUT_FILE;

  const source = createSource(sourceArg);

  logger.info("Starting crawl job", {
    source: source.name,
    type: source.type,
  });

  const rawItems = await source.crawl();
  logger.info("Raw items collected", { count: rawItems.length });

  const normalizedItems = normalizeLocationItems(rawItems);
  logger.info("Items normalized", { count: normalizedItems.length });

  await writeItemsToJsonFile(outputFile, normalizedItems);
  logger.info("Crawl output written", { file: outputFile });
}

function createSource(sourceName: string) {
  if (sourceName === "mock-places") {
    return new MockPlacesSource();
  }

  if (sourceName === "curated-danang-locations") {
    return new CuratedDanangLocationsSource();
  }

  if (sourceName === "overpass-danang-pois") {
    return new OverpassDanangPoisSource();
  }

  throw new Error(`Unsupported source "${sourceName}".`);
}

function getArgValue(name: string): string | undefined {
  const prefix = `${name}=`;
  const arg = process.argv.find((value) => value.startsWith(prefix));
  return arg?.slice(prefix.length);
}

main().catch((error) => {
  logger.error("Crawl job failed", {
    message: error instanceof Error ? error.message : String(error),
  });
  process.exitCode = 1;
});
