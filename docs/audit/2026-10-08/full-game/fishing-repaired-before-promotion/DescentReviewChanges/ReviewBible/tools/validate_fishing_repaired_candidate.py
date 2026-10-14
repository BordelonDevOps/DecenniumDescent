"""FI-E11: verify the repaired full candidate against the actual finite verdict.

This produces a version-bound prepromotion receipt. It does not promote cards,
authenticate synthetic world premises, or close any broader game gate.
"""
from copy import deepcopy
from collections import Counter
from pathlib import Path
import json,re,subprocess,sys,zipfile,xml.etree.ElementTree as ET
from build_fishing_recipe_candidate import ROOT,GAME,AUDIT,read,sha,dump,EXACT_AUTH


def independent_projection(value):
    private={'restricted','director-only','director-internal'}
    if isinstance(value,dict):
        if value.get('visibility') in private:return None
        return {k:independent_projection(v) for k,v in value.items()
            if k not in {'directorGuidance','directorNotes','secret','secrets'} and
            not (isinstance(v,dict) and v.get('visibility') in private)}
    if isinstance(value,list):
        return [independent_projection(v) for v in value
            if not (isinstance(v,dict) and v.get('visibility') in private)]
    return deepcopy(value)


def main():
    assert not (ROOT/'docs/mechanics/FISHING_REVIEW_STATUS.json').exists(), 'Prepromotion receipt is preserved after promotion; verify final hashes through the review manifest'
    for script in ('validate_fishing_recipe_candidate.py','validate_fishing_sequences.py','validate_fishing_exact_repairs.py'):
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/script)],check=True)
    source_report=read(AUDIT/'FISHING_REPAIRED_SOURCE_VALIDATION.json')
    sequences=read(AUDIT/'FISHING_REPAIRED_SEQUENCE_VALIDATION.json')
    focused=read(AUDIT/'FISHING_EXACT_REPAIR_VALIDATION.json')
    rows=[]
    def check(name,condition):
        rows.append({'name':name,'pass':bool(condition)});assert condition,name
    def equal(actual,expected):
        if actual!=expected:raise ValueError('Reconstructed artifact differs')
    def reject(name,fn):
        try:fn()
        except ValueError:check(name,True);return
        check(name,False)
    verdict=AUDIT/'GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md'
    check('Actual exact verdict and separate operational authority preserved',sha(verdict)==EXACT_AUTH['sha256'] and
        EXACT_AUTH['replyId']=='f0bf49fb-8bea-499f-8243-f3db5c302bbf')
    check('All source, valid original sequences and finite FI-E01..10 regressions rerun',
        all(z['pass'] for z in source_report['checks']+sequences['checks']+focused['checks']) and
        len(source_report['checks'])==130 and len(sequences['checks'])==90 and
        focused['coveredIssues']==[f'FI-E{i:02}' for i in range(1,11)])
    check('Fresh regression hashes identify current code and artifacts',all(sha(GAME/p)==h for p,h in focused['inputHashes'].items()))
    protected=read(AUDIT/'FISHING_PART2_SUBMISSION.json')['protectedFiles']
    check('All 63 protected sources and older trade inputs unchanged',len(protected)==63 and all(sha(GAME/p)==h for p,h in protected.items()))
    archives={}
    for path in sorted(AUDIT.glob('fishing-*/MANIFEST.json')):
        manifest=read(path);check('Preserved archive '+path.parent.name,all(sha(path.parent/p)==h for p,h in manifest.items()))
        archives[path.parent.name]=len(manifest)
    submitted=read(AUDIT/'FISHING_EXACT_PART2_SUBMISSION.json')
    check('Original dispatched packets retain their exact submitted hashes',all(sha(AUDIT/v['file'])==v['sha256'] for v in submitted['parts'].values()))
    original=AUDIT/'fishing-exact-submission-original'
    check('Original submitted six artifact hashes remain verifiable',all(sha(original/(ROOT/p).relative_to(GAME))==h for p,h in submitted['artifactHashes'].items()))

    internal=read(ROOT/'data/director/fishing_recipe_candidate_internal.json')
    public=read(ROOT/'data/playtest/fishing_recipe_candidate.json')
    originals=read(ROOT/'data/crafting/Decennium_Descent_Crafting_Bible_v4.json')['recipes']
    cards=internal['cards'];public_ids=[f'recipe-{i}' for i in [*range(160,185),640,641,642]]
    check('All 44 originals, flags, indices and exact work/access fields preserved',len(cards)==44 and all(c['sourceRecipe']==originals[c['sourceRecipeIndex']] for c in cards))
    check('212 mandatory consumed occurrences and zero catalysts retained',sum(len(c['sourceRecipe']['components']) for c in cards)==212 and all(z['consumed'] and z['role']!='catalyst' for c in cards for z in c['sourceRecipe']['components']))
    check('Exact public identities, nine models, and 13/14 operative affinities',
        [c['recipeId'] for c in public['cards']]==public_ids and len(internal['baseModels'])==len(public['baseModels'])==9 and
        len(public['sharedOperationalProfile']['affinityRegistry'])==13 and len(internal['sharedOperationalProfile']['affinityRegistry'])==14)
    old=read(original/(ROOT/'data/director/fishing_recipe_candidate_internal.json').relative_to(GAME))
    check('Every original individual operational card remains numerically and textually unchanged',
        [c['operational'] for c in cards]==[c['operational'] for c in old['cards']])
    expected=deepcopy(internal);expected['visibility']='public';expected=independent_projection(expected)
    expected['sharedOperationalProfile']['affinityRegistry'].pop('Cold');expected['sharedGuide']='docs/mechanics/FISHING_RECIPE_PLAYTEST.md'
    check('Entire public envelope equals independently reconstructed projection',expected==public)

    im=(ROOT/'docs/director-only/FISHING_INTERNAL_RECIPE_CARDS.md').read_text(encoding='utf-8')
    pm=(ROOT/'docs/mechanics/FISHING_PUBLIC_RECIPE_CARDS.md').read_text(encoding='utf-8')
    sections={}
    for c in cards:
        start=im.index('## '+c['recipeId']+' — ');end=im.find('\n## recipe-',start+1)
        sections[c['recipeId']]=im[start:end if end>=0 else len(im)].rstrip('\n')
    expected_pm=('# Fishing public recipe cards\n\n**DRAFT; required exact-review corrections in progress.** '
        'Public: 28 formulas, nine models and thirteen operative affinities.\n\n'
        'Every card uses the complete [shared guide](FISHING_RECIPE_PLAYTEST.md). The JSON preserves full source objects.\n\n')
    public_sections=[]
    for ident in public_ids:
        section=re.sub(r'\*\*Preserved optional Director guidance \(inactive pending separate variant review\):\*\* [^\n]*\n\n','',sections[ident])
        public_sections.append(section)
    expected_pm+='\n\n'.join(public_sections)+'\n'
    check('Entire public manuscript reconstructs independently from exact internal paragraphs',pm==expected_pm)
    for audience,data,manuscript in [('internal',internal,im),('public',public,pm)]:
        for c in data['cards']:
            start=manuscript.index('## '+c['recipeId']+' — ');end=manuscript.find('\n## recipe-',start+1)
            section=manuscript[start:end if end>=0 else len(manuscript)]
            check(audience+' '+c['recipeId']+' JSON effect equals its own exact paragraph',
                section.split('**Operational effect:** ',1)[1].split('\n\n',1)[0]==c['operational']['text'])
    ig=(ROOT/'docs/director-only/FISHING_INTERNAL_GUIDE.md').read_text(encoding='utf-8')
    pg=(ROOT/'docs/mechanics/FISHING_RECIPE_PLAYTEST.md').read_text(encoding='utf-8')
    expected_pg=ig.replace('Internal: all 44 formulas (28 public, three restricted and thirteen Director-only), nine models and fourteen affinities.',
        'Public: 28 formulas, nine models and thirteen operative affinities.').replace('../mechanics/','')
    expected_pg=re.sub(r'^\| Cold \|.*\n','',expected_pg,flags=re.M)
    check('Entire public guide independently reconstructs from shared internal rules',pg==expected_pg)
    text=json.dumps(public,ensure_ascii=False)+pm+pg
    check('Private cards, nested guidance, links and unused Cold registry row excluded',
        all(c['recipeId'] not in text and c['name'] not in text for c in cards if c['visibility']!='public') and
        not any(k in json.dumps(public) for k in ('"directorGuidance"','"directorNotes"','"secret"','"secrets"')) and
        not re.search(r'\]\([^)]*director-only',pm+pg) and 'Cold' not in public['sharedOperationalProfile']['affinityRegistry'] and '| Cold |' not in pg)
    wrong=deepcopy(public);wrong['cards'].append(deepcopy(next(c for c in cards if c['visibility']!='public')))
    reject('Projection negative: private card injection',lambda:equal(wrong,expected))
    wrong=deepcopy(public);wrong['cards'][0]['sourceRecipe']['directorGuidance']={'secret':'injected'}
    reject('Projection negative: nested private guidance injection',lambda:equal(wrong,expected))
    wrong=deepcopy(public);wrong['sharedOperationalProfile']['affinityRegistry']['Cold']=internal['sharedOperationalProfile']['affinityRegistry']['Cold']
    reject('Projection negative: unused Cold registry injection',lambda:equal(wrong,expected))
    reject('Projection negative: private manuscript link injection',lambda:equal(pm+'[private](../director-only/private.md)\n',expected_pm))

    book=GAME/'books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx'
    with zipfile.ZipFile(book) as z:tree=ET.fromstring(z.read('word/document.xml'))
    w='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    paragraphs=[''.join(t.text or '' for t in p.iter(w+'t')) for p in tree.iter(w+'p')]
    for c in public['cards']:
        binding=c['publicBookBinding'];check(c['recipeId']+' all six paragraphs equal actual V5 book',
            len(binding['paragraphs'])==6 and all(paragraphs[p['index']]==p['text'] and p['text'].replace('|','\\|') in pm for p in binding['paragraphs']))
    backlog=read(AUDIT/'FISHING_HISTORICAL_TRANSPORT_BACKLOG.json');reference=backlog['sporefolkAdultReference']
    literal=(GAME/reference['sourcePath']).read_text(encoding='utf-8').splitlines()[reference['sourceLine']-1]
    check('Literal Sporefolk line, locator and source hash verified without reconciling other names',
        literal==reference['literalLine']=='**Known recipe links:** Greater Living Root Cake, Minor Vital Soup, Minor Verdant Net, Refined Verdant Tackle.' and
        sha(GAME/reference['sourcePath'])==reference['sourceSha256'] and not reference['otherPrintedNamesReconciled'])
    by_id={c['recipeId']:c['sourceRecipe'] for c in cards}
    check('All three historical boat links retain real source names and effects',
        [e['sourceRecipeId'] for e in backlog['entries']]==['recipe-172','recipe-173','recipe-177'] and
        all(e['legacyName']==by_id[e['sourceRecipeId']]['legacyName'] and e['legacyEffect']==by_id[e['sourceRecipeId']]['legacyEffect'] and
            e['currentName']==by_id[e['sourceRecipeId']]['name'] and e['currentBody']=='fishing.tackle' and
            not e['newRecipe'] and not e['vehicleStatisticsApproved'] for e in backlog['entries']))
    cases=(AUDIT/'FISHING_REPAIRED_WORKED_SCENARIOS.md').read_text(encoding='utf-8')
    repairs=(AUDIT/'FISHING_EXACT_REPAIR_WORKED_CASES.md').read_text(encoding='utf-8')
    check('All 24 full-scope cases and ten finite repair case groups retained',
        re.findall(r'^## FI-(\d\d)',cases,re.M)==[f'{i:02}' for i in range(1,25)] and
        re.findall(r'^## FI-E(\d\d)',repairs,re.M)==[f'{i:02}' for i in range(1,11)])
    check('Reviewed arithmetic unchanged: 528 quality, 156 structural, 76 quotations',
        len(source_report['qualityCases'])==528 and len(source_report['structuralCases'])==156 and len(source_report['repairQuotes'])==76)
    files=[ROOT/p for p in read(AUDIT/'FISHING_AUTHORING_STATUS.json')['outputs']]
    files.extend([Path(__file__),ROOT/'tools/build_fishing_recipe_candidate.py',ROOT/'tools/templates/fishing_rules.md',
        AUDIT/'FISHING_REPAIRED_WORKED_SCENARIOS.md',AUDIT/'FISHING_EXACT_REPAIR_WORKED_CASES.md',
        AUDIT/'FISHING_HISTORICAL_TRANSPORT_BACKLOG.json',GAME/reference['sourcePath'],book,
        AUDIT/'FISHING_REPAIRED_SOURCE_VALIDATION.json',AUDIT/'FISHING_REPAIRED_SEQUENCE_VALIDATION.json',
        AUDIT/'FISHING_REPAIRED_SEQUENCE_FIXTURES.json',AUDIT/'FISHING_EXACT_REPAIR_VALIDATION.json',verdict])
    hashes={p.relative_to(GAME).as_posix():sha(p) for p in files}
    report={'status':'PASS — repaired full-candidate prepromotion verification','completionGateSatisfied':True,
        'operationalAuthority':EXACT_AUTH,'conditionsSatisfied':[f'FI-E{i:02}' for i in range(1,12)],
        'checks':rows,'projectionAndIntegrationChecks':len(rows),'sourceChecks':130,'sequenceChecks':90,
        'focusedChecks':focused['checkCount'],'protectedInputsUnchanged':63,'preservedArchives':archives,
        'inputHashes':hashes,'regressionInputHashes':focused['inputHashes'],
        'artifactHashes':read(AUDIT/'FISHING_AUTHORING_STATUS.json')['outputs'],
        'recipesPromoted':0,'runtimeImplemented':False,'balanceApproved':False,'publicationApproved':False,
        'wholeGameFlowApproved':False,'sourceInformationDeleted':False,'githubPushed':False,'cosmology':'post-push only',
        'limits':['World premises remain externally adjudicated; synthetic fixtures do not authenticate them.',
            'Core, ecology, legal extraction, actual inventory, preservation, runtime and human balance remain separate gates.']}
    dump(AUDIT/'FISHING_REPAIRED_COMPLETION_VALIDATION.json',report)
    print(json.dumps({k:report[k] for k in ('status','projectionAndIntegrationChecks','sourceChecks','sequenceChecks','focusedChecks','protectedInputsUnchanged','recipesPromoted')}))


if __name__=='__main__':main()
