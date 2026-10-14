"""Record actual scoped final approval, leaving deferred cards and game open."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
GAME=HERE.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
reply=(HERE/'GPT_REMAINING_LIFECYCLE_FINAL_CLOSURE.md').read_text(encoding='utf-8')
assert reply.startswith('# GPT confirmed remaining lifecycle closure')
assert 'no remaining concrete blocker' in reply and 'REVIEWED / reference-VALIDATED' in reply
closure='docs/audit/2026-10-08/full-game/GPT_REMAINING_LIFECYCLE_FINAL_CLOSURE.md'
p=ROOT/'docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST_VALIDATION.json';report=json.loads(p.read_text(encoding='utf-8'))
assert report['status']=='PASS' and report['checks']==129
report['reviewStatus']='REVIEWED / reference-VALIDATED: selected80+5 interfaces only';report['reviewClosure']=closure
p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'data/playtest/remaining_lifecycle_bindings.json';d=json.loads(p.read_text(encoding='utf-8'))
d['status']='REVIEWED / reference-VALIDATED: selected lifecycle/object/command/guard roles;80+5 classifications, full tempHP/form/Time Loop effects deferred'
d['reviewClosure']=closure
for r in d['bindings']:
 role=r['classification'];deferred=role.startswith('DEFER') or 'THP details' in role
 r['status']='DISCUSSED / full temporary-HP or Time Loop effect DEFERRED; prior bounded roles preserved' if deferred else 'REVIEWED / reference-VALIDATED: supplied lifecycle/object/command/guard or prior-component boundary only'
 r['reviewEvidence']=list(dict.fromkeys(r['reviewEvidence']+['GPT_REMAINING_LIFECYCLE_IMPLEMENTATION_FINDINGS.md','GPT_REMAINING_LIFECYCLE_FINAL_CLOSURE.md']))
 r['openIssues']=[v for v in r['openIssues'] if v!='Exact implementation review pending.']
 if r['bindingId']=='cleric.hero.cultist.rite-of-the-crimson-choir':
  r['operationalOverrides'].append('Final review correction: ordinary outgoing burst retains Cleric-feature identity and normal eligible enemy/target-side damage/death/resource responses. Only incoming sealed provenance suppresses a fanatic zero burst. No Choir hit-heal, fanatic-body resources or new explosion opportunity.')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST.md';text=p.read_text(encoding='utf-8')
text=text.replace('**IMPLEMENTED CANDIDATE — GPT corrected implementation review pending.**','**REVIEWED / reference-VALIDATED — selected80+5 lifecycle/object/command/guard interfaces.**')
text+='\n[Final notebook disposition](../../../../docs/audit/2026-10-08/full-game/GPT_REMAINING_LIFECYCLE_FINAL_CLOSURE.md) confirms this bounded scope after the Choir provenance correction.\n'
p.write_text(text,encoding='utf-8')
p=ROOT/'data/playtest/game_development_coverage.json';coverage=json.loads(p.read_text(encoding='utf-8'))
for r in coverage['aspects']:
 if r['id'] not in ('DD-24','DD-35'):continue
 r['closure']='open';r['status']='selected-interfaces-closed-remainder-integrating'
 r['reviewEvidence']=list(dict.fromkeys(r['reviewEvidence']+[closure]))
 r['openIssues']=[v for v in r['openIssues'] if not v.startswith('Remaining80+5 lifecycle implementation:')]
 note='Remaining companion/structure lifecycle80+5: joint bounded approval;129 targeted checks. Choir, Ritual Thrall, Oracle commands/interception/servants/scout, Paladin Echo, Soldier objects/materials and classified guards. No complete-card, tempHP/form or runtime claim.'
 if note not in r.setdefault('completedScopes',[]):r['completedScopes'].append(note)
 r['openIssues'].append('Next form/tempHP corpus175 source roles+5 supports preserved and integrity-verified. Full cards, general corpse cleanup, Time Loop, natural creature rest, remaining source-specific interactions and runtime stay open.')
p.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ('README.md','REVIEW_STATUS.md'):
 p=HERE/name;text=p.read_text(encoding='utf-8')
 text+='\n## Remaining lifecycle bounded closure\n\nThe [Choir correction](CODEX_REMAINING_LIFECYCLE_CORRECTION.md) received [explicit final approval](GPT_REMAINING_LIFECYCLE_FINAL_CLOSURE.md):129 checks,80 exact source roles+5 frozen supports. Ordinary burst damage preserves eligible enemy/target-side triggers; incoming sealed-zero suppression remains separate. All deferred full-card/tempHP/form/Time Loop and runtime work remains open. The next form/tempHP corpus has175 roles+5 supports, including66 Druid passages, other class/Bard buffers, semantic forms,7 feats,9 spells and3 V6 ancestry traits.\n'
 p.write_text(text,encoding='utf-8')
p=ROOT/'docs/mechanics/DEVELOPMENT_ROADMAP.md';text=p.read_text(encoding='utf-8')
text+='\n- [Remaining companion and Soldier structure rules](REMAINING_LIFECYCLE_PLAYTEST.md): selected80+5 interfaces jointly reviewed with129 checks; source-specific command/control/interception, finite bodies, scout/Echo, Palisade kits and repair, Quick Deploy and turrets. Full forms/tempHP and other unimplemented card components remain open.\n'
p.write_text(text,encoding='utf-8')
p=GAME/'START_HERE.md';text=p.read_text(encoding='utf-8')
text+='\nThe [remaining companion and structure rules](DescentReviewChanges/ReviewBible/docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST.md) are jointly reviewed with129 checks: Cleric/Oracle summons, controlled undead, Paladin spirits, Soldier cover and turrets now have explicit creation, command and ending procedures. The175-source form/temporary-HP discussion is next; the whole-game audit is still in progress.\n'
p.write_text(text,encoding='utf-8')
print('Recorded confirmed remaining80+5 closure; full effects and whole game remain open.')
