import { HERO_FORMS_BY_CIRCLE } from '../src/data/druid-shapeshifting.js';

const lines = [];
for (const [circleId, data] of Object.entries(HERO_FORMS_BY_CIRCLE)) {
  for (const form of data.forms) {
    for (const trait of form.traits) {
      lines.push({
        circle: data.circle,
        circleId,
        form: form.name,
        trait,
        len: trait.length,
      });
    }
  }
}

const under60 = lines.filter((l) => l.len < 60).sort((a, b) => a.len - b.len);
console.log('Total hero traits:', lines.length);
console.log('Under 60 chars:', under60.length);
console.log('\nShortest first:');
for (const l of under60) {
  console.log(`${l.len}\t${l.circle}\t${l.form}\t${l.trait}`);
}
