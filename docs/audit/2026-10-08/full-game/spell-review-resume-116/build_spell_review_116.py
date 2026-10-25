from pathlib import Path
import json, hashlib, zipfile
from datetime import datetime, timezone

ROOT = Path(r'C:\Github\DecenniumDescent')
A = ROOT / 'docs/audit/2026-10-08/full-game'
OUT = A / 'spell-review-resume-116'
OUT.mkdir(exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p, value): p.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
q = read(ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_review/remaining_work_queue_67.json')
g = next(g for g in q['groups'] if g['group']=='rank7-mechanics16')
original = ROOT/g['archive']['path']
assert sha(original.read_bytes())==g['archive']['sha256']
checks=[]
with zipfile.ZipFile(original) as z:
    assert z.testzip() is None
    m=json.loads(z.read('MANIFEST.json'))
    for name, binding in [('CANDIDATE.json',m['candidate']),('PREFLIGHT.json',m['check'])]+[('sources/'+x['path'],x) for x in m['sources']]:
        b=z.read(name)
        assert len(b)==binding['bytes'] and sha(b)==binding['sha256'],name
        checks.append(name)
files={}
def add(p):
    assert p.is_file(),p
    files['current/'+p.relative_to(ROOT).as_posix()]=p.read_bytes()
for rel in [
 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json',
 'DescentReviewChanges/ReviewBible/data/director/spell_review/accepted_interface_registry_06.json',
]: add(ROOT/rel)
for name in ['ACTIVE_AUTHORING_CHECKPOINT_FEAT335_ACCEPTED_115.json','FEAT335_FINAL_LOCAL_ACCEPTANCE_115.json','PERTINENT_GPT_DECISIONS_2026_10_20_02.json','GPT_PART5_PERTINENT_RETURNS_01_RECEIPT.json']:
    add(A/name)
for name in ['DECISION.json','HOLD_REGISTER.json','ARTIFACT_BINDINGS.json']:
    add(A/'feat335-final-verdict-115'/name)
for name in ['POLICY_SELECTION.json','REVIEW_RECEIPT.json','RETAINED_LIMITATIONS.json','successor/CONTROL15_READY_REFERENCE_SUCCESSOR14.json']:
    add(A/'copy-ready-preparation-only-part5-successor-01'/name)
for name in ['REVIEW_RECEIPT.json','HOLD_REGISTER.json']:
    add(A/'control15-full-conference-part5-return-02'/name)
for name in ['RANK8_DAMAGE6_PART5_EXACT_AUTHORING_ACCEPTANCE_75.json','RANK7_IDENTITY_CASTING5_PART5_EXACT_AUTHORING_ACCEPTANCE_79.json','RANK9_RESONANCE_FIELDS3_PART5_EXACT_AUTHORING_ACCEPTANCE_90.json']:
    p=A/name; add(p); d=read(p)
    for k in ['selectedSuccessor','holdRegister']:
        bound=d[k]; bp=ROOT/bound['path']; b=bp.read_bytes()
        assert sha(b)==bound['sha256'] and len(b)==bound['bytes']
        add(bp); checks.append(str(bp.relative_to(ROOT)))
add(ROOT/'DescentReviewChanges/ReviewBible/data/director/spell_proposals/illusion_perception_14_current_13.json')
add(A/'feat335-corrected-candidate-114/data/public/feat_candidates/exact_01/spell_dependencies.json')
context={
 'id':'SPELL-REVIEW-RESUME-116','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
 'ownerRequest':'do the spells.', 'reviewDestination':'Calibration Review Part 5',
 'selectedGroup':g,
 'currentOrdinaryCounts':{'appliedReviewed':525,'indexPending':323,'standalone':249,'interfaces':173,'acceptedButUnapplied':53,'notYetAccepted':270},
 'historicalStatusTreatment':'Original source archive remains unchanged. Its UNSENT and 505/343 labels are historical. Current counts and context here supersede workflow status, not original sources.',
 'featReview':'Exact corrected parent335 authored review is complete at checkpoint115; no general feat conference is needed. Separate Planar Binding and Astral Projection feat wrappers remain unavailable.',
 'currentAuthority':'Use full current accepted counterparts supplied here within their scoped authority. CONTROL15_READY_REFERENCE_SUCCESSOR14 carries preparation-only COPY-READY-ALLOWANCE-02. Ordinary Ready is distinct. Earlier candidate recommendations and inherited pending labels are not authorizations or new semantics.',
 'task':'Resolve all33 source questions, author all16 complete source-linked video-game procedures and at least32 substantive deterministic scenarios plus all7 Prismatic entries and both school profiles where applicable. Mark new scoped choices, distinguish real prerequisites from conditional projections, and preserve all sources and unresolved holds. Return complete data-only files for independent semantic review; no canonical application.',
 'canonicalApplied':False,'runtimeExecuted':False,'newAcceptedIdentities':0,
 'inputVerification':{'boundMembersVerified':len(checks),'failed':0,'checks':checks}
}
files['CONTEXT.json']=(json.dumps(context,indent=2,ensure_ascii=False)+'\n').encode()
files['README.md']=b'# Current context for the rank-seven mechanics16 review\n\nRead CONTEXT.json and use this supplement with the unchanged DD_Rank7_Mechanics_16_Source_Conference_01.zip. Complete current accepted models and receipts are supplied, not promoted into canonical implementation. Do not execute downloaded scripts or rerun historical case runners. Return full procedures, decisions and current cases with exact input/output binding and retained holds.\n'
manifest={'id':'SPELL-CURRENT-CONTEXT-116-MANIFEST','files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in sorted(files.items())]}
files['MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
archive=A/'DD_Spell_Current_Context_116.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for n,b in sorted(files.items()):z.writestr(n,b)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for x in manifest['files']:assert sha(z.read(x['path']))==x['sha256']
write(OUT/'CONTEXT.json',context)
write(OUT/'PREPARATION.json',{'id':'SPELL-REVIEW-116-PREPARATION','sourceArchive':g['archive'],'contextArchive':{'path':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes())},'manifestFiles':len(manifest['files']),'checksPassed':len(checks)+len(manifest['files']),'failed':0,'actuallySent':False})
prompt='''Continue the ordinary-spell review. The owner has now said "do the spells."

Checkpoint115 is recorded locally: your final parent335 receipt and corrected successor were independently verified with1,049 passing checks, including all46 selected files,325 procedures,335 identities and284 complete payload cards. The feat authored review is closed for those exact bytes; retain all holds. No generic feat re-review.

Start the next unaccepted group: all16 rank-seven mechanics spells in the attached unchanged DD_Rank7_Mechanics_16_Source_Conference_01.zip, together with DD_Spell_Current_Context_116.zip. Read both manifests and complete bound sources. The source packet's505/343 and UNSENT labels are historical. Actual ordinary counts remain525 applied reviewed/323 pending/249 standalone/173 interfaces, with53 accepted-but-unapplied;270 identities still need acceptance.

Resolve all33 genuine source questions, preserving1 routine/12 interaction-heavy/3 systemic allocation. Use current accepted interfaces without reopening settled semantics. The supplement includes current Control15 Ready-reference successor14, preparation-only policy02, Illusion14, accepted Rank7 identity/casting5, Rank8 damage6, Resonance3 models/receipts/holds, and284 complete feat dependency cards. Older conflicting copies remain historical.

Please work through the full conference and complete operative authored candidate now: all16 procedures with exact access, school/rank, price, eligibility, geometry, timing, RNG, resource commitment, interruption, ownership, lifecycle, suppression, endings and cleanup. Give every source question an explicit reasoned disposition; label genuinely new scoped authorship. Do not import external spell rules. Include at least two complete substantive deterministic scenarios per spell, all seven Prismatic entries, both school profiles where relevant, and positive, adverse and lifecycle branches. Actual missing bodies/world/eligibility remain explicit conditional holds rather than invented source permissions. Preserve original text and benefits.

Return a compact data-only downloadable package with full MODEL, complete procedure/case mirrors as needed, QUESTION_DISPOSITIONS, SOURCE_REFERENCES, HOLD_REGISTER, REVIEW_RECEIPT, VALIDATION_REPORT and manifest. Bind exact input hashes. Do not package giant unchanged context copies: reference the supplied archives. Reopen the final ZIP, check CRC/member hashes, and provide byte length/SHA256. No executable needed. This is authored review only; owner-reserved canonical implementation, runtime, balance, cosmology and release remain separate. I will independently review the full returned semantics and calculations before recording new acceptance. If a source gap genuinely prevents a decision, identify its exact spell/field while completing independent spells. Do not stop at an outline or a proposed plan.'''
(OUT/'GPT_REQUEST.txt').write_text(prompt,encoding='utf-8')
print(json.dumps(read(OUT/'PREPARATION.json'),indent=2))
