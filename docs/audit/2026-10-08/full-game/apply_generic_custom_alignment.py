"""Explicitly supersede conflicting earlier provisional periodic clauses."""
from pathlib import Path
import hashlib
import json

GAME=Path(__file__).resolve().parents[4]
ROOT=GAME/'DescentReviewChanges/ReviewBible'
PATH=ROOT/'data/playtest/condition_playtests.json'
p=json.loads(PATH.read_text(encoding='utf-8'))
review='docs/audit/2026-10-08/full-game/GPT_GENERIC_CUSTOM_ALIGNMENT.md'
supersession='SUPERSESSION — NEW PROVISIONAL INTEGRATION: The unified Bleeding/ongoing-fire family registry supersedes earlier provisional clauses that selected generic records separately, used ending DC as a damage tie-breaker, cleared all generic Bleeding through one Medicine result, or used one Burning save to clear all generic Burning. Original Core quotations and raw review history remain unchanged. See CUSTOM_CONDITION_BINDINGS.md and the recorded GPT_GENERIC_CUSTOM_ALIGNMENT review.'
p['sharedRules'][1]='Record each condition source, affected creature, applying DC, magnitude, start, duration and ending method. Same-name nonnumeric penalties apply once; independent sources continue until each ends. A generic cure naming a condition clears its source records unless a reviewed procedure specifies one-record scope. Bleeding Medicine and Burning DEX saves use the specific procedures below. Track Charmed, Frightened, Marked and Grappled relationships separately. Exhaustion, Intoxication, Unity and Wounds use their explicit tracks.'
p['sharedRules'][4]='Generic Core Bleeding and Burning join family.bleeding and family.ongoing-fire respectively, with source-owner stack groups. At one identical target timing marker, all due generic and custom groups in that family compete: highest expected unmitigated damage, then earliest application. Only the winning group\'s source-permitted instances deal damage. All due groups consume that tick; losers do not defer or bank it. Different printed markers resolve separately. No record also receives a duplicate generic tick. Core generic timing is end of regular target turn; extra turns do not tick. Outside initiative preserve one periodic step per complete six seconds with no duplicate interval across initiative transitions.'
if supersession not in p['sharedRules']:
    p['sharedRules'].append(supersession)
for c in p['conditions']:
    if c['id'] not in ('bleeding','burning'):
        continue
    c['reviewEvidence']=list(dict.fromkeys(c['reviewEvidence']+[review]))
    c['provisionalDecisions'].append(supersession) if supersession not in c['provisionalDecisions'] else None
    if c['id']=='bleeding':
        c['durationAndEnding']='Persists until its source or applicable cure ends it. Self or adjacent helper spends an Action selecting one active eligible Bleed record before a WIS (Medicine) check: printed cure DC, otherwise recorded applying effect/class/spell DC, otherwise 10. Success or Critical Success ends that record only. One legal magical healing event with positive pre-cap/pre-prohibition potential ends all ordinary records with an automatic-healing endpoint, even at full HP or while Corrupted/Decay prevents actual HP gain. Each Shaman Blood Curse instead gets its own printed CON save. Explicit end-one/end-all removers retain exact scope and protected-source exceptions.'
        c['stacking']='Independent source-owner records enter unified family arbitration at their actual marker. No DC tie-break or separate generic damage layer. Medicine ends one selected record; positive-potential magical healing ends all eligible automatic-cure records.'
    else:
        c['effect']='At end of the affected creature\'s regular turn its generic record offers 1d4 fire damage to unified family arbitration, unless its source specifies another magnitude. Only the winning stack group deals damage. Damage immunity does not by itself remove Burning.'
        c['durationAndEnding']='Self or adjacent helper may spend one Action to end all active ordinary-extinguishable attached fires on this creature. Full immersion of all burning portions does the same. Explicit protected-source exceptions survive. At each regular target turn end, after due ticks are consumed, each surviving active ongoing-fire record with future damage remaining makes its own binary DEX save against its own source DC or 10. Success ends only that record. An indefinite generic fire counts as having future damage; a finite record with its final tick consumed expires without another save.'
        c['stacking']='Independent records enter unified ongoing-fire family arbitration. One Action/full immersion clears all ordinary-extinguishable records; DEX saves operate per surviving eligible record, not one selected-source save for all fires.'
PATH.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

rp=ROOT/'data/playtest/custom_condition_bindings.json'
r=json.loads(rp.read_text(encoding='utf-8'))
defs={d['mechanicalId']:d for d in r['definitions']}
for c in p['conditions']:
    if c['id'] not in ('bleeding','burning'):
        continue
    bleed=c['id']=='bleeding'
    template=defs['ranger.synergy.bleed' if bleed else 'ranger.imbue.burn']
    ident='core.'+c['id']
    defs[ident]=dict(mechanicalId=ident,displayName='Core '+c['name'],kind='periodic-rider',
        status='reviewed provisional generic/custom alignment',familyTags=['family.bleeding' if bleed else 'family.ongoing-fire'],
        effect=c['effect'],ending=c['durationAndEnding'],stacking=c['stacking'],immunityRule=c['immunitiesAndOverrides'],
        periodic={'dice':'affected creature PB' if bleed else '1d4','damageType':'source physical type or slashing' if bleed else 'fire',
                  'ticks':None,'baseDurationTicks':None,'marker':'target.regular-turn.end',
                  'stackGroupTemplate':ident+':<sourceIdentity>:<ownerCharacterId>',
                  'maximumDamagingInstancesPerGroup':1,'replacementTiming':False,'extraTurnTicks':False,
                  'refreshNeverShortens':True,'outsideInitiative':'Preserve clock, one step per complete six seconds; no duplicated transition ticks.'},
        cure=template['cure'].copy(),integrationDecisions=[supersession],reviewEvidence=[review],
        applicationSources=[{'kind':'core-condition','path':'data/playtest/condition_playtests.json','conditionId':c['id'],
                             'condition':c,'conditionSha256':hashlib.sha256(json.dumps(c,sort_keys=True,ensure_ascii=False).encode()).hexdigest()}])
r['definitions']=list(defs.values())
for rule in r['familyRules']:
    if rule['id']=='periodic.arbitration':
        rule['rule']='Generic Core and custom groups enter ONE family arbitration at an identical target marker. '+rule['rule'] if not rule['rule'].startswith('Generic Core') else rule['rule']
        rule['reviewEvidence']=list(dict.fromkeys(rule['reviewEvidence']+[review]))
r['supersessions']=[{'reviewEvidence':review,'rule':supersession}]
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Aligned Core Bleeding/Burning with custom families; original Core quotations preserved.')
