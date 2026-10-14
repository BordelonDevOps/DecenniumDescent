"""Promote only the exact-reviewed seven existing IDs and separate ten-spell supplement."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT.parents[1]/'docs/audit/2026-10-08/full-game'

def dump(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    reply=(AUDIT/'GPT_ANCESTRY_BACKGROUND_EXACT_REVIEW_BROWSER.txt').read_text(encoding='utf-8')
    assert 'APPROVE WITH FOUR REPAIRS' in reply and 'Existing seven — APPROVED for operational promotion' in reply
    guide=(ROOT/'docs/mechanics/ANCESTRY_BACKGROUND_PLAYTEST.md').read_text(encoding='utf-8')
    assert 'the Symbiotic Mycelian who owns this trait may use its Reaction' in guide
    assert 'Regeneration can have at most one pending acid/fire suppression.' in guide
    assert 'touch a distinct willing legal creature' in guide and 'distinct willing legal living recipient' not in guide
    data=json.loads((ROOT/'data/playtest/ancestry_spell_supplement_candidate.json').read_text(encoding='utf-8'))
    existing=[s for s in data['spells'] if s['identityType']=='existing-catalog']
    additions=[s for s in data['spells'] if s['identityType']=='new-ancestry-grant-only']
    assert len(existing)==7 and len(additions)==10
    for s in existing:
        assert ('Water Breathing lifetime' not in s['designNotes'])
        assert ('24-elapsed-hour' in s['designNotes'])==(s['id']=='water-breathing')
    status='REVIEWED authored operational PLAYTEST manuscript; four exact-review repairs applied; runtime and human balance pending'
    for s in data['spells']:s['reviewStatus']=status
    data['status']=status
    dump(ROOT/'data/playtest/ancestry_spell_supplement_candidate.json',data)
    for s in existing:s['implementationStatus']=status
    dump(ROOT/'data/playtest/spell_drafts/batch_ancestry_dependencies.json',{'status':status,'scope':'Seven existing ordinary identities only; new ancestry-only spell names are in a separate supplement.','spells':existing})
    selected_path=ROOT/'data/playtest/spell_drafts/selected_sources.json'
    backup=AUDIT/'SELECTED_SPELL_SOURCES_BEFORE_ANCESTRY.json'
    if not backup.exists():backup.write_bytes(selected_path.read_bytes())
    selected=json.loads(selected_path.read_text(encoding='utf-8'))
    selected['ancestry_dependency_completion']=[s['id'] for s in existing]
    dump(selected_path,selected)
    for s in additions:
        assert not s['ordinaryClassAccess'] and not s['sourceCoreEntries']
    dump(ROOT/'data/public/ancestry_playtests/spells.json',{'status':status,'scope':'Ten named ancestry-grant-only spell procedures; no ordinary class access, no claim these had original Core blocks.','spells':additions})
    validator=ROOT/'tools/validate_spell_playtests.py'
    backup=AUDIT/'VALIDATE_SPELL_PLAYTESTS_BEFORE_ANCESTRY.py'
    if not backup.exists():backup.write_bytes(validator.read_bytes())
    text=validator.read_text(encoding='utf-8')
    text=text.replace('All269 individually reviewed selected IDs','All276 individually reviewed selected IDs').replace('len(set(selected))==269','len(set(selected))==276')
    text=text.replace('Remaining579 explicitly blocked','Remaining572 explicitly blocked').replace("s['operational'] is None for s in spells.values())==579","s['operational'] is None for s in spells.values())==572")
    validator.write_text(text,encoding='utf-8')
    print('Promoted approved seven draft records and separate ten-spell ancestry supplement; catalog rebuild/validation still required.')

if __name__=='__main__':main()
