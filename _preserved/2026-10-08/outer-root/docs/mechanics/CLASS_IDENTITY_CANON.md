# Class Identity Canon — Protected Mechanical Loops

**Status:** Canon — 2026-07-31

Resonance is a law of Aethel, not a replacement for class design. Numbers can be tuned during balance passes, but the following play loops must remain recognizable unless the owner explicitly changes canon.

| Class | Protected core mechanic | Relationship to Resonance / anti-spam |
|---|---|---|
| Bard | **Crescendo** | Varied abilities build rhythm; completing/consuming Crescendo can vent strain. Repeating one spell is not rhythm. |
| Cleric | **Conviction / Divine Favor** | Prayer, Rites, and Invocations create a second cadence that can vent limited Dissonance. |
| Crimson Agent | **Blood Gauge / Blood Marks / Veinweaves** | Blood Gauge can route limited strain through the body; it never grants free spell spam. |
| Dragoon | **Momentum** | Movement before a minor Weave technique can stabilize the note; aerial/martial play remains primary. |
| Druid | **Shapeshifting** | Changing form changes the body sounding the Weave and breaks Refrain; form limits still apply. |
| Mage | **Elemental Focus / Nuke Chains / Resonance Surge** | Rotating elemental spells builds chains and vents strain; repeating one nuke builds Refrain normally. |
| Monk | **Ki Flow / Stances** | Ki can stabilize minor Weave techniques but remains a separate martial resource. |
| Mirrorsage | **Echo Slots / Mirrorbind** | Newly captured/replayed Echoes reward adaptation; repeatedly replaying the same Echo builds Refrain. |
| Oracle | **Mystery / Curse / Revelation Charges** | Oracle does not use RP/Dissonance. RC + Prophecy Triggers are its anti-spam architecture. |
| Ranger | **Track Target / Weapon Synergy / Imbues** | Weapon hits between spells reward alternating martial/primal cadence. |
| Shaman | **Totems / Elemental Attunement** | Totems act as resonators and can stabilize limited casting inside their aura. |
| Soldier | **Palisade / Overwatch / Intercept** | No general Weave casting; power comes from positioning and reactions. |
| Thief | **Sneak Attack / Poison / Infiltration** | Hidden delivery can stabilize limited tricks, but stealth does not erase RP cost. |
| Tinker | **Anacite Drone / Bombs / Deployables** | Devices can absorb limited Dissonance at the cost of becoming disabled. |
| Warrior | **Mutations / Serum Engine / Brutality** | No general Weave casting; mutation pressure is the power engine. |
| Wizard | **Spell Matrix** | Rotating prepared matrices is stable; repeating the same matrix builds Refrain. |
| Paladin | **Oath / Smite / Aura / Lay on Hands** | Oath powers remain distinct from Weave spells; melee cadence stabilizes limited Oath casting. |

## Dark-path exception

**Lich** remains a Mage and therefore keeps Elemental Focus, Nuke Chains, and Resonance Surge. **Necromancer** remains a Wizard and therefore keeps Spell Matrix preparation/rotation.

Their exception is **Traumatic Casting**, not the loss of the parent class mechanic. They may force ranked spells and Overcast through Dissonance states that stop ordinary casters, but take direct metaphysical trauma after the spell resolves. Lich may use its Soul Reservoir to absorb one backlash per rest; Necromancer may sacrifice a controlled undead or fresh corpse through Grave Conductor as written.

## Balance rule

A balance pass may change costs, stack caps, cooldowns, Dissonance reduction, damage, healing, or durations. It must not silently replace a protected mechanic with generic spellcasting or make another class's resource an interchangeable reskin.

**Software contract:** `src/data/class-core-mechanics.js`.
