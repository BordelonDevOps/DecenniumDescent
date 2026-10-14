from pathlib import Path
import json, hashlib

G=Path('C:/Github/DecenniumDescent')
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'
D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

rows=[s for s in read(D/'candidate_evocation_rank0_3_sources.json')['spells'] if any(x['school']=='Evocation' and x['rank']==2 for x in s['classAccess'].values())]
assert len(rows)==8
catalog={s['id']:s for s in read(R/'data/public/spell_playtests/catalog.json')['spells']}
for s in rows:
 c=catalog[s['id']]
 assert not c['operational']
 assert s['sourcePlacements']==c['source']['original']['placements']
 assert s['sourceCoreEntries']==c['source']['coreEntries']
 assert s['possibleHistoricalAliases']==c['source']['possibleHistoricalAliases']
 assert s['classAccess']==c['classAccess']
p=D/'candidate_evocation_rank2_sources.json'
if p.exists():
 assert read(p)['spells']==rows
else:
 dump(p,{'status':'SOURCE EVIDENCE ONLY — no authored or selected rules','spells':rows})

intro='''CODEX — EIGHT RANK-TWO EVOCATION IDENTITIES: SOURCE CONFERENCE, NOT EXACT MANUSCRIPT APPROVAL.

The twelve rank-one Evocation exact manuscripts are a separate review. This next source-only packet asks you to reconcile eight untouched rank-two identities. Full original placements, exact Core records, possible historical aliases and actual class access follow. No rank-two draft is selected. Preserve every original record and stable ID; do not silently import another game's spell. Cosmology remains deferred until after the authorized GitHub push and remote verification.

All eight have Evocation access at actual rank2/base3RP: Crimson Agent class5, Dragoon8, Mage3, Wizard3. Five have exact-name Core blocks; Scorching Line, Snowball Swarm and Acid Arrow instead have three separately retained POSSIBLE historical aliases. Their catalog summaries and comparative Core effects match word-for-word but names differ. Please decide explicitly whether each comparative block can supply Action/range/VSF/duration evidence for this provisional stable-ID candidate. This does not rename a source, create an extra learned spell or silently dispose of an unassigned variant.

Shared established rules: actual repertoire and class access; paid cast commitment then cast-begin Dissonance/Refrain and LIFO counters; normal components; attack d20+PB+casting modifier vs AC with ordinary attack critical dice; saves DC8+PB+casting modifier, binary outcomes and no automatic natural1/20. Rank2 has no automatic scaling/upcast. Area targets are an initial resolution snapshot, including allies/caster only when geometrically included, with center/origin line of effect and independent defenses. Shared raw area damage does not combine different recipients or multiple rays into one damage event. Damage types alone do not imply named conditions. Generic spell object targeting covers unattended objects, caster-held objects or willingly offered objects, not hostile worn/carried inventory. Distinct paid attacks can target independently; names do not imply generic physical ammunition or material creation.

One-round hostile riders end at the first future target REGULAR END excluding the entire current turn, or +6 seconds outside, preserving original clocks across initiative/extra turns. Speed0 is not automatically whole-Action denial or full Frozen. The combined hard-control guard is per source character/target/encounter, spent only when a new hard component is successfully established; blocked hard control does not automatically block separate printed damage or invent a soft fallback. Duration endpoints and one-shot delayed-damage execution are different questions: please specify the latter explicitly rather than assuming a generic duration rule defines it. Existing typed condition immunities and actual source-owned cleanup apply.

Please settle each source conflict and missing parameter below with one coherent provisional procedure. Label NEW decisions. Concise but complete dispositions are preferable; exact cards will be submitted afterward.

1. Scorching Raystorm: source Action30/VSF, three rays each2d6fire. Proposed NEW three separately rolled ranged spell attacks, independently allocated at commitment among one to three perceived creatures/legal objects, multiple rays per target allowed, fixed1→2→3 order, no replacement of targets that become illegal and no shared ray dice. Hits are separate damage packets with separate defenses/callbacks, actual critical dice only for that ray. Misses do nothing. No automatic Burning, ordinary Shield only its actual AC protection rather than Magic Missile's named automatic prevention. Please confirm or replace.

2. Lightning Pulse: Action20/VSF,20-foot line,3d6lightning,CON save halves. Need exact width/origin and target scope. Proposed NEW5-foot-wide line from caster in selected direction, all actual creatures with origin line of effect, shared3d6, individual CON full/half. No automatic metal/water chains, Stun, object damage or selective allies. Source origin does not itself force caster inclusion. Confirm geometry and any object scope.

3. Frost Nova: Action15/VSF,15-foot burst,2d8cold and freeze(Speed0) on failed save. Core Instantaneous leaves rider duration missing; save ability and successful-save result are absent. Proposed NEW self-centered15-foot radius including caster and all actual creatures with center line of effect, CON save negates both2d8cold and an immediate Speed0 rider through first future target regular END/+6 outside. Separate cold defenses and Speed0 defenses, no positive-damage requirement. This is Speed0, not automatic Core Frozen/Restrained/Incapacitated; no whole-Action claim. Is self-centered geometry correct for the candidate, or choose a point within15 with15 radius explicitly NEW? Please settle success/no-damage vs half, endpoint, condition classification/removal and repeat-application ownership using actual shared controls. No ice terrain or recurring zone added.

4. Arcane Implosion: Action30/VSF, target takes4d6force;CON save or Stunned1round. Proposed source-faithful automatic4d6force to one perceived creature, then if still legal CON solely for independent Stunned through first future target regular END/+6 outside. Force immunity does not itself protect against Stun. The actual hard guard governs Stun establishment, not damage; spent allowance produces no invented soft fallback and no refund. Please confirm whether save should still be rolled when hard establishment is already impossible, and ensure no postmortem condition/save. No positional pull from the name.

5. Scorching Line / possible Aganazzar's Scorcher: catalog30-foot line3d8fire; comparative Core Action30/VSF/Instantaneous with no actual save. Proposed NEW5-foot-wide line from caster, DEX full/half, shared3d8 to all actual creatures with origin line of effect, no automatic Burning/terrain fire or hostile worn-item destruction. State explicit comparative metadata adoption and whether object targeting is present rather than inferred from fire type.

6. Shatter: Action10/VSF,3d8thunder in10-foot radius and EXTRA damage to objects. Preserve the short point range10 separately from radius10. Proposed NEW perceived point within10/LoE, all actual creatures centerLoE CON full/half; shared3d8. Need exact additional object damage, object eligibility, packet grouping, saves/defenses and structural limits. Suggest unattended/legally offered ordinary objects in area take the base plus an additional1d8thunder in one packet, no save, with actual object defenses; no auto-shattering or magic-item suppression. Do not silently remove 'extra damage to objects' or invent extra construct vulnerability. Please resolve structures/terrain versus discrete objects and bounded object portions explicitly.

7. Snowball Swarm / possible Snilloc's Snowball Swarm: catalog3d6cold5-foot radius; comparative Core Action5/VSF/Instantaneous. Preserve point range5 distinct from radius5. Proposed NEW perceived point within5, all actual creatures centerLoE DEX full/half shared3d6, no ongoing snow/ice, terrain, Frozen or save-disadvantage physiology. State comparative metadata adoption; no unexplained extension to an external version's longer range.

8. Acid Arrow / possible Melf's Acid Arrow: catalog4d4acid initially then2d4acid next round; comparative Core Action30/VSF/Instantaneous, no concrete attack/save. Proposed NEW ranged spell attack to one perceived creature/legal object, hit4d4acid and one attached delayed2d4acid event, miss none. No half damage on miss unless NEW explicit choice. Define 'next round' exactly (proposed target first future regular END for creatures; caster first future regular END for objects; +6 outside, current turns excluded), no extra-turn acceleration or initiative reset, and no continuing range/LoE/perception tether. Delayed dice are a separate nonattack packet that never critically doubles; initial critical affects only initial4d4. No concentration is proposed. Need exact suppression/dispel/end-before-pulse behavior and whether same-ID reapplications replace, refresh or coexist, including different casters. Please choose a finite source-owned policy and say what happens if the recipient is destroyed/dead before the pulse, rather than retarget a corpse/new creature. Ordinary washing does not automatically remove a magical rider without an explicit NEW action/procedure. No physical recoverable arrow or ongoing acid material.

Source reconciliation only: do not close human balance, runtime execution, higher ranks, whole-game flow, GitHub delivery or cosmology. Call out any substantive unresolved issue that prevents exact authoring.

FULL UNMODIFIED SOURCE RECORDS
'''
packet=intro+json.dumps({'spells':rows},ensure_ascii=False,indent=2)+'\n'
q=A/'CODEX_EVOCATION_RANK2_SOURCE_CONFERENCE_PREPARED.txt'
assert not q.exists()
q.write_text(packet,encoding='utf-8')
dump(A/'EVOCATION_RANK2_CONFERENCE_SUBMISSION.json',{'status':'prepared, not dispatched or authored','ids':[s['id'] for s in rows],'sourcePath':str(p),'sourceSha256':sha(p),'packetPath':str(q),'packetSha256':sha(q),'sourcePlacements':8,'exactCoreBlocks':5,'possibleHistoricalAliases':3,'sourceRecordsMatchCurrentCatalog':True,'operationalAtPreparation':sum(bool(s['operational']) for s in catalog.values()),'cosmology':'post-push only'})
print(json.dumps({'sources':8,'characters':len(packet),'sha256':sha(q),'status':'prepared only'},indent=2))
