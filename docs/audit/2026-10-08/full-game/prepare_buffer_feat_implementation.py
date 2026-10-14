"""Preserve candidate overlay and actual first implementation review packet."""
from pathlib import Path
import hashlib
import json

GAME=Path('C:/Github/DecenniumDescent')
ROOT=GAME/'DescentReviewChanges/ReviewBible'
AUDIT=Path(__file__).resolve().parent
source=json.loads((AUDIT/'BUFFER_FEAT_COMPLETION_SOURCES.json').read_text(encoding='utf-8'))
guide=(ROOT/'docs/mechanics/BUFFER_FEAT_PLAYTEST.md').read_text(encoding='utf-8')
heads={r['id']:r['sourceObject']['name'] for r in source['records']}
sections={}
for section in guide.split('\n## ')[1:]:
    for id,name in heads.items():
        if section.startswith(name+' —') or (id=='soul_cage' and section.startswith('Soul Cage feat —')):
            sections[id]='## '+section.strip()+'\n'
assert len(sections)==8,sections.keys()
candidate={'status':'SOURCE-DISCUSSED / RECONCILED CANDIDATE — independent implementation review pending',
           'sourcePath':source['sourcePath'],'sourceFileSha256':source['sourceFileSha256'],
           'guide':'docs/mechanics/BUFFER_FEAT_PLAYTEST.md','originalRegistryCount':335,
           'reviewEvidence':['GPT_BUFFER_FEAT_FIRST_REVIEW.md','GPT_BUFFER_FEAT_BOUNDARIES.md','GPT_BUFFER_FEAT_FINAL_BRIDGES.md'],
           'feats':[dict(id=r['id'],name=r['sourceObject']['name'],sourceObject=r['sourceObject'],
                    sourceObjectSha256=r['sourceObjectSha256'],repeatability='nonrepeatable',
                    acquisition='Actual class feat selection; source-specific prerequisite at acquisition',
                    operationalRules=sections[r['id']]) for r in source['records']]}
dest=ROOT/'data/playtest/feat_drafts/candidate_buffers.json'
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(json.dumps(candidate,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
packet=AUDIT/'CODEX_BUFFER_FEAT_IMPLEMENTATION.md'
assert not packet.exists(),'Do not overwrite an already submitted implementation packet'
parts=['''# Eight full feats: actual implementation review

Please independently audit the actual attached candidate guide, reference adapter, adversarial test code and immutable-source evidence. Your first full drafts,15 dependency decisions and five final bridges are incorporated. No feat is promoted; all335 original feat objects are unchanged. The five ordinary spells remain separately reviewed (83/765 catalog) and are not reopened.

Current local checks:131 targeted +2,520 independent healing-budget boundary cases pass. These establish bounded consistency, not numerical balance or a full runtime. All source access, genuine hostile/soul status, geometry, canonical clocks, current item possession, actual damage provenance and actual rest/turn/death/source-root identities are external authoritative host inputs, consistent with earlier packages. Helper certificates do not create those permissions.

Review specifically:
1. Does every printed clause of all eight source objects now have complete, consistent operational text, preserved identity/prerequisite and explicit NEW bridges?
2. Chef: actual ingredient transaction, later PB changes, successful LR finalization, consumption IDs, cross-Chef recipient limit and potency/rest clocks; recipe independence.
3. Inspiring Leader/Blood: snapshots, continuously present selected others, individual vs owner interruption, rejected offers, independent blood save advantage, exact rest ties.
4. Summons/Medic: multi-body lineage versus reissue, actual source costs and shared clocks; dying episode owner identity, real kit use, actual transition before independent background1HP.
5. Necrotic Affinity: unchanged old absorption API, once-actual-turn die, broad personal necrotic fatal-root seal and exact death-instance/rank5 behavior.
6. Lifeleech: zero initial reserve, no level refill, predesignated spell-root/window target, actual damage and anti-farming, two-pass conditional addons, post-reduction finite funding, Critical/excess distinction, no copied/incidental resource-trigger loop.
7. Soul charges/crystal: one owner pool, eligible decline/full-cap body entitlement, ineligible event no rescan, actual sources/souls, crystal transfer no charge transfer, no Soul Bind/whole-soul prestige equivalence.
8. Soul Cage: pay-before-resolution, exact3d8/CONhalf and independent one-family half-heal suppression, refresh/expiry/consumption, self shield and actual fixed DC provider.

If you find a real blocker, identify exact function/paragraph, concrete reproducer and minimal source-consistent correction. Distinguish already declared host responsibilities from defects in the bounded implementation. If the eight full feats are acceptable, explicitly close their authored bounded playtest scope as REVIEWED / reference-VALIDATED, with human balance/whole-world runtime and the remaining327 feats/ordinary Soul Cage spell/Soulrender/recipes separately open. Do not treat old registry provisional-complete flags as review proof.
''']
paths=[AUDIT/'BUFFER_FEAT_COMPLETION_SOURCES.json',AUDIT/'GPT_BUFFER_FEAT_FINAL_BRIDGES.md',
       ROOT/'docs/mechanics/BUFFER_FEAT_PLAYTEST.md',ROOT/'tools/buffer_feat_playtest_rules.py',
       ROOT/'tools/validate_buffer_feat_playtests.py',ROOT/'docs/mechanics/BUFFER_FEAT_PLAYTEST_VALIDATION.json',
       ROOT/'docs/mechanics/BUFFER_FEAT_SOURCE_VALIDATION.json']
manifest=[]
for path in paths:
    data=path.read_bytes();manifest.append({'path':str(path.relative_to(GAME)).replace('\\','/'),
       'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
    parts.append('\n## Exact file: '+str(path.relative_to(GAME)).replace('\\','/')+'\n\n```text\n'+data.decode('utf-8')+'\n```\n')
# Actual dependency implementations, avoiding full unrelated packages.
dep_files={
 'tools/form_temphp_playtest_rules.py':('class BufferLedger:', '\ndef blood_ritual_offers'),
 'tools/healing_playtest_rules.py':('def healing_packet(', '\ndef false_life_healing_blocked'),
 'tools/core_playtest_rules.py':('def stabilize(', '\ndef damage_event'),
}
for rel,(start,end) in dep_files.items():
    text=(ROOT/rel).read_text(encoding='utf-8');a=text.index(start);b=text.index(end,a)
    parts.append('\n## Actual existing dependency excerpt: '+rel+'\n```python\n'+text[a:b]+'\n```\n')
packet.write_text('\n'.join(parts),encoding='utf-8')
(AUDIT/'BUFFER_FEAT_IMPLEMENTATION_MANIFEST.json').write_text(json.dumps({'status':'submitted content preparation; actual send requires UI evidence','files':manifest},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'candidateFeats':len(sections),'packetBytes':packet.stat().st_size,'packet':str(packet)}))
