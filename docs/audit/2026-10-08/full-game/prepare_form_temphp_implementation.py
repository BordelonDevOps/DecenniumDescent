"""Record implementation submission; never infer review closure."""
from pathlib import Path
import json, hashlib, subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
PYTHON=r'C:\Users\cbord\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
guide=ROOT/'docs/mechanics/FORM_TEMP_HP_PLAYTEST.md'
registry=ROOT/'data/playtest/form_temphp_bindings.json'
data=json.loads(registry.read_text(encoding='utf-8'))
evidence=['GPT_FORM_TEMP_HP_FIRST_REVIEW.md','GPT_FORM_TEMP_HP_BOUNDARIES.md','GPT_FORM_TEMP_HP_PROFILE_BOUNDARIES.md']
for file in evidence:assert (HERE/file).exists()
deferred=[]
for row in data['bindings']:
    ident=row['bindingId'];role=row['classification']
    pending=any(v in role for v in ('DEFER','incomplete buffer contract','blocked buffer','blocked transformation'))
    row['reviewEvidence']=evidence[:]
    row['status']='DEFERRED: exact role discussed; named component completion pending' if pending else 'IMPLEMENTED / TESTED: selected role; GPT implementation review pending'
    row['operationalOverrides']=[
        'Apply only the exact classified role in FORM_TEMP_HP_PLAYTEST.md; original costs, target limits, action, frequency, riders and source identity remain.',
        'One active temporary-HP grant; larger replaces, equal retains existing. Pay legal source before arbitration. Explicit shield endpoint beats recipient-next-completed-LR default.',
        'Form and shield interfaces are not whole-card or whole-catalog completion. Source-sensitive timing/identity decisions are preserved in the three named GPT exchanges.']
    row['openIssues']=[]
    if pending:
        deferred.append(ident)
        row['openIssues']=['Named component remains unimplemented; needs its specific content/world-state completion batch.']
    if ident.startswith('druid.'):
        row['operationalOverrides'].append('DruidState uses same body/HP,26 exact gated form profiles, finite rest-snapshot reserves, same-instance natural renewal and source-scoped recharge/rest uses. Full individual attack/condition/rider execution is delegated to canonical systems.')
        row['openIssues']+=['Global natural-attack versus weapon taxonomy and item/anatomy compatibility matrix remain open; no imported monster stats.']
    if ident=='feat:blood_ritual':row['openIssues'].append('Full feat target-count completion remains open; this interface fixes only independent offered amounts/lifetimes and no invented blood HP cost.')
    if ident=='feat:necrotic_affinity':row['openIssues'].append('Selected resistance/Reaction prevention/post-packet shield integration only; extra-hit and anti-resurrection clauses still need full feat review.')
    if 'GUARD' in role or 'PREV' in role or 'TRANSFORMATION' in role or 'PERCEPTION' in role or 'ADJACENT' in role:
        row['operationalOverrides'].append('Retain prior reviewed procedure; incidental shield/form mention does not authorize a new body, spell, resource or action.')
    if 'BARD' in role:row['operationalOverrides'].append('Preserve complete distinct Bard schema, C=max(1,CHA), Crescendo/start/maintenance distinctions, source tags and Echo exclusions.')
data['status']='IMPLEMENTED / TESTED:175+5 selected source roles discussed;152 checks/1053 arbitration-damage scenarios; GPT implementation review pending;9 named components remain deferred'
assert len(deferred)==9,deferred
data['deferredComponentIds']=deferred
data['referenceFiles']=['docs/mechanics/FORM_TEMP_HP_PLAYTEST.md','tools/form_temphp_playtest_rules.py','data/playtest/druid_form_profiles.json','tools/validate_form_temphp_playtests.py']
registry.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
subprocess.run([PYTHON,'-X','utf8',str(ROOT/'tools/build_form_temphp_reference.py')],check=True)
report=json.loads((ROOT/'docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json').read_text(encoding='utf-8'))
assert report['status']=='PASS' and report['checks']==152 and report['arbitrationDamageScenarios']==1053
files=['docs/mechanics/FORM_TEMP_HP_PLAYTEST.md','data/playtest/druid_form_profiles.json',
       'tools/form_temphp_playtest_rules.py','tools/validate_form_temphp_playtests.py',
       'docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json','docs/mechanics/FORM_TEMP_HP_SOURCE_VALIDATION.json']
