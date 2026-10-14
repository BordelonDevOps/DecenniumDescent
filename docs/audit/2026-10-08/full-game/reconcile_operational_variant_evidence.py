"""Index existing dispositions; never change source access, spell effects or retirement."""
import json,hashlib
from pathlib import Path
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
cat=read(R/'data/public/spell_playtests/catalog.json')['spells'];by={s['id']:s for s in cat}
assert sum(bool(s['operational']) for s in cat)==210
vpath=R/'docs/mechanics/SPELL_VARIANT_REVIEW_STATUS.json';v=read(vpath)
rows=[]
for s in cat:
    if not s['operational']:continue
    for placement in s['source']['original']['placements']:
        if any(a['school']==placement['school'] and a['rank']==placement['level'] for a in s['classAccess'].values()):continue
        rows.append({'id':s['id'],'school':placement['school'],'rank':placement['level'],'placement':placement,
            'coreEntries':[c for c in s['source']['coreEntries'] if c['original']['school']==placement['school'] and c['original']['level']==placement['level']],
            'operationalDesignNotes':s['operational']['designNotes'],'operationalLimitations':s['operational']['limitations'],
            'classAccess':s['classAccess']})
assert len(rows)==6
definitions={
 'resonance-shield':{
  'status':'PRESERVED / INACTIVE ALTERNATIVES — existing provisional single-ID effect selected; historical reconciliation not declared complete',
  'sourceCoreIndex':38,
  'currentOperationalAlternative':'Actual class access is rank0; current reviewed rule is class rank cost plus mandatory1RP for1d4 temporary HP. Rank2 catalog5-per-RP and Core2-per-RP alternatives remain evidence, not optional upgrades.',
  'evidence':['docs/audit/2026-10-08/spell-integration/GPT_SPELL_ADVERSARIAL_REVIEW.md','docs/audit/2026-10-08/spell-integration/REVIEW_DISPOSITION.md','docs/audit/2026-10-08/spell-integration/GPT_SPELL_CLOSURE_AND_FALLING_PROPOSAL.md'],
  'remainingDecision':'Existing operational choice is reviewed. Historical rank2 effect conflict remains expressly provisional; any future access or alternate identity requires a separate decision.'},
 'warding-bond':{
  'status':'PRESERVED / INACTIVE DUPLICATE — prior exact review selects rank1 access',
  'sourceCoreIndex':35,
  'currentOperationalAlternative':'Rank1 ordinary spell with reviewed damage sharing; identical-effect rank2 source is evidence only. No rank2 upgrade or duplicate learnable choice.',
  'evidence':['docs/audit/2026-10-08/full-game/GPT_ABJURATION_RANK1_SOURCE_CONFERENCE.md','docs/audit/2026-10-08/full-game/GPT_ABJURATION_RANK1_EXACT_REVIEW.md'],
  'remainingDecision':'No new mechanical decision introduced by the structural access audit. Preserve the prior duplicate disposition; source retention is required and retirement/deletion is not authorized by this evidence index.'},
 'arcane-lock':{
  'status':'PRESERVED / UNASSIGNED — current unified manuscript does not grant Universal rank2 access',
  'sourceCoreIndex':869,
  'currentOperationalAlternative':'Reviewed starter mechanic uses existing Universal rank1 and Abjuration rank2 class access. All three placements remain source evidence. Its card explicitly defers source rank/RP disagreements to external access.',
  'evidence':['DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_3.json','docs/audit/2026-10-08/spell-integration/CODEX_SPELL_REVIEW_PACKET.json','docs/audit/2026-10-08/spell-integration/REVIEW_DISPOSITION.md','docs/audit/2026-10-08/spell-integration/GPT_SPELL_CLOSURE_AND_FALLING_PROPOSAL.md'],
  'remainingDecision':'No separate rank2 Universal disposition was established by this bounded evidence pass. Preserve the unassigned placement; do not infer a second option, retirement or deletion from the unified effect.'},
 'mirror-image':{
  'status':'PRESERVED / UNASSIGNED — starter manuscript reconciles targeting/duration, not a new rank2 access grant',
  'sourceCoreIndex':556,
  'currentOperationalAlternative':'Actual class access rank1. Existing starter uses Self, three duplicates and concentration up to1minute, explicitly reconciling the source range/duration conflict. Rank2 placement remains preserved.',
  'evidence':['DescentReviewChanges/ReviewBible/data/playtest/spell_drafts/batch_2.json','docs/audit/2026-10-08/spell-integration/CODEX_SPELL_REVIEW_PACKET.json','docs/audit/2026-10-08/spell-integration/REVIEW_DISPOSITION.md','docs/audit/2026-10-08/spell-integration/GPT_SPELL_CLOSURE_AND_FALLING_PROPOSAL.md'],
  'remainingDecision':'Current unified mechanics do not establish a separate rank2 mode or its retirement. Keep the access/variant disposition explicit during the Illusion pass.'}
}
curated={(x['id'],x['school'],x['rank']):x for x in v['variants']}
for row in rows:
    key=(row['id'],row['school'],row['rank'])
    if row['id'] in definitions:
        d=definitions[row['id']]
        entry={'id':row['id'],'school':row['school'],'rank':row['rank'],**d,'sourceEffect':row['coreEntries'][0]['original']['effect']}
        if key not in curated:v['variants'].append(entry)
        else:assert curated[key]==entry,'Do not overwrite a newer curated decision'
        row['existingDisposition']=entry
    else:
        assert key in curated
        row['existingDisposition']=curated[key]
    row['evidenceHashes']=[{'path':p,'sha256':sha(G/p)} for p in row['existingDisposition']['evidence']]
result={'status':'EVIDENCE INDEX COMPLETE FOR SIX OPERATIONAL IDENTITIES WITH UNASSIGNED PLACEMENTS','snapshotOperationalIdentities':210,
 'scope':'Indexes prior manuscript/source decisions. Not a new rules approval, access grant, retirement or source-deletion decision. Thirty structurally unassigned placements do not equal thirty wholly unreviewed mechanics.',
 'operationalAndSourceDataChanged':False,'wholeCatalogClosed':False,'records':rows}
out=A/'OPERATIONAL_UNASSIGNED_VARIANT_EVIDENCE_210.json';assert not out.exists();dump(out,result)
v['operationalUnassignedEvidenceAudit']={'evidence':'docs/audit/2026-10-08/full-game/OPERATIONAL_UNASSIGNED_VARIANT_EVIDENCE_210.json','snapshotOperationalIdentities':210,'placements':6,'scope':result['scope']}
dump(vpath,v)
print(json.dumps({'evidenceIndexed':len(rows),'curatedVariantEntries':len(v['variants']),'sourceChanged':False,'mechanicsChanged':False,'wholeCatalogClosed':False}))
