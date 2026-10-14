# GPT final form profile decisions

ChatGPT said:

These inputs can be settled cleanly without changing any of the 175 source-role classifications.

1. Exact lifetimes for Rally Point, Bastion Descent, Linked Ward, Final Stand
Soldier Rally Point

Confirm your proposal.

The card's general effect duration is until the start of the Soldier's next turn, but it separately says:

temporary HP ... is lost at encounter end.

That is a specific shield-lifetime clause, so use:

temp HP: encounter end
+1 next-save rider: until Soldier's next regular start, consumed earlier if the qualifying save occurs.

The general card duration does not shorten the expressly longer shield duration.

Dragoon Bastion Descent

Confirm your proposal, but mark this as a NEW grammatical integration.

The source says Instant; protection until start next turn, then packages:

temp HP;
cleanse;
resistance to the next damage instance before next turn.

Treat the temp HP as part of that defined “protection” package:

cleanse: instantaneous;
temp HP: until Dragoon's next regular start;
resistance: until used or Dragoon's next regular start.

Any unused Bastion temp HP disappears at that marker rather than inheriting V6 long-rest duration.

Linked Ward

Confirm:

The after-zero temp HP has no printed lifetime, so it receives the V6 default:

until depleted/replaced or recipient's next completed long rest.

The Linked Ward concentration ending does not erase an already granted after-zero buffer.

Final Stand

Confirm your proposed bounded reading, labeled NEW grammatical integration.

When redirected damage reduces the Paladin to 0, the ally receives one paired protection event:

temp HP = Paladin level;
resistance to all damage;
both end at the end of that ally's next regular turn.

This is preferable to splitting the sentence so the resistance gets the printed endpoint while the temp HP silently survives to long rest. It keeps the triggered package finite and source-coherent.

The underlying Final Stand redirection itself still has its own earlier endpoint at the start of the Paladin's next regular turn. 
Pasted text
 
Pasted text

2. Mooncursed ally Howl buffer lifetime

Use the V6 default, not the Mooncursed form instance.

This is a NEW bridge clarification, because the card supplies:

form duration: “While in Mooncursed”;
Howl as an Action;
an instantaneous ally temp-HP grant;
no language saying the allies' shields remain only while the Druid stays Mooncursed.

Therefore:

Mooncursed ally Howl creates independent recipient BufferGrants using the shared 2d8 roll and Buffer Reserve. Once granted, they use ordinary V6 lifetime unless replaced/depleted/long-rest-expired.

Forced reversion does not remove those ally shields.

This differs from Bear/Earth Warden because those buffers are direct properties of the Druid's current form and explicitly disappear when that form ends. The old-form-ending rule therefore removes:

Bear's own buffer;
Earth Warden's own buffer;

but not an independently granted Mooncursed ally buffer.

The source's While in Mooncursed describes the availability of the form/Howl ability, not a dependency on every already-created recipient shield. 
Pasted text

3. Elemental profiles, Earth Warden claw, reach, subtype changes
Elemental Shapeshifting damage mapping

Accept the proposed mapping as NEW bounded profile completion:

Elemental subtype	Natural attack damage
Air	2d8 + WIS lightning
Earth	2d8 + WIS bludgeoning
Fire	2d8 + WIS fire
Water	2d8 + WIS cold

This follows the existing named elemental identities and their printed resistances/movement while avoiding imported elemental stat blocks.

Subtype is selected at form entry and recorded in the form instance.

Earth Warden ordinary claw

Accept:

NEW: 1d8 + WIS slashing, melee reach 5 ft.

No added rider.

Default ordinary form-attack reach

Confirm:

NEW bounded default: an ordinary form natural attack whose source gives no different reach uses melee reach 5 ft.

This is only a delivery default for an already-existing form attack. It does not invent a new attack.

Elemental subtype identity

Confirm each elemental subtype is a distinct form profile:

Air Elemental
Earth Elemental
Fire Elemental
Water Elemental

Changing one subtype to another is a genuine form change:

Bonus Action;
Shapeshift use below20;
one Elemental Shapeshifting use;
new FormInstance;
Refrain clear;
old form-linked effects end.

No passive subtype switching exists.

