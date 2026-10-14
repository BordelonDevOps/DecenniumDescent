/**
 * Protected class-identity contract.
 *
 * Every selectable base class must retain the mechanic(s) below through future
 * balance passes. Numbers can be tuned; the play loop cannot be flattened into
 * generic spellcasting without an explicit canon change.
 */
export const CLASS_CORE_MECHANICS = {
  Bard: {
    primary: "Crescendo",
    resource: "Crescendo stacks (0–5)",
    weaveMode: "hybrid",
    resonanceInterface: "Completing and consuming a 5-stack Crescendo vents 2 Dissonance; repeating the same spell does not count as rhythmic variety.",
    mechanics: [
      "Crescendo — Bard abilities played in rhythm build stacks; at 5, the next qualifying ability consumes the stack for an enhanced effect.",
    ],
  },
  Cleric: {
    primary: "Divine Favor / Conviction",
    resource: "Conviction",
    weaveMode: "full",
    resonanceInterface: "Once per turn, spending 2 or more Conviction on a Rite or Invocation vents 1 Dissonance; prayer changes cadence instead of bypassing Resonance.",
    mechanics: [
      "Divine Favor — prayer, rites, and service to the chosen power generate Conviction, which empowers divine abilities.",
    ],
  },
  "Crimson Agent": {
    primary: "Blood Mark",
    resource: "Blood Gauge (3 → 6)",
    weaveMode: "hybrid",
    resonanceInterface: "Once per turn, spend 1 Blood Gauge while casting to prevent 1 Dissonance; the Agent routes Weave strain through blood rather than gaining free casts.",
    mechanics: [
      "Blood Mark — successful attacks and hemomantic techniques build Blood Gauge, spent to place/detonate Blood Marks or fuel Veinweaves.",
    ],
  },
  Dragoon: {
    primary: "Momentum Gauge",
    resource: "Momentum (5 → 7)",
    weaveMode: "minor",
    resonanceInterface: "If the Dragoon moved at least 20 feet before a Weave cast, reduce that cast's Dissonance gain by 1 (minimum 0); Momentum carries the note through motion.",
    mechanics: [
      "Momentum Gauge — movement and successful attacks build Momentum for leaps, burst attacks, and defensive maneuvers.",
    ],
  },
  Druid: {
    primary: "Shapeshifting",
    resource: "Shapeshifting uses + Resonance Points",
    weaveMode: "full",
    resonanceInterface: "Entering Shapeshift clears the Refrain counter because the Druid changes the body sounding the Weave; beast-form casting remains limited by class features.",
    mechanics: [
      "Shapeshifting — assume specialized beast forms with role-specific movement, defenses, and attacks; Circles unlock Hero and Arch forms.",
    ],
  },
  Mage: {
    primary: "Elemental Focus / Nuke Chains",
    resource: "Resonance Points + Resonance Surge",
    weaveMode: "full",
    resonanceInterface: "A Nuke Chain requires different named spells of the chosen element; completing a three-spell chain vents 2 Dissonance. Repeating one nuke builds Refrain normally.",
    mechanics: [
      "Elemental Focus — specialize in Fire, Cold, or Lightning.",
      "Nuke Chains — three consecutive spells of the chosen element enable an enhanced finisher.",
      "Resonance Surge — trade casting sustainability for burst-damage rotations.",
    ],
  },
  Monk: {
    primary: "Ki Flow",
    resource: "Ki Chain (0–5)",
    weaveMode: "minor",
    resonanceInterface: "Spend 1 Ki when using a minor Weave technique to prevent 1 Dissonance from that technique; Ki and Resonance remain separate pools.",
    mechanics: [
      "Ki Flow — movement/attack chains, critical strikes, and defensive reactions build Ki for advanced techniques.",
      "Stance System — switch combat stances once per round to change tactical function.",
      "Unarmored Flow — mobility, initiative, and stance benefits reward fighting without armor.",
    ],
  },
  Mirrorsage: {
    primary: "Echo Slots / Mirrorbind",
    resource: "Echo Slots (3 → 5; ceiling rules may expand storage)",
    weaveMode: "hybrid",
    resonanceInterface: "The first replay of a newly Mirrorbound Echo ignores Refrain Dissonance; repeating the same stored Echo builds Refrain normally.",
    mechanics: [
      "Echo Slots — captured monster abilities occupy finite Echo Slots until released.",
      "Mirrorbind — copy a witnessed eligible ability from the current battle into an empty Echo Slot.",
      "Charm Bind — temporarily turn a low-intellect creature into a Reflective Companion.",
    ],
  },
  Oracle: {
    primary: "Mystery, Curse & Revelations",
    resource: "Revelation Charges (3 → 7)",
    weaveMode: "revelation",
    resonanceInterface: "Oracle does not track Weave Dissonance. Revelation Charges, the permanent Curse, and Prophecy Triggers are the Oracle's anti-spam architecture.",
    mechanics: [
      "Mystery — determines the Revelation tree, passive identity, and Prophecy Trigger.",
      "Curse — a permanent affliction that also unlocks escalating boons.",
      "Revelation Charges — Oracles do not use Resonance Points; Revelations consume and recover RC through Mystery-specific triggers.",
    ],
  },
  Ranger: {
    primary: "Track Target",
    resource: "Tracked quarry + attack chain",
    weaveMode: "half",
    resonanceInterface: "A successful weapon hit between spell casts clears Refrain and reduces the next spell's Dissonance gain by 1 (minimum 0), rewarding the Ranger's martial/primal cadence.",
    mechanics: [
      "Track Target — mark one quarry for increased pressure and unlock quarry-dependent techniques.",
      "Weapon Synergy — alternating melee and ranged attacks grants follow-up bonuses.",
      "Elemental Imbue — Fire, Cold, or Poison modifies weapon effects.",
      "Druidic Arrow Combo — successful weapon chains unlock an enhanced primal arrow technique.",
    ],
  },
  Shaman: {
    primary: "Totem System",
    resource: "Totems + elemental attunement",
    weaveMode: "hybrid",
    resonanceInterface: "Once per round, the first spell cast inside the Shaman's own active Totem aura generates 1 less Dissonance (minimum 0).",
    mechanics: [
      "Totem System — persistent battlefield structures project allied boons or hostile penalties.",
      "Elemental Affinity — Fire, Ice, Air, or Earth attunement modifies Shaman techniques.",
      "Flask Bomb System — Theurgist/Soothsayer paths convert elemental power into thrown tactical effects.",
    ],
  },
  Soldier: {
    primary: "Palisade / Overwatch",
    resource: "Positioning, reactions, and deployables",
    weaveMode: "none",
    resonanceInterface: "No general Weave casting; class power is entirely positional and martial.",
    mechanics: [
      "Palisade System — deploy barriers that create cover, chokepoints, and controlled firing lanes.",
      "Overwatch System — monitor a declared zone and react when enemies cross or threaten it.",
      "Intercept & Brace — defensive positioning protects allies and stabilizes the line.",
    ],
  },
  Thief: {
    primary: "Sneak Attack / Poison",
    resource: "Positioning + prepared toxins",
    weaveMode: "minor",
    resonanceInterface: "Once per round, a Weave trick cast while hidden ignores its first point of Refrain Dissonance; stealth changes delivery, not RP cost.",
    mechanics: [
      "Sneak Attack — exploit stealth, flanking, Bleed, Poison, or Disable states for bonus damage.",
      "Poison System — apply tactical toxins as a bonus action, with stronger critical effects.",
      "Utility Skills — lockpicking, trap disarming, stealth, and infiltration remain core combat-adjacent power.",
    ],
  },
  Tinker: {
    primary: "Anacite Drone / Deployables",
    resource: "Drone + bombs + devices",
    weaveMode: "minor",
    resonanceInterface: "Once per short rest, route up to 2 Dissonance into an active device; that device becomes disabled until repaired or the next short rest.",
    mechanics: [
      "Mechanical Pet — command and customize an Anacite Drone companion.",
      "Explosive Toolkit — prepare elemental and tactical bombs.",
      "Deployable Devices — turrets, traps, and gadgets reshape battlefield space.",
    ],
  },
  Warrior: {
    primary: "Mutation Slots",
    resource: "Mutation Slots + Serum Engine + Brutality Threshold",
    weaveMode: "none",
    resonanceInterface: "No general Weave casting; mutations and serums are the Warrior's power engine.",
    mechanics: [
      "Mutation Slots — equip and swap adaptive mutations during rests.",
      "Serum Engine — specialized serums trigger or fuel mutations.",
      "Brutality Threshold — dealing and taking damage pushes the Warrior into enhanced mutation states.",
    ],
  },
  Wizard: {
    primary: "Spell Matrix System",
    resource: "Prepared Spell Matrix + Resonance Points",
    weaveMode: "full",
    resonanceInterface: "The first cast of each different prepared Spell Matrix in an encounter generates 0 base Dissonance; repeating a matrix builds Refrain normally.",
    mechanics: [
      "Spell Matrix System — prepare and study modifiable arcane matrices, trading spontaneity for the broadest controlled spell access.",
    ],
  },
  Paladin: {
    primary: "The Oath",
    resource: "Oath + Smite + Aura + Lay on Hands",
    weaveMode: "half",
    resonanceInterface: "Smite, Aura, and Lay on Hands are Oath mechanics and do not generate Weave Dissonance. After a successful melee hit, the next Oath spell before the end of the next turn generates 1 less Dissonance.",
    mechanics: [
      "The Oath — chosen at Level 3; defines Smite type, Aura, signature power, Revelation spell list, and Conduct Clause.",
      "Smite System — Oath-shaped empowered melee strikes.",
      "Aura System — scaling passive zones tied to the Oath.",
      "Lay on Hands — healing/cleansing pool equal to 5 × Paladin level.",
    ],
  },
};


/**
 * Hero paths that deliberately violate the normal Dissonance safety cutoff.
 * They remain tied to their parent class mechanic; this is not a generic caster option.
 */
export const DARK_RESONANCE_PATHS = {
  Lich: {
    baseClass: "Mage",
    mechanic: "Soul Furnace",
    principle: "Force the Weave through accumulated Dissonance, accepting direct magical trauma rather than losing access to ranked casting.",
  },
  Necromancer: {
    baseClass: "Wizard",
    mechanic: "Grave Conductor",
    principle: "Use death, corpses, and bound undead as resonators while forcing spells through Dissonance that would stop an ordinary caster.",
  },
};

export function isDarkResonancePath(heroPath) {
  return Boolean(heroPath && Object.prototype.hasOwnProperty.call(DARK_RESONANCE_PATHS, heroPath));
}

export function getClassCoreMechanic(className) {
  return CLASS_CORE_MECHANICS[className] || null;
}

export default CLASS_CORE_MECHANICS;
