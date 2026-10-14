import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { songDice,canSelectBardFeature,startBardPerformance,beginBardTurn,breakBardRhythm,copiedEchoAmount,shortenBardRecharge } from '../src/lib/bard-playtest.ts';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const draft=JSON.parse(fs.readFileSync(path.join(root,'data/public/Decennium_Descent_Bard_Playtest_v0_1.json'),'utf8'));
const cards=draft.cards;
const sourceLines=fs.readFileSync(path.resolve(root,'../../docs/reference/Player_Rulebook_v6_source_text.txt'),'utf8').split(/\r?\n/);
const byName=n=>cards.find(c=>c.name===n);
assert.equal(cards.length,50);
assert.equal(new Set(cards.map(c=>c.id)).size,50);
const required=['id','name','band','kind','minimumClassLevel','acquisition','activation','target','duration','resolution','effect','crescendoRider','source','scaling','resourceCost','recharge'];
for(const card of cards){
  for(const field of required)assert.ok(card[field]!==undefined && card[field]!==null && card[field]!=='',`${card.name}: missing ${field}`);
  assert.ok(card.source.originalText.includes(card.name),`${card.name}: missing source`);
  assert.equal(card.source.originalText,sourceLines[card.source.line-1],`${card.name}: source text altered`);
  assert.ok(Number.isInteger(card.resourceCost.rp)&&card.resourceCost.rp>=0);
  assert.ok(Number.isInteger(card.recharge.rounds)&&card.recharge.rounds>=0);
  if(card.echoEligible)assert.ok(!card.tags.includes('echo')&&!card.tags.includes('finale'));
}
assert.equal(cards.filter(c=>c.band==='Base').length,10);
assert.equal(cards.filter(c=>c.band==='Arch').length,10);
for(const hero of draft.heroPaths)assert.equal(cards.filter(c=>c.path===hero).length,10);
assert.equal(cards.filter(c=>c.band==='Base'&&c.kind==='passive').length,6);
assert.equal(byName('Encore').recharge.shortRestUses,1);
assert.ok(cards.filter(c=>c.kind==='passive').every(c=>!c.tags.includes('performance')));
assert.ok(cards.filter(c=>c.tags.includes('sustained')).every(c=>c.resourceCost.maintenanceRp>0));

// Walk the owner's worked example, checking actual eligibility, duplicates and automatic grants.
const known=new Set();
for(const step of draft.schedule){
 assert.equal(step.example.length,step.choose);
 let actives=0;
 for(const id of step.example){
  const card=cards.find(c=>c.id===id);assert.ok(card);
  assert.ok(canSelectBardFeature(card,step.classLevel,'Harmony',known,step.bands),`${step.classLevel}: illegal ${card.name}`);
  known.add(id);if(card.kind==='active')actives++;
 }
 assert.ok(actives>=step.minimumActives);
 for(const card of cards.filter(c=>c.acquisition==='automatic'&&c.minimumClassLevel===step.classLevel&&(c.path===null||c.path==='Harmony')))known.add(card.id);
}
assert.equal(known.size,27);
assert.equal(draft.schedule.filter(s=>s.asiOrFeat).length,5);
assert.ok(!canSelectBardFeature(byName('Healing Harmony'),1,'Harmony',new Set(),['Hero']),'Wizard19/Bard1 cannot get Hero abilities');
assert.ok(!canSelectBardFeature(byName('Grand Performance'),20,'Virtuoso',new Set(),['Hero']),'Finales cannot be ordinary selections');
assert.ok(!canSelectBardFeature(byName('Verse of Agony'),20,'Harmony',new Set(),['Hero']),'Hero paths cannot leak');
assert.ok(!canSelectBardFeature(byName('Symphony of Serenity'),10,'Harmony',new Set(),['Hero']),'Symphonies gated at16');

// Different selection orders must remain completable for every path; the printed Harmony example is not the only legal build.
let checkedBuilds=0;
for(const hero of draft.heroPaths)for(let seed=1;seed<=100;seed++){
 let random=seed;const next=()=>((random=(random*1664525+1013904223)>>>0)/4294967296);
 const picked=new Set();
 for(const step of draft.schedule){
  for(let slot=0;slot<step.choose;slot++){
   let options=cards.filter(c=>canSelectBardFeature(c,step.classLevel,hero,picked,step.bands));
   if(slot<step.minimumActives)options=options.filter(c=>c.kind==='active');
   assert.ok(options.length,`${hero} seed${seed} has no choice at level${step.classLevel}`);
   picked.add(options[Math.floor(next()*options.length)].id);
  }
 }
 checkedBuilds++;
}

