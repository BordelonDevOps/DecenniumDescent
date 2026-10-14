Codex has authored the28-condition normalized candidate + finite recovery guide below. All exact Core texts/book SHA/paragraphs remain intact; all original books untouched. First53 reference regressions +4200 Exhaustion-state cases PASS. Please adversarially review EXACT candidate and return only concrete blockers/corrections or bounded closure, not another wholesale duplicate. New decisions beyond round2 needing explicit review: inherited condition immunity suppresses only covered components with clocks continuing; Staggered permanently consumes Guard (Core Guard paragraph394 +2AC firstattack +Interpose), forbids reGuard while active and cannot refresh spent +5ft by reapplication; blocked Exhaustion levels tracked per-source; resurrection with level6 still present dies again; project days actual24h/no overlap/reused costs; Alchemy INT/tool and DC14 fallback if directAddicted has noDC; tolerance doubledose one consumption event at mostone dependence save; Intoxication fear-save use once percontinuousnonzeroepisode; timed direct Intoxicated floors; level5fixeddeadline cannotreset, treatmentcompletionmustprecede deadline, thirdWoundcare nofourth exception; Unity currentrowonly andExposuregain at capinterruptsAnchor.

Potential weak point I want you to attack: direct timed Intoxication floors versus level4/5 timers. If simpler, restrict the generic timed Intoxicated application to floor2 (what its condition says); any timed higher track-setting source must explicitly state whether it creates dose-driven points or has own recovery exception. Avoid an ambiguous floor5 ending and stranding an emergency on a nominally0 track.

Please check no impossible timer, no zero-cost state resets, no mutation of approved source text, no accidental loss of independent conditions, no bestiary/lore leak. Verify prerequisites/roles/cost/DC/ends of all generic projects. Broader individual spell/item and vision audit remain future rows, not claims of full game closure. 28conditions identity/reference plus generic recovery is our bounded scope. Could this close authored DD16 condition definitions/recovery while broader application and balance remain in their own rows?

