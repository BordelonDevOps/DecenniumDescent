import { BASE_DRUID_FORMS, ARCH_DRUID_FORMS, HERO_FORMS_BY_CIRCLE } from '../src/data/druid-shapeshifting.js';

function scanForms(forms, label) {
  const lines = [];
  for (const form of forms) {
    for (const trait of form.traits || []) {
      lines.push({ label, form: form.name, trait, len: trait.length });
    }
  }
  return lines;
}

const baseLines = scanForms(BASE_DRUID_FORMS, 'base');
const archLines = scanForms(ARCH_DRUID_FORMS, 'arch');
const heroLines = [];
for (const data of Object.values(HERO_FORMS_BY_CIRCLE)) {
  for (const form of data.forms || []) {
    for (const trait of form.traits || []) {
      heroLines.push({ label: 'hero', form: form.name, trait, len: trait.length });
    }
  }
}

for (const [name, lines] of [['BASE', baseLines], ['ARCH', archLines], ['HERO', heroLines]]) {
  const under = lines.filter((l) => l.len < 60).sort((a, b) => a.len - b.len);
  console.log(`${name} total: ${lines.length} under60: ${under.length}`);
  for (const l of under) {
    console.log(`  ${l.len}\t${l.form}\t${l.trait}`);
  }
}
