# GPT carrying and body source reconciliation

ChatGPT said:

The new source comparison materially changes the mass/load portion of my preceding proposal. I would withdraw the provisional ×4-per-size body-mass rule before implementation. Nothing in these sources says becoming Large multiplies the creature’s physical body mass or becoming Tiny divides it. Size has explicit effects on space and carrying capacity, while actual mass is a separate quantity needed by True Polymorph and modified by effects such as Petrified.

The coherent candidate should separate four ledgers instead of forcing them into one number:

Quantity	Authority/use in this candidate
PhysicalMassLb	Actual body/object mass in pounds. Used for explicit lifting, dragging, carrying another body, True Polymorph mass limits, and mass-changing conditions.
InventoryLoad	Gameplay Loop’s abstract personal cargo/burden measure. May be fractional. Used for routine inventory capacity and Burdened.
CasualtyLoad	Gameplay Loop’s fixed abstraction for transporting a body/casualty. Not physical body mass.
ExtractionClass	0–6 handling/risk/logistics category. Not pounds and not InventoryLoad.

This is a NEW PROVISIONAL domain-precedence bridge, not a claim that one filename supersedes another. V6 supplies the missing physical-weight procedures; Gameplay Loop retains its inventory/logistics system; Core supplies exact condition effects such as Petrified and the Secure Cargo action. The original records all remain intact.

1. Shared body, size, ordinary Druid events, and placement

The earlier body decision remains correct: Druid forms use the same Body, HP ledger, identity, conditions and physical inventory as every other transformation. Gear melding is already source-established; the missing piece is making ordinary Druid events update that shared body. 
Pasted text

RECOVERED: the exact expressed space is now:

Tiny: 2.5 × 2.5 ft
Small: 5 × 5 ft
Medium: 5 × 5 ft
Large: 10 × 10 ft

So my earlier “Tiny/Small/Medium all occupy one 5-ft cell” suggestion is superseded.

NEW PROVISIONAL implementation rule: the ordinary geometry layer should use a 2.5-ft subcell representation for physical occupancy. A Tiny creature uses one subcell, Small/Medium use 2×2, and Large uses 4×4. Size category remains separate from footprint dimensions because Small and Medium have different carrying/squeezing semantics despite both controlling 5 feet.

The existing Time Loop geometry cannot honestly implement this yet because it supports only integer cells on finite level ground. 
Pasted text
 Therefore a future temporal plan involving exact Tiny co-occupancy/clearance must use the upgraded geometry adapter or reject; the current 5-ft geometry must not silently approximate Tiny as Medium.

Ordinary Druid entry should now be one atomic body event:

RECOVERED: determine the legal form, size option, resources and geometry before spending the entry costs. The Druid guide already requires legal entry before payment. 
Pasted text

NEW PROVISIONAL: preflight the destination footprint at the existing spatial anchor and any required external-item drops. Only then pay Bonus Action/shift/use costs, create the form, assign Body.anatomy=formInstanceId, meld eligible current equipment, update expressed size, and update the canonical footprint. A voluntary shift cannot use resizing as free movement.

Druid-to-Druid form changes are continuous. Preserve the original meld set; never briefly return it to usable equipment. Recompute only the new form's size, movement/anatomy and compatibility of gear that was acquired externally while transformed.

A spell replacing the Druid is also continuous. The current spell helper already ends the Druid and then captures gear, but the complete body bridge must make those steps atomic so the original Druid gear is never exposed during an intervening window. 
Pasted text

Forced reversion remains different from voluntary entry. It happens even if root anatomy cannot currently fit. The reviewed transformation rule already says same anchor, no automatic teleport, no invented crushing damage. 
Pasted text

NEW PROVISIONAL placement rule: on mandatory reversion, first test the root footprint at the same anchor, including ordinary squeezing where legal. If it cannot fit, mark placementConflict. Canonical geometry may then make only the minimum involuntary legal adjacent placement in the same unobstructed region; this is not movement, costs no Speed, triggers no movement rider, and can never cross a wall or protected creature. If no such placement exists, leave the conflict pending rather than fabricating damage or teleportation.

Flying, burrowing and elevation still require the missing richer position adapter. The V6 rule now confirms that loss of usable flight causes falling unless hovering or otherwise held aloft. A Hawk/Sky Serpent/Tempest/winged spell form ending in the air therefore starts ordinary falling from its actual altitude, not from the ground. A buried body similarly does not jump to the surface. Current 2D Time Loop geometry cannot claim those scenes are solved.

2. Physical mass, carrying capacity, Inventory Load, casualty Load, and conditions
Physical body mass

There is still no source profile assigning new pound-mass values to the 26 Druid forms or the 12 creature-form spell profiles.

The current spell helper actually leaves Body.mass unchanged when applying a creature profile; only a True Polymorph object output assigns object_mass. 
Pasted text

I would elevate that into the shared bridge:

NEW PROVISIONAL: creature-form transformations preserve the body’s existing base physical mass unless an exact source expressly changes mass. Size does not itself change body mass.

