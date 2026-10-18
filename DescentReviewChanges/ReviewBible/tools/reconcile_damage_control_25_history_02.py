"""Restore all earlier authored proposal detail and case obligations into the new cohort."""
from copy import deepcopy
from datetime import datetime,timezone
import json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
 directory=R/'data/director/spell_proposals';oldp=directory/'damage_control_25_current_01.json';out=directory/'damage_control_25_current_02.json';report=A/'DAMAGE_CONTROL_25_HISTORY_RECONCILIATION_CHECK_02.json';notes=A/'DAMAGE_CONTROL_25_HISTORY_RECONCILIATION_02.json'
 assert not any(p.exists() for p in [out,report,notes])
 old=read(oldp);d=deepcopy(old);ids={s['id'] for s in old['spells']};matches={};checks=[]
 def ck(label,ok):checks.append({'check':label,'passed':bool(ok)});assert ok,label
 for p in sorted(directory.glob('*.json')):
  if 'current' in p.name:continue
  document=read(p)
  for i,row in enumerate(document.get('records',[])):
   if row.get('spellId') in ids:
    ck('One original authored record '+row['spellId'],row['spellId'] not in matches)
    matches[row['spellId']]={'path':p,'document':document,'row':row,'pointer':'/records/'+str(i)}
 ck('Eighteen existing source-complete authored records recovered',len(matches)==18)
 explanations={
 'orb-of-annihilation':'Retain earlier independently legal object mode and actual object DEX/durability bridge; the short new creature-only alternative omitted prior authored scope.',
 'voltaic-detonation':'Retain separate DEX half-damage and CON Stunned saves plus earlier finite attached-phase ending; the short new one-CON branch is only an unaccepted alternative.',
 'meteor-spear':'Retain prior60x5x5 prism, source-required perceived enemy targeting and both full damage pools; no cylinder substitution.',
 'arc-surge':'Retain prior CON save and explicit perceived-enemy selection; DEX in current01 was a different unaccepted completion.',
 'cone-of-cold':'Retain earlier cone full diameter equal to axial distance (radius=d/2), not current01 half-angle30degrees; replace only tabletop raster convention with exact world-space geometry.',
 'destructive-wave':'Retain earlier10d6 thunder OR radiant and self-centered60ft sphere, excluding caster but including other creatures. Current01 split5+5/remote20ft alternative is preserved separately and not operative in current02.',
 'mental-bomb':'Retain earlier completed-hostile-use trigger, point-centered20ft sphere, INT save and finite next-elected-Reaction debt including actual special Reactions. Preserve current01 retaliation/WIS/ordinary-refresh alternative as history; it has not replaced the earlier fuller proposal.',
 'veil-of-terror':'Retain earlier regular-END repeat WIS saves, source visual image and precise fear identity. Current01 no-repeat-save alternative is not silently substituted.',
 'phantom-swarm':'Retain all-creature20ft sphere and30ft actual movement away from its fixed center. Add an explicit finite original latest marker/no-phase expiry proposal; no single-target10ft or homing caster rewrite.',
 'solar-flare':'Retain prior visual-delivery gate and independent fire/Blinded scope plus perception-qualified enemy set.',
 'sunbeam':'Retain prior five-foot-diameter cylinder, visual-delivery gate, single instantaneous beam and finite blindness. Remove only tabletop discretization wording from proposed current text.',
 'chain-lightning':'Retain prior actual legal object targets and full primary/secondary pre-damage snapshot. Clarify the source-specific remote arc origin and actual Globe/antimagic component checks as NEW, without importing random Chain Arc.',
 'freezing-sphere':'Restore the earlier full top-foot water selection, constant-volume/mass conservation, body/clearance exclusions, ice durability/load/slip/thaw/fire-melt proposal and both original conservation vectors. The problem is now explicit pending review/refinement, not an absent historical ice draft.',
 'blight':'Retain prior10d8 actual living-plant enhancement and narrow tracked mundane-plant mode. The12d8 creature-only current01 alternative is preserved but not selected.',
 'invisible-tide':'Retain complete prior actual Prone/Falling/hover/anchor/aquatic and no-physical-water boundaries.',
 'soulfire-nova':'Retain complete prior Undead classification, damage/blindness independence and actual companion-phase finite ending.',
 'circle-of-death':'Retain complete prior all-creature/60ft radius, material-or-focus, actual source/lifecycle and no repeated effect detail.',
 'frozen-tomb':'Retain complete prior two-future-END hard-guard/Paralyzed procedure and no physical ice or fire-thaw import.'}
 originalcases=[];history=[]
 for s in d['spells']:
  found=matches.get(s['id'])
  if not found:continue
  p=found['path'];row=found['row'];doc=found['document'];source=row['fullSourceAndCurrentAccessRecord']
  ck('Prior exact source equals current catalog '+s['id'],source==s['completeSourceAndAccess'])
  prior=deepcopy(s['procedure']);text=row['procedure']
  text=text.replace('with a consistent table grid convention when discretizing its boundary','with exact continuous world-space body/shape intersection').replace('using a consistent table grid convention','using exact continuous world-space body/shape intersection').replace('NEW table geometry treats','NEW spell-specific engine geometry treats')
  if s['id']=='phantom-swarm':text+='\n\nNEW DIGITAL FINITE-OPPORTUNITY COMPLETION: Record the next future original target regular START, or for an attached chassis the phase boundary after the next original-owner regular turn that has not begun. Exclude an owner turn already underway. With no such original schedule, record application+6 elapsed seconds. Preserve that latest marker and its virtual mapping through reorder/absence; an earlier real lawful opportunity can consume the instruction once, but a later reschedule never extends it. Finish mandatory processing before the one movement check, then expire the instruction. At a marker with no actual authorized attached phase, perform expiry bookkeeping only: no movement, Action, owner command, recharge or save. No later repair, suppression ending or owner return replays it. The original fixed area center and its application plane remain the movement reference; on another plane no route is invented and the opportunity expires. This is a proposed source-scoped extension parallel to DE4, not acceptance of its pending shared rule.'
  if s['id']=='chain-lightning':text+='\n\nNEW AC6 CURRENT INTERFACE COMPLETION FOR CONFERENCE: At the successful post-interrupt snapshot the primary must be a legal target and an operative primary application must be permitted, before it can supply this spell\'s secondary emissions. An actual field preventing that primary application prevents the dependent arcs; mere damage immunity/defense/prevention, save outcome or subsequent primary death does not. The real primary body at the pre-damage snapshot is the expressly authorized origin for each secondary arc for geometric/Globe predicates. This changes no dealer: the original caster remains each recipient root\'s dealer under Null. Recheck each secondary\'s actual payload defenses independently without retargeting, recursive arcs or a second target scan. This local origin/primary-application distinction is NEW and requires review against the accepted ward interfaces; it is not already granted by random Chain Arc.'
  s['procedure']={'completeText':text,'precedence':'This complete text and current shared rules govern the proposed current02 card. Prior current01 structured alternatives are historical only; explicitly named card geometry/save/type/endpoint overrides a generic default.','digitalStatus':'Unadopted authored video-game procedure; all historical NEW choices remain proposed, not recovered canon.'}
  s['previousStructuredAlternative01']=prior;s['originalAuthoredProposalUnchanged']=deepcopy(row);s['originalSharedProposalUnchanged']=deepcopy(doc['sharedProposal']);s['priorProposalBinding']={**info(p),'pointer':found['pointer']};s['newAuthorship']=row['newChoices'];s['historicalReconciliation']=explanations[s['id']]
  for textcase in row['workedCases']:
   cid=textcase.split(':',1)[0];originalcases.append({'id':cid,'spellId':s['id'],'originalText':textcase,'source':{**info(p),'pointer':found['pointer']+'/workedCases'},'status':'Preserved original authored scenario; not an executed runtime test. Carry the complete material obligation into final current vectors.'})
  history.append({'spellId':s['id'],'source':s['priorProposalBinding'],'priorCurrent01Procedure':prior,'resolution':explanations[s['id']],'jointAcceptance':False})
 d['originalCohortCasesUnchanged']=originalcases
 d['sharedRules']['casting']=d['sharedRules']['casting'].replace('other25 casts','other24 casts')
 d['sharedRules']['scope']+=' Current02 restores all18 earlier full authored procedures and36 original cases. Source-specific restored procedure clauses control over generic current01 defaults. Earlier proposal NEW labels remain pending.'
 d['sharedRules']['lineAndCone']='NEW scoped digital presentation of each actual proposed shape, not a global template: Meteor Spear retains its60x5x5 rectangular prism; Sunbeam retains60ft length/5ft-diameter cylinder; Supernova Lance proposes100ft length/5ft-diameter cylinder. Cone of Cold retains60ft axial length with full diameter d at axial distance d, so radius=d/2 and far diameter60. Use exact continuous Euclidean body intersection, not a tabletop raster convention. Horrid Wilting proposes an oriented30ft cube with chosen center in30ft range. Cast-specific origins and line-of-effect remain actual. None changes the geometry of an accepted other spell.'
 d['sharedRules']['duration']='Use each complete spell-specific endpoint, including its named regular-turn or actual attached-phase bridge. A generic default does not replace those original authored records. Preserve original typed/absolute clocks through reorder/absence/extra turns; initial prevention creates no deferred component. Any new companion/no-schedule bridge remains explicitly proposed and requires review. For the seven newly authored high-rank cards with no earlier record, the current01 one-target-round fallback is retained only where actually specified: original next future regular END or6sec outside/no independent schedule, without inventing creature turns. Prone follows its actual stand/cure ending.'
 d['sharedRules']['saveAndDamage']=d['sharedRules']['saveAndDamage'].replace('the unresolved exact mixed-type defense apportionment is flagged separately','Meteor Spear\'s unresolved exact mixed-type defense apportionment is flagged separately')
 d['sharedRules']['digitalGeometry']+=' The earlier source-required individual perception predicate for enemy-only selection is retained; awareness without the required actual perception does not silently add a target. A card\'s own explicit origin exclusion, object mode, prism/cone shape or actual typed predicate takes precedence.'
 for c in d['conferenceDecisions']:
  if c['id']=='DC25-ICE-01':c.update(status='Full earlier proposal restored; semantic/physical edge review pending',proposal=next(s for s in d['spells'] if s['id']=='freezing-sphere')['procedure']['completeText'],nextRequiredWork='Resolve deterministic clearance routing, damaged-ice geometry/support, splitting/rounding and slip-cycle/extra-turn behavior. Preserve prior conserved water/mass/custody/exposure cases; adopt no generic material physics silently.')
  if c['id']=='DC25-MIXED-DEFENSE-01':c['spells']=['meteor-spear'];c['proposal']+=' Destructive Wave current02 instead retains its prior single-type choice, so it no longer creates this mixed-type dependency.'
  if c['id']=='DC25-REACTION-01':c.update(question='Agree the restored after-completed-hostile-use trigger, INT save, point-centered20ft area and earliest finite next-elected-Reaction debt (including an actually chosen special Reaction)?',proposal=next(s for s in d['spells'] if s['id']=='mental-bomb')['procedure']['completeText'])
  if c['id']=='DC25-SWARM-01':c.update(question='Agree the restored20ft all-creature sphere, WIS/30ft fixed-center movement and explicit finite original marker/no-phase completion?',proposal=next(s for s in d['spells'] if s['id']=='phantom-swarm')['procedure']['completeText'])
  if c['id']=='DC25-GEOMETRY-01':c.update(question='Review each preserved explicit shape and the seven new high-rank shapes; no generic current01 shape substitution.',proposal=d['sharedRules']['lineAndCone'])
  if c['id']=='DC25-CHAIN-01':c['proposal']=next(s for s in d['spells'] if s['id']=='chain-lightning')['procedure']['completeText']
  if c['id']=='DC25-VALUE-01':c['question']='Review all retained NEW choices, including Blight10d8 plant/object branch, Destructive Wave10d6 thunder OR radiant, restored repeat-save/visual gates, and seven new high-rank completions. Preserve current01 alternatives as history, not current choices.'
 # Do not let old generated arithmetic vectors claim the changed alternatives still govern.
 d['previousCurrent01CasesUnchanged']=deepcopy(old['currentCases']);d['currentCases']=[]
 for c in old['currentCases']:
  if c.get('spellId') not in matches and c['id'] not in ['DC25-X02']:
   d['currentCases'].append(deepcopy(c))
 d['currentCaseMigrationRequirements']=[{'sourceCaseId':c['id'],'spellId':c['spellId'],'requirement':'Preserve entire original text and author explicit digital initial-state, real-source transaction, deterministic inputs and expected intermediate/final states. Resolve current accepted-interface changes explicitly, never silently drop the scenario.'} for c in originalcases]
 d['preservedCurrent01CaseDisposition']=[{'id':c['id'],'disposition':'retained current' if c['id'] in {x['id'] for x in d['currentCases']} else 'preserved previous alternative; migrate against restored exact procedure before claiming validation'} for c in old['currentCases']]
 d['previousCompleteDraft']=info(oldp);d['historicalReconciliations']=history
 d['id']='DAMAGE-CONTROL-25-CURRENT-02';d['recordedAtUtc']=datetime.now(timezone.utc).isoformat();d['status']='UNADOPTED source-complete25-spell proposal consolidation:18 restored full prior procedures, seven newly drafted procedures,36 original cases retained and32 current01 vectors preserved with explicit migration. No complete semantic review, adoption or runtime claim.'
 paths={found['path'] for found in matches.values()}|{oldp}
 for p in sorted(paths,key=str):
  if p.relative_to(G).as_posix() not in {b['path'] for b in d['sourceBindings']}:d['sourceBindings'].append(info(p))
 # No prior core question, source/access record, complete proposal or scenario may disappear.
 ck('25 source/access records exact',[s['completeSourceAndAccess'] for s in d['spells']]==[s['completeSourceAndAccess'] for s in old['spells']])
 ck('36 prior examples distinct and intact',len(originalcases)==36 and len({c['id'] for c in originalcases})==36)
 ck('32 current01 vectors retained exactly',d['previousCurrent01CasesUnchanged']==old['currentCases'] and len(old['currentCases'])==32)
 for s in d['spells']:
  if s['id'] in matches:ck('Complete original procedure/access/cases preserved '+s['id'],s['originalAuthoredProposalUnchanged']==matches[s['id']]['row'])
 for b in d['sourceBindings']:ck('Current bound file unchanged '+b['path'],info(G/b['path'])==b)
 notes.write_bytes(encoded({'id':'DAMAGE-CONTROL-25-HISTORY-RECONCILIATION-02','before':info(oldp),'matches':history,'originalCaseCount':36,'preservedAlternativeCaseCount':32,'newAdoptions':0,'scope':'Correction of the incomplete current01 draft consolidation. Earlier detailed proposals had not been accepted; they remain explicit proposals. No accepted rule changed.'}))
 out.write_bytes(encoded(d));report.write_bytes(encoded({'proposal':info(out),'reconciliation':info(notes),'checks':checks,'checkCount':len(checks),'failureCount':0,'sourceCount':len(d['sourceBindings']),'identities':25,'placements':26,'restoredPriorProcedures':18,'newHighRankProposals':7,'preservedOriginalCases':36,'preservedAlternativeVectors':32,'currentAdditionalCases':len(d['currentCases']),'newRuleAdoptions':0,'runtimeTestsExecuted':0,'sourceInformationDeleted':0}))
 print(json.dumps(read(report)|{'checks':'see report'}))

if __name__=='__main__':main()
