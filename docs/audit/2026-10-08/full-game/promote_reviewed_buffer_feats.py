"""Promote exactly the eight actually reviewed full feats; preserve all sources."""
from pathlib import Path
import hashlib
import json
AUDIT=Path(__file__).resolve().parent;GAME=AUDIT.parents[3];ROOT=GAME/'DescentReviewChanges/ReviewBible'
closure=AUDIT/'GPT_BUFFER_FEAT_FINAL_CLOSURE.md'
assert 'I find no remaining reproducible blocker' in closure.read_text(encoding='utf-8')
assert 'remaining 327 feats' in closure.read_text(encoding='utf-8')
batch_path=ROOT/'data/playtest/feat_drafts/batch_buffers.json'
assert not batch_path.exists(),'Eight-feat promotion already performed'
manifest=json.loads((AUDIT/'BUFFER_FEAT_IMPLEMENTATION_MANIFEST.json').read_text(encoding='utf-8'))
for record in manifest['files']:
    if record['path'].endswith(('/tools/buffer_feat_playtest_rules.py','/docs/mechanics/BUFFER_FEAT_PLAYTEST.md')):
        assert hashlib.sha256((GAME/record['path']).read_bytes()).hexdigest()==record['sha256']
data=json.loads((ROOT/'data/playtest/feat_drafts/candidate_buffers.json').read_text(encoding='utf-8'))
data.update(status='REVIEWED / reference-VALIDATED — operational bounded playtest overlay; human numerical balance pending',
            reviewClosure=str(closure.relative_to(GAME)).replace('\\','/'),
            reviewClosureSha256=hashlib.sha256(closure.read_bytes()).hexdigest())
batch_path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
path=ROOT/'docs/mechanics/BUFFER_FEAT_PLAYTEST.md';text=path.read_text(encoding='utf-8')
text=text.replace('**SOURCE-DISCUSSED / RECONCILED CANDIDATE. Independent implementation review pending; no feat promoted.**',
 '**REVIEWED / reference-VALIDATED for these eight full feats. Provisional playtest overlay; human numerical balance pending.**')
text=text.replace('The335 original feat objects are preserved.',
 'The335 original feat objects are preserved. [Actual GPT closure](../../../../docs/audit/2026-10-08/full-game/GPT_BUFFER_FEAT_FINAL_CLOSURE.md) reviewed131 targeted checks and2,520 funding boundary cases. The remaining327 feats require separate full-clause review.')
path.write_text(text,encoding='utf-8')
# Retain the old complete binding register before updating three deferred roles.
path=ROOT/'data/playtest/form_temphp_bindings.json'
(AUDIT/'FORM_BINDINGS_BEFORE_BUFFER_FEAT_PROMOTION.json').write_bytes(path.read_bytes())
bindings=json.loads(path.read_text(encoding='utf-8'))
ids={'feat:chef','feat:inspiring_leader','feat:soul_cage'}
for row in bindings['bindings']:
    if row['bindingId'] not in ids:continue
    row['classification']='full-feat-interface-reviewed'
    row['status']='REVIEWED / reference-VALIDATED in complete eight-feat package'
    row['openIssues']=[]
    row['reviewEvidence']=list(dict.fromkeys(row['reviewEvidence']+[data['reviewClosure']]))
    row['operationalOverrides'].append('Full feat clauses now use docs/mechanics/BUFFER_FEAT_PLAYTEST.md and data/playtest/feat_drafts/batch_buffers.json; original source preserved, no same-name spell or prestige grant.')
bindings['deferredComponentIds']=[i for i in bindings['deferredComponentIds'] if i not in ids]
assert bindings['deferredComponentIds']==['oracle.supplement.spiral-touched.spiral-touched-boon-v']
bindings['status']='REVIEWED / reference-VALIDATED: selected175+5 roles; five spells and three previously deferred full feats reviewed separately; Time Loop world transaction remains deferred'
path.write_text(json.dumps(bindings,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Promoted eight exact reviewed feats; original335 preserved; Time Loop is sole remaining original deferred form/buffer component.')
