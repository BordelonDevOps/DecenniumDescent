import fs from "fs";
const text = fs.readFileSync("src/data/paladin-oaths.js", "utf8");

const mercyL13 = "Sanctify Ground — zone removes conditions each round";
const mercyL17 = "Grace Reversal — revive fallen ally if you fall to 0 HP";
console.log("Mercy L13 len:", mercyL13.length);
console.log("Mercy L17 len:", mercyL17.length);

const regex = /id: "([\w-]+)"[\s\S]*?revelationSpells: \[([\s\S]*?)\],\s*\n\s*oathbreaker/g;
let m;
const results = [];
while ((m = regex.exec(text)) !== null) {
  const id = m[1];
  const spells = m[2];
  const l13 = spells.match(/\{ level: 13, spell: "([^"]+)" \}/);
  const l17 = spells.match(/\{ level: 17, spell: "([^"]+)" \}/);
  const block = text.slice(m.index, m.index + 500);
  const isDraft = /draft: true/.test(block);
  if (l13) results.push({ id, level: 13, len: l13[1].length, spell: l13[1], draft: isDraft });
  if (l17) results.push({ id, level: 17, len: l17[1].length, spell: l17[1], draft: isDraft });
}
results.sort((a, b) => a.len - b.len);
console.log("\nAll L13/L17 sorted by length:");
results.forEach((r) => console.log(r.id, "L" + r.level, r.len, r.draft ? "(draft)" : "", "|", r.spell));

const giftRegex = /id: "([\w-]+)"[\s\S]*?finalOathGift:\s*\n?\s*"([^"]+)"/g;
const gifts = [];
while ((m = giftRegex.exec(text)) !== null) {
  gifts.push({ id: m[1], len: m[2].length, text: m[2] });
}
gifts.sort((a, b) => a.len - b.len);
console.log("\nfinalOathGift sorted by length:");
gifts.forEach((g) => console.log(g.id, g.len, "|", g.text));
