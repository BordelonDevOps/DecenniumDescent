"""New data-only inspection and pending conference assembly."""
from pathlib import Path, PurePosixPath
import json,hashlib,zipfile,datetime
G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';D=A/'director-spell-review-127'
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def bind(n,b):return {'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def at(v,p):
 for s in p.strip('/').split('/'):
  s=s.replace('~1','/').replace('~0','~');v=v[int(s)] if isinstance(v,list) else v[s]
 return v
cp=R/'data/director/spell_review/rank7_perception_5_source_conference_01.json';c=json.loads(cp.read_text(encoding='utf-8'));op=A/'DD_Rank7_Perception_5_Source_Conference_01.zip';checks=[]
with zipfile.ZipFile(op) as z:
 assert z.testzip() is None
 for row in c['sourceBindings']:
  b=z.read('sources/'+row['path']);assert bind(row['path'],b)==row;p=G/row['path'];checks.append({'path':row['path'],'archivedExact':True,'currentExact':p.exists() and bind(row['path'],p.read_bytes())==row})
idx=json.loads((R/'data/public/spell_playtests/authored_review_index.json').read_text(encoding='utf-8'));by={e['id']:e for e in idx['entries']};current=[];additional={}
ids=['true-seeing','hallucinatory-terrain','mind-maze','illusory-clone','mass-mirage','seeming','programmed-illusion','puppet-strings','mental-prison','irresistible-dance','eyebite','quicken-cast','contingency']
for sid in ids:
 e=by[sid];assert e['authoredStatus']=='reviewed-authored-operational-playtest';b=e['completeEnvelopeBinding'];raw=(G/b['path']).read_bytes();assert bind(b['path'],raw)==b;doc=json.loads(raw)
 card=at(doc,e['wholeCardPointer']);shared=at(doc,e['sharedRulesPointer'])
 current.append({'spellId':sid,'completeCurrentIndexEntry':e,'completeCurrentCard':card,'completeSharedRules':shared,'additionalSharedRules':[at(doc,p) for p in e.get('additionalSharedRulesPointers',[])]})
 for key in ['completeEnvelopeBinding','authoredAcceptanceReceipt','authoredApplicationReceipt','casebookBinding','retainedHoldsBinding']:
  if key in e:
   row=e[key];raw=(G/row['path']).read_bytes();assert bind(row['path'],raw)==row;additional['current-authority/'+row['path']]=raw
qs=[
 ('RP127-Q22',['inescapable-labyrinth','mirage-arcane','mirage-legion','perfect-veil'],'True Seeing and Hallucinatory Terrain are already accepted/applied; historical pending labels are stale.',
  'Use current exact Illusion14 cards and actual recipient access, concentration,60ft moving extent, usable senses and accessible sensory path. True Seeing identifies false sensory overlays including accessible sound/touch; it does not generically cancel independent compulsion, damage, physical terrain or all mental effects. For each new spell explicitly choose whether its Speed0/attention/tactile consequence depends on deception and therefore ends, is bypassed only for that observer, or is independently maintained. Show a current real True Seeing cast; a generic True Sight label or unsourced creature sense is insufficient. Do not reopen the accepted14.'),
 ('RP127-Q23',['inescapable-labyrinth'],'Speed0 can remove voluntary locomotion without spending a whole-Action denial allowance.',
  'Declare the movement modes affected and test actual standing, climbing/swimming and supported/unsupported flight from named native sources. Give a surviving target with an ordinary Action and real lawful teleport source, showing Speed0 alone neither cancels that Action nor pays a new guard. Conversely a separate real teleport blocker keeps its own predicate. If you choose a broader mental restraint, identify it as NEW with its actual guard. Preserve another independent Speed0 source after this spell ends; no blanket mobility restoration.'),
 ('RP127-Q24',['mindtrap-echo'],'The last completed action can be a wrapper containing newer child casts or reactions.',
  'Select a finite immutable eligible history node and a deterministic priority across ordinary spells, Counterspell reactions, Quicken Cast parent/children, Contingency LOAD versus later paid-free RELEASE, Ready preparation versus release, long action completion and genuine mundane interactions. Accepted Time5 establishes that a resumed parent does not overwrite newer nested casting history. A repeat must reconstruct one newly legal procedure and cost, not restore prior objects/HP, copy dice or replay all wrapper children for one cost. Show the exact node chosen after two actually paid Quicken children and an intervening Counterspell. This is a new Mindtrap selection policy, not a change to those accepted sources.'),
 ('RP127-Q25',['mindtrap-echo'],'Compelled repeat cannot consume a phantom opportunity or recursively compound control.',
  'Use actual acquisition/component/resource data for a costly repeat and the complete mandatory-versus-optional payment policy. Handle HP cost, last limited use, long casting, Reaction-only originals and invalid old target. Specify the next ordinary opportunity and finite expiration for regular-turn actors and owner-attached companions; no extra turn or free command. Competing actual compulsion selects one real budget under accepted arbitration. A repeat of Mindtrap itself or of a wrapper must not rearm the consumed instruction or bypass the source/target encounter guard. Show a precise no-execution result when the selected legal obligations cannot be met.'),
 ('RP127-Q26',['mirage-arcane'],'Tactile depiction must remain consistent with support, movement and partial suppression.',
  'Provide continuous geometry for actual floor, gap, ledge and rigid obstacle and independent sensory channels. A tactile water/rough-ground impression must have specified sensation without silently producing water, collision, extra speed cost or a bridge. Demonstrate crossing a real gap: use a fully sourced normal fall or stop for an actually perceived contradiction, not a made-up damage packet. Keep tactile sensation after contact only as expressly chosen, distinguish personal recognition from source ending, and show a clipped Antimagic region plus accepted Hallucinatory Terrain overlap in exact event order. Generic image limits do not erase the printed feel promise.'),
 ('RP127-Q27',['mirage-legion'],'Six apparent spell performances are not six actual spell events.',
  'Record all six positions, orientation, script, allowed sensory extent and one real controller budget for creation and later changes. Test a truly perceived gesture satisfying a specific Ready trigger separately from actual Counterspell eligibility requiring a begun real spell. Preserve real response commitment if its own trigger permits it; never fabricate six cast ledger records, Refrain, Clone/Echo opportunities, source light, damage, summons or item production. A real Mirror Image source has separate exact attack routing; Mirage Legion adds none unless expressly selected. Personal identification and clipped suppression must not regenerate ended images or erase observer memory.'),
 ('RP127-Q28',['perfect-veil'],'The full interaction predicate must specify who observes, who acts and what permanently changes.',
  'Give a concrete interaction matrix for protected creature speech, touching a known ally, attempted/missed attack, hit, incoming healing, involuntary collision, area exposure, dropped gear, footprints and noncognitive mechanisms. For each state whether that event qualifies and whether revelation is observer-specific, recipient-wide or full-group. No broad implication of absolute untargetability, immunity, memory erasure, secret-faction detection or total cover. Show caster+3 actual willing allies with unique bodies and a carried fifth creature, genuine gear transfer, a remote sensor through its own current rules and actual True Seeing as a separately scoped observer. The strong unnoticeable promise must survive as explicitly selected useful behavior.'),
 ('RP127-Q29',['inescapable-labyrinth','mindtrap-echo','mirage-arcane','mirage-legion','perfect-veil'],'Current card labels and scoped interface acceptance must be distinguished from unsourced global defaults.',
  'Preserve original21 questions, complete source profiles and all original text. Every selected concrete duration, area, control allowance, channel or target policy is NEW for this source unless an exact accepted rule applies. Write at least10 complete cases with actual acquired Illusion rank7 actor,17RP base, correct native class costs/strain/repertoire, concentration transitions, counter windows and state events. Independently reference current accepted72 and Time5/Body8 by exact receipts. Keep genuinely pending Project Image or other absent sources conditional; a stale pending label for an applied card must not create an unnecessary hold.')
]
notes={'id':'RANK7-PERCEPTION5-INDEPENDENT-CONFERENCE-127','status':'PREPARED_NOT_SENT_UNSELECTED','recordedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'identities':[r['spellId'] for r in c['records']],'candidate':bind(str(cp.relative_to(G)).replace('\\','/'),cp.read_bytes()),'sourceChecks':checks,'originalQuestions':c['questions'],'additionalFocusedQuestions':[{'id':i,'spellIds':s,'finding':f,'request':q,'decisionSelected':False} for i,s,f,q in qs],'totalQuestionCount':29,'originalOperationalCases':0,'minimumNewCases':10,'currentAcceptedComparisons':current,'nativeProfiles':[r['completeCurrentCatalogSourceAndAccess'] for r in c['records']],'sourceAuthorityUpdate':'Historical True Seeing/Hallucinatory Terrain and related accepted14 pending labels are superseded by exact application122. Current comparison cards are evidence, not a request to redo them. Time5 is accepted/applied127. All five requested rank7 spells remain pending.','acceptedNewIdentities':[],'canonicalChanges':False,'runtimeExecuted':False}
(D/'RANK7_PERCEPTION5_NEXT_CONFERENCE_NOTES_127.json').write_bytes(enc(notes))
with zipfile.ZipFile(A/'DD_PlanarTravel6_Director_Conference_127.zip') as z:
 m=json.loads(z.read('MANIFEST.json'))
 for row in m['files']:assert bind(row['path'],z.read(row['path']))==row
 payload={n:z.read(n) for n in z.namelist() if n.startswith(('accepted-context/','accepted/','current/'))}
payload.update(additional);payload['original/'+op.name]=op.read_bytes();payload['INDEPENDENT_QUESTIONS_127.json']=enc(notes)
payload['README.md']='''# Rank7 Perception5 director conference127

Author Inescapable Labyrinth, Mindtrap Echo, Mirage Arcane, Mirage Legion and Perfect Veil. All have actual Illusion rank7/base17RP access via Bard19,Mirrorsage19,Wizard13, Action120ftVSF. Preserve original21 questions and answer8 independent followups (29 total), with at least10 NEW complete source-qualified cases. Earlier complete procedures and operational cases are absent; do not accept by source receipts.

The independent notes supply13 exact current accepted comparison cards, their shared rules, index pointers and current binding receipts. True Seeing/Hallucinatory Terrain/Illusion14 and Control15 were applied122, and Time5/Body8 are accepted/applied127; historical pending labels do not reopen them. In particular perception identification does not universally dispel compulsion, tactile sensation must remain meaningful without invented support, and repeating an actual action never replays its old outcomes for free. Use current Time5 nested-cast history for Mindtrap wrapper edge cases.

Current baseline610 reviewed/applied,238 pending,334 standalone,173 scoped interfaces,0 accepted-unapplied. Transport6 remains under director review, not accepted. Current nested index/checkpoint snapshots may precede newly prepared packet routing but bind the same authored counts. Original49 source bindings were checked against their frozen archive; the current index is separately supplied. All source files and pending proposals remain preserved.

Return complete procedures/shared rules, all answers, acquired class fixtures, complete event-state cases and original source/value provenance, exact retained holds, full-value forward/inverse operations and a verified complete downloadable archive. Execute no supplied or historical code. New source authoring is not runtime, human, numerical balance, cosmology or release validation. The owner requests continuing pending spells until accepted and then applying; this prepared packet grants no premature acceptance.
'''.encode()
manifest={'id':'RANK7PERCEPTION5-DIRECTOR-CONFERENCE-127','files':[bind(n,b) for n,b in sorted(payload.items())]};payload['MANIFEST.json']=enc(manifest);out=A/'DD_Rank7Perception5_Director_Conference_127.zip';assert not out.exists()
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for n,b in payload.items():z.writestr(n,b)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
 assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in z.namelist())
 for row in manifest['files']:assert bind(row['path'],z.read(row['path']))==row
receipt={'id':manifest['id'],'status':'PREPARED_NOT_SENT','archive':bind(str(out),out.read_bytes()),'members':len(payload),'bindings':len(manifest['files']),'questions':29,'requiredNewCases':10,'sourceChecks':49,'currentAcceptedComparisons':13,'canonicalChanges':False,'runtimeExecuted':False}
(D/'RANK7PERCEPTION5_PACKET_127.json').write_bytes(enc(receipt));print(json.dumps(receipt,indent=2));print('Current source drift:',[r['path'] for r in checks if not r['currentExact']])
