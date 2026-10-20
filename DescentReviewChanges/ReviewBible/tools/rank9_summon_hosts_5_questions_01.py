"""Unselected source-local questions for five rank-nine summoned hosts."""

IDS = ['summon-elemental-avatar', 'conjure-magmatic-wyrm', 'planar-army', 'summon-herald-of-the-planes', 'summon-avatar-of-decay']
EA, MW, PA, HP, AD = IDS
TIERS = {
    EA: ('C', 'A complete 180-HP body, three attacks per round, elemental resistances and an aura require explicit profiles and timing.'),
    MW: ('C', 'A massive 250-HP fire serpent and 6d12 cone lack a lifespan, complete body and breath procedure; Core says Instantaneous.'),
    PA: ('C', 'Army-scale extraplanar service requires actual count, identities, profiles, command throughput, deployment and endings.'),
    HP: ('C', 'A unique CR15+ celestial, elemental or outsider cannot be supplied by a generic unrated pet or invented cosmological identity.'),
    AD: ('C', 'A 250-HP rot avatar commanding all undead needs a complete body, aura and explicit multiple-controller/agency rules.')
}
Q = []

def q(n, ids, source, options, recommendation):
    Q.append((f'R9SH-{n:02}', ids, source, options, recommendation))

q(1, IDS,
  'None of the five printed descriptions supplies a complete executable creature profile. Accepted defaults cover some missing ordinary values, but do not invent attacks, anatomy, type, mass, movement modes or a rated herald.',
  ['Author complete spell-specific profiles with each inherited default and each NEW field explicitly marked.', 'Bind genuinely complete existing native profiles where exact eligibility and all printed benefits are proven; author only the remaining fields.'],
  'Use actual native evidence first. Return complete positive-use profiles, source ownership and resource records; never substitute a foreign monster or mark a missing profile resolved by an eligibility guard.')
q(2, IDS,
  'The owner-wide one-command and one-offensive-companion allowance is accepted. Several new spells promise multiple attacks, an army, or control over all undead; their additional throughput is not specified.',
  ['Inherit the accepted shared allowances, expressly defining complete multiattack/pulse components within one real offensive opportunity.', 'Select and justify a named spell-local exception where necessary to preserve an army/control promise, with exact cross-family budgets.'],
  'Do not silently multiply allowances, or silently reduce the promised benefit for tabletop convenience. Identify the real gameplay tradeoff and every affected owner/controller/round ledger.')
q(3, IDS,
  'Creation, transport of an existing being, and a new control relation have different identity, source, cargo and death consequences. Names such as avatar/herald do not decide which exists.',
  ['Select a generated-body lifecycle for a source that actually supports that reading, with exact same-spell caps and replacement.', 'Select preexisting identity/transport or control where the wording requires it, with conserved records and an explicit return/ending contract.'],
  'Select each identity separately. Keep no-concentration versus concentration, body death versus source removal, and old concentration ending before a failed replacement distinct. No free corpse, soul, inventory, XP or unlimited resummon refresh follows.')
q(4, [EA, MW, PA, AD],
  'The AC4/AC5/AC6 living-ally healing extensions are named exceptions. Companion10 expressly does not extend them to every new summon. Actual Wizard Conjuration and eligible Flesh Ascendant maximum-HP rules are already settled.',
  ['Use only healing sources whose actual target predicate already admits the selected new body.', 'Author a precise healing-target extension for named new profiles without inventing biology or universally changing Undead/Construct targeting.'],
  'State the eligible healing/repair routes and NullDisabled0 recovery for each profile. Inherit actual creation snapshots and dynamic controller bonuses without alias duplication or capacity-growth healing.')
q(5, [EA, MW, AD],
  'The avatar aura, rot aura and cone need source-local roots and repeated exposure rules. Existing Greater Fire Pet aura, AC6 companion roots and P20 pulse rules have different named scopes.',
  ['Use explicit per-recipient roots and a stated repeated-exposure schedule with declared family keys.', 'Use a single rolled pool where justified while retaining independent recipient saves, defenses and exact damage-root ownership.'],
  'Specify source body as actual dealer where it acts, original stat owner separately, critical versus save dice, concentration consequences and creation-time Null flags. No owner Veil, lifesteal, resource recovery or harmful repeated tick is inherited by name.')
