"""Render the authored-game coverage ledger without promoting discussion to completion."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]
AUDIT = PROJECT / 'docs/audit/2026-10-08/full-game'
DATA = ROOT / 'data/playtest/game_development_coverage.json'
DOC = ROOT / 'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md'


def main():
    if not DATA.exists():
        rows = []
        for line in (AUDIT / 'GPT_COMPLETE_COVERAGE_REVIEW.md').read_text(encoding='utf-8').splitlines():
            cells = [cell.strip().replace('**', '') for cell in line.strip('|').split('|')]
            if len(cells) != 5 or not re.fullmatch(r'\d+', cells[0]):
                continue
            i = int(cells[0])
            rows.append({'id':f'DD-{i:02}', 'number':i, 'domain':cells[1], 'requiredCoverage':cells[2],
                         'notebookInitialAssessment':cells[3], 'acceptanceGate':cells[4],
                         'status':'discussed', 'closure':'open', 'reviewEvidence':['docs/audit/2026-10-08/full-game/GPT_COMPLETE_COVERAGE_REVIEW.md'],
                         'sourceEvidence':[], 'draftEvidence':[], 'validationEvidence':[], 'humanEvidence':[],
                         'openIssues':['Complete the source audit and individual acceptance criteria.'],
                         'completionClass':'human-gate' if i in (71,72,73) else 'release-gate' if i==68 else 'authored-candidate'})
        assert len(rows)==75 and {r['number'] for r in rows}==set(range(75))
        # Only scoped claims already supported by prior local reviews are carried forward.
        rowmap = {r['number']:r for r in rows}
        rev = 'DescentReviewChanges/ReviewBible/'
        rowmap[0].update(status='partially-validated',sourceEvidence=['docs/canon/CANON_MANIFEST.json','START_HERE.md'],
            validationEvidence=['docs/audit/2026-10-08/classes/CLASS_PASS_VALIDATION.json'],
            openIssues=['Complete rule provenance and consistent candidate entrypoint across all 75 areas.'])
        rowmap[1].update(status='source-audit-in-progress', sourceEvidence=[rev+'docs/mechanics/DESIGN_DOCTRINE.md'],
            openIssues=['Review a concise player promise and check it against setting, campaign and mechanics.'])
        for i in (2,3,15,17,23,24):
            rowmap[i].update(status='source-audit-in-progress', sourceEvidence=['docs/audit/2026-10-08/full-game/CORE_RESOLUTION_SOURCE_EVIDENCE.json'],
                openIssues=['Confer on core resolution, death timing and Wound conflicts; finish remaining domain-specific rules.'])
        for i in (4,5,6,7,8):
            rowmap[i]['sourceEvidence']=[rev+'docs/mechanics/CHARGEN_PROGRESSION.md',rev+'docs/mechanics/CLASS_PLAYTEST_RULES.md']
            rowmap[i]['openIssues']=['Reconcile older chargen/path/progression guidance with the current class candidate and approved sources.']
        for i in (9,10):
            rowmap[i].update(status='validated-in-stated-scope',
                sourceEvidence=[rev+'data/playtest/class_sources'],draftEvidence=[rev+'docs/mechanics/CLASS_PLAYTEST_INDEX.md'],
                validationEvidence=['docs/audit/2026-10-08/classes/CLASS_PASS_VALIDATION.json'],
                reviewEvidence=['docs/audit/2026-10-08/classes'],
                openIssues=['Authoring/acquisition checks passed for 17 families and 1223 cards; game-wide interactions and human use remain open.'])
        for i in (11,12,13):
            rowmap[i].update(status='partially-reviewed',sourceEvidence=[rev+'data/playtest/spell_sources'],
                draftEvidence=[rev+'docs/mechanics/SPELL_PLAYTEST_STARTER.md',rev+'docs/mechanics/SPELL_INTEGRATION_RULES.md'],
                reviewEvidence=['docs/audit/2026-10-08/spell-integration/REVIEW_DISPOSITION.md'],
                validationEvidence=[rev+'docs/mechanics/SPELL_PLAYTEST_VALIDATION.json'],
                openIssues=['72 individual spell drafts reviewed; 776 unfinished. Complete aliases, rituals and all class-specific repertoire interfaces.'])
        for i in (16,18,19,20,21,35,41):
            rowmap[i]['status']='partially-reviewed'
            rowmap[i]['draftEvidence']=[rev+'docs/mechanics/CLASS_PLAYTEST_RULES.md',rev+'docs/mechanics/SPELL_INTEGRATION_RULES.md']
            rowmap[i]['reviewEvidence']=['docs/audit/2026-10-08/spell-integration/REVIEW_DISPOSITION.md']
            rowmap[i]['openIssues']=['Existing shared limits reviewed in class/spell scope; complete all remaining interfaces and content references.']
        for i in (30,36,37,38,39,40,42,43,44,45,51,55,56):
            rowmap[i]['sourceEvidence']=[rev+'docs/mechanics/GAMEPLAY_LOOP_CANON.md']
            rowmap[i]['openIssues']=['An existing procedure is available. Audit its domain authority, conflicts and interfaces rather than treating it as absent.']
        for i in (69,70):
            rowmap[i].update(status='partially-validated',validationEvidence=['docs/audit/2026-10-08/classes/CLASS_PASS_VALIDATION.json',rev+'docs/mechanics/SPELL_PLAYTEST_VALIDATION.json'],
                openIssues=['Existing class and spell tests have limited stated scopes. Extend meaningful cross-system scenarios as implementations are completed.'])
        DATA.parent.mkdir(parents=True,exist_ok=True)
        DATA.write_text(json.dumps({'schemaVersion':'1.0','objective':'Complete authored campaign-playtest candidate with every aspect discussed and reviewed',
            'status':'ACTIVE-INCOMPLETE','aspects':rows,
            'completionPolicy':'Discussion, indexing, source counts, generic templates and blocked labels are not completion. Close an aspect only when its source audit, operational authored coverage, adversarial review and appropriate validation are evidenced. Any intentionally excluded option needs an explicit reviewed disposition, not a blanket unfinished status. Human sessions, numerical balance and publication approval remain separate gates.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    packet = json.loads(DATA.read_text(encoding='utf-8'))
    rows = packet['aspects']
    assert len(rows)==75 and len({r['id'] for r in rows})==75
    for row in rows:
        for field in ['sourceEvidence','draftEvidence','reviewEvidence','validationEvidence','humanEvidence']:
            assert all((PROJECT/path).exists() for path in row[field]), (row['id'],field)
        if row['closure']=='closed':
            assert not row['openIssues'] and all(row[k] for k in ['sourceEvidence','draftEvidence','reviewEvidence','validationEvidence'])
    lines=['# Complete game development coverage','',
           '**Active development.** This ledger covers 75 areas agreed with the GPT notebook. It separates discussion from source audit, authored rules, adversarial review, validation and actual human play. Every area remains visible until its acceptance criteria are met.','',
           '[Development roadmap](DEVELOPMENT_ROADMAP.md) · [Machine-readable ledger](../../data/playtest/game_development_coverage.json) · [Full notebook conference](../../../../docs/audit/2026-10-08/full-game/GPT_COMPLETE_COVERAGE_REVIEW.md)','',
           '## Completion standard','',packet['completionPolicy'],'',
           'Retain approved books and source variants. Confer with GPT on conflicts and consequential choices, supply exact evidence, test counterexamples, and save both the decision and its verified correction. A new rule stays explicitly provisional until promoted. Do not delete material unless both the file audit and notebook review establish that it is obsolete.','',
           '## Review order','',
           '1. Resolve shared vocabulary, rolls, time, actions, conditions, movement, defenses, death and recovery.','2. Complete character construction and every player option: all class stages, spells, feats, ancestry, backgrounds and equipment.','3. Complete opposition, encounters, hazards, rewards, crafting and the expedition-to-Haven economy.','4. Reconcile history, geography, factions, social play, the decennial cycle and campaign endings. Follow the owner-directed post-push sequence for religion/cosmology; preserve its sources and deferred dependencies.','5. Finish Director procedures, representative adventures, onboarding, reference material, accessibility, companion state and separate distribution builds.','6. Run reproducible checks, then prepare human playtests and track balance and publication as distinct gates.','',
           '## Coverage and next evidence','', '| Area | Current status | Next required evidence |','|---|---|---|']
    for path in packet.get('historyReferences', []):
        assert (PROJECT / path).is_file(), path
        index = lines.index('## Completion standard')
        lines[index:index] = [f'[Preserved checkpoint history](../../../../{path}) — earlier queue stages remain available verbatim.', '']
    for row in rows:
        issue=' '.join(row['openIssues']) or 'Acceptance evidence recorded.'
        lines.append(f"| [{row['number']}. {row['domain']}](#area-{row['number']}) | {row['status']} | {issue.replace('|','/')} |")
    lines += ['', '## Acceptance criteria', '']
    for row in rows:
        lines += [f"<a id=\"area-{row['number']}\"></a>",f"### {row['number']} {row['domain']}",'',row['requiredCoverage']+'.','', '**Acceptance:** '+row['acceptanceGate']+'.','']
    DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f"PASS: {len(rows)} coverage areas; {sum(r['closure']=='closed' for r in rows)} fully closed; scoped prior work retained; evidence paths valid")


if __name__=='__main__':main()
