# Leatherworking — next source preparation

The source audit preserves all 44 Leatherworking recipes (IDs 280–319 and 652–655): 30 public, one restricted and thirteen Director-only. All 30 public current effects match the actual V5 book paragraphs. No authoring direction or exact-card approval is implied. Begin this conference after the current Blacksmithing exact review and report that review's actual outcome/counts.

The full originals, every component occurrence, work fields, visibility and exact public bindings are in LEATHERWORKING_SOURCE_PREPARATION.json. Original files remain unchanged.

The next conference needs these concrete decisions:

1. **Container capacity versus encumbrance relief.** Current effects promise 10/20/30/40/50 lb carried without counting against normal encumbrance, while mechanics.capacityPounds stores the same number. A normal Pouch holds only 6 lb/0.2 cubic feet; Backpack holds 30 lb/1 cubic foot. Decide whether the recipe expands physical capacity or waives some weight within an existing capacity, and define volume, shape, closure and access. Quiver, Belt and Harness need actual container profiles rather than unlimited abstract slots.

2. **Conservation and nested containers.** Distinguish actual pounds from effective carried Load and Extraction Class. Resolve empty-body weight, liquids, coins, living occupants, corpses, external attachments, nested ordinary/magical containers, multiple packs on one bearer, transfer, suppression, Broken state and dropped containers. Weight relief must not duplicate mass removal through repeated nesting or create a universal portable-space rule. Confer before deciding any metaphysical explanation; cosmology stays post-push.

3. **Bonuses with finite task scopes.** Containers add +1/+2/+3 to checks to secure/retrieve their contents; other gear adds a bonus to a related mobility/handling check. These need exact eligible tasks, who makes the roll, when a roll is actually required, action costs, equipment/access prerequisites and stacking. They do not automatically grant attacks, AC, saving throws, free retrieval or proficiency.

4. **Actual wearable models and slots.** Boots, Gloves, Leather Gear, Armor, Coat and Harness need complete base bindings, pair quantity, mass, material AC/HP, mundane price, fit, hands and don/doff. Resolve conflict with the now-drafted Blacksmith Gauntlets handwear slot, armor suits, ordinary clothes, other belts/backpacks and unarmored restrictions. Leatherworking Armor's current armorBonus is zero; do not import an AC bonus from the word Armor or from Blacksmithing.

5. **Durable construction, grade and quality.** Discuss whether the actual mundane base-body method from Blacksmithing also fits these outputs; do not assume cross-trade approval. Preserve exact components and maximum quality yield, separate supplemental bodies/stock from source costs, handle source fuel/solvent/waste and avoid creating large containers from tiny parts. Durability improvements, prior flaws, grade, magical breakage, repair/reconstruction and suppression need explicit bindings.

6. **Resistances and misleading names.** Only the current printed resistance applies, with exact worn/functioning requirements. Black-Dragon Acidproof Boots currently print only a +2 mobility/handling bonus and no acid resistance. Mammoth-Hide Winter Coat prints cold resistance but no additional climate immunity. Tags, donor metadata, wholeCreatureUse and legacy names supply no unprinted powers. Preserve these discrepancies for review.

7. **Work and access.** DEX / Leatherworker's tools / Tannery Bench, Awl and Cutting knife remain exact. All source field flags, time modes, assistance and ingredient-age rules need their actual shared-framework treatment. Recipe-319 source time is one year with null active hours; keep that null and a separately labeled operational work-year overlay if used. Do not automatically import Blacksmithing's phase, workshop or repair credential.

8. **Economics and player separation.** Preserve Standard source batch values and all 30/1/13 visibility gates. Set how additional actual bodies, size, source-unit share, legitimate quotes, repair and resale work. No automatic artifact valuation, source-monster availability, generated bestiary authority or ingredient-origin conclusions. Full numerical balance/runtime/whole-game closure remains separate.

This preparation does not reduce the recipe queue. The current Blacksmithing set is authored but remains pending exact review. No source deletion or GitHub push has occurred; cosmology remains deferred until successful authorized push and verified remote commit.