Thus a 180-lb Medium character remains base mass 180 lb as a Tiny Hawk, Large Bear, Large Brute, Avian, elemental creature, etc. This is magical transformation, not mundane zoological scaling.

That is substantially safer than inventing mass from size. It also prevents Large anatomy from becoming a material-generation trick.

True Polymorph object anatomy remains the exception: the exact object output has its actual documented object_mass. Its existing ceiling remains the lesser of current input mass and immutable origin ceiling. 
Pasted text

Mass-changing conditions

Body.mass should represent the unconditioned physical anatomy mass. Do not overwrite it when Petrified starts.

Instead use:

effectivePhysicalMass = Body.mass × activeExactMassMultipliers

Core's Petrified therefore contributes exactly ×10.

This matters because condition state is independently current. A form/body event cannot accidentally erase the condition multiplier by assigning some form-default mass.

For a temporary Druid form, Petrified also brings Incapacitated; the existing Druid rules then end that temporary form administratively. After reversion, the root Body.mass remains its base mass and Petrified ×10 still applies. Permanent anatomy that legitimately survives the condition keeps its anatomy and receives the same ×10 overlay.

For True Polymorph object-output limits, use the effective current input mass, then still apply the immutable earliest-origin ceiling. Petrified can therefore never increase a creature-origin output beyond its origin mass, because that ceiling remains independently conserved.

Unknown future mass-changing conditions must receive an exact multiplier/policy before a mass-sensitive operation uses them.

V6 physical carrying/lifting

Use V6 for actual pound-based handling:

physicalCarryLb = STR × 15 × sizeMultiplier

For the bounded form sizes:

Tiny: ×0.5
Small: ×1
Medium: ×1
Large: ×2

Push/drag/lift is twice that limit. Between ordinary carrying capacity and the push/drag limit, push/drag Speed becomes 5 ft as preserved by V6.

Forms retain the character's actual Strength; no monster Strength score appears.

The V6 optional encumbrance variant is preserved but not stacked with Gameplay Load in this integration. Running both would impose two unrelated speed-penalty systems for the same routine inventory. It remains an optional historical alternative unless separately selected for the campaign.

Gameplay Inventory Load

Gameplay Load remains the routine equipment/cargo abstraction rather than being replaced by V6 pounds.

For the existing categories:

Medium capacity = STR Load
Small capacity = max(0, STR − 2) Load
Large capacity = 2 × STR Load

Gameplay does not define Tiny.

NEW PROVISIONAL Tiny completion: Tiny capacity = STR / 2 Load.

Do not round. Inventory Load is stored as a rational quantity. A STR 9 Tiny form therefore has capacity 4.5 Load, and its half-capacity threshold is 2.25 Load.

NEW PROVISIONAL exact threshold: at or above one-half capacity, through capacity, the creature is Burdened and uses the Gameplay penalties: Speed −10 ft and disadvantage on climb/swim/move-silently checks. Above capacity is not routine carried inventory; it requires some other physical handling procedure.

For items that have a native Gameplay Load, that value wins for InventoryLoad.

For items having pounds but no Load:

NEW PROVISIONAL conversion: InventoryLoad = pounds / 10, retaining the fraction and performing no rounding.

The reverse direction is weaker because Gameplay explicitly says approximately 10 lb. A Load-only record does not become documented physical mass for True Polymorph.

For ordinary non-magic-sensitive hauling, the equipment layer may use 10 × Load as a clearly labeled handling estimate when no pounds exist. But True Polymorph, material limits, and other effects explicitly requiring documented physical mass still require actual mass evidence.

Casualty Load

Preserve the Gameplay values:

Small = 3 Load
Medium = 6 Load
Large = 12 Load

They are not body weight.

NEW PROVISIONAL Tiny extension: Tiny casualty = 1.5 Load, continuing the explicit doubling sequence 1.5 → 3 → 6 → 12.

Transporting a creature therefore has two independent gates:

Can the carrier physically handle the actual effective pound mass under the V6 procedure?
Can the expedition/inventory system accommodate its casualty Load and associated cargo Load?

Neither substitutes for the other.

Petrified ×10 changes the pound-mass test. It does not silently multiply casualty Load by ten; casualty Load remains a size/bulk abstraction.

Extraction Class and Secure Cargo

Extraction Class 0–6 remains a risk/handling classification. It is neither pounds nor InventoryLoad.

NEW PROVISIONAL Core bridge: Secure Cargo performs one Action involving one discrete cargo unit/bundle with an assigned ExtractionClass. The action does not waive or expand:

physical carrying/lift limits;
InventoryLoad limits;
hands/harness requirements;
durability;
placement;
condition/custody rules.

The class number describes logistical danger/complexity, not “how many Loads can be lifted.”

This preserves the already-reviewed qualification rather than guessing that “Extraction Load class” is another weight unit.

3. Equipment, melded contents, containers, and custody

My previous equipment/custody framework mostly stands, but the new Load evidence requires one correction.

