import fs from 'fs';

const path = process.argv[2];
const content = fs.readFileSync(path, 'utf8');
const re = /:\s*['"]([^'"]{10,59})['"]/g;
const all = [];
let match;
while ((match = re.exec(content)) !== null) {
  const text = match[1];
  if (!/^[a-z0-9_-]+$/.test(text) && !/^\d+$/.test(text)) {
    const lineNum = content.slice(0, match.index).split('\n').length;
    all.push({ line: lineNum, len: text.length, text });
  }
}
all.sort((a, b) => a.len - b.len);
console.log(`File: ${path}`);
console.log(`Found ${all.length} strings 10-59 chars`);
all.slice(0, 40).forEach((s) => console.log(`${s.len}\tL${s.line}\t${s.text}`));
