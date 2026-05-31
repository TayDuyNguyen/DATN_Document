export const logger = {
  info(message: string, meta?: Record<string, unknown>) {
    log("INFO", message, meta);
  },
  warn(message: string, meta?: Record<string, unknown>) {
    log("WARN", message, meta);
  },
  error(message: string, meta?: Record<string, unknown>) {
    log("ERROR", message, meta);
  },
};

function log(level: "INFO" | "WARN" | "ERROR", message: string, meta?: Record<string, unknown>) {
  const payload = meta ? ` ${JSON.stringify(meta)}` : "";
  console.log(`[${new Date().toISOString()}] ${level} ${message}${payload}`);
}

