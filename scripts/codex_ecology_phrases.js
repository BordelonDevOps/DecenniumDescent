// Combinatorial phrase banks for Creature Lexicon ecology blurbs.
// Goal: avoid the old bestiary's word-for-word repeated paragraph by giving
// each Type several independent sentence slots that recombine differently
// per entry (seeded by name+zone so results are stable across regenerations).
"use strict";

function hashSeed(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function pick(seed, arr, salt) {
  const h = hashSeed(String(seed) + "::" + salt);
  return arr[h % arr.length];
}

// Slot banks keyed by Type. Each slot is an array of sentence fragments.
// opener: establishes what the creature is / where it fits Aethel cosmology
// behavior: how it acts, hunts, or organizes
// pressure: what it costs an Expedition, or what Directors should use it for
const BANKS = {
  Aberration: {
    opener: [
      "Something in {zone} never finished agreeing with the rest of Aethel's geometry, and {name} is the proof.",
      "{name} reads as a rumor the Spiral told itself twice, once correctly.",
      "Where the Weave frays thin over {zone}, wrongness like {name} condenses out of the gap.",
      "No cosmology fully claims {name}; it simply persists where {zone} stops making sense.",
    ],
    behavior: [
      "It does not hunt so much as arrive, and things nearby stop behaving like themselves.",
      "Directors should play its intelligence as patient and incurious about mercy.",
      "It communicates in impressions rather than words, and most minds regret understanding it.",
      "Expedition Recon reports rarely agree on its shape twice in the same debrief.",
    ],
    pressure: [
      "Treat it as a Research hook first and a fight second — knowledge here is worth more than the kill.",
      "Its presence is the omen; a Director can telegraph it for a full session before anyone rolls initiative.",
      "Support teams should expect sanity and morale costs that outlast the encounter.",
      "Recovering intact remains is its own small Expedition inside the Expedition.",
    ],
  },
  Beast: {
    opener: [
      "{name} is {zone}'s answer to hunger — mundane in ancestry, dangerous only in number or terrain.",
      "Nothing about {name} is dungeon-born; it simply never left {zone} once the floors closed over it.",
      "{name} predates the Decennium's architecture and will outlast this Cycle's version of {zone}.",
      "Expeditions meet {name} as a travel problem long before they meet it as a combat problem.",
    ],
    behavior: [
      "It moves in the pattern of its kind above-ground: territorial, opportunistic, rarely suicidal.",
      "Packs or herds of it read {zone}'s hazards better than most parties do on a first pass.",
      "It reacts to noise, light, and blood the way any animal would — which makes it predictable and therefore useful.",
      "Left alone, it is scenery; provoked, it is attrition.",
    ],
    pressure: [
      "Use it to tax rations, light, and rope rather than headline a set-piece.",
      "A Director can let this be the fight that teaches new Combat teams to conserve resources.",
      "Its parts feed Resource Team drop tables more than its death feeds a story.",
      "It is the fight most parties should be able to avoid, if they think to.",
    ],
  },
  Celestial: {
    opener: [
      "{name} claims descent from higher harmony, though {zone} has bent that claim into something stranger.",
      "Whatever sent {name} into {zone} did not account for what the Pact would ask of it here.",
      "{name} carries the manner of a messenger who has forgotten, or refuses to say, who sent it.",
      "Radiance clings to {name} the way guilt clings to a debt not yet called in.",
    ],
    behavior: [
      "It speaks in certainties and expects them honored; Directors should make that costly, not comforting.",
      "Its aid is never free — Pact politics stain even the most radiant motive down here.",
      "It judges before it helps, and its judgment is not aligned with player convenience.",
      "It remembers oaths precisely and holds Expeditions to the letter, not the spirit.",
    ],
    pressure: [
      "Play it as a conditional ally at best — a Director's tool for making mercy expensive.",
      "Its presence should complicate a floor's politics, not simplify a fight.",
      "If it falls, something above the Decennium notices; decide in advance what that costs later.",
      "Use it sparingly — Celestial pressure works best as leverage, not loot.",
    ],
  },
  Construct: {
    opener: [
      "{name} was built, not born, and {zone} still remembers who built it even if the party does not.",
      "Somewhere upstream of {zone}, someone had a use for {name}; the use outlived the reason.",
      "{name} is older engineering wearing a newer purpose, patched together by whoever last needed it to move.",
      "Nothing about {name} improvises — it executes, which is its own kind of danger.",
    ],
    behavior: [
      "It follows its last standing order literally, including orders its makers would now regret.",
      "Damage does not deter it the way pain deters living things; only disabling function stops it.",
      "It recognizes authority by token, seal, or command phrase — not by argument.",
      "Left running long enough, it becomes a fixture of {zone} that other creatures learn to route around.",
    ],
    pressure: [
      "Use it as evidence: what it guards, obeys, or was built for tells an Expedition more than its stat line.",
      "A captured command phrase or control core is often better loot than its salvage value.",
      "It is a puzzle wearing a combat encounter's clothes — let Research teams shine here.",
      "Treat destruction as a last resort; disabling and questioning it (however it 'answers') is more interesting.",
    ],
  },
  Dragon: {
    opener: [
      "{name} treats {zone} as a claim, not a home, and enforces the distinction personally.",
      "Ambition made scales on {name}; the hoard is a symptom, not the point.",
      "{zone} is quieter than it should be wherever {name} has decided to be understood as law.",
      "{name} does not compete for {zone} — it simply outlasts anyone who tries to.",
    ],
    behavior: [
      "It negotiates when negotiation is cheaper than violence, and remembers every party that tried to lie to it.",
      "Its territory is marked in ways only apparent after an Expedition has already crossed the line.",
      "It delegates lesser threats to guard the approach and saves itself for parties worth its time.",
      "Pride is a lever here — flattery, challenge, and bargains land where steel does not.",
    ],
    pressure: [
      "Its hoard should seed surface conflicts for sessions after the fight is over — factions will want a share.",
      "Play the approach as a full session of omens before the confrontation; dragons are earned, not ambushed.",
      "A Director should decide in advance what the hoard buys and who else wants it.",
      "Treat it as a campaign event, not a floor's random encounter.",
    ],
  },
  Elemental: {
    opener: [
      "{name} is {zone}'s weather made vindictive, a concentrated state of matter that decided to have opinions.",
      "Where the Spiral folds hardest over {zone}, raw element condenses into something like {name}.",
      "{name} did not evolve; it precipitated, and it remembers nothing before that moment.",
      "The terrain of {zone} is not a backdrop to {name} — it is {name}'s body, extended.",
    ],
    behavior: [
      "It reads intent the way fire reads fuel: indifferently, and only as a resource.",
      "Binding, summoning, or bargained service explains most of the ones an Expedition meets — ask who bound it.",
      "It fights by reshaping the room, not by outmaneuvering the people in it.",
      "Silence and stillness are the two things it cannot fake; both give away its position.",
    ],
    pressure: [
      "Terrain is half the encounter — let the room do damage the creature's stat block cannot.",
      "A quenched, smothered, or grounded elemental is a puzzle, not a stalemate; reward lateral thinking.",
      "Its origin (natural seam vs. bound servant) should change what victory means here.",
      "Use it to force positioning choices before initiative is even rolled.",
    ],
  },
  Fey: {
    opener: [
      "{name} answers to rules {zone} only partially shares with the rest of the Decennium.",
      "Somewhere adjacent to this fold of the Weave, a bargain is already being kept — {name} is enforcing it.",
      "{name} treats hospitality, names, and debts as load-bearing structure, not manners.",
      "The closer {zone} sits to an old fold, the more likely {name} is to have opinions about trespass.",
    ],
    behavior: [
      "It never lies outright and never tells the whole truth either; Directors should play every promise literally.",
      "Bargains offered by it always cost more than they first appear to — that is the entire point of it.",
      "It keeps its word with exact, punishing precision, which is worse than breaking it.",
      "Music, riddles, and names are weapons here as often as claws are.",
    ],
    pressure: [
      "Let a bargain with it cost something narratively real — a debt, a name, a future favor.",
      "Combat should be the failure state of a fey encounter, not the default one.",
      "Its 'defeat' rarely ends the arrangement it represents; the bargain often outlives the fight.",
      "Use it to teach a table that not every problem in the Decennium has a violent solution.",
    ],
  },
  Fiend: {
    opener: [
      "{name} is Chaos-Realm lineage wearing {zone} like a costume it intends to keep.",
      "The dissonance the Pact requires has a face in {zone}, and today it is {name}.",
      "{name} did not come to {zone} by accident — something summoned, bound, or invited it, and that debt is still open.",
      "Wherever {zone} keeps its oldest scars, {name} tends to be found standing in them.",
    ],
    behavior: [
      "It bargains before it fights, fights before it flees, and never forgets which party did which to it.",
      "Cruelty here is procedural, not passionate — it is simply how the thing gets what it wants.",
      "It reads weakness in a party's cohesion faster than in their hit points.",
      "If bound to a task, it will complete the letter of that task and corrupt everything around the spirit of it.",
    ],
    pressure: [
      "Ask who summoned or bound it before the fight starts — that answer is worth more than its loot table.",
      "Its eternal war with its own kind can be turned into an Expedition's advantage, once, expensively.",
      "Play victory as temporary; the dissonance it fed does not vanish when the body does.",
      "Use it to remind a table that the Pact's peace is a maintained thing, not a natural one.",
    ],
  },
  Giant: {
    opener: [
      "{name} measures {zone} in strides most Expeditions measure in days.",
      "Scale is the argument {name} makes before anyone gets close enough to hear another one.",
      "{zone} bears the marks of {name}'s passing the way a coastline bears the marks of tide.",
      "{name} does not fit the Decennium's corridors so much as override them.",
    ],
    behavior: [
      "It thinks in terms of territory, tribute, and thrown things — subtlety is not the danger here, mass is.",
      "Camps, caravans, and safe havens are what it breaks; adventurers are usually incidental to that.",
      "It negotiates only from a position of visible strength, and reads retreat as an invitation.",
      "Its rages are slow to build and slower to end — the fight rarely ends when the giant does.",
    ],
    pressure: [
      "Use it to force an Expedition to choose what to save — gear cache, safe haven, or each other.",
      "Siege framing works better than a duel; let the terrain itself become a casualty.",
      "Its size should matter mechanically as much as narratively — collateral damage is the point.",
      "A giant fight is a logistics problem wearing a combat encounter's face.",
    ],
  },
  Humanoid: {
    opener: [
      "{name} belongs to {zone}'s living politics, not merely its bestiary.",
      "Somewhere in {zone}, {name} answers to a chain of command an Expedition has not yet mapped.",
      "{name} is a person first and a stat block second, whatever the Excel sheet implies.",
      "{zone} has a culture, and {name} is one of the people who has to live in it after the party leaves.",
    ],
    behavior: [
      "It negotiates, informs, betrays, and remembers — treat it as a political actor, not a spawn point.",
      "Killing it has consequences that outlast the encounter: kin, rank, and reputation all keep score.",
      "It fights smarter than its stat block suggests when defending home ground or kin.",
      "Its loyalty is to people and place first, ideology a distant second.",
    ],
    pressure: [
      "Slaughter has a reputational cost — let floor factions remember which Expeditions chose it anyway.",
      "A parley option should exist even when the table does not expect to take it.",
      "Its death should change something on the floor: a market price, a patrol route, a grudge.",
      "Use it to make the Decennium feel inhabited, not just infested.",
    ],
  },
  Monstrosity: {
    opener: [
      "{name} is life that should not breed true in {zone} — and yet, evidently, it does.",
      "No natural process explains {name}; something in {zone} decided biology was a suggestion.",
      "{zone} keeps producing things like {name}, which is either an infestation or an ecosystem, depending who you ask.",
      "{name} looks assembled from parts that used to belong to smaller arguments.",
    ],
    behavior: [
      "It hunts with an efficiency that outpaces its apparent intelligence, which should worry Directors more than comfort them.",
      "Its territory in {zone} is marked in ways a careful Recon pass can read before contact.",
      "It does not recognize truce, and treats retreat as a hunting behavior to exploit, not a mercy to honor.",
      "Whatever twisted it here keeps twisting its offspring the same way — this is rarely a lone specimen problem.",
    ],
    pressure: [
      "Treat repeat sightings as an infestation problem, not a monster-of-the-week problem.",
      "Its parts are valuable specifically because it should not exist — Research teams will pay for proof.",
      "A Director can escalate this type across a Cycle as 'the thing that's spreading,' not just a floor's encounter.",
      "Use it to make an Expedition choose between finishing the kill and finishing the investigation.",
    ],
  },
  Ooze: {
    opener: [
      "{name} is {zone}'s patience made corrosive — it does not chase, because it has never needed to.",
      "Somewhere a watch rotation failed, a corridor sealed wrong, or a drain backed up, and {name} is the result.",
      "{zone} keeps {name} the way old buildings keep damp: quietly, structurally, and worse than it looks.",
      "{name} has no plan beyond dissolving whatever crosses it, which is exactly why it is dangerous.",
    ],
    behavior: [
      "It squeezes through gaps a locked door was supposed to make irrelevant.",
      "It reacts to heat, cold, or fire the way any digestive process reacts to being interrupted — badly, then worse.",
      "Splitting it without the right approach multiplies the problem instead of solving it.",
      "It does not negotiate, flee meaningfully, or feel provoked — it simply continues.",
    ],
    pressure: [
      "Punish poor watch rotations and sealed, unventilated corridors — this is an environmental hazard with a stat block.",
      "Let equipment loss (armor, rope, rations dissolved) matter as much as hit point loss.",
      "Use it to teach new Expeditions that not every threat wants to talk, flee, or be reasoned with.",
      "Its origin — natural seep vs. failed containment — is worth one line of Director foreshadowing.",
    ],
  },
  Plant: {
    opener: [
      "{name} grew where {zone} should have stayed empty, and kept growing past the point anyone could stop it politely.",
      "{zone}'s bloom cycles produced {name} the way a wound produces scar tissue — necessary, ugly, permanent.",
      "Root, spore, and vine answer to {name} across more of {zone} than any single map admits.",
      "{name} does not hate the Expeditions that pass through {zone}; it simply metabolizes them.",
    ],
    behavior: [
      "It controls area rather than chasing targets, and rewards patience with worse odds the longer a fight runs.",
      "Spores, pollen, or sap do the softening; whatever passes for a 'mouth' does the rest.",
      "It reacts to fire and light with something close to fear, if fear is the right word for a plant.",
      "Cutting the visible threat rarely solves the root problem — literally, in {zone}.",
    ],
    pressure: [
      "Play it as area control and attrition, not a single dramatic strike — let the terrain punish lingering.",
      "A Support team's antidotes and cleared sightlines matter more here than raw damage output.",
      "Its harvestable parts are valuable exactly because most Expeditions are too busy fleeing to collect them.",
      "Use it to make retreat a real, costed choice instead of a free action.",
    ],
  },
  Undead: {
    opener: [
      "{name} is history in {zone} that refused to stay buried, in the most literal sense available.",
      "Whatever ended {name}'s first life did not end its business in {zone}.",
      "{zone} keeps its dead close, and {name} is proof that 'close' is not the same as 'quiet.'",
      "{name} remembers a version of {zone} that no living Expedition member has ever seen.",
    ],
    behavior: [
      "It repeats a pattern from its living life — a duty, a grudge, a routine — with none of the judgment that once tempered it.",
      "Necrotic pressure here is meant to be felt: fear, exhaustion, and dread should cost the party something mechanical.",
      "It does not negotiate with the living, only occasionally with itself, out loud, in fragments.",
      "Turning or destroying it does not always end whatever compelled it to rise in the first place.",
    ],
    pressure: [
      "Necrotic and fear pressure should specifically tax Support teams' healing and morale resources.",
      "Its unfinished business, once learned, is often the actual quest — the fight is a symptom.",
      "Let its remains carry one true clue to why it rose, even in a throwaway encounter.",
      "Use it to remind a table that some floors of the Decennium are, quite literally, graves.",
    ],
  },
};

function ecologyFor(m, displayName) {
  const type = m.type || "Monstrosity";
  const bank = BANKS[type] || BANKS.Monstrosity;
  const zone = m.zoneFound || "the depths";
  const seed = `${m.name}|${zone}|${m.challengeRating}`;
  const opener = pick(seed, bank.opener, "opener").replaceAll("{name}", displayName).replaceAll("{zone}", zone);
  const behavior = pick(seed, bank.behavior, "behavior");
  const pressure = pick(seed, bank.pressure, "pressure");
  return `${opener} ${behavior} ${pressure}`;
}

module.exports = { ecologyFor, hashSeed, pick };