q(6, IDS,
  'Accepted summon suppression differs: AC6 preserves occupied paused bodies, Companion Knight removes expression temporarily, and Companion Wraith ends its manifestation. None is a universal choice for these five.',
  ['Select a retained-body or pending-expression policy for each generated profile with exact geometry, identity, clocks and cargo.', 'Select a terminal expression ending, or suppression of control alone for an existing being, where explicitly justified.'],
  'Define partial-body/local-area versus whole-parent suppression, rider-only suppression, pending orders, dispel capture, unsupported Falling and real expiry. A multi-body army requires individual and parent records; no heal, fresh turn or missed-pulse replay on resumption.')

q(7, [EA],
  'Summon Elemental Avatar prints HP180 but no body size, elemental choice, anatomy, mass, attack type or movement modes. The title does not imply all elements, all movement modes or deity embodiment.',
  ['One complete selected elemental profile, with any element fixed at formation.', 'A finite menu of complete source-local elemental variants preserving the same printed benefit set.'],
  'Provide exact occupied volume, actual mass, handling/carrying, respiration if relevant, attack/saves/checks and perception. Changing appearance or controller cannot refill HP or silently select a new element.')
q(8, [EA],
  'The source says attacks 3x/round, rather than explicitly naming three Actions. Existing Air Pet multiple attacks can form one damaging Action, but the new per-round ceiling must remain real.',
  ['Three separately resolved attacks within one commanded offensive Action and one body/numbered-round allowance.', 'A precisely scheduled split-attack permission with the same genuine three-attack round ceiling and an explicit command exception.'],
  'Favor the inherited multiattack shape if it preserves all three attacks. Specify reach, attack/damage profile, target changes, movement between strikes, failed later targets, unused strikes, extra turns, control transfer and recasting.')
q(9, [EA],
  'Elemental resistances is a positive printed clause without an enumerated damage set. It does not say immunity, absorption, healing or adaptive invulnerability.',
  ['A fixed explicitly enumerated resistance set on the complete profile.', 'A selected elemental variant with an explicitly enumerated corresponding resistance set.'],
  'Retain useful plural resistances and state mixed-damage allocation, exact source-qualified penetration, suppression and form/control changes. Do not invent a missing global elemental-damage taxonomy.')
q(10, [EA],
  'Aura damage has no radius, amount, damage type, target category, trigger, save or overlap rule. Greater Fire Pet uses perceived hostile recipient future STARTs and is only a comparison.',
  ['A genuine passive aura with exact recipient/geometry/pulse/save/damage rules, distinct from the commanded three strikes.', 'An explicitly activated aura mode with a stated action relationship, only if the printed passive-looking benefit is consciously reconciled.'],
  'Require useful quantified aura behavior. State ally/caster/other-avatar exposure, actual LoE, entry versus START timing, outside-initiative cadence, suppression and whether a pulse consumes any allowance. No secret allegiance oracle.')

q(11, [MW],
  'Conjure Magmatic Wyrm gives a massive HP250 serpent that breathes 6d12 fire. Core duration Instantaneous does not define how long this creature exists or imply it vanishes before acting.',
  ['Treat Instantaneous as the creation event and author a precise nonconcentration body lifespan/endings.', 'Expressly reconcile Core to a selected sustaining duration/concentration procedure while preserving the original field unchanged as evidence.'],
  'Select a useful actual lifetime, not an undefined permanent asset or a single instantaneous blast replacing the creature. Define same-spell caps, dismissal, paid replacement and behavior after caster incapacity/death.')
