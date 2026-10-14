"""Preserve prior navigation and index all nine pending feat source packets."""
from pathlib import Path
import json, shutil, hashlib
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
BACKUP=AUDIT/'navigation-before-complete-feat-source-preparation'

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def replace(s,old,new):
    assert old in s,old[:100]
    return s.replace(old,new)

def main():
    paths=[GAME/'START_HERE.md',AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md',
      AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',ROOT/'data/playtest/game_development_coverage.json',
      ROOT/'tools/build_feat_review_queue.py',ROOT/'docs/director-only/FEAT_REVIEW_QUEUE.md',AUDIT/'FEAT_REVIEW_QUEUE_VALIDATION.json']
    BACKUP.mkdir()
    for p in paths:
        dest=BACKUP/p.relative_to(GAME);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    for stem,n in [('GENERAL_EXPLORATION',31),('GENERAL_COMBAT',58)]:
        status=read(AUDIT/(stem+'_FEAT_SOURCE_STATUS.json'))
        assert status['status']=='prepared-not-sent' and status['featsApproved']==0
        prep=read(AUDIT/(stem+'_FEAT_SOURCE_PREPARATION.json'))
        assert len(prep['selectedFeats'])==n
        packet=AUDIT/status['packetFile']
        assert hashlib.sha256(packet.read_bytes()).hexdigest()==status['packetSha256']
    p=ROOT/'tools/build_feat_review_queue.py';s=p.read_text(encoding='utf-8')
    s=replace(s,"    assert len(feats)==335", "    exploration=read(AUDIT/'GENERAL_EXPLORATION_FEAT_SOURCE_PREPARATION.json');exploration_ids={z['featId'] for z in exploration['selectedFeats']}\n    general_combat=read(AUDIT/'GENERAL_COMBAT_FEAT_SOURCE_PREPARATION.json');general_combat_ids={z['featId'] for z in general_combat['selectedFeats']}\n    groups=[reviewed,craft_ids,combat_ids,skill_ids,magic_ids,extended_ids,heritage_ids,general_ids,exploration_ids,general_combat_ids]\n    assert len(exploration_ids)==31 and len(general_combat_ids)==58\n    assert sum(map(len,groups))==len(set().union(*groups))==335\n    assert exploration['sourceFileSha256']==general_combat['sourceFileSha256']==sha(source)\n    assert len(feats)==335")
    s=replace(s,"        else:\n            phase='Complete source record preserved; focused full-clause packet open'", "        elif id in exploration_ids:\n            phase='Complete General exploration/social source packet prepared, unsent'\n            destination=AUDIT/'GENERAL_EXPLORATION_FEAT_SOURCE_AUDIT.md'\n            next_action='Resolve information, travel, foraging, social and economy limits; then author and exact review'\n        elif id in general_combat_ids:\n            phase='Complete General combat/tactical source packet prepared, unsent'\n            destination=AUDIT/'GENERAL_COMBAT_FEAT_SOURCE_AUDIT.md'\n            next_action='Resolve timing, rerolls, finite companion rules and missing class/spell dependencies; then author and exact review'\n        else:\n            raise AssertionError('Unrouted source feat: '+id)\n            phase='Complete source record preserved; focused full-clause packet open'")
    s=replace(s,"'generalDefenseConferenceMember':id in general_ids,", "'generalDefenseConferenceMember':id in general_ids,'generalExplorationConferenceMember':id in exploration_ids,'generalCombatConferenceMember':id in general_combat_ids,")
    s=replace(s,"'pendingFocusedSourcePrepared':238,'otherPendingFocusedPreparation':89", "'generalExplorationSourcePrepared':31,'generalCombatSourcePrepared':58,'pendingFocusedSourcePrepared':327,'otherPendingFocusedPreparation':0")
    s=replace(s,"24+47+25+31+58+22+31+89==327", "sum(len(g) for g in groups[1:])==327")
    s=replace(s,"The other89 pending General entries retain complete records and await focused preparation.", "An eighth packet covers31 General exploration/social feats and a ninth covers the last58 General combat/tactical feats. All327 pending identities now have complete focused source packets, preserved originals and individual questions. All nine packets remain unsent and require source decisions, authoring and exact review.")
    s=replace(s,"| General defense packet | Other pending |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|'", "| General defense packet | General exploration packet | General combat packet | Other pending |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|'")
    s=replace(s,"{n('generalDefenseConferenceMember')} | {sum", "{n('generalDefenseConferenceMember')} | {n('generalExplorationConferenceMember')} | {n('generalCombatConferenceMember')} | {sum")
    s=replace(s,"or r['generalDefenseConferenceMember'])", "or r['generalDefenseConferenceMember'] or r['generalExplorationConferenceMember'] or r['generalCombatConferenceMember'])")
    p.write_text(s,encoding='utf-8')
    for p,prefix in [(GAME/'START_HERE.md','docs/audit/2026-10-08/full-game/'),(AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md','')]:
        s=p.read_text(encoding='utf-8-sig')
        old='Across all feats,238 pending entries now have focused source packets and89 General entries remain; eight feats are operationally reviewed.'
        new='This preparation checkpoint is superseded by the complete source queue below; eight feats remain operationally reviewed.'
        s=replace(s,old,new)
        marker=new
        text='\n\nThe [General exploration/social packet]('+prefix+'GENERAL_EXPLORATION_FEAT_SOURCE_AUDIT.md) preserves 31 full feats and individual questions, 16 counterparts and 25 governing excerpts; eight checks pass with 21 protected inputs unchanged. The [General combat/tactical packet]('+prefix+'GENERAL_COMBAT_FEAT_SOURCE_AUDIT.md) preserves the last 58 full feats and questions, 23 counterparts, two class comparison cards and 36 governing excerpts; eleven checks pass with 38 inputs unchanged. Missing Battle Master/superiority-die definitions and companion, reroll, travel and information limits remain explicit. All 327 pending feats now have focused source packets across nine cohorts; all are unsent. Source preparation does not grant operational approval. All 335 original identities remain preserved; eight feats are reviewed.'
        s=s.replace(marker,marker+text)
        s=s.replace('is being sent sequentially to Calibration Review Part2','was sent in two parts to Calibration Review Part2 and awaits the actual exact-card verdict')
        p.write_text(s,encoding='utf-8')
    p=ROOT/'data/playtest/game_development_coverage.json';d=read(p)
    note='All327 pending feats have full focused source packets across nine disjoint cohorts;8 of335 remain operationally reviewed. General exploration31 and General combat58 add89 full source objects/questions,39 counterpart bindings and61 current-guide excerpts. Source decisions, authoring and exact review remain open; packets unsent, no source deletion or cosmology decision.'
    for r in d['aspects']:
        if r['id'] in ('DD-03','DD-14','DD-16','DD-17'):
            for stem in ('GENERAL_EXPLORATION','GENERAL_COMBAT'):
                for key,suffix in [('sourceEvidence','PREPARATION.json'),('draftEvidence','AUDIT.md'),('validationEvidence','STATUS.json')]:
                    ref='docs/audit/2026-10-08/full-game/'+stem+'_FEAT_SOURCE_'+suffix
                    if ref not in r[key]:r[key].append(ref)
            r['openIssues'].append(note)
        if r['id']=='DD-14':
            r['currentFeatSourcePreparation']={'pendingFocusedSourcePrepared':327,'otherPendingFocusedPreparation':0,'operationalReviewed':8,'packetCount':9,'status':'prepared-not-sent'}
            stale=[x for x in r['openIssues'] if x.startswith('Current focused queue supersedes')]
            r.setdefault('resolvedIssueHistory',[]).extend(stale)
            r['openIssues']=[x for x in r['openIssues'] if x not in stale]
        if 'jewelcraftingCurrentCheckpoint' in r:
            r['jewelcraftingCurrentCheckpoint']='Source conference complete;43 candidate cards authored and locally validated. Both exact-review parts sent, actual Part A receipt preserved; await actual Part B verdict. No Jewelcrafting approval;305 of687 recipes reviewed,197 of433 public.'
    write(p,d)
    p=AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json';d=read(p)
    d['observedAtUtc']=datetime.now(timezone.utc).isoformat()
    d['independentProgress'].update(pendingFeatSourcesPrepared=327,remainingGeneralFeatPreparation=0,generalExplorationSourcePrepared=31,generalCombatSourcePrepared=58)
    d['currentGoalTurnClassification']='progress: all327 pending feat identities now source-prepared in nine focused cohorts; exact Jewelcrafting verdict pending'
    d['nextAction']='Retrieve exact Jewelcrafting verdict on3074a6c4-b718-4241-ae05-f6b3ed1238b0; do not resend or infer approval. Nine feat packets and remaining recipe packets await source conferences after this exact review.'
    write(p,d)
    print(json.dumps({'status':'updated','backupFiles':len(paths),'pendingFocusedSourcePrepared':327,'reviewedFeats':8}))

if __name__=='__main__':main()
