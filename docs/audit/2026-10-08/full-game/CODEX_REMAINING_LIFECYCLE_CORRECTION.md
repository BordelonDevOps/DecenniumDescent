# Remaining lifecycle Choir provenance correction

Codex → Calibration Review. The one reported blocker is corrected. Please review the exact changed code/guide/regressions below and explicitly dispose of the selected80+5 interface.129 targeted checks now pass; the previous124 transactions remain. No source originals or frozen support paragraphs changed. All other reviewed behavior and excluded full-card/tempHP/form/TimeLoop/global-body/runtime work remain unchanged.

Ordinary outgoing burst no longer imposes generic noDamageTriggers, noDeathTriggers, noRetaliation, noResourceGeneration or noCopyChain. It identifies the Cleric source/owner and only its own no-Choir-healing/no-fanatic-body-resource/no-extra-explosion restrictions. Incoming sealed-zero suppression remains exactly as reviewed. The ambiguous attack profile resourceEligible:false field was also renamed attackerOwnResourcePool:false: a created attacker has no independent resource pool; this no longer suggests blanket suppression of eligible original-owner or target-side features. Actual Dark Conviction encounter/turn/victim/frequency predicates remain caller source checks.

## Exact burst and damage functions
    def burst(self,c,*,suppressed=False):
        require(c.profile=='choir','Only Choir explodes')
        if c.explosion_settled:return None
        c.explosion_settled=True
        if suppressed:return None
        return {'sourceId':CHOIR,'sourceOwner':c.source_owner,
                'fanatic':c.instance_id,'position':deepcopy(c.position),'radius':5,'targets':'legal enemies',
                'damage':'1d6 necrotic','save':'DEX half','healing':False,'commandDebit':False,
                'choirHealingEligible':False,'fanaticBodyResourceEligible':False,
                'explosionOpportunityGenerated':False,'fanaticCorpse':False}

    def damage(self,ident,amount,now,*,suppress_zero_explosion=False):
        """Actual damage after defenses, before this body's existing temp HP."""
        c=self.physical.creatures[ident]
        require(isinstance(c,RemainingCreature) and c.active(now),'Active selected finite body required')
        integer(amount,'post-defense damage',0)
        absorbed=min(amount,c.temp_hp);c.temp_hp-=absorbed;c.hp=max(0,c.hp-(amount-absorbed))
        burst=None
        if c.hp==0:
            c.state='ended'
            if c.profile=='choir':burst=self.burst(c,suppressed=suppress_zero_explosion)
        return {'burst':burst,'corpse':False,'woundRoll':False}



## Exact selected creature attack profile
@dataclass
class RemainingCreature(Creature):
    position: object=None
    explosion_settled: bool=False
    local_modes: dict=field(default_factory=dict)

    def attack_profile(self,stats):
        self.verify_stats(stats)
        out={'sourceOwner':self.source_owner,'sourceClass':self.source_class,
             'attack':stats.attack,'saves':stats.pb,'saveDC':stats.dc,
             'range':5,'mode':'melee','damageType':'necrotic','attackerOwnResourcePool':False}
        if self.profile=='choir':out['damage']=(1,6,stats.scale)
        elif self.profile=='thrall':out['damage']=(stats.scale,6,0)
        elif self.profile=='bone-servant':out['damage']=(1,8,stats.scale)
        elif self.profile=='soldier-turret':
            out.update(attack=stats.pb+stats.dexterity,range=60,mode='ranged',
                       damage=(1,6,stats.modifier),damageType='piercing')
        else:raise SpellRuleError('Unregistered remaining companion profile')
        return out




## Exact regression segment
    suppressed=w.damage(cs[0].instance_id,10,3,suppress_zero_explosion=True)
    check('Sealed zero settles explosion permanently',(suppressed['burst'],cs[0].state,cs[0].explosion_settled),(None,'ended',True))
    burst=w.damage(cs[1].instance_id,10,3)['burst']
    check('Normal zero makes one independent source burst',(burst['fanatic'],burst['radius'],burst['healing'],burst['sourceId']),(cs[1].instance_id,5,False,CHOIR))
    check('Meaningful enemy death retains Cleric feature provenance',(burst['sourceOwner'],burst.get('noResourceGeneration',False),burst.get('noDeathTriggers',False)),('owner',False,False))
    check('Ordinary target damage and retaliation rights remain source-adjudicated',(burst.get('noDamageTriggers',False),burst.get('noRetaliation',False)),(False,False))
    check('No invented global copy prohibition',burst.get('noCopyChain',False),False)
    check('Only Choir-local healing and body/opportunity gains are barred',(burst['choirHealingEligible'],burst['fanaticBodyResourceEligible'],burst['explosionOpportunityGenerated'],burst['fanaticCorpse']),(False,False,False,False))
    check('Created attacker lacks own resource pool without suppressing owner feature gates',(cs[1].attack_profile(stats())['attackerOwnResourcePool'],'resourceEligible' in cs[1].attack_profile(stats())),(False,False))


## Corrected tabletop text
Bursts are ordinary source-native Cleric-feature damage, not another command. They cannot trigger Choir's attack-hit healing, grant another fanatic explosion opportunity, or turn the fanatics themselves into corpse, XP, loot, Conviction or resurrection resources. They do not impose blanket damage/death/retaliation/resource/copy prohibitions on enemies. A meaningful hostile nonsummoned enemy damaged or killed by a burst can still qualify for Dark Conviction under that feature's actual encounter, timing and frequency gates. Unrelated target-side damage/death responses and established global copy/resource rules still apply normally. Already snapshotted source-wide bursts resolve independently. There is no repair or return of ended fanatics.

## Validation
{
  "status": "PASS",
  "checks": 129,
  "scope": "Selected remaining80+5 lifecycle/command/object/guard interfaces; not full cards or runtime"
}

## Artifact digests
tools/remaining_lifecycle_playtest_rules.py 5025094fbc461e41a72d2018852513823102039cab6fb8e96941ccb94594ff62
tools/validate_remaining_lifecycle_playtests.py bbeeea463fd905eb7694caf0f456c0186cb86424726ec9d77faf7a3b50060d7e
docs/mechanics/REMAINING_LIFECYCLE_PLAYTEST.md 5cdabd402fbd1937ea0f23e54e3abf6aa7898c1b4253feb9493ca26807d80b5f
