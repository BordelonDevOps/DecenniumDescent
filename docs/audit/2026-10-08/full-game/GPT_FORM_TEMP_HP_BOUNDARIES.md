# GPT form and buffer boundary decisions

ChatGPT said:

The 12 boundaries can be settled without changing the 175 classifications. I would treat the following as the implementation contract before code.

1. “Until lost” does not override V6 long-rest expiry

Merely restating depletion as “until lost” or “until lost or replaced” is not an explicit indefinite-duration exception.

V6 still controls:

temporary HP last until depleted or after a long rest, unless specified otherwise. 
Pasted text

Therefore these four grants use the V6 default next-completed-long-rest endpoint:

mage.hero.archmage.harmonized-core
wizard.hero.necromancer.arcane-leech
paladin.supplement.oath-of-the-ancients.primordial-surge
paladin.supplement.oath-of-the-martyr-king.king-s-smite

“Until lost/replaced” describes ordinary depletion/replacement, not immunity to long-rest expiration.

Only an actual stated duration such as 1 minute, 2 rounds, encounter end, or “while X remains” overrides the default. 
Pasted text

2. Exact lifetimes for the ten questioned grants

Use a consistent distinction:

A source's duration does not automatically become the lifetime of an instantaneous temp-HP grant. The buffer follows the source duration only where wording actually links the buffer to that continuing state.

Decisions:

Source	Buffer lifetime
Bloodbond M grant	V6 default; each qualifying trigger creates an instantaneous grant. Bloodbond concentration ending does not itself erase accepted temp HP.
Lingering Malice Drain M	V6 default; pulse creates an instantaneous grant. Zone ending does not remove accepted temp HP.
Nature's Blessing	V6 default. Speed/forced-movement rider lasts with concentration; the start-only shield is not explicitly stated to vanish with it.
Dread Shelter	V6 default for the one casting-time shield. DR alone is concentration-linked for 1 minute.
Nano-Aegis commanded shield	V6 default. Each paid command creates a separate instantaneous offer; support mode ending does not erase accepted buffer.
Protective Programming	One triggering hit only. The explicit duration: One hit governs the shield itself; any points remaining after that triggering hit disappear.
Monk Discipline Initiate Support	V6 default. Permanent technique availability is not permanent shield duration.
Warder Arrow / capstone	V6 default; instantaneous Arrow-generated grant.
Unbroken Covenant	Until the Final ends (3 rounds). Its preserved source expressly ties the granted temp HP to the Lock ending.
Noble Bearing	V6 default; concentration controls the selected-allies/morale/trigger source, but no separate shield expiry is printed.

Protective Programming is therefore the important short-lived exception: grant before the hit, absorb that hit normally, then discard any remainder. 
Pasted text

3. Tie rule and Noble Bearing replacement

Confirmed.

General arbitration:

incoming greater than current → replace;
incoming lower → reject;
equal → retain existing active grant;
rejected/equal incoming grant cannot donate its expiry or linked permissions.

“Replace” only overrides this when the source explicitly identifies the currently active grant being replaced.

For King's Smite + Noble Bearing:

calculate the source-internal result first;
if Noble Bearing applies to that Smite/recipient, it replaces the King's Smite component inside that source transaction;
produce one Noble Bearing offer;
compare that resulting offer against whatever unrelated active temp HP the target already has.

Thus an equal Noble offer does not displace an unrelated equal shield.

Bloodshield's Reaction exists only if the Bloodshield grant actually becomes active. If its offer loses arbitration, no Bloodshield-linked Reaction exists.

Protective Verse's saving-throw rider is independent and may exist even if its temp-HP offer loses. 
Pasted text

4. Mooncursed Howl reserve allocation

Use deterministic sequential allocation.

NEW integration:

choose and order up to three legal ally recipients before rolling;
roll the one shared 2d8;
for each recipient in declared order:
offer = min(sharedRoll, remainingBufferReserve)
deduct that entire offer from Reserve before ordinary temp-HP arbitration;
continue to next recipient.

Example:

roll = 12
Reserve = 9
recipients A, B, C

Offers are:

A = 9
B = 0
C = 0

Not 3/3/3.

The Druid cannot voluntarily reduce a positive permitted offer to conserve Reserve. “Draws that many, up to remaining” is not discretionary allocation.

A zero offer:

creates no BufferGrant;
creates no linked buffer rider;
consumes no additional Reserve.

