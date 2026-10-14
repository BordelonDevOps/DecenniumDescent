# Eleven Divination cantrips — exact manuscript review

Please review all eleven exact cards against your source conference, supplied sources and shared rules. Approve or state exact required repairs. Current159/689catalog unchanged until approval. All11placements/Core blocks and actual class access retained. This is tabletop manuscript approval, not effect runtime, numerical balance or whole-game closure. Please keep reply under16,000characters.

Exact-card completions needing particular attention:
- Protection from Scrying is already reviewed (full functional comparator below): it prevents NEW information about the protected creature, including beneficial reading, but is not blanket damage/buff immunity for the school. The common card text carries this distinction. Flicker provides only the roll mechanic, not an extra future-event report; Glimpse has separately protected narrative information versus initiative advantage. Soul Mark may exist on a warded creature but gives no direction while its information is blocked; no automatic deletion/expiry reset. A lack of readable RP aura never proves absence of a protected pool.
- Omen remains one truthful cryptic usable current-circumstances clue. Exact candidate applies materially-equivalent inquiry limit across casters as well as rephrasing/subdivision, so a party cannot extract an entire unchanged plot by passing the cantrip around. No daily cap. If all relevant facts actually protected, no-information omen without ward-name. Please approve this exact shared inquiry scope or repair it.
- Far Echo conference's 'audible at that point within5footradius' needs a single capture predicate. Exact candidate selects speech PRODUCED within the5foot sphere AND audible at its center during6seconds beforecaststart, then plays once with timing/relativevolume. That is a clearly marked exact-card completion; if you intended any speech audible in the area regardless of speaker location, specify the replacement. A current applicable Divination ward can withhold new protected-subject information from retrieval, without deleting past speech facts, ordinary recordings or already-known information. No recursiveFarEcho/no new spell/commands/consent. Confirm this matches reviewed no-record-deletion scope rather than creating retroactive historical silence.
- SenseAlignment reports true Director-hidden axes when permitted; protected axesIndeterminate. MundaneobjectUnaligned default onlyafterprotectioncheck, notusingblockedreadasnegativeproof. DetectFaction usesexplicitconfirmednonaffiliation—not absentfield—to reportNotAffiliated.
- Foresight hostile d20 rollconsumedbeforethrow; singleactualmulti-subjectrollmodifiedonceforwholegroup. Glimpse consumesnextACTUALnewinitiative within1min, notcurrentencounterreroll. One pendingbenefit/noinventednewcombatresourcewindow.
- ResonanceSight exactcurrentRPonly; ordinaryvisibility andsameplane/30ftLoE, zeroactualpoolvsundefined; privateintuitivecolornumbernotglobaltaxonomy. Wardunreadabilitycannotbedistinguishedfromnoaura.
- Thoughts alwaysnormalWissaveunlessindependentexactrulepermitsotherwise; verbalunknownlanguageuntranslated, consciouscurrentthoughtonly,noautomaticdreams/speciesassumptions, no targetnotificationotherthanordinarycastingperception/actualdefense. Changedthoughtcanbelegallyreadonfreshcast/save/Refrain.
- Weather forecast1mileHORIZONTALlocaloutdoorregion; indoors/undergroundpointreferenceslocaloutdoorsabove/aroundthesamegeographiclocation, so selectedpointcanbeinsidewithLoEwithoutrequiringwallpenetration. Reportmateriallocalvariation. Existingweatherprocessesaccurate; actualnewlatercausecanchangeit, but Directorrecordsinterveningcause andcannotarbitrarilyrerollunchangedweather. No forecastrevealsofprotectedcreaturefactsjustbecauseinregion. Thisaddsrecordaccountabilityratherthananewweatherengine.
- SenseCorruption yes/noallowedpositivepresence; absent/undefinedrecordnotpositive,noinventedclock; aNoisnotproofnohiddenwardedCorruptionexists. AllretainedsourcecomponentsV,S; noF/Concadded. Newlyauthoreddurationsareexplicitratherthanleftinstantaneous-with-future-trigger.

After required repairs, please say whether all eleven may be promoted. The broader information/privacy/faction/weather domains remain open; this closes only the exact authored cards.

## Exact candidate

Candidate byte SHA256: `adc35f24695bd76ee4f35f39751bcf9bcf50489f3d8be65d8df526eaa8ed52a6`

