import copy, hashlib, json, zipfile
from pathlib import Path

BASE = Path(r'C:\Github\DecenniumDescent')
AUDIT = BASE / 'docs/audit/2026-10-08/full-game/director-spell-review-129'
ZIP_PATH = AUDIT / 'DD_Information8_Director_Return03_131.zip'
PRIOR_ZIP = AUDIT / 'DD_Information8_Director_Return02_131.zip'
PRIOR_DIR = AUDIT / 'information8_return02_received'
INDEX_PATH = BASE / 'DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json'
EXPECTED_ZIP_SHA = '007ef53858a6f5bc69d7811b58d18d19f8434821362977a4a310a831a5c8fad3'
EXPECTED_PRIOR_SHA = 'f8a5f7ee9125a45c12f3bf5caa1907294207b986877eb354dd69895930d32c7c'
EXPECTED_INDEX_SHA = '44fec30864c5836b9d07ef3ee26b2aa63dfe89cda9bdaf824ff040e434ec1f72'
EXPECTED_PUBLIC_OLD = 'Indeterminate. The described120ft detour is a possible route; the shortest surviving route is not established by the available surrounding topology.'
EXPECTED_PRIVATE = 'The described120ft detour may be traversable, but its shorteststatus is unproved without complete actual surrounding topology.'
CHECKS = []
def check(name, ok, detail=None):
    CHECKS.append({'check': name, 'passed': bool(ok), 'detail': detail})
    if not ok:
        raise AssertionError(f'{name}: {detail}')
def sha(b): return hashlib.sha256(b).hexdigest()
def state_sha(v): return sha(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))
def walk_diff(a, b, path='$', out=None):
    if out is None: out=[]
    if type(a) is not type(b): out.append((path, a, b)); return out
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b: out.append((path+'.'+str(k), a.get(k,'<missing>'), b.get(k,'<missing>')))
            else: walk_diff(a[k], b[k], path+'.'+str(k), out)
    elif isinstance(a, list):
        if len(a) != len(b): out.append((path+'.length', len(a), len(b)))
        for i, (x,y) in enumerate(zip(a,b)): walk_diff(x,y,f'{path}[{i}]',out)
    elif a != b: out.append((path, a, b))
    return out
def ptr_get(doc, pointer):
    cur=doc
    for part in pointer.lstrip('/').split('/') if pointer else []:
        part=part.replace('~1','/').replace('~0','~')
        cur=cur[int(part)] if isinstance(cur,list) else cur[part]
    return cur
def ptr_parent(doc, pointer):
    parts=pointer.lstrip('/').split('/')
    key=parts.pop().replace('~1','/').replace('~0','~')
    parent=doc
    for part in parts:
        part=part.replace('~1','/').replace('~0','~')
        parent=parent[int(part)] if isinstance(parent,list) else parent[part]
    return parent,key
def apply_ops(doc, patch):
    for guard in patch.get('absenceGuards',[]):
        try: ptr_get(doc, guard['path'])
        except (KeyError, IndexError, ValueError): continue
        raise AssertionError('absence guard failed: '+guard['path'])
    for op in patch.get('operations',[]):
        name,path=op['op'],op['path']
        if name=='test':
            assert ptr_get(doc,path)==op['value'], ('test failed',path)
        elif name=='replace':
            parent,key=ptr_parent(doc,path)
            if isinstance(parent,list): parent[int(key)]=copy.deepcopy(op['value'])
            else: parent[key]=copy.deepcopy(op['value'])
        elif name=='add':
            parent,key=ptr_parent(doc,path)
            if isinstance(parent,list): parent.insert(len(parent) if key=='-' else int(key),copy.deepcopy(op['value']))
            else: parent[key]=copy.deepcopy(op['value'])
        elif name=='remove':
            parent,key=ptr_parent(doc,path)
            if isinstance(parent,list): parent.pop(int(key))
            else: del parent[key]
        else: raise AssertionError('unsupported patch op: '+name)
    return doc

