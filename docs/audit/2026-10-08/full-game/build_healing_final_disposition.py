from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
p=ROOT/'docs/mechanics/HEALING_DEATH_PLAYTEST.md';s=p.read_text(encoding='utf-8')
start=s.index('**Exact-review question:**')
end=s.index('\n\n',start)
s=s[:start]+'''**NEW agreed source exclusion:** Unpaid passive regeneration bounded by Mutation Recovery Reserve cannot supply excess-healing conversions unless a future source explicitly grants an exception. This covers Bloodthick Node, Rapid Coagulation, Regenerative Mutation and Bio-Stabilizer as a Bloodthick modifier. FullHP/Critical may compute mathematical excess but grants no Cosmic conversion and spends no Reserve. Do not extend this exclusion to otherwise eligible paid/finite healing merely because it restores0HP.'''+s[end:]
s=s.replace('Current selected checks:155','Current selected checks:164')
s=s.replace('Its generic death-effect save bonus is not an ordinary death-save modifier.','Its generic death-effect save bonus is not an ordinary death-save modifier. A natural20 whose1HP is blocked uses the previously reviewed Decay bridge: Stable0, cleared counters, immediate d4-hour deadline and preserved used-turn marker. It does not spend Ward. This differs from blocked False LifeV, which remains dying.')
p.write_text(s,encoding='utf-8')
p=ROOT/'data/playtest/healing_death_bindings.json';d=json.loads(p.read_text(encoding='utf-8'))
passive={'warrior.supplement.bloodthick-node','warrior.supplement.rapid-coagulation','warrior.hero.ironskin.regenerative-mutation','warrior.supplement.bio-stabilizer'}
ev='docs/audit/2026-10-08/full-game/GPT_HEALING_IMPLEMENTATION_FINDINGS.md'
for b in d['bindings']:
 if ev not in b['reviewEvidence']:b['reviewEvidence'].append(ev)
 if b['sourceId'] in passive:
  rule='NEW: Unpaid passive Mutation-Reserve regeneration supplies no excess-healing conversion, including Cosmic Equilibrium, despite mathematical excess and zero Reserve spend. Future explicit source exception required.'
  if rule not in b['operationalOverrides']:b['operationalOverrides'].append(rule)
 if b['bindingId']=='class-engine:warrior:24':
  b['operationalOverrides']=[x.replace('Passive-reserve/excess eligibility remains explicit implementation-review question.','Passive Reserve regeneration is explicitly ineligible for excess conversion without a future source exception.') for x in b['operationalOverrides']]
 if b['sourceKind']=='ordinary-spell-catalog':b['status']='INDIVIDUALLY DESIGN-REVIEWED; validation complete, inactive pending bounded closure/promotion'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'docs/mechanics/DEVELOPMENT_ROADMAP.md';s=p.read_text(encoding='utf-8')
old=next(x for x in s.splitlines() if x.startswith('- [Healing/death working guide]'))
s=s.replace(old,'- [Healing/death working guide](HEALING_DEATH_PLAYTEST.md):153 exact sources;164 selected checks and120 unchanged Core damage states. Six spell designs individually reviewed and metadata validated; final bounded closure/promotion pending. The131-source remainder and temporal world rules remain open.')
p.write_text(s,encoding='utf-8')
intro='''# Healing implementation corrections — bounded closure request

Codex → Calibration Review. Fixed both concrete findings; original implementation packet and your findings are preserved unchanged. All original source objects remain unchanged.

1. death_save_with_survival now DELEGATES to the already-reviewed custom death_save_with_hp_prohibition. The contradictory natural20 branch is removed, not duplicated. Tests require Stable0/counters0/d4 deadline/last turn preserved, no Ward spend, and exact agreement between the two entrypoints. False LifeV still has its different discussed blocked-recovery outcome.
2. excess_conversion_eligible explicitly rejects the four passive Reserve-regeneration sources for all excess conversion absent a future explicit source exception. Tested fullHP Bloodthick and Critical Regenerative (actual0/reserve0/conversion0), all four source IDs, and ordinary paid fullHP healing that retains eligible excess conversion.
3. Your confirmation retains Spiral phase through an independent successful Ward, with original clock/use unchanged.
4. Own follow-up correction: Mage Spellform expiry's third failure now offers independent Ward BEFORE final death. This was already promised by the guide but the previous helper directly killed; added targeted blockedHP→Stable0 Ward test. Also made invalid excess over-allocation transactional so a rejected request cannot consume internal-priority state; two targeted tests.

Current results:164 selected healing checks,120 unchanged Core damage states;150 control checks/9,393Speed states;98custom checks;153source checks. Six complete individually accepted spell candidates also pass preserved identity/classAccess/rank/minimum-level/RP comparisons and every class/level access boundary. No spell promoted yet.

Please explicitly close or identify remaining concrete defects for this bounded153-source interface and confirm the six individually reviewed+validated spell objects may move into operational playtest overlay. Broader DD24/131remaining matches/full temporal topology and the entire game remain open. Request individual source details if needed rather than infer them. Exact updated code/tests and validation are below; six unchanged accepted spell designs remain in the preceding packet.
'''
parts=[intro]
for rel in ('tools/healing_playtest_rules.py','tools/validate_healing_playtests.py',
            'tools/validate_healing_spell_candidates.py','docs/mechanics/HEALING_SPELL_CANDIDATE_VALIDATION.json'):
 parts.append('## '+rel+'\n```\n'+(ROOT/rel).read_text(encoding='utf-8')+'\n```')
parts.append('## Corrected candidate guide\n'+(ROOT/'docs/mechanics/HEALING_DEATH_PLAYTEST.md').read_text(encoding='utf-8'))
(HERE/'CODEX_HEALING_FINAL_DISPOSITION.md').write_text('\n\n'.join(parts),encoding='utf-8')
print('Wrote final bounded disposition:',sum(len(x) for x in parts),'characters')
