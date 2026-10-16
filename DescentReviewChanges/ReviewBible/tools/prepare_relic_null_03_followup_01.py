"""Preserve the two Part4 returns and prepare a source-grounded semantic follow-up."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    check_path=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_02_SOURCE_FORMAT_RESOLUTION_01.json'
    review_path=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_02_FOLLOWUP_REVIEW_01.json'
    request_path=A/'COSMOLOGY_EPILOGUE_RELIC_NULL_03_REVISION_REQUEST_01.txt'
    assert all(not p.exists() for p in [check_path,review_path,request_path])
    now=datetime.now(timezone.utc).isoformat()
    packet=A/'cosmology-epilogue-relic-null-01'
    additional=A/'part4-relic-null-handoff-01'
    original={x['path']:x for x in read(packet/'SOURCE_BINDINGS.json')}
    extra=read(additional/'ADDITIONAL_SOURCE_BINDINGS.json')[0]
    expected={**original,extra['path']:extra}
    checks=[]
    for suffix,folder in [('01','cosmology-epilogue-relic-null-02-return'),('02','cosmology-epilogue-relic-null-02-return-02')]:
        root=A/folder
        got=read(root/'SOURCE_HASHES.json')['sources']
        indexed={x['path']:x for x in got}
        rows=[]
        rows.append({'check':'exact unique source set','passed':len(got)==len(indexed)==84 and set(indexed)==set(expected)})
        rows.append({'check':'original83 entries unchanged in full','passed':all(indexed[k]==v for k,v in original.items())})
        for name,binding in expected.items():
            source=(packet/'sources'/name) if name in original else additional/'additional_sources'/name
            raw=source.read_bytes()
            actual={'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
            returned={k:indexed[name][k] for k in ['path','bytes','sha256']}
            rows.append({'check':'source identity and exact bytes','path':name,'passed':actual==returned=={k:binding[k] for k in actual}})
        extras={k:v for k,v in indexed[extra['path']].items() if k not in extra}
        rows.append({'check':'only added explanatory bindingStatus metadata','passed':set(extras)=={'bindingStatus'},'extraMetadata':extras})
        assert all(x['passed'] for x in rows)
        initial=read(A/f'COSMOLOGY_EPILOGUE_RELIC_NULL_02_RETURN_SOURCE_CHECK_{suffix}.json')
        assert initial['checkCount']==239 and initial['failureCount']==1
        assert initial['failures'][0]['where']==extra['path']
        checks.append({'archive':info(A/f'DD_Cosmology_Epilogue_Relic_Null_02_Return_{suffix}.zip'),
          'originalReceipt':info(A/f'COSMOLOGY_EPILOGUE_RELIC_NULL_02_RETURN_SOURCE_CHECK_{suffix}.json'),
          'checks':rows,'failureCount':0,'normalizedCheckCount':len(rows),
          'resolution':'The original checker compares whole source dictionaries. The additional lifecycle record adds bindingStatus. Its path, 20087 bytes and SHA256 match the supplied source exactly. Original receipts and returned archives are unchanged. This is metadata-format resolution, not semantic approval.'})
    check_path.write_bytes(encoded({'recordedAtUtc':now,'returns':checks,'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0}))
    root=A/'cosmology-epilogue-relic-null-02-return-02'
    m=read(root/'RELIC_NULL_MODEL.json');cases=read(root/'CASEBOOK.json')['cases']
    def pointer(p):
        node=m
        for k in p.strip('/').split('/'): node=node[int(k)] if isinstance(node,list) else node[k]
        return {'file':info(root/'RELIC_NULL_MODEL.json'),'jsonPointer':p,'value':node}
    def case(cid): return {'file':info(root/'CASEBOOK.json'),'caseId':cid,'value':next(x for x in cases if x['id']==cid)}
    findings=[
      {'id':'RN2-01','title':'Restore a usable complete player chapter',
       'finding':'The latest PLAYER_CHAPTER replaces readable relic procedures with long raw JSON, omits the hourly WIS DC15 exposure rule and final passive Insight5, omits creation-time damage-root behavior, abbreviates all three purge requirements and omits individual plant recognition/harvest/freshness and dose outcomes. Shrug success/failure paragraphs are concatenated without explicit outcome labels. The Director/model still contain these rules. Both chapters must carry their full intended operational content and preserve player/Director information boundaries.',
       'required':'Rewrite human-readable chapters and compare each operative rule with the model. Player text must state complete player-facing costs, time, targets, outcomes, recovery and limits; use explicit Director cross-references for private scene information rather than exporting raw model internals.'},
      {'id':'RN2-02','title':'Finish actor envelopes and derive passive scores from actual modifiers',
       'finding':'Toy Perception+3 prints passive11, Wraith Perception+7 prints14, and other profiles disagree with 10+their printed WIS/Perception modifier. In the absence of a separately printed modifier the expected values are Toy13, Wraith17, Devil11, Demon11, Echo12, Glass-Mender13. Clockwork Lunge still lacks reach/target count; Echo Strike lacks explicit melee reach/type/target count; Sera Quarterstaff lacks reach/target count. Rehearse Doubt lacks a complete Action/clock envelope.',
       'required':'Use frozen COMBAT_ACTION line172 and actual actor modifiers. Complete every actor action/reaction and initial placement needed by the rooms, including the fear source and outside/inside initiative deadlines. Do not invent proficiency solely to preserve a mistaken passive.',
       'evidence':[pointer('/actorProfiles/ACT-TOY-SENTINEL'),pointer('/actorProfiles/ACT-SILENCE-WRAITH'),pointer('/actorProfiles/ACT-ECHO-DOPPELGANGER'),pointer('/actorProfiles/ACT-NULL-WITNESS')]},
      {'id':'RN2-03','title':'Make Ladder self-steadying and failure branches executable',
       'finding':'The frightened climber spends its Action to steady but that advantage expires at the start of its next turn; the separate climb also costs an Action. A character with only its normal Action cannot use the benefit. The cable catch covers clipped failure only; unclipped failure and over-capacity clip attempts are undefined. The corrected burdened example is accepted as a useful repair, but it does not resolve these branches.',
       'required':'Choose and label a scoped NEW self-steady timing that an ordinary character can use, with no extra Action assumption. State clip capacity preflight, unclip/withdrawal and unclipped failure against real geometry, hand requirements and movement costs. Work a frightened ordinary climber through the whole sequence.',
       'evidence':[pointer('/chambers/5'),case('RNX-08-A'),case('RNX-08-B')]},
      {'id':'RN2-04','title':'Supply coherent physical maps for the corrected procedures',
       'finding':'A 20x20 return pad cannot occupy a northeast quadrant of a 30x30 room (15x15), and its overhead description lacks an actual support elevation. Tessellation has row/lane labels but no complete coordinates for staging strips, flower beds, markers, safe inter-row/return travel and nets. Quiet Well calls a 10x10 southwest alcove outside its cylinder without specifying whether it extends outside the circular wall. The reachable Glass-Mender side room lacks dimensions/placement for its actor and repair cradle.',
       'required':'Give fixed coordinate bounds, height/support, doors, legal starting/return spaces and connected routes for these NEW scenes. Preserve the approved finite map pattern. Demonstrate a legal round trip and legal current Large-body return without overlaps or assumed off-map room.',
       'evidence':[pointer('/chambers/3'),pointer('/chambers/6'),pointer('/chambers/10'),pointer('/relics/2/reformation')]},
      {'id':'RN2-05','title':'Resolve Return Hold against existing absolute clocks',
       'finding':'Return Hold freezes all local clocks/effects and targeting, while established life, form, concentration and expiry rules retain absolute/virtual deadlines. An enlarged traveler that cannot fit can remain frozen past the enlargement expiry, preventing the very body reversion that would make return legal. The relationship to an outside caster ending concentration, death/Stable recovery, companion expiry and a corpse of an original traveler is unspecified.',
       'required':'Replace or fully reconcile this NEW return fallback with existing clocks and source lifecycles. Prefer preserving real deadlines rather than a parallel universal stasis engine. Explicitly distinguish any allowed +10-to+20-minute agency from the later waiting state. Work blocked return during form expiry, an externally ended concentration effect, one traveler returning earlier, and original-traveler death without copying identities.',
       'evidence':[pointer('/chambers/10/procedures'),case('RNX-09-A'),case('RNX-09-B')]},
      {'id':'RN2-06','title':'Correct worked time and class-feature arithmetic',
       'finding':'RNX-01-B starts a ten-minute Echo Lily harvest at9:55 but claims completion due at10:00; it is due19:55. RNX-14-A counts only60m30s despite the EPI06 procedure requiring consultation10m, meditation60m and symbolic act10m unless already completed stages are explicitly recorded. RNX-03-A now cites Healing Rite correctly but asserts 2d8+M without a Cleric level/S and turns a result at least4 into exactly HP4. RNX-03-B says end/start marker rather than the actual Undying Spellform end of next regular turn.',
       'required':'Use exact source cards and timelines: cleric.json /cards/12 is S d8+M, class S=1/2/3/4 at L1/5/11/17; mage.json /cards/42 expires at end of next regular turn. State level, M, actual dice, HP maximum/cap and costs. Split interrupted-harvest and genuine same-timestamp-boundary cases as necessary. Show all EPI06 stages and168h cooldown from response.',
       'evidence':[case('RNX-01-B'),case('RNX-14-A'),case('RNX-03-A'),case('RNX-03-B')]},
      {'id':'RN2-07','title':'Make Twin Wind examples follow their closure rule',
       'finding':'RNX-11-B supplies only one eligible voter A. A depositing its token immediately meets the all-eligible-resolved close rule, so it cannot then change/deposit another token before a supposed10-minute close. Twelve physical tokens also need a stated procedure when more than twelve independently eligible characters attend; eligibility cannot silently produce a thirteenth token. Leaving/unconscious voters and abstention/token custody need one stable rule.',
       'required':'Retain finite one-identity voting. Work deadline/revote with an explicitly unresolved eligible voter keeping the vote open, and a separate single-voter immediate-close case. Define eligibility snapshot/change/overflow and exact token custody without cloning.',
       'evidence':[pointer('/chambers/8/voting'),case('RNX-11-B')]},
      {'id':'RN2-08','title':'Complete Null recipient and lethal-branch ordering',
       'finding':'The replacement recipientLifecycle table has no explicit branch for an ordinary nonliving Construct such as Toy Sentinel, although RN-N11 still asserts generic Disabled. Silence Wraith is described as a Spirit significant NPC which disperses, without an explicit relation to that table. The livingCreature text explicitly skips Instant Death/Wounds on positive-to-zero, but already-Dying merely says no added failure; RN-N05 expects no Instant Death/Wounds at Stable0. A qualifying hit that leaves positive HP can still trigger a fatal fourth-Wound save under Core unless the scope is settled.',
       'required':'State one ordered Null damage algorithm for positive-to-positive, new zero, existing Dying0, Stable0, source-specific nonliving/created creatures, projections and objects. Decide explicitly where damage-caused Instant Death, Wound/Maiming and existing-fatal-Wound branches are bypassed; preserve independent non-damage expiry/cost events. Bind local actors to actual lifecycle branches, with no anatomy guessed solely from names.',
       'evidence':[pointer('/null/veil/damageNonlethal'),case('RN-N05'),case('RN-N07'),case('RN-N11')]},
      {'id':'RN2-09','title':'Reconcile retained cases with the revised model',
       'finding':'RNX-12-A moves Demon from(20,0)10ft toward PC(0,0), leaving it15ft from Devil(25,0), yet claims Devil is5ft away without moving. RN-C03 retains north-exit/no-combat wording despite the revised east-exit/heartbeat-risk procedure. RN-C06 counts five climb Actions but omits the paid cable attachment and hanging recovery before retry. RN-R08-04 places a rest before transfer yet assumes charge remains0 without saying why that rest fails the pendant refresh conditions.',
       'required':'Preserve all75 case IDs, correct their contents, and audit previous examples against the final model rather than only checking ID presence. Show actual movement, Action, condition, stock and clock ledgers. Treat authored examples as examples, not executed runtime tests.',
       'evidence':[case('RNX-12-A'),case('RN-C03'),case('RN-C06'),case('RN-R08-04')]}
    ]
    report={'recordedAtUtc':now,'reviewedArchive':info(A/'DD_Cosmology_Epilogue_Relic_Null_02_Return_02.zip'),
      'earlierReturnPreserved':info(A/'DD_Cosmology_Epilogue_Relic_Null_02_Return_01.zip'),'sourceFormatResolution':info(check_path),
      'status':'Targeted independent semantic follow-up; remaining defects block adoption. Await actual GPT disposition.',
      'acceptedSelfAuditRepairs':['Prone standing movement before Tessellation recovery','Burdened disadvantage/Help cancellation with explicit capacity','Finite tray/flask carry accounting','Actual Healing Rite chosen, with arithmetic still to correct','CH10 Favor confined to CH10'],
      'findings':findings,'findingCount':len(findings),'newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False,'sourceInformationDeleted':0}
    review_path.write_bytes(encoded(report))
    intro='''Codex has recovered and preserved BOTH exact revision02 returns. I am reviewing your latest post-build repair: 102,637 bytes, SHA256 de3a15bee044b7e631cf46a572a104589f928913c5b618c246369a50d7925905. Thank you for the concrete self-audit repairs; the corrected Prone recovery, Burdened/Help cancellation, explicit carriage and CH10-only Favor are useful.

Source integrity is confirmed: all original83 entries are unchanged, and all84 source path/size/hash triples match the supplied bytes. My original strict dictionary checker flagged only the extra bindingStatus label on source84; that is explained metadata, not a file-access or source-loss failure. Both original receipts and ZIPs remain preserved. No EPI08-14 rules are adopted yet.

Please address the following remaining source-grounded semantic issues against the latest return and the SAME handoff/source set. These are Codex findings/proposals for your review, not owner rulings. Preserve all original/owner constraints and unresolved cosmological identities/epoch.
'''
    sections=[]
    for f in findings:sections.append(f"{f['id']} — {f['title']}\n{f['finding']}\nRequired correction/proof: {f['required']}")
    end='''
Return a complete DD_Cosmology_Epilogue_Relic_Null_03_Return.zip with exactly REGISTER.json, RELIC_NULL_MODEL.json, PLAYER_CHAPTER.md, DIRECTOR_CHAPTER.md, CASEBOOK.json, SOURCE_HASHES.json, VERDICT.md, EVIDENCE_MANIFEST.json. Include explicit RN2-01–09 agree/disagree dispositions and the changed-field map. Keep all75 existing case IDs (repair their contents), adding only focused cases where an essential branch lacks proof. Keep the84 frozen source bindings; do not introduce unseen source authority. Preserve original83 entries exactly. Use actual source-card pointers/line references. Both chapters must be full readable table-usable prose, consistent with the model and their intended audiences. Label new scoped mechanics honestly; no parallel unreviewed general engine or hidden owner decision. Rebuild the output manifest and report archive size/SHA256. This is still candidate authorship, not runtime/human balance/whole-game or publication approval. Please carry out the correction now.'''
    request_path.write_text(intro+'\n\n'+'\n\n'.join(sections)+'\n'+end+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'sourceResolution':info(check_path),'semanticReview':info(review_path),'request':info(request_path),'findings':len(findings),'submitted':False,'newRulesAdopted':False}))

if __name__=='__main__':main()
