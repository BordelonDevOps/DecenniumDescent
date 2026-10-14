# GPT final transformation interfaces

ChatGPT said:

These seven interfaces can be closed without reopening any previously settled class access, costs, profile list, concentration transaction order, Mass target count, or True Polymorph permanence. I would encode them as NEW implementation bridges, not recovered source text.

1. Creature types, physiology, and natural attacks

Confirm the proposal with one qualification on attack-count modifiers.

Creature-origin transformations

A spell-form profile changes anatomy, not creature type.

Retain unchanged:

original creature-type tags;
ancestry/species identity;
class identity;
character/NPC identity;
soul/origin state;
nonanatomical passive features, subject to their actual predicates.

Do not gain humanoid, beast, elemental, undead, etc. merely because a profile resembles one.

The selected anatomy controls only the things it actually replaces:

size;
movement modes;
anatomical senses;
speech;
hands/manipulators;
supplied natural attacks;
anatomy-specific AC/defenses.

An original anatomical option is unavailable while the required anatomy is absent unless its own feature explicitly says it survives transformation.

Examples: original claws, wings, gills, bite, hand-dependent manipulation, etc. do not coexist underneath the selected spell anatomy.

Object-origin creature manifestations

Assign:

originTag = transformed-object

They gain no ordinary biological creature-type tag merely from the profile:

no humanoid;
no beast;
no elemental;
no undead.

Immutable object-origin restrictions remain in force.

Attacks

Every supplied spell-profile melee attack has:

reach 5 ft;
one supplied natural/form attack per ordinary Attack Action;
no imported Multiattack.

An existing subject feature may modify that Action only if its exact wording legally applies to:

natural attacks;
form attacks; or
the Attack Action generically without requiring an unavailable weapon/anatomical component.

So a future exact feature could authorize more attacks, but the profile itself never does.

Weapon-only interoperability remains gated.

2. Mandatory reversion with insufficient space

Confirm the no-teleport proposal.

When a temporary transformation must end:

its original anatomy returns at the same spatial anchor;
the transformation adapter does not move the subject;
it does not push the subject through solid geometry;
it does not deal invented crushing damage;
it does not restore another displaced anatomy;
it does not heal.

If the restored anatomy cannot legally occupy the current geometry, return:

placementConflict = true

and hand the state to the canonical geometry/collision subsystem.

Until that subsystem resolves the conflict:

no free relocation occurs;
no wall traversal is created;
the character cannot use the unresolved overlap to establish legal movement/targeting through a barrier.

This packet therefore leaves one explicit follow-up dependency:

mandatory-reversion geometry conflict resolution

Do not invent nearest-space teleportation inside the transformation spell helper.

3. Creature-origin object anatomy at 0 HP during shaping

Confirm your proposal.

During True Polymorph's first-minute shaping phase, a creature-origin target link ends if, after all same-packet prevention/replacement:

actual HP is 0;
the creature is actually dead; or
an external effect actually applies Incapacitated.

This applies to both:

creature→creature; and
creature→object.

So even if some feature allows a creature to remain conscious or otherwise functional at 0 HP, actual 0 HP itself ends the shaping link.

That is distinct from object anatomy being actionless.

actionlessObjectAnatomy is not Incapacitated and does not itself end:

the target's unrelated concentration;
the caster's True Polymorph shaping concentration.

After True Polymorph stabilizes permanently, reaching 0 HP does not automatically revert the anatomy.

4. Object-origin creature slot ownership through recasts

Confirm the immutable sponsor model.

When caster A successfully creates an object-origin creature:

slotSponsor = A

That sponsor remains attached to the underlying object-origin creature identity through every legal creature-profile replacement.

Therefore caster B successfully True-Polymorphing that same object-origin creature into another creature profile:

does not transfer slot ownership to B;
does not consume B's object-creature slot;
does not grant B control merely because B supplied the new profile;
leaves A's slot occupied.

The same principle applies to any otherwise-legal temporary creature-form replacement: anatomy changes do not change origin sponsor.

Under the current rules, ordinary Polymorph cannot overwrite an already stabilized True Polymorph anyway. If a future legal state permits Polymorph on the same object-origin creature identity, the sponsor still remains A.

A's active slot releases only when that identity actually ceases to be an object-origin creature manifestation, such as:

physical destruction;
actual ending/dispel restoring the original object;
successful allowed transformation into object anatomy.

If B later takes that now-object identity and performs a fresh object→creature True Polymorph, that is a new creature manifestation and reserves B's slot.

Antimagic suppression never releases the sponsor slot.

