"""Internal profile names are aliases for exact supplied abilities, not new content."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
profiles={
 'sacred-chant':['cleric.base.sacred-chant'],
 'sacrament':['cleric.arch.sacrament','cleric.engine[5]'],
 'dark-sacrament':['cleric.hero.cultist.dark-sacrament','cleric.engine[5]'],
 'healing-briar':['ranger.hero.warder.healing-briar'],
 'circle-of-harmony':['monk.hero.enlightened-master.circle-of-harmony'],
 'renewal':['shaman.engine[1]','shaman.hero.theurgist.echo-totem'],
 'renewal-extended':['shaman.engine[1]','shaman.arch.extended-totem-duration','shaman.hero.theurgist.echo-totem'],
 'restoration-field':['tinker.hero.artificer.restoration-field'],
 'desecrated-ground':['paladin.supplement.oathbreaker-shared.desecrated-ground','paladin.engine[11]'],
 'lifewell':['crimson-agent.hero.bloodweaver.lifewell'],
 'unfinished-chorus':['oracle.supplement.bones.unfinished-chorus','oracle.engine[26]'],
 'song-of-mending':['oracle.supplement.life.song-of-mending','oracle.engine[26]'],
 'enhanced-song':['oracle.supplement.life.song-of-mending','oracle.supplement.life.life-revelation-mastery','oracle.engine[26]'],
 'transcendent-meditation':['monk.hero.enlightened-master.transcendent-meditation'],
 'eternal-bloom':['oracle.supplement.life.eternal-bloom','oracle.engine[26]'],
 'wound-eater-iv':['oracle.supplement.wound-eater.wound-eater-boon-iv','oracle.engine[26]'],
 'hemostasis':['crimson-agent.hero.bloodweaver.hemostasis'],
 'cellular-reconstruction':['warrior.hero.ironskin.cellular-reconstruction'],
 'cleric-echoes':['cleric.base.echoes.echoes'],
 'resonant-seed':['oracle.supplement.life.resonant-seed','oracle.engine[26]'],
 'garden':['oracle.supplement.life.garden-of-restoration','oracle.engine[26]'],
 'burning-blood-v':['oracle.supplement.burning-blood.burning-blood-boon-v','oracle.engine[26]','oracle.engine[17]'],
 'crown-restored':['oracle.supplement.flame.crown-restored','oracle.engine[26]'],
 'nano-aegis':['tinker.hero.artificer.nano-aegis-drone'],
}
native={
 'aura-of-grace':['cleric.hero.saint.aura-of-grace'],
 'living-pulse':['ranger.hero.warder.living-pulse'],
 'thief-exsanguinate':['thief.hero.blackguard.exsanguinate'],
 'regenerative-mutation':['warrior.hero.ironskin.regenerative-mutation'],
 'bloodthick-node':['warrior.supplement.bloodthick-node'],
 'rapid-coagulation':['warrior.supplement.rapid-coagulation'],
}
contacts={
 'garden':['oracle.supplement.life.garden-of-restoration'],
 'enhanced-garden':['oracle.supplement.life.garden-of-restoration','oracle.supplement.life.life-revelation-mastery'],
 'resonant-seed':['oracle.supplement.life.resonant-seed'],
}
data={'status':'EXACT_SOURCE_LINKS; scheduling overlay under review',
      'scope':'Internal helper profile labels map to existing supplied source IDs. These are not additional spells, abilities, feat choices or class cards.',
      'reviewEvidence':['GPT_HEALING_PULSE_FIRST_REVIEW.md','GPT_HEALING_PULSE_BOUNDARIES.md','GPT_HEALING_PULSE_IMPLEMENTATION_FINDINGS.md'],
      'profiles':profiles,'nativeRecurrences':native,'contactVariants':contacts}
(ROOT/'data/playtest/healing_pulse_profiles.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Linked',len(profiles),'schedule profiles,',len(native),'native profiles and',len(contacts),'contact variants to supplied sources.')
