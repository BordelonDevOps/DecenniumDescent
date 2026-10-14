import fs from 'fs';

const path = process.argv[2];
const data = JSON.parse(fs.readFileSync(path, 'utf8'));
const thin = [];
for (const p of data) {
  for (const h of p.hallmarks || []) {
    const name = h.split(':')[0]?.trim() || h.slice(0, 30);
    if (h.length < 80) {
      thin.push({ num: p.num, name: p.name, len: h.length, hallmark: h });
    }
  }
}
thin.sort((a, b) => a.len - b.len);
console.log(`Prestige hallmarks under 80 chars: ${thin.length}`);
thin.slice(0, 25).forEach((s) =>
  console.log(`${s.len}\t#${s.num} ${s.name}\t${s.hallmark}`)
);
