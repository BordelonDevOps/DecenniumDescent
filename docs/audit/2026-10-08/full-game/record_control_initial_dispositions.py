"""Record explicit first-conference classifications; does not claim implementation."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
PATH=ROOT/'data/playtest/control_state_coverage.json'
data=json.loads(PATH.read_text(encoding='utf-8'))
groups={
'cleric':{'HOOK':'judging-light','ALREADY':'judgment','DEFER':'celestial-resurgence ritual-of-undeath','STATE':'balanced-scales word-of-binding divine-judgment'},
'crimson-agent':{'ALREADY':'engine[3] blood-mark rupture-trigger phantom-strike hemorrhagic-plague','BOOK':'engine[6]','HOOK':'rupture purify-blood','STATE':'carrion-conductor'},
'dragoon':{'HOOK':'draconic-discipline','NONSTATE':'aegis-leap','STATE':'drake-mark tyrant-s-impale'},
'druid':{'BOOK':'engine[6]','STATE':'panther-form-stealth tanglemaw winter-s-embrace','NONSTATE':'timeless-body','HOOK':'nature-s-ward snow-leopard','APPLY':'carrion-rat-king'},
'mage':{'DEFER':'engine[16]','HOOK':'purifying-beam undead-immunities'},
'mirrorsage':{'STATE':'light-binding','HOOK':'purifying-reflection','BOOK':'reflected-repertoire'},
'monk':{'BOOK':'engine[8] engine[18]','APPLY':'stunning-strike','HOOK':'serenity-breaker-palm healing-touch purifying-palm','STATE':'nerve-strike'},
'oracle':{'BOOK':'engine[2] engine[3] engine[15] engine[16] engine[17] engine[21] engine[22] engine[24] oracle-s-curse oracle-s-burden curse-boon-i curse-boon-ii curse-boon-iii curse-boon-iv curse-boon-v soul-cracked false-life',
 'STATE':'engine[20] curse-manifestation bone-whisper wrathful-brand purging-flame thorned-shelter garden-of-restoration marquis-s-glimpse guiding-bolt constellation-mark omen-reader concord-alignment stars-revelation-mastery',
 'HOOK':'spiral-touched-boon-ii soul-cracked-boon-v ledger-s-memory zealot-s-renewal bloom-oracle life-revelation-mastery rewind-wound paradox-skin',
 'NONSTATE':'ability-score-improvement-oracle-4 burning-blood-boon-i','ALREADY':'burning-blood-boon-ii mark-of-the-doomed'},
'paladin':{'HOOK':'engine[2] lay-on-hands sacred-touch divine-health sanctify-ground aura-of-judgment relentless-pursuit no-escape purifying-smite aura-of-purification holy-inferno cleansing-brand zealot-s-flame sanctified-immolation purifying-crown thorn-crown liberating-smite aura-of-liberation righteous-quake break-bonds shatter-shackles revolution-s-cry unbound-host liberty-unbound',
 'ALREADY':'vengeful-smite judgment-brand mark-of-retribution mourning-smite',
 'STATE':'sentence-of-doom final-verdict binding-word ancient-smite roots-of-memory primordial-surge primordial-crown linked-ward chain-of-duty iron-leash sorrow-s-weight reign-of-ashes-aura'},
'ranger':{'STATE':'engine[0] engine[4] pathfinder-s-mark predator-s-mark rootcall-quake','HOOK':'track-target toxic-affinity','APPLY':'venom-rain plague-bearer'},
'shaman':{'STATE':'engine[1] engine[4] summon-ice-wisp','BOOK':'flask-use','HOOK':'enhanced-elemental-attunement'},
'soldier':{'STATE':'engine[1] suppression-fire hold-the-line divine-lockdown net-bolt marked-for-death','NONSTATE':'guardian-s-rush'},
'thief':{'STATE':'crippling-strike'},
'tinker':{'STATE':'engine[3] engine[5] engine[6] deploy-net-trap','HOOK':'bomb-specialization','NONSTATE':'overpressure-bombs'},
'warrior':{'ALREADY':'brutality-sense brutality-momentum cellular-reconstruction','HOOK':'stabilizing-injection shoulder-spike-cluster','STATE':'infectious-mutation'},
'wizard':{'BOOK':'engine[15]','HOOK':'analyze-magic arcane-sight sigil-authority','STATE':'runic-snare binding-sigil infernal-pact-quest-based-unlock mental-binding arcane-domination mind-prison','APPLY':'will-domination'},
'ordinary':{'HOOK':'dispel-minor aura-glimpse identify detect-magic','ALREADY':'seal-minor-wound feather-fall','APPLY':'earthen-grip','NONSTATE':'elemental-bolt','STATE':'ray-of-frost frost-arrow'},
}
review=(HERE/'GPT_CONTROL_STATE_FIRST_REVIEW.md').read_text(encoding='utf-8')
table=review.split('Classification of all 179 supplied references',1)[1].split('Remaining substantive dependencies',1)[0]
names={'Crimson Agent':'crimson-agent','Oracle engines/shared':'oracle','Oracle curse cards':'oracle','Oracle Battle/Bones/Flame/Life':'oracle','Oracle Shadow/Stars/Time':'oracle','Paladin base/common':'paladin','Paladin Vengeance':'paladin','Paladin Dominion/Flame':'paladin','Paladin Ancients':'paladin','Paladin Chain / Grief / Chains Broken':'paladin','Ordinary spells':'ordinary'}
paragraphs={}
for line in table.splitlines():
 if '\t' not in line: continue
 name,desc=line.split('\t',1)
 owner=names.get(name,name.lower())
 if owner in groups: paragraphs.setdefault(owner,[]).append(desc)
original=json.loads((HERE/'CONTROL_STATE_SOURCE_PACKET.json').read_text(encoding='utf-8'))
assert len(original['records'])==179
keys={(r['kind'],r.get('owner','ordinary'),r['card']['id'] if r['kind']=='class-card' else r['engineIndex'] if r['kind']=='class-engine' else r['spellId']) for r in original['records']}
count=0
for row in data['candidates']:
 owner=row['candidateId'].split(':')[1]
 if (row['sourceKind'],owner,row['sourceId']) not in keys: continue
 suffix=f"engine[{row['sourceId']}]" if row['sourceKind']=='class-engine' else row['sourceId'].split('.')[-1]
 matches=[category for category,values in groups[owner].items() if suffix in values.split()]
 assert len(matches)==1,(row['candidateId'],matches)
 row['classification']=matches[0]
 row['status']='DISCUSSED; implementation/review pending' if matches[0] in ('STATE','APPLY','HOOK') else 'DISPOSITION_RECORDED'
 row['rationale']='\n'.join(paragraphs[owner])
 row['reviewEvidence']=['docs/audit/2026-10-08/full-game/GPT_CONTROL_STATE_FIRST_REVIEW.md']
 row['openIssues']=['This is the control-state classification of the supplied passage, not a complete semantic review of all mechanics on the source.']
 if matches[0]=='DEFER': row['openIssues'].append('Death/replacement/resurrection or transformation subsystem review is still required.')
 if suffix=='cleansing-brand': row['openIssues'].append('Curse rank/tier/removability metadata requires actual affliction source review.')
 count+=1
assert count==179,count
PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{count} explicit first-conference dispositions recorded; none promoted to completed implementation.')