intro='''# Form and temporary-HP exact implementation review

Codex → Calibration Review. The full175 source roles were individually discussed, then your12 boundaries and5 profile clarifications were reconciled. Here is the actual guide, all26 complete-source form profiles, executable helper and adversarial tests. Source integrity passes175+5 plus Druid metadata; originals/frozen class rules are unchanged.

The helper passed152 contract checks and1053 shield arbitration/damage-state scenarios. Scope is deliberately the selected interfaces, not all clauses of175 cards or a whole runtime. Nine explicitly unfinished named components remain deferred (TimeLoop; Chef/InspiringLeader/SoulCage; HarmonicBulwark; four transformation spells). BloodRitual target count, other feat clauses, item/anatomy matrix and natural-weapon interoperability remain separately visible.

Review actual code against your decisions, especially: payment before arbitration; linked versus independent riders; fixed/default expiry; no zero-grant identity; NecroticAffinity one event/after-resistance/pre-oldTHP prevention/post-final-packet grant; SpiritWalk never attacked; same-body Core damage and forced reversion; source-level gates and subtype choice; natural renewal/local Surges; shared Slam/recharge and rest uses; optional entry-only Broodspawn; independent Mooncursed ally shields. Look for implementation defects, atomicity problems and mismatches with the guide.

Integration contracts: caller certifies all source access, actual source-specific costs not debited by selected methods, legal geometry/targets, actual clocks/rests, exact AC compatibility, defense/roll resolution and final state after legal death replacement. Source-qualified full rider text is returned for canonical engines, not claimed executed by this helper. CreatureWorld is shared for form-bound swarm cleanup. Core tempHP scalar must match the canonical BufferLedger projection; after grants/removal caller updates its projection before subsequent Core use. ProtectiveProgramming uses a unique hit dependency removed after that hit, affecting only an accepted matching grant.

Do not treat passing tests as design approval. Please identify concrete defects or confirm closure of the selected reference interface, explicitly keeping the deferred components and whole game open. All records remain preserved.
'''
parts=[intro]
for rel in files:
    text=(ROOT/rel).read_text(encoding='utf-8')
    parts+=['\n## '+rel+'\nSHA256 '+hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()+'\n','```'+('python' if rel.endswith('.py') else 'json' if rel.endswith('.json') else 'markdown')+'\n'+text+'\n```\n']
parts+=['\n## Exact175 disposition IDs\n','```json\n'+json.dumps([{'id':r['bindingId'],'role':r['classification'],'status':r['status'],'open':r['openIssues']} for r in data['bindings']],ensure_ascii=False,indent=2)+'\n```\n']
packet=HERE/'CODEX_FORM_TEMP_HP_IMPLEMENTATION.md';packet.write_text(''.join(parts),encoding='utf-8')
for name in ('README.md','REVIEW_STATUS.md'):
    path=HERE/name
    text=path.read_text(encoding='utf-8')
    marker='## Form and temporary-HP implementation submitted'
    if marker not in text:
        text+='\n'+marker+'\n\nAll175 exact roles and5 supports have been discussed with GPT. The draft guide,26 form profiles and bounded helper pass152 checks plus1053 arbitration/damage scenarios. The exact implementation packet is prepared for browser submission; GPT implementation review is pending. Nine named incomplete components remain deferred, alongside equipment/weapon interoperability and full-catalog dependencies. No whole-game closure or original deletion.\n'
    path.write_text(text,encoding='utf-8')
print(str(packet),packet.stat().st_size,'bytes; scoped implementation review prepared')
if __name__=='__main__':pass