A legal ally-mode Howl may still be activated with Reserve 0 if at least one legal ally is selected. It spends the Howl opportunity and Form Surge but produces no temp HP. That is a paid exhausted-resource outcome, not an empty-target farming activation.

Bear/Earth Warden form entry likewise remains legal at Reserve 0 because those forms have other actual traits; their buffer component simply creates no grant. 
Pasted text

5. Form identity and renewal

Confirmed with one explicit choice:

Natural renewal

At the natural 10-minute endpoint, spending another Shapeshift use to remain in the same form:

keeps the same FormInstance;
requires no additional BA;
extends only that form's endpoint by another 10 minutes;
does not re-enter the form;
does not clear Refrain;
does not redraw Buffer Reserve;
does not reset Form Surge/local once-transformation flags;
does not recreate entry effects.

Existing linked effects remain only according to their own deadlines.

So renewal does not extend:

Carrion Rat King's 1-minute swarm;
Broodmother swarm's independent shorter limit;
Charbear Smoke's 3 rounds;
any other fixed-duration subeffect.

At level 20 the renewal shift-use cost is 0. It may still be declined, causing ordinary reversion.

Early identical-form request

NEW rule: attempting to “change” early into the already-current identical form is rejected before payment. It is neither a change nor an early renewal.

This avoids arbitrary duration extension and re-entry farming.

Reversion/change

Early voluntary reversion:

BA;
no shift use;
ends current form instance;
does not clear Refrain.

A genuine different-form change:

BA;
shift use below20;
ends old instance;
creates a new instance;
clears Refrain name/count;
retains Dissonance.

Returning later to a previously used form, including after normal reversion, is a new instance and therefore gets new per-transformation local flags, but all finite global reserves/payments remain finite. 
Pasted text

6. Once-transformation and special-action scopes

Confirmed.

Local use key:

FormInstanceID + SpecialID

Examples:

Broodmother Spawn
Broodmother crit-negation
Mooncursed Howl
Sky Serpent wet rider
Tempest Raptor wet rider
Shadow Lynx Blink

Broodmother Spawn and crit-negation are separate local permissions and each independently costs its Form Surge when used.

A legally committed special:

spends its local opportunity;
spends Form Surge;
receives no refund because attack misses/save succeeds/etc.

An illegal optional Brood spawn fails preflight without:

undoing valid form entry;
spending Surge;
spending Spawn's local opportunity.

Mooncursed ally Howl and enemy Howl are two modes of the same local Howl use.

Sky Serpent/Tempest wet bonuses are attack riders only. They do not create another Action or attack.

The form helper should expose source-qualified profiles; normal attack/save/movement/condition engines perform actual resolution. 
Pasted text

7. “Normal AC” while gear is melded

Do not carry the pre-shift worn armor/shield AC wholesale into the form.

Engine[0] says equipment melds and cannot be used while melded, while compatible magical numeric bonuses may persist. 
Pasted text

Define:

formNormalAC

as the character's legal AC from components that remain operative while transformed.

Exclude by default:

worn armor's AC calculation;
shield AC;
effects requiring wielding/using melded equipment;
unclassified item bonuses.

Include:

character/body/class passive AC rules that remain active;
explicitly form-compatible bonuses;
passive magical numeric item bonuses only when the item adapter certifies anatomyCompatible=true.

Then forms apply their exact formula:

Bear: max(formNormalAC,14)
Ironhorn: max(formNormalAC,17)
Frost Wyrmling: formNormalAC + 2
Broodmother: formNormalAC + 3

Do not add worn armor again after using a form AC formula.

Until the item/anatomy adapter classifies a magical item, its melded item bonus is suppressed rather than guessed.

No hand-based gear use or material-component access is created.

This AC bridge is NEW, but it is directly required by the existing meld rule. 
Pasted text

8. Natural attacks remain their own category

Confirmed.

For now use explicit identities such as:

formAttack
naturalAttack

Do not globally classify Druid natural attacks as weapon attacks.

Therefore unrelated rules requiring:

weapon attack;
melee weapon attack;
ranged weapon attack;

do not automatically trigger from Druid form attacks.

This is an unresolved interoperability gate, not a prohibition against source text that expressly names natural/form attacks.

So these remain legal:

Circle Forms → natural-form hit;
Primal Strike → form attacks;
Oracle Consumed → natural weapons/unarmed where expressly stated.

