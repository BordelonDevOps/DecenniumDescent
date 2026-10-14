"""Preserve exact named runtime candidates without treating them as approved summons."""
from pathlib import Path
import hashlib
import json

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
base=A/'ILLUSION_NECROMANCY_RANK6_SOURCE_PREPARATION.json';basehash=sha(base)
paths=[R/'data/director/bestiary_source_candidate_internal.json',R/'data/playtest/bestiary_public_source_candidate.json',G/'src/bestiary_data_full.json',G/'src/bestiary_data.json']
protected={str(p.relative_to(G)).replace('\\','/'):sha(p) for p in paths+[base]}
names=['Ghoul','Ghast','Wight','Mummy','Soul Wraith','Wraith']
search=[];records=[]
for p in paths:
    d=read(p);rows=d['records'] if isinstance(d,dict) else d
    matches={n:[{'index':i,'record':r} for i,r in enumerate(rows) if r['name'].casefold()==n.casefold()] for n in names}
    search.append({'file':str(p.relative_to(G)).replace('\\','/'),'sha256':sha(p),'searchedRecords':len(rows),'exactCaseInsensitiveNameMatches':{n:[x['index'] for x in v] for n,v in matches.items()}})
    for n,found in matches.items():
        for x in found:records.append({'searchedName':n,'file':str(p.relative_to(G)).replace('\\','/'),'index':x['index'],'fullOriginalRecord':x['record'],'scope':'Unreviewed source comparison only; no automatic summoning,creation,CR,control or public-projection approval.'})
runtime=[r for r in records if r['file']=='src/bestiary_data_full.json']
assert len(runtime)==5 and {r['searchedName'] for r in runtime}=={'Ghoul','Ghast','Wight','Mummy','Wraith'}
assert len(records)==5
assert next(r['fullOriginalRecord'] for r in runtime if r['searchedName']=='Ghast')['type']=='Fey'
checks=[{'name':'Exact named search over67 internal dossiers,26 public dossiers,707 current runtime rows and50 alternate rows','pass':True},
        {'name':'All five matched runtime records retained complete and byte-source bound','pass':all(read(G/r['file'])[r['index']]==r['fullOriginalRecord'] for r in records)},
        {'name':'Original13-spell source preparation remains unchanged','pass':sha(base)==basehash},
        {'name':'All five protected files unchanged','pass':all(sha(G/n)==h for n,h in protected.items())}]
assert all(c['pass'] for c in checks)
data={'status':'PREPARED NOT SENT; unresolved named-creature evidence','spellIds':['create-undead','command-undeath','summon-soul-wraith'],'basePreparation':base.name,'basePreparationSha256':basehash,'searches':search,'completeMatches':records,
      'questions':['Create Undead names all four Ghoul/Ghast/Wight/Mummy forms, but none has an exact-name dossier in the current67-record source candidate. Resolve the intended profiles jointly; do not silently substitute generic minions or an external game.',
                   'The707-row runtime includes Ghoul Large Undead CR1 HP52 AC13; Ghast Gargantuan Fey CR23 HP918 AC20; Wight Large Undead CR17 HP416 AC19; Mummy Gargantuan Undead CR20 HP805 AC19. Ghast\'s Fey type conflicts with treating that runtime identity as an undead outcome. These facts require adjudication,not a guessed correction.',
                   'Command Undeath explicitly says up to2 CR2 undead. None of these four matched runtime candidates is exactly CR2. Decide the spell\'s exact rank predicate from its source; do not use this list to silently change the cap or infer intended eligibility.',
                   'No exact Soul Wraith name occurs in these four registries. Ordinary Wraith exists only in the707-row runtime and is Gargantuan Undead CR25 HP992 AC21, unlike the spell\'s HP100/AC18. Preserve it as a non-identical comparison; neither name similarity nor the spell title authorizes merging them.'],
      'checks':checks,'protectedFiles':protected,'sourceInformationDeleted':0,'spellsApproved':0,'cosmology':'No cosmology reviewed; historical descriptions are retained without adjudication','dispatchInstruction':'Rebase and send this complete addendum with the rank-six Illusion/Necromancy source packet; all missing or conflicting creature profiles require explicit source reconciliation before candidate authorship.'}
out=A/'RANK6_UNDEAD_PROFILE_SOURCE_ADDENDUM.json';assert not out.exists();out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md='# Rank-six undead spell profile dependencies\n\nPrepared evidence only; no spell or creature is approved. The [complete source addendum](RANK6_UNDEAD_PROFILE_SOURCE_ADDENDUM.json) retains every matched original and records the exact searches.\n\n| Runtime name | Type | Size | CR | HP / AC |\n|---|---|---|---|---|\n'
for rec in runtime:
    r=rec['fullOriginalRecord'];md+=f"| {r['name']} | {r['type']} | {r['size']} | {r['challengeRating']} | {r['hitPoints']} / {r['armorClass']} |\n"
md+='\n'+'\n\n'.join(data['questions'])+'\n\nAll four registries and the prepared13-spell packet remain unchanged. This is a bounded search of these registries, not proof that no historical source exists elsewhere. Carry the addendum into the source conference; no profile is silently imported or rewritten.\n'
(A/'RANK6_UNDEAD_PROFILE_SOURCE_ADDENDUM.md').write_text(md,encoding='utf-8')
print(json.dumps({'status':'PASS preserved named-profile dependency evidence','completeRuntimeRecords':5,'sourceRegistries':4,'checks':len(checks),'protectedFiles':len(protected),'spellsApproved':0}))
