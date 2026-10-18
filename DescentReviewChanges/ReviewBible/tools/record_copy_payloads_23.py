"""Preserve navigation and record copied recipient effects without gate promotion."""
from copy import deepcopy
from datetime import datetime,timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded


def read(p):return json.loads(p.read_bytes())


def main():
    oldcp=A/'ACTIVE_AUTHORING_CHECKPOINT_COPY_RELEASE_CONTINUATION_22.json'
    cp=A/'ACTIVE_AUTHORING_CHECKPOINT_COPY_PAYLOADS_23.json';delta=A/'COPY_PAYLOADS_23_NAVIGATION_DELTA.json'
    report=A/'COPY_PAYLOADS_23_CHECK.json';keep=A/'navigation-before-copy-payloads-23'
    assert not any(p.exists() for p in [cp,delta,report,keep]);now=datetime.now(timezone.utc).isoformat();checks=[]
    def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
    prep=A/'FEAT335_COPY_PAYLOADS_01_PREPARATION.json';pr=read(prep);result=read(A/'FEAT335_COPY_PAYLOADS_01_CHECK.json')
    ck('115 bounded checks with no broad approval',result['checks']==115 and not result['failures'] and not result['runtimeApproved'] and not result['wholeGameComplete'])
    for k in ['archive','progress','request','manifest']:ck('Exact new evidence '+k,info(G/pr[k]['path'])==pr[k])
    queue=R/'data/director/spell_review/remaining_work_queue_17.json';qb=info(queue)
    index=R/'data/public/spell_playtests/authored_review_index.json';ib=info(index)
    ck('525 reviewed323 pending unchanged',read(index)['authoredCounts']=={'reviewed':525,'pending':323})
    start=G/'START_HERE.md';guide=R/'docs/DEVELOPMENT_DIRECTION.md';builder=R/'tools/build_review_map.py'
    ledger=R/'data/playtest/game_development_coverage.json';mapfile=G/'REVIEW_MAP.html';buildfile=A/'REVIEW_MAP_BUILD.json'
    raw={p:p.read_bytes() for p in [start,guide,builder,ledger,mapfile,buildfile]};edits={}
    added='**Copied recipient effects integrated:** [115 checks across27 conditional histories](docs/audit/2026-10-08/full-game/FEAT335_COPY_PAYLOADS_01_CHECK.json) now connect the acquired paid-copy casts to canonical HP/Wounds/death, one temporary-HP grant ledger, healing caps/prohibitions, strongest slow arbitration, Reaction restrictions, AC-family bonuses and same-body personal teleport. Exact supplied turn markers and concentration remove the associated effects. The [complete source/code package and scope limits](docs/audit/2026-10-08/full-game/FEAT335_COPY_PAYLOADS_01_PREPARATION.json) are UNSENT to GPT; world geometry, general interceptors, Ready and other class providers remain open. No new rule or game-wide gate is adopted.'
    for p in [start,guide]:
        text=raw[p].decode('utf8').replace(oldcp.name,cp.name).replace('[checkpoint22]','[checkpoint23]').replace('latest observation was 50% remaining','latest observation was 49% remaining')
        parts=text.split('\n\n');prefix='**Agreed feat-copy release integration:**'
        ck('One copy paragraph '+p.name,sum(s.startswith(prefix) for s in parts)==1)
        for i,s in enumerate(parts):
            if s.startswith(prefix):parts[i]=s+'\n\n'+(added if p==start else added.replace('(docs/audit/','(../../../docs/audit/'))
            elif s.startswith('**GPT continuation required:**'):parts[i]=s.replace('GPT_CONTINUATION_05_HANDOFF_01_PREPARATION.json','GPT_CONTINUATION_05_HANDOFF_02_PREPARATION.json')
            elif s.startswith('**GitHub preservation:**'):parts[i]=s.replace('feat-copy implementation and checkpoint22','feat-copy commitment/payload implementations and checkpoint23')
        edits[p]='\n\n'.join(parts)
    cov=read(ledger);before=deepcopy(cov)
    cov['boundedFeatCopyPayloadProgress']=pr['progress']
    ck('All75 full aspect rows unchanged',cov['aspects']==before['aspects'] and len(cov['aspects'])==75)
    code=raw[builder].decode('utf8');tail=' + read(A / "COPY_RELEASE_CONTINUATION_22_NAVIGATION_DELTA.json")["changes"]\n'
    ck('One previous tail',code.count(tail)==1)
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "COPY_PAYLOADS_23_NAVIGATION_DELTA.json")["changes"]\n')
    featured=[('Current checkpoint23 — copied recipient effects',cp.relative_to(G).as_posix()),('Copy payloads —115 bounded checks, full runtime open',pr['progress']['path']),('Latest prepared continuation context02 — UNSENT',(A/'GPT_CONTINUATION_05_HANDOFF_02_PREPARATION.json').relative_to(G).as_posix())]
    code=code.replace('    featured = [\n','    featured = [\n'+''.join('        '+repr(x)+',\n' for x in featured),1).replace('Current checkpoint22 — paid copy integration and GPT continuation','Checkpoint22 history — paid copy commitment')
    scope='Video game only.525 reviewed/323 pending;249 standalone;173 scoped interfaces. Part4 reached its conversation-length limit; continuation pending owner authorization. No Illusion final. Queue17 unchanged:142 identities/19 groups,181 ungrouped. Copy commitment has136 finite checks; recipient payload integration adds115 checks/27 conditional histories over HP/Wounds/death, buffers, healing, slow/Reaction/AC, teleport and concentration/deadlines. Actual world, Ready, other class providers and listed interfaces remain open. Full progress archives UNSENT to GPT. No new rules or75-domain gate promotions. Last verified push f919c20; later work local until a new verified receipt. Latest allowance49percentremaining; continue to actual review completion or20percent.'
    nodes=[v for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Dict) for k,v in zip(n.keys,n.values) if isinstance(k,ast.Constant) and k.value=='notebookReview'];ck('One map status',len(nodes)==1)
    code=code.replace(ast.get_source_segment(code,nodes[0]),repr(scope),1);compile(code,str(builder),'exec')
    saved=[]
    for p,b in raw.items():
        dst=keep/p.relative_to(G);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b);saved.append({'source':info(p),'preservedCopy':info(dst)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved));ledger.write_bytes(encoded(cov))
    for p,t in edits.items():p.write_text(t,encoding='utf8',newline='\n')
    builder.write_text(code,encoding='utf8',newline='\n')
    changes=[{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in saved if s['source']['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,guide,ledger,builder]]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'newRuleAdoptionsByNavigation':0,'all75DomainGatesUnchanged':True,'sourceInformationDeleted':0}))
    checkpoint=deepcopy(read(oldcp));checkpoint.update(id='ACTIVE-AUTHORING-COPY-PAYLOADS-23',recordedAtUtc=now,status=scope,previousCheckpoint=info(oldcp),boundedFeatCopyPayloads=info(prep),latestPreparedContinuation=info(A/'GPT_CONTINUATION_05_HANDOFF_02_PREPARATION.json'),coverageLedger=info(ledger),navigationDelta=info(delta),preservedNavigation=info(keep/'PRESERVATION_MANIFEST.json'),lastUsageObservation={'usedPercent':51,'remainingPercent':49,'windowMinutes':10080,'secondary':'unavailable'})
    checkpoint['laterLocalWork'].append('Copied recipient payload implementation,115 checks/27 conditional histories, full GPT progress archive and checkpoint23')
    cp.write_bytes(encoded(checkpoint))
    run=subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8');ck('Map build '+run.stderr[-1000:],run.returncode==0)
    build=read(buildfile);ck('No missing links',not build['missingLinks']);ck('Queue17 and authored index unchanged',info(queue)==qb and info(index)==ib)
    checkpoint['navigation']={'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':build['existingDistinctLinks'],'missingLinks':[]};cp.write_bytes(encoded(checkpoint))
    report.write_bytes(encoded({'checkpoint':info(cp),'checks':checks,'checkCount':len(checks),'failures':0,'links':build['existingDistinctLinks'],'queueUnchanged':qb,'indexUnchanged':ib,'all75DomainGatesUnchanged':True,'newRuleAdoptions':0,'sourceInformationDeleted':0}))
    print(json.dumps({'checkpoint':info(cp),'checks':len(checks),'links':build['existingDistinctLinks'],'failures':0}))


if __name__=='__main__':main()
