"""Source-confirmed teaching corrections while the exact verdict is pending.

No rule or approval is inferred from the review's interim progress messages.
The current combat and casting guides independently supply every clarification.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(G).as_posix()
def replace(s,a,b):assert s.count(a)==1,(a,s.count(a));return s.replace(a,b,1)
def main():
 archive=A/'onboarding-before-stance-refrain-clarification';assert not archive.exists();archive.mkdir()
 submission=read(A/'ONBOARDING_CHARTER_EXACT_SUBMISSION.json')
 files=[R/'docs/playtest'/n for n in ['NEWCOMER_PLAYER_GUIDE.md','NEWCOMER_DIRECTOR_GUIDE.md','RESONANCE_CHEATSHEET.md','FIRST_BARD_WALKTHROUGH.md']]
 before={rel(p):sha(p) for p in files};assert all(h==submission['sourceAndDraftHashes'][n] for n,h in before.items())
 sources=[R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',R/'docs/mechanics/SPELL_INTEGRATION_RULES.md']
 sourcehashes={rel(p):sha(p) for p in sources}
 assert all(h==submission['sourceAndDraftHashes'][n] for n,h in sourcehashes.items())
 combat=sources[0].read_text(encoding='utf-8');casting=sources[1].read_text(encoding='utf-8')
 assert 'Choose one stance during a **regular** own turn before the first event' in combat
 assert 'A completed long rest also resets the remembered spell name and Refrain counter.' in casting
 for p in files:
  q=archive/rel(p);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);assert sha(q)==before[rel(p)]
 dump(archive/'MANIFEST.json',before)
 p=files[0];s=p.read_text(encoding='utf-8')
 anchor='Before rolling, say what you intend and identify the roll.'
 stance='**Choose a stance each regular turn.** Before your first attack, spell, relevant check/save or movement that uses a stance benefit or restriction, choose one of the five [combat stances](../mechanics/COMBAT_ACTION_PLAYTEST.md#stances): Aggressive, Guarded, Mobile, Focused or Carrying. If none of those events occurs, choose before your turn ends. Apply the chosen stance\'s actual benefits and restrictions until your next regular-turn start; you cannot choose retroactively. Extra turns preserve the stance and its spent allowances.\n\n'
 s=replace(s,anchor,stance+anchor)
 old='Retune at an eligible short-rest completion restores the amount on the Resonance reference and clears Dissonance. A beneficial long rest restores the RP pool and clears Dissonance.'
 new='Retune at an eligible short-rest completion restores the amount on the Resonance reference and clears Dissonance; it preserves the remembered spell name and Refrain counter unless an actual class feature says otherwise. A beneficial long rest restores the RP pool, clears Dissonance, and resets the remembered spell name and Refrain counter.'
 s=replace(s,old,new);p.write_text(s,encoding='utf-8')
 p=files[1];s=p.read_text(encoding='utf-8');anchor='Use [core resolution](../mechanics/CORE_RESOLUTION_PLAYTEST.md) to distinguish attacks, ordinary saves and task degrees.'
 s=replace(s,anchor,'Each character chooses one stance on every regular own turn before the first applicable attack, spell, check/save or movement; if none occurs, choose before turn end. Apply its actual benefits and restrictions until the next regular start. Extra turns preserve that stance and its spent allowances; there is no retroactive stance choice. Use the complete [stance table](../mechanics/COMBAT_ACTION_PLAYTEST.md#stances).\n\n'+anchor)
 p.write_text(s,encoding='utf-8')
 p=files[2];s=p.read_text(encoding='utf-8')
 s=replace(s,'capped at maximum; clear Dissonance. |','capped at maximum; clear Dissonance. Preserve the remembered spell name and Refrain counter unless an actual class feature says otherwise. |')
 s=replace(s,'| Beneficial completed long rest | Restore RP to maximum and clear Dissonance. |','| Beneficial completed long rest | Restore RP to maximum, clear Dissonance, and reset the remembered spell name and Refrain counter. |')
 p.write_text(s,encoding='utf-8')
 p=files[3];s=p.read_text(encoding='utf-8')
 anchor='## 4. Read a roll before choosing a result\n\n'
 s=replace(s,anchor,anchor+'For the turn examples below, Mira chooses **Mobile stance** on each regular own turn before the first applicable event. It lasts until her next regular start; an extra turn would preserve it and its spent allowances. Mobile changes neither her listed AC, Speed nor these attacks, spells and performances. Its first 5 feet of actual voluntary movement do not provoke, but grant no free movement; its opportunity-attack weapon-die restriction remains applicable. None of the examples below makes an opportunity attack. See the [full stance procedure](../mechanics/COMBAT_ACTION_PLAYTEST.md#stances).\n\n')
 anchor='She gains no spare RP from the excess calculation.'
 s=replace(s,anchor,anchor+' This short rest preserves the remembered ordinary spell name and Refrain counter unless an actual feature says otherwise. A beneficial completed long rest resets both, as well as restoring RP and clearing Dissonance.')
 p.write_text(s,encoding='utf-8')
 assert all(sha(G/n)==h for n,h in sourcehashes.items())
 links=[]
 for n in submission['manuscripts']:
  import re
  p=G/n
  for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
   if target.startswith(('http:','https:','#')):continue
   targetfile=(p.parent/target.split('#')[0]).resolve();assert targetfile.exists(),(n,target)
   links.append({'from':n,'label':label,'target':targetfile.relative_to(G).as_posix(),'exists':True})
 result={'status':'Source-confirmed stance/Refrain teaching clarifications applied; final exact verdict still pending','appliedAtUtc':datetime.now(timezone.utc).isoformat(),'exactReviewTurnId':submission['turnId'],'preservedSubmittedHashes':before,'backup':rel(archive),'currentManuscriptHashes':{rel(p):sha(p) for p in files},'unchangedGoverningSources':sourcehashes,'ruleChanges':0,'characterGrantChanges':0,'newApprovals':0,'allLocalLinksResolve':len(links),'linkChecks':links,'nextAction':'Capture final exact verdict and reconcile these draft clarifications with its named requirements before accepting the teaching manuscripts.'}
 dump(A/'ONBOARDING_STANCE_REFRAIN_CLARIFICATIONS.json',result)
 print(json.dumps({k:v for k,v in result.items() if k not in ['linkChecks','preservedSubmittedHashes','currentManuscriptHashes','unchangedGoverningSources']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
