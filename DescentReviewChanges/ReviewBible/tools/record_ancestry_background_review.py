"""Record the bounded joint review and preserve all unfinished downstream gates."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT.parents[1]
AUDIT=GAME/'docs/audit/2026-10-08/full-game'
PREFIX='DescentReviewChanges/ReviewBible/'

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    reply=(AUDIT/'GPT_ANCESTRY_BACKGROUND_EXACT_REVIEW_BROWSER.txt').read_text(encoding='utf-8')
    assert 'APPROVE WITH FOUR REPAIRS' in reply
    checks=[]
    def check(name,value):checks.append({'check':name,'pass':bool(value)})
    catalog=read(ROOT/'data/public/spell_playtests/catalog.json')['spells'];by_id={s['id']:s for s in catalog}
    previous=read(AUDIT/'ANCESTRY_PROMOTION_PREVIOUS_OPERATIONAL.json')
    check('All269 previous operational records unchanged',len(previous)==269 and all(by_id[k]==v for k,v in previous.items()))
    check('276 existing identities operational,572 unfinished',sum(bool(s['operational']) for s in catalog)==276 and sum(not s['operational'] for s in catalog)==572)
    check('848 original identities and936 placements',len(catalog)==848 and sum(len(s['source']['original']['placements']) for s in catalog)==936)
    submission=read(AUDIT/'ANCESTRY_BACKGROUND_SUBMISSION.json')
    changed=[p for p,h in submission['protectedSources'].items() if sha(GAME/p)!=h]
    expected=[PREFIX+'docs/mechanics/SPELL_PLAYTEST_STARTER.md',PREFIX+'data/playtest/spell_drafts/selected_sources.json']
    check('Only expected spell reference and selected-ID index changed among162 protected paths',sorted(changed)==sorted(expected))
    check('All160 frozen book/class/companion/reference sources unchanged',all(sha(GAME/p)==h for p,h in submission['protectedSources'].items() if p not in expected))
    guide=ROOT/'docs/mechanics/ANCESTRY_BACKGROUND_PLAYTEST.md';text=guide.read_text(encoding='utf-8')
    check('Reaction permission belongs only to Symbiotic Mycelian','the Symbiotic Mycelian who owns this trait may use its Reaction' in text and 'bonded creature gains no independent Reaction permission' in text)
    check('Vitality Transfer has no invented living prerequisite','touch a distinct willing legal creature' in text and 'distinct willing legal living recipient' not in text)
    check('Troll suppression is one pending flag','at most one pending acid/fire suppression' in text and 'consume the pending suppression' in text)
    supplement=read(ROOT/'data/playtest/ancestry_spell_supplement_candidate.json')['spells']
    for s in supplement:
        if s['identityType']=='existing-catalog':
            check(s['id']+' full approved fields promoted',all(by_id[s['id']]['operational'][k]==s[k] for k in ['activation','rangeFeet','targets','duration','concentration','components','resolution','effect','scaling','limitations','designNotes']))
            check(s['id']+' provenance repair',('Water Breathing lifetime' not in s['designNotes']) and (('24-elapsed-hour' in s['designNotes'])==(s['id']=='water-breathing')))
    added=read(ROOT/'data/public/ancestry_playtests/spells.json')['spells']
    check('10 separate additions with zero ordinary access',len(added)==10 and all(not s['ordinaryClassAccess'] and s['id'] not in by_id for s in added))
    # Supporting datasets preserve exact original text; the integration guide owns changes to source procedure.
    data_path=ROOT/'data/playtest/ancestry_background_candidate.json';data=read(data_path)
    data['status']='reviewed-source-and-ASI-size-speed-reference; authored integration guide owns operational overrides'
    data['sourcePolicy']='Full book ancestry/background source plus ANCESTRY_BACKGROUND_PLAYTEST.md integration. Original trait prose is preserved evidence, not a standalone runtime implementation. No builder/variant stacking.'
    for a in data['ancestries']:
        for owner in [a]+a['variants']:
            for trait in owner['traits']:
                trait['status']='original-source-preserved; apply-reviewed-integration-guide'
                if trait['id']=='spore-mycelian--spore-preservation':trait['status']='unresolved-procedure-post-verified-push-cosmology'
                if trait['id']=='revenant--vengeful-tracker':trait['status']='same-plane-reviewed; cross-plane-representation-post-verified-push'
    for b in data['backgrounds']:b['status']='source-package-reviewed; integration-guide-and-stated-equipment-dependencies-apply'
    dump(data_path,data)
    grants_path=ROOT/'data/playtest/ancestry_spell_grants_candidate.json';grants=read(grants_path)
    grants['status']='reviewed-grant-projection; reference-data-not-runtime'
    grants['grantRoute']='Reviewed explicit ancestry route in ANCESTRY_BACKGROUND_PLAYTEST.md; no ordinary class access or RP pool is added.'
    added_ids={s['id'] for s in added}
    for row in grants['grants']:
        row['currentEffectStatus']=by_id[row['spellId']]['status'] if row['spellId'] in by_id else 'reviewed-ancestry-grant-only-supplement'
        row['school']=row.pop('proposedSchool',row.get('school'))
        if row['spellId'] in added_ids:row['identityType']='new-reviewed-ancestry-grant-only-supplement'
    for choice in grants['choiceGrants']:
        for option in choice['options']:option['currentEffectStatus']=by_id[option['spellId']]['status']
    grants['coverage'].update(existingOperational=22,existingUnfinished=0,missingNamedSpells=0,separateAncestrySupplementSpells=10)
    dump(grants_path,grants)
    check('40 fixed grants and2 choices fully bound',len(grants['grants'])==40 and len(grants['choiceGrants'])==2 and all(s['spellId'] in by_id or s['spellId'] in added_ids for s in grants['grants']))
    check('Creation projections retained',len(data['ancestries'])==14 and sum(len(a['variants']) for a in data['ancestries'])==45 and len(data['backgrounds'])==20)
    dependency=read(AUDIT/'ANCESTRY_SPELL_DEPENDENCY_AUDIT.json')
    dump(AUDIT/'ANCESTRY_SPELL_DEPENDENCY_COMPLETION.json',{'status':'All32 fixed named spell dependencies have authored reviewed effects; selectable Wizard-cantrip remainder still open',
       'initialAudit':'ANCESTRY_SPELL_DEPENDENCY_AUDIT.json','fixedGrantRows':40,'choiceGrants':2,'existingReviewedEffects':22,'separateSupplementEffects':10,'remainingWizardCantripOptions':sum(o['currentEffectStatus']!='operational-playtest-draft' for o in grants['choiceGrants'][0]['options'])})
    status={
      'status':'REVIEWED authored operational PLAYTEST ancestry/background integration, within the stated mechanical scope',
      'sourceConferenceTurn':'321c6ade-06af-423a-ad0b-fa926ede2467','exactReviewTurn':'79ec4add-1487-489c-8b33-e464c4bd8baa',
      'approvalCondition':'Exact review approves both manuscripts and complete grant/ASI/size/speed projections after four repairs, all applied.',
      'repairsApplied':['Symbiotic Bond Reaction belongs solely to the owning Mycelian.','Vitality Transfer adds no living-target prerequisite.','Troll acid/fire suppression is one nonstacking pending flag.','Seven spell designNotes have accurate individual provenance.'],
      'coverage':{'ancestries':14,'variants':45,'sourceTraitParagraphs':284,'backgrounds':20,'backgroundSourceFields':89,'fixedSpellGrants':40,'wizardCantripChoices':2,'existingSpellsNewlyReviewed':7,'newAncestryOnlySpells':10},
      'sourceCoverageChecks':391,'candidateStructureChecks':44,'ordinaryCatalogChecks':42,'classAccessBoundaries':89040,
      'originalSourcesDeleted':0,'githubPushed':False,'cosmology':'Deferred until successful authorized GitHub push and verified remote commit',
      'unclosedScope':['Spore Preservation reincarnation procedure — post-push cosmology','Vengeful Tracker cross-plane representation — post-push cosmology','Marked Fugitive Oracle Mystery ID mappings','Equipment/item profiles','Food/water versus bundled Supply numerical accounting','Crafting quality and wider procedures','Reputation label-to-ID/score migration','Remaining selectable Wizard-cantrip effects','Live companion/runtime parity','Human balance','Full game and final joint flow/GitHub delivery'],
      'files':[]}
    # Complete source reference is evidence rather than a conflicting second operational guide.
    source_doc=ROOT/'docs/mechanics/ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md'
    original=source_doc.read_text(encoding='utf-8')
    original=original.replace('The notebook review and authored integration rules must resolve conflicts before these become active playtest rules.','The [reviewed integration guide](ANCESTRY_BACKGROUND_PLAYTEST.md) owns operational clarifications and overrides; this reference preserves the original paragraphs, including superseded wording, for comparison.')
    source_doc.write_text(original,encoding='utf-8')
    for p in [guide,ROOT/'docs/mechanics/ANCESTRY_SPELL_SUPPLEMENT_PLAYTEST.md',source_doc,data_path,grants_path,ROOT/'data/playtest/ancestry_spell_supplement_candidate.json',ROOT/'data/public/ancestry_playtests/spells.json',ROOT/'data/playtest/spell_drafts/batch_ancestry_dependencies.json']:
        status['files'].append({'path':str(p.relative_to(GAME)).replace('\\','/'),'sha256':sha(p)})
    dump(ROOT/'docs/mechanics/ANCESTRY_BACKGROUND_REVIEW_STATUS.json',status)
    for name in ['ANCESTRY_BACKGROUND_PLAYTEST.md','ANCESTRY_SPELL_SUPPLEMENT_PLAYTEST.md','ANCESTRY_BACKGROUND_SOURCE_BINDINGS.md']:
        p=ROOT/'docs/mechanics'/name
        links=re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8'))
        check(name+' local links resolve',all(link.startswith('http') or (p.parent/link.split('#')[0]).exists() for link in links))
    assert all(c['pass'] for c in checks),[c for c in checks if not c['pass']]
    dump(AUDIT/'ANCESTRY_BACKGROUND_PROMOTION_CHECK.json',{'status':'PASS','checks':len(checks),'protectedUnchanged':160,'expectedCatalogIntegrationChanges':expected,'results':checks})
    sub=read(AUDIT/'ANCESTRY_BACKGROUND_EXACT_SUBMISSION.json');sub.update(status='review-complete-four-repairs-applied-and-promoted',responseTurnId=status['exactReviewTurn'],responseEvidence='GPT_ANCESTRY_BACKGROUND_EXACT_REVIEW_BROWSER.txt');dump(AUDIT/'ANCESTRY_BACKGROUND_EXACT_SUBMISSION.json',sub)
    (AUDIT/'GPT_ANCESTRY_BACKGROUND_EXACT_REVIEW.md').write_text('''# Exact ancestry/background manuscript review

Calibration Review turn `79ec4add-1487-489c-8b33-e464c4bd8baa` approves both complete manuscripts and their source projections after four repairs. The full visible reply is preserved in [GPT_ANCESTRY_BACKGROUND_EXACT_REVIEW_BROWSER.txt](GPT_ANCESTRY_BACKGROUND_EXACT_REVIEW_BROWSER.txt). All repairs are applied; see [exact artifact hashes and boundaries](../../../../DescentReviewChanges/ReviewBible/docs/mechanics/ANCESTRY_BACKGROUND_REVIEW_STATUS.json).

Seven existing ordinary spell identities are promoted; ten new ancestry-grant-only procedures remain separate and grant no ordinary class access. The original catalog, prior approved effects, books, class rules and companion sources remain preserved. This review is not full-game, runtime, balance or GitHub approval. Cosmology remains post-push only.
''',encoding='utf-8')
    print(f'PASS {len(checks)} promotion checks;160 frozen files and269 prior spell records unchanged; review recorded.')

if __name__=='__main__':main()
