"""Register the four-source conference, preserving original source and domain gates."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import ast
import json
import subprocess
import sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    base=R/'data/director/spell_review'
    oldq,newq=base/'remaining_work_queue_26.json',base/'remaining_work_queue_27.json'
    oldcp=A/'ACTIVE_AUTHORING_CHECKPOINT_PART5_PROGRESS_33.json'
    cp=A/'ACTIVE_AUTHORING_CHECKPOINT_RANK8_MEMORY_CONTROL_34.json'
    delta=A/'RANK8_MEMORY_CONTROL_34_NAVIGATION_DELTA.json'
    report=A/'RANK8_MEMORY_CONTROL_34_CHECK.json'
    keep=A/'navigation-before-rank8-memory-control-34'
    assert not any(p.exists() for p in [newq,cp,delta,report,keep])
    now=datetime.now(timezone.utc).isoformat();checks=[]
    def ck(n,v): checks.append({'check':n,'passed':bool(v)});assert v,n
    pp=A/'RANK8_MEMORY_CONTROL_4_SOURCE_CONFERENCE_01_PREPARATION.json';prep=read(pp);d=read(G/prep['candidate']['path'])
    for k in ['candidate','archive','manifest','check','request']:ck('Exact source conference '+k,info(G/prep[k]['path'])==prep[k])
    ids=[r['spellId'] for r in d['records']];previous=read(oldq);q=deepcopy(previous)
    group={'group':'rank8-memory-control4','phase':'source-conference-prepared-unsent','identities':ids,'identityCount':4,'candidate':prep['candidate'],'preparation':info(pp),'archive':prep['archive'],'adopted':False,'earlierCompleteProcedures':0,'newCurrentEncounters':0,'riskCounts':d['riskCounts']}
    q['groups'].append(group)
    for row in q['rows']:
        if row['id'] in ids:
            ck('Previously ungrouped '+row['id'],row['currentGroup'] is None)
            row['previousPhaseBeforeConference34']=row['currentPhase']
            row.update(currentGroup=group['group'],currentPhase=group['phase'],nextAction='Confer with actual GPT on21 unselected memory/control choices. Preserve exact episodic events, score-setting history, real CR qualification, source-specific control and communication. No procedure or case adoption before decisions.')
    q['sourceBindings'].extend([info(oldq),info(pp),prep['candidate'],prep['archive'],prep['check']])
    q.update(id='REMAINING-WORK-QUEUE-27',recordedAtUtc=now,previousQueue=info(oldq),pendingDistribution=dict(Counter(r['currentPhase'] for r in q['rows'])),preparedOrActualReviewIdentityCount=181,originalSourceOrReceiptWorkCount=142)
    ck('323 identities/order retained',[r['id'] for r in previous['rows']]==[r['id'] for r in q['rows']] and len(q['rows'])==323)
    ck('27 disjoint groups181 identities',len(q['groups'])==27 and sum(g['identityCount'] for g in q['groups'])==len({i for g in q['groups'] for i in g['identities']})==181)
    ck('142 ungrouped',sum(r['currentGroup'] is None for r in q['rows'])==142)
    ck('All previous groups intact',q['groups'][:-1]==previous['groups'])
    for a,b in zip(previous['rows'],q['rows']):ck('Full source/access/member '+a['id'],all(a[k]==b[k] for k in ['currentIndexEntryUnchanged','completeCurrentSourceAndAccess','previousAuthoringMapRowUnchanged','semanticAcceptanceClaimed']))
    for b in q['sourceBindings']:ck('Exact queue source '+b['path'],info(G/b['path'])==b)
    index=R/'data/public/spell_playtests/authored_review_index.json';ib=info(index)
    ck('Applied counts remain525/323',read(index)['authoredCounts']=={'reviewed':525,'pending':323})
    start,guide,builder=G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',R/'tools/build_review_map.py'
    ledger=R/'data/playtest/game_development_coverage.json';mapfile,buildfile=G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json'
    raw={p:p.read_bytes() for p in [start,guide,builder,ledger,mapfile,buildfile]}
    added='**Rank-eight memory and control sources:** The [four-spell conference](docs/audit/2026-10-08/full-game/RANK8_MEMORY_CONTROL_4_SOURCE_CONFERENCE_01_PREPARATION.json) preserves68 full sources, four native placements,ten reviewed counterparts and21 unselected questions;235 source/access/preservation checks pass. Erase Mind keeps event-memory loss and identity pressure; Feeblemind keeps INT/CHA1 and spell/communication restrictions; Mass Dominate keeps three actual CR10-or-lower targets; Mind Ravel keeps five-minute forgetting and confusion. All four are individually tierC. Recovery, score-layer timing and source-specific control choices require actual GPT. The packet is UNSENT and adopts no rules or cases.'
    edits={}
    for p in [start,guide]:
        text=raw[p].decode('utf8').replace(oldcp.name,cp.name).replace('[checkpoint33]','[checkpoint34]')
        parts=text.split('\n\n');ck('One queue paragraph '+p.name,sum(x.startswith('**Remaining spell work:**') for x in parts)==1)
        for n,s in enumerate(parts):
            if s.startswith('**Remaining spell work:**'):parts[n]=s.replace('Queue26','Queue27').replace('remaining_work_queue_26.json','remaining_work_queue_27.json').replace('177 in twenty-six active/prepared groups and 146','181 in twenty-seven active/prepared groups and 142')+'\n\n'+(added if p==start else added.replace('(docs/audit/','(../../../docs/audit/'))
            elif s.startswith('**GitHub preservation:**'):parts[n]=s+' The new memory/control4 conference and queue27/checkpoint34 are also local.'
        edits[p]='\n\n'.join(parts)
    cov=read(ledger);priorcov=deepcopy(cov);cov.setdefault('activeOrdinarySpellReviewHistory',[]).append(deepcopy(cov['activeOrdinarySpellReview']))
    code=raw[builder].decode('utf8');tail=' + read(A / "GPT_PART5_LABELS_33A_NAVIGATION_DELTA.json")["changes"]\n';ck('One map tail',code.count(tail)==1)
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "RANK8_MEMORY_CONTROL_34_NAVIGATION_DELTA.json")["changes"]\n')
    featured=[('Current checkpoint34 — rank8 memory/control sources',cp.relative_to(G).as_posix()),('Current323 pending identities — queue27',newq.relative_to(G).as_posix())]
    code=code.replace('    featured = [\n','    featured = [\n'+''.join('        '+repr(x)+',\n' for x in featured),1).replace('Current checkpoint33 — actual Illusion return and Companion review','Checkpoint33 history — actual Illusion return and Companion review').replace('Current323 pending identities — queue26','Queue26 history — before rank8 memory/control')
    code=code.replace('    pending = [\n','    pending = [\n        '+repr(('Rank8 memory/control4 —21 questions,4C, UNSENT',pp.name))+',\n',1)
    scope='Video game only.525 reviewed/323 pending;249 standalone;173 scoped interfaces. Actual Illusion14 repaired semantics accepted; Exact13 rendering UNSENT. Actual Part5 CompanionExact05 review remains active at capture,with two CR2 whole-case holds. New memory/control4 conference:68 sources,21 unselected questions,235 checks,4C;no adopted procedures/cases. Queue27:181 identities in27 groups,142 ungrouped. All75 domain gates unchanged. GitHubc9c9ffb covers checkpoint32; subsequent review/authoring/source preparation remains local. Latest allowance37percentremaining;continue to completion or20percent.'
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];ck('One map status',len(nodes)==1)
    code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1);compile(code,str(builder),'exec')
    saved=[]
    for p,b in raw.items():
        dst=keep/p.relative_to(G);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b);ck('Exact previous navigation '+p.name,dst.read_bytes()==b);saved.append({'source':info(p),'preservedCopy':info(dst)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved));newq.write_bytes(encoded(q))
    cov['activeOrdinarySpellReview'].update(recordedAtUtc=now,currentQueue=info(newq),rank8MemoryControl4SourceConference=info(pp));ck('All75 full domain rows unchanged',cov['aspects']==priorcov['aspects'] and len(cov['aspects'])==75);ledger.write_bytes(encoded(cov))
    for p,t in edits.items():p.write_text(t,encoding='utf8',newline='\n')
    builder.write_text(code,encoding='utf8',newline='\n')
    changes=[{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in saved if s['source']['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'newRuleAdoptionsByNavigation':0,'all75DomainGatesUnchanged':True,'sourceInformationDeleted':0}))
    checkpoint=deepcopy(read(oldcp));checkpoint.update(id='ACTIVE-AUTHORING-RANK8-MEMORY-CONTROL-34',recordedAtUtc=now,status=scope,previousCheckpoint=info(oldcp),currentWorkQueue=info(newq),remainingPreparedGroups=q['groups'],rank8MemoryControl4SourceConference=info(pp),lastUsageObservation={'usedPercent':63,'remainingPercent':37,'windowMinutes':10080,'secondary':'unavailable'},laterLocalWork=checkpoint['laterLocalWork']+['Rank8 memory/control4 source conference:68sources/21questions/235checks,prepared unsent;queue27/checkpoint34.'],coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'))
    cp.write_bytes(encoded(checkpoint));run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');ck('Review map build '+run.stderr[-1200:],run.returncode==0)
    built=read(buildfile);ck('No missing links',not built['missingLinks']);ck('Authored index unchanged',info(index)==ib)
    checkpoint['navigation']={'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':built['existingDistinctLinks'],'missingLinks':[]};cp.write_bytes(encoded(checkpoint))
    report.write_bytes(encoded({'checkpoint':info(cp),'queue':info(newq),'checks':checks,'checkCount':len(checks),'failures':0,'links':built['existingDistinctLinks'],'indexUnchanged':ib,'all75DomainGatesUnchanged':True,'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
    print(json.dumps({'checkpoint':info(cp),'queue':info(newq),'checks':len(checks),'links':built['existingDistinctLinks'],'failures':0}))

if __name__=='__main__':main()
