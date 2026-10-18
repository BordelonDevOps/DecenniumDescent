"""One-shot current delivery labels; original checkpoints and prepared packets stay sealed."""
import json
import subprocess
import sys
from datetime import datetime, timezone
from apply_di7_ap_as_01 import G, R, A, info, encoded


def main():
    keep = A/'navigation-before-part5-labels-31a'
    delta = A/'GPT_PART5_LABELS_31A_NAVIGATION_DELTA.json'
    report = A/'GPT_PART5_LABELS_31A_CHECK.json'
    assert not any(p.exists() for p in [keep,delta,report])
    start,guide,builder = G/'START_HERE.md',R/'docs/DEVELOPMENT_DIRECTION.md',R/'tools/build_review_map.py'
    mapfile,buildfile = G/'REVIEW_MAP.html',A/'REVIEW_MAP_BUILD.json'
    files = [start,guide,builder,mapfile,buildfile]
    before = {p:p.read_bytes() for p in files}
    index = info(R/'data/public/spell_playtests/authored_review_index.json')
    queue = info(R/'data/director/spell_review/remaining_work_queue_24.json')
    edits = {}
    for p in [start,guide]:
        parts = before[p].decode('utf8').split('\n\n')
        for n,s in enumerate(parts):
            if s.startswith('**Rank-seven identity and casting sources:**'):
                assert s.count('this packet is UNSENT.') == 1
                parts[n] = s.replace('this packet is UNSENT.','this complete packet was delivered inside handoff03 for awareness; its semantic conference remains pending.')
            elif s.startswith('**Rank-eight damage and interaction sources:**'):
                parts[n] = s+' This complete packet was delivered inside handoff03 for awareness; its semantic conference remains pending.'
        edits[p] = '\n\n'.join(parts)
    code = before[builder].decode('utf8')
    for old,new in [
        ('Latest prepared continuation context02 — UNSENT','Historical prepared continuation context02 — superseded by delivered03'),
        ('Rank7 identity/casting5 —24 questions,5C, UNSENT','Rank7 identity/casting5 — delivered for awareness; conference pending'),
        ('Rank8 damage6 —20 questions,4B/2C, UNSENT','Rank8 damage6 — delivered for awareness; conference pending')]:
        assert code.count(old) == 1, old
        code = code.replace(old,new)
    tail = ' + read(A / "GPT_PART5_REVIEW_31_NAVIGATION_DELTA.json")["changes"]\n'
    assert code.count(tail) == 1
    code = code.replace(tail,tail.rstrip('\n')+' + read(A / "GPT_PART5_LABELS_31A_NAVIGATION_DELTA.json")["changes"]\n')
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
    for p,txt in edits.items():p.write_text(txt,encoding='utf8',newline='\n')
    changes = [{'before':next({**s['source'],'preservedCopy':s['preservedCopy']['path']} for s in preserved if s['source']['path'] == p.relative_to(G).as_posix()),'after':info(p)} for p in edits]
    delta.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'changes':changes,'basis':info(A/'GPT_CONTINUATION_05_ACTUAL_START_01.json'),'sourceInformationDeleted':0,'newRuleAdoptions':0}))
    run = subprocess.run([sys.executable,'-X','utf8',str(builder)],capture_output=True,text=True,encoding='utf8')
    assert run.returncode == 0,run.stderr
    built = json.loads(buildfile.read_bytes())
    assert not built['missingLinks']
    assert index == info(G/index['path']) and queue == info(G/queue['path'])
    result = {'delta':info(delta),'preservation':info(keep/'PRESERVATION_MANIFEST.json'),'map':info(mapfile),'build':info(buildfile),'existingDistinctLinks':built['existingDistinctLinks'],'missingLinks':[],'indexUnchanged':index,'queueUnchanged':queue,'sourceInformationDeleted':0,'newRuleAdoptions':0,'scope':'Clarify actual delivery for awareness versus pending formal semantic conference; frozen historical UNSENT labels retained.'}
    report.write_bytes(encoded(result))
    print(json.dumps({'receipt':info(report),'existingLinks':built['existingDistinctLinks'],'failures':0}))


if __name__ == '__main__':main()
