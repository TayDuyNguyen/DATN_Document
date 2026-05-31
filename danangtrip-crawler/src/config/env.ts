import "dotenv/config";
import { z } from "zod";

const envSchema = z.object({
  NODE_ENV: z.string().default("development"),
  GOOGLE_PLACES_API_KEY: z.string().optional(),
  PEXELS_API_KEY: z.string().optional(),
  PEXELS_API_URL: z.string().default("https://api.pexels.com/v1/search"),
  PEXELS_ENRICH_LIMIT: z.coerce.number().int().positive().default(80),
  PEXELS_PHOTOS_PER_ITEM: z.coerce.number().int().positive().max(5).default(3),
  UNSPLASH_ACCESS_KEY: z.string().optional(),
  DATABASE_URL: z.string().optional(),
  CRAWLER_OUTPUT_FILE: z.string().default("data/crawl-items.json"),
  CRAWLER_USER_AGENT: z.string().default("DanangTripCrawler/0.1 contact:admin@danangtrip.local"),
  OVERPASS_API_URL: z.string().default("https://overpass-api.de/api/interpreter"),
});

export const env = envSchema.parse(process.env);
