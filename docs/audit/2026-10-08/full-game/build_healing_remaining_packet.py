"""Preserve the complement of the broad scan, including exclusions/dependencies."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
def key(r):return (r['kind'],r['owner'],r['card']['id'] if r['kind']=='class-card' else r['engineIndex'])
allrows=json.loads((HERE/'HEALING_SEMANTIC_SUPPLEMENT_CANDIDATES.json').read_text(encoding='utf-8'))['classRecords']
selected=json.loads((HERE/'HEALING_INTERFACE_SUPPLEMENT.json').read_text(encoding='utf-8'))['classRecords']
known={key(r) for r in selected}
rows=[r for r in allrows if key(r) not in known]
assert len(rows)==131
result={'status':'UNREVIEWED_REMAINDER','scope':'All131 remaining passages from the199-match supplemental lexical scan. Every source needs inclusion/exclusion/dependency disposition; no claim of semantic completeness.','classRecords':rows}
(HERE/'HEALING_REMAINING_SOURCE_CANDIDATES.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Remaining131 class healing/recovery semantic matches','',
 'Codex → Calibration Review. After closing the selected interface, discuss every remaining source below. Classify each by exact source ID as HEALING_INTERFACE, TEMP_HP, RESOURCE_ONLY, COMPANION_DEVICE, CONDITION_CURE, MOVEMENT_CONTROL_ONLY, TEMPORAL_DEPENDENCY, OTHER_NAMED_DEPENDENCY or EXCLUSION (adjust role where the actual source needs more precision). Identify exact unresolved interface questions, not just keyword labels. Preserve all original source costs/actions/targets/cadences. Do not assume every lexical match heals, and do not approve a whole card because one component is reviewed.','',
 'Review potential contradictions involving actual-gain triggers, finite resource recovery, tempHP, copied healing, soul/body reconstruction, stat changes and multiple trigger chains. In particular, advise which systems we must discuss next, and name the exact subset requiring follow-up source evidence. These131 complement the68 selected supplemental passages already discussed; initial79 class sources are separate.','',
 '''## Codex source-specific findings to resolve

1. Paladin engine[13] says level17 Wave once/LONG rest while the Hero Lay on Hands card reviewed in the preceding package says1/SHORT rest. Explicitly reconcile this evidence; don't leave two active use cadences. Likewise engine[10] says one paid Smite/round while engine[3] has once/own-turn: retain the narrower shared cap if that is the intended override. No original should be deleted.
2. Oracle engine[26] generic paid-zone upkeep conflicts with terse target-start zones such as Resonant Seed (1RC activation, three target-start pulses). How does a source-owned upkeep payment authorize asynchronous allied target-start pulses without paying once PER ally or inventing free rounds? Distinguish limited1/LR Finals like Crown Restored. Which actual zones need a schedule record/overlay next?
3. Lifewell says start AND later turns use BA+1RP to pulse, besides its Action+4RP+allBG activation; confirm first pulse needs that same-turn BA+1RP or identify an explicit correction. Contrast Healing Briar/Restoration Field initial pulse included in activation and later paid maintenance. Shaman Extended Totem/Echo Totem: enforce genuine paid fourth pulse and no double-heal overlap.
4. Healing-dependent riders differ by source: Divine Invocation Renewal gives5Stamina alongside healing (not base Renewal's actual-gain gate); Purging Flame/Zealot Renewal condition cure clauses independent vs conditioned? Flame Prophecy actual healing, Bloodbond paid-technique-heals trigger and Enhanced Convergence tempHP: distinguish actual gain from an attempted legal heal. Zealot Renewal blocked healing still backlash? Fire immunity vs cannot-below1 backlash and shared damage flags need an exact ruling.
5. Crown's Burn: total numeric actual fire damage (temp absorption+actualHP), divide among up to3 chosen recipients, floor when? Roll S d6+M shared or independently per ally? Zero selected recipients must not divide by0. Is min1 triggered by positive packet or positive numeric total when HP floors yield actual0? Shared-roll damage/healing abilities and explicit copy-half amounts need consistent copied quantity/dieCount provenance.
6. Monk maximum-HP reductions choose strongest among source Monk effects; state clamp and percentage thresholds must be distinct from damage/healing. Confirm applying/restoring maximum does not generate damage/healing/Wounds, and name global multi-source composition dependency. Veinburst Requiem's post-damage 'falls to0' threshold is an additional explicit state effect: does it open a new Wound save or only dying/death rules? A floor cannot be guessed to stop non-damage state loss.
7. Paladin redirection engine[10] says split 'actual damage' AFTER original defenses, then no receiving mitigation, whereas Bloodbond says pre-mitigation split and each recipient defenses. Newly reviewed actualDamageDealt is a POST-HP/temp numeric-drain measure and should not accidentally be reused before redirection. Please keep these source-specific procedures distinct and identify a dedicated redirection sequence packet if needed; don't claim it closed from healing classifications.
8. Tinker destroyed-drone reconstruction and functional-device repair are distinct; support mode/Restoration Field are explicit organic-healing exceptions. Druid temp buffer spends finite reserve but Combat Shapeshifting heals realHP. Mirrorsage copies/converted Mend and finite healing, Wizard added healing dice, Shaman flask stock and limited refunds need exact type/provenance/cadence dispositions rather than a universal 'all copies never trigger anything' beyond their actual source flags.
''','']
for r in rows:
 if r['kind']=='class-card':
  c=r['card'];lines.extend(['## '+c['id'],'',json.dumps({k:c.get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')},ensure_ascii=False),''])
 else:lines.extend([f"## {r['owner']}.engine[{r['engineIndex']}]",'',r['text'],''])
(HERE/'CODEX_HEALING_REMAINING_CONFERENCE.md').write_text('\n'.join(lines),encoding='utf-8')
print('Prepared131 exact remaining source passages:',sum(len(x) for x in lines),'characters')
for r in rows:
 if r['kind']=='class-card':print(r['card']['id'],r['card']['name'])
 else:print(f"{r['owner']}.engine[{r['engineIndex']}]")