check('return_zip_exists', ZIP_PATH.is_file(), str(ZIP_PATH))
with ZIP_PATH.open('rb') as f: actual_zip_sha=hashlib.file_digest(f,'sha256').hexdigest()
check('exact_delivered_zip_size', ZIP_PATH.stat().st_size==492999414, ZIP_PATH.stat().st_size)
check('exact_delivered_zip_sha256', actual_zip_sha==EXPECTED_ZIP_SHA, actual_zip_sha)
with zipfile.ZipFile(ZIP_PATH) as z:
    names=z.namelist()
    check('unique_safe_zip_paths',len(names)==len(set(names)) and all(not n.startswith('/') and '..' not in Path(n).parts for n in names),len(names))
    check('zip_crc',z.testzip() is None,z.testzip())
    manifest=json.loads(z.read('MANIFEST.json'))
    members=manifest['members']
    check('manifest_cardinality',len(members)==len(names)-1 and manifest['memberCountIncludingSelf']==len(names),{'manifest':len(members),'zip':len(names)})
    check('manifest_exact_path_set',set(x['path'] for x in members)==set(names)-{'MANIFEST.json'},None)
    for i,m in enumerate(members):
        b=z.read(m['path'])
        check(f'manifest_member_{i}',len(b)==m['bytes'] and sha(b)==m['sha256'],m['path'])
    review=json.loads(z.read('REVIEW_STATUS.json'))
    proposal=json.loads(z.read('APPLICATION_PROPOSAL.json'))
    precedence=json.loads(z.read('CURRENT_RECEIPT_PRECEDENCE.json'))
    receipt=json.loads(z.read('FOCUSED_CORRECTION_RECEIPT.json'))
    check('status_exact_pending_one_identity',review['pendingCorrectionIds']==['find-the-path'] and review['acceptedByAuthor'] is False and review['appliedByAuthor'] is False,review['pendingCorrectionIds'])
    check('application_proposal_selects_only_find_path',proposal['onlySelectableIdentityIds']==['find-the-path'] and len(proposal['operations'])==1 and proposal['operations'][0]['identityId']=='find-the-path',proposal['onlySelectableIdentityIds'])
    check('seven_previous_identities_excluded',set(proposal['alreadyAppliedIdsExcludedFromNewSelection'])==set(review['alreadyAppliedExactIds']) and len(review['alreadyAppliedExactIds'])==7,None)
    index_raw=INDEX_PATH.read_bytes(); idx=json.loads(index_raw.decode('utf-8-sig'))
    check('current_index_exact_hash',sha(index_raw)==EXPECTED_INDEX_SHA==proposal['currentIndexSha256'],sha(index_raw))
    check('current_index_counts_match',idx['authoredCounts']=={'reviewed':635,'pending':213},idx['authoredCounts'])
    row=next(x for x in idx['entries'] if x['id']=='find-the-path')
    check('selected_identity_is_exact_current_pending',row==proposal['operations'][0]['testCurrentIndexEntry'],row)
    current_rows={x['id']:x for x in idx['entries']}
    check('seven_prior_information_identities_are_already_reviewed',all(current_rows[i]['authoredStatus']=='reviewed-authored-operational-playtest' for i in review['alreadyAppliedExactIds']),review['alreadyAppliedExactIds'])
    check('current_receipt_is_exact',precedence['currentActualCoverage']=={'applied':635,'pending':213,'standalone':359,'scopedInterfaces':173,'acceptedUnapplied':0} and precedence['pendingInformationIds']==['find-the-path'],precedence)
    check('focus_correction_preserves_bound_return02',receipt['boundExactReceivedReturn02']['sha256']==EXPECTED_PRIOR_SHA and receipt['boundExactReceivedReturn02']['bytes']==482654646 and receipt['acceptanceApplicationByAuthor'] is False,receipt['boundExactReceivedReturn02'])
    procedures=z.read('PROCEDURES.json')
    check('all_eight_procedures_unchanged_from_return02',procedures==(PRIOR_DIR/'PROCEDURES.json').read_bytes(),len(procedures))
    for fn in ['SHARED_RULES.json','NATIVE_ACCESS_RECORDS.json','HOLDS.json','ORIGINAL_CASE_DISPOSITIONS.json']:
        check('unchanged_'+fn,z.read(fn)==(PRIOR_DIR/fn).read_bytes(),fn)
    old_case_names={p.name for p in (PRIOR_DIR/'cases').glob('*.json')}
    new_case_names={n.split('/',1)[1] for n in names if n.startswith('cases/') and n.endswith('.json')}
    check('case_file_set_unchanged',old_case_names==new_case_names,len(new_case_names))
    changed=[]
    for name in sorted(old_case_names):
        before=(PRIOR_DIR/'cases'/name).read_bytes(); after=z.read('cases/'+name)
        if before!=after: changed.append(name)
    check('only_find_path_case_changed',changed==['DI6-04-B.json'],changed)
    oldcase=json.loads((PRIOR_DIR/'cases/DI6-04-B.json').read_bytes()); newcase=json.loads(z.read('cases/DI6-04-B.json'))
    diffs=walk_diff(oldcase,newcase,'DI6-04-B')
    expected_paths={
      'DI6-04-B.branches[0].finalState.views.E[1].permittedInformation',
      'DI6-04-B.branches[0].timeline[12].after.views.E[1].permittedInformation',
      'DI6-04-B.branches[0].timeline[12].afterStateSha256',
      'DI6-04-B.branches[0].timeline[12].observations.recipientOutputExactly',
      'DI6-04-B.branches[0].timeline[12].observations.surroundingTopologyReasonPrivateOnly'}
    check('only_five_expected_case_paths_changed',{x[0] for x in diffs}==expected_paths,[x[0] for x in diffs])
    branch=newcase['branches'][0]; event=branch['timeline'][12]
    check('recipient_output_exact_after_new_paid_inquiry',event['after']['views']['E'][1]['permittedInformation']=='Indeterminate' and event['observations']['recipientOutputExactly']=='Indeterminate' and branch['finalState']['views']['E'][1]['permittedInformation']=='Indeterminate',None)
    check('private_qualification_preserved',event['after']['receipts']['NEW-PATH']['qualifiedPartialInformation']==EXPECTED_PRIVATE and event['observations']['surroundingTopologyReasonPrivateOnly'] is True and '120ft is a supplied possible detour, not a proven globalshortest afterbar.' in newcase['wholeCaseQualification']['unavailablePart'],None)
    check('old_recipient_disclosure_removed',EXPECTED_PUBLIC_OLD not in json.dumps(newcase,ensure_ascii=False),None)
    recipient_fields=[]
    def collect_recipient_fields(value,path='$'):
        if isinstance(value,dict):
            for k,v in value.items():
                p=path+'.'+str(k)
                if k in {'permittedInformation','recipientOutputExactly','publicResult'} and isinstance(v,str): recipient_fields.append((p,v))
                collect_recipient_fields(v,p)
        elif isinstance(value,list):
            for i,v in enumerate(value): collect_recipient_fields(v,f'{path}[{i}]')
    collect_recipient_fields(newcase)
    public_leaks=[(p,v) for p,v in recipient_fields if 'surrounding topology' in v.lower() or 'shorteststatus is unproved' in v.lower() or 'shortest surviving route is not established' in v.lower()]
    check('no_private_topology_reason_in_any_recipient_output',not public_leaks,public_leaks[:3])
    check('no_complete_shortest_route_claim',event['after']['receipts']['NEW-PATH']['completeShortestRouteCertified'] is False and event['observations']['completeShortestPositiveUnproved'] is True,None)
    old_cb=json.loads((PRIOR_DIR/'CASEBOOK.json').read_bytes()); new_cb=json.loads(z.read('CASEBOOK.json'))
    old_map={x['id']:x for x in old_cb['mainCases']}; new_map={x['id']:x for x in new_cb['mainCases']}
    check('casebook_case_set_unchanged',set(old_map)==set(new_map) and len(new_map)==16,len(new_map))
    cbchanged=[k for k in old_map if old_map[k]!=new_map[k]]
    check('casebook_only_find_path_changed',cbchanged==['DI6-04-B'],cbchanged)
    cb_diff=walk_diff(old_map['DI6-04-B'],new_map['DI6-04-B'],'CASEBOOK.DI6-04-B')
    check('casebook_copy_matches_exact_five_diffs',{x[0].removeprefix('CASEBOOK.') for x in cb_diff}==expected_paths,[x[0] for x in cb_diff])
    old_ops=json.loads((PRIOR_DIR/'EVENT_OPERATIONS.json').read_bytes()); new_ops=json.loads(z.read('EVENT_OPERATIONS.json'))
    om={x['eventId']:x for x in old_ops}; nm={x['eventId']:x for x in new_ops}
    opchanged=[k for k in sorted(set(om)|set(nm)) if om.get(k)!=nm.get(k)]
    event_id='DI6-04-B/actual-crossbar-after-snapshot:12'
    check('only_exact_recipient_view_operation_changed',opchanged==[event_id],opchanged)
    op=nm[event_id]
    check('operation_expected_hashes_match_case_event',op['expectedBeforeSha256']==event['beforeStateSha256'] and op['expectedAfterSha256']==event['afterStateSha256'],op['expectedAfterSha256'])
    check('case_event_state_hashes_valid',state_sha(event['before'])==event['beforeStateSha256'] and state_sha(event['after'])==event['afterStateSha256'],{'before':state_sha(event['before']),'after':state_sha(event['after'])})
    replay=apply_ops(copy.deepcopy(event['before']),op['forward'])
    check('forward_operation_exactly_reaches_after',replay==event['after'],None)
    reversed_state=apply_ops(copy.deepcopy(replay),op['inverse'])
    check('inverse_operation_exactly_restores_before',reversed_state==event['before'],None)
    check('forward_and_inverse_hashes_match',state_sha(replay)==op['expectedAfterSha256'] and state_sha(reversed_state)==op['expectedBeforeSha256'],None)
    questions=json.loads(z.read('QUESTION_DISPOSITIONS.json'))
    q_old=json.loads((PRIOR_DIR/'QUESTION_DISPOSITIONS.json').read_bytes())
    qdiff=walk_diff(q_old,questions,'QUESTIONS')
    expected_qpaths={'QUESTIONS[8].answer','QUESTIONS[9].answer','QUESTIONS[21].answer','QUESTIONS[24].answer'}
    check('question_changes_confined_to_four_path_correction_notes',{x[0] for x in qdiff}==expected_qpaths,[x[0] for x in qdiff[:10]])
    check('question_correction_note_exact_and_additive',all(x[2].startswith(x[1]) and x[2][len(x[1]):]==' RETURN03: The actual postbar recipient output is exactly Indeterminate. Missing surrounding-topology/shortest-proof reasons remain private authored qualifications, never recipient-visible failure diagnostics. No route procedure/key/bar/cost/clock changes.' for x in qdiff),[x[0] for x in qdiff])
    current_hold=json.loads(z.read('HOLDS.json'))
    hold=next(x for x in current_hold['holds'] if x['id']=='PROTECTED-SHORTER-TERRAIN')
    check('shortest_path_hold_retained',hold['wholeOriginalPreserved'] is True and 'not fabricate' in hold['disposition'].lower() and 'positive specifically not claimed demonstrated' in hold['disposition'].lower(),hold)
    check('director_did_not_accept_or_apply',review['acceptedByAuthor'] is False and review['appliedByAuthor'] is False and receipt['acceptanceApplicationByAuthor'] is False,None)

# Verify the exact prior owner-return archive and its full member bindings independently.
check('prior_return_zip_exists',PRIOR_ZIP.is_file(),str(PRIOR_ZIP))
with PRIOR_ZIP.open('rb') as f: prior_sha=hashlib.file_digest(f,'sha256').hexdigest()
check('prior_return02_exact_archive',PRIOR_ZIP.stat().st_size==482654646 and prior_sha==EXPECTED_PRIOR_SHA,prior_sha)
report={'id':'INFORMATION8-RETURN03-INDEPENDENT-EXACT-AUDIT-129','status':'PASS','checksPassed':len(CHECKS),'failed':0,'archive':{'bytes':ZIP_PATH.stat().st_size,'sha256':actual_zip_sha,'members':len(names)},'focus':{'identity':'find-the-path','onlyChangedCase':'DI6-04-B','onlyChangedEvent':event_id,'forwardInverseExact':True,'pendingBefore':213,'acceptedUnappliedBefore':0},'checks':CHECKS}
(AUDIT/'INFORMATION8_RETURN03_INDEPENDENT_EXACT_AUDIT_129.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False,indent=2))
