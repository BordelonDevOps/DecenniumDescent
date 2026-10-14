"""Register one already prepared cohort; verify sources and archive prior navigation."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import argparse
import hashlib
import json
import re
import shutil

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('prefix');ap.add_argument('--label',required=True);ap.add_argument('--note',required=True);ap.add_argument('--addendum',action='append',default=[]);args=ap.parse_args()
    assert re.fullmatch('[A-Z0-9_]+',args.prefix)
    cp=A/'FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json';cov=read(cp);old=dict(cov)
    filename=args.prefix+'_SOURCE_PREPARATION.json';assert filename not in cov['cohortFiles']
    files=cov['cohortFiles']+[filename];allrows=[read(A/f) for f in files];new=allrows[-1]
    status=read(A/(args.prefix+'_SOURCE_STATUS.json'));assert sha(A/status['packetFile'])==status['packetSha256']
    records=[r for d in allrows for r in d['selectedSpells']];ids=[r['spellId'] for r in records]
    assert len(ids)==len(set(ids));assert all(c['pass'] for d in allrows for c in d['checks'])
    protected={}
    for d in allrows:
        for name,digest in d['protectedFiles'].items():
            assert name not in protected or protected[name]==digest,name
            protected[name]=digest
    addenda=list(dict.fromkeys([str(Path(n).with_suffix('.json')) for n in cov.get('sourceAddenda',[])]+args.addendum))
    for addendum in addenda:
        assert Path(addendum).name==addendum and addendum.endswith('.json')
        d=read(A/addendum)
        if 'checks' in d:assert all(c['pass'] for c in d['checks'])
        md=A/Path(addendum).with_suffix('.md')
        if 'addendumSha256' in d:assert sha(md)==d['addendumSha256']
        for artifact in [A/addendum,md]:
            protected[str(artifact.relative_to(G)).replace('\\','/')]=sha(artifact)
        for name,digest in d.get('protectedFiles',{}).items():
            assert name not in protected or protected[name]==digest,name
            protected[name]=digest
    for name,digest in protected.items(): assert sha(G/name)==digest,name
    catalog=read(R/'data/public/spell_playtests/catalog.json')['spells'];by={r['id']:r for r in catalog}
    assert len(catalog)==848 and sum(r['operational'] is None for r in catalog)==572
    assert all(by[r['spellId']]==r['fullSourceAndCurrentAccessRecord'] for r in records)
    deferred=[r['spellId'] for r in records if r.get('scope')=='post-push receipt only']
    bindings=sum(len(d['currentBookBindings']) for d in allrows);total=len(ids);questions=total-len(deferred)
    remaining=sorted(r['id'] for r in catalog if r['operational'] is None and r['id'] not in set(ids))
    def rank(sid):return min(v['rank'] for v in by[sid]['classAccess'].values())
    ranks=dict(sorted(Counter(rank(s) for s in remaining).items()))
    rank6=sum(rank(s)==6 for s in ids)
    all_through6=not any(rank(s)<=6 for s in remaining)
    all_through7=not any(rank(s)<=7 for s in remaining)
    all_through8=not any(rank(s)<=8 for s in remaining)
    all_pending_prepared=not remaining
    completed_through=min(ranks)-1 if ranks else 9
    assert total==status['counts']['focusedPendingSourceIdentitiesIncludingThisCohort']
    assert bindings==status['counts']['currentBookBindingsIncludingThisCohort']
    assert questions==status['counts']['prePushPreparedSpellQuestionsIncludingThisCohort']
    backup=A/('navigation-before-'+args.prefix.lower()+'-registration');assert not backup.exists();backup.mkdir()
    nav=[G/'START_HERE.md',cp,A/'PREPARED_SPELL_SOURCE_INDEX.md',A/'GPT_REVIEW_CONTINUATION_HANDOFF.md',A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',R/'data/playtest/game_development_coverage.json']
    for p in nav:shutil.copyfile(p,backup/p.name)
    write(backup/'MANIFEST.json',{str(p.relative_to(G)).replace('\\','/'):sha(p) for p in nav})
    cov.update(cohortFiles=files,distinctPreparedPendingSpellIds=total,currentBookBindings=bindings,prePushMechanicalQuestions=questions,postPushReceiptOnlyIds=deferred,protectedInputsUnchanged=len(protected),remainingUnpreparedIdentities=len(remaining),remainingUnpreparedByMinimumClassRank={str(k):v for k,v in ranks.items()},remainingUnpreparedSpellIds=remaining,minimumRank6SourceIdentitiesPrepared=rank6)
    cov['allPendingMinClassRankZeroToSixSourcesCovered']=all_through6
    cov['allPendingMinClassRankZeroToSevenSourcesCovered']=all_through7
    cov['allPendingMinClassRankZeroToEightSourcesCovered']=all_through8
    cov['allPendingMinClassRankZeroToNineSourcesCovered']=all_pending_prepared
    cov['allPendingOrdinarySpellSourcesPrepared']=all_pending_prepared
    cov['highestFullyPreparedMinimumClassRank']=completed_through
    cov['minimumRank6SourceIdentitiesRemaining']=[s for s in remaining if rank(s)==6]
    for level in (7,8,9):
        cov[f'minimumRank{level}SourceIdentitiesPrepared']=sum(rank(s)==level for s in ids)
        cov[f'minimumRank{level}SourceIdentitiesRemaining']=[s for s in remaining if rank(s)==level]
    for name in args.addendum:
        md=name.replace('.json','.md')
        if md not in cov['sourceAddenda']:cov['sourceAddenda'].append(md)
    write(cp,cov)
    summary=f'{len(files)} unsent cohorts, {total} identities, {bindings} book bindings, {questions} mechanical questions and {len(deferred)} unchanged post-push receipts.'
    p=G/'START_HERE.md';s=p.read_text(encoding='utf-8')
    s,n=re.subn(r'(?<=PREPARED_SPELL_SOURCE_INDEX\.md\): ).*?(?= Preparation grants no approval\.)',summary,s);assert n==1
    p.write_text(s,encoding='utf-8')
    p=A/'PREPARED_SPELL_SOURCE_INDEX.md';s=p.read_text(encoding='utf-8')
    s,n=re.subn(r'\*\*[^\n]+packets prepared; none sent or approved\.\*\*[^\n]+',f'**{len(files)} packets prepared; none sent or approved.** These retain {total} distinct unfinished identities and {bindings} exact current-book placements: {questions} mechanical questions and {len(deferred)} unchanged post-push receipts. Ordinary spell totals remain276 operational drafts and572 unfinished identities out of848.',s);assert n==1
    marker='Every unfinished identity whose minimum class-access rank is'
    index=s.index(marker)
    row=f"| [{args.label}]({args.prefix}_SOURCE_AUDIT.md) | {new['counts']['selectedSources']} | {new['counts']['prePushMechanicalQuestions']} | {new['counts']['postPushReceiptOnly']} | {len(new['currentBookBindings'])} | {len(new['checks'])} |\n\n"
    s=s[:index].rstrip()+'\n'+row+s[index:]
    s=re.sub(r'(This does not make those spells selectable or reviewed\.)[^\n]+?(GPT source decisions, authored cards and separate exact review remain necessary\.)',rf'\1 {rank6} rank6 identities are also prepared; {len(remaining)} higher-rank identities remain. \2',s)
    s=re.sub(r'Post-push receipts,unchanged and excluded from current authoring: [^.]+\.', 'Post-push receipts,unchanged and excluded from current authoring: '+', '.join(deferred)+'.',s)
    for ranknum in sorted({int(k) for k in old['remainingUnpreparedByMinimumClassRank']}|set(ranks)):
        s=re.sub(rf'^\| {ranknum} \| \d+ \|$',f'| {ranknum} | {ranks.get(ranknum,0)} |',s,flags=re.M)
    if all_through6:
        completed_counts=', '.join(f'all{sum(rank(s)==level for s in ids)} at rank{level}' for level in range(5,completed_through+1))
        rank_label=('rank9' if min(ranks)==9 else f'rank{min(ranks)}–9') if ranks else ''
        remaining_scope=f'{len(remaining)} {rank_label} identities remain to prepare.' if ranks else 'Every pending source identity has preparation.'
        s=re.sub(r'^Every unfinished identity whose minimum class-access rank is0–\d[^\n]+',f'Every unfinished identity whose minimum class-access rank is0–{completed_through} now has source preparation, including {completed_counts}. This does not make those spells selectable or reviewed. {remaining_scope} GPT source decisions, authored cards and separate exact review remain necessary.',s,flags=re.M)
    s+='\n'+args.note+'\n'
    for name in args.addendum:s+='\nSupporting [named-profile source evidence]('+name.replace('.json','.md')+') must accompany this cohort before dispatch.\n'
    p.write_text(s,encoding='utf-8')
    p=A/'GPT_REVIEW_CONTINUATION_HANDOFF.md';s=p.read_text(encoding='utf-8')
    s=re.sub(r'^### Current checkpoint — (.+)$',r'### Historical checkpoint — \1',s,flags=re.M)
    s+=f'\n### Current checkpoint — {len(files)} prepared spell cohorts\n\nThe [source index](PREPARED_SPELL_SOURCE_INDEX.md) covers {total} pending identities and {bindings} book bindings: {questions} mechanical questions and {len(deferred)} unchanged post-push receipts. All pending ranks0–{completed_through} are prepared; {len(remaining)} remain unprepared. All source packets remain unsent, and ordinary totals remain276 operational/572 pending.\n\n'+args.note+'\n'
    for name in args.addendum:s+='\nThe [complete addendum]('+name+') is required with this source conference.\n'
    s+='\nCurrent gathering conference status is recorded in [the dispatch ledger](GATHERING_TOOL_PART2_DISPATCH.json); do not duplicate an active request. No new exact card approvals, source deletion, push or cosmology review occurred.\n'
    p.write_text(s,encoding='utf-8')
    p=A/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json';o=read(p)
    o['independentProgress'].update(focusedPendingSpellSourcesPrepared=total,preparedSpellCohorts=len(files),currentBookBindingsAcrossPreparedSpellPackets=bindings,prePushSpellQuestionsAcrossPreparedPackets=questions,postPushSpellReceipts=deferred,higherRankUnpreparedSpellIdentities=len(remaining),rank6SourcesPrepared=rank6)
    o['independentProgress']['allPendingMinimumRankZeroToSixSourcesPrepared']=all_through6
    o['independentProgress']['allPendingMinimumRankZeroToSevenSourcesPrepared']=all_through7
    o['independentProgress']['allPendingMinimumRankZeroToEightSourcesPrepared']=all_through8
    o['independentProgress']['allPendingOrdinarySpellSourcesPrepared']=all_pending_prepared
    for level in (7,8,9):o['independentProgress'][f'rank{level}SourcesPrepared']=sum(rank(s)==level for s in ids)
    o['independentProgress']['latestPreparedSpellCohort']={'prefix':args.prefix,'sources':len(new['selectedSpells']),'bookBindings':len(new['currentBookBindings']),'addenda':args.addendum}
    o['independentProgressUpdatedAtUtc']=datetime.now(timezone.utc).isoformat()
    o['currentGoalTurnClassification']='progress:registered '+args.prefix+' source evidence; live GPT request tracked separately in currentRequest'
    o['consecutiveBlockedGoalTurns']=0;write(p,o)
    p=R/'data/playtest/game_development_coverage.json';g=read(p);a=next(x for x in g['aspects'] if x['id']=='DD-12');prefix='docs/audit/2026-10-08/full-game/'
    a['sourceEvidence'].append(prefix+filename);a['validationEvidence'].append(prefix+args.prefix+'_SOURCE_STATUS.json')
    for name in args.addendum:a['sourceEvidence'].append(prefix+name)
    a['currentPreparedSpellSourceCoverage'].update(identities=total,bookBindings=bindings,mechanicalQuestions=questions,deferredReceipts=deferred,higherRankSourcesUnprepared=len(remaining),rank6SourcesPrepared=rank6)
    a['currentPreparedSpellSourceCoverage']['allPendingMinimumRank0To6Prepared']=all_through6
    a['currentPreparedSpellSourceCoverage']['allPendingMinimumRank0To7Prepared']=all_through7
    a['currentPreparedSpellSourceCoverage']['allPendingMinimumRank0To8Prepared']=all_through8
    a['currentPreparedSpellSourceCoverage']['allPendingOrdinarySpellSourcesPrepared']=all_pending_prepared
    for level in (7,8,9):a['currentPreparedSpellSourceCoverage'][f'rank{level}SourcesPrepared']=sum(rank(s)==level for s in ids)
    write(p,g)
    for name,digest in protected.items():assert sha(G/name)==digest,name
    receipt={'status':'PASS source preservation and navigation','cohort':args.prefix,'cohorts':len(files),'identities':total,'bookBindings':bindings,'questions':questions,'deferredReceipts':len(deferred),'protectedInputsUnchanged':len(protected),'remainingUnprepared':len(remaining),'rank6Prepared':rank6,'rank6Remaining':ranks.get(6,0),'backup':str(backup.relative_to(G)).replace('\\','/'),'newSourcePacketSha256':status['packetSha256'],'sourceInformationDeleted':0,'newApprovals':0,'cosmology':'post-verified-push only'}
    write(A/(args.prefix+'_NAVIGATION_RECEIPT.json'),receipt);print(json.dumps(receipt))

if __name__=='__main__':main()
