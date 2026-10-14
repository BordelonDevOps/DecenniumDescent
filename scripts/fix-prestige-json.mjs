import fs from "fs";

const p = new URL("../src/data/prestige-lorebook.json", import.meta.url);
let raw = fs.readFileSync(p, "utf8");

// Remove corrupted junk after valid Sapper object close
raw = raw.replace(
  /("combatRole": "Area control and anti-fortification disruptor\. Ideal in defensive sieges or narrow corridors\.")\s*\},\s*No one knows[\s\S]*?"\s*\},\s*\{\s*"num": 14,/,
  '$1\n  },\n  {\n    "num": 14,'
);

const cleanRole = (text) => {
  if (!text) return "";
  const markers = [
    " The Boom Prophet ",
    " The Choir Below ",
    " The Thunder Crowned ",
    " The Garden Wakes ",
    " Ink in the Veins ",
    " The Burned Banner ",
    " **Overview**:",
  ];
  let cut = text;
  for (const m of markers) {
    const i = cut.indexOf(m);
    if (i > 0) cut = cut.slice(0, i);
  }
  return cut.trim();
};

const data = JSON.parse(raw);
for (const entry of data) {
  if (entry.combatRole) entry.combatRole = cleanRole(entry.combatRole);
}
fs.writeFileSync(p, JSON.stringify(data, null, 2) + "\n");
console.log("Fixed", data.length, "prestige entries");