q(12, [MW],
  'Massive fire serpent supplies a body concept and HP250, but not a Size category, occupied dimensions, body mass, support, locomotion or handling.',
  ['One explicitly sized corporeal serpent profile with actual support and terrain interaction.', 'An explicitly magical supported body profile with each exceptional locomotion/weight rule individually stated.'],
  'Keep a substantial serpent body and exact fit. No flight, lava swimming, burrowing, wall passage, rideability, hands, infinite Load or intangibility arises from the name. State a genuinely legal formation and subsequent route.')
q(13, [MW],
  'The breath is specifically 6d12 fire in a cone; cone length, source origin, save/result, use cost and frequency are missing.',
  ['A complete commanded breath Action with a fixed per-round/recharge/use policy.', 'A complete alternative attack mode sharing its real offensive opportunity with other authored actions.'],
  'Preserve six d12 and fire. Bind exact three-dimensional cone/witness geometry, minimum range if any, allies, cover/occlusion, save modifier/DC provenance, half/none outcome, dice pool, interruption and finite frequency. No imported dragon recharge.')
q(14, [MW],
  'No bite, claw, tail attack, spell list or breath-exhaustion fallback is printed. A complete game creature still needs explicit ordinary actions and a useful behavior when breath is unavailable.',
  ['Use accepted ordinary actions and the full breath as its only authored offense.', 'Author additional narrowly justified native attacks or maneuvers with complete numeric profiles and clear shared budgets.'],
  'Do not claim optional extra attacks were in the source. No attack happens for free on creation; state command hearing/perception, creation-turn eligibility and defensive behavior.')
q(15, [MW],
  'Fire serpent and fire cone do not themselves supply terrain ignition, molten fluid, light, smoke, heat damage to cargo or harvestable fuel.',
  ['Apply only already-authored environmental/object consequences actually triggered by the breath or body.', 'Add specifically bounded environmental expressions with complete rates, geometry, object targeting and endings.'],
  'Keep the printed fire damage while distinguishing visual presentation from mechanics. Any persistent fire/terrain result must have a real source, finite lifecycle and conserved objects; real carried property does not become conjured loot.')

q(16, [PA],
  'Planar Army promises an army of extraplanar creatures to serve. Actual Faction Army creates temporary representations; Greater Planar Ally creates a source-local body. Neither decides this source identity.',
  ['A complete created army with explicit extraplanar source classification and no invented native-plane history.', 'A real called contingent with individual persistent identities, eligibility/consent, source locations and an actual return contract.'],
  'Confer on the word army and the service promise. No default conscription of named NPCs, duplication of possessions, new divine authority or universal plane taxonomy. Genuine travel tests apply only to actual transit.')
q(17, [PA],
  'No soldier count, composition, formation size, quality or CR is printed. Copying Faction Army 3d6/HP20 would be a new design choice, not source recovery.',
  ['A fixed army-scale count with one or more complete profiled unit roles.', 'A declared bounded composition budget with complete qualifying profiles and deterministic count/selection.'],
  'Supply an actual positive army, not an undefined placeholder or one unrelated pet. Explain its capabilities at 26RP and its one-minute source without claiming balance approval. Every unit has its own body, HP, gear, location and eligibility.')
q(18, [PA],
  'An army may inherit the shared one-companion offensive Action, but that creates a consequential throughput choice. Faction Army currently allows only one soldier to spend that allowance.',
  ['Preserve the exact inherited one-soldier offensive command, with a complete account of the army\'s other useful service.', 'Author a bounded cohort command/offense exception giving a stated set of real unit actions within one owner transaction.'],
  'Discuss the intended benefit rather than silently copying a weak or broad rule. A cohort action must still resolve each body\'s reach, path, save, ammo, damage root and interruption. No tabletop aggregation may erase separate targets or casualties.')
q(19, [PA],
  'Core gives120ft range but no deployment radius, fitting policy, predeclaration or partial-formation rule for many bodies.',
  ['Predeclare ordered legal whole-body spaces and form only the selected still-valid count with exact partial-success rules.', 'Require a fully legal complete declared formation and define an atomic all-or-nothing establishment.'],
  'Bind real visibility, LoE, height/support, no overlap, inter-unit order and hidden invalidity after payment. Any partial cohort must have an explicit identity/replacement rule; it grants no after-roll search, crushing or automatic escape.')
