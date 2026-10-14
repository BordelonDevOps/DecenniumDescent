import json, hashlib
from pathlib import Path
G=Path(r'C:\Github\DecenniumDescent'); R=G/'DescentReviewChanges/ReviewBible'; A=G/'docs/audit/2026-10-08/full-game'; D=R/'data/playtest/spell_drafts'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=D/'candidate_divination_rank2.json'; sub=read(A/'DIVINATION_RANK2_EXACT_SUBMISSION.json')
assert sha(p)==sub['candidateSha256BeforeReview']
assert 'After those repairs, all eight may be promoted' in (A/'GPT_DIVINATION_RANK2_EXACT_REVIEW.md').read_text(encoding='utf-8')
d=read(p); by={s['id']:s for s in d['spells']}
repairs=[]
def change(id,field,new,reason):
    old=by[id][field]; assert old!=new
    repairs.append({'id':id,'field':field,'before':old,'after':new,'reason':reason})
    by[id][field]=new
change('locate-person','targets','Self; designate one intended specific person through personal acquaintance or a reliable identity description/name intended to refer to one actual individual.','Exact-review required preflight repair')
change('locate-person','resolution','No save. After costs are committed, resolve whether the designation identifies one actual qualifying person and whether that person currently exists as an eligible creature on your plane within 5,280 feet with readable location information. If so, privately learn the direction, including meaningful vertical bearing. Otherwise receive no direction, without distinguishing ambiguity, death/destruction, range, plane, eligibility or protection. Ordinary walls, cover and lack of originating line of effect do not block a permitted bearing; no prior 30-foot mark or encounter is required.','Exact-review required post-commitment eligibility repair')
change('faction-spy','targets','Self; choose one specifically identifiable headquarters of one exact canonical faction and the qualifying room/area to observe.','Exact-review required preflight repair')
old=by['faction-spy']['effect']
anchor='For the duration, receive ordinary sight in all directions and hearing from the point alongside your local senses.'
assert anchor in old
new=old.replace(anchor,'The observation feed operates at any distance, but only while the selected physical viewpoint and caster are on the same plane. If they are not, no remote sight or hearing is received and the spell does not identify plane separation as the reason. For the duration while this feed is available, receive ordinary sight in all directions and hearing from the point alongside your local senses.')
change('faction-spy','effect',new,'Exact-review required same-plane feed condition after commitment')
change('resonance-tracking','targets','Self; search the area within 30 feet and line of effect for one qualifying actual spell-casting trace, then track the selected event’s surviving local trace under this spell’s rules.','Exact-review required Self/search-area preflight repair')
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
sub.update({'status':'three exact-review preflight repairs applied; Vision Trap shared-timing clarification pending; not promoted','candidateSha256AfterPreflightRepairs':sha(p),'requiredRepairsApplied':repairs})
(A/'DIVINATION_RANK2_EXACT_SUBMISSION.json').write_text(json.dumps(sub,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
vision=by['vision-trap']
old_timing='Use the first future regular target-end marker strictly after application; an end phase already in progress does not count.'
new_timing='Use the end marker of the target’s first future regular turn. If application occurs during the target’s current turn, exclude that entire current turn’s end, whether still upcoming or already in progress.'
assert old_timing in vision['effect']
proposed=vision['effect'].replace(old_timing,new_timing)
combat=R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md'; lines=combat.read_text(encoding='utf-8').splitlines()
evidence=[{'line':i+1,'text':s} for i,s in enumerate(lines) if 'bare hostile target-bound' in s or '**Next turn**' in s or 'exact GPT review' in s or 'At **end**' in s]
fence=chr(96)*3
packet='''# Rank-two Divination — final Vision Trap timing clarification

I applied your three required preflight repairs exactly in scope: Locate Person targets/resolution; Faction Spy targets plus explicit same-plane-only feed in effect; Resonance Tracking targets. Those remain unselected pending this one genuine shared-rule conflict.

Your exact review approves Vision Trap's “first future target regular-turn end strictly after application” and excludes only an end phase already underway. But the same card's duration and your source conference say “end of its first future regular turn.” The existing reviewed COMBAT_ACTION_PLAYTEST expressly excludes the entire current target turn from both a hostile N-round endpoint and “next turn” endpoints, even if its end is still upcoming.

Concrete case: a readied Vision Trap releases during the enemy's current regular turn, after its movement but before it attacks. The first end strictly after application is that current turn's upcoming end. The existing next-turn rule instead uses the end of its next regular turn. These are different endpoints; the current manuscript has both.

Proposed minimal repair: in Vision Trap.effect replace only the timing sentence with:

“Use the end marker of the target’s first future regular turn. If application occurs during the target’s current turn, exclude that entire current turn’s end, whether still upcoming or already in progress.”

All other wording remains as submitted, including next attack consumption (which CAN occur this current turn), the outside-initiative six-second deadline, preserved virtual markers, damage, INT save, replacement behavior and end-phase effects before cleanup. If the target makes no later attack this current turn, the pending rider therefore remains available until its next turn ends, exactly as the shared hostile/next-turn convention states.

Please confirm this repair, or explicitly identify a source-specific exception if you intend to override the shared rule. Please also confirm promotion of all eight after these three preflight repairs plus this timing repair. No runtime or whole-game closure is requested.

## Exact current Vision Trap card before proposed timing repair

'''
packet+='Candidate SHA256 after the three preflight repairs: '+sha(p)+'\n\n'+fence+'json\n'+json.dumps(vision,indent=2,ensure_ascii=False)+'\n'+fence+'\n'
packet+='\n## Exact proposed effect field\n\n'+proposed+'\n'
packet+='\n## Existing shared timing evidence\n\nSource: DescentReviewChanges/ReviewBible/docs/mechanics/COMBAT_ACTION_PLAYTEST.md\nByte SHA256: '+sha(combat)+'\n\n'+fence+'json\n'+json.dumps(evidence,indent=2,ensure_ascii=False)+'\n'+fence+'\n'
packet+='\n## Applied exact-review preflight repairs\n\n'+fence+'json\n'+json.dumps(repairs,indent=2,ensure_ascii=False)+'\n'+fence+'\n'
pp=A/'CODEX_DIVINATION_RANK2_FINAL_CLARIFICATION.md'; assert not pp.exists(); pp.write_text(packet,encoding='utf-8')
(A/'DIVINATION_RANK2_TIMING_PROPOSAL.json').write_text(json.dumps({'id':'vision-trap','field':'effect','oldTiming':old_timing,'newTiming':new_timing,'proposedEffect':proposed,'status':'pending GPT clarification'},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'candidateSha256':sha(p),'approvedPreflightFieldRepairs':len(repairs),'packetCharacters':len(packet),'stillSelected':182},indent=2))
