import fs from 'fs';

const path = process.argv[2];
const content = fs.readFileSync(path, 'utf8');
const re = /d\("([^"]+)"\)/g;
const all = [];
let match;
while ((match = re.exec(content)) !== null) {
  const text = match[1];
  const lineNum = content.slice(0, match.index).split('\n').length;
  all.push({ line: lineNum, len: text.length, text });
}
all.sort((a, b) => a.len - b.len);
console.log(`File: ${path}`);
console.log(`Found ${all.length} d() entries`);
console.log('\nThinnest (<60 chars):');
all.filter((s) => s.len < 60).forEach((s) => console.log(`${s.len}\tL${s.line}\t${s.text}`));
console.log('\n60-79 chars (borderline):');
all.filter((s) => s.len >= 60 && s.len < 80).slice(0, 15).forEach((s) => console.log(`${s.len}\tL${s.line}\t${s.text}`));
