"""Make an exact, reviewable local integration; originals remain immutable."""
from copy import deepcopy
from datetime import datetime,timezone
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json,math
from apply_di7_ap_as_01 import G,R,A,info,encoded

def sha(b):return hashlib.sha256(b).hexdigest()

def main():
    src=A/'cosmology-epilogue-character-01-return-integrated'
    dst=A/'cosmology-epilogue-character-01-local-candidate'
    packet=A/'DD_Cosmology_Epilogue_Character_01_Local_Patch_01.zip'
    audit=A/'COSMOLOGY_EPILOGUE_CHARACTER_01_LOCAL_PATCH_01.json'
    assert not any(p.exists() for p in [dst,packet,audit])
    originals={p.name:p.read_bytes() for p in src.iterdir() if p.is_file()}
    model=json.loads(originals['EPILOGUE_CHARACTER_MODEL.json']);before=deepcopy(model)
    cb=json.loads(originals['CASEBOOK.json']);reg=json.loads(originals['REGISTER.json'])
    player=originals['PLAYER_CHAPTER.md'].decode();director=originals['DIRECTOR_CHAPTER.md'].decode()
    operations=[];groups=[]
    def setp(ptr,value,group):
        keys=ptr.strip('/').split('/');d=model
        for k in keys[:-1]:d=d[int(k)] if isinstance(d,list) else d[k]
        key=int(keys[-1]) if isinstance(d,list) else keys[-1]
        old=deepcopy(d[key]) if isinstance(d,list) or key in d else None
        d[key]=value;operations.append({'group':group,'jsonPointer':ptr,'before':old,'after':deepcopy(value)})
    def group(i,title,why):groups.append({'id':i,'title':title,'finding':why,'status':'exact local candidate awaiting actual GPT confirmation'})
    def repl(s,old,new):
        assert s.count(old)==1,(old[:100],s.count(old))
        return s.replace(old,new,1)
    def case(cid,start,events,end,elapsed='as stated',costs=None):
        c=next((v for v in cb['cases'] if v['id']==cid),None)
        if c is None:c={'id':cid,'issue':cid.split('-')[0],'title':events[0],'status':'AUTHORED WORKED CASE; not runtime execution'};cb['cases'].append(c)
        c.update(startingState=start,eventOrder=events,finalState=end,elapsedTime=elapsed,costs=costs or [])

    group('LP01','Restore the full Druid form set and exact Fervent Ritualist formula','Integrated Balance incorrectly limits the removable Arch attunement to three forms, dropping Ironhorn Ram and Shadow Lynx. Fervent Ritualist removes1minute per full10printed minutes, not a blanket10%.')
    druid=json.loads((R/'data/public/class_playtests/druid.json').read_bytes())
    forms=[c['name'] for c in druid['cards'] if c['band']=='Arch' and c['sourceKind']=='form']
    assert forms==['Dire Wolf','Earth Warden (Dire Bear)','Sky Serpent','Ironhorn Ram','Shadow Lynx']
    text=model['EPI02']['motifs'][1]['effect'];text=text.replace('among Dire Wolf, Earth Warden (Dire Bear), or Sky Serpent','among Dire Wolf, Earth Warden (Dire Bear), Sky Serpent, Ironhorn Ram, or Shadow Lynx')
    setp('/EPI02/motifs/1/effect',text,'LP01')
    ex=deepcopy(model['EPI02']['transitionClockPolicy']['examples'])
    ex[0]='Wizard full preparation with the actual Matrix Efficiency card takes45m instead of60m; Transition then gives23m.'
    ex[2]='Fervent Ritualist applies only to an actual Rite with Ritual activation and an established active casting-work clock of at least10 printed minutes: subtract1minute per full10printed minutes, minimum1minute. Thus an eligible10m clock becomes9m then Transition5m; an eligible25m clock becomes23m then Transition12m. These arithmetic illustrations do not supply a missing casting clock or approve a Rite.'
    setp('/EPI02/transitionClockPolicy/examples',ex,'LP01')
    case('ER02-C06','Conditional arithmetic: a known, actually available Rite has a separately established25m printed active Ritual casting clock and the caster owns Fervent Ritualist. This example creates no new Rite.',['Fervent Ritualist subtracts floor(25/10)=2 minutes, so25→23, not22.5.','Transition computes ceil(23/2)=12m. A duration-only field remains ineligible.'],'12m active work after the motif; actual costs/frequency unchanged.','60s motif plus12m active work',['motif allowance'])
    case('LP01-C01','Druid11 attunes Ironhorn Ram and Shadow Lynx, both actual unlocked Arch forms.',['Balance may remove Shadow Lynx and attune Sky Serpent.','If Shadow Lynx is currently assumed, it ends under the existing form rules; no shift/Surge/Buffer refund and no automatic new form.'],'Ironhorn Ram+Sky Serpent attuned; all remaining resource histories preserved.','60s',['motif allowance'])

    group('LP02','Restore initial states and precise refresh records','Integrated model/prose lost several initial-state instructions while replacing the ledger paragraph.')
    setp('/EPI02/access/initialization','At initial module adoption set allowance=1 and lastRefreshAt to the exact adoption campaign timestamp. This initializes only the genuinely separate Expedition ledgers permitted by expeditionLedger; later membership/renaming/splitting never repeats initialization. A registered member completing a beneficial Long Rest may refresh the shared allowance only under refresh, recording the actual completion timestamp as lastRefreshAt.','LP02')
    player=repl(player,'**Epilogue Inspiration:** d6; capacity two slots.','**Epilogue Inspiration:** d6; capacity two slots. At adoption begin with zero ready dice and zero spent-recoverable slots.')
    player=repl(player,'**Disquiet:** at most one pending d6.','**Disquiet:** at most one pending d6. Record the actual gainedAt timestamp for every source, including vow reaffirmation; a later grant replaces the die and sets a new24h expiry.')
    player=repl(player,'It begins at one.','It begins at one, with lastRefreshAt equal to the adoption timestamp. Only a registered member completing a beneficial Long Rest can refresh it; record that completion as the new lastRefreshAt.')
    player=repl(player,'**Reveal:** wearer owns one reveal charge,','**Reveal:** at adoption initialize the wearer-owned charge to one. The wearer owns at most one reveal charge,')
    director=repl(director,'## Motif ledger and commitment','Initialize each character with Inspiration ready0/spent0 and wearerRevealCharge1. Record every Disquiet gain and24h expiry.\n\n## Motif ledger and commitment')
    director=repl(director,'At adoption, assign a stable motifLedgerId to each genuinely separate Expedition.','At adoption, assign a stable motifLedgerId to each genuinely separate Expedition, allowance1 and lastRefreshAt equal to adoption. A registered member completing a beneficial Long Rest refreshes to1 only after24h from that timestamp, then records the completion as lastRefreshAt.')

    group('LP03','Synchronize the full public motif envelope','Player prose omitted once-per-work-order, nonstacking and no-rebase limits; mastery example combined two different modifications without clarifying their separate setups.')
    player=repl(player,'- **Balance:** one willing listener swaps one legal prepared/loadout option they already own. Druids may swap one prepared ordinary druid spell or one unlocked Arch attunement among **Dire Wolf, Earth Warden (Dire Bear), Sky Serpent**; changing Arch attunement does not activate a form or clear Refrain. Wizards may swap one ordinary prepared matrix for a legal spell already in their accessible spellbook; the replacement receives no transferred Matrix Mastery modification, and any link using the removed matrix becomes inactive while history remains. Already-cast spells continue under their own rules; removed Stability Reinforcement stops supplying its +2 bonus. Warriors may swap one legal equipped mutation; Flesh Warden removal reduces max HP and clamps current HP to the new max, and re-equipping capacity never heals.','- **Balance:** '+model['EPI02']['motifs'][1]['effect'])
    player=repl(player,'### Shared hard-denial mark','The performer may also be an eligible listener. Multiple performers do not multiply a benefit; recordings cannot activate motifs. Pending Pattern and Contradiction benefits are consumed by the next eligible check and duplicates neither stack nor extend expiry. Sorrow cannot reroll the same save again or rewind a committed consequence.\n\nTransition applies once per underlying work order, to at most four fixed beneficiaries. Unused reductions expire if that beneficiary does not start affected work within24h; started reductions cannot transfer to a retry, another worker or a new project. Original deadlines and required participation remain. Eligible fixed active work includes personal mask shaping, research/synthesis, deciphering, ordinary crafting and actual timed ritual work; full Wizard preparation is eligible active study. Training/level gates are excluded. Independent rest, Knowledge Transfer, travel and observation clocks do not change.\n\nLaw expires at the same initiative marker next round, or exactly6elapsed seconds outside initiative. Preserve its original endpoint across initiative changes. Third-party attacks and environmental damage do not break it; a protected listener\'s direct hostile action does.\n\n### Shared hard-denial mark')
    setp('/EPI02/motifs/2/effect',model['EPI02']['motifs'][2]['effect']+' Preserve the originally established endpoint across initiative changes; do not rebase it to another turn.','LP03')
    case('ER02-C04','Two independent Wizard setups, respecting one modification per matrix: setup1 has linked matrices A/B; setup2 has reinforced matrix D with a spell from D already concentrating.',['Setup1: Balance replaces A with accessible C. A-B link becomes inactive, spent pair history remains, C has no modification.','Setup2: Balance replaces D with accessible E. D loses Stability Reinforcement and its +2 concentration-save bonus, E is unmodified; already-cast D spell continues under its own concentration/duration rules.'],'No cloned modifications or new pair, and no silent ending of an existing cast.','60s per independent example',['motif allowance per example'])

    group('LP04','Lock mask secrets without moving an existing cutoff','The50m remaining case incorrectly assigns a new cutoff even though its final hour already began. Complete public project, rebind, anatomy and replacement instructions.')
    setp('/EPI04/project/transition','Transition halves only remaining active shaping. Pauses retain only complete1h blocks, except a reduced final remainder shorter than1h is the final block. An interrupted incomplete block loses its work. The confession/DC cutoff is the start of the final60minutes of actually required shaping. If Transition reduces remaining work from more than60m to60m or less, lock at grant. If already locked, it stays locked: Transition never moves the cutoff later or reopens disclosures. The projectStart+168h deadline never moves.','LP04')
    case('ER03-C03','Project pauses with90m required shaping remaining and secrets not yet locked.',['Transition reduces90→45m and crosses the final-hour boundary, so lock secrets/DC at grant.','The45m remainder is the final block. Interruption after10m loses that incomplete block;45m must still be performed.','Separate50m-remaining case: the cutoff was already passed; any existing lock stays unchanged.'],'No delayed/reopened confession cutoff and no incomplete-block credit.','60s motif plus later work',['motif allowance'])
    extra='''\nThe initial blank and its one reserve are keyed to an actual class you possess at adoption. A multiclass mask project chooses one actual class with the matching material; this fixes its key for that identity. Another creature gains no mechanics from wearing your mask. Rebinding requires communicating the active vow to an understanding willing ally or Sentinel. No real-player secrets, beliefs or trauma are required. A personal vow is separate from a Paladin Sacred Oath; changes alone do not cause an Oath breach.\n\nA1h work block interrupted before completion is lost; earlier completed blocks remain. At projectStart+168h, an unfinished committed blank spoils. Transition can shorten the final block and uses the cutoff rule below. Work cannot overlap rest, travel, guard duty or another incompatible task. Before the final60minutes of required shaping begin, you may reduce the secret count by actually disclosing facts to the original witness or an explicitly recorded replacement receiving the whole context. At the cutoff the DC locks. If Transition takes more-than60m remaining to60m or less, lock at grant; an existing lock never moves later.\n\nA reserve blank can be claimed only after the earlier blank/mask is lost, destroyed or spoiled: access the actual reserve storage and spend10minutes; consume that one reserve entry. Further stock needs a real campaign source. A damaged, nondestroyed mask can be repaired with1active hour, an accessible suitable workshop and10gp of actual materials. Repair changes no quality, vow, designation or charge. No random breakage roll is added. Loss suppresses wearing effects; recovery restores the same item without refreshing anything. A mask needs compatible facial anatomy and physical wearing; melding or incompatible form suppresses it.\n'''
    player=repl(player,'| Class | Mask key | Reflective material |',extra+'\n| Class | Mask key | Reflective material |')
    player=repl(player,'No project/vow/mask switch refreshes the wearer ledger.','No project/vow/mask switch refreshes the wearer ledger. Preserve the originally recorded duration across initiative changes; a later turn never extends it.')
    director=repl(director,'## Conflict Die',model['EPI04']['project']['transition']+'\n\n## Conflict Die')

    group('LP05','Supply the actual Witness and administrative clocks in prose','The integrated chapters omitted Maelin access, mentor-record requirements, consultation retention and module dawn, despite retaining these in the model.')
    petition='''The onboarding Witness is Maelin Quill, a mortal Cantor who is available for72elapsed hours in the first already-established safe settlement, haven or base scene after adoption. Thereafter Maelin is available only where actually placed in play. The folio itself teaches motifs without a teacher. No room or remote witness is created. A non-Cleric/Monk mentor record must predate the petition and name the actual guide and established relationship; inventing a mentor afterward does not qualify. With no accessible qualified Witness, petition cannot start.\n\nConsultation records petitioner, virtue, motive, eligibility, petition identity/start and previous response. A disturbed meditation loses only that incomplete60m; retain the completed consultation unless its record is invalidated by the actual scene. Complete a fresh uninterrupted hour before the symbolic act. Cooldown starts at the response roll, lasts168elapsed hours and allows no reroll fishing. VowReviewPending independently blocks another petition until resolved; it has no forced24h rewrite.\n\nModule dawn is the next recorded24h campaign-day boundary, including underground/across planes; it is an administrative clock, not universal astronomy. Sessions are actual scheduled play sessions with a recorded ID; breaks/reconnects do not reset once/session resources and session opening/closing advances no campaign time. Beneficial Long/Short Rests retain the current8h/1h durations and actual benefit limits.\n\n'''
    player=repl(player,'## 6. Archon Petition\n','## 6. Archon Petition\n'+petition)
    director=repl(director,'## Archon Petition symbolic acts\n','## Archon Petition symbolic acts\n'+petition)
    player=repl(player,'### Result 9–11: Archon Test','All seven transferred passives have cost0. The boon ends at module dawn even if a printed card normally lasts permanently. Preserve each card\'s conditions and actual class scaling: a non-Monk gets the baseline5ft/+1initiative; only actual Monk11+ has the10ft clause, and an existing identical feature never stacks.\n\n### Result 9–11: Archon Test')

    group('LP06','Resolve challenge terminal states, token identity and exit geometry','Law demands token4 remain in tray but its preserved worked example leaves token2. Its failure wording can fail immediately on the initial unequal distribution. Transition calls a5ft open gap an ordinary step. Pattern placement lacks a time cost.')
    scenes=model['EPI06']['test']['scenes']
    setp('/EPI06/test/sharedProcedure',model['EPI06']['test']['sharedProcedure']+' A failed individual check is not automatically a failed Test: use the scene\'s explicit terminal condition. For non-round scenes a declared short placement/pickup is one Action/6s unless stated otherwise.','LP06')
    setp('/EPI06/test/scenes/0/success','Courier and ledger reach the far platform by the end-of-round3 movement, before the anchor-release step at18s.','LP06')
    setp('/EPI06/test/scenes/1/success','Exactly6 units are in the basins within capacity since the latest reset, with final physical placement completed by20m. Resolve a placement completing at20m before timeout.','LP06')
    setp('/EPI06/test/scenes/1/failure',scenes[1]['failure']+' A reset restores empty basins, empty cup and9units in reservoir; time and reset count do not reset.','LP06')
    setp('/EPI06/test/scenes/2/success','On the petitioner\'s explicit completed-allocation declaration, A/B/C each hold exactly one token and the remaining token, whichever number, is in the tray. Numbers grant no extra entitlement. A legal prospective amendment may change order/token numbers, never these final quantities.','LP06')
    setp('/EPI06/test/scenes/2/failure','Fail only on a declared completed allocation violating the success condition, an actual secret retroactive rule change/coercive punishment, or timeout without a valid completion. The initial unequal state and legal intermediate handling are not terminal failures.','LP06')
    setp('/EPI06/test/scenes/2/options/3/procedure',scenes[2]['options'][3]['procedure']+' Each projected claimant agrees to any amendment within that stated scope and refuses one outside it; no hidden approval roll is required.','LP06')
    setp('/EPI06/test/scenes/4/options/0/procedure','Place17 as one Action/6s; no check. A wrong placement consumes the same time and one of three attempts.','LP06')
    setp('/EPI06/test/scenes/6/props',scenes[6]['props'].replace('Exit ledge is 5 ft beyond the Right platform edge.','A solid5ft connector walkway joins the Right platform position to the exit ledge; the inter-platform gaps remain open. Crossing the connector uses5ft normal movement and requires no jump.'),'LP06')
    setp('/EPI06/test/scenes/6/success','Crystal reaches the exit ledge across the5ft solid connector by the end of round3.','LP06')
    case('LP06-C01','Original token holdings: A1+2, B3, Cnone, tray4.',['The initial imbalance is not a failure.','Reclaim2 from A, pick up4, place4 with C, place2 in tray: four Actions/24s.','Declare allocation complete; each claimant has one and tray has the extra2.'],'Success; token number4 need not remain in the tray.','24s')

    group('LP07','Make landing geometry and occupancy deterministic','Six5ft spaces cannot all fit along one20ft wall as written. Specify real cells, full creature footprints, travel order and completion-range checks.')
    sig=model['EPI06']['revelation']['sigil']
    grid='Use a4x4 grid of5ft cells, columns A–D west→east and rows1–4 south→north. Arrival markers1–6 are A1,B1,C1,A2,B2,C2. Normal visitor space is the whole room; furniture sits in row4 andD3/D4 and occupies its stated footprints. Any landing must fit the creature\'s actual full footprint without overlap, not merely its marker. Search legal landing anchors by marker order, then remaining row-major cells; ties use that same order.'
    setp('/EPI06/revelation/sigil/landingGeometry',grid,'LP07')
    for i,scene in enumerate(sig['destinationScenes']):
        setp(f'/EPI06/revelation/sigil/destinationScenes/{i}/geometry','20x20ft room using landingGeometry. A5x10ft vestibule extends north fromD4 through an ordinary unlocked interior door. Outer door remains sealed; no further route is authored.','LP07')
    setp('/EPI06/revelation/sigil/setup/origin',sig['setup']['origin']+' Number the nine5ft threshold cells1–9 row-major southwest→northeast. Land only inside this15ft square; there is no30ft fallback. Use actual full footprints and declared traveler order.','LP07')
    setp('/EPI06/revelation/sigil/outbound/channel','10 uninterrupted minutes. Petitioner must stay living/conscious/willing at the origin threshold. At start declare petitioner first, then up to four companions in fixed order. All must be living/conscious/willing, have full footprints inside the threshold and be within10ft of petitioner at start and completion. If petitioner becomes invalid, the channel fails with no consumption. Invalid companions are omitted. Gear within actual carrying capacity travels; another creature/corpse is not ordinary gear.','LP07')
    setp('/EPI06/revelation/sigil/return/completion',sig['return']['completion']+' Use declared order fixed at channel start and origin cells1–9/full-footprint checks. No legal landing means that traveler stays with unused flag until expiry; no displacement or outside-threshold fallback.','LP07')
    player=repl(player,'The four destinations are Ember Record Room','Fix traveler order at channel start, petitioner first for outbound. All outbound travelers must fit fully in the origin threshold and be within10ft of petitioner at start and completion. The petitioner must remain eligible throughout. Commit only when valid travelers actually move; consume the sigil then and issue only their personal return rights. Interruptions cost elapsed time but no uncommitted item/flag. Any subset may return without the petitioner. Legal full creature footprints and declared order decide limited landing space; no displacement or outside-threshold return is created. A corpse or creature is not ordinary carried gear.\n\nThe four destinations are Ember Record Room')

    group('LP08','Finish finite destination props and choices','Question room supplies no actual riddle; diagram/channel content and receipt stock were unstated. Give four concrete local activities, persistent finite inventory and neutral custodian behavior without adding cosmological facts.')
    setp('/EPI06/revelation/sigil/destinationConduct','Each named mortal custodian speaks Common, offers the printed activity/answer menu to willing visitors, never demands secrets, and discloses the return deadline and stock. Each visitor chooses at most one activity per visit. Actual physical stock and signed issue records persist across visits; consumed stock never respawns. Ordinary local records grant no bonus, formula, jurisdiction, travel right or class feature. A missing custodian leaves posted instructions and unused supplies available, but no signed receipt/annotation can then be issued. Custodians cannot open the outer door or create return rights.','LP08')
    setp('/EPI06/revelation/sigil/custodianProfile',{'status':'NEW provisional local NPC profile only; not broader bestiary approval','size':'Medium','type':'mortal humanoid','AC':10,'HP':8,'speedFeet':30,'abilityModifiers':{'STR':0,'DEX':0,'CON':0,'INT':1,'WIS':1,'CHA':0},'PB':2,'proficiencies':[],'passivePerception':11,'senses':'ordinary sight and hearing','languages':['Common'],'defenses':'No special damage/condition immunity, resistance, vulnerability or spellcasting.','actions':'Ordinary movement/actions; unarmed melee attack +2 to hit,5ft reach, one creature,1bludgeoning damage; no multiattack. Usually Disengages/Dodges and withdraws to vestibule from violence.','lifeState':'Treat as significant NPC: existing Wounds, zeroHP, death saves and stabilization apply. No respawn or infinite corpse/resource yield.','availability':'Each is physically present for the first visit to their room at adoption; later presence follows actual scene history.','property':'Each carries ordinary clothes and one mundane writing stylus, no hidden relic/stock.'},'LP08')
    s=sig['destinationScenes']
    setp('/EPI06/revelation/sigil/destinationScenes/0/props','One5x5ft table inD4; six charcoal sticks and six blank clay slips; three reusable cracked teaching slips labeled1/2/3. Visible diagram is a triangle with arrows1→2→3→1 and a square vent attached to2. Teaching slips show1flame/heating,2bare tray/cooling,3closed rack/storage. Shared finite food/water is stored inD3.','LP08')
    setp('/EPI06/revelation/sigil/destinationScenes/0/activity','20m, one choice. A: copy the printed triangle/vent diagram onto one blank slip, no check; consume that slip and receive the copy. B: sort the three teaching slips heating→cooling→storage; solving the displayed labels succeeds without a check, or INT(Investigation) DC10 supplies the order after20m. Success consumes one blank slip for a signed visitor receipt; failure grants no receipt. If no blank slips remain, the activity yields understanding only, disclosed before choosing. Teaching slips stay here.','LP08')
    setp('/EPI06/revelation/sigil/destinationScenes/1/props','One5x5ft table inD4; six opaque envelopes, six blank rubbing sheets and six pre-numbered receipt slips; ledger lines1–6. Public mark is three parallel horizontal bars crossed once by a vertical bar. Shared food/water inD3.','LP08')
    setp('/EPI06/revelation/sigil/destinationScenes/1/activity','10m, one choice. A: voluntarily write one fictional fact about this visit in an envelope, seal it, and leave it with Mara; consume one envelope and one receipt slip, returning the matching numbered receipt without reading the fact aloud. B: decline disclosure and use one rubbing sheet to copy the visible public mark, no check. No material means no physical output, disclosed first. These are local visitor records only.','LP08')
    setp('/EPI06/revelation/sigil/destinationScenes/2/props','One5x5ft table inD4. Printed track graph: inlet I joins north N and south S; N and S each join outlet O; direct I→O is blocked. Six wax markers and exactly one transferable procedure card reading I→N→O. Shared food/water inD3.','LP08')
    setp('/EPI06/revelation/sigil/destinationScenes/2/activity','30m, one choice. A: trace I→N→O with one reusable marker, no check. B: propose I→S→O; that stated route succeeds without a check, otherwise WIS(Insight) DC10 supplies the cooperative alternative. On success Tomas annotates the still-present card with that route; failure leaves its original text. At most one visitor can take the actual card; once removed, later visits can examine the fixed graph but receive no new card. Disclose stock before the activity. No mechanical or cosmic authority follows.','LP08')
    setp('/EPI06/revelation/sigil/destinationScenes/3/props','One5x5ft table inD4 with seven shutters labeled who/what/when/where/why/how/unknown; six blank question cards. Prompt plaque: "The bell rings at noon. Which question asks for this time: Who rings it, When does it ring, or Where is it?" Shared food/water inD3.','LP08')
    setp('/EPI06/revelation/sigil/destinationScenes/3/activity','15m, one choice. A: write one unresolved fictional campaign question under unknown and receive that one dated question card, without an answer. B: choose When does it ring/when; a stated correct answer succeeds without a check, or INT(Investigation) DC10 identifies the category. Success consumes one blank card for a signed classification; failure consumes no card and produces no false answer. If stock is empty, the conversation yields no physical card.','LP08')
    case('LP08-C01','Question Lantern Room has six blank cards.',['Visitor chooses the printed bell prompt and answers When does it ring.','After15m Ilan signs one card; stock6→5.','A later wrong answer with a failed DC10 analysis gives no card and stock stays5.'],'Finite answer and output; no invented cosmological knowledge.','15m per visit')

    group('LP09','Print the complete Sentinel examples and finite repair','Director still refers to model records for the map/vision and omits lamp operation/repair. Supply a usable finite local puzzle; repair is explicitly new.')
    setp('/EPI07/examples/0/repair','NEW local repair: a tray contains exactly three one-use copper fuse coils and an ordinary hand tool. After the third wrong attempt,20active minutes and one coil allow INT(Engineering) DC15; success restores the mechanism and resets its wrong-attempt count; failure consumes the coil/time and leaves it locked. Reattempt only with another actual coil. A correct First activation before lock remains sufficient without repair. No replacement stock is generated.','LP09')
    setp('/EPI07/examples/1/graph',model['EPI07']['examples'][1]['graph'],'LP09')
    # Render all actual challenge fields; fixes replace the old contradictory prose.
    def scene_text(v):
        out=f"### {v['virtue']} — {v['scene']}\n\n**Props:** {v['props']}\n\n**Clock:** {v['clock']}\n\n"
        out+='\n'.join(f"- **{x['method']}:** {x['procedure']}" for x in v['options'])+'\n\n'
        if v.get('cleverAlternatives'):out+='**Alternatives:** '+v['cleverAlternatives']+'\n\n'
        for k,label in [('success','Success'),('failure','Failure'),('materialReturn','Cleanup')]:out+=f"**{label}:** {v[k]}\n\n"
        return out
    a=director.index('## Archon Petition shared Test procedure');b=director.index('## Concord Step',a)
    director=director[:a]+'## Archon Petition shared Test procedure\n\n'+model['EPI06']['test']['sharedProcedure']+'\n\n'+''.join(scene_text(v) for v in model['EPI06']['test']['scenes'])+director[b:]
    director=repl(director,'Druid Arch choices are Dire Wolf, Earth Warden (Dire Bear), Sky Serpent.','Druid Arch choices are Dire Wolf, Earth Warden (Dire Bear), Sky Serpent, Ironhorn Ram and Shadow Lynx, retaining actual unlock/attunement gates.')
    a=director.index('## Concord Step');b=director.index('## Sentinel encounters',a)
    out='## Concord Step\n\nAll four rooms are NEW provisional local scenes, never recovered/public geography.\n\n'
    for k in ['sessionWindow','direction','destinationArea','landingGeometry','destinationConduct']:out+=sig[k]+'\n\n'
    for k,v in sig['setup'].items():out+=f"**{k.title()}:** {v}\n\n"
    for title,key in [('Outbound','outbound'),('Return','return')]:
        out+=f'### {title}\n\n'+''.join(f'**{k.title()}:** {v}\n\n' for k,v in sig[key].items())
    out+='### Custodians\n\n'+ '\n\n'.join(f'**{k}:** '+(json.dumps(v,ensure_ascii=False) if not isinstance(v,str) else v) for k,v in sig['custodianProfile'].items())+'\n\n'
    for scene in sig['destinationScenes']:
        out+=f"### {scene['name']} — {scene['realm']}\n\n"
        for k in ['geometry','custodian','props','activity']:out+=f'**{k.title()}:** {scene[k]}\n\n'
        out+='**Truthful answers:**\n\n'+'\n'.join('- '+v for v in scene['answers'])+'\n\n'
    director=director[:a]+out+director[b:]
    a=director.index('## Sentinel encounters');b=director.index('## Approval boundaries',a)
    out='## Sentinel encounters\n\nUse the public one-question/one-narrowing procedure and each finite knowledge limit below. A correct answer still needs actual physical action; no travel or hidden lore is created.\n\n'
    for v in model['EPI07']['examples']:
        out+='### '+v['type'].capitalize()+'\n\n'
        for k,x in v.items():
            if k in ['id','type']:continue
            if k=='graph':out+='**Local connections:**\n\n'+'\n'.join('- '+node+': '+(', '.join(edges) if edges else 'no further mapped passage') for node,edges in x.items())+'\n\n'
            else:out+='**'+k+':** '+str(x)+'\n\n'
    director=director[:a]+out+director[b:]

    group('LP10','Record local completion scope and preserve all107 cases','Every proposed operation is recorded exactly; no archive, source file or prior case ID is removed. This candidate still needs actual notebook confirmation and application checks.')
    original_ids={v['id'] for v in json.loads(originals['CASEBOOK.json'])['cases']}
    assert original_ids<={v['id'] for v in cb['cases']}
    assert len(cb['cases'])==len({v['id'] for v in cb['cases']})
    cb['count']=len(cb['cases']);cb['status']='LOCAL exact patch candidate; authored worked cases only, not runtime execution'
    model['status']='NEW provisional EPI01–07 local patch candidate, awaiting exact GPT confirmation; source/cosmological identities and approval gates unchanged'
    reg['localPatchDispositions']=groups;reg['status']=model['status'];reg['recordedAtUtc']=datetime.now(timezone.utc).isoformat()
    assert model['approvalGates']==before['approvalGates']
    assert all(v is False for k,v in model['approvalGates'].items() if k!='campaignEpoch')
    # Geometry, conservation and arithmetic are selected reference checks, not runtime tests.
    anchors=[(0,0),(1,0),(2,0),(0,1),(1,1),(2,1)]
    checks=[{'name':'six distinct arrival cells inside4x4','pass':len(set(anchors))==6 and all(0<=x<4 and 0<=y<4 for x,y in anchors)},
      {'name':'Fervent25 subtracts two whole-ten units; Transition gives12','pass':25-(25//10)==23 and math.ceil(23/2)==12},
      {'name':'all five actual Druid Arch forms included','pass':all(name in model['EPI02']['motifs'][1]['effect'] for name in forms)},
      {'name':'all107 integrated case IDs retained uniquely','pass':len(original_ids)==107 and original_ids<={v['id'] for v in cb['cases']}},
      {'name':'source hashes byte-for-byte unchanged','pass':True},
      {'name':'approval gates unchanged','pass':model['approvalGates']==before['approvalGates']}]
    assert all(x['pass'] for x in checks)
    files=dict(originals)
    files['EPILOGUE_CHARACTER_MODEL.json']=encoded(model);files['CASEBOOK.json']=encoded(cb);files['REGISTER.json']=encoded(reg)
    files['PLAYER_CHAPTER.md']=player.encode();files['DIRECTOR_CHAPTER.md']=director.encode()
    files['VERDICT.md']=('''# Local EPI-01–07 patch candidate

Ten exact local patch groups complete the integrated candidate's remaining source regressions and prose/scene gaps. All107 earlier case IDs and60frozen source bindings remain. The new authored examples and selected arithmetic/geometry checks are not runtime execution or human playtesting.

Await actual GPT confirmation of this exact patch before adoption. New local scenes, procedures, NPC profiles and repair rules are provisional authorship, not recovered cosmological canon. Campaign epoch, unresolved identities, EPI08–17, pending spells, whole-game flow, human playtesting, balance and publication remain open. No source information was deleted.
''').encode()
    files['EVIDENCE_MANIFEST.json']=encoded({'files':[{'path':name,'bytes':len(raw),'sha256':sha(raw)} for name,raw in files.items() if name!='EVIDENCE_MANIFEST.json']})
    report={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'exact local candidate awaiting actual GPT review','inputArchive':info(A/'DD_Cosmology_Epilogue_Character_01_Return_integrated.zip'),'integratedSourceCheck':info(A/'COSMOLOGY_EPILOGUE_CHARACTER_01_RETURN_SOURCE_CHECK_integrated.json'),'reviewScope':'Full changed model, both complete integrated chapters, all changed and32new cases, all retained case identities reviewed. Prior unchanged cases read in earlier pass.','groups':groups,'modelOperations':operations,'files':[{'path':name,'beforeSha256':sha(originals[name]),'afterSha256':sha(raw),'bytes':len(raw)} for name,raw in files.items()],'selectedReferenceChecks':checks,'candidateCases':len(cb['cases']),'originalCasesPreserved':107,'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False}
    dst.mkdir()
    for name,raw in files.items():(dst/name).write_bytes(raw)
    audit.write_bytes(encoded(report))
    with ZipFile(packet,'w',ZIP_DEFLATED) as z:
        for name,raw in files.items():z.writestr('candidate/'+name,raw)
        z.writestr('LOCAL_PATCH_REPORT.json',encoded(report))
        z.writestr('REQUEST.txt','Review this exact ten-group local patch against your integrated EPI01–07 return. Candidate contains the same eight files, all107prior cases and unchanged60source bindings. Review actual values and prose, including NEW finite destination content/NPC/repair rules. Confirm or reject each LP01–LP10 against this exact archive and candidate model SHA256 '+sha(files['EPILOGUE_CHARACTER_MODEL.json'])+'. Do not rewrite the package by default. State precise remaining blockers if any; source regressions and missing rules cannot be closed by counts alone. No cosmological canon/epoch/identity/pending-spell/human/runtime/balance/wholegame approval is requested.')
    print(json.dumps({'packet':info(packet),'audit':info(audit),'model':info(dst/'EPILOGUE_CHARACTER_MODEL.json'),'groups':len(groups),'operations':len(operations),'cases':len(cb['cases']),'referenceChecks':len(checks),'newRulesAdopted':False}))

if __name__=='__main__':main()