Same-profile Elemental renewal

Confirm.

Natural 10-minute renewal of the same elemental subtype:

preserves same FormInstance;
pays normal Shapeshift renewal use below20;
does not consume another one of Elemental Shapeshifting's 2/LR uses;
does not retrigger entry benefits.

The 2/LR payment occurs when entering an Elemental profile, not when extending the same existing profile.

Master of Vermin

Likewise, bat versus ground-swarm choice is part of the form profile.

Switching between bat and non-bat configuration is a genuine new form entry, not a free toggle:

BA;
Shapeshift use below20;
new instance.

Same exact profile renewal does not reselect it.

Pasted text
 
Pasted text
 
Pasted text

4. Recharge/per-rest scopes across transformations

Confirm all of these as source-qualified character clocks, not FormInstance clocks.

Earth Warden Slam

Recharge 2 belongs to the Druid/source ability.

It:

persists through reversion;
persists through changing forms;
is not reset by re-entering Earth Warden;
ticks only on canonical regular-start recharge markers;
outside initiative uses the protected real-time six-second equivalent where applicable.

Shifting cannot manipulate its counter.

Frost Wyrmling Breath

1/short rest remains spent across all shifts and all Frost Wyrmling instances until the actual completed short/long rest resets it.

Blazewood Conflagration

1/long rest persists across reversion/reentry.

Elemental Shapeshifting

2/long rest is likewise owner/source scoped, not per instance.

Broodmother Spawn

Confirm the optional entry-only window.

On entering Broodmother:

evaluate the optional Spawn opportunity;
if legal and chosen, spend its Form Surge and local use;
if illegal or declined, spend neither.

NEW entry-window rule: once that entry transaction closes, there is no later Spawn window during that FormInstance.

So:

declined at entry → cannot spawn later;
illegal at entry → cannot wait until later and spawn;
must enter a new Broodmother FormInstance to receive another entry opportunity.

This prevents an unprinted at-will spawn Action from appearing.

Broodmother's crit-negation remains a different FormInstance + SpecialID permission and remains available independently if its own Surge is later payable. 
Pasted text
 
Pasted text
 
Pasted text

5. Necrotic Affinity packet identity and post-packet grant

Confirm the proposed transaction.

For one canonical incoming damage event ID:

establish that the source is qualifying necrotic spell/supernatural damage;
resolve save/attack and all defenses preceding resistance;
apply Necrotic Affinity's passive necrotic resistance;
define D as the resulting nonnegative damage before temporary HP;
if Reaction is legally used:
spend Reaction immediately;
absorbed = floor(D / 2);
reduce this same packet by absorbed;
existing pre-event temp HP absorbs the remaining packet;
resolve real HP, Instant Death, Wounds, death prevention/replacement and 0-HP state normally;
after the entire packet is resolved, if the holder remains a living legal recipient, offer a Necrotic Affinity buffer equal to absorbed;
grant expires at the end of the holder's next regular turn.

Important consequences:

D=1 may legally consume the Reaction;
floor(1/2)=0;
therefore no BufferGrant is created.

If the character dies from the event:

no post-packet buffer exists;
no corpse receives temporary HP.

If the character survives at 0 HP and is still living:

it may receive the post-packet temp HP;
this does not stabilize;
does not restore consciousness;
does not reset death counters.

The reaction's prevention may itself change whether the packet would have killed/dropped the character, because it occurs before temp HP/real HP resolution.

Event identity

A canonical packet ID may invoke this absorption transaction at most once.

Reject:

replay of the same damage event;
separate “resistance” and “absorption” submissions for the same packet;
recursive reactivation from damage consequences of that same event.

The new temp HP is a post-event consequence and cannot absorb the event that generated it.

And yes: any existing legal same-packet death prevention/replacement finishes before Druid forced-reversion state is evaluated. A character kept above 0 by a valid replacement never entered the forced-0 reversion condition. 
Pasted text
 
Pasted text

These choices leave the full 175+5 package SOURCE-AUDITED / DRAFTABLE — ready for implementation submission, with the previously stated equipment, natural-weapon taxonomy, incomplete feat/spell, Time Loop, balance and full-runtime dependencies still open.
