"""Record implemented repairs without claiming independent acceptance."""
from pathlib import Path
import json

AUDIT=Path(__file__).resolve().parent
ROOT=AUDIT.parents[3]/'DescentReviewChanges/ReviewBible'

def main():
    path=ROOT/'data/playtest/game_development_coverage.json'
    prior=AUDIT/'COVERAGE_BEFORE_TEMPORAL_KERNEL_REPAIRS.json'
    assert not prior.exists(), 'Repair progress already recorded'
    assert (AUDIT/'GPT_TEMPORAL_KERNEL_FINDINGS.md').exists()
    assert (AUDIT/'gpt-temporal-kernel-repairs.png').exists()
    prior.write_bytes(path.read_bytes())
    coverage=json.loads(path.read_text(encoding='utf-8'))
    for row in coverage['aspects']:
        if row['id'] not in ('DD-03','DD-08','DD-09','DD-21','DD-24','DD-27','DD-35','DD-63','DD-64'):
            continue
        row['openIssues']=[x for x in row['openIssues'] if not x.startswith('Time Loop: twelve source boundaries settled.')]
        row['openIssues'].append('Time Loop: twelve source boundaries settled; actual notebook review found six bounded-kernel issues. Targeted repairs now pass70 adversarial test methods and are back under independent GPT review. Full playable activation remains disabled; seven major source integrations are missing. This is not temporal or whole-domain closure.')
        row['reviewEvidence']=list(dict.fromkeys(row['reviewEvidence']+[
            'docs/audit/2026-10-08/full-game/GPT_TEMPORAL_KERNEL_FINDINGS.md',
            'docs/audit/2026-10-08/full-game/CODEX_TEMPORAL_KERNEL_REPAIRS.md']))
    path.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    note='''
## Six temporal-kernel findings repaired; independent confirmation pending

The actual notebook returned [six findings](GPT_TEMPORAL_KERNEL_FINDINGS.md). The [repair packet](CODEX_TEMPORAL_KERNEL_REPAIRS.md) contains the updated helper, all70 passing test methods, current scope guide and unchanged existing maximum-HP source constructor. It was submitted for independent confirmation. The source constructor already rejects the review's two invented max-HP IDs; an explicit temporal table also now rejects actual valid sources with unimplemented temporal policies. Full Time Loop stays unavailable, the seven larger integrations remain unfinished, and no domain was promoted.

The next control/pulse source preparation is [V3](TEMPORAL_CONTROL_PULSE_POLICY_SOURCES_V3.json):44 selected control records,32 pulse binding records,3 direct supplemental records and all33 pulse/native/contact aliases. This is evidence preparation, not an adopted temporal policy. Earlier preparation versions remain preserved.
'''
    for name in ('README.md','REVIEW_STATUS.md'):
        p=AUDIT/name
        p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8')
    p=AUDIT/'TEMPORAL_KERNEL_REPAIR_LOG.md'
    p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8')
    print('Recorded70 passing tests and actual independent repair submission; no temporal closure.')

if __name__=='__main__':main()