q(20, [PA],
  'Serve you is broader than an attack, while the one-minute duration and actual expedition jobs forbid inventing completed watches, labor output, institutional rank or proficiency.',
  ['Allow complete profiled combat/manipulation/transport services with actual time, capacity and commands.', 'Also authorize specified skilled tasks by giving complete proficiencies and linking real existing job records.'],
  'Preserve meaningful service without phantom offscreen progress. Materials, worker identity, movement, working time and custody remain real; a conjured uniform grants no faction permission, training, tax exemption or Extraction.')
q(21, [PA],
  'A one-minute concentration army needs individual casualties, local suppression, whole-parent endings and any true returned-person behavior reconciled.',
  ['Generated bodies end under a selected finite-body policy, with external cargo settled at actual positions.', 'Called beings retain underlying bodies and use a separately authored lawful return/stranding policy at each ending.'],
  'Resolve blocked returns, plane separation, independent dispel of one body versus parent, Null-disabled soldiers and foreign passengers individually. No global rescue immunity, fresh loot or batch recreation of dead units.')

q(22, [HP],
  'The source calls a UNIQUE CR15+ celestial, elemental or outsider to aid you. Unique might identify a real named being, or a uniquely instantiated herald; neither reading is already settled.',
  ['A genuinely existing eligible unique individual with actual availability, identity and retained resources.', 'A specifically authored unique herald identity/manifestation with a registry and complete source-local definition, explicitly selected as NEW.'],
  'Keep unique meaningful across recasts, casters, control and concurrent manifestations. No generic unnamed unrated profile may quietly replace it. A new herald must not silently become a canonical god or rewrite an established NPC.')
q(23, [HP],
  'CR15+ is an inclusive lower bound with no printed upper cap. The supplied72-entry bestiary includes the Director-sealed CR22 Elemental Lumen, but a source stat block is not an operationally accepted summon profile.',
  ['Bind an actually eligible complete native profile and resolve every missing field before claiming a positive case.', 'Author and disclose a complete new eligible profile/selection policy, preserving15+ as a separate rating and balance obligation.'],
  'Do not invent a ceiling or relabel an unrated creature CR15. Keep exact type, unique status, defenses/actions/body/gear/agency/source clocks explicit. Lumen is evidence of a candidate, not automatic availability, consent or approval; Fiend is not automatically Outsider.')
q(24, [HP],
  'Aid you does not explicitly grant domination, universal obedience, secret extraction, free finite powers, a bargain price or willing consent.',
  ['A source-local cooperative aid contract with explicit willingness/availability and bounded commands.', 'A specific spell-created service relation with explicit agency, permitted acts and conflict limits.'],
  'Return actual useful aid and precise refusal/illegality behavior without making every positive case a rejection. Name any cost or permission added as NEW; no hidden deity veto, compulsory oath violation or free resource refresh.')
q(25, [HP],
  'Arrival and ending depend on the selected identity. Lumen\'s preserved source specifically says it cannot be permanently displaced from its arena while its Seal is active; that does not automatically answer a temporary call.',
  ['Actual transport with source-specific eligibility, legal endpoints, travel guards and a fully specified return.', 'A source-local manifestation while preserving the distinct existing identity and prohibiting ungranted duplicate bodies or arena benefits.'],
  'Confer on the actual Gate-bound text if using that candidate. No blanket immunity to Anchor/wards, automatic bypass of arena objectives, stolen Gate rewards or invented forced-return exception. Preserve its source and the public/Director knowledge boundary.')
q(26, [HP],
  'The herald may have real knowledge, equipment, spellcasting, finite uses and continuing effects. Summoning does not inherently disclose every hidden record or refresh anything.',
  ['Use the exact selected being\'s extant resources, knowledge permissions and agency, conserved across arrival/return.', 'Define a complete finite manifestation resource budget distinct from the original, explicitly resolving what information and child effects it can produce.'],
  'Keep real spell costs/components/repertoire/concentration/cadence, gear custody and downstream effect expiry. Aid is not automatic prophecy, all research completion or disclosure beyond the failed Sixth Gate. Supply complete positive ability use before calling the case complete.')

