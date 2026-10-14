# Six training feats: complete operating proposal

**UNADOPTED; awaiting joint GPT review.** This proposal completes the draft procedures for Acrobat, Animal Affinity, Athletic Prodigy, Charismatic, Diplomat and Naturalist. It preserves all six full original records and their original GE questions. The other 25 General exploration feats are outside this document. The operational feat count remains eight reviewed and 327 pending.

[Structured proposal and preserved sources](../../data/director/training_feat_operating_proposal_internal.json) · [Original General exploration source audit](../../../../docs/audit/2026-10-08/full-game/GENERAL_EXPLORATION_FEAT_SOURCE_AUDIT.md) · [Separate 25 Skill-feat proposals](SKILL_FEAT_OPERATING_PROPOSAL.md)

## Shared procedure

### Acquire the actual feat

UNADOPTED NEW scope: these six feats are nonrepeatable and require an actual legal feat selection at the class progression's existing milestone. Check the printed permanent ability prerequisite at acquisition. A title, descriptive similarity or compatibility alias grants no second acquisition. The six names below remain distinct source identities.

### Snapshot each skill separately

NEW: immediately before applying this feat, record whether the character is already proficient in each listed skill. For a skill not yet proficient, grant proficiency. For a skill already proficient, grant twice-PB Expertise for that skill. Make this branch decision independently for every skill, before any of this feat's own grants. Do not let its first proficiency grant count as prior proficiency for a second reading of the same clause.

### Record and retain the selected branch

NEW: save the acquisition event, feat ID, skill, prior proficiency and resulting grant. A proficiency branch does not turn into Expertise merely because another source later grants the same proficiency. Resolve the later source under its own duplicate rule. Where an earned advancement permits sequential choices, process and record the actual chosen acquisition order; do not rewrite that order after observing a later result or silently treat all grants as simultaneous.

### One proficiency contribution

RETAIN current character foundation: a check uses its actual ability modifier plus at most one applicable proficiency contribution. Twice PB replaces normal PB. Two Expertise sources still supply twice PB, never three or four times PB. If an independently reviewed source explicitly supplies a larger proficiency multiplier, use the largest applicable single multiplier; this proposal grants none. A qualifying skill and tool do not each add PB.

### Do the real task

The feat grants training, not automatic success or a new permitted action. Apply task degrees, contested ties, actual senses, equipment, legal access, time, materials and advantage/disadvantage normally. A skill check may use a different ability when the actual governing task expressly calls for it; the applicable proficiency grant remains in that skill. No feat creates a movement mode, willing creature, food, information, companion or new social authority.

### Existing overlap stays distinct

Acrobat grants only Acrobatics training/Expertise. Acrobatic, Athletic Prodigy and Acrobatic Mastery remain separate original feats with their own prerequisites and effects. Animal Affinity does not grant Beast Whisperer or Beast Lore. Naturalist grants no Ranger class level or Ranger Training hiding permission. Shared skills do not merge source IDs or create repeatable acquisitions.

### What still needs joint approval

The acquisition-time branch, nonrepeatability and duplicate-branch policy are explicit new authoring choices. They need GPT agreement across all feat cohorts, including Cultural Expert, fixed training grants and any later retraining procedure. Current operational feat count remains eight of 335; these six and the separate 25 Skill-feat proposals remain pending. No source registry or public operational manifest is changed.

## GE-01 — Acrobat

Source identity: `acrobat`. Original prerequisite: **Dexterity 13 or higher**.

**Source effect, unchanged**

You gain proficiency in the Acrobatics skill. If you are already proficient, you add double your proficiency bonus to Acrobatics checks.

**Proposed procedure**

Gain proficiency in Acrobatics if not already proficient immediately before acquiring this feat. Otherwise use twice PB for Acrobatics checks. This does not substitute Dexterity for an Athletics check, grant a climbing Speed, improve an actual jump distance or allow a reroll. Those benefits require their own actual sources.

**Worked adjudications**

- A DEX 16, PB +2 character without Acrobatics gains a +5 normal Dexterity (Acrobatics) modifier, not +7.

- A DEX 16, PB +2 character already proficient in Acrobatics now uses +7. Already having another twice-PB Acrobatics source leaves +7, not +11.

- Owning this feat does not satisfy a prerequisite asking for the differently named Acrobatic feat unless a future explicit identity decision says so.

<details><summary>Complete original source and conference question</summary>

