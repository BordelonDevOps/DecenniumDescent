"""Clarify current versus historical review labels without changing sealed evidence."""
import json
import subprocess
import sys
from datetime import datetime, timezone
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    keep = A/'navigation-before-part5-labels-33a'
    delta = A/'GPT_PART5_LABELS_33A_NAVIGATION_DELTA.json'
    report = A/'GPT_PART5_LABELS_33A_CHECK.json'
    assert not any(p.exists() for p in [keep,delta,report])
    start,guide,builder = G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',R/'tools/build_review_map.py'
    mapfile,buildfile = G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json'
    before = {p:p.read_bytes() for p in [start,guide,builder,mapfile,buildfile]}
    index = info(R/'data/public/spell_playtests/authored_review_index.json')
    queue = info(R/'data/director/spell_review/remaining_work_queue_26.json')
    edits = {}
    for p in [start,guide]:
        parts = before[p].decode('utf8').split('\n\n')
        matched = 0
        for n,s in enumerate(parts):
            if s.startswith('**Companion/life10 exact draft ready:**'):
                matched += 1
                assert 'It is UNSENT and unadopted.' in s and 'both remain UNSENT.' in s
                s = s.replace('**Companion/life10 exact draft ready:**','**Companion/life10 actual exact review:**').replace('It is UNSENT and unadopted.','It was delivered in Part5 with the expanded evidence; exact review is active and authored application remains pending.').replace('Send the [separate complete evidence supplement]','The [separate complete evidence supplement]').replace('with Exact05; both remain UNSENT.','was delivered with Exact05; both full archives are in the actual review.')
                parts[n] = s
            elif s.startswith('**Remaining spell work:**'):
                parts[n] = s.replace('accompanies the unchanged Control15/Illusion14 full packets','was supplied for Control15/Illusion14 review; the actual Illusion return and Current13 now supersede its earlier pending label')
            elif s.startswith('**Rank-seven perception and control sources:**'):
                parts[n] = s.replace('pending Illusion14/Control15/terrain/Project Image proposals supply no new authority.','frozen Illusion14/Control15/terrain/Project Image comparisons supply no new authority. Illusion14 has since received scoped semantic acceptance, but its exact canonical integration is still pending; no rank-seven card inherits approval.')
        assert matched == 1
        edits[p] = '\n\n'.join(parts).replace('the latest observation was 38% remaining','the latest observation was 37% remaining')
    code = before[builder].decode('utf8')
    replacements = [
        ('Command Undeath — historical/current workbook conflict, UNSENT','Command Undeath — full evidence delivered; exactCR2 holds remain'),
        ('Companion10 exact05 — complete eight files, two content holds, UNSENT','Companion10 exact05 — actual Part5 review active; two content holds'),
        ('Illusion14 Current12 — actual full submission with current acceptance context','Illusion14 Current12 submission history — superseded by actual Part5 return'),
        ('Companion Current04 — full actual conference active','Companion Current04 conference history — returned; nine repairs replayed'),
        ('Companion/life10 Current04 —27 authored cases,5 questions,UNSENT','Companion/life10 Current04 preparation history — superseded by Exact05'),
        ('Illusion14 conference12 — prepared unsent','Illusion14 conference12 preparation history — delivered and returned'),
        ('Latest allowance38percentremaining','Latest allowance37percentremaining'),
    ]
    for old,new in replacements:
        assert code.count(old) == 1,old
        code = code.replace(old,new)
    tail = ' + read(A / "PART5_PROGRESS_33_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail) == 1
    code = code.replace(tail,tail.rstrip('\n')+' + read(A / "GPT_PART5_LABELS_33A_NAVIGATION_DELTA.json")["changes"]\n')
    compile(code,str(builder),'exec')
    edits[builder] = code
    preserved = []
    for p,raw in before.items():
        dest = keep/p.relative_to(G)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(raw)
        assert dest.read_bytes() == raw
        preserved.append({'source':info(p),'preservedCopy':info(dest)})
    (keep/'PRESERVATION_MANIFEST.json').write_bytes(encoded(preserved))
    for p,txt in edits.items():
        p.write_text(txt,encoding='utf8',newline='\n')
    changes = [{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in preserved if s['source']['path'] == p.relative_to(G).as_posix()),'after':info(p)} for p in edits]
    delta.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'changes':changes,'actualIllusionBasis':info(A/'ILLUSION_PERCEPTION_14_PART5_RETURN_01_RECEIPT.json'),'actualCompanionBasis':info(A/'COMPANION_LIFE_10_EXACT05_PART5_SUBMISSION_01.json'),'sourceInformationDeleted':0,'newRuleAdoptions':0}))
    run = subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8')
    assert run.returncode == 0,run.stderr
    built = json.loads(buildfile.read_bytes())
    assert not built['missingLinks'] and index == info(G/index['path']) and queue == info(G/queue['path'])
    result = {'delta':info(delta),'preservation':info(keep/'PRESERVATION_MANIFEST.json'),'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':built['existingDistinctLinks'],'missingLinks':[],'indexUnchanged':index,'queueUnchanged':queue,'sourceInformationDeleted':0,'newRuleAdoptions':0,'scope':'Current navigation distinguishes actual deliveries and semantic return from historical prepared/active labels. Frozen original packets/checkpoints stay unchanged. Latest allowance37percentremaining.'}
    report.write_bytes(encoded(result))
    print(json.dumps({'receipt':info(report),'existingLinks':built['existingDistinctLinks'],'failures':0}))


if __name__ == '__main__':
    main()
