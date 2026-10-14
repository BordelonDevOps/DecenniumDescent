from pathlib import Path
import ast,copy,json,hashlib
G=Path('C:/Github/DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
compact=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
x=read(D/'candidate_evocation_rank2.json');rows=copy.deepcopy(x['spells'])
tree=ast.parse((A/'author_evocation_rank2_candidate.py').read_text(encoding='utf-8'))
shared={t.id:n.value.value for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str) for t in n.targets if isinstance(t,ast.Name) and t.id in ['common','area','objects','hostile_end']}
defaults={k:rows[0][k] for k in rows[0] if k!='id' and all(s[k]==rows[0][k] for s in rows)}
for s in rows:
 for k in defaults:del s[k]
 for k,v in list(s.items()):
  if not isinstance(v,str):continue
  pieces=[v]
  for name,frag in shared.items():
   out=[]
   for z in pieces:
    if isinstance(z,str) and frag in z:
     chunks=z.split(frag)
     for j,c in enumerate(chunks):
      if c:out.append(c)
      if j<len(chunks)-1:out.append({'shared':name})
    else:out.append(z)
   pieces=out
  if len(pieces)>1 or not isinstance(pieces[0],str):s[k]={'concat':pieces}
def expand(s):
 r=copy.deepcopy(defaults);r.update(s)
 for k,v in list(r.items()):
  if isinstance(v,dict) and 'concat' in v:r[k]=''.join(shared[z['shared']] if isinstance(z,dict) else z for z in v['concat'])
 return r
assert [expand(s) for s in rows]==x['spells']
intro='''CODEX — EIGHT RANK-TWO EVOCATION EXACT CARDS, PART 1 OF 2.

All eight full source-reconciled cards are authored but unselected. Your source conference and three authoring clarifications are incorporated. Please review all eight plus shared wording together and give APPROVE/REPAIR, with exact replacements only where needed. These are complete fields, full unmodified source/access evidence and retained possible historical aliases. Source evidence adoption for three historical names is not identity merger. Ten local checks establish only source/schema/nonpromotion preservation. Catalog remains261 reviewed/587 unfinished.

LOSSLESS FORMAT: each card inherits defaults. A field encoded {"concat":[...]} joins literal strings and {"shared":"name"} values with no added characters. Reconstruction has been checked against the original eight complete candidate objects. Part2 inherits the same defaults/shared strings.

Part1: Scorching Raystorm, Lightning Pulse, Frost Nova, Arcane Implosion. Part2: Scorching Line, Shatter, Snowball Swarm, Acid Arrow.

Frost Nova now follows existing same-owner exact-profile refresh; different owners remain independent. Its specifically reviewed elemental Speed0 classification/extension does not import Frozen or Root. Shatter fixes its whole area/structural snapshot before any damage, uses neutral nearest-center section geometry and retains object damage. Acid Arrow attaches after initial damage only to the same continuing recipient, with independent one-shot riders and no new cast on execution. All three historical records remain separately preserved, including source Instantaneous metadata. No earlier operational card or class/source file changed.

Please confirm both exact-card parts are available and review the actual wording. No separate new supplement is proposed; after approval, discovery references can link these complete cards from the integration/control guides. Approval does not imply balance, runtime, whole-game flow, GitHub delivery or cosmology review.

PART 1 OF 2
'''
parts=[]
for n,group in [(1,rows[:4]),(2,rows[4:])]:
 body=({'defaults':defaults,'sharedFragments':shared,'cards':group} if n==1 else {'cards':group,'sharedFragmentsForConvenience':shared})
 packet=(intro if n==1 else 'RANK-TWO EVOCATION EXACT REVIEW — inherit Part1 defaults/sharedFragments exactly. The repeated sharedFragmentsForConvenience block is an identical reference copy, not extra rules.\n\nPART 2 OF 2\n')+compact(body)+'\n'
 p=A/f'CODEX_EVOCATION_RANK2_EXACT_REVIEW_PART{n}.txt';assert not p.exists();p.write_text(packet,encoding='utf-8');parts.append({'part':n,'path':str(p),'sha256':sha(p),'characters':len(packet)})
full=A/'CODEX_EVOCATION_RANK2_EXACT_REVIEW.md';assert not full.exists();full.write_text('\n\n'.join(Path(p['path']).read_text(encoding='utf-8') for p in parts),encoding='utf-8')
sub=read(A/'EVOCATION_RANK2_EXACT_SUBMISSION.json');sub.update(status='two lossless exact parts prepared; not dispatched',parts=parts,packetPath=str(full),packetSha256=sha(full),losslessFieldReconstruction='PASS');dump(A/'EVOCATION_RANK2_EXACT_SUBMISSION.json',sub)

