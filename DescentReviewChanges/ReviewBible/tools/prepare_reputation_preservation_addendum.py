"""Preserve actual reputation helper/source evidence for the existing FL-23 question."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(raw):return sha256(raw).hexdigest()
def record(p):return {'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def save(p,x):p.write_text(x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    target=A/'REPUTATION_PRESERVATION_SOURCE_ADDENDUM.json'
    assert not target.exists()
    probes=read(A/'REPUTATION_PRESERVATION_RUNTIME_PROBES.json')
    assert probes['probeCount']==12 and all(p['currentBehaviorReproduced'] for p in probes['probes'])
    selected=list(probes['sourceFiles'])+['docs/reference/Player_Rulebook_v6_source_text.txt','docs/audit/2026-10-08/full-game/EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json','DescentReviewChanges/ReviewBible/docs/mechanics/ANCESTRY_BACKGROUND_REVIEW_STATUS.json']
    files={s:record(G/s) for s in selected}
    for s,e in probes['sourceFiles'].items():assert files[s]==e,s
    excerpts=[]
    def lines(rel,start,end,label):
        original=(G/rel).read_text(encoding='utf-8-sig').splitlines()
        assert 1<=start<=end<=len(original)
        excerpts.append({'id':label,'file':rel,'oneBasedStart':start,'oneBasedEnd':end,'exactLines':original[start-1:end]})
    def between(rel,begin,end,label):
        original=(G/rel).read_text(encoding='utf-8-sig').splitlines()
        i=next(i for i,s in enumerate(original) if s==begin)
        j=next(j for j,s in enumerate(original) if j>i and s==end)
        lines(rel,i+1,j,label)
    loop='DescentReviewChanges/ReviewBible/docs/mechanics/GAMEPLAY_LOOP_CANON.md'
    between(loop,'## 18. Reputation and renown','## 19. Advancement rewards','RP-S01')
    guide='DescentReviewChanges/ReviewBible/docs/mechanics/REPUTATION.md'
    lines(guide,1,len((G/guide).read_text(encoding='utf-8').splitlines()),'RP-S02')
    player='docs/reference/Player_Rulebook_v6_source_text.txt'
    between(player,'Reputation in Aethel','The 12-Person Expedition Limit','RP-S03') if 'The 12-Person Expedition Limit' in (G/player).read_text(encoding='utf-8').splitlines() else lines(player,5509,5515,'RP-S03')
    storage='DescentReviewChanges/ReviewBible/src/lib/character-storage.js'
    lines(storage,1,100,'RP-S04')
    builder='DescentReviewChanges/ReviewBible/src/components/CharacterBuilder.tsx'
    lines(builder,1194,1220,'RP-S05')
    questions=[
        {'id':'RP-A01','parent':'FL-23','subject':'Numeric scale, qualitative bands and unchanged source values','question':'Resolve the existing -5..+5 versus -3..+3 question once in FL-23. Define explicit named source/version mappings; do not rewrite historical +5 to +3 merely by loading it. Preserve original values and evidence even if an active display uses another reviewed scale. Does the -2 Hated/+2 Honored runtime band match the selected procedure?','probes':['RP-P02','RP-P11']},
        {'id':'RP-A02','parent':'FL-23','subject':'Unknown faction keys and malformed values','question':'Define a lossless authoritative record plus any derived playable view. Current normalization drops unknown keys and coerces malformed values to0; setters temporarily admit keys that disappear on the next normalize. Preserve unsupported IDs, explicit zero, absence and original invalid values for repair; unknown data must not grant playable standing. Specify a versioned migration, export/import and roundtrip contract before changing any save.','probes':['RP-P01','RP-P03','RP-P04','RP-P06','RP-P07','RP-P08','RP-P09','RP-P12']},
        {'id':'RP-A03','parent':'FL-23','subject':'Background initialization versus later character history','question':'Current applyBackgroundReputation overwrites background keys and discards unknown keys each time the builder applies it. Specify fresh-character initial grants, already-initialized characters, a changed background and corrections without erasing later earned standing or applying a grant twice. Retain original background and change provenance; do not assume that selecting the same label is a new event.','probes':['RP-P05','RP-P12']},
        {'id':'RP-A04','parent':'FL-23','subject':'Numeric authority, tier labels and neutral visibility','question':'Current scoreFromTierLabel(tierLabel(3)) returns2. Keep descriptive tiers separate from the authoritative numeric/history record. Decide the display for absent, explicitly recorded0, hidden or unresolved standing without converting those records into one save value. A compact list may omit neutral display entries only while preserving the underlying original record.','probes':['RP-P09','RP-P10','RP-P11']},
        {'id':'RP-A05','parent':'FL-23','subject':'Stable institution identifiers and literal source preservation','question':'The actual module has44 definitions, including9 draft flags,4 resonanceTrack flags and20 background maps. Preserve every current key and label as evidence; do not merge similar institution categories, infer allies/enemies, or treat a draft flag as completed faction design. Set a source-backed process for campaign-specific keys and future aliases. Faith/planar/prophecy/resonance-track descriptions are receipts only here: their cosmological meaning or powers remain deferred until after the verified push.','probes':['RP-P01','RP-P06','RP-P07']},
        {'id':'RP-A06','parent':'FL-23','subject':'Change events, scene caps and record provenance','question':'Bind any settled numeric standing change to the actual faction, event, actors/witnesses and scene, retaining the Loop normal1/major2/per-scene2 statements as disputed source until FL-23 settles them. Distinguish faction standing, one NPC attitude, Expedition renown, licenses and explicit priced privileges. Do not derive universal magical discounts or invent a political relationship from matching category names. Define reversible event records before companion automation.','probes':[]},
    ]
    # Derive source facts, rather than placing unverified counts into the register.
    factions=probes['fullOriginalFactionRecords']
    draft_count=sum(f.get('draft') is True for f in factions)
    track_count=sum(f.get('resonanceTrack') is True for f in factions)
    questions[4]['question']=questions[4]['question'].replace('including9 draft flags,4 resonanceTrack flags',f'including{draft_count} draft flags,{track_count} resonanceTrack flags')
    fl=next(r for r in read(A/'EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json')['decisionCases'] if r['id']=='FL-23')
    submission=read(A/'TEACHING_NAVIGATION_EXACT_V1_PREPARATION.json')
    unchanged=[]
    for rel,e in submission['manifest'].items():
        if rel=='README_TEACHING_EXACT_V1.md':continue
        assert record(G/rel)==e,rel
        unchanged.append(rel)
    obj={'status':'prepared-unsent-addendum-to-existing-FL-23','preparedAtUtc':datetime.now(timezone.utc).isoformat(),'scope':'Data preservation and institutional standing interfaces only; no new faction, reputation rule, migration or cosmology interpretation is applied. These six subquestions refine FL-23 instead of opening duplicate conflicting scale decisions.','parentQuestion':fl,'questions':questions,'fullSourceFiles':files,'exactSourceExcerpts':excerpts,'runtimeProbeReport':{'path':'docs/audit/2026-10-08/full-game/REPUTATION_PRESERVATION_RUNTIME_PROBES.json',**record(A/'REPUTATION_PRESERVATION_RUNTIME_PROBES.json')},'originalDefinitions':{'factions':44,'backgroundMaps':20,'draftFlags':draft_count,'deferredResonanceTrackFlags':track_count},'activeTeachingSubmittedDiskPayloadsUnchanged':len(unchanged),'activeTeachingArchiveUnchanged':record(Path(submission['archive']))=={'bytes':submission['bytes'],'sha256':submission['sha256']},'sourceFilesModified':0,'savedCharactersRead':0,'savedCharactersWritten':0,'submittedToGPT':False,'cosmologyReviewed':False}
    save(target,obj)
    text=['# Reputation preservation — source addendum to FL-23','','**Prepared, unsent.** Six precise subquestions extend the existing expedition reputation conference. No score scale, faction meaning or save migration is adopted. The active teaching review remains unchanged.','','[Complete evidence register](REPUTATION_PRESERVATION_SOURCE_ADDENDUM.json) · [12 actual helper probes](REPUTATION_PRESERVATION_RUNTIME_PROBES.json)','','The existing JavaScript helpers were imported locally and called only with synthetic in-memory records. They drop unknown faction keys, clamp out-of-range values, coerce malformed scores to zero, and overwrite background keys when background initialization is reapplied. Tier labels cannot preserve every numeric score. These are observed implementation behaviors, not approved rules or proof that a real character lost data. No browser saves or actual character files were accessed.','','The storage adapter calls that normalization during load/export/upsert; the character builder calls background application from its background control. Full files and exact excerpts are retained. Source preservation requires deciding an explicit migration and initialization contract before changing stored data.','','| Question | Subject |','|---|---|']
    for q in questions:text.append(f"| {q['id']} | {q['subject']} |")
    text += ['','The44 original definitions and20 background maps are preserved in full as internal source evidence. Literal descriptions involving faith, planes, prophecy or resonance tracks are not interpreted in this addendum. Their meaning and powers remain deferred to the careful post-push cosmology review.','','Confer on these questions with FL-23 after the current teaching review. Carry fulfilled ancestry/background, LAX/NWX/LRX and recipe scopes; preserve every old source and every current payload. No information has been deleted.','']
    save(A/'REPUTATION_PRESERVATION_SOURCE_ADDENDUM.md','\n'.join(text))
    print(json.dumps({'subquestions':len(questions),'actualHelperProbes':12,'factions':44,'backgroundMaps':20,'draftFlags':draft_count,'unchangedTeachingDiskPayloads':len(unchanged),'sourceFilesModified':0}))
if __name__=='__main__':main()
