"""Preserve30 unfinished low-rank Necromancy sources; no operational promotion."""
from copy import deepcopy
import hashlib
import json
from prepare_low_illusion_spell_source_audit import ROOT, GAME, AUDIT, current_book_rows, digest
from prepare_combat_feat_source_audit import section

QUESTIONS = {
    'rotting-touch': 'Preserve Touch and exactly1 necrotic per round for3 rounds. Decide hostile application attack/save, first tick and all three native regular markers, repeat casting, suppression, concentration and removal. Separate a source damage sequence from disease, Bleeding, healing prohibition or physical decomposition; none follows merely from the name. No extra-turn or initiative-reset ticks.',
    'finger-of-the-dead': 'Preserve1d4 necrotic and heal1HP. Define attack/save, healing recipient and whether the heal requires a hit, positive resolved damage or actual donor-funded HP loss. Resolve zeroHP, temp/formHP, floors, immunity, trivial/friendly targets and repeat casts using existing drain rules. Any finite donor/reserve or no-recursion integration must be explicit, preserving the promised heal rather than silently deleting it.',
    'corpse-light': 'Preserve a real corpse glowing green. Specify eligible body/remains, light radius/intensity, lifetime despite Instantaneous, simultaneous casts, suppression and whether movement carries the light. Define effects of raising, resurrection, destruction or consumption of that same body. No automatic undead detection, corpse preservation, creature animation, information or origin/afterlife claim.',
    'whispers-from-beyond': 'Preserve WIS save and disadvantage on the next attack. Define eligible targets/senses, expiry of the unused mark, precise attack commitment and cancellation/automatic-result handling. Do not replace the attack penalty with Frightened or a forced action. Multiple same-source marks need finite arbitration without generating a second attack or importing a spirit-contact explanation.',
    'spectral-claw': 'Preserve1d6 slashing plus1 necrotic at the printed30ft range. Specify attack/save and a single mixed-type damage event with actual defense/critical rules for each component. Determine whether a visible claw exists only for resolution. No persistent weapon, extra natural attack, remote manipulator, physical claw material or automatic scaling solely from the name.',
    'gravewind-flicker': 'Preserve both pushing an object and shutting a door. Define finite target mass/size, displacement, range/line of effect, held/resisted objects and ordinary hinges, locks or obstructions. Keep actual custody and final supported placement. Decide occupied doorways and hazards without granting automatic crushing damage, unlocking, creature movement or persistent control.',
    'toll-the-dead': 'Preserve1d8 necrotic or1d12 if already injured. Define attack/save, the pre-event injured predicate and its snapshot across normalHP, formHP, tempHP and maximum changes. Wounds and current missingHP are different records; choose explicitly. No extra injury, implied cantrip scaling or stronger die based on damage inflicted by this same unresolved event.',
    'death-whisper': 'Preserve one question to an actual corpse. Define body condition, age, language, possible answers/knowledge, response length, refusal/deception and a finite recast/corpse-family limit. Compare reviewed Speak with Dead and pending Lesser without merging identities. Describe only the playable information interface; do not settle soul location, afterlife, identity ownership or cosmic origin.',
    'bone-shard': 'Preserve1d6 piercing and ignoring non-metal armor. Set exact attack resolution and substitute AC calculation, distinguishing armor base from DEX, shields, cover, natural armor, wards and mixed materials. Bind treatment to actual equipment records; names alone do not certify material. Define projectile/remains custody without granting free valuable bone/ammunition or ignoring every nonmetal defensive effect.',
    'wither-plant': 'Preserve a nonmagical plant withering and dying. Define finite size/extent and whether rooted colonies, ordinary trees, cultivated crops or creature-stat plants qualify; establish resistance for any hostile creature target if allowed. Preserve actual remaining mass and ecological/harvest state. No automatic creature death by botanical name, poisoning, plant-material multiplication or new ingredient availability.',
    'blood-trickle': 'Preserve1 damage per round for3 rounds. Decide whether this is source-qualified Bleeding, damage type, eligible anatomy, application resolution, first tick and exactly three regular opportunities. Reconcile Medicine/healing cure endpoints, suppression and same-source replacement. Do not accidentally add generic Bleeding damage on top or turn repeat casts into extra native ticks.',
    'decay': 'Preserve immediate2d6 necrotic followed by1d6 each round for3 rounds. Define application attack/save, success branch, tick markers, concentration, repeated casts and ending. Distinguish this ordinary spell identity from the existing custom Decay healing prohibition; the shared name does not import that prohibition or erase the three later damage installments.',
    'dread-whisper': 'Preserve WIS save, flee for1round and1d4 psychic. Specify damage on each save outcome, finite forced movement direction/path/timing, available movement/actions, impassable or dangerous routes and opportunities. Reconcile current hard-denial and Frightened rules explicitly without silently granting Frightened or replacing the printed flight with only disadvantage.',
    'putrefy': 'Preserve the corpse becoming unusable for divine magic. Resolve a finite corpse-local mechanical blocker, duration, target eligibility, removal, destruction/reconstruction and interaction with current resurrection/animation/information effects. The term divine is not an existing universal source classification: use explicit reviewed source bindings or identify a precise deferred dependency. Do not define gods, souls, afterlife or cosmology, nor silently broaden this to every spell or identity-wide permanent denial.',
    'pact-of-bone': 'Preserve both+1AC and+2 necrotic resist. Reconcile the numeric resistance with current binary halving resistance through an explicit NEW rule, including damage ordering/rounding and modifier families. Define target, lifetime/concentration and recasting despite Instantaneous. No automatic bone armor, body change, healing, additional HP or extrapolated patron/pact cosmology.',
    'soul-tap': 'Preserve the wording conflict: catalog says steal1d6HP and Resonance on hit; Core says steal1d6HP/mana on hit. Decide one roll versus separate quantities, HP/RP branches, damage type, hit resolution, actual donor funding and recipient caps with cost2RP paid first. Address temp/formHP, zero pools, immunity/floors, self/friendly targets and causal recursion. Do not invent a soul currency or treat the ambiguous mana wording as approved unlimited recovery.',
    'eyes-of-the-grave': 'Preserve undead detection within60ft. Specify instantaneous snapshot versus sustained duration, perception/line-of-effect/obstruction rules and exactly what information is learned: presence, direction, count or location. Use actual creature eligibility, not appearance or names. Distinguish reviewed Sense Undead; no automatic identity, alignment, motive, hidden lore or cosmic-origin revelation.',
    'ray-of-sickness': 'Preserve2d8 poison damage and Poisoned on failed CON. Reconcile whether the save controls damage as well as the condition and whether any separate attack is required. Set finite Poisoned duration/end saves, immunity distinctions and repeated casts. No invented disease, poison dose material, extra damage pulses or automatic condition when the applicable save succeeds.',
    'inflict-wounds': 'Preserve a Touch attack for3d10 necrotic with ordinary spell-attack and critical handling. Specify eligible targets and actual touch geometry. The Core Healing tag contains no healing clause: record that mismatch without inventing HP gain, corpse revival or wound cure. The name also does not grant an automatic Wound beyond the reviewed damage/Wound procedure.',
    'corpse-puppet': 'Preserve animating a small corpse for simple tasks. Define exact body eligibility, task menu, profile, speed/load, commands, range, finite duration/concentration and number controlled. Integrate one real body identity and existing companion budgets where applicable, including damage/end/remains. Do not silently upgrade it to a combat minion, spellcaster, free skilled worker, living resurrection or renewable corpse/harvest donor.',
    'bone-armor': 'Preserve armor from actual bones,+2AC for1hour. Specify bone quantity/mass, custody/consumption or return, legal wearer/fit, donning, armor-versus-ward classification and AC family with existing armor/shields. Resolve suppression, breakage, removal and expiry using the same material identity. No new bones, permanent marketable armor, healing, unused craft stock or durability refresh from recasting.',
    'speak-with-dead-lesser': 'Preserve exactly one question to a recently deceased corpse. Define recently with a finite elapsed window, body/knowledge/language/response rules and recast limits, comparing Death Whisper and reviewed Speak with Dead without automatic identity merge. Explain their source-specific mechanical differences. This does not decide soul availability, afterlife travel, divine authority or resurrection.',
    'summon-bone-archer': 'Preserve one undead archer,HP20,2d6 piercing and concentration up to1minute. Supply complete AC,speed,size,senses,saves,attack modifier/range,initiative and command/offense costs under current creature rules. Define creation space, replacement/count, ammunition, ending/remains and resource provenance. Keep summon origin unresolved cosmologically; no extra command pool, renewable corpse fuel or free salvage/ammunition.',
    'ghoul-touch': 'Preserve1d8 necrotic and Paralyzed on failed CON at Touch. Clarify any attack requirement, damage on save outcomes, finite paralysis duration, repeat saves/removal and current hard-denial scope. Resolve separate condition/damage immunity. No unprinted poison disease, stench aura, indefinite paralysis or delayed extra attacks inherited from an external version.',
    'cursed-soulrot': 'Preserve1d6 necrotic per round for5 rounds. Define application attack/save, exactly five native markers, concentration, repeated casts and suppression/removal. Decide explicit Curse typing if any; name alone cannot select curse-removal eligibility or create a soul injury. No permanent maxHP loss, healing denial or skipped-turn catch-up damage without a new source decision.',
    'drain-vigor': 'Preserve-2STR and2d6 necrotic as separate clauses. Define attack/save and outcomes, penalty duration/concentration, score floor and derived checks/attacks/damage/carrying, same-source stacking and restoration. Distinguish capacity changes from damage or healing. The word drain grants no caster HP/RP/stat increase, permanent advancement loss or automatic incapacitation.',
    'gentle-repose': 'Preserve a corpse from decay through a finite target/duration/concentration decision despite Instantaneous. State exactly which physical-age/harvest clocks pause and how elapsed time resumes. Distinguish corpse condition from elapsed resurrection/question windows; extending those requires explicit authority. Retain body identity and prior damage/age, without restoring consumed remains, producing repeat harvests or deciding afterlife/soul state.',
    'ray-of-enfeeblement': 'Preserve halving damage from the target\'s Strength attacks. Define attack/save, lifetime/concentration, repeat endings and the actual Strength-attack predicate, including mixed damage/riders. Specify rounding and ordering with resistance/other reductions. No STR score reduction, halving every spell or environmental packet, HP loss, condition or new damage because Core tags this Damage.',
    'blindness-deafness': 'Preserve choice of Blinded or Deafened and CON negates. Set choice timing, finite lifetime/concentration, repeat saves/removal and same-source replacement when modes differ. Apply actual reviewed condition/sense rules and source-specific immunity. No both-modes default, eye/ear destruction, perception through walls or loss of unrelated alternate senses.',
    'wither': 'Preserve a limb becoming withered and weak. Give a finite eligible-anatomy/limb selection, attack/save, duration/concentration and exact bounded mechanical penalty with end/removal. Compare Disable Limb and Drain Vigor rather than merging them. Do not infer permanent amputation, automatic Wound, paralysis, item loss or repeated penalties for the same anatomy from the sparse wording.'
}
PENDING_COUNTERPARTS = ['disable-limb', 'feral-might', 'steel-skin', 'shadow-blade', 'light', 'mage-hand', 'snap-freeze']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    inherited = json.loads((AUDIT/'LOW_ILLUSION_SPELL_SOURCE_PREPARATION.json').read_text(encoding='utf-8'))
    protected = deepcopy(inherited['protectedFiles'])
    assert all(sha(GAME/p) == h for p, h in protected.items())

    def read(path):
        protected[path.relative_to(GAME).as_posix()] = sha(path)
        return json.loads(path.read_text(encoding='utf-8-sig'))

    catalog = read(ROOT/'data/public/spell_playtests/catalog.json')
    rows = catalog['spells']; by_id = {r['id']: r for r in rows}
    all_low = {r['id'] for r in rows if r['operational'] is None and min(v['rank'] for v in r['classAccess'].values()) <= 2}
    selected = [r for r in rows if r['id'] in all_low and r['schools'][0] == 'Necromancy']
    assert len(selected) == 30 and {r['id'] for r in selected} == set(QUESTIONS)
    previous = [inherited] + [read(AUDIT/f'LOW_{school}_SPELL_SOURCE_PREPARATION.json') for school in ['UNIVERSAL', 'TRANSMUTATION']]
    prior_ids = [r['spellId'] for d in previous for r in d['selectedSpells']]
    assert len(prior_ids) == len(set(prior_ids)) == 78 and not set(prior_ids).intersection(QUESTIONS)
    assert set(prior_ids) | set(QUESTIONS) == all_low
    sources = read(ROOT/'data/playtest/spell_sources/catalog.json')
    core = read(ROOT/'data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json')
    book = current_book_rows(); bindings = []; effect_differences = []
    for row in selected:
        assert row['source']['original'] == sources[row['id']]
        for entry in row['source']['coreEntries'] + row['source']['possibleHistoricalAliases']:
            assert entry['original'] == core['spells'][entry['index']]
        for placement in row['source']['original']['placements']:
            matches = [b for b in book if b['name'] == row['name'] and b['school'] == placement['school'] and b['level'] == placement['level']]
            assert len(matches) == 1
            bindings.append({'spellId': row['id'], 'catalogPlacement': placement, 'currentBookRow': matches[0], 'summaryDifferencePreserved': placement['summary'] != matches[0]['summary']})
            for entry in row['source']['coreEntries']:
                original = entry['original']
                if placement['school'] == original['school'] and placement['level'] == original['level'] and placement['summary'] != original['effect']:
                    effect_differences.append({'spellId': row['id'], 'catalogSummary': placement['summary'], 'coreEffect': original['effect'], 'coreIndex': entry['index']})
    counterparts = [r for r in rows if r['operational'] is not None and 'Necromancy' in r['schools']]
    counterparts += [by_id[id] for id in ['gust', 'stoneflesh', 'shield', 'magehand'] + PENDING_COUNTERPARTS]
    assert len({r['id'] for r in counterparts}) == len(counterparts)
    mentions = [r for r in read(ROOT/'data/public/spell_playtests/class_name_mentions_for_review.json') if r.get('spellId') in QUESTIONS]
    manifest = read(ROOT/'data/public/class_playtests/manifest.json')
    classes = {r['class']: r for r in manifest['classes']}; class_records = []
    for mention in mentions:
        path = (ROOT/'docs/mechanics'/classes[mention['class']]['data']).resolve(); data = read(path)
        if mention['location'] == 'engine':
            record = {'engine': data.get('engine', [])}
        else:
            matches = [c for c in data['cards'] if c['id'] == mention['location']]
            assert len(matches) == 1
            record = {'card': matches[0]}
        class_records.append({'mention': mention, **record, 'file': path.relative_to(GAME).as_posix(), 'scope': 'Textual comparison only; no ordinary spell grant or identity merge.'})
    equipment = read(ROOT/'data/playtest/equipment_acquisition_candidate.json')
    armor = [r for r in equipment['items'] if r['category'] == 'Armor and shields']
    excerpts = deepcopy(inherited['currentGoverningExcerpts'])
    extra = {
        'HEALING_DEATH_PLAYTEST.md': None,
        'FORM_TEMP_HP_PLAYTEST.md': None,
        'CREATURE_LIFECYCLE_PLAYTEST.md': None,
        'HEALING_PULSE_PLAYTEST.md': ['Keep the original clock', 'Targets, payments and separate budgets', 'Finite installments and independent components'],
        'BUFFER_FEAT_PLAYTEST.md': ['Shared rules', 'Blood Ritual — Magic; Constitution13+ and character level4+', 'Necrotic Affinity — Magic; Religion proficiency **or** character level8+', 'Lifeleech — Magic; actual spellcasting ability', 'Soul Cage feat — Magic; level8+ and (Lifeleech **or** actual spellcasting ability)'],
        'CRAFTING_HARVEST_PLAYTEST.md': ['Material identity, consumption and substitution', 'Identify and harvest', 'Preservation and spoilage'],
        'EQUIPMENT_ACQUISITION_PLAYTEST.md': ['Armor and shields', 'Fit and size'],
        'CONTROL_STATES_PLAYTEST.md': ['Curse and disease', 'Speed arbitration'],
        'CONDITIONS_PLAYTEST.md': ['Bleeding', 'Paralyzed', 'Poisoned'],
    }
    for name, headings in extra.items():
        path = ROOT/'docs/mechanics'/name; text = path.read_text(encoding='utf-8')
        protected[path.relative_to(GAME).as_posix()] = sha(path)
        for heading in headings or [None]:
            excerpts.append({'file': path.relative_to(GAME).as_posix(), 'sha256': sha(path), 'heading': heading or 'entire guide', 'exactText': section(text, heading) if heading else text})
    records = [{'spellId': r['id'], 'questionId': f'NE-{i+1:02}', 'fullSourceAndCurrentAccessRecord': r, 'recordSha256': digest(r), 'individualQuestion': QUESTIONS[r['id']]} for i, r in enumerate(selected)]
    complete_low_bindings = len(bindings) + sum(len(d['currentBookBindings']) for d in previous)
    checks = [
        ('30 exact remaining low-rank Necromancy identities', len(records) == 30),
        ('Disjoint from78 earlier focused sources', not set(prior_ids).intersection(QUESTIONS)),
        ('Four prepared cohorts cover all108 pending min-access-rank0..2 identities', set(prior_ids) | set(QUESTIONS) == all_low and len(all_low) == 108),
        ('All original catalog and Core rows retained exactly', True),
        ('30 current-book bindings;111 across four cohorts', len(bindings) == 30 and complete_low_bindings == 111),
        ('276 operational and572 pending spells unchanged', sum(r['operational'] is not None for r in rows) == 276 and sum(r['operational'] is None for r in rows) == 572),
        ('Every full source has an individual question', all(len(r['individualQuestion']) > 190 for r in records)),
        ('Soul Tap wording difference retained', {r['spellId'] for r in effect_differences} == {'soul-tap'}),
        ('21 operational andseven pending counterparts remain distinct', len(counterparts) == 28 and sum(r['operational'] is not None for r in counterparts) == 21),
        ('Every current class mention has an actual source binding', len(class_records) == len(mentions)),
        ('Actual armor records included without inferred material classification', bool(armor)),
        ('Every excerpt matches its current protected guide', all(e['exactText'] in (GAME/e['file']).read_text(encoding='utf-8') for e in excerpts)),
        ('All protected inputs unchanged', all(sha(GAME/p) == h for p, h in protected.items())),
    ]
    assert all(ok for _, ok in checks), [name for name, ok in checks if not ok]
    counts = {'sourceSpells': 848, 'operationalSpells': 276, 'remaining': 572, 'selectedLowNecromancy': 30, 'exactCoreEntries': sum(len(r['source']['coreEntries']) for r in selected), 'currentBookBindings': len(bindings), 'reviewedCounterparts': 21, 'pendingCounterparts': 7, 'classComparisonRecords': len(class_records), 'governingExcerpts': len(excerpts), 'armorComparisonRecords': len(armor), 'catalogCoreEffectDifferences': len(effect_differences), 'currentBookSummaryDifferences': sum(r['summaryDifferencePreserved'] for r in bindings), 'focusedPendingSpellSourcesPrepared': 108, 'currentBookBindingsAcrossFourPackets': complete_low_bindings}
    data = {'status': 'prepared-not-sent; source questions only', 'commonOperationalQuestion': inherited['commonOperationalQuestion'], 'selectedSpells': records, 'currentBookBindings': bindings, 'completeCounterparts': counterparts, 'classComparisonRecords': class_records, 'actualArmorComparisonRecords': armor, 'catalogCoreEffectDifferences': effect_differences, 'currentGoverningExcerpts': excerpts, 'currentRankCosts': catalog['costByRank'], 'currentClassProgression': catalog['classProgression'], 'counts': counts, 'checks': [{'name': name, 'pass': ok} for name, ok in checks], 'protectedFiles': protected, 'spellsApproved': 0, 'sourceInformationDeleted': 0, 'cosmology': 'Strictly post-push: use existing mechanical corpse/identity/source interfaces without defining soul, deity, afterlife or origin. Preserve unresolved source words and name any actual post-push dependency.', 'futureDispatch': 'Rebase dependencies after active Fishing source conference. Full source decisions precede authoring and separate exact review. All108 prepared low-rank identities remain unapproved.'}
    dump(AUDIT/'LOW_NECROMANCY_SPELL_SOURCE_PREPARATION.json', data)
    lines = ['# Low-rank Necromancy spell source audit', '', data['status'], '', data['commonOperationalQuestion'], '', 'All30 selected identities retain their complete catalog record,30 exact Core rows and30 current-book placements. Soul Tap retains its HP-and-Resonance versus HP/mana wording conflict. Twenty-one operational comparison spells,seven pending spells and actual armor records accompany the questions. No spell is promoted by preparation.', '', '| Case | Spell | Full-source question |', '|---|---|---|']
    lines += [f"| {r['questionId']} | {r['fullSourceAndCurrentAccessRecord']['name']} ({r['spellId']}) | {r['individualQuestion']} |" for r in records]
    lines += ['', 'The four prepared cohorts now cover all108 currently unfinished identities with a minimum class-access rank of0,1 or2, preserving111 current-book placements. This is preparation coverage, not spell completion:276 of848 ordinary identities remain operational and572 unfinished. Existing guides and original sources are unchanged.', '', 'The current Fishing source conference remains active. These questions are unsent. Corpse and recovery interfaces can be discussed mechanically; gods, souls, afterlife and cosmic origin remain for the careful review after the authorized GitHub push and remote verification.', '']
    report = '\n'.join(lines)
    (AUDIT/'LOW_NECROMANCY_SPELL_SOURCE_AUDIT.md').write_text(report, encoding='utf-8')
    packet = 'PREPARED LOW-RANK NECROMANCY SOURCE CONFERENCE — NOT SENT.\n\n' + report + '\nCOMPLETE SOURCE AND CURRENT DEPENDENCY EVIDENCE\n' + json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    path = AUDIT/'CODEX_LOW_NECROMANCY_SPELL_SOURCE_PREPARED.txt'; path.write_text(packet, encoding='utf-8', newline='\n')
    status = {'status': 'prepared-not-sent', 'packetFile': path.name, 'characters': len(packet), 'packetSha256': sha(path), 'counts': counts, 'checkCount': len(checks), 'protectedFilesUnchanged': len(protected), 'spellsApproved': 0, 'sourceInformationDeleted': 0, 'cosmology': 'post-push only'}
    dump(AUDIT/'LOW_NECROMANCY_SPELL_SOURCE_STATUS.json', status)
    print(json.dumps(status))

if __name__ == '__main__':
    main()
