"""Read-only whole-envelope checks for the frozen language exact submission.
Standard library only. Writes a report outside the supplied tree, never changes inputs.
These are byte/record/text/reference checks, not a gameplay runtime or campaign audit.
"""
from pathlib import Path
import argparse, collections, hashlib, json, re, zipfile

B='DescentReviewChanges/ReviewBible'
A='docs/audit/2026-10-08/full-game'
V=A+'/language-source-reviewer-files'
EXPECTED='788e1210d28120b5e94a6ddc4d1dcc69e48a2aeb7cfd60f434c9680b30fa2ec1'

def objects(x):
    if isinstance(x,dict):
        yield x
        for y in x.values(): yield from objects(y)
    elif isinstance(x,list):
        for y in x: yield from objects(y)

def audit(root,archive):
    checks=[]
    def check(group,name,passed,detail=None):
        c={'group':group,'name':name,'passed':bool(passed)}
        if detail is not None:c['detail']=detail
        checks.append(c)
    def read(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
    def text(p):return (root/p).read_text(encoding='utf-8-sig')
    def sha(p):return hashlib.sha256((root/p).read_bytes()).hexdigest()
    m=read('FILE_MANIFEST.json')
    check('submission','184 payload entries',len(m)==184)
    if archive:
        raw=archive.read_bytes()
        check('submission','archive bytes',len(raw)==12859675,{'actual':len(raw)})
        check('submission','archive SHA256',hashlib.sha256(raw).hexdigest()==EXPECTED)
        with zipfile.ZipFile(archive) as z:
            check('submission','exact archive membership',len(z.namelist())==185 and set(z.namelist())==set(m)|{'FILE_MANIFEST.json'})
    for p,e in m.items():
        check('manifest-integrity',p,(root/p).is_file() and (root/p).stat().st_size==e['bytes'] and sha(p)==e['sha256'])
    original=read('ORIGINAL_SOURCE_V2_FILE_MANIFEST.json')
    check('originals','152 original payloads',len(original)==152)
    for p,e in original.items():check('original-integrity',p,sha(p)==e['sha256'])
    authority_manifest=read(V+'/REVIEWER_FILE_MANIFEST.json')
    check('authority','14 manifested source-authority files',len(authority_manifest)==14)
    for p,e in authority_manifest.items():check('authority-integrity',p,sha(V+'/'+p)==e['sha256'])
    private=read(B+'/data/director/language_communication_candidate_internal.json')
    public=read(B+'/data/playtest/language_communication_candidate_public.json')
    source_author=read(V+'/LANGUAGE_AUTHORING_REGISTER.json')
    source_classes=read(V+'/CLASS_LANGUAGE_INTERFACE_REGISTER.json')
    source_pending=read(V+'/PENDING_LANGUAGE_INTERFACES.json')
    source_grants=read(V+'/GRANT_IDENTITY_REGISTER.json')
    src_advanced=read(B+'/data/director/advanced_craft_recipe_candidate_internal.json')
    pub_advanced=read(B+'/data/crafting/advanced_craft_recipe_candidate_public.json')
    advanced_by_id={r['recipeId']:r for r in src_advanced['cards']}
    pub_by_id={r['recipeId']:r for r in pub_advanced['cards']}
    source_prep=read(A+'/LANGUAGE_COMMUNICATION_SOURCE_PREPARATION.json')
    source_add=read(A+'/LANGUAGE_ADVANCED_INTERFACE_ADDENDUM.json')
    guide=text(B+'/docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md')
    worked=text(B+'/docs/mechanics/LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md')
    internal_guide=text(B+'/docs/director-only/LANGUAGE_COMMUNICATION_INTERNAL_CANDIDATE.md')
    cases=read(A+'/LANGUAGE_CANDIDATE_WORKED_ADJUDICATIONS.json')['cases']
    checklist=read(V+'/LANGUAGE_EXACT_CANDIDATE_CHECKLIST.json')['cases']
    check('whole-envelope','public chapter byte text',public['guideText']==guide)
    check('whole-envelope','public/internal ordinary rules',public['rules']==private['rules'])
    check('whole-envelope','public/internal record contracts',public['recordSchema']==private['recordSchema'])
    check('whole-envelope','public/internal all derived grants',public['grants']==private['derivedGrants'])
    check('whole-envelope','all 32 sequence objects exact in both envelopes',public['workedAdjudications']==private['workedAdjudications']==cases)
    for old,new in zip(source_author['decisions'],private['decisionApplicationRegister']):
        check('source-directions',old['id'],all(new.get(k)==v for k,v in old.items()))
        # Full original language source wording is retained in the internal guide.
        word=old['authoringWording']
        check('internal-manuscript',old['id'],word in internal_guide)
    check('source-directions','all 16 decisions present',len(private['decisionApplicationRegister'])==16)
    check('source-directions','LA16 exact receipt',private['deferredReceipt']==source_author['decisions'][-1])
    for k,count in [('baseGrants',14),('variants',45),('backgrounds',20)]:
        check('grants',k,len(public['grants'][k])==count)
    check('grants','base exact source directions',public['grants']['baseGrants']==source_grants['baseGrants'])
    check('grants','45 variants exact source directions',public['grants']['variants']==source_grants['variants'])
    for key in ('aliases','explicitlyNotAliases','dialectPolicy','scripts'):
        check('grants',key,public['grants'][key]==source_grants[key])
    known_classes={c['id']:c for c in source_classes['selectedCards']}
    extra=source_classes['additionalActuallyReadCalledCard'];known_classes[extra['id']]=extra
    check('classes','49 exact interface identities',set(known_classes)=={c['id'] for c in private['classInterfaces']} and len(private['classInterfaces'])==49)
    public_class={c['id']:c for c in public['classInterfaces']}
    for c in private['classInterfaces']:
        native=[o for o in objects(read(c['sourceFile'])) if o.get('id')==c['id']]
        check('class-source-records',c['id'],len(native)==1 and native[0]==c['originalSourceRecord'])
        check('class-dispositions',c['id'],c['disposition']==known_classes[c['id']]['disposition']==public_class[c['id']]['disposition'] and c['classCardPromoted'] is False and public_class[c['id']]['classCardPromoted'] is False)
    native_spells={c['id']:c for c in source_prep['spellComparisonRecords']}
    ps={c['id']:c for c in public['spellInterfaces']}
    for c in private['spellInterfaces']:
        n=native_spells[c['id']]
        check('spell-source-records',c['id'],c['originalSourceRecord']==n and c['status']==ps[c['id']]['status']==n['status'] and c['operational']==ps[c['id']]['operational']==n['operational'] and ps[c['id']]['classAccess']==n['classAccess'])
    check('pending','15 pending/8 operative',sum(c['operational'] is None for c in ps.values())==15 and len(ps)==23)
    check('pending','full routes and feat originals unchanged',private['pendingInterfaces']==source_pending)
    check('pending','8 pending public feat identities',len(public['pendingFeatInterfaces'])==8 and {c['id'] for c in public['pendingFeatInterfaces']}=={c['id'] for c in source_pending['feats']})
    completed=private['completedAdvancedInterfaces']
    check('advanced','40 complete Scribing records',len(completed['completeScribingCards'])==40)
    for c in completed['completeScribingCards']:check('advanced-original-records',c['recipeId'],c==advanced_by_id[c['recipeId']])
    for key,sec in completed['completeApplicableProcedureSections'].items():
        check('advanced-sections',key,sec==src_advanced['procedureSections'][key]==source_add['completeApplicableProcedureSections'][key])
    check('advanced','19 complete native sections',len(completed['completeApplicableProcedureSections'])==19)
    expected_public={c['recipeId'] for c in completed['completeScribingCards'] if c['visibility']=='public'}
    check('audience','28 exact public Scribing memberships',len(public['publicScribingCards'])==28 and {c['recipeId'] for c in public['publicScribingCards']}==expected_public)
    for c in public['publicScribingCards']:check('public-original-records',c['recipeId'],c==pub_by_id[c['recipeId']])
    rendered=json.dumps(public,ensure_ascii=False)
    for c in completed['completeScribingCards']:
        if c['visibility']!='public':check('audience-private-exclusion',c['recipeId'],not re.search(re.escape(c['recipeId'])+r'\b',rendered) and c['name'] not in rendered)
    check('audience','no private coordinator membership','recipe-686' not in rendered)
    check('audience','no internal source dossier keys',all(not({'originalSourceRecord','matrixResearch','hiddenMetadata'}&set(o)) for o in objects(public)))
    for case,orig in zip(cases,checklist):
        check('sequence-parity',case['id'],case['id']==orig['id'] and case['expected']==orig['expected'] and case['runtimePassed'] is False)
        block=worked.split('## '+case['id']+' — ',1)[1].split('\n## ',1)[0]
        check('sequence-manuscript',case['id'],case['setup'] in block and case['adjudicatedOutcome'] in block and all(step['event'] in block for step in case['chronology']))
    for path in [B+'/docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md',B+'/docs/mechanics/LANGUAGE_COMMUNICATION_WORKED_SEQUENCES.md',B+'/docs/director-only/LANGUAGE_COMMUNICATION_INTERNAL_CANDIDATE.md']:
        for link in re.findall(r'\]\(([^)]+)\)',text(path)):
            if '://' in link:continue
            file,_,anchor=link.partition('#');target=(root/path).parent/file if file else root/path
            check('navigation',path+' -> '+link,target.exists())
    # Contradiction detector, not a production schema validator.
    pd=public['recordSchema']['definitions']['provenance']
    check('contract-consistency','absent source value can omit sourceSpelling','sourceSpelling' not in pd['required'],{'correction':'LAX-02'})
    check('scope-consistency','TI04 device summary is explicitly automaton scoped',not guide.startswith('A crafted device requires') and '\nA crafted device requires' not in guide and 'scope' in public['rules']['deviceControl'],{'correction':'LAX-03'})
    profiles={c['recipeId']:c['operational']['profile'] for c in src_advanced['cards'] if c['sourceRecipe']['skill']=='Tinkering'}
    return {'reviewId':'LAX-EXACT-2026-10-11','scope':'Independent read-only bytes, full recursive source/envelope comparisons, manuscript parity and consistency detectors. Not runtime, campaign, human balance or automatic semantic certification.', 'archiveSha256':EXPECTED,'checks':checks,'count':len(checks),'passed':sum(c['passed'] for c in checks),'failed':[c for c in checks if not c['passed']],'groups':dict(collections.Counter(c['group'] for c in checks)),'tinkeringNativeProfiles':profiles}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--archive',type=Path);p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    root=args.root.resolve();output=args.output.resolve()
    if output==root or root in output.parents:raise SystemExit('Output must be outside the inspected tree.')
    result=audit(root,args.archive);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['count','passed','failed']},indent=2))
if __name__=='__main__':main()
