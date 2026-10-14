/** Decennium Descent character backgrounds (Aethel canon). */
export const BACKGROUNDS = [
  {
    name: "Aethel City Guard Veteran",
    description:
      "You served in the City Guard of Aethel, dealing with everything from back-alley brawls to organized crime.",
    skillProficiencies: ["Athletics", "Insight"],
    toolProficiencies: ["Gaming Set", "Vehicles (Land)"],
    feature: "Watchman's Eye",
    featureDescription:
      "You gain advantage on Wisdom (Perception) checks to spot trouble within city limits and on checks to navigate Aethel.",
    alignmentTendency: "Often Lawful",
    startingReputation: "Neutral with Aethel authorities, Liked among common folk",
  },
  {
    name: "Arcane Academy Dropout",
    description:
      "You studied at a prestigious arcane academy but left before graduation due to expulsion, restrictive policies, or disturbing discoveries.",
    skillProficiencies: ["Arcana", "History"],
    toolProficiencies: [],
    languages: ["Two of your choice"],
    feature: "Theoretical Knowledge",
    featureDescription:
      "You have advantage on Intelligence (Arcana) checks to identify magical effects, traditions, or items.",
    alignmentTendency: "Often Chaotic",
    startingReputation: "Disliked by formal arcane institutions, Neutral with independent mages",
  },
  {
    name: "Battlefield Medic",
    description:
      "You served as a healer during conflicts, tending to the wounded on blood-soaked battlefields.",
    skillProficiencies: ["Medicine", "Insight"],
    toolProficiencies: ["Healer's kit", "Herbalism kit"],
    feature: "Trauma Response",
    featureDescription:
      "When you use a healer's kit to stabilize a dying creature, they regain 1 hit point immediately.",
    alignmentTendency: "Often Good",
    startingReputation: "Liked by veterans, Neutral with opposing forces",
  },
  {
    name: "Corruption Survivor",
    description:
      "You were exposed to a corrupting force and survived, though not without scars both physical and psychological.",
    skillProficiencies: ["Religion", "Insight"],
    toolProficiencies: ["Herbalism kit"],
    languages: ["One exotic language (Abyssal, Infernal, or Deep Speech)"],
    feature: "Corruption Sense",
    featureDescription:
      "You can sense strong sources of corruption within 60 feet and have advantage on saves against diseases and corruption.",
    alignmentTendency: "Often Good",
    startingReputation: "Liked by cleansing orders, Disliked by those who study corruption",
  },
  {
    name: "Cult Escapee",
    description:
      "You were once part of a secretive cult but broke free. You live with memories of what you witnessed and fear of reclamation.",
    skillProficiencies: ["Religion", "Deception"],
    toolProficiencies: ["Disguise Kit"],
    languages: ["One exotic language (Abyssal, Infernal, or Deep Speech)"],
    feature: "Dark Insights",
    featureDescription:
      "You have advantage on Intelligence (Religion) checks related to dark cults, eldritch entities, or occult practices.",
    alignmentTendency: "Often Good or Neutral",
    startingReputation: "Hated by former cult, Liked by groups that oppose cults",
  },
  {
    name: "Dimensional Refugee",
    description:
      "You are not originally from Aethel but from another plane or dimension that was destroyed or became uninhabitable.",
    skillProficiencies: ["Survival", "History"],
    toolProficiencies: [],
    languages: ["Two of your choice"],
    feature: "Otherworldly Perspective",
    featureDescription:
      "You have advantage on Intelligence checks related to identifying extraplanar phenomena and can suggest unconventional solutions.",
    alignmentTendency: "Any",
    startingReputation: "Neutral with most natives, Liked by multiverse scholars",
  },
  {
    name: "Disgraced Noble Scion",
    description:
      "You hail from a noble family but scandal, betrayal, or your own actions led to your disgrace.",
    skillProficiencies: ["History", "Persuasion"],
    toolProficiencies: ["Gaming Set"],
    languages: ["One of your choice"],
    feature: "Lingering Influence",
    featureDescription:
      "Once per week, you can leverage past connections to gain an audience with minor officials or secure temporary lodging.",
    alignmentTendency: "Varies greatly",
    startingReputation: "Disliked by established nobility, Neutral with underground groups",
  },
  {
    name: "Expedition Cartographer",
    description:
      "You've made your living mapping the unknown territories of Aethel, accompanying merchants and adventuring parties.",
    skillProficiencies: ["Survival", "Investigation"],
    toolProficiencies: ["Cartographer's Tools", "Navigator's Tools"],
    feature: "Trailblazer",
    featureDescription:
      "You have excellent memory for maps and geography. You can identify safe routes, hazards, and prime camping locations.",
    alignmentTendency: "Often Neutral",
    startingReputation: "Liked by merchant guilds and explorers' societies, Neutral with indigenous tribes",
  },
  {
    name: "Frontier Settler",
    description:
      "You helped establish or maintain frontier settlements on the edges of civilization, wilderness, or unexplored territories.",
    skillProficiencies: ["Survival", "Animal Handling"],
    toolProficiencies: ["One type of artisan's tools", "Vehicles (land)"],
    feature: "Frontier Adaptability",
    featureDescription:
      "You excel at making do with limited resources, improvising tools, and creating shelter in wilderness environments.",
    alignmentTendency: "Often Neutral",
    startingReputation: "Liked by frontier communities and traders, Neutral with urban elites",
  },
  {
    name: "Guild Artisan Dropout",
    description:
      "You left your guild before completing your training, taking your skills but losing the protection of organized craftsmanship.",
    skillProficiencies: ["Investigation", "Persuasion"],
    toolProficiencies: ["One type of artisan's tools"],
    feature: "Trade Secret",
    featureDescription:
      "You retain knowledge of your former craft and can identify quality craftsmanship and navigate guild bureaucracy.",
    alignmentTendency: "Often Chaotic",
    startingReputation: "Disliked by former guild, Neutral with rival guilds",
  },
  {
    name: "Marked Fugitive",
    description:
      "You carry something you were never meant to have: a relic, secret, stolen spell, or divine fragment, and are hunted for it.",
    skillProficiencies: ["Stealth", "Arcana"],
    toolProficiencies: ["Thieves' Tools"],
    languages: ["One obscure or factional language"],
    feature: "Echo of the Stolen",
    featureDescription:
      "Once per long rest, you may replicate a 1st-level spell you've seen cast within the last hour.",
    alignmentTendency: "Often Chaotic",
    startingReputation: "Liked by underground resistance, Hated by the faction you stole from",
  },
  {
    name: "Planar Merchant",
    description:
      "You've made your living trading goods between planes or dealing in items with extraplanar origins.",
    skillProficiencies: ["Persuasion", "Arcana"],
    toolProficiencies: ["One type of artisan's tools or gaming set"],
    languages: ["Two of your choice"],
    feature: "Planar Connections",
    featureDescription:
      "Once per week, you can attempt to acquire rare items with planar origins or gain information about planar phenomena.",
    alignmentTendency: "Often Neutral",
    startingReputation: "Liked by planar trading guilds, Disliked by planar customs authorities",
  },
  {
    name: "Relic Hunter",
    description:
      "You make your living discovering, identifying, and sometimes selling ancient artifacts and relics.",
    skillProficiencies: ["History", "Investigation"],
    toolProficiencies: ["Cartographer's tools or Thieves' tools"],
    languages: ["One of your choice"],
    feature: "Relic Lore",
    featureDescription:
      "You can accurately identify the culture, age, and significance of ancient artifacts with Intelligence (History) checks.",
    alignmentTendency: "Any",
    startingReputation: "Liked by museums and collectors, Disliked by indigenous peoples",
  },
  {
    name: "Rift Scarred Survivor",
    description:
      "You were present during a Rift event and survived, but the experience left indelible marks.",
    skillProficiencies: ["Survival", "Arcana"],
    toolProficiencies: [],
    languages: ["One Exotic language (Abyssal, Celestial, Primordial, or Deep Speech)"],
    feature: "Planar Sense",
    featureDescription:
      "You have advantage on saving throws against being frightened or charmed by aberrations, celestials, elementals, fey, or fiends.",
    alignmentTendency: "Often Chaotic",
    startingReputation: "Neutral with planar scholars, Disliked by mundane authorities",
  },
  {
    name: "Seeker of the Lost Pantheon",
    description:
      "You are driven by a quest to uncover truths behind Aethel's Lost Pantheon – deities worshiped in ages past but now forgotten.",
    skillProficiencies: ["Religion", "History"],
    toolProficiencies: ["Calligrapher's supplies or Cartographer's tools"],
    languages: ["Two of your choice (often ancient or obscure)"],
    feature: "Whispers of the Past",
    featureDescription:
      "You have advantage on Intelligence checks to decipher ancient ruins, symbols, or texts related to Aethel's pre-current faith history.",
    alignmentTendency: "Often Neutral or Chaotic",
    startingReputation: "Neutral with mainstream religious orders, Liked with fringe historians",
  },
  {
    name: "Wildling Herbalist",
    description:
      "You lived on the fringes of civilization, learning the secrets of plants, natural remedies, and wilderness survival.",
    skillProficiencies: ["Nature", "Medicine"],
    toolProficiencies: ["Herbalism Kit"],
    languages: ["Sylvan or Primordial"],
    feature: "Natural Remedy",
    featureDescription:
      "Identify plants with ease; during a long rest, gather components to create one Potion of Healing or antitoxin without gold.",
    alignmentTendency: "Often Neutral",
    startingReputation: "Liked by Druidic circles and wildling communities, Disliked by alchemists guilds",
  },
  {
    name: "Prophecy Bearer",
    description:
      "You are the subject of a prophecy that has shaped your life — ancient or recent, embraced or resisted.",
    skillProficiencies: ["Religion", "History"],
    toolProficiencies: [],
    languages: ["Two of your choice"],
    feature: "Fated Path",
    featureDescription:
      "Once per long rest, gain advantage on one check, save, or attack directly related to fulfilling your prophecy.",
    alignmentTendency: "Any",
    startingReputation: "Liked by believers in your destiny, Disliked by those who fear what you're foretold to do",
  },
  {
    name: "Underworld Escapee",
    description:
      "You broke free from Aethel's criminal underworld, though your past continues to shadow you.",
    skillProficiencies: ["Stealth", "Deception"],
    toolProficiencies: ["Thieves' tools", "One gaming set"],
    feature: "Criminal Network",
    featureDescription:
      "Identify criminal operations, gang symbols, and black markets in settlements; know how the underworld operates.",
    alignmentTendency: "Often Chaotic",
    startingReputation: "Disliked by law enforcement, Hated by former associates, Neutral with reformed criminals",
  },
  {
    name: "Elemental Touched",
    description:
      "You have been marked by elemental power through rift exposure, ritual, ancestry, or convergence at birth.",
    skillProficiencies: ["Arcana", "Nature"],
    toolProficiencies: [],
    languages: ["Primordial (Auran, Aquan, Ignan, or Terran dialect)"],
    feature: "Elemental Affinity",
    featureDescription:
      "Communicate with elemental creatures of your affiliated type; resistance to damage matching your element.",
    alignmentTendency: "Varies by element",
    startingReputation: "Liked by elemental cultists of your element, Disliked by opposing elemental factions",
  },
  {
    name: "Celestial Emissary",
    description:
      "You serve as an agent of celestial powers — chosen, ancestral, or marked by a near-death touch from higher realms.",
    skillProficiencies: ["Religion", "Persuasion"],
    toolProficiencies: [],
    languages: ["Celestial"],
    feature: "Divine Insight",
    featureDescription:
      "Once per long rest, enter a brief trance for cryptic but truthful guidance on a specific question or situation.",
    alignmentTendency: "Often Good",
    startingReputation: "Liked by good-aligned temples, Hated by fiendish cults",
  },
];

export function getBackgroundByName(name) {
  return BACKGROUNDS.find((b) => b.name === name) || null;
}
