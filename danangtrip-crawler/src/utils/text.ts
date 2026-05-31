const vietnameseCharMap: Record<string, string> = {
  đ: "d",
  Đ: "D",
};

export function toAsciiText(value: string): string {
  return value
    .replace(/[đĐ]/g, (char) => vietnameseCharMap[char] ?? char)
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^\x00-\x7F]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