I previously treated melded items as continuing ordinary carried Load. That creates an unsupported problem where a perfectly legal Medium adventurer becomes unable to enter Tiny Hawk because their preexisting ordinary equipment suddenly exceeds the Tiny form's Gameplay capacity.

The better bounded rule is:

NEW PROVISIONAL: original gear that legally melds is removed from the transformed body's active InventoryLoad capacity calculation while melded, but its identities, Load, physical mass, ownership, charges, durability, containers and contents remain fully conserved in a separate melded-custody tree.

This does not create infinite cargo compression.

Entry may only meld items actually in legal current custody before transformation. You cannot pile beyond your legal pre-form load and then use Shapeshift to hide it.

While melded, the items and all contained contents are inaccessible: they cannot be drawn, fired, consumed, transferred, opened, used as material components, reloaded, or charged.

New external cargo acquired after shifting is subject to the transformed form's current InventoryLoad capacity.

When the transformed character itself is carried as cargo, the carrier's handling record includes:

casualtyLoad(expressedSize) + subject's melded InventoryLoad + subject's external cargo Load

and physical lifting uses:

effective body mass + documented/handling mass of all physical cargo in that body's custody

So Shapeshift cannot turn a backpack full of iron into weightless transport merely because it is inaccessible to the Druid.

This keeps three things distinct:

melded items do not hinder the Druid's own transformed inventory capacity;
they still physically/logistically accompany the character;
they remain unavailable and cannot generate duplicates.

Containers follow the same rule. A backpack that melds takes its whole custody subtree with it. Its contents remain separate item identities and current charges/stock remain current.

Compatibility across all forms

For all 26 Druid forms, preserve the reviewed default: no generic hands are invented. Hero/Arch speech does not imply hands. 
Pasted text

For the 12 spell profiles, Humanoid alone has explicit hands; the other 11 do not. 
Pasted text

The common candidate therefore remains:

Equipment	Druid 26	Spell Humanoid	Other 11 spell creature profiles
Original worn armor	Melded, ordinary armor AC/use suppressed	Original gear is still melded by the spell; may equip real external armor afterward	Melded; external ordinary armor default incompatible absent exact certification
Original shield/weapon	Melded/unusable	Melded original; newly acquired compatible external weapon/shield usable	No hands, so ordinary held use unavailable
Focus/tool/components	Melded/inaccessible	External real items can be used normally if source permits	No generic hand use
Worn/held magic property	Suppressed while its required item is melded	Works only if externally actually worn/held	Suppressed unless exact anatomy-compatible source
Attunement/possession-only passive	May continue when equipment adapter certifies it truly requires neither wearing, holding nor activation	Same	Same
Container and contents	Meld whole custody subtree	External container can be carried normally	Requires exact anatomy-compatible external custody
New external gear	Never joins old meld set	Ordinary compatible gear possible	Only source-certified nonhand/anatomy-compatible gear

Spell Humanoid having hands does not unmeld the gear captured when the spell began. It can acquire real external gear later. That distinction is already consistent with the spell rules, which treat original meld and later external equipment separately. 
Pasted text

On Druid form-to-form change, keep the original meld tree untouched. Revalidate only external gear. Anything incompatible must have a legal drop destination preflight before a voluntary change.

On final reversion, surviving melded items attempt to return to their recorded prior custody. Current external equipment and conserved ownership win conflicts. If an old armor/weapon slot is occupied, do not overwrite the current item; the returning item moves to legal carried storage or drops at the anchor/nearest legal adjacent item location. Destroyed, consumed, transferred, or otherwise no-longer-owned identities never reappear.

If restoring all returned items would exceed the root form's active InventoryLoad capacity, excess returning items are resolved through the same custody/drop procedure rather than deleting them or making the reversion illegal. Forced reversion cannot be blocked merely by cargo overload.

For Time Loop later, this remains compatible with the settled rule that snapshot meld membership is intersected with current existing/owned item identities, while current charges, durability, quantities and ownership stay conserved. The physical provenance layer already prevents surviving transferable matter from being cloned or silently erased. 
Pasted text

Revised conference disposition

I would record the corrected candidate as:

SOURCE-DISCUSSED / IMPLEMENTATION-READY — shared Druid/spell Body, exact size/space, physical-pound mass, Gameplay InventoryLoad, casualty Load, ExtractionClass, condition-mass overlay and equipment/custody bridge reconciled.

The main corrections to my preceding answer are that form size does not automatically rescale body mass, Tiny must retain its actual 2.5-ft combat space, and melded original gear is conserved separately rather than automatically burdening the form's own active InventoryLoad.

The NEW PROVISIONAL rules are the domain split between pounds/Load/ExtractionClass, Tiny InventoryLoad and casualty values, fractional Load arithmetic, weight→Load conversion, current-mass condition overlay, melded-load handling, Secure Cargo interpretation, 2.5-ft subcell geometry, and the bounded forced-placement/custody procedures.

Full ordinary bridge code, richer altitude/burrow geometry, item-specific exceptions, parent restoration, full Time Loop, and the whole-game/GitHub gate remain open.
