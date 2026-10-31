from __future__ import annotations
import datetime as dt, hashlib, json, zlib, zipfile
from pathlib import Path, PurePosixPath
ROOT=Path.cwd(); A=ROOT/'docs/audit/2026-10-08/full-game/director-spell-review-129'
OUT=A/'rank9_defenseform8_current_source_308_prepared'
PACKET=OUT/'DD_Rank9_DefenseForm8_CurrentSource_308.zip'; DELIVERY=OUT/'DD_Rank9_DefenseForm8_CurrentSource_308_DELIVERY.json'
PREP=A/'RANK9_DEFENSEFORM8_SOURCE_PREPARATION_308.json'; PRIOR_PACKET=A/'rank9_defenseform8_source_packet_218_refreshed/DD_Rank9_DefenseForm8_CurrentSource_218.zip'
PRIOR_RETURN=A/'rank9_defenseform8_return218_received/DD_Rank9_DefenseForm5_Director_Return218.zip'; PRIOR_DELIVERY=A/'rank9_defenseform8_return218_received/DD_Rank9_DefenseForm5_Director_Return218_DELIVERY.json'
AUTH={'reviewedApplied':822,'pending':26,'acceptedUnapplied':0,'completeStandaloneProcedures':546,'scopedInterfaces':173}; CHECKS=[]
def digest(b): return (len(b),hashlib.sha256(b).hexdigest(),f'{zlib.crc32(b)&0xffffffff:08x}')
def check(name,ok,detail=None): CHECKS.append({'check':name,'passed':bool(ok),'detail':detail})
def main():
 delivery=json.loads(DELIVERY.read_text(encoding='utf-8-sig')); raw=PACKET.read_bytes(); check('outer archive matches delivery bytes/hash/CRC',digest(raw)==(delivery['archive']['bytes'],delivery['archive']['sha256'],delivery['archive']['crc32']))
 with zipfile.ZipFile(PACKET) as z:
  names=z.namelist(); ns=set(names); unsafe=[n for n in names if not n or '\\' in n or PurePosixPath(n).is_absolute() or any(x in ('','.','..') for x in PurePosixPath(n).parts)]
  check('ZIP integrity, unique safe names, exact allowlist',z.testzip() is None and len(names)==len(ns) and not unsafe and set(delivery['exactAllowlist'])==ns and delivery['memberCount']==len(ns),{'members':len(names),'unsafe':unsafe})
  external={x['path']:x for x in delivery['members']}; extbad=[n for n in names if n not in external or digest(z.read(n))!=(external[n]['bytes'],external[n]['sha256'],external[n]['crc32'])]
  manifest=json.loads(z.read('MEMBER_MANIFEST.json')); internal={x['path']:x for x in manifest['members']}; payload=ns-{'MEMBER_MANIFEST.json'}
  intbad=[n for n in payload if n not in internal or digest(z.read(n))!=(internal[n]['bytes'],internal[n]['sha256'],internal[n]['crc32'])]
  check('every archive member binds externally and every payload binds internally',not extbad and not intbad and set(internal)==payload and manifest['memberCountExcludingSelf']==len(payload),{'externalErrors':extbad[:5],'internalErrors':intbad[:5]})
  candidate=json.loads(z.read('current/CURRENT_SOURCE_CONFERENCE_CANDIDATE_308.json')); sources=candidate['sourceBindings']; sourcebad=[]
  for row in sources:
   member='sources_current/'+row['path']; p=ROOT/PurePosixPath(row['path'])
   if member not in ns or digest(z.read(member))!=(row['bytes'],row['sha256'],row['crc32']) or not p.exists() or digest(p.read_bytes())!=(row['bytes'],row['sha256'],row['crc32']): sourcebad.append(row['path'])
  check('87 current source bindings match archive and worktree',len(sources)==87 and not sourcebad,{'count':len(sources),'errors':sourcebad[:5]})
  with zipfile.ZipFile(PRIOR_PACKET) as old:
   oc=json.loads(old.read('CURRENT_SOURCE_CONFERENCE_CANDIDATE_218.json')); changes=[]
   for row in sources:
    m='sources_current/'+row['path']
    if m not in old.namelist() or z.read(m)!=old.read(m): changes.append(row['path'])
  disclosed=[x['path'] for x in candidate['sourceBindingRefresh']['changedFromReturn218Packet']]
  check('single changed source since Return218 packet is disclosed exactly',changes==disclosed and changes==['DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'],changes)
  index=json.loads(z.read('current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json')); catalog=json.loads(z.read('current/DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json'))
  q=json.loads(z.read('current/CURRENT_SPELL_QUEUE_307.json')); h=json.loads(z.read('current/CURRENT_HANDOFF_307.json')); p=json.loads(z.read('current/CURRENT26_PENDING_IDENTITY_AUDIT_307.json'))
  entry=next(x for x in index['entries'] if x['id']=='timeless-form'); spell=next(x for x in catalog['spells'] if x['id']=='timeless-form'); tsentry=next(x for x in index['entries'] if x['id']=='time-stop'); tsspell=next(x for x in catalog['spells'] if x['id']=='time-stop')
  check('authority and Timeless Form pending/non-operational state exact',delivery['authority']==AUTH and index['authoredCounts']=={'reviewed':822,'pending':26} and entry['authoredStatus']=='pending-authored-procedure' and spell.get('operational') is None,{'authority':delivery['authority'],'timelessStatus':entry['authoredStatus'],'operational':spell.get('operational')})
  check('Time Stop remains pending/non-operational and pending audit includes it',tsentry['authoredStatus']=='pending-authored-procedure' and tsspell.get('operational') is None and 'time-stop' in p['pendingIds'],{'timeStopStatus':tsentry['authoredStatus'],'operational':tsspell.get('operational')})
  check('only Timeless Form is in adjudication scope',delivery['targetIds']==['timeless-form'] and manifest['targetPendingIds']==['timeless-form'] and candidate['currentReviewTargets'][0]['spellId']=='timeless-form' and candidate['currentPendingGroup']['spellIds']==['timeless-form'],delivery['targetIds'])
  check('current 307 queue/handoff/pending inputs and authority bind; parent files remain exact',q['currentAuthority']==h['currentAuthority']==p['authority']==AUTH and h['currentPreparation']['pendingIds']==['timeless-form','invulnerable-sphere'] and p['pendingCount']==26 and digest(z.read('current/CURRENT_HANDOFF_307.json'))==digest((A/'CURRENT_HANDOFF_307.json').read_bytes()) and digest(z.read('current/CURRENT_SPELL_QUEUE_307.json'))==digest((A/'CURRENT_SPELL_QUEUE_307.json').read_bytes()),{'authority':h['currentAuthority'],'next':h['currentPreparation']['pendingIds']})
  fw=json.loads(z.read('current/FINAL_WORD_DIRECTOR_DECISION_303.json')); sh=json.loads(z.read('current/ELEMENTAL_SHELL_DIRECTOR_DECISION_306.json'))
  check('Final Word and Elemental Shell holds remain preserved with no acceptance/application',fw['heldIds']==['final-word'] and fw['acceptedIds']==fw['appliedIds']==[] and sh['heldIds']==['elemental-shell'] and sh['acceptedIds']==sh['appliedIds']==[],{'finalWord':fw['heldIds'],'shell':sh['heldIds']})
  with zipfile.ZipFile(PRIOR_RETURN) as old:
   od=json.loads(PRIOR_DELIVERY.read_text(encoding='utf-8-sig')); ext={x['path']:x for x in od['members']}; im=json.loads(old.read('MEMBER_MANIFEST.json')); imap={x['path']:x for x in im['members']}; ci=json.loads(old.read('CASE_INDEX.json')); cases=[x for x in ci['cases'] if x.get('spellId')=='timeless-form']; bad=[]
   for row in cases:
    name=row['path']; original=old.read(name); target='history/Return218/'+name
    if target not in ns or z.read(target)!=original: bad.append(name+'#packet')
    for table in (ext,imap):
     bind=table.get(name)
     if bind is None or digest(original)!=(bind['bytes'],bind['sha256'],bind['crc32']): bad.append(name+'#source-binding')
  check('all 11 prior Timeless Form cases are byte-exact to both Return218 manifests',len(cases)==11 and not bad,{'count':len(cases),'errors':bad[:5]})
  procedures=json.loads(z.read('history/Return218/PROCEDURES.json')); proc=next(x for x in procedures['spells'] if x.get('spellId')=='timeless-form')
  check('prior Timeless Form procedure and qualifications are preserved',proc['accepted'] is False and proc['applied'] is False and 'DF218-B03' in proc['holds'] and proc['conditionalQualificationIds']==['DF218-Q-AGING'] and len(proc['caseIds'])==11,{'holds':proc['holds'],'conditional':proc['conditionalQualificationIds'],'cases':len(proc['caseIds'])})
  req=json.loads(z.read('current/TIMELESS_FORM_DIRECTOR_REQUIREMENTS_308.json')); request=z.read('current/REQUEST_308.txt').decode('utf-8')
  check('Director requirements and packet request match exact DF218-B03 minimum evidence and scope',req['scopeIds']==['timeless-form'] and req['blockerIds']==['DF218-B03'] and len(req['minimumClosureEvidence'])==3 and 'Time Stop itself remains pending' in request and 'DF218-B03' in request and 'do not manufacture a positive trace' in request and 'Invulnerable Sphere remains next' in request,{'scope':req['scopeIds'],'blocker':req['blockerIds'],'requestBytes':len(request)})
  check('packet records no acceptance/application, canonical change, or runtime claim',delivery['canonicalChanges'] is False and delivery['githubChanges'] is False and delivery['runtimeExecuted'] is False and delivery['sourceProgramsExecuted'] is False and delivery['targetIds']==['timeless-form'],{k:delivery[k] for k in ('canonicalChanges','githubChanges','runtimeExecuted','sourceProgramsExecuted')})
 prep=json.loads(PREP.read_text(encoding='utf-8-sig')); check('prep record matches one target, 87 sources, 11 cases and current authority',prep['sourceAuthority']==AUTH and prep['pendingIds']==['timeless-form'] and prep['currentSourceFileCount']==87 and prep['targetCaseCountFromReturn218']==11 and prep['canonicalChanges'] is False and prep['githubChanges'] is False,{'targets':prep['pendingIds'],'sources':prep['currentSourceFileCount'],'cases':prep['targetCaseCountFromReturn218']})
 failed=[x for x in CHECKS if not x['passed']]; report={'id':'TIMELESS-FORM-PACKET-308-INDEPENDENT-AUDIT','recordedAtUtc':dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),'status':'PASS' if not failed else 'FAIL','archive':{'path':PACKET.relative_to(ROOT).as_posix(),**dict(zip(('bytes','sha256','crc32'),digest(raw)))} ,'delivery':{'path':DELIVERY.relative_to(ROOT).as_posix(),**dict(zip(('bytes','sha256','crc32'),digest(DELIVERY.read_bytes())))} ,'authority':AUTH,'targetIds':['timeless-form'],'checkCount':len(CHECKS),'passedChecks':len(CHECKS)-len(failed),'failedChecks':len(failed),'checks':CHECKS,'acceptedIds':[],'appliedIds':[],'canonicalChanges':False,'runtimeExecuted':False}
 out=A/'TIMELESS_FORM_PACKET_308_INDEPENDENT_AUDIT.json'; out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'status':report['status'],'checks':f'{report["passedChecks"]}/{report["checkCount"]}','archiveSha256':report['archive']['sha256'],'audit':str(out),'failed':failed},indent=2)); assert not failed
if __name__=='__main__': main()
