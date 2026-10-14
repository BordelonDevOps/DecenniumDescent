"""Read-only bounded source/presentation checks for this exact submitted archive.
Does not execute the game, grant features, or mutate the submission.
"""
from pathlib import Path
from collections import Counter
from hashlib import sha256
from urllib.parse import unquote
import argparse, json, re, zipfile

def digest(b): return sha256(b).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--archive',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    s=a.root;r=s/'DescentReviewChanges/ReviewBible';au=s/'docs/audit/2026-10-08/full-game';rows=[]
    def ck(group,name,actual,expected=True):
        rows.append(dict(group=group,name=name,passed=actual==expected,actual=actual,expected=expected))
    manifest=load(s/'FILE_MANIFEST.json')
    ck('manifest','payload count',len(manifest),218)
    if a.archive:
        b=a.archive.read_bytes();ck('archive','bytes',len(b),65100794);ck('archive','SHA256',digest(b),'df0390f6a17a00428e102d3de2b8195d4334f1ead80493b70ffb6dfa21b03085')
        with zipfile.ZipFile(a.archive) as z:ck('archive','member count',len(z.namelist()),219)
    for p,v in manifest.items():
        q=s/p;ck('manifest',p+' exists',q.is_file())
        if q.is_file():
            b=q.read_bytes();ck('manifest',p+' bytes',len(b),v['bytes']);ck('manifest',p+' SHA256',digest(b),v['sha256'])
    st=load(au/'TEACHING_NAVIGATION_REVIEW_STAGING.json');ck('support','147 source files',len(st['sourceFiles']),147)
    for p,v in st['sourceFiles'].items():
        actual=s/p
        if p=='docs/audit/2026-10-08/full-game/TEACHING_NAVIGATION_REVIEW_README.md':
            # This original preparation README is explicitly preserved in the supplied
            # before-exact-dispatch directory; the new dispatch README uses FILE_MANIFEST.
            actual=au/'teaching-before-exact-dispatch/TEACHING_NAVIGATION_REVIEW_README.md'
            ck('support','preparation README original archived, not current',digest(actual.read_bytes()),v['sha256'])
        else:ck('support',p,digest(actual.read_bytes()),v['sha256'])
    cases=load(au/'TEACHING_NAVIGATION_REVIEW_CHECKLIST.json');ck('scope','29 questions',len(cases['questions']),29);ck('scope','9 candidate files',len(cases['candidateFiles']),9)
    # Navigation inverse is text-level in the submitted preparer, not byte-level.
    rec=load(au/'CHARACTER_CREATION_NAVIGATION_CANDIDATE_RECEIPT.json');original=s/rec['original'];candidate=s/rec['candidate'];text=candidate.read_text();ck('navigation','five notes',len(rec['changes']),5)
    restored=text.replace(rec['candidateBanner'],'',1)
    for c in reversed(rec['changes']):
        ck('navigation','unique replacement '+c['old'][:48],restored.count(c['proposedReplacement']),1);restored=restored.replace(c['proposedReplacement'],c['old'])
    ck('navigation','inverse equals original decoded manuscript',restored,original.read_text())
    # Avoid duplicating full manuscripts in the JSON report.
    rows[-1]['actual']={'sha256Utf8':digest(restored.encode()),'characters':len(restored)};rows[-1]['expected']={'sha256Utf8':digest(original.read_text().encode()),'characters':len(original.read_text())}
    ck('navigation','original bytes still exact',digest(original.read_bytes()),rec['originalSha256'])
    lang=load(r/'data/playtest/language_communication_candidate_public.json');worksheet=(r/'docs/playtest/CHARACTER_LANGUAGE_WORKSHEET.md').read_text()
    ck('language','record contracts',len(lang['recordSchema']['definitions']),8);ck('language','eight numbered forms',len(re.findall(r'^## [1-8]\.',worksheet,re.M)),8)
    mp=load(au/'LANGUAGE_WORKSHEET_PREPARATION.json')['definitionToFormMap'];ck('language','all contracts have form mapping',{m['contractDefinition'] for m in mp}==set(lang['recordSchema']['definitions']))
    h=next(x for x in lang['grants']['baseGrants'] if x['ancestryId']=='human');ck('language','Human Common',h['derivedFixed'],['common']);ck('language','Human one choice',h['derivedChoice']['count'],1)
    nm=next(x for x in lang['grants']['variants'] if x['variantId']=='nomadic-human');ck('language','Nomadic no language increment',nm['countAdded'],0)
    bm=next(x for x in lang['grants']['backgrounds'] if x['backgroundId']=='battlefield-medic');ck('language','Battlefield Medic source Languages absent',bm['sourceLanguagesFieldPresent'],False)
    glossary=(r/'docs/playtest/PLAYTEST_TERMS_GLOSSARY.md').read_text();gloss_rows=[l for l in glossary.splitlines() if l.startswith('| ') and not l.startswith('| Term |')];ck('glossary','48 definitions',len(gloss_rows),48)
    # Read every complete class dataset, retain all cards; source ID appears in its full manuscript.
    paths=[r/'data/public/Decennium_Descent_Bard_Playtest_v0_1.json']+sorted((r/'data/public/class_playtests').glob('*.json'));ck('classes','17 full datasets',len(paths),17)
    class_receipts=[];n=0
    for p in paths:
        d=load(p);cards=d['cards'];n+=len(cards);slug=p.stem;g=r/'docs/mechanics/BARD_PLAYTEST_v0_1.md' if 'Bard_Playtest' in slug else r/f'docs/mechanics/classes/{slug}.md';gt=g.read_text();ck('classes',slug+' full manuscript exists',g.is_file());ck('classes',slug+' unique card identities',len({c['id'] for c in cards}),len(cards))
        # JSON equality is a source comparison, not a class-card promotion.
        for card in cards:ck('class-card membership',card['id'],card['id'] in gt)
        class_receipts.append({'dataPath':p.relative_to(s).as_posix(),'guidePath':g.relative_to(s).as_posix(),'cards':len(cards),'engineEntries':len(d.get('engine',[])),'datasetSha256':digest(p.read_bytes()),'guideSha256':digest(g.read_bytes()),'scope':'Parsed complete dataset and checked all card IDs against full guide; resource-reference semantics assessed separately, not 1,223 new approvals.'})
    ck('classes','1223 complete cards',n,1223)
    ca=load(r/'data/public/class_playtests/crimson-agent.json');ck('actual discrepancies','Crimson auto9 present in current engine','automatically reaches capacity 6 at class 9' in ca['engine'][7]);ck('actual discrepancies','Crimson handout omits automatic9','automatically at Crimson Agent 9' not in (r/'docs/playtest/CLASS_RESOURCE_REFERENCE.md').read_text())
    # Prior fulfillment: unchanged final representations/index; do not reopen mechanics.
    f=load(au/'LOW_RANK_136_EXACT_FULFILLMENT.json')
    for p,v in f['finalArtifacts'].items():ck('LRX carry-forward',p,digest((s/p).read_bytes()),v['sha256'])
    ip=f['authoredReviewIndex'];ck('LRX carry-forward','authored index hash',digest((s/ip['path']).read_bytes()),ip['sha256']);idx=load(s/ip['path'])
    ck('LRX carry-forward','authoredCounts receipt',f['authoredCounts'],{'reviewed':412,'pending':436})
    ck('LRX carry-forward','authoredCounts index',idx['authoredCounts'],{'reviewed':412,'pending':436})
    ck('LRX carry-forward','separate representation counts',idx['representationCounts'],{'preservedLegacyOperationalRecords':276,'completeReviewedStandaloneProcedures':136})
    ck('LRX carry-forward','index retains 848 unique identities',len({e['id'] for e in idx['entries']}),848)
    ck('LRX carry-forward','136 promoted',f['promotedAuthoredProcedures'],136);ck('LRX carry-forward','no runtime',f['runtimeVerified'],False);ck('LRX carry-forward','Blink not promoted',f['blinkPromoted'],False)
    pub=load(r/'data/public/spell_playtests/candidate_low_rank_136.json');ck('LRX carry-forward','standalone runtime selection disabled',pub.get('runtimeAdapter',{}).get('selectionEnabled') is False or pub.get('selectionEnabled') is False or '"selectionEnabled": false' in (r/'data/public/spell_playtests/candidate_low_rank_136.json').read_text())
    # Exact selected existing recipe records, not example-created recipes.
    ar=load(r/'data/crafting/advanced_craft_recipe_candidate_public.json');hr=load(r/'data/playtest/herbalism_recipe_candidate.json')
    def cards(d):return d if isinstance(d,list) else d['cards']
    def ident(c):return c.get('recipeId',c.get('id'))
    for rep,key,data in [('FIRST_CRAFT_WALKTHROUGH_SOURCE_CHECK.json','selectedPublicCard',hr),('COMPANION_COMMAND_WALKTHROUGH_SOURCE_CHECK.json','selectedPublicRecipe',ar)]:
        v=load(au/rep)[key];rid=ident(v);actual=next(c for c in cards(data) if ident(c)==rid);ck('selected recipe',rid+' complete recorded equality',v==actual)
    # Resolve every direct link and anchor in eight manuscripts. Internal archive, not a player export.
    candidates=cases['candidateFiles'];texts=[]
    for item in candidates:
        p=item if isinstance(item,str) else item.get('path',item.get('file'))
        if p and p.endswith('.md'):texts.append(s/p)
    links=[]
    def anchors(t):
        counts={};out=set()
        for raw in re.findall(r'^#{1,6}\s+(.+)$',t,re.M):
            raw=re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',raw);slug=''.join(c for c in raw.lower() if c.isalnum() or c in '_- ').replace(' ','-');base=slug;num=counts.get(base,0);counts[base]=num+1;out.add(slug if num==0 else slug+'-'+str(num))
        return out
    for p in texts:
        for raw in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if re.match(r'\w+://|mailto:',raw):continue
            rel,_,anchor=unquote(raw.strip('<>')).partition('#');target=(p.parent/rel).resolve() if rel else p.resolve();exists=target.is_file();ok=exists and (not anchor or anchor in anchors(target.read_text(encoding='utf-8-sig')))
            links.append({'from':p.relative_to(s).as_posix(),'target':str(target.relative_to(s)) if target.is_relative_to(s) else str(target),'anchor':anchor,'exists':exists,'anchorValid':ok});ck('direct navigation',p.name+' -> '+raw,ok)
    a.out.mkdir(parents=True,exist_ok=True)
    result={'scope':'Read-only exact archive, source, membership, navigation and fulfilled-gate checks. Semantic outcomes in separate TE verdict; not gameplay runtime/human trials.','checks':len(rows),'failedChecks':[x for x in rows if not x['passed']],'groupCounts':dict(Counter(x['group'] for x in rows)),'classReceipts':class_receipts,'links':links,'results':rows}
    (a.out/'TEACHING_READ_ONLY_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'checks':len(rows),'failures':len(result['failedChecks']),'groups':result['groupCounts'],'failed':result['failedChecks'][:8]},ensure_ascii=False))
    if result['failedChecks']: raise SystemExit(1)
if __name__=='__main__':main()
