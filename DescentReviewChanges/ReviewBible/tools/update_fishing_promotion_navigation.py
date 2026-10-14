"""Record the verified Fishing promotion without closing broader game work."""
from datetime import datetime,timezone
import re,shutil,subprocess,sys,json
from build_fishing_recipe_candidate import ROOT,GAME,AUDIT,read,write,dump,sha,EXACT_AUTH


def main():
    review=ROOT/'docs/mechanics/FISHING_REVIEW_STATUS.json';manifest=read(review)
    assert manifest['aggregateReviewedRecipes']==392 and manifest['validationChecks']==717
    assert all(sha(GAME/p)==h for p,h in manifest['artifactHashes'].items())
    protected=read(AUDIT/'FISHING_PART2_SUBMISSION.json')['protectedFiles']
    assert all(sha(GAME/p)==h for p,h in protected.items())
    paths=[GAME/'START_HERE.md',AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md',
        AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json',ROOT/'data/playtest/game_development_coverage.json',
        ROOT/'tools/build_crafting_recipe_review_catalog.py',ROOT/'tools/build_crafting_review_queue.py',
        ROOT/'tools/build_feat_review_queue.py',ROOT/'data/director/crafting_recipe_review_catalog.json',
        ROOT/'data/playtest/crafting_recipe_review_catalog_public.json',ROOT/'docs/mechanics/CRAFTING_RECIPE_REVIEW_INDEX.md',
        ROOT/'docs/director-only/CRAFTING_REVIEW_QUEUE.md',AUDIT/'CRAFTING_RECIPE_REVIEW_CATALOG_VALIDATION.json',
        AUDIT/'CRAFTING_REVIEW_QUEUE_VALIDATION.json']
    archive=AUDIT/'navigation-before-fishing-promotion';assert not archive.exists();hashes={}
    for p in paths:
        target=archive/p.relative_to(GAME);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
        hashes[p.relative_to(GAME).as_posix()]=sha(p)
    dump(archive/'MANIFEST.json',hashes)
    p=ROOT/'tools/build_crafting_recipe_review_catalog.py';text=p.read_text(encoding='utf-8')
    marker="        ('Jewelcrafting','data/director/jewelcrafting_recipe_candidate_internal.json','docs/mechanics/JEWELCRAFTING_REVIEW_STATUS.json','docs/mechanics/JEWELCRAFTING_PUBLIC_RECIPE_CARDS.md','docs/director-only/JEWELCRAFTING_INTERNAL_RECIPE_CARDS.md'),"
    assert marker in text
    text=text.replace(marker,marker+"\n        ('Fishing','data/director/fishing_recipe_candidate_internal.json','docs/mechanics/FISHING_REVIEW_STATUS.json','docs/mechanics/FISHING_PUBLIC_RECIPE_CARDS.md','docs/director-only/FISHING_INTERNAL_RECIPE_CARDS.md'),")
    write(p,text)
    p=ROOT/'tools/build_crafting_review_queue.py';text=p.read_text(encoding='utf-8')
    for old,new in [('len(checked_manifests)==8','len(checked_manifests)==9'),("sum(x['reviewed'] for x in rows)==348","sum(x['reviewed'] for x in rows)==392"),
            ('prepared_only==339','prepared_only==295'),('**348 of 687 recipes reviewed; 339 remain.** All339','**392 of 687 recipes reviewed; 295 remain.** All295'),
            ('Public operational reviews are223 of433','Public operational reviews are251 of433'),
            ("'reviewed':348,'remaining':339","'reviewed':392,'remaining':295"),("'otherSourcePrepared':339","'otherSourcePrepared':295"),
            ("'verifiedReviewedManifests':8","'verifiedReviewedManifests':9")]:
        assert old in text,old;text=text.replace(old,new)
    text=text.replace('Fishing is the next prepared source conference; use current reviewed dependencies and check the actual dispatch state before sending.',
        'Fishing exact review is also complete: FI-E01..11 fulfilled,44 cards promoted after717 checks,63 protected inputs unchanged;28 public cards. Rebase the unsent gathering-tool packet on these reviewed interfaces while preserving its original evidence. Check actual dispatch state before sending.')
    write(p,text)
    p=ROOT/'tools/build_feat_review_queue.py';text=p.read_text(encoding='utf-8')
    text=text.replace('Jewelcrafting exact review is complete; Fishing is the next planned source conference. Check live dispatch state before sending any feat packet.',
        'Fishing exact review is complete; the gathering-tool source conference is next. Check live dispatch state before sending any feat packet.')
    write(p,text)
    statement=('**Current joint work:** All44 Fishing cards are now reviewed operational PLAYTEST content under the '
        '[actual exact verdict]({prefix}GPT_FISHING_EXACT_OPERATIONAL_REVIEW.md). '
        '[FI-E01–11 are fulfilled]({prefix}FISHING_EXACT_REPAIRS_APPLIED.json): 130 source/arithmetic,90 sequence,368 focused regression and129 projection/integration checks pass (717 total). '
        'All63 protected inputs and original submissions remain preserved. Current recipe totals are392/687 reviewed,295 remaining;public251/433. '
        'Next: rebase and confer on the128 gathering-tool sources,then167 advanced-trade sources and remaining whole-game systems. '
        'Runtime,human balance,final joint flow review,GitHub push and post-push cosmology remain separate gates.')
    for p,prefix in [(GAME/'START_HERE.md','docs/audit/2026-10-08/full-game/'),(AUDIT/'GPT_REVIEW_CONTINUATION_HANDOFF.md','')]:
        text=p.read_text(encoding='utf-8');text,n=re.subn(r'^\*\*Current joint work:\*\*.*$',statement.format(prefix=prefix),text,count=1,flags=re.M);assert n==1
        if p.name=='START_HERE.md':
            text=text.replace('**348 of 687 reviewed; 339 remain.** Public: 223 of 433 reviewed','**392 of 687 reviewed; 295 remain.** Public: 251 of 433 reviewed')
            text=text.replace('Fishing44 required repairs, then 128 gathering-tool and 167 advanced-trade sources','128 gathering-tool and 167 advanced-trade sources')
            text=text.replace('Tailoring and Jewelcrafting. Individual review','Tailoring, Jewelcrafting and Fishing. Individual review')
            text,n=re.subn(r'^\| Fishing \|.*$',
                '| Fishing | [Reviewed public guide](DescentReviewChanges/ReviewBible/docs/mechanics/FISHING_RECIPE_PLAYTEST.md), [public cards](DescentReviewChanges/ReviewBible/docs/mechanics/FISHING_PUBLIC_RECIPE_CARDS.md), [completion receipt](docs/audit/2026-10-08/full-game/FISHING_EXACT_REPAIRS_APPLIED.json). All44 cards promoted;28 public;717 checks pass. |',text,count=1,flags=re.M);assert n==1
        else:
            text=text.replace('**348 of687 reviewed;339 remain**. Public totals: **223 of433 reviewed;210 remain**','**392 of687 reviewed;295 remain**. Public totals: **251 of433 reviewed;182 remain**')
            text=text.replace('The actual exact verdict now requires FI-E01..11 repairs; current implementation and evidence are recorded above.',
                'FI-E01..11 have now been fulfilled and all44 cards promoted; the current completion receipt is recorded above.')
            text=text.replace('Fishing exact review remains active.','Fishing exact review has since completed; see the current receipt above.')
            text=text.replace('Fishing exact review remains the active notebook request.','Fishing exact review has since completed; this paragraph preserves the earlier preparation checkpoint.')
            text=text.replace('Current totals348/687 reviewed,339 remaining;public223/433. Fishing44 is now authored; its exact review remains pending. No Fishing approval, deletion, push or cosmology review.',
                'Historical totals at that Jewelcrafting checkpoint were348/687 reviewed,339 remaining;public223/433. Fishing has since completed; current totals and its receipt appear above. No deletion,push or cosmology review occurred.')
        write(p,text)
    p=ROOT/'data/playtest/game_development_coverage.json';coverage=read(p)
    for aspect in coverage['aspects']:
        if aspect['id'] not in ('DD-28','DD-29','DD-30','DD-38','DD-39','DD-40'):continue
        old=[s for s in aspect['openIssues'] if s.startswith('Fishing44 exact verdict requires') or s.startswith('Current recipe pass348/')]
        aspect.setdefault('resolvedIssueHistory',[]).extend(old);aspect['openIssues']=[s for s in aspect['openIssues'] if s not in old]
        aspect.setdefault('completedScopes',[]).append('Fishing44 authored operational PLAYTEST cards promoted under actual FI-E01..11 conditional authority;717 checks,63 protected inputs unchanged; public28 cards,guide andJSON verified. No runtime,human-balance,availability or whole-game approval inferred.')
        aspect['openIssues'].append('Fishing scoped card review is complete; broader availability,harvesting/economy/Supply/body interfaces,runtime and human balance remain for whole-game integration.')
        for name in ['FISHING_EXACT_REPAIRS_APPLIED.json','FISHING_REPAIRED_COMPLETION_VALIDATION.json']:
            rel='docs/audit/2026-10-08/full-game/'+name
            if rel not in aspect['validationEvidence']:aspect['validationEvidence'].append(rel)
        if aspect['id']=='DD-29':
            aspect['openIssues'].append('Current recipe pass392/687 reviewed,295 remaining,public251/433. Complete Mining43,Skinning43,Salvaging42,Enchanting43,RuneCarving41,Scribing40,Tinkering43 and broader interfaces; pending sources prepared but not approved.')
            aspect['fishingCurrentCheckpoint']='FI-E01..11 fulfilled;44 reviewed operational cards. See FISHING_REVIEW_STATUS.json and completion receipt.'
    dump(p,coverage)
    p=AUDIT/'GPT_REVIEW_CONTINUATION_CURRENT_OBSERVATION.json';observation=read(p)
    observation['observedAtUtc']=datetime.now(timezone.utc).isoformat();observation['threadStatus']='idle'
    observation['currentRequest'].update({'status':'Completed exact Fishing verdict; FI-E01..11 fulfilled;44 cards promoted',
        'completedExactVerdictPending':False,'completedExactVerdictPresent':True,'replyId':EXACT_AUTH['replyId'],
        'completionReceipt':'FISHING_EXACT_REPAIRS_APPLIED.json','notebookStatusAsObserved':'idle'})
    observation['authoredProgress'].update({'status':'All44 Fishing operational cards reviewed and promoted',
        'checks':717,'sourceProjectionArithmeticChecks':130,'focusedRepairChecks':368,'sequenceChecks':90,
        'projectionAndIntegrationChecks':129,'implementedRepairAreas':[f'FI-E{i:02}' for i in range(1,12)],
        'fullOriginalSequenceRevalidationPending':False,'exactReviewReady':True,'currentReviewedRecipes':392,
        'newApprovals':44,'publicReviewed':251,'remainingRecipes':295})
    observation['currentGoalTurnClassification']='progress: FI-E09 completed,all original valid sequences rerun,FI-E11 full projection/literal/source gate passed;44 Fishing cards promoted under actual conditional verdict'
    observation['consecutiveBlockedGoalTurns']=0
    observation['nextAction']='Confer with GPT on the completed Fishing receipt,then rebase the unsent gathering-tool source conference on current reviewed rules while preserving original packets. Whole-game integration and final joint flow review precede authorized push; verify remote commit before cosmology.'
    dump(p,observation)
    for script in ('build_crafting_recipe_review_catalog.py','build_crafting_review_queue.py','build_game_coverage.py'):
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/script)],check=True)
    assert all(sha(GAME/p)==h for p,h in protected.items())
    assert all(sha(GAME/p)==h for p,h in manifest['artifactHashes'].items())
    dump(AUDIT/'FISHING_PROMOTION_NAVIGATION_RECEIPT.json',{'status':'PASS','reviewedRecipes':392,'remainingRecipes':295,
        'publicReviewed':251,'publicRemaining':182,'protectedInputsUnchanged':63,'broaderGoalClosed':False,
        'sourceInformationDeleted':False,'githubPushed':False,'cosmology':'post-push only'})
    print('Fishing promotion navigation complete; broader game coverage remains open.')


if __name__=='__main__':main()
