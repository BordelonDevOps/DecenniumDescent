"""Preserve the Heartcell notebook decisions and apply the bounded joint review."""
from copy import deepcopy
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import ast, json, re, subprocess, sys
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p):
    return json.loads(p.read_bytes())

def main():
    now = datetime.now(timezone.utc).isoformat()
    review_id = 'HEARTCELL-OWNER-UPDATE-02'
    capture = A/'COSMOLOGY_HEARTCELL_HUNT_2026_10_15_TURN_CAPTURE.json'
    native = A/'COSMOLOGY_HEARTCELL_HUNT_2026_10_15_THREAD_CAPTURE.json'
    terminal = A/'HEARTCELL_OWNER_UPDATE_02_TERMINAL_CAPTURE.json'
    verdict = A/'HEARTCELL_OWNER_UPDATE_02_VERDICT.txt'
    candidate = R/'data/director/cosmology/heartcell_owner_update_02.json'
    companion = R/'docs/director-only/cosmology/HEARTCELL_OWNER_UPDATE_02.md'
    equations = R/'data/director/cosmology/equation_of_oblivion_notebook_drafts_01.json'
    equations_md = R/'docs/director-only/cosmology/EQUATION_OF_OBLIVION_NOTEBOOK_DRAFTS_01.md'
    receipt = A/'HEARTCELL_OWNER_UPDATE_02_RECEIVED_DECISION.json'
    check = A/'HEARTCELL_OWNER_UPDATE_02_APPLICATION_CHECK.json'
    delta = A/'HEARTCELL_OWNER_UPDATE_02_NAVIGATION_DELTA.json'
    checkpoint = A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_HEARTCELL_OWNER_UPDATE_02.json'
    preserved = A/'before-heartcell-owner-update-02'
    current = R/'docs/director-only/cosmology/CURRENT_COSMOLOGY_READ_FIRST.md'
    core = R/'docs/canon/CANON_CORE.md'
    start = G/'START_HERE.md'
    ledger_path = R/'data/playtest/game_development_coverage.json'
    nav = R/'tools/build_review_map.py'
    assert all(not p.exists() for p in [candidate,companion,equations,equations_md,receipt,check,delta,checkpoint,preserved])
    final = read(terminal)
    assert final['responseComplete'] and final['reviewId']==review_id
    final_text = verdict.read_text(encoding='utf-8')
    for phrase in ['CONFIRM WITH ONE PRECISION','CONFIRM WITH TERMINOLOGY BOUNDARY','explanatory inference, not owner-confirmed fact','No seven-stage taint model was approved']:
        assert phrase in final_text, phrase

    ui = read(capture)
    turns = {t['turnKey']:t for t in ui['turns']}
    thread = json.loads(read(native)['content'][0]['text'])
    human = {}
    for turn in thread['turns']:
        for item in turn['items']:
            if item['type']=='userMessage':
                human[turn['id']] = ''.join(b['text'] for b in item['content'] if b['type']=='text')
    def owner(key):
        if key in human:
            return {'messageId':key,'quote':human[key],'capture':native.relative_to(G).as_posix(),'kind':'human-user-message; app-reader and browser conversation'}
        text=turns[key]['text'].split('You said:',1)[1].split('ChatGPT said:',1)[0]
        text=re.sub(r'\nWorked for [^\n]+\n?$', '',text).strip()
        return {'messageId':key,'quote':text,'capture':capture.relative_to(G).as_posix(),'kind':'human-user-message; rendered browser turn'}
    ids = [
        '106ea483-0615-4b95-88c9-209a65dce471','4b6b5251-da64-4522-9c18-3abdeaa2ac71',
        '74e1ecd7-0b67-4041-a0ee-ed70fadb1183','d645d271-e46a-471b-8178-1eb7cdc7be9f',
        'f049b1f6-7e93-4c72-a50b-a747f734f004','7d97de4d-318f-4495-b5e5-eb2280445df6',
        'befa539e-47e2-4d1a-89ee-c0cdb1e91a95','106fba3d-0833-483a-b742-1a5d57959d11',
        '4ee1e558-03db-4979-9665-e67c9c657a3c','104a71eb-1b86-4db6-928e-6c2f71952912',
        '7211f4cc-8bee-4c92-a714-11da09fa926c','fa0d32fa-f1a1-4c27-856d-02e30f98fa69',
        '8406394c-8040-4b2b-b1a3-0405d9ff4f37'
    ]
    owners=[owner(k) for k in ids]
    assert owners[0]['quote']=='for the cosmology, please always use the original'
    assert owners[3]['quote']=='A cycle should be a musical equilavent like an AEON? it should be an age.'
    assert owners[-1]['quote']=='commit it to codex'
    assert owners[-2]['quote']=='No. There are a very VERY limited number of ways to avoid it. Divine/Abyssal intervention is possible but extremely rare.'

    # Original source excerpts remain intact; the later owner clarification is a separate layer.
    source_specs=[
        ('The Cosmology of Decennium Descent.docx',[27,33,34,35,39]),
        ('The Decennium Descent and the Matrix of Oblivion.docx',[27])
    ]
    original_evidence=[]
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for name,indices in source_specs:
        p=G/name
        with ZipFile(p) as z: root=ET.fromstring(z.read('word/document.xml'))
        paras=[''.join(t.text or '' for t in node.findall('.//w:t',ns)) for node in root.findall('.//w:p',ns)]
        original_evidence.append({'source':info(p),'part':'word/document.xml','paragraphs':[{'paragraphIndexZeroBased':i,'text':paras[i]} for i in indices]})
    assert 'Calan’thir named them the Choir' in original_evidence[0]['paragraphs'][3]['text']
    assert 'Asmodeus himself stepped across threshold' in original_evidence[0]['paragraphs'][4]['text']
    assert original_evidence[1]['paragraphs'][0]['text'].startswith('The Sundering lasted twenty cycles.')

    protected_paths=[
        *(G/p for p,_ in source_specs),G/'The_World_of_Aethel_Lore.docx',
        G/'webpage.html',G/'src/components/CosmologyViewer.tsx',G/'src/data/cosmology-lore.json',
        R/'data/director/cosmology/owner_reconciliation_reviewed_01.json',
        R/'docs/director-only/cosmology/OWNER_RECONCILIATION_REVIEWED_01.md',
        A/'COSMOLOGY_OWNER_RECONCILIATION_01_ADOPTION_CHECK.json',
        A/'COSMOLOGY_Q6_LATER_LOCK_01_TERMINAL_THREAD_CAPTURE.json',
        A/'COSMOLOGY_PLANES_SOURCE_INVENTORY_DRAFT_01_CHECK.json',
        capture,native,terminal,verdict
    ]
    protected=[info(p) for p in protected_paths]
    formula_ids=['7d97de4d-318f-4495-b5e5-eb2280445df6','c262246e-9105-48cd-842b-7866db28ba13','befa539e-47e2-4d1a-89ee-c0cdb1e91a95','106fba3d-0833-483a-b742-1a5d57959d11']
    formula_drafts=[]
    for key in formula_ids:
        t=turns[key]
        tex=[unescape(x) for x in re.findall(r'<annotation[^>]*>(.*?)</annotation>',t['html'],re.S)]
        assert tex
        formula_drafts.append({'turnKey':key,'ownerRequest':owner(key)['quote'],
            'assistantTextAsRendered':t['text'].split('ChatGPT said:',1)[1].strip(),
            'texAnnotationsInDomOrder':tex,'status':'new authored notebook draft; not recovered source formula or adopted numerical runtime'})
    assert [len(t['texAnnotationsInDomOrder']) for t in formula_drafts]==[13,14,12,30]
    eqdata={'recordedAtUtc':now,'sourceCapture':info(capture),'drafts':formula_drafts,
        'semanticStatus':'Owner commissioned mathematical and occult inscription designs; preserve variants without silently choosing a numerical canon.',
        'originalEquationRecovered':False,'numericalModelAdopted':False,'publicExportEnabled':False,
        'openDesignChecks':['Choose final inscription and stable symbol key.','Reconcile variant operators and derivative conditions before any operational interpretation.','Define domain/normalization/units only if a numerical implementation is wanted; decorative notation supplies no thresholds.']}
    equations.write_bytes(encoded(eqdata))
    chosen=formula_drafts[-1]['texAnnotationsInDomOrder'][-1]
    equation_text='''# Equation of Oblivion — notebook drafts

Director/design material. These designs were commissioned by the owner in **Resolve Heartcell Origins** on 15 October 2026. They are new authored expressions of the lore. They do not recover the incomplete formula in the original Matrix manuscript.

The owner wants a beautiful engraved, symbol-heavy forbidden theorem: hard to find, harder to decipher, and almost impossible to complete. Its symbols require Research across multiple libraries within the Descent. Functional understanding carries increasing taint.

The notebook's final proposed occult engraving is preserved below as a **draft**, with its original notation:

$$
'''+chosen+'''
$$

The notebook also preserves an inverse-expression draft, a normalized distinction-collapse draft, a combined seven-term expression, and the engraved/occult/fragment variants. Their full responses and all 69 exact TeX annotations are in [the structured draft archive](../../../data/director/cosmology/equation_of_oblivion_notebook_drafts_01.json).

The final engraving's proposed key is Identity, Memory, Loyalty, Choice, Motion/Becoming, Resonance and Dissonance, with a primordial-distinction denominator. This is the notebook's design key, not a recovered original passage. Earlier variants use different letters and normalizations. Final selection, operator meanings and puzzle placement remain to reconcile. A five-fragment structure and seven taint stages were suggestions, not adopted rules.

Use [the current owner decisions](HEARTCELL_OWNER_UPDATE_02.md) for source authority, taint, Hunt and exceptional death rules. The complete key and explanatory text remain Director/design material; later player handouts must reveal only their intended fragment.
'''
    equations_md.write_text(equation_text,encoding='utf-8',newline='\n')

    decisions=[
        {'id':'HC02-01','status':'owner preference settled','ownerMessageIds':ids[:3],
         'decision':'Use original cosmology manuscripts first; apply explicit owner corrections; use review artifacts as indexes/conflict records; report actual remaining gaps. Earlier source-preference question is resolved. This does not name the Heartcell builder.'},
        {'id':'HC02-02','status':'qualitative owner definition adopted','ownerMessageIds':[ids[3]],
         'decision':'A primordial cosmological Cycle is an age, with a musical/aeonic analogy. Twenty cycles therefore denotes twenty such ages. No fixed years, calendar conversion or operational-machine cycle is supplied.'},
        {'id':'HC02-03','status':'owner intent recorded; source-order reconciliation open','ownerMessageIds':[ids[4]],
         'decision':'First Choir arose in response to Asmodeus attacking Calanthir; later virtues arise from its resonance. Preserve original P27/P33-39 order and Matrix P27. Exact event/awakening timing and principle-to-name mapping remain unresolved. GPT withdrew its no-agency-before-assault and one-to-one mapping inferences.'},
        {'id':'HC02-04','status':'owner authoring brief adopted; formula variants preserved as drafts','ownerMessageIds':ids[5:8],
         'decision':'An expressive engraved/occult Equation should invite theories and be difficult to find, decipher and complete. Preserve requested new formulas separately from original-source evidence; no numerical model or fixed fragment count adopted.'},
        {'id':'HC02-05','status':'qualitative owner rules adopted','ownerMessageIds':ids[8:10],
         'decision':'Research across multiple Descent libraries deciphers the Equation. Functional knowledge progressively taints/corrupts; greater understanding increases danger. Creatures at Descent level 5 onward can also be tainted by voices/proximity to the Old Ones. Causes are distinct; no arithmetic combination or threshold is supplied.'},
        {'id':'HC02-06','status':'qualitative owner rule with correction adopted','ownerMessageIds':ids[10:12],
         'decision':'A Pact Hunt initiates hardcore status and death is normally final. There are very limited exceptional escapes, including extremely rare Divine/Abyssal intervention. The earlier absolute prohibition of divine intervention is superseded; ordinary recovery does not supply a routine exception.'}
    ]
    unresolved=[
        'Underlying Heartcell authorship and the exact relation of machinery to the Pact manifestation remain source questions, not a pending source-preference choice.',
        'Choir P35 versus P39 chronology and the exact sense of attack/awakening remain to reconcile; no fabricated intermediate event.',
        'No exact mapping of the seven Harmony principle names to named Choir members is supplied.',
        'Original complete Equation remains unrecovered; new inscription variants need final selection, symbol/operator consistency and fragment presentation.',
        'Research procedure, functional-knowledge stages, taint scale/combination, exposure frequency, reductions/cures and failure consequences remain to develop.',
        'Hunt initiation/detection, notice, persistence or termination, and the identity and conduct of hunters remain to develop.',
        'Death-state timing, individual resurrection/soul/clone/time effects and exceptional Divine/Abyssal intervention require their exact interface review.',
        'Existing unresolved identity, Maladomini, Shardspire and World I-VI issues remain; this update does not close all cosmology.'
    ]
    data={'reviewId':review_id,'recordedAtUtc':now,'status':'bounded owner update jointly checked and applied',
        'conversationUrl':ui['conversationUrl'],'exactOwnerMessages':owners,'decisions':decisions,
        'originalSourceEvidence':original_evidence,'gptVerdict':info(verdict),'terminalCapture':info(terminal),
        'equationDrafts':info(equations),'remainingDependencies':unresolved,
        'sourcePreferenceAmbiguityClosed':True,'heartcellBuilderNamed':False,'exactChoirMappingApproved':False,
        'originalFormulaRecovered':False,'sevenStageTaintApproved':False,'numericalMechanicsImplemented':False,
        'runtimeApproved':False,'publicExportEnabled':False,'fullCosmologyApproved':False,'sourceInformationDeleted':0}
    candidate.write_bytes(encoded(data))
    companion.write_text('''# Heartcell — owner decisions of 15 October 2026

**Current Director/design addendum.** The owner asked Codex to read **Resolve Heartcell Origins**, including the request to “commit it to codex.” The decisions below were checked with that actual GPT notebook under **HEARTCELL-OWNER-UPDATE-02**. They are saved locally; this is not a new GitHub push.

## Source authority

“For the cosmology, please always use the original” settles the earlier source-preference question. Read the original Cosmology, Matrix and surviving World of Aethel manuscripts first, then apply the owner's explicit corrections. Review records help locate evidence and conflicts; they do not replace the manuscripts. Report remaining gaps after checking the relevant lore.

This preference does not identify a builder for the underlying Heartcell. The earlier eleven owner corrections remain in force within their recorded scope. The later Director builder account must not become controlling merely because its file is newer.

## Primordial cycles and the First Choir

A primordial **Cycle is an age**, understood through a musical/aeonic analogy. The Matrix's twenty cycles means twenty such cosmological ages. No fixed duration, mortal-year conversion or connection to the ten-year dungeon Opening has been supplied.

The owner says the First Choir arose in response to Asmodeus attacking Calan'thir and that later virtues spawn from the Choir's resonance. Preserve that intent.

**Chronology still needs reconciliation.** Original Cosmology P27 has unfinished nascent chords; P33-35 narrates their maturation, manifestation and naming as the Choir; P39 then describes the direct assault with the Choir already defending the Spiral. Matrix P27 places awakening during the Sundering. GPT confirmed this ordering conflict and withdrew its inference that the seven had no individuality or agency until the assault. Do not silently reorder the manuscript or invent another event.

The exact mapping of the seven named Harmony principles to named Choir members is also still open. Additional resonant virtues do not provide that mapping.

## Equation, Research and taint

The owner commissioned an expressive engraved and occult Equation that makes players theorize: hard to find, harder to decipher, almost impossible to complete. [All notebook equation variants](EQUATION_OF_OBLIVION_NOTEBOOK_DRAFTS_01.md) are preserved as new authored drafts with their exact notation. They are not a recovered original formula or a numerical simulation.

The symbols must be deciphered through **Research across multiple libraries within the Descent**. Gaining functional knowledge taints the researcher, and increasing understanding brings increasing corruption and danger, potentially leading to a fall, a Pact hunt or death.

Creatures from **Descent level 5 onward** can also be tainted simply by hearing the Old Ones' voices through proximity. Environmental exposure and functional understanding are distinct causes. This statement does not require an ignorant tainted creature to possess forbidden knowledge, and it supplies no automatic Hunt threshold or arithmetic taint formula.

## Pact Hunt and death

**Once a Hunt is initiated, the character becomes hardcore. Death is normally final.** Ordinary recovery from death does not supply a routine escape from this consequence.

The owner's subsequent correction explicitly retains a very limited number of exceptions: **Divine or Abyssal intervention is possible but extremely rare**. GPT's earlier absolute prohibition of divine intervention is superseded. No guaranteed intervention, purchasable rescue or routine spell exception has been established.

Research stages, numeric taint thresholds, exposure rates, taint combination, cures, Hunt detection/notification, Hunt termination and the exact spell/death/intervention procedures remain to develop. Seven stages, three formal knowledge states, five puzzle fragments and fixed equations for taint were notebook proposals. They have not been adopted as rules.

## Evidence and remaining work

[The structured decision record](../../../data/director/cosmology/heartcell_owner_update_02.json) preserves thirteen exact owner messages, six dispositions, six original-source paragraphs, and the completed GPT check. Earlier sources and review receipts remain preserved. The source-preference ambiguity and qualitative age definition are resolved; the underlying builder, Choir chronology/mapping, original missing formula, identity questions and missing World I-VI remain open in their respective scopes.

This update is a Director/design rule direction. Exact operational mechanics, all affected spell interfaces, public handouts and human playtesting still require completion.
''',encoding='utf-8',newline='\n')
    receipt.write_bytes(encoded({'reviewId':review_id,'receivedAtUtc':now,'conversationUrl':ui['conversationUrl'],
        'terminal':info(terminal),'verdict':info(verdict),'prompt':info(A/'HEARTCELL_OWNER_UPDATE_02_PROMPT.txt'),
        'submittedOnce':True,'format':'plain-text terminal verdict; no archive requested',
        'boundariesConfirmed':4,'qualification':'Choir chronology/mapping and mechanical interfaces remain open',
        'candidate':info(candidate),'companion':info(companion)}))

    # Preserve every edited current file before changing its reading pointer or status.
    to_preserve=[current,core,start,ledger_path,nav,G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json']
    preservation=[]
    for p in to_preserve:
        dest=preserved/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(p.read_bytes());assert dest.read_bytes()==p.read_bytes()
        preservation.append({**info(p),'preservedCopy':dest.relative_to(G).as_posix()})
    (preserved/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preservation))
    current.write_text('''# Current cosmology reading order

Start with [the latest Heartcell owner update](HEARTCELL_OWNER_UPDATE_02.md): original-source priority is settled; primordial cycles are ages; the Choir clarification and chronology conflict are recorded; the commissioned Equation drafts, Research taint, proximity taint and exceptional Hunt/death rule are preserved.

Then read [the earlier eleven owner corrections](OWNER_RECONCILIATION_REVIEWED_01.md). Their historical source-preference ambiguity and undefined cycle meaning are qualified by the latest update. The underlying Heartcell builder remains unresolved. An exact Harmony-to-Choir mapping and a fully reconciled awakening chronology remain open.

Read [creation and origins](CREATION_ORIGINS_REVIEWED_01.md) and [gods and pantheons](GODS_PANTHEONS_REVIEWED_01.md) as earlier records subject to both owner updates. Mephistopheles is Cania only; the devouring-to-one correction and no-essence-tether correction remain current. The survivor's identity and Maladomini's replacement ruler are not supplied.

Original Cosmology, Matrix and surviving World manuscripts govern cosmological source reading, with explicit owner corrections applied. Original passages, mortal belief, owner decisions and new notebook designs retain separate provenance. The new Equation drafts do not recover the missing original formula or World I-VI.

This is Director/design material. Q6 has a captured terminal verdict awaiting its evidence-archive verification. Planes, souls/death/resurrection, history, divine/class powers and campaign revelations still need their remaining reviews. Numerical mechanics, runtime, human playtesting and publication are not certified by these records.
''',encoding='utf-8',newline='\n')
    old_core=core.read_text(encoding='utf-8')
    old_para=next(p for p in old_core.split('\n\n') if p.startswith('**Underlying Heartcell authorship remains conditional.**'))
    new_para='**Cosmology source priority is settled; underlying Heartcell authorship remains unresolved.** The owner says to always use the original cosmology and to answer from existing lore first, with explicit owner corrections applied. The later Director builder account remains preserved secondary evidence. This preference does not name a builder or establish a separate machinery/prison construction event. See the [latest owner update](../director-only/cosmology/HEARTCELL_OWNER_UPDATE_02.md).'
    new_core=old_core.replace(old_para,new_para,1)
    assert new_core.replace(new_para,old_para,1)==old_core
    core.write_text(new_core,encoding='utf-8',newline='\n')
    prior_checkpoint=A/'ACTIVE_AUTHORING_CHECKPOINT_AFTER_OWNER_ADOPTION_AND_WEBSITE_SOURCE.json'
    state=read(prior_checkpoint)
    scope=('Heartcell owner update jointly confirmed in the actual Resolve Heartcell Origins notebook: thirteen exact owner messages, six dispositions, original-source priority clarified, primordial Cycle is an age, Choir response/derivative virtues recorded with P35/P39 chronology and exact mapping still open. '
        'Four newly commissioned Equation draft responses and 69 exact TeX annotations preserved; no recovered original formula or numerical model. Research/functional-knowledge taint, level-5 voice/proximity taint, Hunt hardcore death and extremely rare Divine/Abyssal exceptions recorded; operational thresholds and spell/death interfaces remain open. '
        'Q6 terminal verdict captured; evidence archive still pending retrieval/verification. A 76-record planes source inventory is provisional. Saved cosmology website remains included. Ordinary spells419reviewed/429pending, latest verified GitHub backup18c6e3a, subsequent work local.')
    before_ledger=read(ledger_path);ledger=deepcopy(before_ledger)
    for row in ledger['aspects']:
        if row['id'] in {'DD-50','DD-61','DD-65','DD-69'}:
            row.setdefault('completedScopes',[]).append(scope)
            row.setdefault('currentEvidenceAddenda',[]).append({'id':'heartcell-owner-update-02','recordedAtUtc':now,'receipt':receipt.relative_to(G).as_posix(),'fullDomainClosed':False})
            row.setdefault('validationEvidence',[]).extend(p.relative_to(G).as_posix() for p in [receipt,candidate,companion,equations])
    for a,b in zip(before_ledger['aspects'],ledger['aspects']):
        assert all(a.get(k)==b.get(k) for k in ['closure','humanEvidence','ownerEvidence'])
        if a['id'] not in {'DD-50','DD-61','DD-65','DD-69'}:assert a==b
    ledger_path.write_bytes(encoded(ledger))
    old_start=start.read_text(encoding='utf-8')
    old_line=next(x for x in old_start.splitlines() if x.startswith('**Current joint review:**'))
    new_line='**Current joint review:** The [latest Heartcell owner decisions](DescentReviewChanges/ReviewBible/docs/director-only/cosmology/HEARTCELL_OWNER_UPDATE_02.md) are saved and jointly checked with GPT. Original-source priority is clarified; primordial cycles are ages; Research/proximity taint and Hunt death with rare Divine/Abyssal exceptions are recorded. Choir chronology/mapping and detailed mechanics remain open. The [saved cosmology website](webpage.html) is included in the audit. Q6 has a terminal verdict awaiting evidence-archive verification. Ordinary spells remain **419 reviewed / 429 pending**. Use the [review map](REVIEW_MAP.html) and [current checkpoint](docs/audit/2026-10-08/full-game/ACTIVE_AUTHORING_CHECKPOINT_AFTER_HEARTCELL_OWNER_UPDATE_02.json). Latest verified GitHub backup is 18c6e3a; subsequent work is local. **You are monitoring usage; the earlier 50% stop is withdrawn.**'
    new_start=old_start.replace(old_line,new_line,1);assert new_start.replace(new_line,old_line,1)==old_start
    start.write_text(new_start,encoding='utf-8',newline='\n')
    nav_text=nav.read_text(encoding='utf-8')
    chain=' + read(A / "OWNER_ADOPTION_WEBSITE_SOURCE_01_NAVIGATION_DELTA.json")["changes"]\n'
    assert nav_text.count(chain)==1
    nav_text=nav_text.replace(chain,chain.rstrip('\n')+' + read(A / "HEARTCELL_OWNER_UPDATE_02_NAVIGATION_DELTA.json")["changes"]\n',1)
    nodes=[v for node in ast.walk(ast.parse(nav_text)) if isinstance(node,ast.Dict) for k,v in zip(node.keys,node.values) if isinstance(k,ast.Constant) and k.value=='notebookReview']
    assert len(nodes)==1
    literal=ast.get_source_segment(nav_text,nodes[0]);nav_text=nav_text.replace(literal,repr(scope),1)
    marker='    pending = [\n';assert nav_text.count(marker)==1
    links=[('Heartcell owner update — original sources, ages, taint and Hunt',receipt.name),
           ('Q6 — captured terminal verdict; archive verification pending','COSMOLOGY_Q6_LATER_LOCK_01_TERMINAL_THREAD_CAPTURE.json'),
           ('Planes — 76 source claims, provisional inventory','COSMOLOGY_PLANES_SOURCE_INVENTORY_DRAFT_01_CHECK.json')]
    nav_text=nav_text.replace(marker,marker+''.join('        '+repr(x)+',\n' for x in links),1)
    compile(nav_text,str(nav),'exec');nav.write_text(nav_text,encoding='utf-8',newline='\n')
    changes=[{'before':next(x for x in preservation if x['path']==p.relative_to(G).as_posix()),'after':info(p)} for p in [current,core,start,ledger_path,nav]]
    delta.write_bytes(encoded({'recordedAtUtc':now,'changes':changes,'sourceInformationDeleted':0,'fullDomainClosureChanged':False,'ownerUpdate':info(candidate)}))
    run=subprocess.run([sys.executable,'-X','utf8',str(nav)],capture_output=True,text=True,encoding='utf-8')
    if run.returncode:
        print(run.stdout[-2000:]);print(run.stderr[-5000:]);raise SystemExit(run.returncode)
    navigation=read(A/'REVIEW_MAP_BUILD.json');assert not navigation['missingLinks']
    assert all(info(G/r['path'])==r for r in protected)
    check.write_bytes(encoded({'reviewId':review_id,'recordedAtUtc':now,'exactOwnerMessages':13,'dispositions':6,
        'docxParagraphs':6,'equationDraftResponses':4,'exactTexAnnotations':69,'originalsAndCapturesUnchanged':protected,
        'candidate':info(candidate),'companion':info(companion),'equations':info(equations),'equationsReadingCopy':info(equations_md),
        'receipt':info(receipt),'preservationManifest':info(preserved/'PRESERVATION_MANIFEST.json'),
        'navigationLinks':navigation['existingDistinctLinks'],'missingLinks':[],'sourcePreferenceAmbiguityClosed':True,
        'heartcellBuilderNamed':False,'fullChoirTimingClosed':False,'exactChoirMappingApproved':False,
        'sevenStageTaintApproved':False,'numericalMechanicsImplemented':False,'spellFlagsChanged':False,
        'sourceInformationDeleted':0,'githubPushed':False}))
    state.update(recordedAtUtc=now,previousCheckpoint=info(prior_checkpoint),status=scope,goalTurnClassification='progress',
        previousGoalTurnClassification='progress',coverageLedger=info(ledger_path),coverageDelta=info(delta),
        navigation={'map':info(G/'REVIEW_MAP.html'),'receipt':info(A/'REVIEW_MAP_BUILD.json'),'links':navigation['existingDistinctLinks'],'missingLinks':[]},
        ownerStartPage=info(start))
    state['heartcellOwnerUpdate']={'status':'jointly checked and locally applied','candidate':info(candidate),'companion':info(companion),
        'check':info(check),'receipt':info(receipt),'equations':info(equations),'sourcePreferenceAmbiguityClosed':True}
    state['ownerCosmologyCorrections'].update(status='earlier eleven corrections retained, qualified by Heartcell owner update02',
        readingOrder=info(current),sourcePreferenceAmbiguityClosed=True,heartcellBuilderStillUnresolved=True)
    state['activeGptReview'].update(status='Q6 terminal verdict recovered; output archive retrieval/verification pending',
        terminalCapture=info(A/'COSMOLOGY_Q6_LATER_LOCK_01_TERMINAL_THREAD_CAPTURE.json'))
    state['planesSourceInventory']=info(A/'COSMOLOGY_PLANES_SOURCE_INVENTORY_DRAFT_01_CHECK.json')
    state['safeNextActions']=[
        'Do not repeat the original-source preference question: the later human messages in Resolve Heartcell Origins answer it. Builder remains unresolved; original lore must be read before new unresolved claims.',
        'Q6 terminal verdict is preserved; retrieve/verify its existing15130byteZIP hashf72ec4b82e5c73934352df25cde796a2001d947824952ec3c6788509737bf168. Native send_message caused a stale branch/systemError; use the existing correct Calibration Review Part2 browser tab and preserve versions.',
        'Apply the expected q6_later_lock_reviewed_01.json/Q6_LATER_LOCK_REVIEWED_01.md only after evidence verification. Registered path/public ceiling do not settle identity or full encounter mechanics.',
        'Before running the unexecuted prepare_cosmology_planes_01.py, include this current Heartcell owner update, its original-source preference and remaining conflicts, plus the76record source inventory and saved website. Then complete the Q6 prerequisites and submit actual sources once.',
        'Discuss remaining Choir chronology and named Harmony correspondence from original passages. Do not promote withdrawn GPT no-agency or one-to-one assumptions.',
        'Develop Research/Equation puzzle and distinct taint causes, Hunt procedures and rare death exceptions with actual spell/soul interfaces. Current owner direction is qualitative; seven stages and numeric combination remain unapproved.',
        'Continue planes, souls/death, history, divine/class powers and revelations; preserve ordinary spell/feat and whole-game requirements. No final completion or runtime/human-playtest approval.',
        'Latest verified GitHub backup18c6e3a; this work local. User monitors usage;50percentcutoff withdrawn.'
    ]
    state.setdefault('preservationManifests',[]).append(info(preserved/'PRESERVATION_MANIFEST.json'))
    checkpoint.write_bytes(encoded(state))
    print(json.dumps({'check':info(check),'companion':info(companion),'checkpoint':info(checkpoint),
        'exactOwnerMessages':13,'equationTexAnnotations':69,'missingNavigationLinks':0,'sourceInformationDeleted':0}))

if __name__=='__main__':
    main()

