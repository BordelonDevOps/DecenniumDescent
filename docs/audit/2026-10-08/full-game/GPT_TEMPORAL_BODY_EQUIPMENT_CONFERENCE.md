# GPT shared body, equipment and mass conference

ChatGPT said:

The gap is real: the Druid rules already say there is one body, that gear melds, and that size/anatomy changes matter, but DruidState currently mutates only its own form/resource state. TransformationWorld.Body is therefore missing ordinary Druid body events that the spell-transformation path already records. 
Pasted text

I would settle the three issues as follows. I distinguish CONFIRMED / RECOVERED rules from NEW PROVISIONAL integration rules.

Shared Body / ordinary Druid events

CONFIRMED / RECOVERED: A Druid form remains the same physical identity and HP ledger. Gear melds and cannot be used; shifting does not repair, reload, restore charges, or refresh it. Druid entry has to pass source/space legality before payment, while an actual form ending removes dependent effects only after the triggering packet is fully resolved. Unsupported loss of flight begins ordinary falling. 
Pasted text

The ordinary bridge should therefore make the shared TransformationWorld.Body authoritative for expressed anatomy even while the source is Druid rather than spell transformation.

NEW PROVISIONAL — canonical body event model: use Body.anatomy for the currently expressed transformation identity regardless of whether that identity is a spell Link or a Druid FormInstance. Resolution must distinguish the two registries rather than assuming every non-None anatomy ID is a spell link.

On the first Druid entry from root anatomy:

preflight the destination form profile, effective size, physical footprint, current inventory/custody state, and all required item placement;
only after that succeeds, pay the Bonus Action/shift/other entry costs;
create the real FormInstance;
set Body.anatomy = formInstanceId;
move the Druid's current body-carried/worn/held gear into its meld record;
set Body.size and Body.mass to the expressed form values;
update the canonical pose/footprint atomically;
do not create a second HP/body record.

The existing rule that illegal entry spends nothing therefore extends to body fit and required item-drop legality. 
Pasted text

On a Druid form → Druid form change, there is no momentary root body. Preserve the original meld chain. Do not return the old gear, make it usable for an instant, and immediately meld it again. End the old form-dependent effects, create the new instance, and atomically change expressed size/mass/footprint. Any external gear acquired while transformed is not silently added to the original meld set; it is reconciled against the destination anatomy as discussed in issue 3.

This differs intentionally from the spell rule under which one transformation closes and the next spell immediately recaptures the resulting gear. The spell path expressly has a close-and-recapture transaction with no intervening action window. 
Pasted text

A spell replacing a Druid form is likewise continuous. The Druid instance ends and its dependent form effects close, but its original melded items never become usable between operations. The successful spell then owns the expressed anatomy and captures any currently external gear required by the spell's ordinary transformation rules. This needs one atomic body transaction around the existing druid._end('spell-transformation') path rather than today's disconnected calls. The current spell helper already ends the Druid before installing the link, which is the right source order but not yet the complete body transaction. 
Pasted text

On final Druid reversion/expiry/forced ending:

clear the Druid anatomy identity;
return root Body.size and root physical mass;
end form-dependent shield/creature/effect children;
return only original melded item identities that still exist and are still legally in that character's custody;
reconcile external gear and equipment slots;
resolve root placement from the same spatial anchor.

Do not restore destroyed, consumed, transferred, or otherwise physically unavailable items. That is already required by the Time Loop physical/gear decisions and by the spell transformation rules. 
Pasted text

NEW PROVISIONAL — footprint convention: for these 26 Druid and 12 spell profiles, use one grid cell for Tiny/Small/Medium and a 2×2 footprint for Large. An ordinary voluntary change to a larger form selects a legal footprint containing the existing anchor; the anchor itself does not move. Same-size form changes preserve the current footprint where possible rather than using transformation as free repositioning.

Large is only used where the exact Druid profile's mayLarge permits it; Hawk remains Tiny; otherwise the exact profile size wins. The 12 spell forms use their explicit Tiny/Small/Medium/Large profile size without inference. 
Pasted text
 
Pasted text

Forced ending is different from voluntary entry. A mandatory reversion is never prevented simply because the root shape does not fit. It occurs, then placement is reconciled. The existing transformation rule already requires the same anchor and forbids invented crushing damage or teleportation. 
Pasted text

NEW PROVISIONAL — mandatory placement resolution: first try the normal root footprint at the same anchor. If the ordinary squeezing rules make that anatomy legal at that same anchor, use squeezing. Otherwise mark a real placementConflict; do not grant voluntary movement. The canonical geometry resolver may make at most an involuntary nearest-adjacent placement into a legal footprint in the same unobstructed region, never through a wall/closed barrier/occupied cell. It costs no movement and triggers no movement benefits because it is placement normalization, not a Move. If no adjacent placement is legal, keep the conflict unresolved until the obstruction is removed or another legal relocation effect occurs.

That is intentionally stricter than “search arbitrarily far for somewhere to put the character.”