Historical origin metadata remains immutable even after the active slot is released.

5. Antimagic and the first-minute timer

I would not make temporary transformation links end merely because antimagic suppresses them.

Use one consistent suppression model.

NEW rule

Antimagic suppresses but does not end:

Polymorph;
Mass Polymorph target links;
Shapechange;
True Polymorph during its shaping minute;
stabilized True Polymorph.

While suppressed:

underlying/root anatomy is physically expressed;
the transformation record remains active;
concentration remains required where applicable;
concentration can still end normally;
the absolute duration/stabilization clock continues;
no timer resets;
no second anatomy record may silently stack underneath it.

For ordinary 60-second transformations, the spell may expire while suppressed.

True Polymorph shaping

Its 60-second shaping checkpoint continues while suppressed.

If at the checkpoint:

concentration is still valid; and
the link has not otherwise ended,

the spell stabilizes permanently even while suppressed.

When antimagic later ceases, the stabilized transformed anatomy resumes.

This preserves the meaning of one uninterrupted spell record instead of making brief suppression erase an otherwise valid 26-RP rank-9 transformation.

Replacement while suppressed

A suppressed transformation still occupies the target's one active transformation slot.

A new transformation may target it only if normal replacement rules permit that replacement.

If the new transformation actually succeeds:

the suppressed old record ends;
only the new record remains.

Same-caster concentration replacement still follows the previously settled commit rule: starting the new concentration spell ends the caster's old concentration even if that old transformation is currently suppressed.

No hidden-form stack exists.

6. Melded equipment when one transformation replaces another

Use the close-and-recapture procedure, not a permanent first-root meld set.

On a successful different transformation replacement, perform one atomic transaction:

close the old anatomy record;
restore every still-existing item in that old record's original meld set to the restored underlying anatomy;
do not recreate dropped, destroyed, consumed or otherwise absent items;
include any legitimately equipped external gear currently on that restored anatomy;
immediately start the new transformation;
snapshot all currently equipped/carried items eligible to meld as the new record's original meld set;
apply the new anatomy.

There is no intermediate action/reaction/targeting window between steps.

This procedure applies to:

spell replacing spell;
True Polymorph replacing an allowed prior transformation;
a spell successfully replacing Druid Shapeshift.

For Druid replacement specifically:

the Druid form actually ends;
its original equipment returns once;
then the new spell captures the resulting equipment state.

External equipment that had previously been dropped because an anatomy could not use it remains where it was dropped. It is not teleported back into the new meld set.

Likewise, destroyed/lost equipment never regenerates.

Important exception: suppression

Antimagic suppression is not record closure.

Therefore it does not rebuild or recapture a meld set. When suppression ends, the same transformation record and same meld identities resume.

This approach keeps item identity conserved while allowing a genuine new transformation record to have a coherent new equipment snapshot.

7. Healing legality in object anatomy

Confirm.

Creature-origin currently in object anatomy

The underlying identity remains a creature-origin character for HP/Wounds/death history, but its current target anatomy is an object.

Therefore an effect whose targeting requirement is:

one creature / living creature / ally creature

cannot newly select it while object anatomy is active.

Ordinary magical healing does not become object repair.

So:

no new Cure-type creature-target healing;
no healing-to-object conversion;
no special repair unless an exact source explicitly permits it.

When creature anatomy legally returns, ordinary creature healing eligibility returns.

Existing attached effects

Effects already attached before transformation continue or stop according to their own exact lifecycle.

If the effect:

was already applied and simply has an independent duration, it is not automatically erased solely because anatomy changed;
requires a fresh eligible creature target at each pulse/tick, that later pulse must recheck current target legality and may fail while the target is an object.

No generic transformation rule overrides those source-specific procedures.

Object-origin identity

An object-origin identity never acquires ordinary healing eligibility, even while currently represented by creature anatomy.

Its immutable origin restriction survives all transformation chains.

If future source-qualified nonorganic repair applies, that is its own separate procedure and not HP healing by analogy.

Disposition

These seven bridges complete the currently identified identity/anatomy/permanence integration boundaries for the five-spell draft package.

The implementation should now preserve three separate concepts explicitly:

immutable origin identity — creature-origin vs object-origin;
current anatomy — one active physical expression;
transformation source record — caster/source/profile/concentration/permanence/meld set/slot sponsor.

That separation prevents the main laundering problems: creature types, souls, healing rights, companion ownership, hidden forms, and equipment duplication.

The five spells should remain complete draft proposals / implementation pending until Codex returns the actual helper, profiles, tests, and player-facing procedure for independent review.
