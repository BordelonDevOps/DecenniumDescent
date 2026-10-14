"""Record notebook decisions without changing preserved source objects."""
from pathlib import Path
import json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
evidence='docs/audit/2026-10-08/full-game/GPT_HEALING_SUPPLEMENT_REVIEW.md'
final='docs/audit/2026-10-08/full-game/GPT_HEALING_FINAL_BOUNDARIES.md'
reply=(HERE/'GPT_HEALING_SUPPLEMENT_REVIEW.md').read_text(encoding='utf-8')
table=reply.split('T. Source classifications for all 68 supplemental records',1)[1].split('These classifications directly',1)[0]
roles={}
for line in table.splitlines():
 if '\t' not in line:continue
 ident,role=line.split('\t',1)
 if ident=='Source':continue
 if '.engine[' in ident:
  owner,index=re.fullmatch(r'(.+)\.engine\[(\d+)\]',ident).groups();key=f'class-engine:{owner}:{index}'
 else:key=f'class-card:{ident.split(".")[0]}:{ident}'
 roles[key]=role
assert len(roles)==68,len(roles)
p=ROOT/'data/playtest/healing_death_bindings.json';data=json.loads(p.read_text(encoding='utf-8'))
overrides={
 'mage.hero.lich.undying-spellform':'Partial zero override: speech, half movement, normal Action and concentration allowed; no independent BA/Reaction. Existing concentration avoids automatic zero loss but damage save remains. Separate restrictions apply. Expiry at0 destabilizes and adds1 failure.',
 'oracle.supplement.false-life.false-life-boon-iii':'Exactly one permitted turn choice: move, speak or Revelation using its printed activation/costs. Revelation can start concentration; prior concentration is not preserved by this feature.',
 'oracle.supplement.false-life.false-life-boon-i':'Distinct positive-to-zero damage-floor and failed-death-save would-die replacement modes share the printed1/LR use. Do not promote this into an all-causes Ward.',
 'oracle.supplement.false-life.false-life-boon-v':'Delayed quarter-maximum direct recovery at next regular start before death save. Extra turn does not advance it. Dead target is not revived; broad gain prohibition leaves0 without invented stability.',
 'oracle.supplement.spiral-touched.spiral-touched-boon-iii':'Specific pre-Wound recovery after Instant Death fails and no true floor prevents crossing. Preserve original drop Wound trigger; spend use, attempt quarter-maximum direct recovery, phase out, then Wound. Fatal Wound ends phase unless independently replaced.',
 'oracle.supplement.spiral-touched.spiral-touched-boon-v':'DEFER: snapshot participant contract is discussed/tested, including Wounds, RC, per-encounter use and Soul Bind restoration. Full clocks/environment/equipment/body duplication semantics require temporal package; no complete execution claim.',
 'oracle.supplement.fate-bound.fate-bound-boon-iv':'Reroll failed death save before committing natural1/failure counters, then use new result. Generic death-effect save bonus does not apply to ordinary death saves.',
 'oracle.supplement.wound-eater.wound-eater-boon-iii':'Direct pending death of a legal living dying hostile0 target emits no damage/Wound event. Legal Ward may intercept. Healing requires actual death; paid use/action remains spent.',
 'cleric.hero.cultist.ritual-of-undeath':'Would-die Ward can replace damage or non-damage death if body/explicit source eligibility permits. Positive pre-eventHP→1 is loss prevention through Decay; already0 blockedHP→Stable0 with immediate d4-hour deadline. Stop same-packet skipped death branches. Reconcile retained lethal tracks.',
 'monk.hero.enlightened-master.breath-of-the-thousand-petals':'At most6 total targets including at most2 eligible corpses. Each source Monk may resurrect each target identity once in the campaign. Living healing does not consume that history. Strict post-previous-end death marker; use/cost/floor clocks retained.',
 'paladin.supplement.oath-of-mercy.grace-reversal':'Only source-specific post-zero Reaction window after survival/Wounds, before zero Reaction loss finalizes. No self-target. Identity history is per source Paladin/target until that Paladin Long Rest; death does not reset it.',
 'paladin.supplement.oath-of-mercy.channel-life':'Donor non-damage HP cost first, cannot be prevented/refunded, must remain1. Recipient ordinary heal accepts legal modifiers. Packet forbids ALL excess-to-tempHP conversion across owners; eligible excess-to-damage conversion remains possible.',
 'crimson-agent.hero.bloodweaver.transfusion':'Donor pays K normalHP before recipient baseK+floor(K/2) ordinary healing. No damage/redirection/temp payment/refund; donor remains1. Recipient legal modifiers/restrictions apply.',
 'crimson-agent.hero.bloodweaver.veinweave-vitality-link':'Separate child heal requires actual restoration by paid Agent source; child carries blockLinkTriggers for every downstream link, shared root/provenance retained.',
 'monk.hero.enlightened-master.shared-breath':'Child healing shares root causal ledger. Every link application can fire once/root; no return path or sibling branch repeats an already visited link.',
 'warrior.engine[24]':'Reserve spends only actualHP gained; unchanged reserve does not itself grant permission for excess conversion. Passive-reserve/excess eligibility remains explicit implementation-review question.',
}
for b in data['bindings']:
 if b['bindingId'] in roles:
  b['classification']=roles[b['bindingId']]
 if b['sourceKind']=='ordinary-spell-catalog':
  b['classification']='INDIVIDUAL DRAFT: '+str(b['sourceId'])+'; exact object pending review/promotion'
  b['status']='DRAFTED; inactive, individual implementation review pending'
 else:
  b['status']='DISCUSSED; bounded operational implementation review pending'
 for ev in (evidence,final):
  if ev not in b['reviewEvidence']:b['reviewEvidence'].append(ev)
 b['operationalOverrides']=['Apply HEALING_DEATH_PLAYTEST.md only to this source\'s classified healing/death components; retain exact printed actions, costs, prerequisites, target caps and cadences.']
 lookup=f"{b['bindingId'].split(':')[1]}.engine[{b['sourceId']}]" if b['sourceKind']=='class-engine' else str(b['sourceId'])
 if lookup in overrides:b['operationalOverrides'].append(overrides[lookup])
 b['openIssues']=['Exact implementation review pending.']
 if 'DEFER' in (b['classification'] or ''):b['openIssues'].append('Full temporal procedure remains deferred to dedicated package.')
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'data/playtest/spell_drafts/candidate_healing_death.json';draft=json.loads(p.read_text(encoding='utf-8'))
if final not in draft['reviewEvidence']:draft['reviewEvidence'].append(final)
for s in draft['spells']:
 if s['id']=='resurrection':
  s['limitations']=s['limitations'].replace('Apply the separately reviewed lethal-track reconciliation once authored; this spell is not yet operational.','After successful return, retain Exhaustion6/Expedition6 and enter their protected living-collapse states. Later positive unprevented gain is lethal again; qualifying care and point gates still apply. This candidate remains inactive pending exact review.')
 if s['id']=='death-ward':
  s['effect']=s['effect'].replace('Preserve the damage packet and all ordinary Instant Death/Wound/condition calculations.','Preserve the raw damage packet, Core Instant Death check, half-maximum/Maiming Wound triggers and attached conditions. The prevented positive-to-zero crossing does not itself create a drop-only Wound save.')
  s['designNotes']=s['designNotes'].replace('Exact damage/HP-loss interface is under supplemental conference; inactive pending review.','The agreed damage/HP-loss interface is in the candidate guide; inactive pending exact review.')
p.write_text(json.dumps(draft,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'tools/validate_control_playtests.py';text=p.read_text(encoding='utf-8-sig')
text=text.replace("'reviewStatus':'REVIEWED / reference-VALIDATED; selected helpers only'","'reviewStatus':'Prior148 checks reviewed; new positive-damage/numeric-damage clarification under healing implementation review'")
text=text.replace('Bounded review recorded.','Prior bounded review retained; healing clarification pending.')
p.write_text(text,encoding='utf-8')
print('Recorded68 supplemental dispositions and6 inactive spell drafts; preserved originals unchanged.')
