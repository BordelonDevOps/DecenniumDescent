// Read-only imported helper probes on synthetic data. No browser/storage access.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import * as rules from '../src/data/reputation.js';

const R=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const G=path.dirname(path.dirname(R));
const A=path.join(G,'docs/audit/2026-10-08/full-game');
const target=path.join(A,'REPUTATION_PRESERVATION_RUNTIME_PROBES.json');
if(fs.existsSync(target))throw new Error('Preserve earlier probe evidence');
const rows=[];
function probe(id,description,input,fn,expected){
  const before=structuredClone(input);
  const actual=fn(input);
  const unchanged=JSON.stringify(input)===JSON.stringify(before);
  const reproduced=JSON.stringify(actual)===JSON.stringify(expected);
  if(!unchanged||!reproduced)throw new Error(id+' unexpected probe result');
  rows.push({id,description,input:before,actual,expectedCurrentImplementation:expected,currentBehaviorReproduced:reproduced,syntheticInputObjectUnchanged:unchanged,ruleAcceptance:false});
}
probe('RP-P01','Normalization omits an unrecognized campaign faction key',{'war-veterans':2,'campaign-local-guild':5},rules.normalizeReputation,{'war-veterans':2});
probe('RP-P02','Normalization clamps source Loop endpoint scores to the runtime range',{'war-veterans':5,'opposing-forces':-5},rules.normalizeReputation,{'war-veterans':3,'opposing-forces':-3});
probe('RP-P03','Normalization rounds a numeric string',{'war-veterans':'1.7'},rules.normalizeReputation,{'war-veterans':2});
probe('RP-P04','Normalization replaces a malformed score with neutral',{'war-veterans':'unresolved'},rules.normalizeReputation,{'war-veterans':0});
probe('RP-P05','Background reapplication overwrites later standing and drops unknown keys',{'war-veterans':3,'opposing-forces':-2,'campaign-local-guild':2},x=>rules.applyBackgroundReputation(x,'Battlefield Medic'),{'war-veterans':1,'opposing-forces':0});
probe('RP-P06','Setter admits unknown key for one return value',{},x=>rules.setReputationScore(x,'campaign-local-guild',2),{'campaign-local-guild':2});
probe('RP-P07','The same setter result loses that key on later normalization',{},x=>rules.normalizeReputation(rules.setReputationScore(x,'campaign-local-guild',2)),{});
probe('RP-P08','Adjuster also admits an unknown key which later normalization drops',{},x=>rules.normalizeReputation(rules.adjustReputationScore(x,'campaign-local-guild',1)),{});
probe('RP-P09','Absent and explicit zero retain different normalized map shapes',{},x=>({absent:rules.normalizeReputation(x),zero:rules.normalizeReputation({'war-veterans':0})}),{absent:{},zero:{'war-veterans':0}});
probe('RP-P10','Compact entries omit an explicit neutral score',{'war-veterans':0},x=>rules.activeReputationEntries(x),[]);
probe('RP-P11','Qualitative label roundtrip loses the distinct value +3',{score:3},x=>rules.scoreFromTierLabel(rules.tierLabel(x.score)),2);
probe('RP-P12','Unknown background keeps known normalized standing but drops unknown faction keys',{'war-veterans':2,'campaign-local-guild':1},x=>rules.applyBackgroundReputation(x,'Synthetic Unrecognized Background'),{'war-veterans':2});
const protectedPaths=['src/data/reputation.js','src/lib/character-storage.js','src/components/ReputationPanel.tsx','src/components/CharacterBuilder.tsx','docs/mechanics/REPUTATION.md','docs/mechanics/GAMEPLAY_LOOP_CANON.md','data/playtest/ancestry_background_candidate.json'];
const sources=Object.fromEntries(protectedPaths.map(rel=>{const b=fs.readFileSync(path.join(R,rel));return ['DescentReviewChanges/ReviewBible/'+rel,{bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex')}];}));
const sourceModule=fs.readFileSync(path.join(R,'src/data/reputation.js'),'utf8');
if(/^\s*import\b/m.test(sourceModule))throw new Error('Unexpected helper dependency; inspect before reproduction');
const result={status:'observed-existing-behavior-not-rule-approval',scope:'12 calls to actual reputation helpers using synthetic in-memory records. No localStorage, browser character data, saved character or source mutation. No social/faction/cosmology rule is chosen.',extendsQuestion:'FL-23',probeCount:rows.length,probes:rows,sourceFiles:sources,factionDefinitionCount:rules.FACTIONS.length,backgroundMappingCount:Object.keys(rules.BACKGROUND_STARTING_REPUTATION).length,fullOriginalFactionRecords:rules.FACTIONS,fullOriginalBackgroundMappings:rules.BACKGROUND_STARTING_REPUTATION,meaningReview:'All original literal labels/descriptions retained as source data only. Faith, planar, prophecy and resonance-track meaning/powers remain deferred to the user-directed post-push cosmology review.',requiresJointDecision:true,submitted:false,savedCharactersRead:0,savedCharactersWritten:0,sourceFilesModified:0};
fs.writeFileSync(target,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({probeCount:rows.length,factionDefinitionCount:rules.FACTIONS.length,backgroundMappingCount:Object.keys(rules.BACKGROUND_STARTING_REPUTATION).length,savedCharactersRead:0,savedCharactersWritten:0}));