Earth Warden Slam, Frost Wyrmling Breath, Howls, Thunder Step and other alternate form actions retain their full individual:

activation;
range/area;
frequency;
cost;
save;
rider.

They are not entries in an interchangeable unlimited attack list.

A future weapon/natural-attack taxonomy needs its own exact-source review. 
Pasted text

9. Overflowing Light natural expiry

Confirmed.

Its special cleanse belongs to the specific Overflowing Light grant identity.

The cleanse does not trigger if that grant was:

rejected during arbitration;
replaced by another buffer;
depleted to 0;
explicitly removed;
lost because the target/body ceased to be a valid holder.

At the original two-round natural endpoint:

verify the active temp-HP grant is still that exact Overflowing Light grant;
verify remaining amount ≥1;
target may end exactly one actual eligible:
Frightened
Poisoned
Staggered
discard the grant.

If none is present, no cleanse occurs.

Mastery changes only the excess-conversion cap 10→20.

Independent riders such as Protective Verse's saving benefit are separate timed effect records and can survive buffer replacement. A buffer-linked natural-expiry rider cannot.

Healing/excess-conversion decisions remain otherwise unchanged. 
Pasted text

10. Blood Ritual ally amount

Yes.

Self offer:

2 × character level

Witnessing/blood-sharing ally offer:

floor(selfOffer / 2) = character level

It is based on the feat's newly calculated self offer, not:

the self character's existing active temp HP;
whatever amount wins arbitration;
the self grant's later remaining value.

Each recipient then performs its own ordinary buffer arbitration.

The drop of blood is thematic/material participation only; no HP loss is printed and none should be invented.

Target count remains open for the feat-completion batch. Do not silently apply a generic three-target maximum. 
Pasted text

11. Necrotic Affinity absorption stage

This one can be made deterministic now without inventing a new ability.

The source already supplies:

passive necrotic resistance;
Reaction when necrotic damage from spell/supernatural source is taken;
absorb half rounded down;
gain that absorbed amount as temp HP until end next turn. 
Pasted text

NEW pipeline integration:

resolve attack/save and ordinary defenses;
apply Necrotic Affinity's passive necrotic resistance normally;
call the remaining nonnegative amount D;
before any temporary HP absorbs this packet, the Reaction may trigger;
absorbed = floor(D / 2);
reduce this packet by absorbed;
existing pre-event temp HP absorbs the remaining packet normally;
resolve remaining HP/death/Wound consequences;
after that packet completes, offer a new Necrotic Affinity temp-HP grant equal to absorbed;
its explicit expiry is end of the user's next regular turn.

Thus the newly generated shield cannot retroactively protect against the packet that created it.

The absorbed portion is true prevention, not healing, transfer or redirection.

If absorbed=0, no buffer grant identity is created even if the Reaction was legally spent.

This resolves the absorption/buffer component, but does not by itself declare every other clause of the feat fully audited.

12. Spirit Walk: one character represented in two places

Confirmed, with one correction to the phrasing about attacks.

The source says the spirit cannot be targeted by attacks or effects requiring a physical target. 
Pasted text

Therefore, within this source:

the physical body remains a legal attack target normally;
the spirit position is never a legal attack target;
the spirit may be affected only by non-attack effects whose targeting does not require a physical target and whose other eligibility rules are satisfied.
Area overlap

If a single area event contains both body and spirit positions:

represent both spatial exposures;
deduplicate by character identity;
resolve the area's damage/conditions once against the one character ledger.

Do not double:

HP damage;
temporary-HP loss;
conditions;
Wounds/death consequences;
resources;
concentration checks;
clocks.

If only the spirit position lies in the area:

effects requiring a physical target do nothing to that representation;
a nonphysical effect may qualify normally.

If only the body lies in it, resolve against the body normally.

Separate independently created legal effect events can affect the character separately, but there is no internal “damage transfer” between body and spirit. They are two positions of one identity, not two creatures.

No duplicate Action, Reaction, resource pool, condition ledger or duration clock exists. 
Pasted text

These 12 reconciliations leave the packet at:

SOURCE-AUDITED / DRAFTABLE — 175+5 form/buffer interface, implementation pending.

Chef, Inspiring Leader, Soul Cage, Harmonic Bulwark and the four polymorph-family spells remain named follow-up development work rather than removed content, and Time Loop/global temporal-body conservation remains separate as requested. 
Pasted text
