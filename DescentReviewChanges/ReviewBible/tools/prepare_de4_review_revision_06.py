"""Assemble GPT's exact corrections as a new pending revision; preserve all sources."""
from copy import deepcopy
from datetime import datetime,timezone
import json,hashlib
from apply_di7_ap_as_01 import G,R,A,info,encoded
from prepare_ac5_current_interfaces_01 import at
from prepare_de4_fate_guard_amendment_01 import parent

def read(p):return json.loads(p.read_bytes())

def main():
 reviewdir=A/'de4-digital-conference-05-review-final';oldp=R/'data/director/spell_proposals/divination_enchantment_rank4_current_05.json';newp=oldp.with_name('divination_enchantment_rank4_current_06.json');oldg=A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_03.json';newg=A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_04.json';keep=A/'de4-review-revision-06';checkp=A/'DE4_REVIEW_REVISION_CHECK_06.json'
 assert not any(p.exists() for p in [newp,newg,keep,checkp])
 old=read(oldp);d=deepcopy(old);g=read(oldg);ng=deepcopy(g);cor=read(reviewdir/'PROPOSED_CORRECTIONS.json');addition=read(reviewdir/'ADDITIONAL_CASES.json');checks=[]
 def ck(n,ok):checks.append({'check':n,'passed':bool(ok)});assert ok,n
 ck('Exact reviewed candidate',info(oldp)==cor['inputCandidate']);ck('Exact reviewed amendment',info(oldg)==cor['inputAmendment'])
 for b in read(reviewdir/'EVIDENCE_MANIFEST.json')['files']:
  raw=(reviewdir/b['name']).read_bytes();ck('Verified Director payload '+b['name'],len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'])
 # Exact downloaded data operations, never executing downloaded code.
 for i,o in enumerate(cor['operations']):
  target=d if o['file']==oldp.relative_to(G).as_posix() else ng
  ck('Known operation target '+str(i),o['file'] in [oldp.relative_to(G).as_posix(),oldg.relative_to(G).as_posix()])
  node,key=parent(target,o['pointer'])
  if o['operation']=='replace':ck('Exact before '+str(i),node[key]==o['before']);node[key]=deepcopy(o['after'])
  else:ck('New key '+str(i),o['operation']=='add' and key not in node);node[key]=deepcopy(o['value'])
 d['currentExamples']+=deepcopy(addition['cases'])
 exact_gpt_policy=d['sharedRules']['DE4-PRESENTATION-06']
 # Explicit bounded addition for conference: event existence must not reveal hidden occupants.
 existence='NEW BURNING-HANDS EVENT-EXISTENCE COMPLETION FOR CONCURRENCE: For this source only, each actually manifested Burning Hands cone generates exactly one complete original shared3d6 operation at its ordinary damage-resolution checkpoint whether the eligible recipient set is empty, entirely hidden, or includes known recipients. It is the same cast operation, not an extra roll, attack or damage packet per recipient. A cast interrupted or prevented before manifestation generates none. A manifested empty cone deals no damage and triggers no hit/damage/Wound/kill/resource consequence, even though its finite original pool is available under BURNING-HANDS-DAMAGE. Thus the presence, number, values, availability and timing of the published pool do not encode whether hidden recipients exist. No target list, saves, defenses or damage outcome is added to this presentation. A paid Coin may alter that original empty-cone pool only through its ordinary actual predicates, with its normal consumed item/Reaction/guard and no refunded cost; it creates no recipient or successful damage event. This is explicit NEW per-source RNG-generation authorship, not a rule for other empty areas or unlisted spells.'
 policy=exact_gpt_policy+'\n\n'+existence
 d['sharedRules']['DE4-PRESENTATION-06']=policy;ng['proposedSourcePresentationPolicy06']['exactText']=policy
 ng['proposedSourcePresentationPolicy06']['CodexConcurrence']='Concur with the five explicitly bounded GPT entries in principle; the attached exact candidate includes one additional empty-cone event-existence completion requiring GPT disposition before final acceptance.'
 before_public=d['currentExamples'][18]['actionsAndResolution'][0]
 ck('N19 private wording source exists',before_public.startswith('Public engine uniform d3'))
 d['currentExamples'][18]['actionsAndResolution'][0]=before_public.replace('Public engine uniform d3','Privately presented engine uniform d3',1)
 # The old review did not approve the later digital policy. Correct three operative mirrors.
 source_doc=R/'docs/mechanics/SPELL_INTEGRATION_RULES.md'
 original_para=next(x for x in source_doc.read_text(encoding='utf-8').split('\n\n') if x.startswith('The [rank-1 Divination exact review]'))
 bad_para=original_para.replace('normal table information rules','established gameplay-information rules under DE4-RNG-05')
 corrected_para=original_para.replace('requires Fate Coin to wait','established that Fate Coin waits').replace('normal table information rules','the information rules then specified')+' The NEW pending DE4 amendment separately proposes the three-spell guard, DE4-RNG-05 engine interpretation and DE4-PRESENTATION-06 source-specific disclosure policy. Those later proposals were not part of the earlier rank-1 review; they require their own exact acceptance.'
 keep.mkdir();preserved=[];newplans=[]
 for f in ng['plannedActiveRepresentationChanges']:
  p=G/f['source']['path'];raw=p.read_bytes();ck('Accepted source still exact '+p.name,info(p)==f['source'])
  saved=keep/'before'/p.relative_to(G);proposed=keep/'proposed'/p.relative_to(G);saved.parent.mkdir(parents=True,exist_ok=True);proposed.parent.mkdir(parents=True,exist_ok=True);saved.write_bytes(raw)
  nf=deepcopy(f)
  if p.suffix=='.json':
   v=read(p);v2=deepcopy(v)
   for op in nf['operations']:
    node,key=parent(v2,op['pointer']);ck('Proposed before '+p.name+op['pointer'],node[key]==op['before'])
    op['after']=op['after'].replace(bad_para,corrected_para)
    if ng['digitalRngContract'] in op['after']:op['after']=op['after'].replace(ng['digitalRngContract'],ng['digitalRngContract']+'\n\n'+policy)
    node[key]=op['after']
   rev=deepcopy(v2)
   for op in reversed(nf['operations']):node,key=parent(rev,op['pointer']);ck('Reverse after '+p.name+op['pointer'],node[key]==op['after']);node[key]=op['before']
   ck('Only explicit JSON changes '+p.name,rev==v);proposed.write_bytes(encoded(v2))
  else:
   text=raw.decode('utf-8');v2=text
   if p==source_doc:
    nf['replacements']=[x for x in nf['replacements'] if x['before']!='normal table information rules']
    nf['replacements'].append({'before':original_para,'after':corrected_para,'expectedOccurrences':1})
   for rep in nf['replacements']:
    ck('Literal prose count '+p.name+rep['before'][:35],v2.count(rep['before'])==rep['expectedOccurrences']);v2=v2.replace(rep['before'],rep['after'])
   v2=v2.replace(ng['proposedGuardVerbatim'],ng['proposedGuardVerbatim']+'\n\n'+ng['digitalRngContract']+'\n\n'+policy)
   nf['appendPresentationContractAfterEachDigitalContract']=policy
   proposed.write_text(v2,encoding='utf-8',newline='\n')
  nf['proposedWholeFile']=info(proposed);nf['metadataStatus']='Exact pending semantic proposal; final dependency/card/excerpt hashes still require full rebinding after conference. Not live adoption.';newplans.append(nf)
  ck('Live file unchanged '+p.name,p.read_bytes()==raw);preserved.append({'source':info(p),'before':info(saved),'proposed':info(proposed)})
 ng['plannedActiveRepresentationChanges']=newplans
 ng.update(id='DE4-FATE-GUARD-AMENDMENT-DRAFT-04',recordedAtUtc=datetime.now(timezone.utc).isoformat(),previousCompleteProposal=info(oldg),status='UNADOPTED full pending semantic revision with explicit presentation policy and corrected historical attribution; no live changes.')
 ng['localAdditionalCorrections06']={'historicalAttribution':{'originalParagraph':original_para,'priorProposedParagraph':bad_para,'proposedParagraph':corrected_para,'mirrors':3},'presentationGenerationCompletion':existence,'exactGPTPolicyPreserved':exact_gpt_policy}
 ng['sourceBindings'] += [info(oldg),info(reviewdir/'PROPOSED_CORRECTIONS.json'),info(reviewdir/'REVIEW.json')]
 newg.write_bytes(encoded(ng));(keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
 oldrel=oldp.relative_to(G).as_posix();newrel=newp.relative_to(G).as_posix()
 for c in d['currentExamples']:
  for ref in c.get('sourceRefs',[]):
   if ref['path']==oldrel:ref['path']=newrel
 d['currentExamples'].append({'id':'DE4-N37','spellId':'fate-reversal','title':'Burning Hands visible operation does not report hidden occupancy','status':'NEW proposed source-operation/presentation composition; not runtime execution','initialState':{'source':'actual catalog Burning Hands /spells/426/operational','cast':'one genuinely paid legal cast, operative manifestation; original caster/known cone perceived by controller H; no new cast or class access granted by fixture','originalFaces':[2,4,6],'authorizedView':'DE4-PRESENTATION-06/BURNING-HANDS-DAMAGE','recipientBranches':['empty eligible set','one entirely hidden eligible target','one known plus one hidden eligible target'],'H':'independently legal Coin holder with hand, Reaction, actual perception/range/LoE and unspent lineage'},'operation':{'committedCoinChoice':'component0','replacementFace':5},'expected':{'eachBranchOriginalDrawCount':3,'eachBranchPublishedOriginalFaces':[2,4,6],'eachBranchReplacementDrawCount':1,'eachBranchPublishedFinalFaces':[5,4,6],'eachBranchSharedTotal':15,'eachBranchCoinConsumed':True,'eachBranchReactionConsumed':True,'eachBranchGuardSpent':True,'emptyBranchDamageRecipients':0,'emptyBranchDamageOrHitHooks':0,'recipientListOrSaveResultsInPresentation':False,'hiddenRecipientExistenceFromOperationPresentation':False},'negativeBranch':'If prevented before actual cone manifestation there is no original damage operation or reroll event. No substitute operation is fabricated.','scope':'NEW per-source generation timing to be explicitly agreed; other spells and hidden world events unchanged.','sourceRefs':[{'path':newrel,'pointer':'/sharedRules/DE4-PRESENTATION-06'},{'path':(R/'data/public/spell_playtests/catalog.json').relative_to(G).as_posix(),'pointer':'/spells/426/operational'}]})
 # Complete parent records, exact original source text and old alternatives remain available.
 d['previousCompleteDraft']=info(oldp);d['previousChangedCaseRecords06']=[deepcopy(c) for c,n in zip(old['currentExamples'],d['currentExamples']) if {k:v for k,v in c.items() if k!='sourceRefs'}!={k:v for k,v in n.items() if k!='sourceRefs'}]
 d['previousChangedSpellRecords06']=[deepcopy(s) for s,n in zip(old['spells'],d['spells']) if s!=n]
 d['directorReview06']={'review':info(reviewdir/'REVIEW.json'),'exactCorrections':info(reviewdir/'PROPOSED_CORRECTIONS.json'),'additionalCases':info(reviewdir/'ADDITIONAL_CASES.json'),'finalReviewArchive':info(A/'DD_DE4_Digital_Conference_05_Review_FINAL.zip'),'verdict':'CHANGE_REQUIRED; source-specific agreements do not adopt candidate','appliedOperationsToNewPendingRevision':19,'newCasesFromDirector':['DE4-N35','DE4-N36']}
 d['codexResponse06']={'agreedContentCorrections':['Mass Pacify applies to actual compelled attacks too; preserve attack-only scope.','N11 retains Portal branches and restores actual Alignment Sanctuary ward-entry branch.','N35/N36 supplement, not replace, original scenario obligations.'],'presentation':'Concur in principle with five bounded Director entries; request explicit agreement on appended empty-cone generation completion before exact application.','textCorrections':['N19 result is private to authorized controller, not generally public.','Earlier rank-1 review is not retroactively credited with new DE4 digital policy; three proposed mirrors corrected.'],'narrowerLocalOptionsRetained':info(R/'data/director/spell_review/de4_visibility_adapter_options_06.json'),'localOptionsStatus':'Earlier unsent alternative; not governing this candidate and not a second stacked policy.'}
 d['guardAmendment']=info(newg)
 d['spells'][0]['procedure']=d['spells'][0]['procedure'].replace('in amendment03.','in amendment04.');d['sharedRules']['DE4-RNG-05']+='\n\nSOURCE POLICY BINDING: DE4-PRESENTATION-06 in this same pending revision supplies only its five explicitly proposed entries. Unlisted events remain denied. Both documents require exact joint acceptance before live application.'
 for p in [oldp,newg,reviewdir/'REVIEW.json',reviewdir/'PROPOSED_CORRECTIONS.json',reviewdir/'ADDITIONAL_CASES.json',R/'data/director/spell_review/de4_visibility_adapter_options_06.json']:
  if info(p)['path'] not in {b['path'] for b in d['sourceBindings']}:d['sourceBindings'].append(info(p))
 d.update(id='DE4-CURRENT-PROCEDURES-06',recordedAtUtc=datetime.now(timezone.utc).isoformat(),status='UNADOPTED corrected video-game candidate; 15 procedures,37 current cases,30 exact original scenario texts. Presentation concurrence and exact rebinding remain open.')
 d['remainingJointChoices']=['Concur or correct DE4-PRESENTATION-06 five source entries and explicit Burning Hands empty-cone operation generation, preserving private controller versus character predicates.','Confirm exact nineteen Director operations, corrected historical attribution/private wording and N35/N36/N37 evidence against this actual revision.','After semantic concurrence assemble and verify final dependency/card/excerpt/catalog bindings before exact file acceptance; no unseen hash approval.']
 ck('Original source/access unchanged',[s['completeSourceAndAccess'] for s in d['spells']]==[s['completeSourceAndAccess'] for s in old['spells']]);ck('All30 originals unchanged',d['originalExamplesUnchanged']==old['originalExamplesUnchanged']);ck('37 unique case IDs',len(d['currentExamples'])==len({c['id'] for c in d['currentExamples']})==37)
 ck('N35 real DC15',8+3+4==15);ck('N36 Monk DC18 and RP11',8+6+4==18 and 18-7==11);ck('N36 Stable7200',2*3600==7200);ck('N36 two14 packets and finite40',sum([2,3,4,5])==14 and sum([10]*4)==40);ck('N11 Sanctuary DC14 cost5',8+3+3==14 and 15-5==10);ck('N37 shared final15',5+4+6==15)
 for c in d['currentExamples']:
  for ref in c.get('sourceRefs',[]):
   if 'pointer' in ref:ck('Case pointer '+c['id']+ref['pointer'],at(d if ref['path']==newrel else read(G/ref['path']),ref['pointer']) is not None)
 for b in d['sourceBindings']:ck('Source binding '+b['path'],info(G/b['path'])==b)
 ck('All9 accepted source bytes unchanged',all(info(G/x['source']['path'])==x['source'] for x in preserved))
 newp.write_bytes(encoded(d));checkp.write_bytes(encoded({'id':'DE4-REVIEW-REVISION-CHECK-06','candidate':info(newp),'amendment':info(newg),'checks':checks,'checkCount':len(checks),'failureCount':0,'currentExamples':37,'originalTexts':30,'sourceFiles':len(d['sourceBindings']),'proposedRepresentations':9,'acceptedLiveFilesChanged':0,'newRuleAdoptions':0,'scope':'Exact downloaded operation preconditions, source/hash/pointer preservation, reversible proposal edits and direct arithmetic. Not game-runtime verification or final rebound-file acceptance.'}))
 print(json.dumps({'candidate':info(newp),'amendment':info(newg),'checks':len(checks),'sources':len(d['sourceBindings']),'liveChanges':0}))

if __name__=='__main__':main()
