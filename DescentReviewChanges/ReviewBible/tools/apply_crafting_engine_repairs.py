"""Apply the eight finite repairs required by the actual GPT framework review."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'

def main():
    p=ROOT/'docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md'
    s=p.read_text(encoding='utf-8')
    if 'This reduced maximum is a crafting flaw' in s:
        raise SystemExit('Eight repairs already applied; do not repeat.')
    (AUDIT/'CRAFTING_HARVEST_BEFORE_EXACT_REPAIRS.md').write_bytes(p.read_bytes())
    repairs=[
      ('Use a recipe only when its effect card has separately been completed and reviewed, or when the table explicitly tests that unfinished recipe with its open fields recorded.',
       "An unreviewed recipe may be executed only as an isolated framework test of access, scheduling, ingredients, crafting check, quality, yield, trade XP, preservation or price-reference behavior. Its unfinished output effect grants no gameplay benefit, activation, statistic, condition, spell-like effect, charge, duration, resource change or market classification beyond fields already independently reviewed. Normal campaign use of the finished product requires that recipe's output/effect card to be separately completed and reviewed."),
      ('A quantity-1 Flawed durable item starts at half its normal maximum structural HP, rounded down, minimum 1, and has the same maximum reduction until repaired through the ordinary equipment repair procedure; repair restores the ordinary profile, not a higher grade.',
       "A quantity-1 Flawed durable item has maximum structural HP equal to half its ordinary maximum, rounded down, minimum 1, and begins at that reduced maximum. This reduced maximum is a crafting flaw, not ordinary structural damage. Ordinary equipment repair may restore current structural HP only up to that reduced maximum; it does not remove the flaw, increase the item's maximum, alter its equipment grade or convert it to Standard quality. Removing a crafting flaw requires an explicit reviewed rework procedure; absent one, the reduced maximum persists."),
      ('Critical success additionally preserves one otherwise damaged ordinary unit already present in the manifest; if none exists, it gives no extra unit.',
       "Critical success additionally preserves one otherwise damaged ordinary unit within the selected attempted allocation that the manifest already recorded as damaged but potentially recoverable. If the selected allocation contains no such unit, Critical Success grants no additional unit. It cannot recover an unselected or already-forfeited category, duplicate an exceptional drop or exceed the manifest's finite anatomy."),
      ("Before work, list recoverable physical ordinary components and their capped quantities from the item's known construction; an unknown bill of materials gives no invented valuable component. Roll INT or WIS plus the one applicable PB contribution against DC 10. Success recovers up to 25% of each listed component's original quantity, rounded by its unit rule; failure recovers none.",
       "Before work begins, record each recoverable ordinary component and the maximum quantity physically remaining in the item after known prior damage, loss or consumption. On Success, recover 25% of each recorded recoverable quantity, rounded down under that component's normal unit rule. Explicitly divisible bulk material may use the framework's 0.01-source-unit precision. Failure recovers none. No later appraisal may increase the predeclared recoverable cap. An unknown bill of materials gives no invented valuable component. Roll INT or WIS plus the one applicable PB contribution against DC 10."),
      ('This makes the card\'s storage/processing details mandatory.',
       "This makes the card's storage/processing details mandatory.\n\nIf a required reserved component ceases to satisfy its recipe requirement before completion and no completed recipe phase expressly stabilized it, pause the order before further active work. Before resuming, the lead may reserve a fresh legal component satisfying that same requirement, including an already-legal substitution. The replacement lot keeps its own identity and age. Completed active-work phases remain completed, but any component already physically consumed or irreversibly processed before becoming unusable remains spent. If no legal replacement is supplied, abandon the order under the normal abandonment rule; do not make a completion or quality roll."),
      ('| 5 | Fouled apparatus: 1 active hour of cleanup by each participating worker; until all those hours are completed the station is unavailable. They may work simultaneously. |',
       '| 5 | Fouled apparatus: the station requires cleanup labor equal to 1 active labor-hour × the number of workers who participated in the failed order. Any physically capable workers may perform that cleanup; multiple workers may contribute simultaneously. The station cannot support another crafting order until the total required cleanup labor is completed. |'),
      ('The 2-gp crafting Crystal Vial and 5-gp equipment Vial remain distinct records unless an explicit compatibility/substitution ruling is recorded.',
       "The 2-gp crafting Crystal Vial and 5-gp equipment Vial remain distinct records unless an explicit compatibility/substitution ruling is recorded.\n\nAn exact recipe component's stored numeric `tier` remains part of that component's identity and may be compared for that recipe's explicit substitution requirements even when the stored number exceeds 6. This does not extend the generic V4 material-tier ladder or generic harvesting entitlement beyond Tier VI. A Tier 7–10 stored component therefore receives no generic harvest DC, public availability, rarity right or substitution source merely from that number; it requires its actual recipe/source acquisition procedure or another separately reviewed rule."),
      ('Each character may schedule at most two active Watches and must satisfy the separately reviewed rest rules; this is a ceiling, not an exemption from fatigue, interruption or danger.',
       "Each character may schedule at most two active Watches and must satisfy the separately reviewed rest rules; this is a ceiling, not an exemption from fatigue, interruption or danger. For this supplement, an active work Watch means time committed to crafting, harvesting, preservation, trade training, formula research or assisting those activities. The two-Watch ceiling limits this framework's work contribution; it does not by itself resolve whether another reviewed subsystem permits a distinct noncrafting activity in the remaining Watch. Rest, Strain, fatigue and expedition legality continue to come from their own governing rules.")]
    for old,new in repairs:
        if s.count(old)!=1:raise ValueError(('Expected exact single replacement',old))
        s=s.replace(old,new,1)
    p.write_text(s,encoding='utf-8')
    cp=ROOT/'data/playtest/crafting_engine_candidate.json';c=json.loads(cp.read_text(encoding='utf-8'))
    c['rules'].update({'unreviewedOutputEffectsExecutable':False,'flawedDurableMaxHpPersistsThroughOrdinaryRepair':True,
        'criticalHarvestRecoveryScope':'selected attempted allocation only','dismantleRecoveryBasis':'25% of predeclared physically remaining ordinary components',
        'illegalPerishableDuringWork':'pause; replace legal input or abandon; no quality roll','mishapFiveCleanup':'one labor-hour per original participant; any capable worker can contribute',
        'storedComponentTierAboveSix':'identity/substitution comparison only; no generic harvest entitlement','twoWatchCeilingScope':'framework work only; other subsystems retain governing rules'})
    cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'appliedRepairs':len(repairs),'machineRulesAligned':True}))

if __name__=='__main__':main()
