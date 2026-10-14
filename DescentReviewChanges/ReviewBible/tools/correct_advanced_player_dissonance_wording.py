"""Correct the TD-08 transcription in the player adaptation; retain prior bytes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p, obj): p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    guide = R/'docs/mechanics/ADVANCED_CRAFT_CANDIDATE_GUIDE.md'
    public = R/'data/crafting/advanced_craft_recipe_candidate_public.json'
    status = A/'ADVANCED_CRAFT_PUBLIC_AUTHORING_STATUS.json'
    backup = A/'advanced167-before-player-dissonance-correction'
    assert not backup.exists(), 'Preserve existing correction; do not overwrite'
    internal = read(R/'data/director/advanced_craft_recipe_candidate_internal.json')
    source = internal['procedureSections']['TD-08']['text']
    old = 'Protected Dissonance routing uses the actual once-per-short-rest Bonus Action, up to two current qualifying active devices within30 feet.'
    new = 'Protected Dissonance routing uses the actual once-per-short-rest Bonus Action to route up to two current Dissonance into one qualifying active device of the routing Tinker within30 feet.'
    text = guide.read_text(encoding='utf-8')
    p = read(public)
    assert text.count(old) == 1 and p['operatingGuideText'] == text
    before = {}
    for file in [guide, public, status, A/'ADVANCED_CRAFT_PUBLIC_CANDIDATE_VALIDATION.json', A/'ADVANCED_CRAFT_WORKED_CASE_VALIDATION.json']:
        dest = backup/file.relative_to(G)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, dest)
        before[file.relative_to(G).as_posix()] = sha(file)
    text = text.replace(old, new)
    guide.write_text(text, encoding='utf-8')
    p['operatingGuideText'] = text
    dump(public, p)
    s = read(status)
    s['adaptationCorrection'] = {'id':'ADV-PLAYER-EDIT-02','sourceSection':'TD-08','reason':'Correct points versus targets transcription; one device receives up to two current Dissonance. No class-source change.'}
    for file in [guide, public]: s['outputHashes'][file.relative_to(G).as_posix()] = sha(file)
    dump(status, s)
    dump(A/'ADVANCED_CRAFT_PLAYER_DISSONANCE_CORRECTION.json', {
        'id':'ADV-PLAYER-EDIT-02','correctedAtUtc':datetime.now(timezone.utc).isoformat(),
        'sourceSection':'TD-08','completeSourceText':source,'oldText':old,'correctedText':new,
        'preservedPriorFiles':before,'backupDirectory':backup.relative_to(G).as_posix(),
        'currentPublicCandidateSha256':sha(public),'currentPlayerGuideSha256':sha(guide),
        'newMechanicalDecision':False,'newApprovals':0,'sourceFilesChanged':0})
    print(json.dumps({'status':'Corrected player wording to source TD-08','publicCandidateSha256':sha(public),'guideSha256':sha(guide)}))

if __name__ == '__main__': main()