```json
{
  "id": "acrobat",
  "name": "Acrobat",
  "description": "You become more nimble and agile.",
  "prerequisite": "Dexterity 13 or higher",
  "effect": "You gain proficiency in the Acrobatics skill. If you are already proficient, you add double your proficiency bonus to Acrobatics checks.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

Define acquisition-time versus later qualification for existing Acrobatics proficiency, doubled PB as expertise rather than another PB source, and stacking with Athletic Prodigy/Acrobatic Mastery. Preserve distinct Acrobat and Acrobatic identities until explicitly reconciled; this feat grants no movement mode or automatic success.

</details>

## GE-04 — Animal Affinity

Source identity: `animalAffinity`. Original prerequisite: **Wisdom 13 or higher**.

**Source effect, unchanged**

You gain proficiency in Animal Handling. If already proficient, you add double your proficiency bonus.

**Proposed procedure**

Gain proficiency in Animal Handling if not already proficient immediately before acquiring this feat. Otherwise use twice PB for Animal Handling checks. Apply it to an actual Animal Handling task allowed by the creature and situation. It provides no telepathy, creature language, automatic attitude change, trained mount, companion, domination or guaranteed cooperation. A different social or knowledge skill does not gain this proficiency merely because an animal is present.

**Worked adjudications**

- A WIS 14, PB +3 character already trained in Animal Handling uses +8 on an eligible Wisdom (Animal Handling) check.

- An untrained holder gains normal proficiency, then later gains another Animal Handling grant from a separate source: this feat remains its original proficiency branch. The new grant follows its own rule.

- Even an excellent check does not create an absent beast or let an untrained mount use combat actions unavailable under its real control procedure.

<details><summary>Complete original source and conference question</summary>

```json
{
  "id": "animalAffinity",
  "name": "Animal Affinity",
  "description": "You have a way with animals.",
  "prerequisite": "Wisdom 13 or higher",
  "effect": "You gain proficiency in Animal Handling. If already proficient, you add double your proficiency bonus.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

Define Animal Handling proficiency and existing-proficiency doubled PB, including later proficiency, noncompounding expertise and actual eligible creatures/tasks. It creates neither telepathy, automatic obedience, a companion nor a universal social check against any creature; compare Beast Whisperer separately.

</details>

## GE-06 — Athletic Prodigy

Source identity: `athleticProdigy`. Original prerequisite: **Strength or Dexterity 15 or higher**.

**Source effect, unchanged**

You gain proficiency in Athletics and Acrobatics. If already proficient, you add double your proficiency bonus.

**Proposed procedure**

The prerequisite is Strength 15 or Dexterity 15; either permanent score suffices. Evaluate Athletics and Acrobatics separately at acquisition. Grant proficiency in each untrained skill and twice-PB Expertise in each already proficient skill. Neither skill grant changes which ability the ordinary task uses. The feat gives no Speed, movement, jumping-distance increase or automatic success. Other Expertise in one of these skills is an overlapping grant of twice PB, not another multiplier.

**Worked adjudications**

- STR 15, DEX 12 meets the prerequisite. If Athletics is already trained but Acrobatics is not, acquire Athletics Expertise and ordinary Acrobatics proficiency.

- With PB +3, STR +2 and DEX +1 in that mixed case, ordinary Athletics is +8 and ordinary Acrobatics is +4. An Acrobatics roll of 12 totals 16.

- If both skills are already proficient, both gain twice PB independently. If both already have Expertise, neither becomes four times PB.

<details><summary>Complete original source and conference question</summary>

```json
{
  "id": "athleticProdigy",
  "name": "Athletic Prodigy",
  "description": "Your physical prowess is exceptional.",
  "prerequisite": "Strength or Dexterity 15 or higher",
  "effect": "You gain proficiency in Athletics and Acrobatics. If already proficient, you add double your proficiency bonus.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

Preserve both Athletics and Acrobatics grants under STRorDEX15. Decide existing-proficiency expertise separately for each skill, acquisition timing and later proficiency. Prevent quadruple PB with Acrobat/other expertise; this grants no extra movement mode, substituted ability or universal success.

</details>

## GE-09 — Charismatic

Source identity: `charismatic`. Original prerequisite: **Charisma 13+**.

**Source effect, unchanged**

You gain proficiency in Persuasion and Deception. If already proficient, you add double your proficiency bonus.

**Proposed procedure**

Evaluate Persuasion and Deception separately at acquisition: gain proficiency if untrained, or twice-PB Expertise if already proficient. These grants do not extend to Performance, Intimidation, Reputation or Insight. Persuasion and Deception remain distinct tasks with actual possible stakes, evidence, audience understanding and failure. The feat does not force agreement, make a lie objectively true, change standing or defeat magical truth restrictions by itself.

**Worked adjudications**

- A CHA 16, PB +2 holder already proficient in Persuasion but not Deception has +7 Persuasion and +5 Deception after acquiring this feat.

- The same holder's Performance proficiency and modifier remain exactly what their other real sources provide; Charismatic grants neither.

- Two actual feats each granting Persuasion Expertise still yield +7 in this example, not +11; the overlapping grant history remains recorded.

<details><summary>Complete original source and conference question</summary>

```json
{
  "id": "charismatic",
  "name": "Charismatic",
  "description": "Your personality is magnetic.",
  "prerequisite": "Charisma 13+",
  "effect": "You gain proficiency in Persuasion and Deception. If already proficient, you add double your proficiency bonus.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

Preserve Persuasion and Deception proficiency with separately adjudicated existing-proficiency double PB. Define acquisition/later proficiency and nonstacking expertise, not automatic cooperation or lie immunity. Distinguish both skills from Intimidation, Performance and social combat effects.

</details>

## GE-14 — Diplomat

Source identity: `diplomat`. Original prerequisite: **Charisma 13 or higher**.

**Source effect, unchanged**

You gain proficiency in Persuasion and Insight. If already proficient, you add double your proficiency bonus.

**Proposed procedure**

Evaluate Persuasion and Insight separately at acquisition: gain proficiency if untrained, or twice-PB Expertise if already proficient. Use the actual ability for each task, normally Charisma for Persuasion and Wisdom for Insight. Diplomacy still requires an eligible request and a perceivable, understandable interaction. Insight can reveal only what the actual successful task supports; it is neither automatic mind reading nor a guarantee that a suspected statement is false. This feat grants no extra audience, faction rank or negotiated discount.

**Worked adjudications**

- CHA 14, WIS 16 and PB +3 with existing Insight but no Persuasion produces +5 Persuasion and +9 Insight after acquisition.

- A legal choice order acquiring Charismatic first can leave Persuasion proficient before a later Diplomat acquisition, so Diplomat grants Expertise there. Record both events; this is sequential ownership, not free retroactive rewriting.

- An opposed Insight total of 16 against Deception 16 keeps the existing state under current Core ties; Expertise does not create an automatic win.

<details><summary>Complete original source and conference question</summary>

```json
{
  "id": "diplomat",
  "name": "Diplomat",
  "description": "You are skilled in negotiation and persuasion.",
  "prerequisite": "Charisma 13 or higher",
  "effect": "You gain proficiency in Persuasion and Insight. If already proficient, you add double your proficiency bonus.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

Preserve Persuasion and Insight proficiency and apply any existing-proficiency double PB independently. Define timing and overlap with Charismatic/other expertise. Insight is not automatic mind reading, and Persuasion is not compelled consent; actual social procedure and possible failure remain.

</details>

## GE-23 — Naturalist

Source identity: `naturalist`. Original prerequisite: **Wisdom 13 or higher**.

**Source effect, unchanged**

You gain proficiency in Nature and Survival. If already proficient, you add double your proficiency bonus.

**Proposed procedure**

Evaluate Nature and Survival separately at acquisition: gain proficiency if untrained, or twice-PB Expertise if already proficient. Nature remains the relevant knowledge skill, normally Intelligence; Survival remains the actual navigation, tracking or resource-finding skill, normally Wisdom, when the task calls for it. The feat grants no free forage yield, hidden ecological fact, ingredient identity, wilderness immunity or new resource. It does not bypass the actual Supply, source-depletion, route, watch or creature-size procedures. No creature origin or cosmology is inferred from its name.

**Worked adjudications**

- INT 12, WIS 16, PB +2 with Nature trained and Survival untrained gives Nature +5 and Survival +5 after acquisition; equal totals arise from different ability/proficiency contributions.

- Two sources of Survival Expertise use one twice-PB contribution. A tool credential that also fits the task does not add a second PB.

- A successful knowledge check can identify a plant from available evidence. If an area is already depleted, the feat does not make another harvest exist.

<details><summary>Complete original source and conference question</summary>

```json
{
  "id": "naturalist",
  "name": "Naturalist",
  "description": "You have extensive knowledge of nature.",
  "prerequisite": "Wisdom 13 or higher",
  "effect": "You gain proficiency in Nature and Survival. If already proficient, you add double your proficiency bonus.",
  "type": "General",
  "draft": false,
  "deprecated": false,
  "needsReview": false
}
```

Preserve Nature and Survival training and existing-proficiency double PB separately. Define acquisition/later proficiency and strongest expertise handling. Distinguish knowledge, navigation, tracking and resource-finding tasks; no automatic foraging output or access to hidden ecology/cosmology.

</details>

## Evidence and boundary

The 18 examples are authored adjudications, not complete character-builder runtime tests. The local check verifies their explicit arithmetic, six exact source objects, identity/scope and unchanged reviewed manifest. No active rules, character saves, source registries or submitted expedition files are edited. Joint source agreement and exact candidate review still precede operational adoption; numerical balance and human testing remain open.