q(27, [AD],
  'Avatar of Decay prints HP250, aura of rot and commands all undead. It does not explicitly assign the avatar itself an Undead type, anatomy, attacks or immunity.',
  ['An explicitly typed complete generated profile with the printed HP and both substantive benefits.', 'A source-qualified existing profile only if all required properties and identity rules are independently supported.'],
  'Do not infer a lich, deity, auto-resurrection, necrotic immunity, spell list or personal soul. State the exact effect of actual type on healing, Null, banishment and acquired maximum-HP features.')
q(28, [AD],
  'Aura of rot lacks numeric effect, radius, affected categories, damage type, trigger and save. Rot is not automatically disease, corrosion, maximum-HP loss, crop death or object destruction.',
  ['A fully quantified damage aura with exact body/LoE/recipient/timing/save rules.', 'A fully quantified rot rider or damage-plus-rider aura, explicitly authored with all lifecycle and stacking fields.'],
  'Preserve a real useful aura. Resolve living, Undead, allies, caster, objects and environmental targets as stated choices; do not silently substitute a mere visual or add unlimited permanent decay.')
q(29, [AD],
  'Commands ALL UNDEAD has no printed numeric cap, CR limit or own-summons qualifier. Command Undeath\'s exactlyCR2/two-body limit is source-local and cannot be imported.',
  ['A spatially bounded all-eligible-Undead command relation with no hidden count/CR cap.', 'Another explicit complete admission/channel model retaining the all-undead promise and explaining its reach.'],
  'Confer on range, perception, LoE, plane, PCs/bosses, allies/enemies and classification transitions. Do not narrow it to owned pets, count corpses as Undead creatures, or infer a global cosmological command channel.')
q(30, [AD],
  'Control can collide with existing Command Undeath, Wizard/Mage ownership and other actual control sources. All-undead wording does not name a save, Charm type or universal newest-effect priority.',
  ['Explicit automatic admission with stated actual hard-control and source-specific immunity/priority handling.', 'An expressly NEW save or contest model with a defined admission point and preserved printed broad eligibility.'],
  'Choose and justify any added resistance. Identify original caster, acting avatar, controlling character, target and encounter guard keys; no fresh guard per summon. Preserve native ownership/resources and every competing relation rather than deleting history.')
q(31, [AD],
  'The caster commands the avatar, which commands other Undead. The source does not state whether one paid command propagates, each target needs a command, or all can act independently.',
  ['A complete bounded chain of command using existing real opportunities and exact shared allowances.', 'A named all-undead command exception with explicit per-body scheduled execution and cross-owner reservations.'],
  'Make all-undead control operationally useful while keeping costs explicit. Do not grant a companion an invented owner turn, refresh independent initiatives, charge an unwilling original owner a phantom Bonus Action, or erase another source\'s structural caps.')
q(32, [AD],
  'The avatar expires after one minute of concentration, but the command relation and pending orders have no separate stated lifetime. Suppression of aura, body and control can occur independently.',
  ['Tie each created control relation to the live avatar source and its own actual scope, ending cleanly with the parent.', 'Select a distinct explicitly bounded relation lifetime only if justified, preserving every underlying creature and actual schedule.'],
  'Specify loss of reach, avatar/caster death, suppression, ending, resumption and multiple avatars. Clear spent/expired orders without replay; restore actual agency without a new turn, free heal, allegiance or loot. Independent aura effects retain their own lawful endpoints.')

