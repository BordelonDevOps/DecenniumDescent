# Absolute Domination — accepted static authored procedure 292

GPT accepted Absolute Domination / AG190-B01 only after verifying the corrected conditional END-save branches. This updates the authored review index; the native spell catalog, runtime selection, and downstream gates remain unchanged.

## Preserved native card and procedure

{
  "additionalRpCost": 0,
  "classAccess": {
    "Wizard": {
      "baseRpCost": 26,
      "minimumClassLevel": 17,
      "rank": 9,
      "school": "Enchantment"
    }
  },
  "id": "absolute-domination",
  "name": "Absolute Domination",
  "operational": null,
  "reviewFlags": [
    "Not selectable in this spell playtest packet until individual operational review"
  ],
  "schools": [
    "Enchantment"
  ],
  "source": {
    "catalogKey": "absolute-domination",
    "catalogPath": "src/data/spells.js",
    "catalogSha256": "3358a2e1afcbc340dbafd92e45e39a7d2d0a24fed5c0719a3d233263ce530078",
    "coreEntries": [
      {
        "index": 400,
        "original": {
          "casting_time": "1 action",
          "components": "V, S, F",
          "duration": "Concentration, up to 1 minute",
          "effect": "Control any creature (WIS save at end of each turn); lasts 1 minute.",
          "level": 9,
          "name": "Absolute Domination",
          "range": "120 feet",
          "resolution": "Wisdom save",
          "rp_cost": 26,
          "school": "Enchantment",
          "source_paragraph": 9476,
          "tags": [
            "Control"
          ]
        }
      }
    ],
    "corePath": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "coreSha256": "50c3e9683349e93192191381ab6354ca7d675a24fcc9bb9b039c23e67fecca4f",
    "original": {
      "alternateSummaries": [],
      "castingTime": "Not specified in current rulebook",
      "classLearnLevels": {
        "Wizard": 17
      },
      "classLevels": {
        "Wizard": 9
      },
      "classRanks": {
        "Wizard": 9
      },
      "classSchools": {
        "Wizard": "Enchantment"
      },
      "classes": [
        "Wizard"
      ],
      "components": "Not specified in current rulebook",
      "description": "Control any creature (WIS save at end of each turn); lasts 1 minute.",
      "duration": "Not specified in current rulebook",
      "level": 9,
      "name": "Absolute Domination",
      "placements": [
        {
          "level": 9,
          "name": "Absolute Domination",
          "school": "Enchantment",
          "summary": "Control any creature (WIS save at end of each turn); lasts 1 minute."
        }
      ],
      "range": "Not specified in current rulebook",
      "resonanceRank": 9,
      "school": "Enchantment",
      "schools": [
        "Enchantment"
      ],
      "source": "Player Rulebook — Spell Lists",
      "status": "canon"
    },
    "possibleHistoricalAliases": []
  },
  "status": "blocked-pending-operational-review",
  "visibility": "public-source-review"
}

{
  "admission": "KEEP any creature,minute concentration and native Wisdom resistance. Select one actually perceived creature within120ft/LoE, including self; no imported CR/type ceiling. NEW initial WIS resolves the Core Wisdom-save field; success establishes nothing, failure admits one non-Charmed hard-control component only through actual defenses and the shared guard. Creature classification is application-only; a later same-identity form change does not silently release control. A legal creation does not grant a current-turn order.",
  "command": "Use the complete rank9 order and companion contracts above, explicitly retaining their broader known Action-spell/RP choice and all actual restrictions. A mental command cannot manufacture a hand, speech, target, free focus, ability use or source knowledge. Orders use only real regular control opportunities, even if an extra turn exists. Without a valid opportunity order, normal agency remains; only a real companion chassis supplies its own Dodge default.",
  "replacement": "NEW one live Absolute controller per target across casters. Only an actually admitted new control replaces the old same-spell component; a saved/immune/guard-blocked attempt does not. Old and different-identity effects retain their exact scope. Actual concentration loss, source-owned removal, matching save, recipient terminal ending or original maximum ends control. Loss of same-plane communication merely prevents a new order; it does not pause the clock or bank one.",
  "saves": "KEEP one WIS at END of EACH ACTUAL affected target turn, including a genuinely source-authorized inserted full turn and an affected current turn, while this application still exists, even if control is suppressed. This explicit native exception applies only to its ending save, not orders, recharge, regular budgets or periodic ticks. A successful save ends this application and its pending order. No damage-triggered save is added. Original maximum is establishment+60elapsed seconds. The separate companion/fallback save bridge is labelled NEW and is not evidence of an extra turn. Under AG291-OBLIGATION-REVISION-01, the two conditional inserted-turn END-save tests satisfy the external-provider review obligation for authored-procedure acceptance only. Actual gameplay using an inserted full turn still requires its separately authorized source, lawful acquisition, activation, eligible recipient, and actual actor history under AG190-H-SOURCE."
}

## Accepted conditional closure tests

- Failure branch: WIS 1 + 7 = 8 vs. DC 19; control and pending regular Dodge remain.
- Success branch: WIS 12 + 7 = 19 vs. DC 19; the application, pending order, and caster concentration pointer end.
- The branches establish no actual provider or gameplay turn.

## Retained qualifications

- Acceptance is limited to the preserved Absolute Domination procedure, corrected conditional inserted-turn END-save tests, and AG291-OBLIGATION-REVISION-01.
- The conditional tests establish no actual inserted-turn provider, grant, acquisition, activation, eligible recipient, or gameplay history.
- Actual gameplay using an inserted full turn still requires its separately authorized source, lawful acquisition, activation, and eligible recipient under AG190-H-SOURCE.
- The native WIS save at END of every actual affected target turn remains unchanged; an inserted turn creates no command opportunity, regular budget, recharge, Reaction refresh, Ready change, or regular-clock tick.
- AG190-H-SOURCE, AG190-H-PHYSICAL, AG190-H-CONTENT, AG190-H-LIFECYCLE, AG190-H-RUNTIME, AG190-H-PLAY, AG190-H-BALANCE, AG190-H-COSMOLOGY, AG190-H-DOMAIN, and AG190-H-RELEASE remain retained.
- AG190-B02 remains open for Puppetmaster's Realm. Native catalog is byte-exact and runtime selection remains disabled; implementation, human-play, balance, cosmology, domain-closure, and release gates remain closed.