EXACT normalized candidate:
{
  "schemaVersion": "1.0",
  "status": "provisional draft; final adversarial review pending",
  "scope": "All28 Core condition identities preserved. New generic procedures are explicit playtest proposals, not edits to approved books or a claim of game-wide balance.",
  "sharedRules": [
    "This overlay governs generic conditions in the combined candidate. A reviewed card overrides a generic clause only where it prints the specific exception. An unreviewed historical summary never grants an extra ability or bypasses a gate. The existing combined source-character/target/encounter hard-denial cap still applies to class/spell/companion applications.",
    "Record each condition source, affected creature, applying DC, magnitude, start, duration and ending method. Same-name nonnumeric penalties apply once; independent sources continue until each ends. A generic cure naming the condition clears its generic source records, while a cure naming just one application clears only that record. Track Charmed, Frightened, Marked and Grappled relationships separately. Exhaustion, Intoxication, Unity and Wounds use their explicit tracks.",
    "Immunity to a named condition prevents that condition, including an inherited component, but does not silently grant immunity to every parent condition that can cause it. For example, Prone immunity prevents the Prone component of Unconscious, not its other effects. Immunity to an inflicted condition never erases the underlying zero-HP or dead state. Gaining immunity suppresses applicable existing effects while immunity lasts; their clocks continue unless explicitly paused. Removing immunity does not reapply a one-time consequence or restart an old duration.",
    "Advantages and disadvantages never multiply dice: any advantage and any disadvantage cancel to one normal d20 roll, regardless of the number of sources. Automatic failure of a required check/save is resolved without a roll. A condition does not give a save where its source grants none. A critical-if-hit rider never makes a missed attack hit.",
    "For generic Bleeding/Burning, tick once at the end of each regular turn, not extra turns. Outside initiative tick once per six full elapsed seconds. Retain the last periodic event across initiative transitions; changing time modes cannot duplicate a tick in the same six-second period. At each tick choose the active record with highest expected damage before defenses, then highest ending DC, then earliest application; use that whole record, not mixed damage/type/DC from different records. Specific printed replacement timing controls its own record.",
    "Strain is the expedition track and is separate from the six-level Exhaustion condition. Oracle one-turn Revelation backlash is also separate from global Exhaustion; its printed penalties and endpoint remain unchanged. Wound Eater feeding failures explicitly use global Exhaustion. Never silently convert similarly named tracks.",
    "See CONDITION_RECOVERY_PLAYTEST.md for finite recovery, cleansing, substance, Intoxication and Unity procedures. These new proposals are labeled separately from recovered source rules. Conditions do not reveal Director secrets or force player beliefs or decisions."
  ],
  "conditions": [
    {
      "id": "addicted",
      "name": "Addicted",
      "coreText": "The creature has dependence on a named substance. Without a maintenance dose after a long rest, it gains Withdrawal.",
      "compatibleV6Details": [],
      "sourceConflicts": [],
      "effect": "Record dependence on one named substance. After each completed long rest, if the creature has not taken the required maintenance dose for that substance, apply Withdrawal for that substance. Existing source procedures for repeated doses, dependence DC, tolerance and overdose continue to operate.",
      "application": "Applied only by a substance or dependence procedure that explicitly creates or advances dependence. Merely consuming a substance does not automatically grant Addicted unless its procedure says so.",
      "durationAndEnding": "A new maintenance dose is due immediately after each completed long rest. Until taken, apply that substance's Withdrawal; a pre-rest dose cannot satisfy this new interval. A dose suppresses symptoms until the next maintenance interval, but dependence persists. A seven-day no-dose recovery project or an explicit dependence-removal effect can remove it; see CONDITION_RECOVERY_PLAYTEST.md.",
      "stacking": "Track one Addicted record per named substance. Separate substance dependencies coexist; duplicate dependence on the same substance does not create multiple copies unless a source defines severity.",
      "immunitiesAndOverrides": "A feature explicitly preventing dependence blocks application. Magic that only removes symptoms does not automatically remove dependence, consistent with the source treatment text.",
      "provisionalDecisions": [
        "NEW: maintenance dose may relieve that substance's current Withdrawal symptoms without removing Addicted; exact dependence cure procedure remains deferred."
      ],
      "openDependencies": [
        "Audit individual substance cards, dose escalation wording, equipment availability and specific cure effects during item integration."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 727,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "bleeding",
      "name": "Bleeding",
      "coreText": "Take damage equal to proficiency bonus at the end of each turn. An action and Medicine check or magical healing ends it.",
      "compatibleV6Details": [],
      "sourceConflicts": [],
      "effect": "At the end of the affected creature's regular turn, take damage equal to its current PB, unless the selected reviewed application prints a different magnitude. Use that application's specified physical type; if none, slashing.",
      "application": "Only explicit Bleeding applications create a source record. Record DC (or 10), magnitude, type and endpoint.",
      "durationAndEnding": "Persists until its source ends or a generic cure ends Bleeding. The affected creature or an adjacent helper may spend an Action and make WIS (Medicine) against the selected active record's DC, or DC 10 absent a source DC. Task Success or Critical Success ends it. A legal magical healing effect with positive healing potential before caps and condition reductions also ends it after resolution, even if full HP or Corrupted reduces actual healing to zero.",
      "stacking": "Keep independent records but use one selected whole record per tick by shared precedence. A generic cure clears all generic Bleeding records.",
      "immunitiesAndOverrides": "Creatures explicitly immune to bleeding/blood-loss effects cannot gain it. Specific spell/class/item Bleeding numbers replace the generic PB magnitude only when printed.",
      "provisionalDecisions": [
        "NEW: affected-creature PB; explicit physical type or slashing fallback; source DC or 10; one regular-turn tick and strongest-record selection.",
        "Source-faithful clarification: magical healing need not increase current HP to end Bleeding."
      ],
      "openDependencies": [],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 729,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "blinded",
      "name": "Blinded",
      "coreText": "Cannot see; automatically fails sight checks; attacks have disadvantage and attacks against it have advantage.",
      "compatibleV6Details": [
        "V6 matches: cannot see, automatically fails sight-required checks, own attacks have disadvantage, attacks against have advantage."
      ],
      "sourceConflicts": [],
      "effect": "The creature cannot see, automatically fails checks that require sight, has disadvantage on attack rolls, and attack rolls against it have advantage.",
      "application": "Only an effect that explicitly inflicts Blinded applies it.",
      "durationAndEnding": "Use the applying effect's printed duration, save, cure or endpoint.",
      "stacking": "Multiple Blinded applications do not increase the penalties; track independent durations only when needed to know when all sources have ended.",
      "immunitiesAndOverrides": "A sense that does not require sight may still function. A feature explicitly allowing sight while Blinded overrides only its printed scope.",
      "provisionalDecisions": [],
      "openDependencies": [
        "Full special-senses and vision interaction belongs to the stealth/vision pass."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 731,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "burning",
      "name": "Burning",
      "coreText": "Take fire damage at end of turn. An action, immersion, or successful Dexterity save ends it.",
      "compatibleV6Details": [],
      "sourceConflicts": [],
      "effect": "At the end of the affected creature's regular turn take 1d4 fire damage, replaced by a selected application that explicitly prints another magnitude. Then make the ending DEX save.",
      "application": "Applied only by an effect that explicitly inflicts Burning. Record the applying effect's DC; if none exists, use DC 10.",
      "durationAndEnding": "The affected creature or adjacent helper may spend an Action to end ordinary Burning. Full immersion of all burning portions also ends it immediately. Otherwise, after each periodic damage tick make a binary DEX save against selected source DC (or 10); success ends Burning. Exceptional flames ignore these methods only if their reviewed card explicitly says so.",
      "stacking": "Independent records retain their endpoints, but one selected whole record supplies magnitude/DC/type at each tick. Generic ending methods clear all generic Burning records.",
      "immunitiesAndOverrides": "Fire immunity prevents the damage but does not automatically end Burning unless the source or immunity says so. An effect explicitly immune to Burning blocks application.",
      "provisionalDecisions": [
        "NEW: 1d4 fire fallback, source DC or 10, damage then free ending save; Action/immersion can end before damage.",
        "NEW: shared periodic timing and strongest-record precedence; adjacent helper and immersion boundaries."
      ],
      "openDependencies": [],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 733,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "charmed",
      "name": "Charmed",
      "coreText": "Cannot willingly harm the charmer; charmer has advantage on social checks against it.",
      "compatibleV6Details": [
        "V6 specifies the creature cannot attack the charmer or target the charmer with harmful abilities or magical effects, and gives the charmer advantage on social interaction checks."
      ],
      "sourceConflicts": [],
      "effect": "The creature cannot willingly attack or target the charmer with a harmful ability or magical effect. The charmer has advantage on social ability checks against that creature. Charmed by itself does not command actions, alter beliefs or force allegiance.",
      "application": "Each application identifies the charmer/source.",
      "durationAndEnding": "Use the applying effect's printed duration and repeat-save/ending procedure.",
      "stacking": "A creature may be Charmed by more than one source; each source relation is tracked independently. Advantage does not stack.",
      "immunitiesAndOverrides": "Charm immunity prevents application. Forced actions from another effect are not made voluntary merely because the creature is Charmed.",
      "provisionalDecisions": [
        "Agency clarification: Charmed never by itself grants control over beliefs, targets or decisions beyond the explicit harm restriction."
      ],
      "openDependencies": [],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 735,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "corrupted",
      "name": "Corrupted",
      "coreText": "Healing is reduced, corruption-sensitive effects worsen, and long rests may shift behavior or form until cleansed.",
      "compatibleV6Details": [
        "V6: healing effects restore half normal HP; disadvantage on saves against spells/abilities from evil creatures; faint aura detectable by magic revealing evil; at end of each long rest make DC 15 Wisdom save or alignment shifts one step toward evil."
      ],
      "sourceConflicts": [],
      "effect": "Halve each healing effect's final potential HP once, rounded down, before the HP ceiling. Saves against spells/abilities from individually recorded Evil creatures have disadvantage; its aura can be detected by effects revealing evil. At each completed long rest make DC 15 WIS save or move one moral step Good to Neutral to Evil, leaving law/chaos unchanged. Already Evil remains Evil. Alignment does not compel conduct, party separation, PvP or automatic oathbreaking.",
      "application": "Only effects that explicitly inflict Corrupted apply it.",
      "durationAndEnding": "Persists until an explicit cleansing effect or the eight-hour cleansing project in CONDITION_RECOVERY_PLAYTEST.md succeeds. Long rest alone does not cleanse it. At a simultaneous cleansing/rest endpoint, resolve cleansing first and make the Corrupted rest save only if it remains.",
      "stacking": "Corrupted does not stack with itself. Apply the generic half-healing reduction once; an effect does not halve again merely because it restates the same Corrupted penalty.",
      "immunitiesAndOverrides": "Natural-20 death-save recovery and recovered Stable 1-HP recovery are state-recovery rules rather than healing effects and still restore exactly 1 HP. Explicit cleansing or protection may override within scope.",
      "provisionalDecisions": [
        "NEW: round half healing down once; guaranteed death-save/Stable one-HP state recovery is not a healing effect.",
        "Source-grounded: individual recorded alignment or Evil tag only; no ancestry/faction inference, forced behavior or automatic conduct violation.",
        "NEW: generic cleansing project supplies a finite recovery route."
      ],
      "openDependencies": [
        "Cross-check separately reviewed corruption-sensitive transformations and specific restoration effects."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 737,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "dazed",
      "name": "Dazed",
      "coreText": "Choose either action or movement on the turn, not both; no bonus action.",
      "compatibleV6Details": [],
      "sourceConflicts": [],
      "effect": "On every affected turn, including extra turns, choose Action-mode (at most one Action total and no voluntary Speed expenditure or Dash) or Movement-mode (ordinary movement, no Action). Movement expressly included in the permitted Action still resolves. No Bonus Action; Reactions and concentration are unaffected.",
      "application": "Only an effect that explicitly inflicts Dazed applies it.",
      "durationAndEnding": "Use the applying effect's endpoint. Applies immediately: earlier voluntary movement that turn forbids further Actions; an earlier Action forbids further voluntary Speed expenditure; if both already occurred, neither may occur again. Do not undo completed events. Extra-Action grants cannot bypass the one-Action ceiling.",
      "stacking": "Multiple Dazed applications do not further reduce the turn; track only the longest/independent ending sources.",
      "immunitiesAndOverrides": "An immunity to Dazed blocks application. Forced movement is not voluntary movement and remains possible.",
      "provisionalDecisions": [
        "NEW: immediate mid-turn handling, each extra turn gets its own mode, one-Action ceiling, explicit action-contained movement exception."
      ],
      "openDependencies": [
        "Interaction with future nonstandard action types if any are introduced."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 739,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "deafened",
      "name": "Deafened",
      "coreText": "Cannot hear and fails hearing checks; verbal coordination may fail.",
      "compatibleV6Details": [
        "V6 matches inability to hear and automatic failure of hearing-required checks."
      ],
      "sourceConflicts": [],
      "effect": "The creature cannot hear and automatically fails checks that require hearing. It cannot satisfy a rule that specifically requires hearing another creature's command, warning, chant or audible signal.",
      "application": "Only effects that explicitly inflict Deafened apply it.",
      "durationAndEnding": "Use the applying effect's duration/end condition.",
      "stacking": "Multiple applications do not compound.",
      "immunitiesAndOverrides": "Deafened does not prevent the creature from speaking or supplying its own verbal components unless another condition such as Silenced applies.",
      "provisionalDecisions": [
        "Operational clarification: 'verbal coordination may fail' means hearing-dependent coordination requirements fail; no generic roll is added."
      ],
      "openDependencies": [
        "Future command/audible-coordination features must state whether hearing is required."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 741,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "exhausted",
      "name": "Exhausted",
      "coreText": "Use the six-level exhaustion track; effects are cumulative and level 6 is death.",
      "compatibleV6Details": [
        "Level 1: disadvantage on ability checks.",
        "Level 2: Speed halved.",
        "Level 3: disadvantage on attack rolls and saving throws.",
        "Level 4: hit point maximum halved.",
        "Level 5: Speed reduced to 0.",
        "Level 6: death."
      ],
      "sourceConflicts": [],
      "effect": "Track 0-6 cumulative levels: 1 disadvantage ability checks; 2 half Speed after flat changes; 3 disadvantage attacks and saves; 4 maximum HP max(1,floor(otherwise-applicable maximum/2)); 5 Speed zero; 6 death.",
      "application": "An effect that grants one or more Exhaustion levels increases the track by that amount, maximum 6, unless it explicitly sets a level instead.",
      "durationAndEnding": "Eligible beneficial eight-hour long rest removes one level under CONDITION_RECOVERY_PLAYTEST.md, at most one generic removal per 24 hours. Source-specific prerequisites can block removal. Meeting a prerequisite such as Moisture Dependency immersion does not itself remove a level unless printed.",
      "stacking": "Levels add, maximum 6. Derive level-4 maximum from the otherwise-applicable current maximum, never a previously halved value. Clamp HP down when maximum decreases; raising maximum does not heal. Level-5 zero Speed overrides halving.",
      "immunitiesAndOverrides": "An explicit Exhaustion immunity blocks levels. Removing Exhaustion from a dead level-6 creature does not restore life; resurrection is still required.",
      "provisionalDecisions": [
        "NEW: maximum-HP floor1, recomputation/clamping and flat-Speed-before-halving order.",
        "NEW: finite generic long-rest recovery; source-specific removal blocks remain.",
        "Recovered V6: six cumulative level effects."
      ],
      "openDependencies": [],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 743,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "frightened",
      "name": "Frightened",
      "coreText": "Disadvantage while source is visible and cannot willingly move closer.",
      "compatibleV6Details": [
        "V6 specifies disadvantage on ability checks and attack rolls while the source of fear is within line of sight, and prohibits willingly moving closer."
      ],
      "sourceConflicts": [],
      "effect": "While the source of fear is visible/in line of sight, the creature has disadvantage on ability checks and attack rolls. While Frightened it cannot willingly move closer to that source.",
      "application": "Each application records its fear source.",
      "durationAndEnding": "Use the applying effect's duration and repeat-save procedure.",
      "stacking": "Separate fear sources are tracked independently. Disadvantage does not stack.",
      "immunitiesAndOverrides": "Fear immunity blocks application. Forced movement may move the creature closer because the prohibition is on willing movement.",
      "provisionalDecisions": [],
      "openDependencies": [],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 745,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "grappled",
      "name": "Grappled",
      "coreText": "Speed 0; ends if grappler is incapacitated or reach is broken.",
      "compatibleV6Details": [
        "V6 adds that the creature cannot benefit from bonuses to Speed and confirms ending when the grappler is incapacitated or an effect removes the target from reach."
      ],
      "sourceConflicts": [],
      "effect": "Speed becomes 0 and cannot be increased by bonuses while Grappled.",
      "application": "A Grappled application records the grappler/source and its reach.",
      "durationAndEnding": "Ends if the grappler becomes Incapacitated, the grappled creature leaves the grappler's reach, or the applying effect's printed escape/end procedure succeeds. Under the existing shared playtest grapple rule, an otherwise unspecified escape uses an Action and STR (Athletics) or DEX (Acrobatics) against the source DC.",
      "stacking": "Multiple grapplers may maintain separate Grappled records; Speed remains 0 until all relevant grapples end.",
      "immunitiesAndOverrides": "A creature immune to Grappled cannot receive it. Teleportation or forced movement that breaks reach ends that grapple unless a specific effect says otherwise.",
      "provisionalDecisions": [],
      "openDependencies": [
        "Final generic grapple/shove procedure remains part of the combat maneuver audit."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 747,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "incapacitated",
      "name": "Incapacitated",
      "coreText": "Cannot take actions or reactions.",
      "compatibleV6Details": [
        "V6 matches: cannot take actions or reactions."
      ],
      "sourceConflicts": [],
      "effect": "The creature cannot take an Action, Bonus Action or Reaction. Passive effects continue unless their own rules require consciousness or another condition disables them. Incapacitated by itself does not reduce Speed or prohibit speech.",
      "application": "Applied by a condition or effect that explicitly says the creature is Incapacitated.",
      "durationAndEnding": "Use the parent condition/effect's duration.",
      "stacking": "Does not stack.",
      "immunitiesAndOverrides": "Current shared concentration rules end concentration immediately when the creature becomes Incapacitated. A specific effect may preserve a passive benefit through Incapacitation if explicitly stated.",
      "provisionalDecisions": [
        "NEW integration: Bonus Actions are included in unavailable actions.",
        "Already explicit in CLASS_PLAYTEST_RULES.md: becoming Incapacitated ends concentration."
      ],
      "openDependencies": [],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 749,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "intoxicated",
      "name": "Intoxicated",
      "coreText": "Disadvantage on precise Dexterity and Intelligence checks; advantage on one save against fear. Stacks worsen into Dazed and Unconscious.",
      "compatibleV6Details": [
        "Existing Intoxication Track: 0 Sober; 1 Relaxed with advantage on one fear save and disadvantage on precise memory checks; 2 Intoxicated condition; 3 Dazed and Speed -10 ft; 4 Unconscious for 1d4 hours plus Constitution save against poisoning; 5 medical emergency, gain a Wound or die without treatment at Director discretion."
      ],
      "sourceConflicts": [],
      "effect": "Use the single0-5 Intoxication track and procedures in CONDITION_RECOVERY_PLAYTEST.md. Level1 grants one fear-save advantage use per continuous nonzero episode and disadvantage precise-memory checks; level2 additionally gives disadvantage precise DEX/INT checks; level3 additionally Dazed and Speed-10; levels4/5 additionally Unconscious and their poisoning/emergency procedures.",
      "application": "Only explicit intoxication gains advance the track. Direct Intoxicated sets at least2; an explicit short duration can create a separately timed application as described in the recovery guide. No bonus level merely from an alcoholic item's name.",
      "durationAndEnding": "Use the hourly sobriety, level4 timer or level5 emergency procedure, or an explicit reviewed cure. Full details including direct timed applications are in CONDITION_RECOVERY_PLAYTEST.md.",
      "stacking": "One track. One fear-save advantage use for the entire episode until level0, never refreshed by moving between positive levels. Other independent Dazed/Unconscious/Poisoned sources remain after intoxication recovers.",
      "immunitiesAndOverrides": "An effect explicitly preventing intoxication blocks track gain. Unconscious at level 4 uses the normal Unconscious condition.",
      "provisionalDecisions": [
        "NEW: cumulative condition thresholds, direct-application floor and continuous-episode fear-save limit.",
        "NEW: finite sobriety, poisoning and medical-emergency procedures; source values/conditions preserved."
      ],
      "openDependencies": [
        "Individual brew/substance cards still need their complete dose, access and balance audit."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 751,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "invisible",
      "name": "Invisible",
      "coreText": "Cannot be seen normally; attacks against it have disadvantage and its attacks have advantage until location is revealed.",
      "compatibleV6Details": [
        "V6: impossible to see without special senses or magic; heavily obscured for hiding; location may be detected by noises or tracks; attacks against have disadvantage and own attacks have advantage."
      ],
      "sourceConflicts": [
        "Core explicitly ends the generic attack advantage/disadvantage when location is revealed; V6 states those attack modifiers without that endpoint. Core controls the conflict."
      ],
      "effect": "Cannot be seen normally. Until an observer knows its location, that observer attacks it with disadvantage and it attacks that observer with advantage. Once location is revealed, these Invisible-specific modifiers end for that observer. Do not re-grant them through V6 generic unseen rules solely because it is still Invisible. A special sense actually seeing it bypasses these modifiers. Knowing location is not seeing; effects requiring sight still need sight.",
      "application": "Only an effect explicitly granting Invisible applies it.",
      "durationAndEnding": "Use the granting effect's duration. V6 attacks reveal location upon attacking; resolve the revealing attack first, then observers able to perceive evidence know the location. Independent hiding/concealment uses its own procedure; later broad vision integration must specify losing and regaining location knowledge. Invisible remains visually effective after revelation.",
      "stacking": "Multiple Invisible effects do not stack.",
      "immunitiesAndOverrides": "A special sense or magic that actually sees the creature removes Invisible's unseen benefits for that observer within that sense's scope. Knowing location is not the same as seeing.",
      "provisionalDecisions": [
        "Operational distinction: visibility state and known location are separate.",
        "No generic detection DC, automatic attack-reveal rule or movement-rehide rule is invented here.",
        "Recovered V6: attacking reveals location. NEW timing clarification: resolve that attack before its revelation; Core location endpoint specifically overrides the otherwise-conflicting unseen attack modifiers."
      ],
      "openDependencies": [
        "Stealth, sound, tracks, hiding and location-reveal procedure in the vision/stealth pass."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 753,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "marked",
      "name": "Marked",
      "coreText": "A named creature or faction can track, target, or trigger abilities against the marked creature.",
      "compatibleV6Details": [],
      "sourceConflicts": [],
      "effect": "Marked establishes a source-specific relationship between the marked creature and one named creature, faction or effect. It makes the target eligible only for tracking, targeting or trigger rights explicitly printed by that reviewed source.",
      "application": "Every application records marker source/faction, the granting ability or rule, and any rights/duration printed there.",
      "durationAndEnding": "Use the applying source's duration/end rule. If none is supplied, that Marked application remains incomplete and should not be activated until its source is reviewed.",
      "stacking": "Marks from different named sources may coexist. Reapplying the same mark refreshes/replaces according to that source. Generic Marked supplies no additive numerical bonus.",
      "immunitiesAndOverrides": "An effect preventing marks blocks application within scope.",
      "provisionalDecisions": [
        "NEW integration: Marked alone grants no universal location knowledge, global tracking bonus, damage bonus or permission to bypass cover/planar boundaries."
      ],
      "openDependencies": [
        "Individual mark-producing features must define their specific rights."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 755,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "paralyzed",
      "name": "Paralyzed",
      "coreText": "Incapacitated, cannot move or speak, fails Strength/Dexterity saves, adjacent hits are critical.",
      "compatibleV6Details": [
        "V6 adds attack rolls against the creature have advantage and specifies attacks that hit from within 5 feet are critical."
      ],
      "sourceConflicts": [],
      "effect": "The creature is Incapacitated, cannot move or speak, automatically fails Strength and Dexterity saving throws, attack rolls against it have advantage, and any attack that hits it from within 5 feet is a critical hit.",
      "application": "Only an effect explicitly inflicting Paralyzed applies it.",
      "durationAndEnding": "Use the applying effect's duration and repeat-save/ending procedure.",
      "stacking": "Does not stack.",
      "immunitiesAndOverrides": "Paralysis immunity blocks application. Incapacitated consequences, including loss of Bonus Action/Reaction and concentration ending under the shared rule, apply.",
      "provisionalDecisions": [],
      "openDependencies": [],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 757,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "petrified",
      "name": "Petrified",
      "coreText": "Incapacitated stone-like state; resistance to damage, immunity to poison/disease, weight ×10.",
      "compatibleV6Details": [
        "V6: transformed into inanimate substance, weight ×10, cease aging, Incapacitated, cannot move/speak, unaware, attacks against have advantage, automatically fails Strength/Dexterity saves, resistance to all damage, immunity to poison and disease, existing poison/disease suspended rather than neutralized."
      ],
      "sourceConflicts": [
        "Core damage rules separately state Corruption damage cannot be resisted unless an effect explicitly protects against Corruption. Petrified does not explicitly name Corruption."
      ],
      "effect": "The creature becomes an inanimate stone-like substance, weight ×10, ceases aging, is Incapacitated, cannot move or speak, is unaware, automatically fails Strength and Dexterity saves, and attacks against it have advantage. It has resistance to all damage except Corruption damage, and immunity to poison and disease; existing poison/disease effects are suspended rather than removed.",
      "application": "Only an effect explicitly inflicting Petrified applies it.",
      "durationAndEnding": "Use the applying effect's duration/removal rule. Suspended poison/disease resumes if Petrified ends and the underlying effect has not otherwise expired or been cured.",
      "stacking": "Does not stack.",
      "immunitiesAndOverrides": "Petrification immunity blocks application. Corruption resistance is not granted because the special Core Corruption rule requires explicit Corruption protection.",
      "provisionalDecisions": [
        "Integration ruling: generic all-damage resistance from Petrified does not satisfy Core's explicit-protection requirement for Corruption."
      ],
      "openDependencies": [
        "Interaction with aging clocks and object-targeting effects belongs to later environment/item passes."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 759,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "poisoned",
      "name": "Poisoned",
      "coreText": "Disadvantage on attacks and ability checks.",
      "compatibleV6Details": [
        "V6 matches exactly."
      ],
      "sourceConflicts": [],
      "effect": "The creature has disadvantage on attack rolls and ability checks.",
      "application": "Only an effect explicitly inflicting Poisoned applies it.",
      "durationAndEnding": "Use the applying effect's duration/removal rule.",
      "stacking": "Multiple Poisoned applications do not stack disadvantage; independent durations may coexist.",
      "immunitiesAndOverrides": "Poisoned immunity blocks application. Poison damage resistance alone does not imply Poisoned immunity unless stated.",
      "provisionalDecisions": [],
      "openDependencies": [],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 761,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "prone",
      "name": "Prone",
      "coreText": "Crawl or stand; melee attackers within 5 ft. have advantage; ranged attackers have disadvantage.",
      "compatibleV6Details": [
        "V6: only movement is crawl unless standing; own attack rolls have disadvantage; attacks from within 5 feet have advantage, otherwise disadvantage."
      ],
      "sourceConflicts": [
        "For a ranged attack made from within 5 feet, V6 distance-only wording would grant advantage while Core specifically says ranged attackers have disadvantage. Core controls."
      ],
      "effect": "Own attacks have disadvantage. Melee attacks against it within5 feet have advantage; ranged attacks against it have disadvantage at every distance; other attacks beyond5 feet have disadvantage. Movement requires crawling or standing. Drop Prone without Speed expenditure; standing costs half current Speed, rounded down, requires nonzero Speed and sufficient movement. Crawl costs2 feet per foot, or3 in difficult terrain.",
      "application": "Applied when an effect explicitly knocks a creature Prone or another rule such as Unconscious causes it.",
      "durationAndEnding": "Ends when the creature successfully stands or an explicit effect ends Prone.",
      "stacking": "Does not stack.",
      "immunitiesAndOverrides": "Prone immunity blocks application. A feature may explicitly ignore Prone attack penalties.",
      "provisionalDecisions": [
        "Core-vs-V6 conflict resolved in favor of Core for ranged attacks within 5 feet.",
        "Recovered V6 movement: half-Speed standing and2/3-for1 crawling. NEW explicit zero-Speed standing prohibition, preventing zero-cost standing while Grappled."
      ],
      "openDependencies": [],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 763,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "resonance-burn",
      "name": "Resonance Burn",
      "coreText": "Maximum RP reduced and spell failure risk increases until a long rest or treatment.",
      "compatibleV6Details": [],
      "sourceConflicts": [
        "The current spell pilot explicitly uses Dissonance/Refrain and excludes the historical Burn/fizzle system to avoid stacking two strain engines."
      ],
      "effect": "Preserved source condition only. It is inactive in the current Dissonance-only playtest configuration and therefore applies no numeric RP-cap reduction or spell-failure procedure until separately reviewed.",
      "application": "A feature whose only unresolved consequence is Resonance Burn remains blocked/non-operational in this configuration unless that feature separately defines all needed numbers without invoking the historical Burn engine.",
      "durationAndEnding": "Source says until a long rest or treatment when active; exact treatment remains part of the historical Burn review.",
      "stacking": "No stacking procedure is active in the current configuration.",
      "immunitiesAndOverrides": "A reviewed configuration may explicitly enable Resonance Burn instead of or alongside another strain model, but that requires a separate decision.",
      "provisionalDecisions": [
        "Pilot decision: preserve but do not execute Resonance Burn while Dissonance/Refrain is the active strain system."
      ],
      "openDependencies": [
        "An individual card invoking unresolved historical Burn is not operational until separately adapted and reviewed; no universal second failure engine is active."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 765,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "preserved; inactive in this Dissonance configuration",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "restrained",
      "name": "Restrained",
      "coreText": "Speed 0; attacks against have advantage, own attacks and Dexterity saves have disadvantage.",
      "compatibleV6Details": [
        "V6 adds that the creature cannot benefit from bonuses to Speed."
      ],
      "sourceConflicts": [],
      "effect": "Speed becomes 0 and cannot benefit from Speed bonuses. Attack rolls against the creature have advantage; its own attack rolls and Dexterity saving throws have disadvantage.",
      "application": "Only an effect explicitly inflicting Restrained applies it.",
      "durationAndEnding": "Use the applying effect's printed duration, save or escape rule. If an effect creates a physical restraint and provides no escape procedure, use the existing shared playtest escape procedure only if that source is eligible for it.",
      "stacking": "Multiple Restrained applications do not compound penalties, but all independently maintained sources must end before the creature is no longer Restrained.",
      "immunitiesAndOverrides": "Restrained immunity blocks application. Teleportation does not automatically end a restraint unless it breaks the source relationship or the applying effect says so.",
      "provisionalDecisions": [],
      "openDependencies": [
        "Final generic physical-restraint escape procedure in combat rules."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 767,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "silenced",
      "name": "Silenced",
      "coreText": "Cannot use verbal components, command words, Chants, or audible coordination.",
      "compatibleV6Details": [],
      "sourceConflicts": [],
      "effect": "The creature cannot use spell/ability verbal components, command words, Chants, or any feature requiring audible coordination. It may still think, perceive, move, use somatic/nonverbal abilities and use effects that explicitly function without sound.",
      "application": "Only effects explicitly inflicting Silenced apply it.",
      "durationAndEnding": "Use the applying effect's duration/end rule.",
      "stacking": "Does not stack.",
      "immunitiesAndOverrides": "An ability explicitly usable without speech or audible sound is unaffected. Silence immunity blocks application only if explicitly defined.",
      "provisionalDecisions": [
        "Clarification: Silenced is not universal mental or magical shutdown."
      ],
      "openDependencies": [
        "Specific audible-command features must state whether they require being heard by recipients."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 769,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "staggered",
      "name": "Staggered",
      "coreText": "Cannot react, loses Guard, and the next forced movement gains +5 ft. Ends at start of next turn.",
      "compatibleV6Details": [],
      "sourceConflicts": [],
      "effect": "Cannot take Reactions. Remove current Guard: its unused +2 AC against the first attack and enabled Interpose end. Guard cannot be gained while Staggered. The next otherwise-legal forced-movement event before expiry gains5 feet in the same direction, once; solid obstacles still stop it.",
      "application": "Only an effect explicitly inflicting Staggered applies it.",
      "durationAndEnding": "Ends at the start of the affected creature's next regular turn. The +5-foot rider is consumed by the first qualifying forced movement or expires unused.",
      "stacking": "Duplicate applications do not add multiple5-foot riders. Later application can refresh the endpoint but cannot refresh a consumed rider while continuously Staggered. A new condition episode after it fully ends may grant a new rider.",
      "immunitiesAndOverrides": "Forced movement still obeys obstacle, solid-matter and legality rules. A feature explicitly preventing forced movement can negate the movement despite Staggered.",
      "provisionalDecisions": [
        "NEW endpoint clarification: 'next turn' means the affected creature's next regular turn.",
        "NEW: +5 feet is consumed once.",
        "Core Guard paragraph394: +2 AC against first attack before next turn and enable Interpose. NEW: Guard removed rather than paused, cannot regain during Staggered; consumed rider not refreshed by reapplication."
      ],
      "openDependencies": [
        "Full Guard/Interpose action review remains in combat; this condition now names the existing Guard benefits it removes."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 771,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "stunned",
      "name": "Stunned",
      "coreText": "Incapacitated, cannot move, fails Strength/Dexterity saves, attacks against have advantage.",
      "compatibleV6Details": [
        "V6 adds that the creature can speak only falteringly."
      ],
      "sourceConflicts": [],
      "effect": "The creature is Incapacitated, cannot move, automatically fails Strength and Dexterity saving throws, attack rolls against it have advantage, and it can speak only falteringly.",
      "application": "Only an effect explicitly inflicting Stunned applies it; source-character hard-denial limits remain separate application rules.",
      "durationAndEnding": "Use the applying effect's duration/repeat-save procedure.",
      "stacking": "Does not stack.",
      "immunitiesAndOverrides": "Stun immunity blocks application. Incapacitated consequences apply, including no Bonus Action/Reaction and concentration ending under the shared rule.",
      "provisionalDecisions": [],
      "openDependencies": [],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 773,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "unconscious",
      "name": "Unconscious",
      "coreText": "Incapacitated, unaware, drops held items, falls Prone, adjacent hits are critical.",
      "compatibleV6Details": [
        "V6 adds cannot move or speak, automatically fails Strength/Dexterity saves, attacks against have advantage, and any hit from within 5 feet is critical."
      ],
      "sourceConflicts": [],
      "effect": "The creature is Incapacitated, unaware of surroundings, cannot move or speak, drops held items, falls Prone, automatically fails Strength and Dexterity saving throws, attack rolls against it have advantage, and any attack that hits from within 5 feet is a critical hit.",
      "application": "Applied by effects explicitly causing Unconscious, including the active 0-HP rules.",
      "durationAndEnding": "Use the causing rule's endpoint. Healing above 0 ends only Unconscious caused solely by the 0-HP state; it does not remove an independent Unconscious effect.",
      "stacking": "Multiple causes may coexist; the creature remains Unconscious until all relevant causes end.",
      "immunitiesAndOverrides": "An immunity to Unconscious blocks applicable external effects but does not necessarily override death/0-HP rules unless explicitly stated. Incapacitated consequences apply.",
      "provisionalDecisions": [],
      "openDependencies": [],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 775,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "unity-exposure",
      "name": "Unity Exposure",
      "coreText": "Track exposure from 0-6. At thresholds, distinctions, memories, loyalties, and eventually identity begin to erode.",
      "compatibleV6Details": [],
      "sourceConflicts": [],
      "effect": "Use the provisional public score0-6 table in CONDITION_RECOVERY_PLAYTEST.md:0/1 no generic penalty;2 -1 specific distinction Perception/Investigation;3 -1 INT/WIS checks;4 -1 INT/WIS/CHA checks;5 disadvantage those checks;6 disadvantage those checks and saves. Use current row only. Player agency remains.",
      "application": "Only explicit effects such as reviewed substances, hazards or Director mechanics may alter Unity Exposure.",
      "durationAndEnding": "Persists; only an explicit reviewed effect or successful three-day Anchor Project changes the score. Ordinary rest does not clear it.",
      "stacking": "Exposure changes modify the single 0-6 track; cap at 6 unless an authoritative source explicitly allows another state.",
      "immunitiesAndOverrides": "An effect explicitly preventing Unity Exposure blocks only the exposure it covers.",
      "provisionalDecisions": [
        "NEW provisional public threshold/recovery mechanics, discussed with GPT; not recovered canon.",
        "Public score does not imply knowledge of hidden causes, truths, involuntary beliefs or identity deletion. Director handling remains separately packaged."
      ],
      "openDependencies": [
        "Review all Unity application sources and Director narrative threshold material separately; no source-approved numeric threshold table was recovered in the bounded searches."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 777,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "withdrawal",
      "name": "Withdrawal",
      "coreText": "Disadvantage on ability checks and RP recovery; severity depends on substance and duration of dependence.",
      "compatibleV6Details": [
        "Dependence source: user needs a dose after each long rest or gains Withdrawal; treatment may use Medicine, Religion, Alchemy or a recovery project, while magic can remove symptoms without necessarily removing dependence."
      ],
      "sourceConflicts": [
        "Current Retune is deterministic and has no RP-recovery roll on which disadvantage can operate."
      ],
      "effect": "The creature has disadvantage on ability checks. If an RP-recovery procedure actually calls for a roll, that recovery roll has disadvantage. The current deterministic Retune formula receives no invented numeric penalty from this wording. Oracle Revelation Charges are not RP and are unaffected.",
      "application": "Applied for a named substance when its Addicted maintenance requirement is missed or another source explicitly inflicts Withdrawal. Record the substance/source separately.",
      "durationAndEnding": "A legal maintenance dose suppresses that substance's symptoms for its current maintenance interval without removing Addicted. Reviewed symptom relief follows its printed duration. A successful dependence recovery project removes both named dependence and its Withdrawal. The generic condition has no extra numerical severity levels; a substance adds severity only where its reviewed card defines it.",
      "stacking": "Separate substance Withdrawal records may coexist, but disadvantage on ability checks applies only once. Severity does not numerically stack unless a substance-specific rule defines it.",
      "immunitiesAndOverrides": "An effect explicitly preventing Withdrawal symptoms suppresses the condition within its scope but need not remove Addicted.",
      "provisionalDecisions": [
        "NEW: a maintenance dose can end current Withdrawal symptoms while dependence persists.",
        "Integration decision: deterministic Retune is not numerically altered because 'disadvantage' has no roll to modify.",
        "Oracle RC explicitly remains outside an RP-only condition."
      ],
      "openDependencies": [
        "Review substance-specific additions individually; do not infer penalties for deterministic RP recovery or Oracle RC."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 779,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    },
    {
      "id": "wounded",
      "name": "Wounded",
      "coreText": "Each Wound imposes -1 Constitution saves and reduces Hit Dice recovery; three Wounds is Critical.",
      "compatibleV6Details": [],
      "sourceConflicts": [
        "V6 Appendix has a separate temporary Wounded condition: cannot regain HP except magical healing/long rest, disadvantage Constitution saves, damage at 0 causes one death-save failure, ends on magical healing/long rest. Core owns this conflict for the current candidate, so that V6 temporary package is preserved but inactive."
      ],
      "effect": "Use the existing Core Wound records from the reviewed HP/Wound overlay. Each Wound gives -1 Constitution saving throws and reduces maximum Hit Dice recovered per long rest by 1. At three Wounds the creature is Critically Wounded under that overlay's Speed, healing-ceiling and failed-Wound-save rules.",
      "application": "Wounds are gained only through the active Wound-trigger/save system or an effect explicitly granting a Wound. Do not separately add a second condition penalty merely because a source labels the creature Wounded.",
      "durationAndEnding": "Each Wound persists until a reviewed treatment or effect removes that Wound. Removing a Wound also removes its linked Injury. Leaving three Wounds ends Critical state under the existing overlay.",
      "stacking": "Wound records stack numerically according to Core. The current overlay allows 0-3 living Wounds; a failed Wound save begun at three Wounds is fatal instead of creating a fourth.",
      "immunitiesAndOverrides": "An effect explicitly preventing Wounds blocks only qualifying Wound gain within scope. Ordinary HP healing does not remove Wounds unless it explicitly says so.",
      "provisionalDecisions": [
        "Integration decision already reviewed: Core Wound records are the active meaning of Wounded in this candidate; the conflicting V6 temporary Wounded package is inactive and does not double-apply penalties."
      ],
      "openDependencies": [
        "Specific restoration effects that remove Wounds will be cross-checked during spell/item/condition integration."
      ],
      "source": {
        "path": "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx",
        "sha256": "53db5a16af10bc351e1f59a8af6d4201579962a21fc61b9bf6e27255b11ee433",
        "paragraph": 781,
        "paragraphIndex": "zero-based all w:p descendants"
      },
      "configuration": "active provisional overlay",
      "reviewEvidence": [
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_FIRST_REVIEW.md",
        "docs/audit/2026-10-08/full-game/GPT_CONDITIONS_SECOND_REVIEW.md"
      ]
    }
  ]
}


EXACT recovery guide:
# Condition recovery and exposure — provisional procedures

**Draft awaiting final adversarial review.** These are fictional game procedures. The sources provide the condition identities, existing dose/tolerance rules, six Exhaustion levels and Intoxication thresholds; the exact generic recovery projects and missing endpoints below are newly authored proposals discussed with GPT. Preserve the original sources. Use with [all 28 conditions](CONDITIONS_PLAYTEST.md) and [HP, Wounds and death](CORE_RESOLUTION_PLAYTEST.md).

## Time, costs and checks

A project day is a consecutive 24-hour interval starting when that project begins, not a calendar-date change. A three-day project finishes no earlier than 72 elapsed hours; seven days means at least 168 hours. Only one project of the same kind for the same patient and named condition may be active. Concurrent clocks measure the same elapsed time once; the same active hour or consumed Supply cannot pay two activities. An active practitioner cannot simultaneously perform a long rest. A patient can receive care while resting where the care permits it.

Consume each stated Supply or kit use at the beginning of its attempt or daily work. Interruption does not refund it. Missing a required project day, taking a forbidden dose or receiving forbidden new Exposure ends that attempt; completed costs remain spent, and starting again requires a fresh full project. Merely suppressing symptoms does not interrupt abstinence or time already properly completed.

Project skill checks use the reviewed four-degree task rules. Success and Critical Success give the stated success; Failure and Critical Failure give the stated failure unless specifically differentiated. No extra reward or complication is inferred from an undefined degree. Saving throws remain binary. Use WIS (Medicine), INT (Religion), INT (Arcana), or an INT check using proficiency with alchemist's supplies for Alchemy. These ability/tool assignments are explicit integration choices; an actual feature can supply its printed alternative.

## Exhaustion

The six V6 effects are cumulative: level 1 disadvantage on ability checks; 2 Speed halved; 3 disadvantage on attack rolls and saves; 4 maximum HP halved; 5 Speed zero; 6 death. Compute level-4 maximum as `max(1, floor(otherwise-applicable maximum HP / 2))`. Recompute from the otherwise-applicable maximum whenever it changes. Clamp current HP when the maximum falls; restoring the maximum does not heal. Flat Speed changes apply before halving; a zero-Speed condition overrides the calculation. A maximum-HP reduction alone is not damage and does not trigger a Wound save.

**NEW generic recovery:** At the end of a beneficial eight-hour long rest, remove one Exhaustion level from a living creature at levels 1–5 if it met the campaign's food/water requirements, the originating cause no longer actively imposes or refreshes Exhaustion, and no source-specific rule blocks removal. At most one generic level can be removed per 24 elapsed hours. Specific reviewed effects can remove additional levels as printed. A prerequisite such as Moisture Dependency's one-hour immersion unlocks recovery; it does not itself remove a level unless explicitly stated. Track blocked-source levels separately so another source's removable level may still be selected; the patient chooses a legal level to remove.

Exhaustion 6 causes death. Removing levels from the corpse never revives it. A resurrection effect must also leave the creature below 6 or it immediately dies again. Global Exhaustion, expedition Strain, and Oracle's one-turn Revelation backlash remain separate records; this procedure does not clear the other two.

## Dependence and Withdrawal

Preserve Core's existing substance procedures: resolve benefit and crash; a repeat dose before the next long rest requires the substance's dependence CON save; three uses within seven days cause tolerance that halves duration unless doubled; more than two doses before a long rest triggers the substance's severe complication and dependence advancement. This document supplies endpoints, not a replacement substance catalog. Use each item's reviewed dependence DC and severe complication. An item lacking its actual consequence remains in the item review queue rather than gaining an invented generic overdose result.

**Maintenance:** At each completed long rest, a new maintenance dose is due for each named dependence. Withdrawal applies immediately until a qualifying dose is taken after that rest; a dose taken before its completion cannot satisfy the new interval. The dose ends that substance's current symptoms until the next maintenance interval but does not remove dependence. Ordinary consumption time, stock, crash, tolerance and repeated-dose rules still apply. No free dose or Action is granted.

**Tolerance:** Record doses in a rolling seven-day window. The third dose is the first tolerant dose. Count a doubled dose as two doses for tolerance, repeated-dose and overdose accounting; resolve its two-dose thresholds as one consumption event, with at most one dependence save for that event. Seven full days with no dose clears tolerance. One long rest does not clear tolerance. Track each substance separately.

**NEW dependence recovery project:** Complete seven consecutive project days without a dose of the named substance. Each day the patient spends one hour in treatment/recovery work and consumes one Supply. Choose Medicine, Religion or Alchemy at project start. At the end of the seventh full day, the designated practitioner (who may be the patient) makes that check against the substance's dependence DC, or NEW DC 14 if a direct Addicted effect supplied no substance DC. Success removes that named Addicted and its associated Withdrawal. Failure removes neither; a new attempt needs a new seven-day project. There is no extra automatic Wound on Critical Failure.

The existing Haven activity “Treat Dependence or Withdrawal” gives advantage on the next recovery check and prevents one ordinary withdrawal escalation after one full day under qualified care. For this bridge, a proficient practitioner spends an eight-hour care activity during a project day; that day's one-hour treatment requirement is included, not additional. Advantage applies once to the next recovery check and cannot be stockpiled. Different sources of advantage still do not stack. The activity does not independently cure dependence or erase a dose's printed crash.

Withdrawal imposes disadvantage on ability checks. “Disadvantage on RP recovery” affects an actual RP recovery roll only; deterministic Retune receives no invented arithmetic penalty. Oracle RC is not RP. The generic Withdrawal condition has no further severity track. An individual substance can add an explicitly reviewed duration or escalation; otherwise do not invent one. Symptom-removal magic does not remove dependence unless it explicitly does, but valid symptom suppression is compatible with completing a no-dose project.

## Intoxication

Use one dose-driven score from 0 to 5. Increase it only when an effect explicitly grants Intoxication. A direct effect saying “Intoxicated” supplies a minimum effective score of 2 for its printed duration; if no duration is given, set the dose-driven score to at least 2. A timed direct application does not itself count as a dose or grant repeated increases. Effective score is the greater of the dose-driven score and active direct-application floors. Resolve threshold entries when effective score increases. Removing a direct floor does not erase independent dose-driven points or other sources' conditions.

| Score | Consequence |
|---|---|
| 0 | Sober; no Intoxication consequence. |
| 1 | Disadvantage on precise-memory checks. One available advantage use on a fear save. |
| 2 | Also disadvantage on precise DEX and INT checks. |
| 3 | Also Dazed and Speed −10 feet. |
| 4 | Also Unconscious for the level-4 timer and a poisoning save. |
| 5 | Also a medical emergency with a fixed one-hour deadline. |

The rows are cumulative. The Director identifies a “precise” check before rolling: fine manipulation or exact memory/analysis, not every possible use of DEX/INT. The player may spend the one fear-save advantage use before rolling. It refreshes only after effective score reaches 0 and a later new episode begins, never at each positive level. An explicit independent Dazed, Unconscious or Poisoned effect is not removed merely because intoxication ends.

**NEW natural reduction:** At dose-driven scores 1–3, one complete hour without new Intoxication removes one point; repeat each hour. A new positive gain resets that hourly timer even if a direct floor conceals the dose-driven change. A timed floor itself does not stop underlying points declining. At score 4 use its specific timer; score 5 cannot decay naturally. After a reduction to 3 or below, begin the next hourly interval at that transition. A timed floor can prevent the effective score from dropping until that application ends.

**NEW level 4:** On entering effective score 4 (or returning from treated 5), roll 1d4 once and set that many hours as the recovery deadline. Make a DC 14 CON save; on failure add Poisoned caused by intoxication while effective score is at least 4. Unconscious from this track lasts until that deadline unless cured earlier. Ending Unconscious alone does not clear points or reset the deadline. Reapplying score 4 without leaving it does not reroll or extend the deadline. At its deadline, if alive and no emergency is active, reduce dose-driven score to at most 3 and end track-caused Unconscious/Poisoned. If a direct timed floor still holds effective score at 4, its Unconscious/Poisoned consequences remain until the floor ends; do not reroll timers. A generic cure explicitly ending Intoxication removes all its track/floor records and track-caused consequences.

**NEW level 5:** On entering effective score 5, set a fixed emergency deadline one hour later and remain Unconscious. Additional gains at 5 never reset or extend it. A helper may spend ten uninterrupted minutes and one healer's-kit use, consumed at start, then make DC 15 WIS (Medicine). Success before the deadline ends the emergency, sets the dose-driven score to 4, clears any direct floor of 5 from this episode, adds one Wound if below three, and begins the level-4 timer/save. At three Wounds, successful emergency care prevents death without creating a fourth Wound; this is a specific provisional exception for this treatment. This direct Wound has no Injury roll and does not itself trigger a Wound save. Wound immunity prevents that added Wound where applicable.

Failure leaves the original emergency and deadline; another fully paid attempt is possible if it can finish before that deadline. At the exact deadline, death takes precedence over an unfinished or simultaneously finishing generic attempt. No natural score reduction can clear the emergency. A reviewed effect explicitly removing Intoxication or the emergency can end it by its own procedure. An immunity to Unconscious or Poisoned does not, by itself, prevent the separate emergency or death state.

## Corrupted

Use the condition's half healing, individually recorded Evil-source save disadvantage, aura and DC 15 WIS long-rest save. A failed long-rest save shifts the moral axis Good → Neutral → Evil without changing law/chaos. Never infer Evil from ancestry, species, faction, homeland or appearance. This label change does not compel beliefs, behavior, PvP, party separation or automatic oathbreaking. Specific conduct clauses still judge actual conduct.

**NEW generic cleansing:** One practitioner spends eight uninterrupted hours with one patient in a secure location, consumes one Supply at start, and makes INT (Religion) or INT (Arcana) against DC 15 at completion. Success removes Corrupted. Failure leaves it without any extra automatic Wound, condition or Exposure. No more than one generic attempt may complete for that patient in 24 elapsed hours; practitioners cannot stack concurrent attempts. The practitioner is working, while the patient may rest if otherwise eligible. If cleansing and the patient's long rest complete together, resolve cleansing first; make the Corrupted rest save only if it remains. A specific reviewed cleansing spell/item uses its own costs and procedure.

Guaranteed one-HP recovery from a natural-20 death save or the Stable recovery clock remains one HP: these are state-recovery rules, not healing effects. Ordinary one-point magical healing can still be halved to zero. It nevertheless ends generic Bleeding if it had positive pre-reduction healing potential.

## Unity Exposure — public provisional track

The source defines a 0–6 track with erosion of distinction and identity but no operational numeric threshold table was found in the bounded Core/V6/Director and current reference searches. GPT also reported no owner-approved numerical table in its available notebook history. The following is **NEW candidate mechanics**, not recovered setting truth. It grants no public knowledge of the exposure's hidden causes or identities.

Use the current row only; do not add lower-row modifiers.

| Score | Mechanical effect |
|---|---|
| 0 | No effect. |
| 1 | Tracked, without a generic numerical penalty. |
| 2 | −1 Perception/Investigation checks specifically distinguishing similar identities, copies, duplicates or conflicting sensory impressions. Declare this scope before rolling. |
| 3 | −1 INT and WIS ability checks. |
| 4 | −1 INT, WIS and CHA ability checks. |
| 5 | Disadvantage on INT, WIS and CHA ability checks. |
| 6 | Disadvantage on INT, WIS and CHA ability checks and saves. The character remains playable with player agency. |

Record changes only from explicit reviewed effects; cap at 0–6. These mechanics never decide a character's beliefs, loves, loyalty, factual memories, conduct or hidden revelations. A player can portray blurred memories or identity pressure without surrendering character control.

**NEW Anchor Project:** In a secure Haven or equivalent safe location, complete three full consecutive project days. Each day the patient spends two hours affirming chosen memories, relationships or personal distinctions and consumes one Supply. The player chooses the content. At the end of the third full day, make a WIS save against DC `10 + current Exposure`, including the track's actual penalties. Success reduces Exposure by one; failure does not. A new reduction requires a new full project. Ordinary rest does not reduce Exposure.

Any successful positive Exposure-gain event during the attempt interrupts it, including a gain capped at 6; prevented gains do not. Already consumed Supply remains spent. Only one Anchor Project per patient can be active. Specific reviewed removal effects may work differently. Director context and later source reconciliation remain separately packaged; private narrative information does not silently add numerical penalties or erase player agency.

## Evidence and remaining integration

The exact first and second GPT reviews, Core condition definitions, complete V6 appendix, direct dependency passages, Guard text, and bounded source searches are retained in `docs/audit/2026-10-08/full-game` at the project root. The normalized entries retain exact Core text and book hashes. These generic procedures make recovery playable but do not finish every substance/item, cure spell, encounter hazard, source of Exposure, rest resource or Director scene. Their individual audits remain in the 75-area ledger.
