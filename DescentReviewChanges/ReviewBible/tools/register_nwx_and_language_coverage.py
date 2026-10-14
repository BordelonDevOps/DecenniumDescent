"""Record fulfilled teaching review and submitted language conference without domain closure."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import copy
import build_game_coverage

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G/'docs/audit/2026-10-08/full-game'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p): return p.relative_to(G).as_posix()
def dump(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    receipt = A/'NWX_LANGUAGE_COVERAGE_REGISTRATION.json'
    backup = A/'navigation-before-nwx-coverage-registration'
    assert not receipt.exists() and not backup.exists()
    status = read(R/'docs/playtest/ONBOARDING_REVIEW_STATUS.json')
    assert sha(G/status['receipt']) == status['receiptSha256']
    assert all(sha(G/p)==h for p,h in status['manuscriptHashes'].items())
    fulfilled = read(G/status['receipt'])
    assert fulfilled['completionGateSatisfied'] and not fulfilled['dd01Closed']
    language = read(A/'LANGUAGE_COMMUNICATION_V2_SUBMISSION.json')
    assert language['sourceVerdictPending'] and language['actualPromptMatches']
    refresh = read(A/'QUEUED_HANDOFFS_AFTER_NWX_REFRESH.json')
    assert len(refresh['packets']) == 4
    assert all(sha(G/x['preparationFile'])==x['preparationSha256'] for x in refresh['packets'])
    data = R/'data/playtest/game_development_coverage.json'
    doc = R/'docs/mechanics/GAME_DEVELOPMENT_COVERAGE.md'
    start = G/'START_HERE.md'
    handoff = A/'GPT_REVIEW_CONTINUATION_HANDOFF.md'
    paths = [data,doc,start,handoff]
    previous = {rel(p):sha(p) for p in paths}
    for p in paths:
        q=backup/rel(p);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
        assert sha(q)==sha(p)
    dump(backup/'MANIFEST.json',previous)
    ledger=read(data);before=copy.deepcopy(ledger)
    rows={r['id']:r for r in ledger['aspects']}
    selected=['DD-01','DD-58','DD-60','DD-61','DD-62','DD-66']
    common='First exact six-manuscript teaching review fulfilled under NWX-01–06: sixteen corrections, twenty case dispositions, 200 reproduced immutable-source checks, eighteen focused authored/static adjudications and 128 entry-path links/anchors. Reviewed teaching/editorial scope only; no new mechanics or class/spell/feat approvals, human session outcome, runtime certification or final whole-game flow.'
    issues={
        'DD-01':['The charter is a reviewed source-grounded editorial synthesis. Test every completed major system against its promise and record remaining contradictions; DD-01 final systemic consistency remains open. Human readability and balance retain separate gates. Cosmology and the seasonal chapter remain deferred until the authorized push and verified remote commit.'],
        'DD-58':['The six-step session-zero procedure and twelve-row table agreement passed exact authored teaching review. Carry it through final whole-game flow as remaining expedition/content procedures settle. Actual new-group use and human usability are separate, unperformed checks; no numerical or canon rule is added by the table agreement.'],
        'DD-60':['The current first-character/first-turn/casting/rest/advancement entry path is reviewed in its stated teaching scope. Complete expedition/content dependencies and the starter-session flow required by the acceptance gate. An actual new group has not yet demonstrated a starter session without owner intervention; historical quickstart/session-app material remains preserved separately.'],
        'DD-61':['Current newcomer guides and Resonance reference passed their scoped review and link checks. Complete travel, Director and remaining class-resource references, then measure the two-lookup acceptance criterion across the full frequently-used mechanic set.'],
        'DD-62':['Mira’s creation, turns, casting, recovery and advancement examples passed the finite source/arithmetic and NWX boundary review. Complete and check the remaining companion, travel, crafting and death examples against the eventual full candidate; these checks are not gameplay-runtime or human balance evidence.'],
        'DD-66':['The six teaching/editorial manuscripts have completed exact terminology, timing and reference corrections. Finish the full-candidate terminology dictionary, lint and mechanical ambiguity review after remaining content decisions; current teaching acceptance does not close game-wide editing.'],
    }
    for rid in selected:
        row=rows[rid]
        row['status']='teaching-scope-reviewed-broader-gate-open'
        row['openIssues']=issues[rid]
        row.setdefault('completedScopes',[]).append(common)
        for field,values in {
            'reviewEvidence':[fulfilled['verdictFile']],
            'validationEvidence':[status['receipt'],rel(R/'docs/playtest/ONBOARDING_REVIEW_STATUS.json')],
            'draftEvidence':list(status['manuscriptHashes']) if rid in ['DD-60','DD-66'] else
                [rel(A/'DESIGN_CHARTER_CANDIDATE.md')] if rid=='DD-01' else
                [rel(R/'docs/playtest/SESSION_ZERO_PLAYTEST.md')] if rid=='DD-58' else
                [rel(R/'docs/playtest/RESONANCE_CHEATSHEET.md')] if rid=='DD-61' else
                [rel(R/'docs/playtest/FIRST_BARD_WALKTHROUGH.md')],
        }.items():
            for value in values:
                if value not in row[field]:row[field].append(value)
    language_row=rows['DD-46']
    language_row['status']='source-conference-submitted-verdict-pending'
    language_row['openIssues']=[
        'LA-01–16 were submitted once in Calibration Review Part 2 with 152 current complete source payloads and the fulfilled onboarding receipt. The completed advanced Scribing/device interfaces are included. Capture the actual source decisions, author the language/communication candidate and complete exact review and character-record integration; no language rule or cosmology interpretation is approved merely by submission.',
        'Keep pending spell/feat effects in their dedicated queues and retain LA-16 as a literal post-push cosmology receipt.'
    ]
    for p in [A/'LANGUAGE_COMMUNICATION_V2_PREPARATION.json',A/'LANGUAGE_COMMUNICATION_V2_REVIEW_SCOPE.md',A/'LANGUAGE_ADVANCED_INTERFACE_ADDENDUM.json',A/'LANGUAGE_COMMUNICATION_V2_SUBMISSION.json']:
        if rel(p) not in language_row['sourceEvidence']:language_row['sourceEvidence'].append(rel(p))
    unchanged=[r['id'] for r in before['aspects'] if r['id'] not in selected+['DD-46']]
    assert all(rows[r['id']]==r for r in before['aspects'] if r['id'] in unchanged)
    assert all(rows[r['id']]['acceptanceGate']==r['acceptanceGate'] and rows[r['id']]['closure']==r['closure'] and rows[r['id']]['humanEvidence']==r['humanEvidence'] for r in before['aspects'])
    dump(data,ledger)
    build_game_coverage.main()
    text=start.read_text(encoding='utf-8-sig')
    text=text.replace('**Current position: 10 October 2026.**','**Current position: 11 October 2026.**')
    text=text.replace('[complete-file handoff](docs/audit/2026-10-08/full-game/FEAT_COMPLETE_FILE_HANDOFF_PREPARATION.json) consolidates236 files; it is unsent and requires a refresh after intervening decisions.','[refreshed complete-file handoff](docs/audit/2026-10-08/full-game/FEAT_COMPLETE_FILE_HANDOFF_V2_PREPARATION.json) supplies268 files, including completed crafting/teaching evidence and preserved prior versions. It remains unsent; incorporate intervening language decisions before dispatch.')
    text=text.replace('Full evidence and the [completed-Scribing update](docs/audit/2026-10-08/full-game/LANGUAGE_COMMUNICATION_V2_REVIEW_SCOPE.md) are prepared; focused GPT review remains pending.','Full evidence and the [completed-Scribing update](docs/audit/2026-10-08/full-game/LANGUAGE_COMMUNICATION_V2_REVIEW_SCOPE.md) are submitted in Part 2; the source verdict is pending.')
    text=text.replace('[complete-file handoff](docs/audit/2026-10-08/full-game/EXPEDITION_COMPLETE_FILE_HANDOFF_PREPARATION.json) preserves161 files and verifies386 source-book paragraphs; unsent, pending an interface refresh.','[refreshed complete-file handoff](docs/audit/2026-10-08/full-game/EXPEDITION_COMPLETE_FILE_HANDOFF_V2_PREPARATION.json) supplies194 files and retains386 verified source-book paragraphs; unsent, pending intervening language/content decisions.')
    text=text.replace('[complete-file handoff](docs/audit/2026-10-08/full-game/BESTIARY_COMPLETE_FILE_HANDOFF_PREPARATION.json) supplies337 files and exact historical/current pairs; unsent, with no creature or cosmology approval.','[refreshed complete-file handoff](docs/audit/2026-10-08/full-game/BESTIARY_COMPLETE_FILE_HANDOFF_V2_PREPARATION.json) supplies370 files with exact historical/current pairs and completed crafting evidence; unsent, with no creature or cosmology approval.')
    marker='Preparation grants no approval. |'
    assert text.count(marker)==1
    text=text.replace(marker,'Preparation grants no approval. [Low-rank137](docs/audit/2026-10-08/full-game/LOW_RANK_SPELL_FILE_HANDOFF_V2_PREPARATION.json) and [higher-rank435](docs/audit/2026-10-08/full-game/HIGHER_RANK_SPELL_FILE_HANDOFF_V2_PREPARATION.json) complete-file refreshes retain the original sources; incorporate completed language decisions before dispatch. |')
    start.write_text(text,encoding='utf-8')
    prefix='''## Current checkpoint — 11 October, after NWX coverage registration

The first exact six-manuscript teaching review is fulfilled. The 75-area ledger now records its actual reviewed scopes in DD-01/58/60/61/62/66, with their broader acceptance gates and human evidence unchanged. DD-46 records the live, once-submitted LA-01–16 source conference; capture its completed verdict before language authoring. No domain was newly closed by this metadata registration.

Four queued complete-file packets have refreshed v2 evidence: higher-rank435 spells (353 files), pending327 feats (268), bestiary (370) and expedition26 (194). Their original archives and all changed historical dependencies remain preserved. See [refresh receipt](QUEUED_HANDOFFS_AFTER_NWX_REFRESH.json). They remain UNSENT and require incorporation of the active language decisions and any intervening content decisions before their conferences. The existing low-rank137 v2 remains available.

'''
    handoff.write_text(prefix+handoff.read_text(encoding='utf-8-sig'),encoding='utf-8')
    # The coverage renderer checks all evidence paths; also check edited root links.
    import re
    links=re.findall(r'\]\(([^)]+)\)',text)
    local=[s.split('#')[0] for s in links if not s.startswith(('https:','http:','#'))]
    assert all((G/p).exists() for p in local)
    dump(receipt,{'status':'PASS scoped review/evidence registration','completedAtUtc':datetime.now(timezone.utc).isoformat(),
                  'preservedAt':rel(backup),'previousHashes':previous,'currentHashes':{rel(p):sha(p) for p in paths},
                  'teachingAspectsUpdated':selected,'languageAspectUpdated':'DD-46','unchangedAspects':unchanged,
                  'all75AcceptanceGatesUnchanged':True,'allClosuresUnchanged':True,'humanEvidenceUnchanged':True,
                  'fulfillmentReceiptSha256':status['receiptSha256'],'startPageLocalLinksChecked':len(local),
                  'newApprovals':0,'sourceInformationDeleted':0,'wholeGameFlowComplete':False})
    print('PASS: six teaching scopes, one submitted source conference, four packet links; 75 acceptance gates and closures preserved')

if __name__=='__main__':main()
