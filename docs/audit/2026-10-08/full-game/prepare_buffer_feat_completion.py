"""Preserve named feat dependencies for a future full-clause conference."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
path=ROOT/'src/data/feats.js'
feats=json.JSONDecoder().raw_decode(path.read_text(encoding='utf-8').split('export const feats = ',1)[1])[0]
by_id={r['id']:r for r in feats}
ids=['chef','inspiring_leader','empowered_summoning','field_medic','blood_ritual','necrotic_affinity','soul_cage','lifeleech']
rows=[{'id':ident,'sourceObject':by_id[ident],'sourceObjectSha256':hashlib.sha256(json.dumps(by_id[ident],sort_keys=True,ensure_ascii=False).encode()).hexdigest()} for ident in ids]
data={'status':'PREPARED / UNDISCUSSED full-clause batch; no feat promotion',
      'scope':'Seven buffer-intersection feats plus the exact Lifeleech dependency of Soul Cage; not the entire335-feat catalog.',
      'sourcePath':'src/data/feats.js','sourceFileSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'records':rows}
(HERE/'BUFFER_FEAT_COMPLETION_SOURCES.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
text='''# Eight named feats — completion preparation

**Prepared, not submitted or adopted.** The form/buffer conference reviewed selected components of seven feats. Completing Soul Cage also requires the existing Lifeleech feat: its printed soul charges explicitly power Soul Cage. This is a semantic dependency supplement, not a new feat. All335 registry records remain preserved.

Questions for the later full-clause conference:

1. Chef needs an actual food quantity, ingredients/tool use, recipients, shield amount, consumption action/time, shelf life and rest eligibility. Prevent portable infinite rest-food caches while preserving the source's long-rest cooking role. Distinguish necessary food consumption from trading surplus meal items in the existing economy.
2. Inspiring Leader needs exact recipient count, self eligibility, hearing/language/range, interruption, shield amount and per-recipient refresh frequency. Preserve the printed ten minutes and Charisma13 prerequisite. Repeated speeches should not evade a shared source-family limit.
3. Empowered Summoning retains Charisma14, creation-time2PB shield, and PB on each summoned creature's first damage roll per round. Define actual summons versus bound/returned existing creatures, caster/source attribution, area damage, shared rolls, attacks versus damage ticks and multiclass companions. Do not multiply one roll's PB over all targets or refresh it by dismissal/recreation. Keep the existing shared command budget.
4. Field Medic retains Medicine training, a Bonus Action option to use a healer's kit and PB shield after actual stabilization. The reviewed Core kit use automatically stabilizes one living dying creature and consumes one actual kit use; replayed stabilization of an already Stable target is illegal. Does the feat's second sentence apply to all actual stabilization by this owner, including a Medicine Action or spell, or only the kit? State one source-faithful interpretation and any new restriction explicitly.
5. Blood Ritual retains Constitution13, level4, ten minutes and1/LR. Self offer2×level and each eligible ally offerlevel are already agreed; allies last1 hour, self uses default recipient LR. Complete target count, blood-sharing consent, presence/range/interruption, the independent curse/disease save advantage's deadline and its next-save scope. No HP loss is printed for the drop of blood. Do not grant any actual lycanthropic oath merely from its thematic prerequisite language.
6. Necrotic Affinity retains Religion proficiency OR level8. Its resistance/Reaction prevention/post-packet shield is already reviewed; complete the separate melee-hit1d6 once-per-turn and24-hour anti-resurrection clauses. Clarify own turn versus every actual turn, natural melee attacks, extra Actions, damage provenance and final killer attribution. Translate “effects of fifth level or lower” to this game's actual rank/access system, including class abilities without spell ranks. No copied kill, staged target or temporary form should create a new corpse or soul entitlement.
7. Lifeleech's necrotic spell healing requires actual damage, eligibility, target and pulse limits, excess handling and the existing Critical/healing-prohibition procedures. Its soul spark and Soul Cage capture need one owner charge pool and one entitlement per real eligible death. Preserve cap3; do not double a kill's charge from both feats. Specify party/created/summoned/revived target exclusions explicitly as new integration where absent.
8. Soul Cage requires Lifeleech OR spellcasting ability plus level8. Clarify the exact prerequisite grammar. Complete black-crystal requirements, ownership, soul consent/eligibility, capture action and timing, range/perception, competing captors, resurrection/Soul Bind interaction, soul release and charge decay. Is a charge truly the trapped soul or a residue that does not prevent resurrection? Avoid leaving that world consequence implicit.
9. Soul Cage's one-charge2d8 shield and two-charge3d8 necrotic Agony Lance need activation, target, range, DC/stat owner, save, lifetime, per-use frequency and paid-failure rules. “Disadvantage on the next healing it receives” has no defined generic healing roll: choose and label an operational conversion, not a silently assumed half-heal. Specify how fixed healing, rolled healing, stabilization, shields and resurrection interact.
10. Present full source-qualified feat objects with prerequisites, acquisition/repeatability, every action/cost/target/deadline/frequency and each clause. Preserve original and legacy text. Identify prior reviewed interfaces, genuinely new design choices and remaining external catalog dependencies. Full object drafting and bounded validation precede promotion; passing old buffer tests is not full-feat approval.

'''
for r in rows:text+='\n## '+r['id']+'\n```json\n'+json.dumps(r,ensure_ascii=False,indent=2)+'\n```\n'
(HERE/'CODEX_BUFFER_FEAT_COMPLETION_PREPARED.md').write_text(text,encoding='utf-8')
print('Prepared8 exact feat sources including Lifeleech dependency; not submitted/adopted.')