Flight/burrow/climb require one more explicit boundary. The present kernel geometry is only a finite level-ground plane. 
Pasted text
 So:

entering Hawk/Sky Serpent/Tempest/air-elemental while currently on legal ground is fine; gaining flight itself does not require an elevated pose;
once the body actually occupies altitude, the canonical position system must retain altitude. Reversion without flight starts falling from that location; never snap to ground;
a form ending while actually burrowed cannot teleport to the surface. It becomes a terrain-placement conflict requiring the vertical/terrain geometry adapter;
Master of Vermin's “Tiny gaps” likewise needs a clearance-capability field rather than pretending its Medium size became Tiny.

In other words, the new body bridge can be complete about events and ownership without falsely claiming that the existing 2D geometry already models altitude, burrowing, ceilings, or narrow-clearance traversal.

Mass and same physical identity

There is no existing profile-level mass authority for the 26 Druid forms. The Druid profiles supply size but not mass. The 12 spell creature profiles likewise supply sizes but not creature-form mass. What does already exist is immutable PhysicalOrigin.mass, mutable Body.mass, and True Polymorph's requirement for documented current/origin mass when creating an object. 
Pasted text
 
Pasted text

Therefore retaining root mass in every form would itself be an invented rule. It also produces particularly bad outcomes for Tiny Hawk and Large anatomy.

NEW PROVISIONAL — bounded form mass rule: use magical anatomy mass scaled from the immutable earliest physical origin, never from the previous transformation:

effectiveMass = max(1, ceil(originMass × 4^(effectiveSizeIndex - originSizeIndex)))

with adjacent categories scaled ×4 upward or ÷4 downward.

For the bounded relevant sizes that means, relative to a Medium-origin character:

Tiny = origin mass ÷16;
Small = origin mass ÷4;
Medium = origin mass;
Large = origin mass ×4.

This is a gameplay mass convention, not a biological simulation.

It applies to both Druid profiles and the 12 creature-form spell profiles so the shared Body.mass does not change semantics depending on which transformation subsystem expressed the anatomy. Optional Druid Large uses the Large value. Hawk uses Tiny. Elemental/Vermin variants use their actually expressed profile size. Spell Avian uses Small; Brutes/Greater Winged/Elemental Earth use Large; the other supplied profiles use Medium. 
Pasted text

Always derive it from the earliest immutable origin, so repeated shape chains never multiply mass exponentially.

CONFIRMED interaction with True Polymorph: the object-output ceiling remains min(current anatomy mass, earliest origin mass). Therefore becoming Large does not magically let a 180-pound person create a 720-pound saleable object. Becoming Tiny does lower the currently available mass ceiling while Tiny. Chains never rebase the earliest-origin ceiling upward. 
Pasted text

NEW PROVISIONAL physical interpretation: transformation-created excess or reduced body mass is magical anatomy state, not independent matter. It cannot be harvested, sold, butchered, stockpiled, or separated into a new physical root. Any severed/derived matter remains subject to the existing root-provenance/no-duplication rules.

Body.mass should represent the expressed body only. Equipment mass remains attached to the actual item identities. If a rule needs total supported/carried weight, calculate body mass plus the current physical items in that body's custody, including melded items. Do not add equipment mass to True Polymorph's body-to-object mass allowance.

Meld therefore does not erase encumbrance or ownership. It only makes the item inaccessible/inoperative. Hawk's explicit prohibition on carrying Medium allies remains exact; do not invent a separate “Hawk cannot fly with its own ordinary gear” limit unless the general carrying/encumbrance rules independently produce one. 
Pasted text

Actual form entry should record:

immutable origin mass and size reference;
expressed profile/effective size;
calculated effective body mass;
current distinct inventory/custody IDs.

The form does not own a new physical root.

Equipment / physical custody / reconciliation

CONFIRMED / RECOVERED: the current guides already establish several hard boundaries:

original Druid equipment melds and cannot be used;
worn armor AC, shield AC and properties requiring melded gear use are excluded;
shifting never repairs, reloads or restores charges;
spell transformations meld original carried/equipped gear;
destroyed/consumed/lost gear never reappears;
Shapechange keeps compatible external gear and drops incompatible external gear;
only the spell Humanoid profile explicitly has hands; the other 11 spell profiles have none;
no Druid form invents hands. 
Pasted text
 
Pasted text
 
Pasted text

The current Body.equipment/Body.melded sets are not enough to implement “returns in its prior state,” containers, slot conflicts, or external gear. The ordinary bridge therefore needs runtime custody metadata, while continuing to use the existing physical item identities rather than creating another inventory.

NEW PROVISIONAL — custody record: each discrete physical item needs, alongside its existing owner/provenance, a current custody state such as:

WORN(slot)
HELD(hand/slot)
CARRIED(container/body)
MELDED(anatomyMeldId, priorCustody)
GROUND(location)
DESTROYED/CONSUMED/TRANSFERRED through the existing physical history.