coverage=read(R/'data/playtest/game_development_coverage.json')
summary=[]
for a in coverage['aspects']:
 if a['id']=='DD-50':
  summary.append({'id':'DD-50','domain':'Cosmology','ownerSequence':'After successful GitHub push and verified remote commit only; preserve sources; not reviewed in this packet.'});continue
 summary.append({k:a[k] for k in ['id','domain','requiredCoverage','acceptanceGate','completionClass','status','closure','sourceEvidence','draftEvidence','openIssues'] if k in a})
intro='''CODEX — DELIVERY WORK PRIORITIZATION AFTER THE OWNER’S ELAPSED-TIME CONCERN

Separate this from the exact eight-card review in the other two attachments. The owner has just asked why the work has run for20hours without completion. We need change the working method, not redefine the requested end state or claim unfinished work is done. I agree that the many tiny spell conferences have displaced the rest of the game audit. Finish the supplied eight-card review, then help prioritize concrete work across the complete game.

Actual current file state:17 class families, Base/Arch/Hero,1223 authored cards and ten Paladin oath/oathbreak pairs;261 reviewed ordinary spell identities,587 unfinished;8 reviewed feats,327 unfinished. The full coverage ledger has75 areas, many already discussed, but only one marked fully closed. The supplied ledger below contains acceptance criteria and current issue text; OPEN is not proof an entire system is missing, and human/runtime/publication gates must not be confused with authored-candidate work. Source paths identify existing material whose contents require inspection before claiming a gap or approving flow. DD13 still contains an old83/765 count; the current verified catalog is261/587, and that stale ledger line needs correction.

The original user wants the whole folder audited/consolidated without information loss, all class stages/oaths, every aspect discussed, a fleshed-out game, then actual joint flow agreement before pushing to BordelonDevOps/DecenniumDescent. Cosmology must be reviewed only AFTER a verified push. Source deletion still requires both audits to confirm obsolescence; no deletion is needed for consolidation.

Working-method proposal, for review:
1. Continue the full objective; do not substitute a smaller starter game or falsely close587 spells/327 feats.
2. Separate concrete authoring/integration gaps from later runtime, human balance and publication gates. Existing complete books/procedures should be reconciled and linked, not rewritten merely because an audit row is OPEN.
3. Review shared procedures once. Use larger content batches for routine spells/feats with explicit shared defaults, source provenance and exceptions; reserve additional conferences for substantive source conflicts. Do not invent hypothetical edge-case gates for every routine record or repeatedly test unchanged files.
4. Next inspect and complete whole player/Director flows: character creation and advancement; inventory/equipment/feats/crafting; encounters and rewards; expedition/rest/extraction/Haven; onboarding/examples/indexes; actual public/Director packaging and final Git delivery. Keep spell catalog completion as a substantial parallel workstream within this same task, not the only workstream.
5. Preserve all completed source/conference/candidate work. Keep the full Time Loop implementation disabled unless its own actual integration is completed; do not present disabled code as working. Judge the authored tabletop procedure separately from optional companion automation.

Please respond with a compact, prioritized set of concrete authored-delivery blockers from this evidence, identifying what file content must be read next to settle each, and any flaw in the proposed workflow. Distinguish requirements already justified by owner/source evidence from additional recommendations. This packet is NOT a final flow review or push request, and file-path lists are NOT evidence that content is correct. Do not invent approvals, waive unresolved authored requirements, lower the full objective, or review cosmology. A concise next-step sequence is enough; avoid expanding the ledger into another list of speculative gates.

CURRENT COVERAGE LEDGER EXCERPT (COSMOLOGY CONTENT EXCLUDED)
'''
p=A/'CODEX_DELIVERY_WORK_PRIORITIZATION.txt';assert not p.exists();p.write_text(intro+json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dump(A/'DELIVERY_WORK_PRIORITIZATION_SUBMISSION.json',{'status':'prepared, not dispatched','packetPath':str(p),'packetSha256':sha(p),'coveragePath':'DescentReviewChanges/ReviewBible/data/playtest/game_development_coverage.json','coverageSha256AtPreparation':sha(R/'data/playtest/game_development_coverage.json'),'cosmologyContentExcluded':True,'purpose':'prioritize full objective; not final approval or scope reduction'})
wrapper='Please review the two exact rank-two Evocation card parts first (all8 cards plus shared wording; APPROVE/REPAIR). Then address the separate delivery-prioritization attachment in light of the owner’s20-hour concern. Preserve the full objective and distinguish actual authored blockers from runtime/human balance/publication gates; the next work should cover the whole game flow, not automatically start another isolated spell batch. This is not final flow approval or permission to push early. Cosmology remains strictly post-push. Please confirm all three attachments are available.'
(A/'CODEX_EVOCATION_RANK2_AND_DELIVERY_REVIEW_WRAPPER.txt').write_text(wrapper+'\n',encoding='utf-8')
print(json.dumps({'exactParts':parts,'deliveryPacketCharacters':len(p.read_text(encoding='utf-8')),'sourceCandidateUnchanged':sha(D/'candidate_evocation_rank2.json')==sub['candidateSha256BeforeReview']},indent=2))
