"""Preserve the first internal draft and apply the exact ADV-EDIT-01 correction."""
from pathlib import Path
from datetime import datetime, timezone
import json
import re
import shutil
from build_advanced_craft_internal_candidates import read, dump, sha, render_card

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
PRIMARY='Original trigger frame and original working striker/discharge block are primary and must survive in recoverable form for magical reconstruction; the captive spring/actuation member, separate subordinate contacts, supports, catches, grip covers, fittings and feet are replaceable only with actual compatible stock through the applicable restoration procedure.'
MODEL='Steel trigger frame, replaceable captive spring/actuation member, and original working striker/discharge block; no loose expendable ammunition.'
RULE='The original 3-lb trigger frame and original 2-lb working striker/discharge block are primary and must survive in recoverable form. The 2-lb captive spring/actuation member and separate subordinate contacts, supports, catches, grip covers, fittings and feet may be replaced with actual compatible stock through the applicable restoration procedure. Contacts do not replace the primary discharge block. Preserve the same trap identity, original primaries, 12 × 12 × 3-inch envelope, 8-lb empty mass and 3/2/2/1-lb allocation. A missing/nonfunctional spring prevents discharge until repair is complete. Positive-HP repair uses DC10, max(1 hour, recorded maximumHP/10 hours) and 2.50 gp material reference; HP0 uses the original recipe DC, max(8 hours, maximumHP/10 hours) and 25% of the existing finished-unit reference. Actual trained Tinker\'s tools, INT, station, implements, compatible stock and completed work remain necessary. No spring replacement refills charges, services the trap, resets arming/command/offense/custody history, removes flaws or reverses terminal dismantling. Original-actuator requirements for automaton chassis and other bodies are unchanged.'