Ownership and custody are separate. “I still own the sword in the wagon” does not mean it melds when I turn into a Hawk.

On first Druid entry, meld only gear physically on/in the body: worn, held and body-carried items, including carried containers and their contained item identities. Do not pull remote/stored owned property into the form.

Containers remain distinct physical objects. A melded backpack and every object inside it remain current identities with current charges/stock/durability. They are inaccessible while melded; contents cannot be withdrawn, added, fired, consumed or used as components until custody returns.

Common compatibility defaults:

Item category	Druid forms	Spell Humanoid	Other 11 spell profiles
Worn armor	Original armor melded; AC/properties requiring wear suppressed	Ordinary anatomy/size rules may permit	Default incompatible unless exact item says nonhumanoid/form-compatible
Shield / held weapon	Melded and unusable	May use normally	No hands → unusable
Hand-held focus/tool/material	Melded/inaccessible	May use if ordinary source permits	No hands → unusable
Passive magic requiring “worn/held/equipped”	Suspended while melded	Works only if actually compatible/equipped	Suspended unless exact item says otherwise
Passive numeric effect requiring only possession/attunement, with no physical-use predicate	May remain if source/item adapter certifies it	May remain	May remain if anatomy-independent
Carried container/content	Melds as custody tree; inaccessible	Can remain carried if legal	Only if exact anatomy/custody rule allows; otherwise meld/drop as source transaction dictates
Newly acquired external gear	Never joins original Druid meld set	Ordinary use possible	Only exact nonhand/anatomy-compatible gear

The important default for passive magic is therefore not “all magic items keep working.” It is: if the source says “while worn/held/equipped,” meld suspends it. If the source is genuinely body-independent and only requires attunement/possession, the equipment adapter may certify it as continuing. Exact item wording overrides this default. This is the meaning I would give the existing “compatible certified passive bonus” language. 
Pasted text

For the 26 Druid profiles, none receives generic hand use. Arch/Hero speech does not create hands. An exact future form/item card can override that, but profile name or vaguely humanoid appearance cannot.

Druid form-to-form: preserve the original meld set and its prior-custody metadata. Newly acquired external gear stays external if compatible with the destination form. If it becomes incompatible, preflight its drop for a voluntary shift. Dropping it does not add it to the meld set and does not destroy it.

Shapechange/internal spell switch: use the same per-item compatibility logic rather than today's coarse “if any retained gear, destination must have hands” test. Hands are required for held items, not necessarily for every passive collar/harness/body-independent item. The existing helper's single hands gate is therefore too coarse for the final equipment bridge even though it was adequate for the bounded spell profile tests. 
Pasted text

Final Druid reversion: reconcile in this order:

Current external items that still exist and are already legally equipped/carried remain current.
Each surviving original melded item tries to return to its recorded prior custody/slot.
If that slot is now occupied by a conserved current external item, do not overwrite the current item. Return the old item as ordinary carried inventory if legal.
If it cannot legally be carried/equipped, drop it at the current anchor or nearest legal adjacent item placement.
If no legal drop placement exists, mark that item placement pending; do not delete it, duplicate it, or move another character.
Destroyed, consumed, transferred or externally owned items never return.

Current external gear therefore has priority over reconstructing an old equipment slot, because current ownership/custody is conserved. The old melded sword may come back into the backpack instead of knocking a newly equipped sword out of the character's hand.

For Time Loop later, preserve the already-settled formula:

restored meld = snapshot meld ∩ currently existing identities ∩ identities still legally owned/held by participant

Current external gear remains external. Incompatible external gear gets the same atomic drop preflight. Charges, ammo, stock, durability and ownership remain current. Nothing about anatomy restoration refreshes an item. The existing physical provenance layer already requires surviving transferable physical identities to reconcile rather than be cloned or silently retired. 
Pasted text

The implementable ordinary bridge I would expect from these decisions is therefore a single DruidBodyBridge over the existing TransformationWorld.Body, Inventory/custody state, BufferLedger and canonical geometry, not a second Druid body. It should own source-qualified entry/change/end body transactions, effective size/mass, meld/custody metadata, and placement preflight; DruidState should continue owning form resources, local uses and clocks.

I would record this conference as:

SOURCE-DISCUSSED / IMPLEMENTATION-READY — ordinary Druid shared-body, mass, equipment/custody and placement bridge settled.

The clearly NEW PROVISIONAL pieces are the size→footprint rule, factor-4-per-size mass rule, body-mass-vs-item-mass separation, explicit custody states/slot conflict priority, nonhand equipment defaults, and the bounded mandatory-placement procedure. The gear-meld/no-refill rules, one-body identity, spell-form hands/sizes, no-duplicate physical matter, same-anchor reversion, and conserved ownership/loss rules are recovered from already-reviewed sources.

Full parent restoration, 3D/elevation/burrow geometry implementation, complete item-specific compatibility mapping, the seven larger integrations, full Time Loop, and the final whole-game/GitHub gate remain open.
