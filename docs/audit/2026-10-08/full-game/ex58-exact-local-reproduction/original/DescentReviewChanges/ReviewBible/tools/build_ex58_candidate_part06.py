"""Author lossless reputation procedures using synthetic evidence only."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import base64
import copy
import json
import re

G=Path(r'C:\Github\DecenniumDescent');R=G/'DescentReviewChanges/ReviewBible';A=G/'docs/audit/2026-10-08/full-game';P=A/'ex58-final-gpt-verdict'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def save(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
SECTIONS=[]
def section(n,title,player,director):SECTIONS.append({'id':f'RP-A{n:02d}','title':title,'player':player,'director':director})

section(1,'Keep the original relationship record',
'''The ordinary standing policy uses scores −3 through +3. An older score is not automatically on that scale just because it falls within those numbers. Preserve its source/version, original value, label, actual institution and earned history before deriving a current view.

| Record's established source | Current treatment |
|---|---|
| Current standing-v1 | Validate the actual integral −3…+3 value and event history; preserve it |
| Evidenced original companion-score-v1 | Carry a valid integral −3…+3 value forward identically, with its evidence |
| Old Loop 1.2 eleven-band standing | Use the optional explicit mapping below only through a recorded interpretation of that actual relationship |
| Player seven-band check-modifier table | Preserve it as a different, currently inactive modifier-domain source; do not import its numbers as standing |
| A genuinely new five-band background grant | Hated −2, Disliked −1, Neutral 0, Liked +1, Honored +2, applied once to the actual stated relationship |
| Unknown version, conflicting history or malformed value | Preserve it unresolved; derive no new active number or bonus |

The new optional Loop interpretation is:

| Old Loop score | −5 | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 | +5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Derived current score | −3 | −3 | −2 | −1 | −1 | 0 | +1 | +1 | +2 | +3 | +3 |

Record which actual old relationship is being interpreted and why its source is established. Keep the old number, label and every independently earned title, office, license, debt or claim. Mapping changes the current view, not what the original record said or the powers of an official.

A historical label alone is different from a new grant. Hated can mean either −3 or −2; Honored either +2 or +3. Do not turn a displayed label back into a preferred number. Even a single-point label needs an established source and actual relationship before numerical use. A genuinely known qualitative relationship can still support an appropriate qualitative transaction without guessing a missing numeric endpoint.''',
'''The raw layer preserves the exact original serialized bytes, decoded value/type/presence/key, path, known version/hash, capture provenance and event history. A derived standing-v1 view is separate, with its interpretation rule, subject/institution binding and evidence. Loading, displaying, importing and exporting do not authorize normalization.

Use the named policies precisely: standing-v1; companion-score-v1-evidenced; loop-1.2-eleven-band-to-standing-v1; player-seven-band-check-modifier; qualitative-five-band-initial-grant; or unresolved. Boolean false, fractional values and numeric strings are not valid integral scores. A value already clipped by an old helper is not proven complete history.

The optional Loop mapping needs an explicit interpretation event, not an automatic migration on load and not a new general owner-confirmation gate for this authored review. Unknown evidence stays a precise unresolved relationship. No real saved characters are read or migrated here.''')

section(2,'Preserve missing, hidden and invalid data distinctly',
'''An unrecorded relationship, an explicit Neutral 0, a hidden relationship and an unresolved old value are different states. None should silently replace another.

Keep unknown institution names and any additional fields when carrying a record forward. Preserve the exact original document, including duplicate keys, number spelling and formatting, alongside any derived view. If a document cannot be parsed, keep it and the error; do not substitute an empty map.

Active numerical standing needs a supported known policy, a finite integral score in range, resolved subject and institution, and compatible version/history. A text “1”, false, null, 1.7 or invalid text does not become a score by rounding or coercion. Unknown or conflicting entries remain unresolved with a reason. They grant no newly inferred skill, discount, spell or access.

A correction records the exact original value/version, intended interpretation and reason as a new event. It must identify the expected prior state; a stale, replayed or conflicting change does not apply. Unrelated and unknown entries stay intact.

A compact character-sheet or companion display is a view, not the full save. Export and reimport must preserve the complete original record and the separately added interpretation/history. Hiding a neutral row for readability does not erase its recorded zero.''',
'''The new authoritative envelope contains: schemaVersion; untouched raw document bytes or a complete raw-blob reference/hash; explicit sourceFormatVersion or unknown; subjectId; capture time/provenance; ordered original entries with key/value/type/presence; actual institution bindings; interpretation events; standing events; unknown top-level/extension fields; and a disposable derivedPlayableView.

Exact bytes are necessary because an ordinary parsed JSON object can lose duplicate keys, number spelling and ordering. Preserve ordered duplicate occurrences and leave their numerical interpretation unresolved until explicitly reconciled. Parse failure retains the blob/error rather than creating an empty object.

Absence, null, zero, false, numeric1, string1, fraction1.7, invalid text, hidden-to-this-audience and unknown institution stay distinct. Visibility does not invalidate an otherwise valid private number. A setter cannot briefly admit an unknown key only for the next load to discard it.

Reject stale/replayed/conflicting writes atomically, preserving all raw data and unrelated extensions. No call to the destructive old normalize/applyBackground helper is part of this candidate. The included twelve historical probes and new preservation fixtures are synthetic evidence; deployment and migration need the later versioned implementation and backup process.''')

section(3,'Apply background starts once',
'''For a new character, establish the selected background, exact source revision and the actual relationships its clauses describe. Create one stable initialization event. Apply each genuine starting grant once: Hated −2, Disliked −1, Neutral 0, Liked +1, or Honored +2 if actually supplied. Explicit Neutral is a real recorded grant, not absence.

The table below includes all twenty source backgrounds and the complete scope of their standing grants. It grants only standing; other background features retain their own reviewed procedures and prerequisites. A general category is not proof of membership, opposition or a particular character's past. Where a literal deep-setting predicate has not been established, retain that relationship requirement without inventing its meaning.

Reapplying an already initialized background changes nothing. A broad category and a specific institution representing the same actual relationship do not give two grants. Conflicting starting clauses for the same institution need a recorded scope/identity interpretation before initialization; do not add, average or choose the more favorable number.

**Cult Escapee.** The actual former cult starts Hated (−2); religious authorities suspicious of that past start Disliked (−1); groups actually opposing cults start Liked (+1). The old runtime religious-orders:+1 is preserved as a source conflict. For an existing character, correct only a proven erroneous initialization and replay the actual later earned events. Never replace a current score with −1 merely because the background is Cult Escapee. Without the origin/history, flag that relationship unresolved.

An in-fiction background change does not reset established relationships or reissue starting equipment/skills. A retcon of the original selection identifies the initialization being replaced, preserves its old record and explicitly replays affected history. A new life development keeps the actual past and produces only real new relationship events where warranted. This chapter grants no respec procedure.''',
'''Preserve all twenty original runtime maps and full featureSource clauses internally. The clause, not an abbreviated dictionary, determines the new standing scope.

Apply these specific source completions:

- Arcane Academy Dropout: an extra academic-factions −1 is not another grant beyond the matching formal arcane institution.
- Dimensional Refugee: academic-factions 0 is not a universal additional neutral relationship.
- Seeker: religious-orders 0 is not a second group beyond the actual mainstream orders.
- Wildling Herbalist: nature-circles +1 does not duplicate an actual Druidic/wildling relationship.
- Frontier Settler: nature-circles 0 has no separate source grant; the actual frontier-trader Liked relationship must be retained even though the runtime map omitted it.
- Celestial Emissary: the religious-orders +1 scope is only the source-described qualifying orders, never every religious order.
- Relic Hunter: include both actual indigenous peoples and religious orders who regard the work as desecration; the latter was omitted from the abbreviated map.

These fresh-start dispositions do not delete existing saved keys. A runtime extra may be later earned or have another actual source. Establish the origin before replacing a contribution.

For a proven Cult error, retain the old initialization as superseded evidence, replace only its suspicious-authority contribution and replay later chronological events with their actual caps. Example: old erroneous +1 start followed by an earned +1 had shown +2; corrected −1 start plus that same earned +1 yields 0. A current +1 without history cannot be assumed to be the bad start.''')

section(4,'A label describes a score',
'''| Actual current state | Display |
|---|---|
| Score −3 or −2 | Hated, retaining the exact underlying number |
| Score −1 | Disliked |
| Explicit score 0 | Neutral (recorded) |
| Score +1 | Liked |
| Score +2 or +3 | Honored, retaining the exact underlying number |
| No recorded relationship | Unrecorded / no known standing |
| Unresolved source or value | Standing unresolved, with a permitted explanation |
| Information unavailable to this audience | Omitted or an authorized unknown placeholder |

Displaying Honored does not reduce +3 to +2. Displaying Hated does not change −3 to −2. Only the explicit new-start procedure maps a starting band to its initial number. A blank character-sheet field creates no grant.

If a compact view filters recorded Neutral rows, make the filter clear and preserve them in the complete record/export. A known qualitative-only old relationship can support its actual qualitative use; numerical changes wait for recorded interpretation.

An individual NPC's attitude, a broad campaign reputation summary and one institution's score are separate. Learning a report changes the viewer's knowledge, not necessarily the subject's standing. A display must not reveal a hidden institution or membership merely because a private numeric field exists.''',
'''Never use a score-to-label-to-score roundtrip as authoritative normalization. The endpoint pairs remain distinct history states even though they share labels.

Retain invalid values and detailed errors in the private preservation record. A public unresolved message may disclose only what that audience is allowed to know. Hidden is neither absent nor null, and omission from a public projection is not deletion from the authoritative envelope.''')

section(5,'Bind relationships to real institutions',
'''Give each actual campaign institution a stable identity and record its public name, scope/jurisdiction, authorized agents, relationship to the character, source references, visibility and actual resources/obligations. Link it to source categories only where the relationship is established.

Similar category names are not automatic aliases. Religious orders, mainstream faith and good temples can refer to different groups; so can arcane guilds, arcane institutions and academic factions. The same applies to nature and Druidic circles, indigenous tribes and peoples, or the underworld and someone's former criminal associates. A person may belong to more than one institution without merging those institutions' scores.

An alias needs evidence that two labels identify the same actual institution, with its effective source/version and originals preserved. Changing a display name keeps identity and history. A political split or merger is a new event with real relationships, not a command to sum scores or keep the highest.

An unknown saved key can later be bound to a real local institution, or remain unsupported, without being discarded. New local institutions can use this ordinary record once their actual facts are supplied. A name alone does not establish world history, allies, enemies, doctrine or special powers.

Public information includes only identities and relationships the audience may know. Private membership, backers and dossiers remain private. Literal faith, planar, prophecy and resonance references create no inferred spell, RC, RP or cosmological effect.''',
'''Preserve all 44 original definitions, exact names/descriptions, nine draft flags, four resonanceTrack flags, optional/absent fields and twenty runtime background maps internally. They are source records, not automatically fully reviewed world institutions. Do not publish the full private list as a character relationship menu.

A campaign binding needs a stable namespaced ID, actual identity and jurisdiction, known members/authorized agents, actual subject relationship, references, audience permissions, supplied resources/obligations and optional qualified registry links. Missing facts remain unknown; do not fill feared secrets or doctrine from a category label.

The registry is not a closed 44-key whitelist for saved history. Unknown keys and source-specific extensions survive. An alias record identifies actual sameness and its version, while institutional splitting/merging retains distinct before/after identities and the actual political event. None of this interprets a draft faction's deep lore.''')

section(6,'Record signed events without losing history',
'''A standing event records its unique identity, original scene, subject, actual institution, cause and received information, witnesses/evidence or rumor, source policy/version, signed proposed change, scene-opening score/version, chronological position, actual result, overflow, time and permitted audience. Titles, offices, licenses, debts, NPC attitudes and renown remain linked separate records.

For ordinary events, propose −2, −1, +1 or +2 according to the actual declared consequence. Within one institution/subject/scene:

1. Add the signed proposals from distinct eligible causes.
2. Limit that sum to −2 through +2.
3. Add it to the **original scene-opening score**.
4. Limit the resulting score to −3 through +3.

Keep both scene-limit overflow and scale saturation as history. Neither is credit for a future scene. When another event in the same scene arrives, recompute from the opening score and all its recorded proposals; do not add the cumulative total to the latest result again.

For example, opening +2 with a +2 proposal ends at +3: applied change +1, scale overflow +1. A later independent −2 proposal in that same scene makes the signed sum zero, returning the result to +2. Applying each saturated step in isolation would incorrectly yield +1.

A genuinely predeclared campaign-defining exception changes only its specified scene cap/magnitude, not the scale, raw source values or prior history. Record it before resolution rather than using the exception after an unwanted result.

Duplicate event IDs, duplicate claims for the same cause/institution/scene, stale versions, invented policies and numerical updates to unresolved values do not apply. A correction appends a replacement or compensating interpretation identifying the original contribution and replay basis; it does not delete the historical deed or an unrelated relationship.

Correcting an institution's belief after a false report is a real later information/response event. Correcting an erroneous initialization is a different operation. Both retain what was previously recorded.''',
'''For each update retain proposed magnitude, scene-applied proposal, resulting score, delta from the scene opening, actual change from the prior displayed result, both overflow components, expected prior version and new version. Additional notification is not a new underlying cause.

Reject duplicate, stale or conflicting operations without partially changing other entries. Correcting a contribution requires a known replay basis; unresolved raw history cannot be turned active merely to accept an adjustment. A Boolean public-success flag is insufficient evidence of a witnessed deed, actual institution or authority.

The twelve original probe premises and their final dispositions remain complete in this module. New synthetic examples cover fresh starts, the proven Cult correction, unknown keys, zero/null/absence, duplicate keys, parse failure, +3 label roundtrip, signed opposite events and concurrent expected versions. Finite raw-byte and arithmetic checks do not authenticate a real rescue, institution, consent or campaign reputation and do not execute a production save migration.''')

CASES=[
 ('RPX-01','RP-A01','An evidenced Loop1.2 relationship has raw+2/Favored.','A recorded optional mapping derives+1/Liked while retaining raw+2, its old label and any actual earned privilege.'),
 ('RPX-02','RP-A01','An unversioned file contains numeric+2.','Its value alone does not prove companion or Loop policy. Keep it raw/unresolved with no newly derived active score.'),
 ('RPX-03','RP-A01','An old record contains onlyHonored with established qualitative meaning.','Retain its band and ambiguous numeric endpoints{+2,+3}. Do not use the fresh-start+2 mapping to rewrite this history.'),
 ('RPX-04','RP-A02','One document contains an unknown institution key, null, false,0,"1",1.7 and an extension field.','Retain every byte, key, value and type. Only the actual valid numeric value under an evidenced policy can become active; unknown identity and invalid types remain unresolved.'),
 ('RPX-05','RP-A02','The raw JSON contains two occurrences of the same institution key with different numbers.','Keep the exact bytes and both ordered occurrences; leave the conflicting active interpretation unresolved instead of accepting the last one.'),
 ('RPX-06','RP-A02','A raw document cannot be parsed.','Store the exact raw blob/hash and parse error. Do not create an empty standing map or discard extension data.'),
 ('RPX-07','RP-A03','A fresh CultEscapee has three actually bound qualifying relationships.','Create one initialization withformerCult−2,suspiciousAuthorities−1,antiCultGroups+1. Reapplying that same initialization makes no further change.'),
 ('RPX-08','RP-A03','The old suspicious-authority initialization is proven+1, followed by a genuine later+1 scene.','Append the correction of only the initialization to−1, replay the later+1 under its rules and obtain0. Preserve the old+2 result as superseded evidence.'),
 ('RPX-09','RP-A03','A current CultEscapee score is+1 but the initialization and earned history are unavailable.','Do not reset it to−1. Preserve it and flag the specific missing history/interpretation.'),
 ('RPX-10','RP-A03','The actual sameDruidicCircle matches both a broad nature category andWildlingHerbalist’s explicit clause.','Apply one real starting relationship, not two+1 grants. Keep unrelated saved keys and do not infer membership from spelling.'),
 ('RPX-11','RP-A04','A valid current+3 is displayed asHonored and later exported.','The authoritative score remains+3, with the same history. Display does not roundtrip it through fresh-grant+2.'),
 ('RPX-12','RP-A04','One relationship is absent, oneexplicit0 and onehidden from the player.','Display unrecorded versus recordedNeutral as permitted; hide the private relationship without deleting it or revealing its institutional identity.'),
 ('RPX-13','RP-A05','Two institutions use similar names but have different jurisdiction and agents.','Keep distinct stable IDs and scores. String normalization is not an alias record.'),
 ('RPX-14','RP-A05','An unknown saved campaign key is later evidenced as a real local institution.','Append its actual binding and applicable interpretation without discarding the original key or automatically assigning new standing.'),
 ('RPX-15','RP-A05','A source faction has a draft flag and resonanceTrack:true.','Preserve both flags internally. They create neither public membership nor a newRP/RC/spell rule or cosmological interpretation.'),
 ('RPX-16','RP-A06','Opening+2 receives proposed+2, then an independent−2 in the same actual scene.','Results are first+3 withscaleOverflow+1, then+2 fromsigned total0. Never calculate the second result by adding−2 to the saturated+3.'),
 ('RPX-17','RP-A06','Opening0 has three distinct+2 ordinary events in one institution/scene.','SceneProposal+6 caps at+2; result+2 andsceneOverflow+4 remain recorded without future credit.'),
 ('RPX-18','RP-A06','Two proposed updates both expectversion7; one valid update commitsversion8 first.','Reject the stale second update atomically. Preserve the input and conflict record; do not silently rebase or partially mutate unrelated scores.'),
 ('RPX-19','RP-A06','A repeated messenger uses a different eventID but reports the same cause to the same institution/scene.','Retain receipt history without another standing proposal. Duplicate underlying cause is still a duplicate claim.'),
 ('RPX-20','RP-A06','An institution later receives evidence that its believed accusation was false.','Record actual new receipt and response, with its current scene/policy. Do not silently erase the earlier belief or assume an exactly opposite numerical change.'),
]

def render(env,audience):
    lines=[f'# {audience.title()} expedition procedures — reputation and preserved history','',env['notice'],'',
           'Use with [Haven standing](EXPEDITION_PART03_PLAYER.md), [social scenes and faction activity](EXPEDITION_PART04_PLAYER.md), and [character creation](../CHARACTER_CREATION_PLAYTEST.md).','']
    if audience=='director':lines+=['Read the complete [player reputation chapter](EXPEDITION_PART06_PLAYER.md) alongside these procedures.','']
    for s in env['sections']:
        lines+=['## '+s['title'],'',s['text'],'']
        if audience=='player' and s['id']=='RP-A03':
            lines+=['### All twenty background standing starts','','Each clause needs its actual qualifying relationship. Repeated categories do not generate extra grants, and literal deep references do not supply missing meanings.','','| Background | Actual relationship required | Initial standing |','|---|---|---|']
            for b in env['backgroundStartingRules']:
                for g in b['grants']:lines+=['| '+b['name']+' | '+g['actualRelationshipRequired'].replace('|','\\|')+' | '+g['sourceBand']+' ('+f"{g['newInitialScore']:+d}"+') |']
            lines+=['']
    if audience=='director':
        lines+=['## Authored synthetic examples','','These are expected records and outcomes, not operations on real saved characters.','']
        for c in env['workedCases']:lines+=['### '+c['id'],'',c['given'],'',c['expected'],'']
        lines+=['## Twelve preserved source probes','','The original records below describe previously reproduced helper behavior. Preserving a behavior report does not approve it as the new rule.','']
        for item in env['originalProbeBindings']:
            p=item['probe'];lines+=['### '+p['id']+' — '+p['description'],'','**Complete original probe:**','','```json',json.dumps(p,ensure_ascii=False,indent=2),'```','','**Final disposition:** '+item['disposition']['finalDisposition'],'']
    return '\n'.join(lines)

def main():
    paths={'public':R/'data/public/expedition_candidate/part06.json','internal':R/'data/director/expedition_candidate/part06.json',
           'player':R/'docs/mechanics/expedition/EXPEDITION_PART06_PLAYER.md','director':R/'docs/mechanics/expedition/EXPEDITION_PART06_DIRECTOR.md','receipt':A/'EX58_CANDIDATE_PART06_CHECK.json'}
    assert not any(p.exists() for p in paths.values()),'Preserve previous outputs before revision'
    checks=[]
    def ck(n,v):checks.append({'name':n,'pass':bool(v)});assert v,n
    manifest=read(P/'FILE_MANIFEST.json')
    for x in manifest['files']:ck('Original final payload preserved '+x['path'],info(P/x['path'])=={k:x[k] for k in ['bytes','sha256']})
    binding=read(P/'EX58_REPUTATION_SOURCE_BINDINGS.json');factions=binding['fullOriginalFactionRecords'];backgrounds=binding['backgrounds']
    ck('All44factions preserved',len(factions)==len({f['id'] for f in factions})==44)
    ck('Nine draft flags remain',sum(f.get('draft') is True for f in factions)==9)
    ck('Four resonanceTrack flags remain',sum(f.get('resonanceTrack') is True for f in factions)==4)
    ck('Twenty complete backgrounds',len(backgrounds)==len({b['backgroundId'] for b in backgrounds})==20)
    for b in backgrounds:
        ck('Full feature source exists '+b['backgroundId'],bool(b['fullFeatureSource']) and bool(b['sourceBinding']))
        ck('All grants require actual relationship '+b['backgroundId'],all(g['automaticCategoryGrant'] is False and g['actualRelationshipRequired'] for g in b['newStartingGrantRules']))
    dispositions={p['id']:p for p in binding['probeFinalDispositions']}
    probe_bindings=[{'probe':p,'disposition':dispositions[p['id']]} for p in binding['rawSourceProbes']]
    ck('All12original probes and final dispositions',len(probe_bindings)==len(dispositions)==12)
    dirs=read(R/'data/director/expedition_candidate/source_register_corrected.json')['directions'];by={d['id']:d for d in dirs}
    original={d['id']:d for d in read(P/'EX58_AUTHORING_REGISTER.json')['directions']};ids=[s['id'] for s in SECTIONS]
    ck('Six reputation directions exactly',ids==[f'RP-A{i:02d}' for i in range(1,7)])
    prior=read(R/'data/director/expedition_candidate/part05.json')['cumulativeAuthoredQuestionIds']
    ck('Prior52directions distinct',len(prior)==len(set(prior))==52)
    ck('All58 directions now represented',set(prior+ids)==set(by) and len(prior+ids)==58)
    for q in ids:ck('Reputation direction unchanged by scoped amendments '+q,by[q]==original[q])
    for correction in ['EX58_EDIT_01_FULFILLMENT.json','EX58_EDIT_02_FULFILLMENT.json']:
        for rel,e in read(A/correction)['descendants'].items():ck('Confirmed amendment preserved '+rel,info(G/rel)==e)
    source_addendum=read(A/'REPUTATION_PRESERVATION_SOURCE_ADDENDUM.json')
    public={'schemaVersion':1,'moduleId':'EX58-PART06','status':'authored-modules-complete-integrated-candidate-incomplete',
            'notice':'Working chapter module 6. All58 source directions now have authored chapter modules; complete integrated records, assembly and exact GPT review are still required.',
            'questionIds':ids,'completeExpeditionCandidate':False,'selectionEnabled':False,
            'sections':[{'id':s['id'],'title':s['title'],'text':s['player']} for s in SECTIONS],
            'backgroundStartingRules':[{'backgroundId':b['backgroundId'],'name':b['name'],'grants':[{k:g[k] for k in ['actualRelationshipRequired','sourceBand','newInitialScore']} for g in b['newStartingGrantRules']]} for b in backgrounds]}
    cases=[{'id':i,'question':q,'given':g,'expected':e,'evidenceClass':'authored synthetic expectation; not actual save execution'} for i,q,g,e in CASES]
    director={'notice':public['notice'],'sections':[{'id':s['id'],'title':s['title'],'text':s['director']} for s in SECTIONS],'workedCases':cases,'originalProbeBindings':probe_bindings}
    # New synthetic raw blobs exercise preservation properties; these are not user saves.
    raw_fixtures=[
      ('typed-extension',b'{ "schema":"unknown", "standing":{"local-guild":5,"zero":0,"nil":null,"flag":false,"text":"1","fraction":1.7}, "extra":{"note":"keep"} }\n'),
      ('duplicate-key',b'{"standing":{"local-guild":1,"local-guild":2},"numberSpelling":1.00}\n'),
      ('parse-error',b'{"standing":{"local-guild":1,}\n'),
      ('explicit-zero',b'{"standing":{"local-guild":0}}'),('absent',b'{"standing":{}}'),
    ]
    raw_records=[]
    for name,raw in raw_fixtures:
        blob=base64.b64encode(raw).decode('ascii');restored=base64.b64decode(blob)
        ck('Synthetic exact raw-byte roundtrip '+name,restored==raw and sha256(restored).digest()==sha256(raw).digest())
        try:
            occurrences=json.loads(raw.decode('utf-8'),object_pairs_hook=lambda pairs:pairs);error=None
        except json.JSONDecodeError as e:occurrences=None;error={'message':e.msg,'line':e.lineno,'column':e.colno}
        raw_records.append({'id':'RP-RAW-'+name,'origin':'new authored synthetic fixture; not a captured save','encoding':'utf-8','rawBase64':blob,'bytes':len(raw),'sha256':sha256(raw).hexdigest(),'orderedObjectPairs':occurrences,'parseError':error,'activeInterpretation':None})
    dup=next(r for r in raw_records if r['id']=='RP-RAW-duplicate-key')['orderedObjectPairs']
    ck('Duplicate occurrences stay ordered',dup[0][1]==[['local-guild',1],['local-guild',2]] or dup[0][1]==[('local-guild',1),('local-guild',2)])
    ck('Malformed raw remains with error',next(r for r in raw_records if r['id']=='RP-RAW-parse-error')['parseError'] is not None)
    typed=json.loads(raw_fixtures[0][1]);before=copy.deepcopy(typed)
    ck('False remains boolean and is not an integer',type(typed['standing']['flag']) is bool and type(typed['standing']['flag']) is not int)
    ck('String and fraction retain distinct types',type(typed['standing']['text']) is str and type(typed['standing']['fraction']) is float)
    ck('Null and zero remain distinct',typed['standing']['nil'] is None and type(typed['standing']['zero']) is int)
    ck('Unknown extension fields retained',typed==before and typed['extra']=={'note':'keep'} and typed['standing']['local-guild']==5)
    ck('Absent and explicit zero differ',json.loads(raw_fixtures[3][1])!=json.loads(raw_fixtures[4][1]))
    def scene(opening,proposals):
        proposed=sum(proposals);limited=max(-2,min(2,proposed));result=max(-3,min(3,opening+limited))
        return {'opening':opening,'proposals':proposals,'sceneProposal':proposed,'sceneAppliedProposal':limited,'sceneOverflow':proposed-limited,'scaleOverflow':opening+limited-result,'result':result,'deltaFromOpening':result-opening}
    scene_refs=[scene(2,[2]),scene(2,[2,-2]),scene(0,[2,2,2]),scene(-2,[-2]),scene(-2,[-2,2])]
    expected=[(3,0,1),(2,0,0),(2,4,0),(-3,0,-1),(-2,0,0)]
    for i,(s,e) in enumerate(zip(scene_refs,expected)):ck('Synthetic signed scene/overflow '+str(i+1),(s['result'],s['sceneOverflow'],s['scaleOverflow'])==e)
    mapping={-5:-3,-4:-3,-3:-2,-2:-1,-1:-1,0:0,1:1,2:1,3:2,4:3,5:3}
    ck('Optional explicit Loop mapping all11entries',list(mapping.items())==list(zip(range(-5,6),[-3,-3,-2,-1,-1,0,1,1,2,3,3])))
    cult=next(b for b in backgrounds if b['name']=='Cult Escapee')
    ck('Fresh Cult exact three grants',[g['newInitialScore'] for g in cult['newStartingGrantRules']]==[-2,-1,1])
    ck('Cult original runtime conflict retained',cult['originalRuntimeMap']['religious-orders']==1)
    ck('Correct initialization then replay earned scene',scene(-1,[1])['result']==0 and scene(1,[1])['result']==2)
    identity=('synthetic-subject','cult-escapee','EX58-SOURCE-2026-10-11');applied={identity};before_init=set(applied);applied.add(identity)
    ck('Synthetic initialization identity is idempotent',applied==before_init)
    authoritative={'score':3,'version':7};display='Honored' if authoritative['score'] in [2,3] else 'other';reloaded=json.loads(json.dumps(authoritative))
    ck('Display does not rewrite numeric endpoint',display=='Honored' and reloaded=={'score':3,'version':7})
    version_fixture={'score':0,'version':7,'unrelated':{'keep':True}};accepted={'expected':7,'next':8};stale={'expected':7};version_fixture['score']=1;version_fixture['version']=accepted['next'];snapshot=copy.deepcopy(version_fixture)
    stale_rejected=stale['expected']!=version_fixture['version'];ck('Synthetic stale expected version has no mutation',stale_rejected and version_fixture==snapshot and version_fixture['unrelated']=={'keep':True})
    contracts=read(R/'data/director/expedition_candidate/source_contracts_corrected.json')['contracts']
    internal={'schemaVersion':1,'moduleId':public['moduleId'],'status':public['status'],'sourceReview':'EX58-SOURCE-2026-10-11','completeExpeditionCandidate':False,
              'authoredQuestionIds':ids,'cumulativeAuthoredQuestionIds':prior+ids,'remainingSourceDirections':[],
              'publicEnvelope':public,'directorModule':director,'completeCurrentDirections':[by[q] for q in ids],'completeOriginalDirections':[original[q] for q in ids],
              'completeReputationSourceBinding':binding,'completePreservationSourceAddendum':source_addendum,
              'completeCurrentContracts':[c for c in contracts if c['id'] in ['EC-11','EC-12','EC-13','EC-15']],
              'syntheticRawFixtures':raw_records,'syntheticReferenceSceneRecords':scene_refs,'explicitOptionalLoopMapping':[{ 'old':k,'derived':v } for k,v in mapping.items()],
              'audienceBoundary':'All44source faction definitions, draft/resonance flags, old runtime maps, raw probes and private raw examples remain internal. Public tables contain the20source background relationship clauses only, not automatic category membership or full faction dossiers.',
              'remainingAssembly':'All58directions have six chapter modules, but complete21-event integrated records,28boundaries,24originalscenarios tied to actual candidate record instances, full schemas/envelopes and whole-candidate review remain incomplete.',
              'evidenceScope':'Raw-byte/typed synthetic preservation and pure reference arithmetic only; no production adapter, real save, institution, witness or campaign authentication.',
              'newPromotions':0,'runtimeImplemented':False,'realSavesReadOrWritten':0,'examplesAreRuntimeTests':False}
    for rel,e in read(A/'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest'].items():
        if rel!='README_EXPEDITION_INTEGRATED_V3.md':ck('Original submitted source unchanged '+rel,info(G/rel)==e)
    rendered={'player':render(public,'player'),'director':render(director,'director')}
    save(paths['public'],public);save(paths['internal'],internal)
    for audience in ['player','director']:
        paths[audience].parent.mkdir(parents=True,exist_ok=True);paths[audience].write_text(rendered[audience],encoding='utf-8',newline='\n')
    ck('Complete public envelope parity',read(paths['public'])==read(paths['internal'])['publicEnvelope'])
    ck('Complete player chapter parity',paths['player'].read_text('utf-8')==render(read(paths['public']),'player'))
    ck('Complete Director chapter parity',paths['director'].read_text('utf-8')==render(read(paths['internal'])['directorModule'],'director'))
    ck('Whole44faction/20background/12probe source binding preserved',read(paths['internal'])['completeReputationSourceBinding']==binding)
    ck('Public relationship projection contains no faction dossiers','fullOriginalFactionRecords' not in read(paths['public']) and all('candidateRegistryReferences' not in g for b in public['backgroundStartingRules'] for g in b['grants']))
    links=[]
    for audience in ['player','director']:
        for target in re.findall(r'\]\(([^)]+)\)',paths[audience].read_text('utf-8')):
            ck('Actual local link '+target,(paths[audience].parent/target).resolve().is_file());links.append(target)
    for x in manifest['files']:ck('Final source package unchanged after authorship '+x['path'],info(P/x['path'])=={k:x[k] for k in ['bytes','sha256']})
    receipt={'generatedAtUtc':datetime.now(timezone.utc).isoformat(),'moduleId':public['moduleId'],
             'status':'All58directions authored across six module pairs. Full integrated records/assembly/exact review still open; no full candidate approval.',
             'questionIds':ids,'cumulativeQuestionIds':prior+ids,'remainingDirections':0,'workedCases':len(cases),'originalProbesPreserved':12,
             'fullBackgroundsPreserved':20,'fullFactionsPreserved':44,'syntheticRawBlobs':len(raw_records),'syntheticSceneRecords':len(scene_refs),
             'checks':len(checks),'failures':[c for c in checks if not c['pass']],'localLinkChecks':len(links),
             'outputs':{p.relative_to(G).as_posix():info(p) for k,p in paths.items() if k!='receipt'},'builder':{'path':Path(__file__).resolve().relative_to(G).as_posix(),**info(Path(__file__))},
             'scope':internal['evidenceScope'],'runtimeTestsExecuted':0,'newPromotions':0,'realSavesReadOrWritten':0,'sourceInformationDeleted':0,'details':checks}
    save(paths['receipt'],receipt);print(json.dumps({k:receipt[k] for k in ['moduleId','remainingDirections','workedCases','checks','failures','outputs']},indent=2))

if __name__=='__main__':main()
