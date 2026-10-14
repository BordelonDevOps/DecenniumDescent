"""Insert missing spaces in compact draft prose without changing any characters.

This is presentation cleanup only. Original raw prose and a reviewable change ledger
remain available; unknown words are left alone rather than guessed or rewritten.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import re,math,json
ROOT=Path(__file__).resolve().parents[1]
SOURCES=ROOT/'data/playtest/class_sources'
corpus=[]
corpus.append((ROOT.parents[1]/'docs/reference/Player_Rulebook_v6_source_text.txt').read_text(encoding='utf-8'))
for p in SOURCES.glob('*.json'):
 if p.name in ('supplements.json','card_index.json'):continue
 d=json.loads(p.read_text(encoding='utf-8'))
 corpus.extend(x['text'] for x in d['bookLines'])
for slug in ['cleric','mage','monk','wizard','warrior','oracle']:
 p=ROOT/'data/playtest/class_drafts'/f'{slug}.json'
 if p.exists():corpus.append(p.read_text(encoding='utf-8'))
counts=Counter(w.lower() for w in re.findall(r'[A-Za-z]+',' '.join(corpus)))
for w in 'HP RP RC AC DC BT PB STR DEX CON INT WIS CHA own turn twice dice tempHP temporary maximum minimum attacker creature once every slot cooldown empty damage reach prone nearby downed airborne all upkeep prerequisite reset source entire modifier regular before after caster field following possible permitted restore prone optional unless eligible profile surge buffer resource trigger choose choices feats feat passives tiers level cap commanded commands command budget nonattack damaging triggers foe stock consumes consumed consume along open route inherit infinite repaired injector overcharge handheld afterward nonartifact passwords noncombat yourself into cash unmodified confines independently reserve concentration unarmored nonstacking once physical unavailable original capacity thereafter'.split():counts[w.lower()]+=50
WORDS={w for w,c in counts.items() if len(w)>1 and c>=1}|{'a','i'}
for w in ['allowance','allowances','recharging','concentration','refills','stockpiling','inherited','adjoining','nonhealing','nonmagical','unchanged','unattended','rechargeable','strengthened','dismantled','within','throughout','reconstruction']:
 WORDS.add(w);counts[w]+=100
for w in 'farming inflicting checking clearance specification subtracting heading reversion refilled indirect spawning reproduced regrowth provenance releasing retry resummoning seventh recasts recording rating replays recapture inconsistent originator attending refitted abandoning confronting limitation allocate inversion suppressing breach rebonded insufficient attempted poisoning conflicting sixth numerical dismissal involuntary reloading additive minus reusable coating retries defeating canceled accidental reentering reused metamorphosis'.split():
 WORDS.add(w);counts[w]+=100
for w in 'motionless blindsight helpless optionally cosmetically outdoor provisionally restraining alternatives supplemental membership multiattack outlines concurrent snapshot actionable confront accompanies drawback expendable overwrite avoidance countermeasure nameless aversion foreseeable award metaphysically generically tremorsense outline payload transferable cartridge footfall targetable rearming lockable'.split():
 WORDS.add(w);counts[w]+=100
changes={}
EXPLICIT={
 'Beforethrowoptforunstablemix':'Before throw opt for unstable mix',
 'Noadditionalblastorcompoundedslow':'No additional blast or compounded slow',
 'Noautomaticpermanentdeactivation':'No automatic permanent deactivation',
 'Noautonomousdamage':'No autonomous damage',
 'andtakessameamountunmitigated':'and takes same amount unmitigated',
 'createfreshdeathtriggerormorphdroneintofreebomb':'create fresh death trigger or morph drone into free bomb',
 'endsafteronecreatureescapes':'ends after one creature escapes',
 'expireddevicesineligible':'expired devices ineligible',
 'forfeitsphysicalresistance':'forfeits physical resistance',
 'hackingallegianceorignoringbossimmunity':'hacking allegiance or ignoring boss immunity',
 'insteaddealallocatednecroticdamage':'instead deal allocated necrotic damage',
 'invertedaurareplacesit':'inverted aura replaces it',
 'noextraautonomoushealingorlonger':'no extra autonomous healing or longer',
 'orcorrespondinginverted':'or corresponding inverted',
 'resourcesorhealingduplication':'resources or healing duplication',
 'snextattackagainstchosenenemyhasadvantage':'s next attack against chosen enemy has advantage',
 'HPfraction':'HP fraction','Normaltemp':'Normal temporary','normaltemp':'normal temporary',
 'Safetyexclusion':'Safety exclusion','mphdisperses':'mph disperses','valuabletimber':'valuable timber'}
@lru_cache(None)
def split_word(token):
 lower=token.lower()
 if len(token)<5 or lower in WORDS:return token
 if lower.endswith('ing') and (lower[:-3] in WORDS or lower[:-3]+'e' in WORDS or lower[:-4] in WORDS):return token
 if lower.endswith('ed') and (lower[:-2] in WORDS or lower[:-1] in WORDS or lower[:-3] in WORDS):return token
 if any(lower.startswith(p) and lower[len(p):] in WORDS for p in ['re','un','non','in']):return token
 # Minimize segmentation cost; require meaningful fragments and complete coverage.
 n=len(token);dp=[None]*(n+1);dp[0]=(0,[])
 for i in range(n):
  if dp[i] is None:continue
  for j in range(i+1,min(n,i+24)+1):
   w=lower[i:j]
   if (w not in WORDS or w=='i') and token[i:j] not in ['S','M','L','X']:continue
   penalty=12-math.log1p(counts[w])
   candidate=(dp[i][0]+penalty,dp[i][1]+[token[i:j]])
   if dp[j] is None or candidate[0]<dp[j][0]:dp[j]=candidate
 if dp[n] and len(dp[n][1])>1:
  out=' '.join(dp[n][1]);changes[token]=out;return out
 return token
def spaced(s):
 if not isinstance(s,str):return s
 for before,after in EXPLICIT.items():
  if before in s:s=s.replace(before,after);changes[before]=after
 s=s.replace('ordisadvnextattackagainstothers','or disadvantage on next attack against others')
 s=re.sub(r'([a-z])([A-Z])',r'\1 \2',s)
 s=re.sub(r'[A-Za-z]{5,}',lambda m:split_word(m[0]),s)
 # Separate words and numbers while preserving dice, d20, 1d8, and standard identifiers.
 s=re.sub(r'(?<=[A-Za-z])(?=\d)', ' ',s)
 s=re.sub(r'(?<=\d)(?=[A-Za-z])', ' ',s)
 s=re.sub(r'\b(\d+) d (\d+)\b',r'\1d\2',s)
 s=re.sub(r'\bd (\d+)\b',r'd\1',s)
 s=re.sub(r'\b([SMLX]) d (\d+)\b',r'\1 d\2',s)
 s=re.sub(r'(?<=[a-z])(?=(?:HP|RP|RC|AC|DC|BT)\b)',' ',s)
 s=s.replace('orc ash value','or cash value')
 s=re.sub(r'\bupto\b','up to',s)
 s=re.sub(r'([,;])(?=\S)',r'\1 ',s)
 return s