```json
{
  "status": "LOCAL CANDIDATE — SOURCE-RECONCILED; exact manuscript review pending; NOT SELECTABLE",
  "scope": "Eleven Divination cantrips; eleven original placements/Core blocks and exact class access preserved. Authored tabletop procedures, not runtime, numerical-balance or whole-game certification.",
  "reviewEvidence": [
    "docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_SOURCE_CONFERENCE.md"
  ],
  "spells": [
    {
      "id": "foresight-flicker",
      "activation": "Action",
      "rangeFeet": 0,
      "targets": "Self.",
      "duration": "Up to 1 minute, until consumed; no concentration. If applied in initiative, ends at the caster's tenth future regular-start marker; outside initiative, ends 60 elapsed seconds after application. Preserve its virtual phase or absolute deadline through initiative changes, absence and death; an already-passed start does not count.",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "The next eligible hostile d20 roll against you has disadvantage. Establish eligibility and consume this pending benefit before the roll, even if advantage cancels it or another source already imposes disadvantage. You cannot inspect the result before deciding whether to consume it.",
      "effect": "An eligible roll is an attack targeting you or a hostile opposed/task check made directly against you as its opposing subject. Hostility is established from ordinary information available to you, not a magical allegiance report. A saving throw against your spell or feature is not a roll against you for this purpose. If one legal d20 roll affects you and other creatures together, disadvantage applies to that single roll for its whole resolution; do not reroll a separate version for the others.",
      "scaling": "None. No automatic increase in targets, range, duration or information.",
      "limitations": "One pending Foresight Flicker per caster across classes; successful recasting replaces the old benefit. Advantage/disadvantage combines normally and never supplies an automatic miss. No damage-die modifier, initiative bonus, retrospective reroll, future-event report, attack cancellation or action denial. The benefit changes an eligible roll without disclosing hidden information about its maker; an information-only divination ward is not immunity to this roll modifier. One successful application owns its endpoint; stale cleanup cannot remove its replacement. A failed or countered cast creates no replacement and refunds no committed casting cost or strain. Actual class access and repertoire, audible V/free-hand S components, casting sequence, Refrain/Dissonance, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Base RP is 0 but repeated cantrips still follow their actual strain rules. No automatic upcast or unstated scaling. Source-specific protections apply only to their actual scope. Protection from Scrying prevents new Divination/Scrying information about its protected subject, including beneficial inspection, but grants no blanket immunity to damage, buffs or other noninformational mechanics merely because of their school; it does not erase already-known facts or ordinary records.",
      "designNotes": "PRESERVED: Action/V,S and disadvantage on the next enemy roll against you. CONFLICT RULING: functional Self range replaces raw30-foot metadata without adding an ally target. NEW: one-minute pending window, exact hostile d20 eligibility, pre-roll consumption and shared-roll handling.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourcePlacements": [
        {
          "name": "Foresight Flicker",
          "school": "Divination",
          "level": 0,
          "summary": "Next enemy roll against you has Disadvantage."
        }
      ],
      "sourceCoreEntries": [
        {
          "index": 208,
          "original": {
            "school": "Divination",
            "level": 0,
            "name": "Foresight Flicker",
            "effect": "Next enemy roll against you has Disadvantage.",
            "source_paragraph": 9241,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Detection"
            ],
            "rp_cost": 0
          }
        }
      ],
      "classAccessEvidence": {
        "Cleric": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Mirrorsage": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Ranger": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Shaman": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Wizard": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Paladin": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "omen-whisper",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One creature, object or location you perceive within 30 feet and line of effect; alternatively, one specific course of action you are considering beginning within the next minute in the current situation.",
      "duration": "Instantaneous",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "No roll. The Director gives one brief, truthful, cryptic but usable phrase or sentence about the most immediately relevant circumstance, danger, opportunity or likely consequence connected to the chosen subject or proposed action.",
      "effect": "Only you perceive and understand the whisper. It supplies a supernatural clue from current circumstances, including relevant hidden circumstances when their disclosure is permitted; it is not merely a cosmetic noise. Its wording may be symbolic but must convey a usable clue rather than deliberately contradict the relevant facts. No deity, spirit, speaker or binding promise is established. Recasting about materially the same subject or action while circumstances remain materially unchanged gives the same omen or a restatement, without cumulative extra detail. A material change can yield a different omen.",
      "scaling": "None. No automatic increase in targets, range, duration or information.",
      "limitations": "It does not guarantee future decisions, dice or events not yet caused, compel anyone to enact a predicted outcome, reveal a whole stat block/inventory/plot or automatically succeed at a task. New voluntary actions or genuinely new causes may make a previously truthful omen obsolete. Rephrasing the same inquiry, switching casters or serially subdividing it does not create extra information from an unchanged omen; use the same materially equivalent subject/circumstance boundary. No additional daily use cap is added. If all relevant information is specifically protected, the Director gives only an uninformative opaque omen without naming the protection; permitted information about other subjects remains available. Actual class access and repertoire, audible V/free-hand S components, casting sequence, Refrain/Dissonance, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Base RP is 0 but repeated cantrips still follow their actual strain rules. No automatic upcast or unstated scaling. Source-specific protections apply only to their actual scope. Protection from Scrying prevents new Divination/Scrying information about its protected subject, including beneficial inspection, but grants no blanket immunity to damage, buffs or other noninformational mechanics merely because of their school; it does not erase already-known facts or ordinary records.",
      "designNotes": "PRESERVED: Action/30feet/V,S/instantaneous and a cryptic supernatural tip. NEW: bounded subject/action input, one truthful usable private clue, current-circumstances scope and no incremental detail for materially repeated inquiry. No universal future-certainty or spirit-contact ability.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourcePlacements": [
        {
          "name": "Omen Whisper",
          "school": "Divination",
          "level": 0,
          "summary": "Hear a vague message from beyond; Director gives cryptic tip."
        }
      ],
      "sourceCoreEntries": [
        {
          "index": 210,
          "original": {
            "school": "Divination",
            "level": 0,
            "name": "Omen Whisper",
            "effect": "Hear a vague message from beyond; DM gives cryptic tip.",
            "source_paragraph": 9243,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Utility"
            ],
            "rp_cost": 0
          }
        }
      ],
      "classAccessEvidence": {
        "Cleric": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Mirrorsage": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Ranger": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Shaman": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Wizard": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Paladin": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "far-echo",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One point you perceive within 30 feet and line of effect; its capture area is a 5-foot-radius sphere.",
      "duration": "One replay lasting at most 6 elapsed seconds; no concentration. The fixed playback window does not restart with initiative.",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "No roll. Sample the 6 elapsed seconds immediately before this cast began, excluding its own V component. Retrieve speech produced within the chosen capture sphere that was actually audible at its center during that historical window. Immediately replay that eligible speech once from the chosen point over the original relative timing.",
      "effect": "Preserve the original language, approximate voice, overlapping speakers and relative volume as heard at the sampled center; listeners use ordinary hearing rules at the replay point. A quiet source remains quiet and overlapping voices remain overlapping. The spell neither isolates a speaker nor translates, authenticates, identifies or interprets speech. Speech that could not actually be heard at the historical center because of silence, sound-blocking barriers or other actual causes is absent. If no eligible speech occurred, the replay is silence. The Director needs only the relevant recent fictional speech facts, not a continuous audio engine.",
      "scaling": "None. No automatic increase in targets, range, duration or information.",
      "limitations": "The selected sphere is fixed for this cast and the historical window cannot be moved to an older time or another plane. Far Echo replay sounds cannot themselves supply source speech for another Far Echo. Current applicable divination protection can withhold new information about a protected subject from this retrieval; it does not erase the historical event, previously known speech or ordinary recordings. The replay creates no creature or new spell components and provides no magical command, oath, consent or proof of truth. Ordinary listeners may still hear and react to the sound. It creates no permanent recording item or increasing volume loop. Actual class access and repertoire, audible V/free-hand S components, casting sequence, Refrain/Dissonance, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Base RP is 0 but repeated cantrips still follow their actual strain rules. No automatic upcast or unstated scaling. Source-specific protections apply only to their actual scope. Protection from Scrying prevents new Divination/Scrying information about its protected subject, including beneficial inspection, but grants no blanket immunity to damage, buffs or other noninformational mechanics merely because of their school; it does not erase already-known facts or ordinary records.",
      "designNotes": "PRESERVED: Action/30feet/V,S and replay of the last6seconds of speech in a location. NEW: exact5-foot sphere, eligible speech produced there and audible at its center, pre-cast sample window, once-only ordinary-audible playback, no recursive Far Echo source. Core Instantaneous metadata becomes a finite at-most6-second replay without concentration. The precise capture predicate is an exact-card completion for review.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourcePlacements": [
        {
          "name": "Far Echo",
          "school": "Divination",
          "level": 0,
          "summary": "Replay last 6 seconds of speech in location."
        }
      ],
      "sourceCoreEntries": [
        {
          "index": 213,
          "original": {
            "school": "Divination",
            "level": 0,
            "name": "Far Echo",
            "effect": "Replay last 6 seconds of speech in location.",
            "source_paragraph": 9246,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Utility"
            ],
            "rp_cost": 0
          }
        }
      ],
      "classAccessEvidence": {
        "Cleric": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Mirrorsage": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Ranger": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Shaman": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Wizard": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Paladin": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "soul-mark",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One living creature you perceive within 30 feet and line of effect.",
      "duration": "1 minute, no concentration. If applied in initiative, ends at the caster's tenth future regular-start marker; outside initiative, ends 60 elapsed seconds after application. Preserve its virtual phase or absolute deadline through initiative changes, absence and death; an already-passed start does not count. Ends earlier if the marked creature dies.",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "No save. Apply one invisible, nonphysical mark to the selected creature. While that living creature is on your plane and within 1 mile (5,280 feet), you continuously sense its direction from your current position, including meaningful vertical bearing.",
      "effect": "The direction is a bearing, not its distance, exact coordinates, room, route, appearance, surroundings or condition. Ordinary cover and walls after application do not block the sense. A specific divination/masking protection applies to its actual scope; a blocked read supplies no bearing. Beyond 1 mile or on another plane also gives no bearing, without distinguishing why. Shapechange, disguise and appearance changes retain the same creature identity and do not detach or transfer the mark. Death ends this application; there is no tracking of its corpse, soul, resurrection or another body.",
      "scaling": "None. No automatic increase in targets, range, duration or information.",
      "limitations": "One active Soul Mark per caster across classes; successful recasting replaces it. Other casters may independently mark the same creature with their own endpoints. Protection from Scrying blocks the new directional information while applicable, not automatically the noninformational existence of this mark; an otherwise surviving mark can again report direction when protection ends. Expiry/death never leaves a removable item or corpse beacon. No condition, allegiance, identity-change announcement, precise location, passage through a wall or ownership of the target is granted. One successful application owns its endpoint; stale cleanup cannot remove its replacement. A failed or countered cast creates no replacement and refunds no committed casting cost or strain. Actual class access and repertoire, audible V/free-hand S components, casting sequence, Refrain/Dissonance, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Base RP is 0 but repeated cantrips still follow their actual strain rules. No automatic upcast or unstated scaling. Source-specific protections apply only to their actual scope. Protection from Scrying prevents new Divination/Scrying information about its protected subject, including beneficial inspection, but grants no blanket immunity to damage, buffs or other noninformational mechanics merely because of their school; it does not erase already-known facts or ordinary records.",
      "designNotes": "PRESERVED: Action/30feet/V,S,1minute tag and direction within1mile. NEW: living-target/death boundary, same-plane bearing, nonphysical marker, ordinary-wall continuation, independent caster records and explicit no-information result. No concentration or saving throw is added.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourcePlacements": [
        {
          "name": "Soul Mark",
          "school": "Divination",
          "level": 0,
          "summary": "Tag a creature for 1 minute; you know its direction if within 1 mile."
        }
      ],
      "sourceCoreEntries": [
        {
          "index": 215,
          "original": {
            "school": "Divination",
            "level": 0,
            "name": "Soul Mark",
            "effect": "Tag a creature for 1 minute; you know its direction if within 1 mile.",
            "source_paragraph": 9248,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "1 minute",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Utility"
            ],
            "rp_cost": 0
          }
        }
      ],
      "classAccessEvidence": {
        "Cleric": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Mirrorsage": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Ranger": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Shaman": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Wizard": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Paladin": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "sense-alignment",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One creature or object you perceive within 30 feet and line of effect.",
      "duration": "Instantaneous",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "No save. Privately receive a snapshot of the target's actual current canonical Lawful/Neutral/Chaotic and Good/Neutral/Evil axes. Each recorded axis is reported, including Director-hidden records if unprotected. An undefined or unrevealed-through-protection axis reads Indeterminate, never a guessed value.",
      "effect": "An object is Unaligned unless it itself has an explicit alignment record. An aligned object is read by the same two-axis procedure; its owner, creator, faction, material, logo or visual theme does not confer alignment on it. Evaluate actual protection before drawing an Unaligned conclusion: a protected answer cannot be converted into a claim that the record is absent. A protection affecting only one axis leaves the other independently reportable when permitted. An actual masking source may alter the output only if its exact rules authorize doing so.",
      "scaling": "None. No automatic increase in targets, range, duration or information.",
      "limitations": "No current personality, moral judgment, belief, intention, truthfulness, crime, oath status, faction, soul condition or guaranteed future conduct is revealed. The report is private, instantaneous and nonphysical; it does not compel speech or cause a permanent visible mark. Knowing an alignment does not authorize changing it. The historical Movement tag grants no movement or teleport. Actual class access and repertoire, audible V/free-hand S components, casting sequence, Refrain/Dissonance, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Base RP is 0 but repeated cantrips still follow their actual strain rules. No automatic upcast or unstated scaling. Source-specific protections apply only to their actual scope. Protection from Scrying prevents new Divination/Scrying information about its protected subject, including beneficial inspection, but grants no blanket immunity to damage, buffs or other noninformational mechanics merely because of their school; it does not erase already-known facts or ordinary records.",
      "designNotes": "PRESERVED: Action/30feet/V,S/instantaneous and alignment of one creature or object. NEW: exact two-axis snapshot, independent protected/undefined outputs, explicit object Unaligned default and private information boundary; no saving throw added.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourcePlacements": [
        {
          "name": "Sense Alignment",
          "school": "Divination",
          "level": 0,
          "summary": "Briefly detect the alignment of one creature or object."
        }
      ],
      "sourceCoreEntries": [
        {
          "index": 217,
          "original": {
            "school": "Divination",
            "level": 0,
            "name": "Sense Alignment",
            "effect": "Briefly detect the alignment of one creature or object.",
            "source_paragraph": 9250,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Movement",
              "Detection",
              "Alignment"
            ],
            "rp_cost": 0
          }
        }
      ],
      "classAccessEvidence": {
        "Cleric": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Mirrorsage": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Ranger": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Shaman": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Wizard": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Paladin": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "glimpse-future",
      "activation": "Action",
      "rangeFeet": 0,
      "targets": "Self.",
      "duration": "Instantaneous glimpse plus a pending initiative benefit for up to 1 minute, until consumed; no concentration. If applied in initiative, ends at the caster's tenth future regular-start marker; outside initiative, ends 60 elapsed seconds after application. Preserve its virtual phase or absolute deadline through initiative changes, absence and death; an already-passed start does not count.",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "No roll. On resolution the Director gives a brief qualitative glimpse of the most likely events during the next 6 seconds if current circumstances continue. Separately, your next new initiative roll during the pending window has advantage; consume the entitlement on that roll even if another source already supplies advantage.",
      "effect": "The glimpse may concern imminent motion, an approach, attack, collapse, hazard or lack of meaningful immediate change. It is a limited current-circumstances projection, not a full transcript or future die result. Future choices and new events remain capable of changing it. The initiative benefit can apply to the next actual new combat initiative roll before its endpoint, including if that combat begins more than 6 seconds after casting. It cannot modify or reroll initiative already established for the current encounter.",
      "scaling": "None. No automatic increase in targets, range, duration or information.",
      "limitations": "One pending Glimpse Future initiative benefit per creature across classes; successful recasting replaces rather than accumulates it. If no qualifying roll occurs before expiry, the benefit is lost. Merely calling an ongoing scene a new combat does not grant another initiative roll or reset resources. Applicable information protection can hide details of the glimpse without automatically canceling the separate initiative modifier. This supplies no party-wide warning mechanic, free Action, completed task, condition removal, RP, round reset or guaranteed sequence of future choices. One successful application owns its endpoint; stale cleanup cannot remove its replacement. A failed or countered cast creates no replacement and refunds no committed casting cost or strain. Actual class access and repertoire, audible V/free-hand S components, casting sequence, Refrain/Dissonance, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Base RP is 0 but repeated cantrips still follow their actual strain rules. No automatic upcast or unstated scaling. Source-specific protections apply only to their actual scope. Protection from Scrying prevents new Divination/Scrying information about its protected subject, including beneficial inspection, but grants no blanket immunity to damage, buffs or other noninformational mechanics merely because of their school; it does not erase already-known facts or ordinary records.",
      "designNotes": "PRESERVED: Action/V,S, six-second future glimpse and advantage on initiative for next combat. CONFLICT RULING: functional Self replaces raw30-foot metadata without ally access; Core Instantaneous glimpse is separated from NEW finite1-minute pending initiative entitlement. No concentration is added.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourcePlacements": [
        {
          "name": "Glimpse Future",
          "school": "Divination",
          "level": 0,
          "summary": "See 6 seconds into the future; advantage on initiative next combat."
        }
      ],
      "sourceCoreEntries": [
        {
          "index": 218,
          "original": {
            "school": "Divination",
            "level": 0,
            "name": "Glimpse Future",
            "effect": "See 6 seconds into the future; advantage on initiative next combat.",
            "source_paragraph": 9251,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Utility"
            ],
            "rp_cost": 0
          }
        }
      ],
      "classAccessEvidence": {
        "Cleric": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Mirrorsage": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Ranger": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Shaman": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Wizard": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Paladin": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "detect-faction",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One creature or object you perceive within 30 feet and line of effect; choose one exact canonical factionId you know when casting.",
      "duration": "Instantaneous",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "No save. Privately report Affiliated if the target has an explicit current membership/affiliation record for the chosen faction; Not Affiliated if an explicit current record establishes nonaffiliation; otherwise Indeterminate. An actual protection that blocks this information also returns Indeterminate without identifying the cause.",
      "effect": "Director-hidden actual affiliation is valid spell information and is reported unless specifically protected. Mere absence of a membership field is not an explicit nonaffiliation record. For an object, only an explicit institutional affiliation or issuance record qualifies. A counterfeit logo, creator's membership, present owner, appearance or style alone supplies no affiliation. Target identity is the actual selected creature or object, not the identity it claims to represent.",
      "scaling": "None. No automatic increase in targets, range, duration or information.",
      "limitations": "Positive/negative reputation is not membership. No current loyalty, intentions, rank, credentials, authority, exact reputation score or other faction memberships are disclosed. The caster must supply the one known unambiguous canonical faction; the spell cannot enumerate unknown factions or invent affiliation/nonaffiliation records for undefined NPCs and objects. It grants no proof token, public announcement, membership, reputation change or legal permission. Actual class access and repertoire, audible V/free-hand S components, casting sequence, Refrain/Dissonance, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Base RP is 0 but repeated cantrips still follow their actual strain rules. No automatic upcast or unstated scaling. Source-specific protections apply only to their actual scope. Protection from Scrying prevents new Divination/Scrying information about its protected subject, including beneficial inspection, but grants no blanket immunity to damage, buffs or other noninformational mechanics merely because of their school; it does not erase already-known facts or ordinary records.",
      "designNotes": "PRESERVED: Action/30feet/V,S/instantaneous and determine affiliation of creature or object. NEW: one-known-faction test and explicit Affiliated/Not Affiliated/Indeterminate records, no save, private snapshot and object issuance predicate.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourcePlacements": [
        {
          "name": "Detect Faction",
          "school": "Divination",
          "level": 0,
          "summary": "Determine if a creature or object is affiliated with a faction."
        }
      ],
      "sourceCoreEntries": [
        {
          "index": 219,
          "original": {
            "school": "Divination",
            "level": 0,
            "name": "Detect Faction",
            "effect": "Determine if a creature or object is affiliated with a faction.",
            "source_paragraph": 9252,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Detection",
              "Faction"
            ],
            "rp_cost": 0
          }
        }
      ],
      "classAccessEvidence": {
        "Cleric": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Mirrorsage": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Ranger": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Shaman": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Wizard": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Paladin": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "resonance-sight",
      "activation": "Action",
      "rangeFeet": 0,
      "targets": "Self; view ordinarily visible creatures and objects within 30 feet, on the same plane and in line of effect.",
      "duration": "1 round, no concentration. Ends at the caster's first future regular-start marker in initiative, or 6 elapsed seconds after application outside initiative. Preserve that virtual phase/absolute deadline through initiative changes, absence and death; an already-passed start does not count.",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "No roll or additional scanning Action. Privately perceive a colored aura for each eligible subject with an actual RP pool. The aura lets you read that subject's exact current RP amount and updates as the amount changes during the spell.",
      "effect": "Its color is your intuitive private visual encoding of the number, not an externally standardized palette. A defined pool at 0 RP reads as a dim/colorless zero aura. A subject with no defined RP pool has no aura. An effect preventing the read likewise supplies no readable aura and does not identify its own protection; the absence of a readable aura therefore is not proof that a pool does not exist.",
      "scaling": "None. No automatic increase in targets, range, duration or information.",
      "limitations": "You learn only current RP, not maximum RP, Dissonance, Refrain, class, charges, spell repertoire, HP, recovery history or another resource. A missing pool is never invented as 0 RP. The aura is visible only to you, emits no real light, and does not reveal Invisible/Hidden creatures or satisfy vision through obscurity or total cover. Losing ordinary visibility, range or line of effect removes the current read without freezing a falsely current value. No RP, transfer permission, energy source, detectable public light or resource reset is created. Actual class access and repertoire, audible V/free-hand S components, casting sequence, Refrain/Dissonance, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Base RP is 0 but repeated cantrips still follow their actual strain rules. No automatic upcast or unstated scaling. Source-specific protections apply only to their actual scope. Protection from Scrying prevents new Divination/Scrying information about its protected subject, including beneficial inspection, but grants no blanket immunity to damage, buffs or other noninformational mechanics merely because of their school; it does not erase already-known facts or ordinary records.",
      "designNotes": "PRESERVED: Action/V,S,30-foot information area and colored RP auras for1round. NEW: Self casting origin, exact-current-RP private encoding, actual-zero distinction, dynamic ordinary-visibility predicate and no pool invention. No concentration is added.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourcePlacements": [
        {
          "name": "Resonance Sight",
          "school": "Divination",
          "level": 0,
          "summary": "See Resonance Points as colored auras for 1 round."
        }
      ],
      "sourceCoreEntries": [
        {
          "index": 220,
          "original": {
            "school": "Divination",
            "level": 0,
            "name": "Resonance Sight",
            "effect": "See Resonance Points as colored auras for 1 round.",
            "source_paragraph": 9253,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "1 round",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Detection",
              "Resonance"
            ],
            "rp_cost": 0
          }
        }
      ],
      "classAccessEvidence": {
        "Cleric": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Mirrorsage": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Ranger": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Shaman": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Wizard": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Paladin": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "read-surface-thoughts",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One creature you perceive within 30 feet and line of effect.",
      "duration": "Instantaneous",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "The target makes a Wisdom save against your actual spell DC. Success gives no thought. Failure gives one immediate thought occupying its conscious attention at resolution, if such a thought exists and is not specifically protected. This spell grants no option to waive the save; any independently authorized save-failure rule retains its own scope.",
      "effect": "Receive one brief phrase, image, emotion, sensory impression or simple idea. A verbal thought retains the language in which the target frames it; unknown words remain unintelligible without independent language comprehension. Nonverbal images and feelings are perceived as such, not automatically translated into a precise proposition. An actually unconscious creature has no conscious surface thought to supply. Ordinary sleep does not make its dreams eligible without an exact rule granting that permission. Thought eligibility follows actual present mental state, not an assumed creature-type stereotype.",
      "scaling": "None. No automatic increase in targets, range, duration or information.",
      "limitations": "No memory search, interrogation, truth compulsion, complete motive reading, guaranteed future intent, mind control or psychic damage. The target is not automatically alerted by success/failure of reading, but normal perception of V/S casting or an actual mental-defense feature can reveal the attempt. Success grants no later immunity. A later legal cast uses a fresh save and reads only the thought then actually current, with ordinary Refrain; repeated casting cannot turn one thought into a hidden biography or force the target to think about a chosen subject. A blocked or absent thought gives no reason distinguishing save, protection or current lack of thought. Actual class access and repertoire, audible V/free-hand S components, casting sequence, Refrain/Dissonance, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Base RP is 0 but repeated cantrips still follow their actual strain rules. No automatic upcast or unstated scaling. Source-specific protections apply only to their actual scope. Protection from Scrying prevents new Divination/Scrying information about its protected subject, including beneficial inspection, but grants no blanket immunity to damage, buffs or other noninformational mechanics merely because of their school; it does not erase already-known facts or ordinary records.",
      "designNotes": "PRESERVED: Action/30feet/V,S/instantaneous, one current thought and WIS save negates. NEW: conscious one-thought boundary, original-language handling, no automatic notification/immunity, no inferred sentience from species and explicit lack of a spell-granted voluntary save waiver.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourcePlacements": [
        {
          "name": "Read Surface Thoughts",
          "school": "Divination",
          "level": 0,
          "summary": "Glimpse the current thought of a creature (WIS save negates)."
        }
      ],
      "sourceCoreEntries": [
        {
          "index": 221,
          "original": {
            "school": "Divination",
            "level": 0,
            "name": "Read Surface Thoughts",
            "effect": "Glimpse the current thought of a creature (WIS save negates).",
            "source_paragraph": 9254,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Wisdom save",
            "tags": [
              "Utility"
            ],
            "rp_cost": 0
          }
        }
      ],
      "classAccessEvidence": {
        "Cleric": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Mirrorsage": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Ranger": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Shaman": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Wizard": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Paladin": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "detect-weather",
      "activation": "Action",
      "rangeFeet": 30,
      "targets": "One point you perceive within 30 feet and line of effect, on your current plane.",
      "duration": "Instantaneous information about the following 24 hours; no continuing buff or concentration.",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "No roll. The Director gives an accurate 24-hour forecast for the local outdoor region within 1 mile horizontally of that point on the same plane. Describe meaningful local variations when the terrain makes the region's weather differ. An indoor or underground point refers to the outdoor local weather above/around that same geographical location rather than the room's climate.",
      "effect": "Report relevant temperature bands/trends, precipitation type and approximate timing, wind direction/strength, weather-caused visibility and significant storm or environmental-weather hazards. The report is intelligible to the caster and accurate for the current natural processes and already-existing magical weather expected to continue; record the forecast as the current weather expectation. A weatherless environment reports that fact. It supplies useful specific conditions rather than a vague warning that weather might change.",
      "scaling": "None. No automatic increase in targets, range, duration or information.",
      "limitations": "A genuinely new later cause, such as a voluntary weather-changing spell, new supernatural event or catastrophe, can change actual conditions after the forecast without having been predicted. The Director must identify an actual intervening cause in the game record, not silently invalidate the forecast by rerolling unchanged weather; this need not reveal that cause to the caster. The spell does not control weather, grant exposure protection, reveal encounters/loot, complete travel, recover resources or predict unrelated events. Information about a specifically protected subject remains limited by that actual protection; ordinary ambient weather is not automatically protected by a creature standing in it. Actual class access and repertoire, audible V/free-hand S components, casting sequence, Refrain/Dissonance, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Base RP is 0 but repeated cantrips still follow their actual strain rules. No automatic upcast or unstated scaling. Source-specific protections apply only to their actual scope. Protection from Scrying prevents new Divination/Scrying information about its protected subject, including beneficial inspection, but grants no blanket immunity to damage, buffs or other noninformational mechanics merely because of their school; it does not erase already-known facts or ordinary records.",
      "designNotes": "PRESERVED: Action/30feet/V,S/instantaneous and accurate next24-hour weather prediction. NEW: finite1-mile local outdoor region, explicit indoor reference, forecast fields and current-processes/future-agency boundary. This is a tabletop forecast record, not a claim a weather simulation is implemented.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourcePlacements": [
        {
          "name": "Detect Weather",
          "school": "Divination",
          "level": 0,
          "summary": "Accurately predict weather for the next 24 hours."
        }
      ],
      "sourceCoreEntries": [
        {
          "index": 222,
          "original": {
            "school": "Divination",
            "level": 0,
            "name": "Detect Weather",
            "effect": "Accurately predict weather for the next 24 hours.",
            "source_paragraph": 9255,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Detection"
            ],
            "rp_cost": 0
          }
        }
      ],
      "classAccessEvidence": {
        "Cleric": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Mirrorsage": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Ranger": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Shaman": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Wizard": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Paladin": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    },
    {
      "id": "sense-corruption",
      "activation": "Action",
      "rangeFeet": 0,
      "targets": "Self; sense a 30-foot-radius area on the same plane, limited by line of effect.",
      "duration": "Instantaneous",
      "concentration": false,
      "components": [
        "V",
        "S"
      ],
      "resolution": "No roll. Privately learn Yes if at least one creature, object, area or active effect within the sensing area currently bears an explicit canonical Corruption record/tag/state that this detection is permitted to read. Otherwise learn No.",
      "effect": "Actual hidden Corruption is valid spell information and yields Yes when unprotected. Total cover blocks the relevant part of the sensing area. Undefined/missing records do not establish Corruption and do not create a numeric value. A specific masking/protection effect excludes only the information within its written scope; it does not announce that masking occurred. A No result means no permitted positive presence was detected, not proof that no protected Corruption could exist.",
      "scaling": "None. No automatic increase in targets, range, duration or information.",
      "limitations": "This reveals no direction, distance, location, count, identity, type, severity, numeric track, cause, hidden consequence or cure. Alignment, disease, ordinary poison, faction, reputation, crime or creature species does not itself establish Corruption. No fear, damage, attack permission, protection, healing, harvest right or new global Corruption clock is created. Actual class access and repertoire, audible V/free-hand S components, casting sequence, Refrain/Dissonance, class hooks and interruption follow SPELL_INTEGRATION_RULES.md. Base RP is 0 but repeated cantrips still follow their actual strain rules. No automatic upcast or unstated scaling. Source-specific protections apply only to their actual scope. Protection from Scrying prevents new Divination/Scrying information about its protected subject, including beneficial inspection, but grants no blanket immunity to damage, buffs or other noninformational mechanics merely because of their school; it does not erase already-known facts or ordinary records.",
      "designNotes": "PRESERVED: Action/V,S/instantaneous and presence within30feet. NEW: Self casting origin, same-plane30-foot line-of-effect area, exact canonical positive predicate and strictly Yes/No output. Existing Detect Corruption and sensor interfaces remain separate named spells.",
      "implementationStatus": "LOCAL CANDIDATE — source-reconciled; exact manuscript review pending; not selectable",
      "sourcePlacements": [
        {
          "name": "Sense Corruption",
          "school": "Divination",
          "level": 0,
          "summary": "Detect presence of corruption within 30 feet."
        }
      ],
      "sourceCoreEntries": [
        {
          "index": 223,
          "original": {
            "school": "Divination",
            "level": 0,
            "name": "Sense Corruption",
            "effect": "Detect presence of corruption within 30 feet.",
            "source_paragraph": 9256,
            "casting_time": "1 action",
            "range": "30 feet",
            "duration": "Instantaneous",
            "components": "V, S",
            "resolution": "Automatic or opposed as described",
            "tags": [
              "Detection",
              "Corruption"
            ],
            "rp_cost": 0
          }
        }
      ],
      "classAccessEvidence": {
        "Cleric": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Mirrorsage": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Ranger": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Shaman": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Wizard": {
          "rank": 0,
          "minimumClassLevel": 1,
          "school": "Divination",
          "baseRpCost": 0
        },
        "Paladin": {
          "rank": 0,
          "minimumClassLevel": 2,
          "school": "Divination",
          "baseRpCost": 0
        }
      },
      "sourceReview": [
        "docs/audit/2026-10-08/full-game/GPT_DIVINATION_CANTRIP_SOURCE_CONFERENCE.md"
      ],
      "reviewEvidence": []
    }
  ]
}
```

