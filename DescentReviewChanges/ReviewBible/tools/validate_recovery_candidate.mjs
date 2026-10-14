import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {extractionDc} from '../src/lib/gameplay-loop.ts';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const data=read('data/public/Decennium_Descent_Gameplay_Loop_v1_2.json');
assert.deepEqual(data,read('src/data/gameplay-loop.json'),'Public/runtime procedures diverged');
const ex=data.extraction,h=ex.handlingModifiers;
assert.deepEqual(h.capAppliesTo,['highestExtractionClass','attentionExposed','burdened','unsecuredDangerousLots']);
assert.deepEqual(h.outsideCap,['pursued','securedRoute']);
assert.deepEqual(h.unsecuredDangerousLot.tags,['Volatile','Cursed','Living']);

// Hand-worked boundary cases from the prose. These catch cap placement, not just field presence.
const cases=[
 [{tierDc:12},12],
 [{tierDc:12,highestExtractionClass:6},18],
 [{tierDc:12,highestExtractionClass:6,attentionExposed:true,burdened:true,unsecuredDangerousLots:3},19],
 [{tierDc:12,highestExtractionClass:6,attentionExposed:true,burdened:true,unsecuredDangerousLots:3,pursued:true},21],
 [{tierDc:12,highestExtractionClass:6,attentionExposed:true,burdened:true,unsecuredDangerousLots:3,securedRoute:true},17],
 [{tierDc:12,highestExtractionClass:6,attentionExposed:true,burdened:true,unsecuredDangerousLots:3,pursued:true,securedRoute:true},19],
 [{tierDc:12,unsecuredDangerousLots:9},15],
 [{tierDc:12,securedRoute:true},10],
];
for(const [input,expected] of cases)assert.equal(extractionDc(input),expected,JSON.stringify(input));
let combinations=0;
for(let ec=0;ec<=6;ec++)for(const attention of [false,true])for(const burdened of [false,true])for(let lots=0;lots<=5;lots++)for(const pursued of [false,true])for(const secured of [false,true]){
 const parts=[ex.cargoDcModifierByHighestClass[String(ec)],attention?h.attentionExposed:0,burdened?h.burdened:0,Math.min(lots*h.unsecuredDangerousLot.perLot,h.unsecuredDangerousLot.maximum)];
 const expected=12+Math.min(ex.cargoModifierCap,parts.reduce((a,b)=>a+b,0))+(pursued?h.pursued:0)+(secured?h.securedRoute:0);
 assert.equal(extractionDc({tierDc:12,highestExtractionClass:ec,attentionExposed:attention,burdened,unsecuredDangerousLots:lots,pursued,securedRoute:secured}),expected);
 combinations++;
}
console.log(`PASS extraction: ${cases.length} hand-worked cases, ${combinations} JSON/helper combinations; public/runtime identical.`);
