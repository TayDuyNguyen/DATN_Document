import fs from "node:fs";
import path from "node:path";

const rootDir = path.resolve(".");
const seedDir = path.resolve(rootDir, "..", "database-seeders");
const targetFiles = [
  "01_categories_subcategories.sql",
  "02_tags_amenities.sql",
  "03_tour_blog_categories.sql",
  "04_users.sql",
  "05_locations.sql",
  "06_tours.sql",
  "07_blog_posts.sql",
  "08_bookings_payments.sql",
  "09_ratings_interactions.sql",
  "10_system_tables.sql",
];

const report = [];

for (const file of targetFiles) {
  const filePath = path.join(seedDir, file);
  const before = fs.readFileSync(filePath, "utf8");
  const after = normalizeSeederContent(before);

  fs.writeFileSync(filePath, after, "utf8");

  report.push({
    file,
    beforeNonAscii: countNonAscii(before),
    afterNonAscii: countNonAscii(after),
    changed: before !== after,
  });
}

console.log(JSON.stringify(report, null, 2));

function normalizeSeederContent(content) {
  return content
    .split(/(\r?\n)/)
    .map((part) => {
      if (part === "\n" || part === "\r\n") {
        return part;
      }

      return toAsciiContent(repairMojibakeIfUseful(part));
    })
    .join("");
}

function repairMojibakeIfUseful(value) {
  if (!hasMojibakeSignal(value)) {
    return value;
  }

  const repaired = Buffer.from(value, "latin1").toString("utf8");

  return qualityScore(repaired) >= qualityScore(value) ? repaired : value;
}

function hasMojibakeSignal(value) {
  return /(?:Ã|Â|â|Ä|Æ|áº|á»|�)/.test(value);
}

function qualityScore(value) {
  const mojibakePenalty = (value.match(/(?:Ã|Â|â|Ä|Æ|áº|á»|�)/g) ?? []).length * 4;
  const controlPenalty = (value.match(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F-\u009F]/g) ?? []).length * 2;
  const vietnameseSignal = (value.match(/[ăâêôơưđĂÂÊÔƠƯĐáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]/g) ?? []).length;

  return vietnameseSignal - mojibakePenalty - controlPenalty;
}

function toAsciiContent(value) {
  return value
    .replace(/[đĐ]/g, (char) => (char === "Đ" ? "D" : "d"))
    .replace(/[‘’‚‛]/g, "'")
    .replace(/[“”„‟]/g, '"')
    .replace(/[–—]/g, "-")
    .replace(/…/g, "...")
    .replace(/™/g, "TM")
    .replace(/®/g, "(R)")
    .replace(/©/g, "(C)")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^\x00-\x7F]/g, "");
}

function countNonAscii(value) {
  return (value.match(/[^\x00-\x7F]/g) ?? []).length;
}