## Existing Protection from Scrying, unchanged

```json
{
  "id": "protection-from-scrying",
  "activation": "Action",
  "rangeFeet": 60,
  "targets": "One willing creature you can perceive within range and line of effect, including yourself.",
  "duration": "1 hour: expires 3,600 elapsed seconds after application; entering, leaving or reordering initiative does not change that deadline.",
  "concentration": false,
  "components": [
    "V",
    "S",
    "F"
  ],
  "resolution": "Automatic after legal casting. Check an information-gathering effect's actual generating source classification, using its real casting-class school placement where applicable.",
  "effect": "The target supplies no new information to effects explicitly classified as Divination or Scrying that attempt to perceive, locate, inspect, read, identify or otherwise obtain information about it. Apply this protection equally against hostile, neutral and beneficial information gathering. A multi-subject or area effect may still obtain permitted information about other subjects.",
  "scaling": "None.",
  "limitations": "No ordinary invisibility, concealment, false identity, attack defense, memory erasure, record deletion or retroactive protection. A class sense is blocked only insofar as its actual source classifies it as Divination/Scrying; the underlying class engine remains intact. Theme or guessed purpose is not classification. Known information remains known. Independent applications do not stack extra power and each retains its own endpoint. Apply SPELL_INTEGRATION_RULES.md for actual class access and repertoire, costs before resolution, components, concentration, Dissonance/Refrain and exact source cadence. No automatic scaling or generic upcast.",
  "designNotes": "PRESERVED: Action, 60 feet, V/S/F and divination/scrying immunity. NEW CONFLICT RULING: ongoing 1 hour without concentration replaces Instantaneous metadata; immunity is operationally defined as prevention of new information about one willing target, not a blanket damage/benefit immunity against a school name."
}
```
