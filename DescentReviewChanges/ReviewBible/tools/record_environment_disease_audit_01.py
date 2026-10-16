"""Make the bounded disease interface audit discoverable without changing gameplay status."""
from copy import deepcopy
from datetime import datetime, timezone
import ast,json,subprocess,sys
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    now=datetime.now(timezone.utc).isoformat()
    target=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_DISEASE_INTERFACE_AUDIT_01.json'
    delta=A/'DISEASE_INTERFACE_AUDIT_01_NAVIGATION_DELTA.json'
    keep=A/'navigation-before-disease-interface-audit-01'
    assert all(not p.exists() for p in [target,delta,keep])
    audit=A/'ENVIRONMENT_DISEASE_INTERFACE_AUDIT_01.json';data=read(audit)
    assert data['counts']['sourceFiles']==33 and data['submitted'] is False
    for binding in data['sourceBindings']:assert info(G/binding['path'])==binding
    previous=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_RELIC_NULL_03_SUBMISSION_01.json'
    start=G/'START_HERE.md';nav=R/'tools/build_review_map.py';ledger=R/'data/playtest/game_development_coverage.json'
    originals={};saved=[]
    for p in [start,nav,ledger,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']:
        raw=p.read_bytes();out=keep/p.relative_to(G);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
        originals[p]=raw;saved.append({**info(p),'preservedCopy':out.relative_to(G).as_posix()})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(saved))
    text=originals[start].decode();old=previous.relative_to(G).as_posix();new=target.relative_to(G).as_posix();assert text.count(old)==1
    text=text.replace(old,new,1)
    note='**Prepared disease-interface audit:** [33 unchanged source files](docs/audit/2026-10-08/full-game/ENVIRONMENT_DISEASE_INTERFACE_AUDIT_01.json) now bind 31 class interfaces, four ancestry/background records, five spell records, 14 remedy cards, five pending bestiary records and 37 original-book paragraphs. Eight authoring requirements and 12 future case specifications identify the remaining disease procedure work. This is an unsent source audit, not a new disease ruleset or approval. Part4 revision03 remains the current live joint review.\n\n'
    split=text.find('\n\n',text.find('**Current joint review:**'));assert split>=0
    text=text[:split+2]+note+text[split+2:];start.write_text(text,encoding='utf-8',newline='\n')
    coverage=json.loads(originals[ledger]);before=deepcopy(coverage);row=next(x for x in coverage['aspects'] if x['id']=='DD-22');oldrow=deepcopy(row)
    row['draftEvidence'].append(audit.relative_to(G).as_posix())
    row.setdefault('currentEvidenceAddenda',[]).append({'id':'environment-disease-interface-audit01','recordedAtUtc':now,'sourceFiles':33,
      'currentClassCards':31,'sourceBookParagraphs':37,'findingGroups':8,'futureCaseSpecifications':12,'submitted':False,'newRulesAdopted':False})
    for key in ['status','closure','humanEvidence','completionClass']:assert row[key]==oldrow[key]
    assert [v for v in coverage['aspects'] if v['id']!='DD-22']==[v for v in before['aspects'] if v['id']!='DD-22']
    ledger.write_bytes(encoded(coverage))
    code=originals[nav].decode();tail=' + read(A / "RELIC_NULL_03_SUBMISSION_01_NAVIGATION_DELTA.json")["changes"]\n';assert code.count(tail)==1
    code=code.replace(tail,tail.rstrip('\n')+' + read(A / "DISEASE_INTERFACE_AUDIT_01_NAVIGATION_DELTA.json")["changes"]\n',1)
    code=code.replace('    pending = [\n','    pending = [\n        '+repr(('Environment — exact disease interfaces and authoring requirements',audit.name))+',\n',1)
    compile(code,str(nav),'exec');nav.write_text(code,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in saved if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [start,ledger,nav]]
    changes[0]['operations']=[{'oldCheckpoint':old,'replacementCheckpoint':new,'insertedParagraph':note}]
    changes[1]['operations']=[{'aspectId':'DD-22','old':oldrow,'replacement':row}]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'newRulesAdopted':False,'fullDomainClosureChanged':False,'humanOrOwnerEvidenceChanged':False}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:print(run.stdout[-1000:]);print(run.stderr[-2500:]);raise SystemExit(run.returncode)
    build=read(A/'REVIEW_MAP_BUILD.json');assert not build['missingLinks']
    state=read(previous);state.update(recordedAtUtc=now,previousCheckpoint=info(previous),goalTurnClassification='progress',previousGoalTurnClassification='progress',
      status='Part4 revision03 still actively generating, with exact archive/source acknowledgement and new progress on return/lifecycle corrections. Independently completed and linked the33-source disease interface audit:31 class cards,37 original paragraphs,eight authoring requirements and12 future cases. No new rules adopted.',
      coverageDelta=info(delta),coverageLedger=info(ledger),ownerStartPage=info(start),newRuleAdoptions=0,
      newRuleAdoptionScope='Source-interface audit only; no disease or cosmology rule applied.',
      navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':build['existingDistinctLinks'],'missingLinks':[]})
    state['environmentDiseaseInterfaceAudit']=info(audit)
    state['activeGptReview']['lastBrowserObservation']={'recordedAtUtc':now,'heading':'Patching revision 03 compliance corrections','stopVisible':True,
      'progress':'GPT states it is removing universal clock freezing from Return Hold and preserving actual form/concentration/life/duration/expiry clocks. This is progress text, not the finished returned rule.'}
    state['safeNextActions'].append('For the later HZ09 disease conference, use ENVIRONMENT_DISEASE_INTERFACE_AUDIT_01.json. It preserves exact interfaces/statuses and future case specifications; it does not authorize adopting a new disease baseline or pending Contagion/Plague Wind/bestiary rules.')
    state['resumedBlockedAudit']={'classification':'progress','previousConnectionBlockerResolved':True,'evidence':info(audit),
      'meaningfulProgress':'New33-source disease interface audit completed while same actual Part4 response remains live.'}
    state.setdefault('preservationManifests',[]).append(info(keep/'PRESERVATION_MANIFEST.json'));target.write_bytes(encoded(state))
    print(json.dumps({'checkpoint':info(target),'audit':info(audit),'links':build['existingDistinctLinks'],'missingLinks':0,'newRulesAdopted':False}))

if __name__=='__main__':main()
