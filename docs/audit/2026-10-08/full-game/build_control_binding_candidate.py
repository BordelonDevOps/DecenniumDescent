"""Author control bindings with intact source evidence; not a full card compiler."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
BASE='docs/audit/2026-10-08/full-game/'
initial=json.loads((HERE/'CONTROL_STATE_SOURCE_PACKET.json').read_text(encoding='utf-8'))['records']
extra=json.loads((HERE/'CONTROL_STATE_SUPPLEMENT_SOURCE_PACKET.json').read_text(encoding='utf-8'))['records']
coverage_path=ROOT/'data/playtest/control_state_coverage.json'
coverage=json.loads(coverage_path.read_text(encoding='utf-8'))
cov={r['candidateId']:r for r in coverage['candidates']}
review=(HERE/'GPT_CONTROL_COUNTEREXAMPLE_REVIEW.md').read_text(encoding='utf-8')
dispositions={}
for line in review.split('Focused resolutions',1)[0].splitlines():
 if '\t' in line:
  ident,desc=line.split('\t',1)
  if '.' in ident: dispositions[ident]=desc
assert len(dispositions)==40,len(dispositions)
for r in extra:
 c=r['card']; row=cov[f"class-card:{r['owner']}:{c['id']}"]
 text=dispositions[c['id']]
 row.update(status='DISCUSSED; implementation/review pending',classification='HOOK' if text.startswith('HOOK') else 'STATE',
            rationale=text,reviewEvidence=[BASE+'GPT_CONTROL_COUNTEREXAMPLE_REVIEW.md'],
            openIssues=['Exact clock/semantic corrections are under review; no whole-card completion implied.'])

# Explicit source-to-component associations. A component ID is not a grant:
# its exact source's application, limits, saves and endpoint remain mandatory.
mapping={}
def add(owner, keys, ids):
 for key in keys.split(): mapping[(owner,key)]=ids.split()
add('cleric','balanced-scales','cleric.balanced-scales.mark')
add('cleric','word-of-binding','core.silenced cleric.word-of-binding.speed-zero cleric.word-of-binding.damage-hook')
add('cleric','divine-judgment','cleric.divine-judgment.mark')
add('crimson-agent','carrion-conductor','crimson-agent.carrion-conductor.corpse-mark crimson-agent.carrion-conductor.used-corpse')
add('dragoon','drake-mark','dragoon.drake-mark')
add('dragoon','tyrant-s-impale','core.restrained dragoon.tyrants-impale.restraint')
add('druid','panther-form-stealth','core.grappled druid.panther.grapple')
add('druid','tanglemaw','core.restrained druid.tanglemaw.restraint')
add('druid','winter-s-embrace','druid.winters-embrace.slow')
add('druid','carrion-rat-king','core.poisoned')
add('mirrorsage','light-binding','core.restrained mirrorsage.light-binding.restraint')
add('monk','stunning-strike','core.stunned monk.stunning-strike.reaction-denial')
add('monk','nerve-strike','monk.nerve-strike.speed-zero monk.nerve-strike.reaction-bonus-denial')
add('oracle','engine[20] curse-manifestation','oracle.curse-manifestation.self-state')
add('oracle','bone-whisper','core.incapacitated oracle.bone-whisper.soft-fallback')
add('oracle','wrathful-brand','oracle.wrathful-brand oracle.wrathful-brand.attack-penalty')
add('oracle','purging-flame','oracle.purging-flame.undead-attack-penalty')
add('oracle','thorned-shelter','oracle.thorned-shelter.buff oracle.thorned-shelter.speed-zero')
add('oracle','garden-of-restoration','oracle.garden-of-restoration.zone oracle.garden-of-restoration.undead-attack-penalty')
add('oracle','marquis-s-glimpse','oracle.marquis-glimpse.hard-control oracle.marquis-glimpse.soft-fallback')
add('oracle','guiding-bolt','oracle.guiding-bolt.star-mark')
add('oracle','constellation-mark','oracle.constellation-mark')
add('oracle','omen-reader','oracle.omen-reader.star-ash')
add('oracle','concord-alignment','oracle.concord-alignment.aura')
add('oracle','stars-revelation-mastery','oracle.guiding-bolt.enhanced-slow')
add('paladin','sentence-of-doom','paladin.sentence-of-doom.empowerment')
add('paladin','final-verdict','paladin.final-verdict.hp-prohibition')
add('paladin','binding-word','core.restrained paladin.binding-word.restraint')
add('paladin','ancient-smite primordial-surge primordial-crown','paladin.ancients.root')
add('paladin','roots-of-memory','core.restrained paladin.roots-of-memory.restraint')
add('paladin','linked-ward','paladin.linked-ward.link')
add('paladin','chain-of-duty','paladin.chain-of-duty.link')
add('paladin','iron-leash','paladin.iron-leash.speed-zero paladin.iron-leash.reaction-denial paladin.iron-leash.action-denial')
add('paladin','sorrow-s-weight','paladin.sorrows-weight.slow')
add('paladin','reign-of-ashes-aura','paladin.reign-of-ashes-aura.slow paladin.reign-of-ashes-aura.buff-suppression')
add('ranger','engine[0]','ranger.track-target.quarry')
add('ranger','engine[4]','ranger.glacial-thorn.speed-zero ranger.venomlash.damage-penalty')
add('ranger','pathfinder-s-mark','ranger.pathfinders-mark.location')
add('ranger','predator-s-mark','ranger.predators-mark.upgrade')
add('ranger','rootcall-quake','ranger.rootcall-quake.speed-zero')
add('ranger','venom-rain plague-bearer','core.poisoned')
add('shaman','engine[1]','shaman.frost-totem.slow')
add('shaman','engine[4]','shaman.flask.root shaman.flask.weaken shaman.flask.reaction-denial core.stunned')
add('shaman','summon-ice-wisp','shaman.ice-wisp.speed-zero')
add('soldier','engine[1]','soldier.overwatch.snare')
add('soldier','suppression-fire','soldier.suppression-fire.slow')
add('soldier','hold-the-line','soldier.hold-the-line.speed-zero')
add('soldier','divine-lockdown','soldier.divine-lockdown.speed-zero soldier.divine-lockdown.reaction-denial soldier.divine-lockdown.slow')
add('soldier','net-bolt','core.restrained soldier.net-bolt.restraint soldier.net-bolt.large-slow')
add('soldier','marked-for-death','soldier.marked-for-death')
add('thief','crippling-strike','thief.crippling-strike.slow')
add('tinker','engine[3]','tinker.target-scanner.mark tinker.target-taunter.attack-penalty tinker.poison-vents.attack-penalty core.stunned')
add('tinker','engine[5]','tinker.cryo.speed-zero tinker.shock.verbal-block tinker.shock.construct-reaction-denial tinker.glue.slow tinker.overload-core.reaction-denial')
add('tinker','engine[6]','core.restrained tinker.net-trap.restraint tinker.decoy-dummy.attack-penalty')
add('tinker','deploy-net-trap','core.restrained tinker.net-trap.restraint')
add('warrior','infectious-mutation','warrior.infectious-mutation.roll-penalty')
add('wizard','runic-snare','core.restrained wizard.runic-snare.restraint')
add('wizard','will-domination','core.stunned wizard.will-domination.reaction-denial')
add('wizard','binding-sigil','wizard.binding-sigil.mark')
add('wizard','infernal-pact-quest-based-unlock','wizard.gravebrand')
add('wizard','mental-binding','core.charmed wizard.mental-binding.command')
add('wizard','arcane-domination','core.charmed wizard.arcane-domination.command wizard.arcane-domination.reaction-denial')
add('wizard','mind-prison','core.incapacitated wizard.mind-prison.command wizard.mind-prison.slow wizard.mind-prison.reaction-denial')
add('ordinary','earthen-grip','core.restrained ordinary.earthen-grip.restraint')
add('ordinary','ray-of-frost','ordinary.ray-of-frost.slow')
add('ordinary','frost-arrow','ordinary.frost-arrow.slow')
# Supplemental bindings.
add('crimson-agent','veinjammer','crimson-agent.veinjammer.slow crimson-agent.veinjammer.concentration-penalty')
add('dragoon','drakestorm-dive','dragoon.drakestorm-dive.cold-slow dragoon.drakestorm-dive.reaction-denial')
add('dragoon','elemental-lance','dragoon.elemental-lance.cold-slow dragoon.elemental-lance.opportunity-denial')
add('mage','elemental-bolt elemental-surge','mage.cold-focus.flat')
add('mage','cold','mage.cold-focus.flat mage.cold-focus.glacier')
add('mage','elemental-fusion','mage.elemental-fusion.slow mage.elemental-fusion.reaction-denial mage.elemental-fusion.opportunity-denial')
add('mage','cascade-storm','mage.cascade-storm.cold-slow mage.cascade-storm.reaction-denial')
add('mage','undying-spellform','mage.undying-spellform.mobility-cap')
add('monk','echoing-guard','monk.echoing-guard.stagger')
add('monk','pressure-point-strike','monk.pressure-point.arm monk.pressure-point.leg')
add('oracle','ledger-s-command','oracle.ledger-command.control oracle.ledger-command.soft-fallback')
add('oracle','tremor-sense','core.prone oracle.tremor-sense.slow')
add('oracle','shardburst','core.prone oracle.shardburst.slow')
add('oracle','gale-of-unmaking','oracle.gale-of-unmaking.slow')
add('oracle','seal-s-fracture','oracle.seals-fracture.backlash')
add('oracle','slumber-glimpse','oracle.slumber-glimpse.action-denial oracle.slumber-glimpse.reaction-denial oracle.slumber-glimpse.initiative-penalty oracle.slumber-glimpse.attack-bonus oracle.slumber-glimpse.soft-fallback')
add('oracle','resonant-seed','oracle.resonant-seed.slow')
add('oracle','moment-s-pause','oracle.moments-pause.action-denial oracle.moments-pause.reaction-denial oracle.moments-pause.initiative-delay oracle.moments-pause.soft-fallback')
add('oracle','the-spiral-opens','oracle.spiral-opens.forced-echo')
add('paladin','black-manifestation','paladin.black-manifestation.slow paladin.black-manifestation.reaction-denial')
add('paladin','law-s-weight','paladin.laws-weight.control')
add('paladin','decree-of-submission','core.charmed core.frightened paladin.decree-of-submission.command paladin.decree-of-submission.soft-fallback')
add('paladin','echo-of-ages','paladin.echo-of-ages.attack-denial paladin.echo-of-ages.soft-fallback')
add('paladin','standing-stone','paladin.standing-stone.slow')
add('paladin','iron-leash-aura','paladin.iron-leash-aura.slow paladin.iron-leash-aura.movement-limit')
add('paladin','reign-of-ashes','paladin.reign-of-ashes.ash-bound')
add('paladin','royal-decree','paladin.royal-decree.choice core.prone')
add('shaman','elemental-affinity','shaman.elemental-affinity.ice-slow')
add('shaman','elemental-chorus','shaman.elemental-chorus.slow')
add('thief','vein-cutter','thief.vein-cutter.slow thief.vein-cutter.attack-damage-penalty')
add('thief','crippling-lash','thief.crippling-lash.slow thief.crippling-lash.weapon-hit-damage-penalty')
add('warrior','brutal-strike','warrior.brutal-strike.stagger')
add('warrior','mutation-overload','warrior.mutation-overload.backlash')
add('warrior','stonecore','warrior.stonecore.speed-side-effect')
add('warrior','hypermutation-spike','warrior.hypermutation-spike.speed-floor')

rows=[]
for r in initial+extra:
 kind=r['kind']; owner=r.get('owner','ordinary')
 ident=r['card']['id'] if kind=='class-card' else r['engineIndex'] if kind=='class-engine' else r['spellId']
 row=cov[f'{kind}:{owner}:{ident}']
 suffix=f'engine[{ident}]' if kind=='class-engine' else ident.split('.')[-1]
 components=mapping.get((owner,suffix),[])
 # Distinguish Land/Thorns state source; a shared semantic family does not merge records.
 if kind=='class-card' and '.thorns.tanglemaw' in ident: components=components+['druid.thorns-tanglemaw.restrained-damage']
 if kind=='class-card' and ident.endswith('.primordial-crown'): components=components+['paladin.primordial-crown.attack-target-restriction']
 if row['classification'] in ('STATE','APPLY'):
  assert components,(ident,row['classification'])
 row['bindingIds']=sorted(set(components+row['existingPartialBindings']))
 if kind=='class-card': source={k:r['card'].get(k) for k in ('name','activation','cost','rangeAndTarget','duration','frequency','effect','prerequisite')}
 elif kind=='class-engine': source={'effect':r['text']}
 else: source=r['operational']
 rows.append({'bindingId':row['candidateId'],'sourceKind':kind,'sourcePath':r['path'],'sourceId':ident,
   'sourceSha256':row['sourceSha256'],'classification':row['classification'],
   'componentIds':row['bindingIds'],'sourceProcedure':source,
   'interpretation':row['rationale'],'reviewEvidence':row['reviewEvidence'],
   'scope':'Control-related components only; source costs, eligibility, targets, use caps, condition immunity, source ending and hard-denial guard still apply.',
   'status':'CANDIDATE; exact review pending'})
assert len(rows)==219
data={'schemaVersion':'1.0','status':'IN_REVIEW','scope':'219 supplied passages: original179 plus40 selected supplemental cards. No exhaustive all-source claim. Component lists identify alternative/cumulative source components, never simultaneous unconditional application.',
 'operationalGuide':'docs/mechanics/CONTROL_STATES_PLAYTEST.md','bindings':rows,
 'openIssues':['Exact clock corrections under review.','Actual inflicted disease/curse source catalog and special endpoints.','Death/replacement/resurrection interfaces.','Remaining all-source semantic review; cards contain mechanics outside this bounded pass.']}
(ROOT/'data/playtest/control_state_bindings.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
coverage_path.write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{len(rows)} source-qualified candidate bindings; all original source objects retained.')
