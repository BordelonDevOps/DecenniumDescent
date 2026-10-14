"""Consolidate navigation while preserving the complete previous start page."""
from pathlib import Path
from datetime import datetime,timezone
import json,re,shutil
from build_fishing_recipe_candidate import ROOT,GAME,AUDIT,read,sha,dump,write


def main():
    start=GAME/'START_HERE.md';history=GAME/'DEVELOPMENT_STATUS_HISTORY_2026-10-10.md'
    assert not history.exists(),'Preserve existing history; this is a one-time consolidation'
    navigation=[start,AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md',
        AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',
        AUDIT/'FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json',ROOT/'data/playtest/game_development_coverage.json']
    backup=AUDIT/'navigation-before-start-page-consolidation';assert not backup.exists()
    old_hashes={}
    for p in navigation:
        rel=p.relative_to(GAME);dest=backup/rel;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,dest);old_hashes[rel.as_posix()]=sha(p)
    dump(backup/'MANIFEST.json',old_hashes)
    old=start.read_text(encoding='utf-8')
    banner=('# Development status history — snapshot before navigation consolidation\n\n'
        '**Historical snapshot, 10 October 2026.** Open [START_HERE.md](START_HERE.md) for the current position. '
        'Every paragraph and link from the previous start page is preserved below, including older totals and pending labels. '
        'Those statements describe their recorded checkpoints; they are not all current. Original bytes and hashes are also retained in '
        '[the navigation backup](docs/audit/2026-10-08/full-game/navigation-before-start-page-consolidation/MANIFEST.json).\n\n'
        '<!-- BEGIN COMPLETE PREVIOUS START PAGE -->\n\n')
    write(history,banner+old)
    assert history.read_text(encoding='utf-8')[len(banner):]==old
    assert sha(backup/'START_HERE.md')==old_hashes['START_HERE.md']
    coverage=read(AUDIT/'FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json')
    cohort_files=list(coverage['cohortFiles']);new='ABJURATION_CONJURATION_RANK4_SOURCE_PREPARATION.json'
    assert new not in cohort_files;cohort_files.append(new)
    selected=[];book=[];protected={};table=[]
    names=['Low-rank Illusion','Low-rank Universal','Low-rank Transmutation','Low-rank Necromancy',
        'Rank-three Evocation','Remaining rank-three spells','Rank-four Abjuration and Conjuration']
    for name,filename in zip(names,cohort_files):
        data=read(AUDIT/filename);records=data['selectedSpells'];selected+=records;book+=data['currentBookBindings']
        for p,h in data['protectedFiles'].items():
            assert p not in protected or protected[p]==h
            protected[p]=h
        prefix=filename.removesuffix('_SOURCE_PREPARATION.json')
        status=read(AUDIT/(prefix+'_SOURCE_STATUS.json'))
        deferred=sum(r.get('scope')=='post-push receipt only' for r in records)
        table.append(f"| [{name}]({prefix}_SOURCE_AUDIT.md) | {len(records)} | {len(records)-deferred} | {deferred} | {len(data['currentBookBindings'])} | {status['checkCount']} |")
    ids=[r['spellId'] for r in selected]
    deferred=[r['spellId'] for r in selected if r.get('scope')=='post-push receipt only']
    assert len(ids)==len(set(ids))==153 and len(book)==158 and set(deferred)=={'blink','banishment'}
    assert all(sha(GAME/p)==h for p,h in protected.items())
    coverage.update({'distinctPreparedPendingSpellIds':153,'currentBookBindings':158,
        'prePushMechanicalQuestions':151,'postPushReceiptOnlyIds':deferred,
        'protectedInputsUnchanged':len(protected),'cohortFiles':cohort_files,
        'allPendingMinClassRankZeroToFourSourcesCovered':False,
        'minimumRank4AbjurationConjurationSourcesCovered':16,
        'reviewApprovalsGranted':0,'packetsSent':0})
    dump(AUDIT/'FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json',coverage)
    index=['# Prepared spell source conferences','',
        '**Seven packets prepared; none sent or approved.** These retain 153 distinct unfinished identities and 158 exact current-book placements. '
        'There are 151 mechanical source questions and two unchanged receipts (Blink and Banishment) for the post-push cosmology review. '
        'Ordinary spell totals remain 276 operational drafts and 572 unfinished identities out of 848.','',
        '| Source cohort | Identities | Mechanical questions | Post-push receipts | Book bindings | Local source checks |',
        '|---|---:|---:|---:|---:|---:|',*table,'',
        'All unfinished identities with minimum class-access rank 0–3 have source preparation. The rank-four Abjuration/Conjuration cohort adds 16 identities; other rank-four and higher cohorts remain to prepare. '
        'Source preparation precedes GPT decisions, authored cards and separate exact review. It is not operational approval.','',
        'The latest cohort preserves Elemental Drain\'s 2-RP/5-RP conflict, Spell Shield\'s level/Tier conflict and both Alignment Anchor placements (including Cleric rank7/17RP versus Druid rank4/7RP). '
        'Its 17 full Core records, 17 book bindings, 29 reviewed counterparts, six pending comparisons and 37 governing excerpts remain available in the complete evidence.','',
        'The [coverage manifest](FOCUSED_SPELL_SOURCE_PREPARATION_COVERAGE.json) records duplicate checks and current protected-input validation. '
        'Rebase relevant dependencies before dispatching a packet; preserve earlier prepared revisions. Fishing exact review is the current notebook request.','']
    write(AUDIT/'PREPARED_SPELL_SOURCE_INDEX.md','\n'.join(index))
    new_start=r'''# Decennium Descent — start here

**Working folder: `C:\Github\DecenniumDescent`**  
**Current position: 10 October 2026.** The working finish line is a coherent campaign-playtest candidate. Human balance, publication approval and full companion implementation remain separate gates.

**Current joint work:** All 44 Fishing cards are drafted, including 28 public cards. The complete three-part candidate is with [Calibration Review Part 2](https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6aca4e7e-fd2c-83ea-bf0f-971997ed1a9b) for exact review. All 220 local checks pass; the submitted revision is archived. [Dispatch and receipts](docs/audit/2026-10-08/full-game/FISHING_EXACT_PART2_SUBMISSION.json). Fishing approvals remain zero until the actual verdict and any required repairs.

**Owner-directed sequence:** finish the authored candidate and joint whole-game flow review, push to [GitHub](https://github.com/BordelonDevOps/DecenniumDescent), verify the remote commit, then undertake the [careful cosmology review](docs/audit/2026-10-08/full-game/POST_GITHUB_COSMOLOGY_REVIEW.md). No push or cosmology review has occurred.

## Start reading or building a character

| What you need | Open this |
|---|---|
| A Base-class character | [Base classes: start here](DescentReviewChanges/ReviewBible/docs/mechanics/BASE_CLASSES_START_HERE.md), then [character creation and advancement](DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_CREATION_PLAYTEST.md) |
| All Base, Arch and Hero progressions | [17-class library](DescentReviewChanges/ReviewBible/docs/mechanics/CLASS_PLAYTEST_INDEX.md) and [class foundation tables](DescentReviewChanges/ReviewBible/docs/mechanics/CHARACTER_FOUNDATION_TABLES.md) |
| Paladin Oaths and Oathbreakers | [All ten paired paths](DescentReviewChanges/ReviewBible/docs/mechanics/PALADIN_OATHS_AND_OATHBREAKERS.md) |
| Ancestry and background choices | [Ancestries/backgrounds](DescentReviewChanges/ReviewBible/docs/mechanics/ANCESTRY_BACKGROUND_PLAYTEST.md) and [their spell supplement](DescentReviewChanges/ReviewBible/docs/mechanics/ANCESTRY_SPELL_SUPPLEMENT_PLAYTEST.md) |
| Starting gear and item use | [Equipment and acquisition](DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md), [starting packages](DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_STARTING_PACKAGES.md), [item procedures](DescentReviewChanges/ReviewBible/docs/mechanics/EQUIPMENT_ITEM_PROCEDURES.md) |
| Checks, combat and conditions | [Core resolution](DescentReviewChanges/ReviewBible/docs/mechanics/CORE_RESOLUTION_PLAYTEST.md), [combat procedure](DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md), [conditions](DescentReviewChanges/ReviewBible/docs/mechanics/CONDITIONS_PLAYTEST.md) |
| Spell and feat procedures | [Spell integration](DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md), [spell packet entrypoint](DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_PLAYTEST_STARTER.md), [feat index](DescentReviewChanges/ReviewBible/docs/mechanics/FEAT_PLAYTEST_INDEX.md) |
| Crafting, harvesting and recipes | [Shared framework](DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_HARVEST_PLAYTEST.md), [all 16 trades](DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_TRADE_REFERENCE.md), [reviewed recipe index](DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md) |
| Detailed interfaces and remaining work | [75-area development ledger](DescentReviewChanges/ReviewBible/docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md). This links bodies/carrying, healing, companions, damage sharing, Strain, Time Loop and other procedures with their exact scope and evidence. |

## Current completion picture

| Area | Authored or reviewed so far | Still open |
|---|---|---|
| Classes | All 17 Base/Arch/Hero progressions drafted; 1,223 cards | Full cross-system interaction and human balance review |
| Paladin paths | Ten Oath/Oathbreaker pairs; 120 path cards and six shared Oathbreaker cards | Wider interaction and balance review |
| Character foundation | All 17 foundations, advancement and multiclass interfaces jointly reviewed | Remaining choice/dependency and companion integration |
| Ancestries/backgrounds | 14 bases, 45 variants, 20 backgrounds and 17 spell dependencies reviewed in their stated scope | Supply/Reputation/Oracle and other named dependencies; two post-push cosmology branches |
| Equipment | 220 item records, 17 class kits, seven packs and 20 background mappings reviewed | Full crafting outputs, transport, faction/artifact economy and software integration |
| Recipes | **348 of 687 reviewed; 339 remain.** Public: 223 of 433 reviewed | Fishing44 exact review, then 128 gathering-tool and 167 advanced-trade sources; availability and integration remain separate |
| Ordinary spells | **276 operational drafts; 572 unfinished.** All 848 identities and 936 placements preserved | Individual mechanics, remaining source preparation and integration; ten ancestry-only spells remain separate |
| Feats | **8 of 335 reviewed; 327 remain.** Every pending source has focused preparation | GPT source decisions, authored effects and exact review |
| Whole game | 75 aspects tracked; one meets all its closure criteria | Remaining authored-candidate criteria, final flow and delivery. Full Time Loop execution remains unpromoted. |

The current recipe pass includes Alchemy, Herbalism, Cooking, Poisoncrafting, Blacksmithing, Leatherworking, Tailoring and Jewelcrafting. Individual review does not certify ingredient availability, all interactions, runtime parity or balance. The [recipe index](DescentReviewChanges/ReviewBible/docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md) links each reviewed scope and its evidence.

## Development queues

| Workstream | Current evidence and next decisions |
|---|---|
| Fishing | [Draft public guide](DescentReviewChanges/ReviewBible/docs/mechanics/FISHING_RECIPE_PLAYTEST.md), [public cards](DescentReviewChanges/ReviewBible/docs/mechanics/FISHING_PUBLIC_RECIPE_CARDS.md), [220-check local report](docs/audit/2026-10-08/full-game/FISHING_CANDIDATE_VALIDATION.json). Await exact GPT verdict; apply and verify any finite repairs before promotion. |
| Remaining recipes | [Internal trade queue](DescentReviewChanges/ReviewBible/docs/director-only/CRAFTING_REVIEW_QUEUE.md), [128 gathering-tool sources](docs/audit/2026-10-08/full-game/GATHERING_TOOL_SOURCE_AUDIT.md), [167 advanced-trade sources](docs/audit/2026-10-08/full-game/ADVANCED_CRAFT_SOURCE_AUDIT.md) |
| Spells | [Prepared source index](docs/audit/2026-10-08/full-game/PREPARED_SPELL_SOURCE_INDEX.md): seven unsent cohorts, 153 identities, 158 book bindings, 151 mechanical questions and two post-push receipts (Blink and Banishment). Preparation grants no approval. |
| Feats | [Internal feat queue](DescentReviewChanges/ReviewBible/docs/director-only/FEAT_REVIEW_QUEUE.md), including all 327 pending sources and their class/crafting/spell dependencies |
| Expedition to Haven | [26 source/interface cases](docs/audit/2026-10-08/full-game/EXPEDITION_HAVEN_FLOW_SOURCE_AUDIT.md): Supply, Pressure, routes, extraction, transport, reputation and settlement remain to reconcile |
| Bestiary and materials | [Harvest/crafting crosslink audit](docs/audit/2026-10-08/full-game/BESTIARY_CRAFTING_CROSSLINK_AUDIT.md); unresolved labels, units and source contexts are preserved |
| Final delivery | [Joint flow and GitHub delivery gate](docs/audit/2026-10-08/full-game/FINAL_FLOW_AND_GITHUB_DELIVERY.md), [live notebook handoff](docs/audit/2026-10-08/full-game/GPT_REVIEW_CONTINUATION_HANDOFF.md) |

## Source books and authority

The recovered V6 release was owner-approved on 5 August; V7.2 calibration followed on 6 August and remains testing evidence. Current review drafts preserve those sources. The [canon manifest](docs/canon/CANON_MANIFEST.json) assigns authority by domain, rather than filename date.

| Source | File |
|---|---|
| Player rules | [Player Rulebook V6](books/player/Decennium_Descent_Player_Rulebook_v6.docx) |
| Core systems | [Known Descent V2](books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx) |
| Player crafting | [Known Descent V5](books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx) |
| Feat sources | [Compendium](books/player/Decennium_Descent_Feat_Compendium_v1.docx) and [current source registry](src/data/feats.js) |
| Public creatures | [Monster Manual of the Known Descent V2](books/player/Decennium_Descent_Monster_Manual_of_the_Known_Descent_v2.docx) |
| Director material | [The Director's Crucible](docs/manuals/The_Directors_Crucible_Complete_Director_Edition.docx) and [recovered lore addendum](docs/director-only/RECOVERED_THEME_ADDENDUM.md). Director and sealed-bestiary content retain their private audience. |

## Folder map and preserved history

| Location | Purpose |
|---|---|
| `books`, `docs`, `data`, `src` at this root | Recovered main game working tree; the canon manifest identifies authoritative sources |
| `DescentReviewChanges/ReviewBible` | Current assembled review candidate and development tools; this is not a second application to launch |
| `docs/audit/2026-10-08/full-game` | Source evidence, GPT decisions, submitted versions, checks and open questions |
| `DescentReviewChanges/incoming` | Preserved delivery/calibration packs, including V7.2 |
| `DecenniumDescentv6`, `_preserved`, `archive`, `backups` | Earlier snapshots and original files retained for recovery and comparison |
| `Descent assets` | Separate imported asset experiment and tools |
| Codex's folder under `Documents\ChatGPT` | Conversation workspace; the game source is the GitHub folder named at the top |

No original information was deleted during this consolidation. The [complete previous start page](DEVELOPMENT_STATUS_HISTORY_2026-10-10.md) retains every historical paragraph and link, including detailed review counts and superseded checkpoints. The [recovery audit](docs/audit/2026-10-08/AUDIT_REPORT.md), [readiness record](docs/audit/2026-10-08/READINESS.md) and [recipe-history reconciliation](docs/audit/2026-10-08/full-game/CRAFTING_HISTORY_RECONCILIATION.md) retain the earlier recovery trail.
'''
    write(start,new_start)
    # Local links in the concise entrypoint, new index and rendered history all
    # keep the original root context. The raw snapshot remains byte-identical.
    link_count=0
    for p in [start,history,AUDIT/'PREPARED_SPELL_SOURCE_INDEX.md']:
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if re.match(r'^[a-z]+:',link):continue
            assert (p.parent/link.split('#')[0]).exists(),(p.name,link)
            link_count+=1
    observation=read(AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json')
    observation['observedAtUtc']=datetime.now(timezone.utc).isoformat()
    observation['independentProgress'].update({'focusedPendingSpellSourcesPrepared':153,
        'currentBookBindingsAcrossSevenSpellPackets':158,'prePushSpellQuestionsAcrossSevenPackets':151,
        'postPushSpellReceipts':['blink','banishment'],'abjurationConjurationRank4SourcesPrepared':16,
        'abjurationConjurationRank4Checks':11,'abjurationConjurationRank4ProtectedInputs':74,
        'conciseStartPage':True,'fullPreviousStartPagePreserved':history.name})
    observation['currentGoalTurnClassification']='progress:16 more spell sources preserved with15 mechanical questions and Banishment deferred; start page consolidated without losing historical text; Fishing exact review still active on actual C turn'
    observation['consecutiveBlockedGoalTurns']=0
    dump(AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',observation)
    handoff=AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md';text=handoff.read_text(encoding='utf-8')
    addition=('The [rank-four Abjuration/Conjuration audit](ABJURATION_CONJURATION_RANK4_SOURCE_AUDIT.md) preserves16 further identities and17 Core/book bindings, with29 reviewed counterparts,six pending comparisons and37 exact governing excerpts. '
        'Eleven source checks pass across74 protected inputs. Elemental Drain\'s2/5RP and Spell Shield\'slevel/Tier conflicts remain explicit; Alignment Anchor keeps both placements and class costs. '
        'Banishment is receipt-only for post-push cosmology. The [seven-packet index](PREPARED_SPELL_SOURCE_INDEX.md) now covers153 identities/158book bindings:151 mechanical questions andtwo post-push receipts. No new spell approval.\n\n')
    text=text.replace('## Next prepared source evidence','## Next prepared source evidence\n\n'+addition,1);write(handoff,text)
    game_coverage=read(ROOT/'data/playtest/game_development_coverage.json')
    for aspect in game_coverage['aspects']:
        if aspect['id'] in ['DD-03','DD-11','DD-12','DD-13','DD-18','DD-21','DD-26','DD-35','DD-49']:
            for key,suffix in [('sourceEvidence','PREPARATION.json'),('draftEvidence','AUDIT.md'),('validationEvidence','STATUS.json')]:
                path='docs/audit/2026-10-08/full-game/ABJURATION_CONJURATION_RANK4_SOURCE_'+suffix
                if path not in aspect.setdefault(key,[]):aspect[key].append(path)
        if aspect['id']=='DD-12':aspect['openIssues'].append('Seven unsent source cohorts preserve153 identities/158book bindings:151 pre-push mechanical questions and Blink/Banishment post-push receipts. Newly prepared16 rank4 Abjuration/Conjuration identities pass11 source checks; no approvals,276 operational/572 pending unchanged.')
        if aspect['id']=='DD-00':
            aspect.setdefault('completedScopes',[]).append('Start-page navigation consolidated on10October:complete prior42,876-byte page preserved in raw backup and readable root history;current counts and active review separated from historical checkpoints. No source/card/approval changed.')
            aspect.setdefault('sourceEvidence',[]).extend(['DEVELOPMENT_STATUS_HISTORY_2026-10-10.md','docs/audit/2026-10-08/full-game/START_PAGE_CONSOLIDATION_RECEIPT.json'])
    dump(ROOT/'data/playtest/game_development_coverage.json',game_coverage)
    receipt={'status':'PASS navigation consolidation; no source deletion or promotion',
        'previousStartSha256':old_hashes['START_HERE.md'],'rawBackup':'navigation-before-start-page-consolidation/START_HERE.md',
        'readableFullHistory':history.relative_to(GAME).as_posix(),'completePriorTextPreserved':True,
        'newStartSha256':sha(start),'previousBytes':(backup/'START_HERE.md').stat().st_size,'currentBytes':start.stat().st_size,
        'localLinksVerified':link_count,'preparedSpellIdentities':153,'bookBindings':158,
        'prePushQuestions':151,'deferredReceipts':deferred,'protectedSpellInputsUnchanged':len(protected),
        'newSpellApprovals':0,'newRecipeApprovals':0,'sourceInformationDeleted':False,'cosmology':'post-push only'}
    dump(AUDIT/'START_PAGE_CONSOLIDATION_RECEIPT.json',receipt);print(json.dumps(receipt))


if __name__=='__main__':main()