FINDINGS = [
    'All five are rank9/class17/base26RP, Action/120ft/V,S,F. Four have concentration up to one minute; Wyrm uniquely has Core Instantaneous. These known fields are not reopened as questions.',
    'Druid/Mage/Wizard access the three Conjuration identities. Herald is Divination through Cleric/Wizard; Decay is Necromancy through Cleric/Druid/Wizard. Mage does not inherit the last two and Cleric does not inherit the Conjuration trio.',
    'Elemental Avatar retains180HP,three attacks per round,plural elemental resistances and actual aura damage. Wyrm retains250HP,a massive serpent body and6d12 fire cone. No nominal label substitutes for complete effects.',
    'Planar Army retains an army of extraplanar creatures serving the caster. Herald retains a unique eligible creature and open-endedCR15+ lower bound. Decay retains250HP,real aura of rot and commands all undead without silently importing Command Undeath\'s two/exactCR2 limits.',
    'Accepted ordinary command/attached-phase rules are supplied in full. Explicit multiple attacks can share one offensive Action; extra turns do not multiply numbered-round allowances. Army and chained undead command throughput are consequential unresolved source-local choices.',
    'Complete applied AC4/AC5/AC6 comparisons show source-specific healing/suppression/creation and transport decisions. Their current accepted procedures govern stale internal proposal labels; the new five do not inherit every exception by analogy.',
    'Actual Companion10 exact05 source/model/casebook/register/acceptance and its two held exactCR2 cases are included unchanged. Control15 and preparation-only copied Ready context remain accepted-but-unapplied and scoped; the independent five positive-content holds remain open.',
    'The bounded original bestiary scan covers67 public and5 Director-sealed entry files, all preserved in full. Lumen is printed Large Elemental/CR22, has a Gate-bound clause, fragmentary Sixth-Gate disclosure limits and incomplete action geometry. That is a genuine source candidate, not an approved eligible summon or globally exhaustive search.',
    'Original cosmology manuscripts, saved website, current owner corrections and Q6 are supplied. Avatar,extraplanar,herald andUndead do not invent native planes,soul identity,divine authority,Hunt exceptions or an Equation.',
    'Full real body,source,gear,resource,clock,agency and job identities must survive control/transport/suppression/ending. Literal fictional complexity is handled by software; no tabletop simplification is an active requirement.'
]
CASES = [
    'At least two complete source-qualified positive encounters per identity, plus meaningful independent branches. Supply actual original class/access/repertoire/automatic features,real26RP transaction,all current modifiers,body coordinates/height/mass/support,actual actor opportunities,RNG,transitions and final state. A native source-only stat block is not an executable test premise.',
    'Elemental Avatar: all three independently resolved strikes and real passive aura; one miss/critical/blocked later target; actual resistance against mixed damage; different-source control/extra-turn stress without fourth attack or duplicate root.',
    'Wyrm: lawful massive whole-body formation and exact6d12 cone against multiple recipients with distinct cover/defenses; complete second use/frequency/lifespan example; no inferred fuel,terrain burning or free ordinary attack.',
    'Army: full actual multi-unit count/composition/deployment,one obstruction,explicit command throughput and useful service; independent casualties/Null/local suppression,cargo settlement and whole-parent ending with no fabricated army-wide state.',
    'Herald: an actually complete eligibleCR15+unique profile,positive useful aid and source-bound knowledge/resource use; concurrent call/availability,unique identity,transport/manifestation choice,blocked return and actual Gate-bound restrictions where relevant. Retain a content hold until a real positive profile is supplied and reviewed.',
    'Decay: real aura plus commands over several independently sourced Undead including one not already owned; competing relation/admission/immunity/hard-guard facts,real independent and attached schedules,full chain of command and restoration of original agency.',
    'Every body: ordinary zero versus qualifying NullDisabled0,actual legal healing or missing-target guard,concentration/expiry/dispel/full and rider-only suppression,unsupported Falling,actual gear and pending-placement conservation. Creation and resumption never refill old budgets or source clocks.',
    'Source packaging checks are not authored acceptance. Arithmetic/specification checks are not engine execution; finite profile ratings,positive content prerequisites,human gameplay,balance,cosmology and whole-game/release approval remain distinct.'
]

assert len(Q) == 32 and len({r[0] for r in Q}) == 32
