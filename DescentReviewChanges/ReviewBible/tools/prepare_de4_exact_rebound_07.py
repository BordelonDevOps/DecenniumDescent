"""Prepare complete, explicitly pending DE4 artifacts and rebind every changed active mirror.

No live target is written. Historical records and sealed AC6 payloads stay byte-identical.
"""
from copy import deepcopy
from datetime import datetime, timezone
import json,hashlib,re
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at

def read(p):return json.loads(p.read_bytes())
def main():
 out=A/'de4-exact-rebound-07';checkp=A/'DE4_EXACT_REBOUND_07_CHECK.json';prep=A/'DE4_EXACT_REBOUND_07_PREPARATION.json'
 assert not any(p.exists() for p in [out,checkp,prep])
 now=datetime.now(timezone.utc).isoformat();curp=R/'data/director/spell_proposals/divination_enchantment_rank4_current_07.json';cur=read(curp);amendp=A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_04.json';amend=read(amendp);review=A/'de4-review-followup-06-review-final/REVIEW.json';receipt=A/'DE4_REVIEW_FOLLOWUP_06_FINAL_RECEIPT.json'
 checks=[];buffers={};before={};changes=[]
 def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
 def rel(p):return p.relative_to(G).as_posix()
 def planned(p,raw):return info(p,raw)
 def put(name,raw):assert name not in buffers;buffers[name]=raw
 def targetraw(p):return buffers['proposed/'+rel(p)]
 def targetjson(p):return json.loads(targetraw(p))
 def savejson(p,d):buffers['proposed/'+rel(p)]=encoded(d)
 for f in amend['plannedActiveRepresentationChanges']:
  p=G/f['source']['path'];raw=p.read_bytes();ck('Live baseline '+rel(p),info(p)==f['source']);before[p]=raw
  proposed=G/f['proposedWholeFile']['path'];ck('Exact reviewed semantic mirror '+p.name,info(proposed)==f['proposedWholeFile'])
  put('before/'+rel(p),raw);put('proposed/'+rel(p),proposed.read_bytes())
 catalog=R/'data/public/spell_playtests/catalog.json';guide=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md';indexp=R/'data/public/spell_playtests/authored_review_index.json'
 original_catalog=read(catalog);newcat=targetjson(catalog);fateids={'mark-omen','fate-coin'}
 provenance={'developmentDirection':'video-game-only','status':'PENDING exact-file acceptance; these are staged bytes, not live adoption.','semanticReview':info(review),'actualReviewReceipt':info(receipt),'meaning':'The earlier two-spell guard remains historical authorship. The DE4 extension supplies the three-spell guard, explicit digital RNG mapping and five-entry disclosure policy after separate exact acceptance. This does not alter original source/access or add any class feature to the guard.','noRuntimeOrBalanceApproval':True}
 interpretation='CURRENT DE4 EXTENSION (staged pending exact-file acceptance): the operative limitations now contain the separately reviewed three-spell Mark Omen/Fate Coin/Fate Reversal lineage guard and DE4-RNG-05/DE4-PRESENTATION-06. Earlier designNotes and rank-one review evidence describe the historical two-spell rule. The later review is recorded separately; neither that history nor this extension grants unlisted hidden RNG information, class access, runtime execution or balance approval.'
 for i,s in enumerate(newcat['spells']):
  old=original_catalog['spells'][i]
  ck('Catalog identity/source/access '+s['id'],all(s[k]==old[k] for k in old if k!='operational'))
  if s['id'] in fateids:
   s['operational']['currentInterpretation']=interpretation;s['operational']['de4ExtensionEvidence']={'semanticReview':info(review),'correctionReceipt':info(receipt),'pendingExactFileAcceptance':True}
  else:ck('Unrelated catalog card unchanged '+s['id'],s==old)
 savejson(catalog,newcat);catbind=planned(catalog,targetraw(catalog));byid={s['id']:s for s in newcat['spells']}
 # Preserve the old whole-file binding and change discovery metadata only; membership waits for receipt.
 before[indexp]=indexp.read_bytes();put('before/'+rel(indexp),before[indexp]);idx=read(indexp);oldidx=deepcopy(idx)
 ck('Baseline authored counts',idx['authoredCounts']=={'reviewed':465,'pending':383});ck('Index catalog baseline',idx['sourceCatalogSha256']==info(catalog)['sha256'])
 idx.setdefault('sourceCatalogBindingHistory',[]).append({'binding':info(catalog),'reason':'Before proposed DE4 Fate extension; preserved before bytes are supplied with the exact candidate.'});idx['sourceCatalogSha256']=catbind['sha256'];idx['currentSourceCatalogBinding']=catbind
 put('proposed/'+rel(indexp),encoded(idx));ck('All848 discovery entries unchanged',idx['entries']==oldidx['entries']);ck('Standalone and review counts unchanged',idx['representationCounts']==oldidx['representationCounts'] and idx['authoredCounts']==oldidx['authoredCounts'])
 # The two rank-one draft mirrors have the same added provenance as their complete catalog cards.
 for name in ['candidate_divination_rank1.json','batch_divination_rank1.json']:
  p=R/'data/playtest/spell_drafts'/name;d=targetjson(p)
  for s in d['spells']:
   if s['id'] in fateids:
    op=byid[s['id']]['operational']
    for k in ['currentInterpretation','de4ExtensionEvidence']:s[k]=deepcopy(op[k])
    ck('Draft operational fields '+name+s['id'],all(v==op[k] for k,v in s.items()))
  d['de4IntegrationProvenance']=deepcopy(provenance);savejson(p,d)
 # 202 catalog-bound feat dependency rows receive the exact new whole-file binding.
 depsp=R/'data/public/feat_candidates/exact_01/spell_dependencies.json';deps=targetjson(depsp);olddeps=read(depsp);rebound=[]
 for ident,s in deps['spells'].items():
  prior=olddeps['spells'][ident];ck('Immutable original public dependency '+ident,s['originalCatalogRecord']==prior['originalCatalogRecord'])
  if s['binding']['file']==rel(catalog):
   ptr=s['binding']['pointer'];card=at(newcat,ptr);ck('Same dependency identity '+ident,card['id']==ident)
   if ident in fateids:s['completeCurrentProcedureCard']=deepcopy(card)
   ck('Entire current public dependency '+ident,s['completeCurrentProcedureCard']==card)
   s['binding']={**s['binding'],'bytes':catbind['bytes'],'sha256':catbind['sha256']};rebound.append(ident)
 deps['de4IntegrationProvenance']={**deepcopy(provenance),'priorCatalogBinding':info(catalog),'currentCatalogBinding':catbind,'catalogRowsRebound':rebound};savejson(depsp,deps)
 # Guide bytes are exactly the agreed proposed prose, including explicit new-authorship history.
 guidetext=targetraw(guide).decode('utf-8').replace('\r\n','\n');guidebind=planned(guide,targetraw(guide));heading='Mark Omen and Fate Coin: reviewed spell-specific rerolls'
 match=re.search(r'^## '+re.escape(heading)+r'\n.*?(?=^## |\Z)',guidetext,re.M|re.S);assert match;fate_excerpt=match.group(0)
 ck('Complete agreed policy in guide',amend['proposedSourcePresentationPolicy06']['exactText'] in fate_excerpt)
 excerpt_refresh=[];general_rebound=[]
 for name in ['magic_extended','general_combat']:
  p=R/f'data/director/feat_candidates/exact_01/cohorts/{name}.json';d=targetjson(p);old=read(p);prior_excerpts=[]
  for i,e in enumerate(d['currentGoverningExcerpts']):
   if e['file']!=rel(guide):continue
   prior_excerpts.append({'pointer':'/currentGoverningExcerpts/'+str(i),'completePriorRecord':deepcopy(old['currentGoverningExcerpts'][i]),'completeReviewedProposedRecord':deepcopy(e)})
   if e['heading']==heading:
    ck('Same complete proposed Fate lines before ordering refresh '+name,sorted(x for x in e['exactText'].splitlines() if x.strip())==sorted(x for x in fate_excerpt.splitlines() if x.strip()))
    e['exactText']=fate_excerpt
   ck('Current full excerpt occurs in guide '+name+str(i),e['exactText'] in guidetext)
   e['sha256']=guidebind['sha256'];e['currentWholeFileBinding']=guidebind;e['excerptEncoding']='UTF-8 decoded text with CRLF normalized to LF; whole-file hash binds unchanged raw bytes.'
   e['preparedWholeFileSha256']=old['currentGoverningExcerpts'][i].get('preparedWholeFileSha256',old['currentGoverningExcerpts'][i]['sha256'])
   e['preparedExcerptStillExact']=old['currentGoverningExcerpts'][i]['exactText']==e['exactText'];e['wholeFileChangedSincePreparation']=e['preparedWholeFileSha256']!=guidebind['sha256'];excerpt_refresh.append(name+':'+str(i))
  d['de4PriorGoverningExcerptRecords']=prior_excerpts
  if name=='general_combat':
   for ident,s in d['completeCurrentSpellDependencies'].items():
    prior=old['completeCurrentSpellDependencies'][ident];ck('Immutable original general dependency '+ident,s['completeOriginalCatalogObject']==prior['completeOriginalCatalogObject'])
    if s['currentProcedureFile']==rel(catalog):
     ptr=s['currentAuthoredIndexEntry']['wholeCardPointer'];card=at(newcat,ptr)
     if ident in fateids:s['completeCurrentProcedureCard']=deepcopy(card)
     ck('Entire general current card '+ident,s['completeCurrentProcedureCard']==card)
     s['currentProcedureBinding']={'file':rel(catalog),'bytes':catbind['bytes'],'sha256':catbind['sha256'],'pointer':ptr};general_rebound.append(ident)
  d['de4IntegrationProvenance']={**deepcopy(provenance),'currentGuideBinding':guidebind,'historicalSourceFilesUnchanged':True};ck('Historical cohort sourceFiles unchanged '+name,d['sourceFiles']==old['sourceFiles']);savejson(p,d)
 ck('Expected public dependency count',len(rebound)==202);ck('Expected general dependency count',len(general_rebound)==196);ck('Eleven guide excerpt bindings',len(excerpt_refresh)==11)
 # Machine-readable changed-leaf records distinguish all history from current metadata.
 def diff(a,b,pointer=''):
  if isinstance(a,dict) and isinstance(b,dict):
   result=[]
   for k in sorted(set(a)|set(b)):
    q=pointer+'/'+k.replace('~','~0').replace('/','~1')
    if k not in a:result.append({'operation':'add','pointer':q,'after':b[k]})
    elif k not in b:raise AssertionError('No deletion permitted: '+q)
    else:result.extend(diff(a[k],b[k],q))
   return result
  if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):return [x for i,(u,v) in enumerate(zip(a,b)) for x in diff(u,v,pointer+'/'+str(i))]
  return [] if a==b else [{'operation':'replace','pointer':pointer,'before':a,'after':b}]
 for p,raw in before.items():
  after=targetraw(p);row={'target':rel(p),'before':planned(p,raw),'after':planned(p,after),'preservedBefore':'before/'+rel(p),'proposedFile':'proposed/'+rel(p),'status':'STAGED ONLY; exact-file acceptance required'}
  if p.suffix=='.json':row['operations']=diff(json.loads(raw),json.loads(after))
  else:row['proseScope']='Byte-identical to proposed mirror verified in Followup06; no additional prose change';ck('Reviewed prose unchanged '+p.name,after==(A/'de4-review-revision-06/proposed'/p.relative_to(G)).read_bytes())
  changes.append(row)
 ck('Ten exact integration targets',len(changes)==10)
 plan={'id':'DE4-EXACT-REBIND-07-INTEGRATION-PLAN','createdAtUtc':now,'status':'UNADOPTED; no live file modified','semanticReview':info(review),'currentCandidate':info(curp),'changes':changes,'provenance':provenance,'unchangedAuthoredCounts':{'reviewed':465,'pending':383},'afterAcceptanceOnly':{'authoredCounts':{'reviewed':480,'pending':368},'completeStandaloneProcedures':204,'newSpellIds':[s['spellId'] for s in cur['spells']],'instructions':'After actual exact acceptance, preserve the live index baseline and install these exact ten target bytes plus byte-identical model/casebook/chapters. Then separately record acceptance/discovery membership with the actual receipt and refresh the interface registry; no present or unseen acceptance is claimed.'},'publicCatalogRowsRebound':rebound,'generalCombatCatalogRowsBound':general_rebound,'governingExcerptBindingsRefreshed':excerpt_refresh,'sealedAC6PayloadsChanged':False}
 put('INTEGRATION_PLAN.json',encoded(plan))
 model=deepcopy(cur);model['id']='DE4-EXACT-MODEL-07';model['status']='Pending exact authored-file acceptance for video-game development; no runtime/human/balance/canon/release approval.'
 for s in model['spells']:s['id']=s['spellId']
 model['exactIntegration07']={'input':info(curp),'semanticReview':info(review),'caseDelta':'Only the exact N04 adjective correction from Followup06; all15 procedures and allsharedRules remain identical to Current06.','plannedCurrentBindings':[x['after'] for x in changes],'referenceResolution':'The sourceBindings are frozen before-source evidence, not a claim that all stay current after integration. Current rule references to a changed target resolve the proposedFile named in INTEGRATION_PLAN. Historical/original/source-preservation fields retain frozen before bytes. Current07 self-references resolve the complete immutable Current07 input included among sources. All unchanged source paths resolve their exact frozen bytes.','historicalCurrent07RecordPreserved':True}
 put('SPELLS_MODEL.json',encoded(model));cb={'id':'DE4-EXACT-CASEBOOK-07','status':'37 authored source-grounded cases; not engine execution','input':info(curp),'cases':deepcopy(cur['currentExamples']),'historicalOriginalTexts':deepcopy(cur['originalExamplesUnchanged']),'historicalOriginalSharedProposal':deepcopy(cur['originalSharedProposalUnchanged']),'historicalOriginalIssues':deepcopy(cur['originalIssuesUnchanged']),'referenceResolution':model['exactIntegration07']['referenceResolution']};put('CASEBOOK.json',encoded(cb))
 # Both complete manuscripts carry every procedure field and all shared rules verbatim.
 def render(value,level=3):
  if isinstance(value,str):return value+'\n\n'
  if isinstance(value,dict):return ''.join('#'*min(level,6)+' '+str(k)+'\n\n'+render(v,level+1) for k,v in value.items())
  if isinstance(value,list):return ''.join(render(v,level) for v in value)
  return json.dumps(value,ensure_ascii=False)+'\n\n'
 body='## Shared rules\n\n'+render(model['sharedRules'])
 for s in model['spells']:
  body+='## '+s['completeSourceAndAccess']['name']+'\n\n'+render(s['procedure'])
 for name,title in [('PLAYER_CHAPTER.md','Divination and Enchantment rank four'),('DIRECTOR_REVIEW.md','DE4 complete procedures and review context')]:
  text='# '+title+'\n\nPending exact authored review for the video game. This complete manuscript preserves agreed procedure text; historical pending labels require the separate acceptance receipt to establish current authored status. Runtime implementation, human playtesting and balance remain open.\n\n'+body
  if name=='DIRECTOR_REVIEW.md':text+='## Full case evidence\n\nSee CASEBOOK.json for all37 current cases, all30 original texts, exact pointers and ledgers. Original source and access objects are retained in SPELLS_MODEL.json and all full sources are supplied.\n'
  put(name,text.encode())
 bindings={b['path']:b for b in cur['sourceBindings']}
 for p in [curp,amendp,review,receipt,A/'DE4_CURRENT_07_CHECK.json',A/'de4-review-followup-06-review-final/PROPOSED_CORRECTIONS.json',A/'de4-review-followup-06-review-final/VERDICT.md']+list(before):bindings[rel(p)]=info(p)
 for b in bindings.values():ck('Frozen source exact '+b['path'],info(G/b['path'])==b)
 put('SOURCE_HASHES.json',encoded({'id':'DE4-EXACT-07-SOURCES','scope':'Frozen original inputs. Proposed updated current bytes have separate target bindings in INTEGRATION_PLAN.','bindings':list(bindings.values())}))
 register={'id':'DE4-EXACT-07-REGISTER','status':'REQUEST_EXACT_FILE_ACCEPTANCE','developmentDirection':'video-game-only','reviewBasis':[info(review),info(A/'de4-digital-conference-05-review-final/REVIEW.json')],'singleCaseCorrection':info(A/'de4-review-followup-06-review-final/PROPOSED_CORRECTIONS.json'),'spellIds':[s['id'] for s in model['spells']],'spellCount':15,'placements':sum(len(s['completeSourceAndAccess']['source']['original']['placements']) for s in model['spells']),'caseIds':[c['id'] for c in cb['cases']],'currentCaseCount':37,'historicalOriginalTexts':30,'integrationTargetCount':10,'scope':'Confirm exact one-word N04 correction, complete mirrors/provenance and binding-only integration. Retain settled substantive decisions and AC6 closure. No fresh full-cohort semantic review is requested.','noSourceInformationDeleted':True,'runtimeImplemented':False,'humanPlaytested':False,'balanceApproved':False,'cosmologyCanonModified':False,'domainGateStatusChanged':False,'countsBeforeAcceptance':{'reviewed':465,'pending':383}}
 ck('Fifteen IDs / seventeen placements',len(set(register['spellIds']))==15 and register['placements']==17);ck('Thirty-seven current and thirty original',len(cb['cases'])==37 and len(cb['historicalOriginalTexts'])==30)
 for s,old in zip(model['spells'],cur['spells']):
  ck('Complete procedure unchanged '+s['id'],s['procedure']==old['procedure']);ck('Original source/access preserved '+s['id'],s['completeSourceAndAccess']==old['completeSourceAndAccess'])
  for name in ['PLAYER_CHAPTER.md','DIRECTOR_REVIEW.md']:ck('Complete procedure rendered '+s['id']+name,render(s['procedure']) in buffers[name].decode())
 ck('Entire shared rules unchanged',model['sharedRules']==cur['sharedRules']);put('REGISTER.json',encoded(register))
 for p,raw in before.items():ck('Live target remains untouched '+rel(p),p.read_bytes()==raw)
 manifest={'id':'DE4-EXACT-07-MANIFEST','status':'Pending actual GPT exact review','files':[{'name':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in buffers.items()],'scope':'Every candidate payload except this manifest; outer archive covers manifest. Before and proposed bytes are distinct.'};put('EVIDENCE_MANIFEST.json',encoded(manifest))
 out.mkdir()
 for n,raw in buffers.items():p=out/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 checkp.write_bytes(encoded({'id':'DE4-EXACT-REBOUND-07-CHECK','recordedAtUtc':now,'checks':checks,'checkCount':len(checks),'failureCount':0,'manifest':info(out/'EVIDENCE_MANIFEST.json'),'frozenSourceCount':len(bindings),'integrationTargets':10,'activeFilesModified':0,'runtimeTestsExecuted':0,'scope':'Exact hash/source preservation, whole-card/excerpt equality, complete rendering, pointer-discovery and authorized narrow correction. Not game-engine testing.'}))
 prep.write_bytes(encoded({'id':'DE4-EXACT-REBOUND-07-PREPARATION','recordedAtUtc':now,'candidate':info(curp),'manifest':info(out/'EVIDENCE_MANIFEST.json'),'check':info(checkp),'payloads':len(buffers),'sources':len(bindings),'integrationTargets':10,'counts':{'reviewed':465,'pending':383},'status':'Prepared, UNSENT, UNADOPTED'}));print(json.dumps({'preparation':info(prep),'checks':len(checks),'sources':len(bindings),'payloads':len(buffers),'activeFilesModified':0}))

if __name__=='__main__':main()
