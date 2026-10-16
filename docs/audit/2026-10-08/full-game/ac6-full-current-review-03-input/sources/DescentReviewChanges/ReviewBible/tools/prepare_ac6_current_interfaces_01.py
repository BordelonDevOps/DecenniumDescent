"""Preserve the complete AC6 scope and record independently found interface gaps.

Preparation only. Does not adopt spells, change source catalogs, or contact GPT.
"""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded, digest
from prepare_ac5_current_interfaces_01 import at


def read(p):
    return json.loads(p.read_bytes())


def main():
    out = A / 'AC6_CURRENT_SOURCE_INTERFACE_AUDIT_01.json'
    checkfile = A / 'AC6_CURRENT_SOURCE_INTERFACE_CHECK_01.json'
    forgefile = R / 'data/director/spell_proposals/resonance_forge_revision_02.json'
    assert not any(p.exists() for p in [out, checkfile, forgefile])
    now = datetime.now(timezone.utc).isoformat()
    history_path = R / 'data/director/spell_proposals/abjuration_conjuration_rank6.json'
    history = read(history_path)
    catalog_path = R / 'data/public/spell_playtests/catalog.json'
    index_path = R / 'data/public/spell_playtests/authored_review_index.json'
    catalog, index = read(catalog_path), read(index_path)
    lookup = {x['id']: (i, x) for i, x in enumerate(catalog['spells'])}
    entries = {x['id']: x for x in index['entries']}
    checks = []

    def ck(name, value):
        checks.append({'check': name, 'pass': bool(value)})
        assert value, name

    ck('current ordinary spell count', index['authoredCounts'] == {'reviewed': 435, 'pending': 413})
    source_paths = {history_path, catalog_path, index_path, Path(__file__).resolve()}
    source_paths.update(G / p for p in history['sourceFiles'])
    ac5 = read(A / 'ac5-current-review-02-input/CURRENT_REVIEW_INPUT.json')
    # Include actual modern governing files, not old embedded copies as authority.
    source_paths.update(G / b['path'] for b in ac5['sourceBindings'] if b['path'].startswith('DescentReviewChanges/ReviewBible/docs/') or '/cosmology/' in b['path'])
    class_paths = [G / b['path'] for b in ac5['classFiles']]
    source_paths.update(class_paths)
    source_paths.update(A / n for n in ['AC4_EXACT_ACCEPTANCE_03_RECEIPT.json', 'BANISHMENT_EXACT_ACCEPTANCE_04_RECEIPT.json', 'AC5_CURRENT_REVIEW_02_SUBMISSION_RECEIPT.json'])
    source_paths.add(G / 'docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md')
    current_records = []
    for old in sorted(history['records'] + history['completeUntouchedDeferredReceipts'], key=lambda x: x['questionId']):
        ident = old['spellId']; i, card = lookup[ident]
        ck('preserved complete source/access ' + ident, card == old['fullSourceAndCurrentAccessRecord'])
        ck('still pending ' + ident, entries[ident]['authoredStatus'] == 'pending-authored-procedure')
        current_records.append({'spellId': ident, 'questionId': old['questionId'], 'catalogPointer': f'/spells/{i}', 'completeCurrentSourceAndAccess': card, 'currentAuthoredIndexEntry': entries[ident], 'historicalRecord': old,
            'currentScope': 'Full operational authoring and joint review required. Earlier pre-push receipt restriction is historical; verified push prerequisite has been satisfied.'})
    ck('all fourteen identities and sixteen placements retained', len(current_records) == 14 and sum(len(x['completeCurrentSourceAndAccess']['source']['original']['placements']) for x in current_records) == 16)

    comparison_ids = ['resonance-anchor', 'spell-seal', 'corruption-cleanse', 'counterspell', 'dispel-magic', 'dispel-magic-lesser', 'greater-dispel',
        'dimensional-anchor', 'corruption-barrier', 'crystalline-barrier', 'alignment-lock', 'alignment-anchor', 'alignment-suggestion', 'alignment-purge',
        'alignment-sanctuary', 'alignment-shield', 'faction-ally', 'faction-champion', 'faction-portal', 'alignment-portal', 'planar-protection',
        'planar-ally-minor', 'planar-window', 'arcane-portal', 'banishment', 'banish-elemental', 'elemental-banishment', 'planar-binding',
        'summon-air-pet', 'summon-water-pet', 'summon-greater-fire-pet', 'summon-spectral-steed', 'conjure-elemental-lance', 'chain-lightning',
        'resonance-nexus', 'resonance-dampening-field', 'resonance-influence', 'fabricate', 'fate-coin', 'true-seeing']
    comparisons = []
    for ident in comparison_ids:
        i, card = lookup[ident]; entry = entries[ident]
        f = (index_path.parent / entry['procedureFile']).resolve()
        ck('comparison in repository ' + ident, f.is_relative_to(G))
        document = read(f); source_paths.add(f)
        pointer = entry.get('wholeCardPointer', entry['procedurePointer'])
        whole = at(document, pointer)
        ck('comparison identity ' + ident, whole.get(entry.get('wholeCardIdField', 'id')) == ident)
        rec = {'id': ident, 'catalogPointer': f'/spells/{i}', 'completeCatalogCard': card, 'currentAuthoredIndexEntry': entry, 'authoredFile': info(f), 'wholeCardPointer': pointer, 'completeAuthoredCard': whole}
        if entry.get('sharedRulesPointer'):
            rec['completeSharedRules'] = at(document, entry['sharedRulesPointer'])
        if entry.get('supportingProfilePointers'):
            rec['supportingProfiles'] = {p: at(document, p) for p in entry['supportingProfilePointers']}
        comparisons.append(rec)

    blacksmith_path = R / 'data/playtest/blacksmithing_recipe_candidate.json'
    smith = read(blacksmith_path); source_paths.add(blacksmith_path)
    ck('reviewed blacksmithing shared classification is magical', smith['sharedOperationalProfile']['classification']['magical'] is True)
    ck('all twenty-seven public smith recipes are magical imprints', len(smith['cards']) == 27 and all(c['operational']['effect']['classification'] == 'durable-magical-nonartifact' for c in smith['cards']))
    recipes = [{'pointer': f'/cards/{i}', 'completeCard': smith['cards'][i]} for i in [0, 25]]
    ck('concrete recipe identities', [x['completeCard']['recipeId'] for x in recipes] == ['recipe-42', 'recipe-628'])

    bestiary_path = R / 'data/director/bestiary_source_candidate_internal.json'
    bestiary = read(bestiary_path); source_paths.add(bestiary_path)
    cr6 = [{'pointer': f'/records/{i}', 'completeRecord': x} for i, x in enumerate(bestiary['records']) if (x.get('statBlock') or {}).get('printedCoreFields', {}).get('challengeRating') == '6']
    ck('bounded bestiary source scan', len(bestiary['records']) == 67 and len(cr6) == 8)

    oldforge = next(x for x in history['records'] if x['spellId'] == 'resonance-forge')
    old_eligibility = "NEW eligible RP-funded production is one otherwise legal Blacksmithing creation order whose whole active manufacturing process is mundane heating/shaping/joining of real metal, or an independently specified complete mundane metal-body recipe from another trade whose actual source explicitly permits an ordinary forge/anvil for that whole process. A general Tinkering, Enchanting or Rune Carving recipe is not eligible merely because it contains metal. Keep its actual trade/level/formula access, input roles/quantities, packaging, tools, auxiliaries, output card, permissions and required site category. The forge supplies the compatible ordinary forging station/heat only; it cannot waive a genuinely required specialized facility or classify a field-prohibited recipe as field crafting. No unknown recipe, rare ingredient, magical imbuement, living growth, incubation/calendar wait, attunement, encoding, recharge, servicing, repair, rework or formula research is completed by this production interface."
    new_eligibility = "NEW revision: eligible RP-funded production includes one otherwise legal, complete, reviewed Blacksmithing creation order, including its actual magical nonartifact recipe-imprint process. This is an explicit spell-specific acceleration of that entire recipe's active creation work; it is not restricted to mundane heating or metal-only ingredients. Use only a recipe with a complete operational output and a Forge-and-Anvil production interface whose real workpieces fit this fixture. All actual skill levels, tools, training, formula/discovery access, ingredients, ordered complete mundane base reservations, model/size/grade restrictions, work phases, output limits and required site category still apply. The forge supplies its compatible station and the stated work replacement; it supplies no base item, ingredient, formula or automatic success. An independently specified complete mundane metal-body recipe can also qualify if its source expressly permits this station for its entire active manufacture. Enchanting, Rune Carving and Tinkering are not admitted merely for containing metal: another trade needs its own complete reviewed compatibility rule. The forge cannot waive a required specialized facility or turn a field-prohibited recipe into field crafting. Living growth, incubation/calendar waits, attunement, recharge, servicing, repair, rework and formula research receive no manufacturing credit. Printing the recipe's actual magical imprint on its reserved body is now expressly permitted; inventing an artifact or an unreviewed output is not."
    old_learning = "NEW any work order using this magical work-replacement interface earns no numerical creation/failure-research trade XP, while an actual success still enters its recipe first-success history; this learning tradeoff is an explicit proposal like the earlier unadopted Fabricate exception, not an inherited reviewed rule. Ordinary unaccelerated work using only the forge as a station keeps its own actual XP rules."
    new_learning = "NEW revision: retain the reviewed crafting learning procedure for the actual lead, including the actual recipe/trade identity, first-success history, triviality and ordinary success awards. The forge adds no XP multiplier, second work order, assistant award or reset of history. A failure-research award still requires its independently satisfied actual-input, actual-work and useful-finding predicates; credited recipe minutes are not falsely reported as elapsed personal work. The older proposal's blanket no-XP penalty is withdrawn in this unadopted revision because no governing source supplies it. Other pending spells, including Fabricate, are not changed by this proposal."
    ck('exact old forge paragraphs located', oldforge['procedure'].count(old_eligibility) == 1 and oldforge['procedure'].count(old_learning) == 1)
    old_persistence = 'Finished mundane output made from real stock persists after this forge ends;'
    ck('old forge output persistence located', oldforge['procedure'].count(old_persistence) == 1)
    new_procedure = oldforge['procedure'].replace(old_eligibility, new_eligibility).replace(old_learning, new_learning).replace(old_persistence, 'Finished output made from real reserved bodies and stock persists under its actual recipe-imprint procedure after this forge ends;')
    new_procedure += "\n\nNEW explicit phase bridge: a completed ten-minute cycle grants its stated recipe-work credit within the current original phase. It does not automatically establish a new safe phase boundary. Reaching that source phase's full adjusted credit requirement stabilizes the incorporated inputs and progress under the source rule; elapsed perishability and personal work/rest clocks advance by actual time only. Forced interruption before a phase stabilizes loses that phase's unfinished credited progress, including credit from earlier completed cycles in that same phase, as the reviewed ordinary phase rule requires. Paid cycle RP is never returned. A voluntarily scheduled pause is safe only at an actual completed phase boundary or another source-permitted breakpoint. This bridge does not rewrite the recipe's material, failure or completion process."
    forge_cases = [
        ('FG-R02-01', 'Actual Refined Gale Sword creation', 'Wizard 11 with INT +4/PB +4, RP40, legally knows/prepares Resonance Forge; no price modifier or strain surcharge. A separate proficient STR +3/PB +4 Blacksmith at trade level3 uses recipe-42 for their first nontrivial success, in a proper expedition station with all required tools and real inputs. One undamaged Standard Medium longsword base (3lb, HP5, reference15gp), the specified Forge water occurrence (25lb, nonconsumed), two leather strips and one Vulture claw are reserved; actual workpiece stock fits the 500lb limit. Commit13RP; four completed cycles cost20 further protected RP and take40 actual minutes, crediting the whole240-minute phase. Wizard RP ends7. Check natural8+3+4=15 againstDC12: Standard. Same longsword becomes its magical +1 attack/+1 damage imprint, remains HP5, and gains no air-damage rider. Lead earns ordinary first-success4XP; recipe reference92gp plus real base15gp gives107gp reference, with no guaranteed buyer.'),
        ('FG-R02-02', 'Forge Dwarf time and output quality', 'Independent otherwise identical recipe-42 order with an actually eligible Forge Dwarf lead: four source hours become180 adjusted minutes by the reviewed 0.75 rule. Three full cycles cost15 protected RP and30 actual minutes; caster RP40-13-15=12. Actual total15 againstDC12 is Standard, treated as Exceptional output by the ancestry. Choose durability: undamaged base maximum/current5 becomes6, not a larger accuracy or damage bonus. First nontrivial success still gives4XP, not an extra ancestry award. No second multiplier shortens the fixed ten-minute cycle.'),
        ('FG-R02-03', 'Interrupted unstable phase loses earlier credit', 'Independent240-minute recipe-42 phase: caster starts40RP, spends13 to cast, then pays three5RP cycles. First two cycles complete at actual20minutes; third is interrupted at minute26. RP12 remains. No part of the third cycle is credited. Because the single original240-minute phase never stabilized, forced interruption also loses its prior120 credited minutes under the phase rule. Stock keeps its real condition and26minutes of actual aging. Starting anew needs real remaining RP;12RP cannot finance four new cycles. No refund, rest or saved phase is fabricated.'),
        ('FG-R02-04', 'Real base damage survives a Flawed imprint', 'Independent recipe-42 order reserves an undamaged HP5 longsword. A real compatible intervening damage event leaves currentHP3 before final completion; the surviving positive-HP base stays legal. Final craft total10 againstDC12 is Flawed. Its ordinary maximum5 becomes2; actual damage deficit2 is retained, leaving currentHP0. The same body bears a dormant Broken imprint, produces no working sword and receives no automatic repair from the forge. Genuine repair must use its own actual source.'),
        ('FG-R02-05', 'Source recipe and material identity remain exact', 'Recipe-628 Alien-Chitin Lamellar needs actual formula access, Blacksmithing5, its one reserved complete eligible scale-mail base, chitin/ingot/strips/rivets, proper expedition station and DC13. It is eligible despite its nonmetal chitin input because the actual reviewed Blacksmithing interface supplies the Forge-and-Anvil process. An otherwise legal unmodified480-minute order requires eight cycles,80 actual minutes and40 protected RP beyond the13RP initial cast; one40RP caster cannot alone fund all nine payments. An independently capable real sponsor can supply their own cycles under the full attendance rule. No fictional RP pool or missing material is created.'),
        ('FG-R02-06', 'Protected conversion, support and ending', 'The initial cast uses the actual applicable ordinary spell-price rules. Each later forge cycle remains a magical nonspell operation with exactly5 actual RP conversion principal; spell-only Nexus/Influence/Dampening interfaces do not price it. A sponsor must attend the full actual ten minutes and gains no assistant bonus merely for paying. If the real support for the300lb fixture fails or the fixture is suppressed during a cycle, apply its exact ending/interruption procedure, actual stock placement and original phase history; no completed product or RP refund is produced.'),
    ]
    forge = {'id': 'DD-RESONANCE-FORGE-REVISION-02', 'recordedAtUtc': now, 'status': 'UNADOPTED AND UNSENT; complete local proposed correction awaiting actual GPT review.',
        'spellId': 'resonance-forge', 'questionId': 'AC6-12', 'completeCurrentSourceAndAccess': lookup['resonance-forge'][1],
        'historicalProposal': oldforge, 'procedure': new_procedure,
        'explicitChanges': ['Admit actual reviewed Blacksmithing magical-imprint creation instead of excluding every current public recipe.', 'Keep ordinary reviewed XP and first-success/triviality rules instead of the unsupported blanket XP ban.', 'Make original phase stabilization explicit; completed cycles do not independently stabilize unfinished phases.'],
        'remainingNewChoicesForJointReview': ['Eight-hour fixture, 300lb mass, AC17/HP50, five-foot/500lb work envelope.', 'Five actual protected RP and ten actual work minutes replace up to sixty adjusted manufacturing minutes.', 'All other old numerical choices and source classifications remain unadopted; review the entire resulting procedure.'],
        'completeReadRecipes': recipes, 'sharedBlacksmithProfile': smith['sharedOperationalProfile'],
        'workedCases': [{'id': ident, 'title': title, 'proposedAdjudication': body, 'evidenceKind': 'Authored conditional example, not runtime or human test', 'sourceRefs': [{'path': history_path.relative_to(G).as_posix(), 'pointer': '/records/9'}, {'path': blacksmith_path.relative_to(G).as_posix(), 'pointer': '/sharedOperationalProfile'}, {'path': blacksmith_path.relative_to(G).as_posix(), 'pointer': '/cards/25' if ident == 'FG-R02-05' else '/cards/0'}, {'path': 'DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md', 'section': 'Active time and expedition scheduling; Quality and finite output; Trade XP and specialties'}]} for ident, title, body in forge_cases],
        'newSpellAdoptions': 0, 'sourceInformationDeleted': 0, 'runtimeTestsExecuted': 0}
    forgefile.write_bytes(encoded(forge)); source_paths.add(forgefile)

    issue_rows = [
        ('AC6-C01', 'all', 'Keep all fourteen identities and sixteen placements. Three former post-push receipts now require full procedures. Alignment Nexus has distinct Divination6/60ft/13RP and Conjuration8/120ft/21RP operations; actual class access chooses its branch. No flattening into a rank-six portal or a single universal effect.'),
        ('AC6-C02', 'globe-of-invulnerability', 'Keep source rank-five-or-lower spell blocking and explicitly adjudicate its NEW origin/recipient geometry. Current low-rank spells can have remote legally authorized origins and actual teleport endpoint exceptions; imaginary trajectories are not physical paths. Class magical nonspells need their actual classification, not a name-based rank.'),
        ('AC6-C03', 'globe-of-invulnerability', 'Explicitly reconcile protected incoming rank-four ordinary Banishment mandatory closure with BAN-CLOSE-03: its narrow terminal-return exception overrides endpoint transport-prevention only, not terrain. A new Globe cannot trap an ended Banishment cell by applying an ordinary arrival rule without confronting that exact accepted exception.'),
        ('AC6-C04', 'guards-and-wards', 'The older three-constituent parcel must preserve all components and one parent rank/source. Source-specific removal of a lock or mark differs from parent dispel. True Seeing remains pending in the current index; do not cite its old presumed permissions as an adopted rule. Actual current sight/obscurement rules still govern.'),
        ('AC6-C05', 'forbiddance', 'Use accepted AC4-ALIGN01 order for effective axes; earliest eligible Lock/Anchor applies last, Suggestion baseline and Purge retain their own procedure. Unknown/protected axes are not guessed. Specify formation/entry/regular-start exposure and owner-attached timing without creating extra turns.'),
        ('AC6-C06', 'resonance-seal', 'Review explicit self/cross-family exclusions, source-owner permission, seven-day maximum and suppression/resumption anchor. Reviewed Resonance Anchor stays normally dispellable; Spell Seal is pending. The old draft cannot silently amend another pending spell or accepted Anchor. Spatial eligibility must not freeze creatures, cells or source clocks.'),
        ('AC6-C07', 'corruption-purge', 'Preserve ALL qualifying corruption effects, not just one minor symptom, while respecting real special removal protections and intrinsic Oracle Curse. Null Veil has three exact accepted purge routes and is not generically Corruption by appearance; no implicit cleanse of Veil, numeric tracks, souls or completed consequences.'),
        ('AC6-C08', 'summon-greater-air-pet;faction-army;planar-ally-greater', 'Correct blanket zero-HP disappearance under qualifying Null damage: finite summons remain the same NullDisabled0 body while source exists. Genuine expiry, replacement, concentration end and non-damage source termination remain real. Define actual legal healing targets for each new profile; the AC4 two-profile healing extension is scoped and does not automatically cover new summons.'),
        ('AC6-C09', 'summon-greater-air-pet', 'Preserve HP65/AC18/2d8 wind slash/50% projectile miss chance. Decide separate projectile lineage and the actual d2 timing, automatic/natural20 hits, multicomponent impacts, redirected events and explosion geometry. Fate Coin expressly rerolls one physical die from a qualifying observed original roll, including non-d20 pools; assess this exact source rather than assuming all reroll abilities are attack-only.'),
        ('AC6-C10', 'elemental-warp-field', 'Resolve actual five damage types, allied eligibility and live ten-foot aura; one defense step per applicable recipient. Post-defense transferred damage gains no second resistance or prevention. Mixed packets, actual immunity and source-specific transfer restrictions retain their exact ordering.'),
        ('AC6-C11', 'chain-arc', 'Preserve six targets,3d8 and random successors. Complete pre-damage snapshot and finite uniform selection; no hidden candidate roster, ally omission or same-body repeat. Specify how actual legal reaction/reroll sources affect the selection die and why removing a prior body does not redraw established successors.'),
        ('AC6-C12', 'conjure-skybrand-weapon;forbiddance;chain-arc', 'Declare exact damage dealer and root creation event for fields, later commands and each attack. An effect-only Skybrand has no creature dealer identity by default. Apply actual caster Veil at each genuinely new attack/root, while descendants of an existing root inherit its flag. Pure transfers preserve and actual new reflections re-evaluate.'),
        ('AC6-C13', 'resonance-forge', 'Substantive gap: all27 current public Blacksmithing cards are magical nonartifact imprints. Old mundane-only eligibility excludes them. Review the complete local revision02 with real recipes42 and628, their body reservations, inputs, tools, formula/site, actual work phases, final quality and persistent damage.'),
        ('AC6-C14', 'resonance-forge', 'Five protected RP cycle principal is not initial casting RP or a spell price. Read exact class/resource rules and eventual accepted Nexus; no conversion discount, pooled imaginary sponsor or duplicate attendance. Credit work only on complete cycles and stabilize only at source phase boundaries. Review ordinary XP restoration versus the old unadopted no-XP tradeoff explicitly.'),
        ('AC6-C15', 'faction-army', 'Preserve3d6 actual soldiers with distinct bodies, not one stat block multiplied into free attacks. Resolve shared command/offense, chosen source profile and affiliation versus membership/standing. Rank-five Champion remains live and unadopted now; refresh its exact result before conferring on Army. Intrinsic equipment and real cargo retain different identities.'),
        ('AC6-C16', 'planar-barrier', 'Fully author the wall that blocks extraplanar creatures: geometry, actual predicate/provenance, unknown eligibility, physical/forced/carrying contact, already intersecting bodies, occupied resumption and actual teleport endpoint exceptions. Creature type, current travel and mortal Wheel name are not interchangeable proof of origin. Do not reduce it to a cosmetic or same-plane-only wall.'),
        ('AC6-C17', 'planar-ally-greater', 'Fully preserve one-hour CR6 extraplanar assistance. The67-record internal source candidate has eight printed CR6 identities, all still operationally unreviewed. Type/name alone establishes no eligible extradimensional origin or complete operational profile. Review exact source evidence or explicitly author a complete summon-only profile for the intended role, including its CR-certification limit; do not substitute the weak Minor profile or claim existing monster approval.'),
        ('AC6-C18', 'alignment-nexus', 'Author both printed operations: insight-zone bonuses for Divination6 and a genuine empowering planar portal for Conjuration8. Keep actual per-class school/rank, range and cost, genuine arrival/return/custody, stable plane record and alignment changes. Owner locks forbid inferred Wheel ontology or new soul/native identity. Unknown world facts remain unknown; any needed playable campaign metadata must be explicitly NEW.'),
        ('AC6-C19', 'all', 'Local source/pointer checks do not certify semantics, runtime, balance or humans. Preserve22 original case strings separately from current adjudications; include original14 question and old16 issue dispositions plus every new finding. Fresh AC5 acceptance will require a binding and dependency refresh, not use of pending drafts as authority.'),
    ]
    issues = [{'id': i, 'spellScope': s.split(';'), 'requiredReview': t} for i, s, t in issue_rows]
    scenarios = [
        ('globe-of-invulnerability', 'Outside rank5 multi-target cast with one protected inside recipient and one outside; discounted rank6 still bypasses the ceiling.'),
        ('globe-of-invulnerability', 'Actual Wizard class nonspell Dispel versus ordinary spell Dispel at the protected anchor; identify each exact card and legal origin.'),
        ('globe-of-invulnerability', 'Accepted ordinary Banishment ends at t60 with its origin inside a Globe; apply the narrow mandatory-return exception and actual occupied placement.'),
        ('globe-of-invulnerability', 'Existing attached buff and an externally anchored ongoing field overlap the sphere; distinct suppression, ending and spent-tick behavior.'),
        ('guards-and-wards', 'Two eligible doors, one mundane lock, one removed closure layer and one parent dispel; no regeneration of an ended component.'),
        ('guards-and-wards', 'Actual Invisible entrant, ward veil, physical stone and six-second outline; explain location knowledge versus sight eligibility.'),
        ('forbiddance', 'Two overlapping field sources, different simultaneous alignment snapshots and later Lock/Anchor/Purge change; one real family exposure and no instant eligibility-change pulse.'),
        ('forbiddance', 'Owner-attached companion and initiative transition at an already-spent pulse; no extra regular turn or duplicate damage.'),
        ('resonance-seal', 'One-minute mobile concentration source with permitted seven-day Seal; actual source clock ends first.'),
        ('resonance-seal', 'Suppressed Seal and a moving live parent; reanchoring and an actually legal higher-rank dispel without casting through blocked magic.'),
        ('resonance-seal', 'Cross-family Seal/Anchor attempt and legal replacement; preserve accepted Anchor and pending Spell Seal boundaries.'),
        ('corruption-purge', 'Multiple removable corruption records plus intrinsically protected Oracle Curse, Null Veil, Wound and numeric Exposure; actual all-record purge but no invented cures.'),
        ('corruption-purge', 'Divisible environmental overlap, indivisible protected generator and a barrier removed during resolution; finite captured snapshot does not expand.'),
        ('summon-greater-air-pet', 'Natural20 projectile with two damage components, independent miss-position explosion and legal observed Fate Coin d2 reroll; one lineage, not repeated independent chances.'),
        ('summon-greater-air-pet', 'Veiled character damage takes pet to NullDisabled0; actual legal healing restores same body before original expiry, then real source ending.'),
        ('elemental-warp-field', 'Mixed17fire/9necrotic packet, ordinary resistance, pre-defense share and post-defense transfer; no second reduction.'),
        ('chain-arc', 'Six preselected distinct bodies, unseen eligible successor, friendly candidate, immune first target and later removed target; actual random draw and visibility.'),
        ('chain-arc', 'Legal Fate Coin versus hidden Director selection die; separate information access and actual original-roll replacement guard.'),
        ('conjure-skybrand-weapon', 'Two attacks in one command with Veil suppressed before first and active before second through a genuine independent change; establish real dealer/root at each attack.'),
        ('conjure-skybrand-weapon', 'No command, invalid second target, interrupted source and same-round other companion; two printed attacks without extra offense.'),
        ('resonance-forge', 'Execute all six FG-R02 conditional examples against actual recipes and governing text; correct proposed math/eligibility where needed.'),
        ('resonance-forge', 'Actual initial cast pricing under then-accepted Nexus/Dampening/Influence versus subsequent protected5RP nonspell cycle; real sponsor attendance and no spell refund.'),
        ('faction-army', '3d6=12 but nine of eighteen declared spaces remain; nine separate bodies and one command, including independent damage and real cargo.'),
        ('faction-army', 'NullDisabled soldier stays a body until healed or independently ended; parent suppression/expiry and ordinary items never duplicate intrinsic equipment.'),
        ('planar-barrier', 'Known qualifying extraplanar creature, actually ordinary local creature and unknown provenance; no inference from Elemental/Fey/Humanoid labels.'),
        ('planar-barrier', 'Forced collision, grappling passenger and suppressed wall resuming on occupied space; no crushing, arbitrary ejection or frozen falling.'),
        ('planar-ally-greater', 'Full one-hour CR6-role ally profile, commandable action, actual caster costs and one-hour expiry with carried real property.'),
        ('planar-ally-greater', 'Blocked arrival and destination or return obstruction under its specifically authored summoning model; no automatic import of Banishment closure.'),
        ('alignment-nexus', 'Cleric11 Divination6/13RP versus Druid15 Conjuration8/21RP and their distinct60/120ft operations; no rank-six portal access from a global header.'),
        ('alignment-nexus', 'Insight-zone eligibility under accepted alignment overlays, unknown axes and actual timed bonus use; no hidden alignment roster.'),
        ('alignment-nexus', 'Genuine empowering portal traversal, legal destination and finite return/cargo history without adopting mortal Wheel geography.'),
        ('alignment-nexus', 'Caster/recipient alignment changes, suppression, closure and independent clock while on another plane; actual source-defined consequences, not reset time.'),
    ]
    required_cases = [{'id': f'AC6-N{i:02d}', 'spellId': s, 'requiredScenario': t, 'status': 'Required future authored example; not yet resolved or executed'} for i, (s, t) in enumerate(scenarios, 1)]
    bindings = [info(p) for p in sorted(source_paths)]
    for b in bindings:
        ck('source available and exact ' + b['path'], info(G / b['path']) == b)
    original_cases = [{'spellId': x['spellId'], 'originalText': t, 'id': t.split(':', 1)[0]} for x in history['records'] for t in x['workedCases']]
    ck('twenty-two original examples', len(original_cases) == 22 and len({x['id'] for x in original_cases}) == 22)
    ck('six complete new forge examples', len(forge['workedCases']) == 6)
    report = {'id': 'DD-AC6-CURRENT-INTERFACES-01', 'recordedAtUtc': now,
        'status': 'UNSENT independent preparation. All fourteen spell identities remain pending. AC5 is actively being reviewed; refresh those dependencies before dispatch.',
        'counts': {'identities': 14, 'printedPlacements': 16, 'historicalFullProposals': 11, 'historicalDeferredIdentitiesNowInFullScope': 3, 'historicalCases': 22, 'currentComparisons': len(comparisons), 'currentClassFiles': len(class_paths), 'newInterfaceIssues': len(issues), 'requiredAdditionalExamples': len(required_cases), 'newCompleteForgeExamples': 6},
        'selectedRecords': current_records, 'historicalSharedProposal': history['sharedProposal'], 'historicalIssues': history['explicitJointIssues'], 'originalExamples': original_cases,
        'completeCurrentComparisons': comparisons, 'classFiles': [info(p) for p in class_paths],
        'manualReadScope': 'All eleven historical spell procedures and their22cases, all14current source/access records, current Null lifecycle/root sections, relevant crafting work/quality/XP rules, complete Blacksmith recipes42/628 and shared Blacksmith rules, exact Minor Planar Ally/Resonance Anchor/Corruption Cleanse/Fate Coin cards; other complete comparison cards/class envelopes are included for subsequent review, not claimed independently reviewed by this preparation.',
        'currentReviewIssues': issues, 'requiredAdditionalExamples': required_cases, 'forgeRevision': info(forgefile),
        'blacksmithEvidence': {'source': info(blacksmith_path), 'publicRecipeCount': 27, 'allMagicalNonartifactImprints': True, 'completeReadCards': recipes, 'sharedProfile': smith['sharedOperationalProfile']},
        'greaterAllyBestiaryEvidence': {'source': info(bestiary_path), 'scanRecordCount': 67, 'exactPrintedCr6Count': 8, 'completeMatchingRecords': cr6, 'scope': 'Bounded source scan and current review status, not an exhaustive lore/origin determination or creature approval. All eight source candidates are operationally unreviewed. Actual type is not extraplanar provenance. Preserve CR6 role without invented certification.'},
        'sourceBindings': bindings, 'sourceRefreshRequiredBeforeDispatch': ['Resolve active AC5 joint conference and refresh every affected full comparison/acceptance/source binding.', 'Include complete canonical current sources and explicit owner cosmology locks; old embedded snapshots remain history.', 'Author complete Planar Barrier, Greater Planar Ally and both Alignment Nexus operations, not permanent receipt-only deferrals.', 'Review full Forge revision and each scoped issue with actual GPT; no new provisional decisions are accepted by this file.'],
        'newSpellAdoptions': 0, 'sourceInformationDeleted': 0, 'runtimeTestsExecuted': 0, 'humanPlaytested': False}
    out.write_bytes(encoded(report))
    ck('inputs preserved after preparation', all(info(G / b['path']) == b for b in bindings))
    checkfile.write_bytes(encoded({'recordedAtUtc': now, 'report': info(out), 'forgeRevision': info(forgefile), 'checks': checks, 'checkCount': len(checks), 'failureCount': 0, 'validationScope': 'Source identity, preserved records, pointer identities and preparation counts only; semantic findings remain for actual joint review.', 'sourceInformationDeleted': 0, 'newSpellAdoptions': 0}))
    print(json.dumps({'report': info(out), 'forgeRevision': info(forgefile), 'counts': report['counts'], 'sources': len(bindings), 'checks': len(checks), 'failures': 0}))


if __name__ == '__main__':
    main()