def main():
    backup=A/'advanced167-before-trap-spring-correction';assert not backup.exists()
    cap=read(A/'ADVANCED_TRAP_SPRING_FINAL_CAPTURE.json')
    turn=cap['turns'][0];reply=next(x for x in turn['items'] if x['type']=='agentMessage')
    verdict=A/'GPT_ADVANCED_TRAP_SPRING_CLARIFICATION.md'
    assert verdict.read_text(encoding='utf-8').rstrip('\n')==reply['text'] and reply['id']=='a01ad150-d04b-4fb8-ae18-9ea476535a93'
    assert PRIMARY in reply['text'] and MODEL in reply['text']
    dpath=R/'data/director/advanced_craft_recipe_candidate_internal.json';d=read(dpath)
    files=[dpath,R/d['sharedGuide'],R/d['bodyGuide'],A/'ADVANCED_CRAFT_INTERNAL_AUTHORING_STATUS.json',A/'ADVANCED_CRAFT_INTERNAL_CANDIDATE_VALIDATION.json',A/'ADVANCED_CRAFT_AUTHORING_PROGRESS.json',A/'ADVANCED_TRAP_SPRING_SUBMISSION.json',R/'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md']
    files += [R/f"docs/director-only/{t.upper().replace(' ','_')}_INTERNAL_RECIPE_CARDS.md" for t in ['Enchanting','Rune Carving','Scribing','Tinkering']]
    old=[]
    for p in files:
        dest=backup/p.relative_to(G);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
        old.append({'path':p.relative_to(G).as_posix(),'sha256':sha(p)})
    dump(backup/'MANIFEST.json',old)
    authority={'id':'ADV-EDIT-01','replyId':reply['id'],'turnId':turn['id'],'file':verdict.relative_to(G).as_posix(),'sha256':sha(verdict),'rule':RULE}
    d['controllingCorrections']=[authority];d['openExactReviewIssues']=[]
    d['resolvedEditorialIssues']=[{'id':'ADV-EDIT-01','status':'resolved by completed targeted GPT verdict; no exact promotion','historicalConflict':read(backup/dpath.relative_to(G))['openExactReviewIssues'][0]}]
    original_sentence='Ordinary supports, catches and grip covers can be replaced; the primary frame/spring/working mechanism must survive.'
    s=d['procedureSections']['B-04'];assert original_sentence in s['text']
    s['controllingText']=s['text'].replace(original_sentence,RULE);s['laterCorrection']='ADV-EDIT-01'
    ac=d['procedureSections']['AC-09'];ac['controllingText']=ac['text'].replace('missing frame/actuator','missing model-designated primary frame/actuator').replace('Replace only subordinate grips/covers/fasteners/contact inserts explicitly allowed.','Replace only subordinate members expressly permitted by the applicable body profile; for TI-trap, these include its captive spring/actuation member and separate subordinate contacts.');ac['laterCorrection']='ADV-EDIT-01'
    for bid,b in d['bodyModels'].items():
        if bid.startswith('TI-'):
            b['operationalBodyText']=s['controllingText'];b['controllingCorrections']=['ADV-EDIT-01']
    trap=d['bodyModels']['TI-trap'];trap['operationalPrimaryRule']=PRIMARY;trap['operationalModelDescription']=MODEL
    trap.pop('openExactReviewIssue',None)
    affected=[]
    for c in d['cards']:
        o=c['operational']
        for p in o['paragraphs']:
            if p['label']=='Restoration and reference prices':p['text']=p['text'].replace('missing frame/actuator','missing model-designated primary frame/actuator')
        if o['profile']=='TI-trap':
            affected.append(c['recipeId']);o['controllingCorrections']=['ADV-EDIT-01']
            for p in o['paragraphs']:
                if p['label']=='Complete output bodies':
                    p['text']=p['text'].replace(trap['sourceAuthoringProfile']['model'],MODEL)
            o['paragraphs'].insert(2,{'label':'Trap primary members and spring restoration','text':RULE})
        c['manuscriptText']=render_card(c)
    assert affected==['recipe-585','recipe-588','recipe-592','recipe-598','recipe-599','recipe-601','recipe-605','recipe-609','recipe-610','recipe-613','recipe-619']
    dump(dpath,d)
    for t in ['Enchanting','Rune Carving','Scribing','Tinkering']:
        cs=[c for c in d['cards'] if c['sourceRecipe']['skill']==t];p=R/f"docs/director-only/{t.upper().replace(' ','_')}_INTERNAL_RECIPE_CARDS.md"
        p.write_text(f'# {t} — internal recipe candidates\n\n**{len(cs)} candidates; public projection, state-sequence validation and exact review pending.** Original sources remain unchanged; ADV-EDIT-01 controls trap spring restoration.\n\n'+'\n'.join(c['manuscriptText'] for c in cs),encoding='utf-8')
    for p in [R/d['sharedGuide'],R/d['bodyGuide']]:
        text=p.read_text(encoding='utf-8');first,rest=text.split('\n',1)
        p.write_text(first+'\n\n**Controlling correction ADV-EDIT-01:** '+RULE+'\n\nThe older source quotations below remain preserved; this correction supersedes their trap-spring conflict and generic missing-actuator shorthand only.\n'+rest+'\n\n## Preserved completed correction\n\n'+verdict.read_text(encoding='utf-8'),encoding='utf-8')
    pg=R/'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md';text=pg.read_text(encoding='utf-8').replace('missing frames/actuators','missing model-designated primary frames/actuators')
    text=text.replace('**Traps:** place one', '**Trap restoration:** '+RULE+'\n\n**Traps:** place one')
    pg.write_text(text,encoding='utf-8')
    sub=read(A/'ADVANCED_TRAP_SPRING_SUBMISSION.json');sub.update(status='Completed targeted correction captured and applied to derived candidates; no promotion',replyId=reply['id'],verdictFile=verdict.name,verdictSha256=sha(verdict));dump(A/'ADVANCED_TRAP_SPRING_SUBMISSION.json',sub)
    status=read(A/'ADVANCED_CRAFT_INTERNAL_AUTHORING_STATUS.json');status['openExactReviewIssueIds']=[];status['controllingCorrections']=[authority]
    for path in status['outputHashes']:status['outputHashes'][path]=sha(G/path)
    dump(A/'ADVANCED_CRAFT_INTERNAL_AUTHORING_STATUS.json',status)
    progress=read(A/'ADVANCED_CRAFT_AUTHORING_PROGRESS.json');progress['resolvedEditorialIssues']=['ADV-EDIT-01'];progress['nextAction']='Complete public projection and meaningful state-sequence validation, then submit all167 actual candidates for exact review.';dump(A/'ADVANCED_CRAFT_AUTHORING_PROGRESS.json',progress)
    protected=read(A/'ADVANCED_CRAFT_JOINT_SUBMISSION.json')['currentFileHashes'];assert all(sha(G/p)==h for p,h in protected.items())
    receipt={'status':'Applied ADV-EDIT-01 beside preserved originals', 'appliedAtUtc':datetime.now(timezone.utc).isoformat(),'authority':authority,'affectedTrapCards':affected,'preservedPriorFiles':len(old),'protectedFilesUnchanged':len(protected),'candidateSha256':sha(dpath),'recipesApproved':0,'validationNeedsRefresh':True}
    dump(A/'ADVANCED_TRAP_SPRING_INTEGRATION.json',receipt);print(json.dumps(receipt,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
