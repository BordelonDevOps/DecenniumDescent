"""Find explicit geometry in active queued cases; do not rewrite historical data."""
from datetime import datetime, timezone
import json, re
from apply_di7_ap_as_01 import G, R, A, info, encoded

SPECS = [
 ('spell_proposals/damage_control_25_current_08.json',['currentCases','currentDigitalVectors','mixedDefenseOptionVectors04','highRankCurrentVectors05','namedLifecycleSupplement06','currentConferenceWorkedSupplements08']),
 ('spell_proposals/persistent_damage_20_current_06.json',['currentExamples','currentSupplementalExamples','adversarialVectors04']),
 ('spell_proposals/illusion_perception_14_current_11.json',['currentExamples','supplementalVectors09']),
 ('spell_proposals/control_15_current_11.json',['currentExamples']),
 ('spell_review/memory_2_conference_01.json',['conditionalConferenceVectors']),
 ('spell_review/creation_conference_01.json',['conditionalConferenceVectors']),
 ('spell_review/material_terrain_8_conference_01.json',['conditionalConferenceVectors'])]


def main():
    out=A/'CURRENT_OCCUPIED_SPACE_AUDIT_01.json'
    assert not out.exists()
    results=[]
    for filename, groups in SPECS:
        path=R/'data/director'/filename
        doc=json.loads(path.read_bytes())
        hits=[]
        def walk(x,p,case_id):
            if isinstance(x,dict):
                case_id=x.get('id',x.get('caseId',case_id))
                for k,v in x.items():
                    q=p+'/'+k.replace('~','~0').replace('/','~1')
                    if isinstance(v,list) and len(v)==3 and all(isinstance(a,(int,float)) for a in v) and 'half' in k.lower():
                        hits.append({'pointer':q,'caseId':case_id,'kind':'EXPLICIT_HALF_EXTENTS','value':v,'horizontalBelowSmallMediumDefault':min(v[:2])<2.5,'disposition':'Needs actual actor/shape/source classification; do not automatically replace.'})
                    if isinstance(v,str) and re.search(r'half.?extent|2\s*[x×]\s*2|two.foot.*(?:bod|occup)|bod(?:y|ies).*(?:\[\s*1\s*,\s*1\s*,\s*1\s*\])',v,re.I):
                        hits.append({'pointer':q,'caseId':case_id,'kind':'TEXTUAL_GEOMETRY','value':v,'disposition':'Inspect exact declared body/occupied-space and downstream consequences.'})
                    walk(v,q,case_id)
            elif isinstance(x,list):
                for i,v in enumerate(x):walk(v,p+'/'+str(i),case_id)
        for group in groups:
            assert group in doc, (filename,group)
            walk(doc[group],'/'+group,None)
        results.append({'source':info(path),'activeGroupsInspected':groups,'hits':hits,'hitCount':len(hits)})
    data={'id':'CURRENT-OCCUPIED-SPACE-AUDIT-01','recordedAtUtc':datetime.now(timezone.utc).isoformat(),
          'trigger':info(A/'PERSISTENT_DAMAGE_20_CONFERENCE_06_ACTUAL_GPT_FINAL.json'),
          'acceptedAuthority':info(R/'docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md'),
          'scope':'Read-only search of active queued-case groups only. No global text replacement; every hit needs actual actor/source classification. Historical/source objects remain untouched. Small/Medium5x5, Tiny2.5x2.5, Large10x10 require actual applicable size/anatomy and measured height.',
          'results':results,'totalHits':sum(r['hitCount'] for r in results),'correctionsApplied':0,'runtimeTestsExecuted':0,
          'requiredChecks':['Current actual occupied body footprint and measured height','Caster/target/area range and line of effect','Source shape/body intersections','Close-quarters and other attack/save conditions','Whole-path and final collisions/support','Actual fall/movement/clock consequences','Historical ID/text preservation and exact new-version delta']}
    out.write_bytes(encoded(data))
    print(json.dumps({'report':info(out),'totalHits':data['totalHits'],'byFile':[{'source':r['source']['path'],'hits':r['hitCount'],'caseIds':sorted({str(h['caseId']) for h in r['hits']})} for r in results]}))


if __name__=='__main__':main()