assert.deepEqual([1,4,5,10,11,16,17,20].map(songDice),[1,1,2,2,3,3,4,4]);
const initial={crescendo:0,lastPerformance:null,gainedThisTurn:0,rp:20,dissonance:4};
const verse=byName('Verse of Courage'),note=byName('Dissonant Note'),echo=byName('Echo of Inspiration');
let state=startBardPerformance(initial,verse).state;
assert.equal(state.crescendo,1);
state=startBardPerformance(state,echo).state;
assert.equal(state.crescendo,1,'Bonus Action cannot grant another normal stack');
state=startBardPerformance(beginBardTurn(state),verse).state;
assert.equal(state.crescendo,2);
state=startBardPerformance(beginBardTurn(state),verse).state;
assert.equal(state.crescendo,2,'Repeating the same last performance gains nothing');
// External spells never call the helper and therefore cannot erase lastPerformance.
assert.equal(state.lastPerformance,verse.id);
let atFive={...initial,crescendo:5,rp:0};
assert.throws(()=>startBardPerformance(atFive,echo),/Insufficient RP/);
assert.equal(atFive.crescendo,5,'Failed payment cannot vent or consume');
const consumed=startBardPerformance({...atFive,rp:1},echo);
assert.equal(consumed.spent,5);assert.equal(consumed.state.crescendo,0);assert.equal(consumed.state.dissonance,2);assert.equal(consumed.state.rp,0);
assert.equal(consumed.state.gainedThisTurn,0,'Consumption gives no replacement stack');
assert.equal(startBardPerformance({...initial,crescendo:5,dissonance:1},verse).state.dissonance,0,'Vent cannot make Dissonance negative');
const explicitFive=startBardPerformance({...initial,crescendo:5},byName('Chorus of Renewal'));
assert.equal(explicitFive.spent,5);assert.equal(explicitFive.state.rp,12);assert.equal(explicitFive.state.dissonance,2);
const partial=startBardPerformance({...initial,crescendo:3},byName('Harmonic Convergence'));
assert.equal(partial.spent,3);assert.equal(partial.state.dissonance,4,'Only five-stack expenditure vents');
assert.throws(()=>startBardPerformance({...initial,crescendo:2},byName('Harmonic Convergence')),/Insufficient Crescendo/);
const quick=startBardPerformance(initial,verse,{accelerated:true}).state;
assert.equal(quick.crescendo,2);
assert.equal(startBardPerformance(quick,note,{accelerated:true}).state.crescendo,2,'Accelerators share a turn cap');
assert.equal(breakBardRhythm({...initial,crescendo:4},'damage',true).crescendo,4);
assert.equal(breakBardRhythm({...initial,crescendo:4},'concentration',true).crescendo,0);
assert.equal(breakBardRhythm({...initial,crescendo:4},'silence',true).crescendo,0);
const end=breakBardRhythm({...initial,crescendo:4},'encounter-end');
assert.equal(end.rp,20);assert.equal(end.dissonance,4);

// Adversarial tiny-die case: minimum-one rounding must not exceed the original via multiple portions.
assert.equal(copiedEchoAmount(1,[.5,.25,.25]),1);
assert.equal(copiedEchoAmount(7,[.5,.25]),5);
assert.equal(copiedEchoAmount(7,[.75,.25,.25]),7);
assert.equal(copiedEchoAmount(0,[.5]),0);
assert.throws(()=>copiedEchoAmount(10,[-.5]),/Invalid/);
assert.throws(()=>copiedEchoAmount(1.5,[.5]),/Invalid/);
const shortened=shortenBardRecharge(3,false,1);
assert.equal(shortened.counter,2);
assert.equal(shortenBardRecharge(shortened.counter,shortened.resetUsed,'reset').counter,2,'Reset chains cannot bypass round limit');
assert.deepEqual(shortenBardRecharge(0,false,'reset'),{counter:0,resetUsed:false},'An ineligible reset does not consume its use');

const authoritative=JSON.parse(fs.readFileSync(path.resolve(root,'../../data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json'),'utf8'));
assert.deepEqual(draft.rpByClassLevel,authoritative.caster_pools.Bard);
assert.deepEqual(draft.spellRankRpCosts,authoritative.resonance_costs);
const result={status:'PASS',cards:50,workedExampleFeatures:27,levelSchedules:draft.schedule.length,randomLegalProgressions:checkedBuilds,coverage:['schema/source mapping','all Hero acquisition routes','multiclass and capstone gates','Crescendo gain/spend/payment','interruption','Echo fraction/rounding cap','recharge reset guard','Core V2 RP parity'],limits:'Reference-rule checks only. No combat balance simulation, full effect engine or human playtest.'};
fs.writeFileSync(path.join(root,'docs/mechanics/BARD_PLAYTEST_VALIDATION.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
