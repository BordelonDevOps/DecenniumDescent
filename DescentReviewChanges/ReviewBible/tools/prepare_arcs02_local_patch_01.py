"""Build a complete, source-preserving prose correction for the actual second arc return."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, json, re
from zipfile import ZipFile, ZIP_DEFLATED
from apply_di7_ap_as_01 import G, R, A, info, encoded


def read(p): return json.loads(p.read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()


def main():
    source=A/'cosmology-epilogue-campaign-arcs-01-return-02'
    first=A/'cosmology-epilogue-campaign-arcs-01-return-01'
    root=A/'arcs02-local-patch-01'; candidate=root/'candidate'
    archive=A/'DD_Campaign_Arcs_02_Local_Patch_01.zip'
    review=A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_RETURN_02_SEMANTIC_REVIEW_01.json'
    assert all(not p.exists() for p in [root,archive,review])
    model=read(source/'CAMPAIGN_ARCS_MODEL.json'); cases=read(source/'CASEBOOK.json')
    original_cases=read(first/'CASEBOOK.json')['cases']; original_byid={x['id']:x for x in original_cases}
    old_cases=deepcopy(cases)
    root.mkdir();candidate.mkdir()
    for p in source.iterdir():
        (candidate/p.name).write_bytes(p.read_bytes())
        q=root/'original-return02'/p.name;q.parent.mkdir(exist_ok=True);q.write_bytes(p.read_bytes())

    findings=[
      {'id':'AR2-01','finding':'The new Director AIR-01–14 supplement renames/reassigns IDs and substitutes several unsupported rows. For example model AIR-04 is Nomadic Human, AIR-05 Winterfang, AIR-07 Physical Conditioning, AIR-10 Adaptive Perfection and AIR-11 Adaptive Mutation; the prose instead assigns other topics to those IDs.',
       'resolution':'Keep the exact Return02 model and all 51 source identities unchanged. Render the complete actual rows, access predicates, dispositions and supplied source evidence into the Director chapter. Do not invent replacement AIR identities.'},
      {'id':'AR2-02','finding':'Both Return02 chapters instruct holding gauge zero for 60 seconds, while the preserved CF-1 plate requires 60 seconds venting positive pressure until the gauge reaches zero; initially verified zero requires no wait. New ARC17-C29 incorrectly sets gauge zero immediately on opening the vent.',
       'resolution':'Use exact model CF-1 text in both chapters. Opening V invalidates readiness immediately; the normal positive-pressure vent interval remains 60 seconds. Correct C29 to block printing while that vent is in progress and reach verified zero only at t66 after its opening Action. Retain the accepted new pressReady rule unchanged.'},
      {'id':'AR2-03','finding':'ARC15-C02 formerly demonstrated completion exactly at Equinox E. Return02 replaces it with a generic batch example duplicated by new C10, losing the original equality scenario.',
       'resolution':'Restore the exact original C02 equality scenario from Return01; leave new C10 as the batch example. All 78 IDs remain in the same order.'},
      {'id':'AR2-04','finding':'ARC16-C28 now narrates takeoff, later abort/return and payment but reports only six total elapsed seconds, losing the earlier explicit timing-scope qualification.',
       'resolution':'Retain all actual stages, set elapsedSeconds null and provide a formula including takeoff, actual abort/return duration and actual settlement time. Record entitlement at t6 and payment only at the later real meeting. No free return or settlement is inferred.'},
      {'id':'AR2-05','finding':'The replacement Player chapter is much shorter than Return01 and omits previously stated material terms, relic boundaries, exact Equinox equality and refusal options. The Director chapter keeps stale contradictory passages above an appended correction supplement; several detailed operative fields are still missing.',
       'resolution':'Preserve all original returns. Rebuild the Player chapter from its fuller Return01 text with targeted current corrections and complete model contract/press instructions. Rebuild the Director chapter from every operative field of the unchanged Return02 model in readable sections, retaining its existing schematic maps. Exact field-to-prose mapping is recorded for audit. No source facts are deleted or new mechanics added.'},
      {'id':'AR2-06','finding':'The Return02 prose introduces four mandatory vessel-start conditions while correcting the four-condition contract list. Requiring serviceable cabin air for all departures is not in the actual powered-support prerequisites and could bar an otherwise valid no-breath crew/party.',
       'resolution':'Use the unchanged model actual anatomy, protection and support predicates. The four-condition enumeration belongs to contract acceptance. Do not introduce a universal cabin-air prerequisite through prose.'}
    ]

    # Restore only the lost equality scenario; the added batch example remains.
    next(x for x in cases['cases'] if x['id']=='ARC15-C02').update(deepcopy(original_byid['ARC15-C02']))
    wage=next(x for x in cases['cases'] if x['id']=='ARC16-C28')
    wage.update(start='Wage chest40gp; first sortie reserved10gp each, no advance. Baseline fuel and air activation begins at t0 with the coordinated takeoff.',
      events='Both operators complete takeoff at t6, earning both shares. Record actual post-takeoff travel, abort, return and later meeting time. At the actual settlement with Aren, transfer the real20gp once.',
      elapsedSeconds=None,elapsedFormula='6 + actual post-takeoff time through the return/meeting + actual settlement time; overlapping activity is counted once',
      end='Entitlement exists at t6; payment occurs only at the later actual settlement. After payment wage chest20gp, mission chest200gp. Actual fuel/air/damage and the time of the abort/return remain recorded, with no refund or free travel. The elapsed formula does not assert an unprovided route or duration.')
    vent=next(x for x in cases['cases'] if x['id']=='ARC17-C29')
    vent.update(events='Open V with an Action during t0–6. Completion starts venting and invalidates pressReady immediately. Attempt a print Action during t6–12 while the required 60-second vent interval is still incomplete. Keep V open through t66; only then does that uninterrupted vent interval establish gauge0.',
      elapsedSeconds=66,
      end='At t12 the print is blocked because V is open and current readiness is false; a verified zero gauge has not yet been established. No paper or ink is consumed. At t66 gauge0 is verified and the one pressure charge is spent. Later printing requires real safe service, a new legal cell activation and a new successful60-second test. Neither the prior test nor the still-running old drive restores pressure or readiness.')
    cases['status']='Local correction candidate from Return02; exact joint confirmation pending. Authored examples only, not runtime/human tests.'
    (candidate/'CASEBOOK.json').write_bytes(encoded(cases))

    # Keep the fuller original player reference; apply exact bounded replacements.
    player=(first/'PLAYER_CHAPTER.md').read_text(encoding='utf8')
    edits=[]
    def replace(old,new):
        nonlocal player
        assert player.count(old)==1,(old[:120],player.count(old))
        player=player.replace(old,new,1);edits.append({'old':old,'replacement':new})
    def section(start,end,new):
        old=player[player.index(start):player.index(end)]
        replace(old,new.rstrip()+'\n\n')
    replace('## Player Chapter — NEW Provisional Authored Playtest Reference','## Player Chapter — NEW Provisional Authored Playtest Candidate (Local correction 01)')
    a,b,c=model['arcs']
    containment='## Stabilizing recovered fragments\n\n'+a['containment']['procedure']+'\n\n'+a['containment']['incomplete']
    section('## Stabilizing a recovered fragment','## Equinox consequences',containment)
    replace('A fragment completing stabilization **exactly at E** counts as sealed before the deadline.','A fragment completing stabilization **exactly at E** counts as sealed before the deadline.') if 'A fragment completing stabilization **exactly at E** counts as sealed before the deadline.' in player else None
    replace('## Equinox consequences','A fragment completing stabilization **exactly at E** counts as sealed before the deadline.\n\n## Equinox consequences')
    replace('## Route and baseline plan', '## Route and baseline plan\n\nThe baseline starts fuel and cabin-air clocks at actual activation, at the start of the separate six-second coordinated takeoff. That takeoff grants no travel; the outbound legs below begin afterward. Earlier activation, delay or cancellation still consumes actual resources. Declining before activation consumes neither fuel nor air; wage entitlement begins only on completed takeoff.')
    for old,new in [
      ('**32,100 seconds = 8 h 55 m**','**32,106 seconds = 8 h 55 m 06 s**'),
      ('**482 m 12 s**','**482 m 18 s**'),
      ('**117 m 48 s**','**117 m 42 s**'),
      ('**185 m = 3 h 5 m**','**184 m 54 s = 3 h 4 m 54 s**'),
      ('**30,894 seconds = 8 h 34 m 54 s**','**30,900 seconds = 8 h 35 m 00 s**'),
      ('**462 m 06 s**','**462 m 12 s**'),
      ('**137 m 54 s**','**137 m 48 s**'),
      ('**205 m 06 s**','**205 m 00 s**')]:replace(old,new)
    old='A known weather current on the outbound horizontal leg can instead be avoided with a **30 powered-minute detour**. Taking it changes the sample to 9 h 25 m elapsed, 512 m 12 s powered, 87 m 48 s fuel remaining, and 2 h 35 m air remaining.'
    replace(old,b['route']['weather']+'\n\n**Engine-off mooring alternative.** '+b['route']['workedDefaultSchedule']['engineOffAlternative'])
    # Complete public operating procedures already disclosed to occupants.
    public_ops=['## Complete vessel operating reference','These procedures use the actual crew, anatomy, inventory, geometry and support state; they do not grant abilities or stock.']
    for key,title in [('body','Hull, rooms and access'),('movement','Powered movement'),('training','Role instruction'),('fuel','Fuel supply and refilling'),('air','Cabin air and cartridge replacement'),('highAtmosphere','Exposure and recovery'),('breach','Hull breaches'),('emergency','Canopy limits'),('hoods','Actual hood use'),('repair','Repairs')]:
        public_ops += ['### '+title,b['vessel'][key]]
    public_ops += ['### Launch orientation',b['launchDock']['geometry'],b['launchDock']['crewStarts'],b['launchDock']['withdrawal']]
    for key,value in b['vessel']['airlock'].items():public_ops += ['### Airlock — '+label(key),value]
    for key,value in b['vessel']['supportStates'].items():public_ops += ['### Support — '+label(key),value]
    public_ops += ['### Strand work and interruption',b['strandScene']['procedure'],b['strandScene']['risk']]
    public_ops += ['### Carrying during the sample',b['route']['workedDefaultSchedule']['sampleCarrying']]
    replace('## Wages and reward','\n\n'.join(public_ops)+'\n\n## Wages and reward')
    replace('A canceled departure before takeoff earns no wage. Abort after takeoff still earns that sortie\'s shares. Two ordinary two-crew sorties exhaust the wage pool. An agreed advance moves the real coins aboard and therefore changes the manifest.',
      'A canceled departure before completed takeoff earns no wage. Abort after completed takeoff still earns that sortie\'s shares. Already activated fuel and air clocks continue and are not refunded. Two ordinary two-crew sorties exhaust the wage pool. An agreed advance moves the real coins aboard and therefore changes the manifest.')
    terms=['## Complete patent offer and annual term','The term requires actual understanding, signature or witnessed mark, the actual bond and actual readable plate access. The following are the complete material offer terms; no hidden additional clause is implied.']
    for clause in c['contractHandout']:
        title,body=clause.split(': ',1);terms += ['### '+title,body]
    section('## Starting the annual term','## CF-pattern proof press','\n\n'.join(terms))
    press=['## Complete CF-pattern operating instructions']
    for plate in c['knowledgeReward']['plates']:
        title,body=plate.split(': ',1);press += ['### '+title,body]
    press += ['### Appointments and diagnosis',c['knowledgeReward']['procedures']]
    for key,value in c['knowledgeReward']['operation'].items():press += ['### '+label(key),value]
    replace('## Refusal and the free-will scene','\n\n'.join(press)+'\n\n## Refusal and the free-will scene')
    replace('If the physical copy set does not yet exist, allocation does not create it. The press must actually make it from remaining stock.',c['refusalExercise']['delivery'])
    # Player text explicitly excludes sensitive scenario defaults, NPC stats and private motives.
    (candidate/'PLAYER_CHAPTER.md').write_text(player,encoding='utf8',newline='\n')

    # Render every model field, excluding only administrative review metadata.
    # Mapping is kept in REGISTER, not injected into table-facing prose.
    mapping=[]; omitted=[]; lines=[
      '# Decennium Descent — Complete Director Reference for EPI-15–17',
      '', '> NEW provisional authored playtest candidate. Exact local correction review is pending. Original manuscripts and explicit owner decisions retain authority. Campaign-era, runtime, human, balance, whole-game and publication gates remain separate.',
      '', 'These sections give the complete current model procedures in one reading order. They replace the abbreviated Director chapter and its contradictory supplement in the preserved Return02. The three schematic maps below are orientation aids; explicit coordinates and actual footprints govern.', '']
    exclude={'/id','/recordedAtUtc','/common/status','/common/reviewNote','/common/approvalGates','/reviewOutcome'}|{f'/arcs/{i}/status' for i in range(3)}
    def render(value,path,title,depth):
        if path in exclude:
            omitted.append({'pointer':path,'reason':'Administrative status/approval metadata; unchanged in exact model, not an operative rule.'});return
        heading='#'*min(depth,6)+' '+title
        lines.extend([heading,''])
        if isinstance(value,dict):
            for key,item in value.items():render(item,path+'/'+key,label(key),depth+1)
        elif isinstance(value,list):
            for i,item in enumerate(value):
                itemtitle=item.get('name',item.get('title',item.get('id',str(i+1)))) if isinstance(item,dict) else str(i+1)
                render(item,path+'/'+str(i),str(itemtitle),depth+1)
        else:
            text=str(value) if not isinstance(value,bool) else ('Yes' if value else 'No')
            lines.extend([text,''])
            mapping.append({'pointer':path,'heading':title,'textSha256':sha(text.encode()),'occursInDirector':True})
    render(model['common'],'/common','Shared rules and authority',2)
    for i,profile in enumerate(model['profiles']):render(profile,f'/profiles/{i}',profile['name'],2)
    for i,arc in enumerate(model['arcs']):render(arc,f'/arcs/{i}',arc['id']+' — '+arc['title'],1)
    render(model['reviewRequired'],'/reviewRequired','Remaining approval gates',2)
    render(model['knownProposalSeams'],'/knownProposalSeams','Scope boundaries',2)
    diagrams=re.findall(r'```\n[\s\S]*?```',(first/'DIRECTOR_CHAPTER.md').read_text(encoding='utf8'))
    assert len(diagrams)==3
    lines += ['# Schematic maps','']
    for title,diagram in zip(['Lantern Court','Broken Ladder strand berth','Canian patent chamber'],diagrams):lines += ['## '+title,'',diagram,'']
    director='\n'.join(lines)
    (candidate/'DIRECTOR_CHAPTER.md').write_text(director,encoding='utf8',newline='\n')

    # Make source-preserving exact differences and coverage reviewable.
    changed_cases=[]
    for old,new in zip(old_cases['cases'],cases['cases']):
        assert old['id']==new['id']
        if old!=new:changed_cases.append({'id':old['id'],'before':old,'after':new})
    assert [x['id'] for x in changed_cases]==['ARC15-C02','ARC16-C28','ARC17-C29']
    register=read(source/'REGISTER.json')
    register['localPatch01']={'status':'Exact candidate review pending; do not infer acceptance from historical Return02 verdict.',
      'findings':findings,'caseCorrections':changed_cases,'playerBase':info(first/'PLAYER_CHAPTER.md'),'playerExactEdits':edits,
      'directorCoverage':mapping,'omittedAdministrativeNodes':omitted,
      'modelBytesUnchanged':info(source/'CAMPAIGN_ARCS_MODEL.json'),'sourceHashLedgerBytesUnchanged':info(source/'SOURCE_HASHES.json')}
    (candidate/'REGISTER.json').write_bytes(encoded(register))
    original_verdict=(source/'VERDICT.md').read_text(encoding='utf8')
    (candidate/'VERDICT.md').write_text('# Exact local correction candidate — review pending\n\nThis package changes only the two readable chapters, three explicitly recorded example corrections, and review metadata. CAMPAIGN_ARCS_MODEL.json and SOURCE_HASHES.json are byte-identical to Return02. No new local rule is proposed by this patch. The actual independent findings and inverse player edits are in REGISTER.json. The following historical GPT verdict applies to Return02; exact confirmation of this corrected package remains pending.\n\n'+original_verdict,encoding='utf8',newline='\n')
    output_manifest={'id':'ARCS02-LOCAL-PATCH01','status':'Local exact correction candidate, pending GPT confirmation','sourceBindingsVerified':51,'authoredExamples':78,'runtimeTests':0,'humanPlaytests':0,
      'files':[{'path':p.name,**{k:v for k,v in info(p).items() if k!='path'}} for p in sorted(candidate.iterdir()) if p.name!='EVIDENCE_MANIFEST.json']}
    (candidate/'EVIDENCE_MANIFEST.json').write_bytes(encoded(output_manifest))
    # Independent preservation/reference/selected arithmetic checks only.
    checks=[]
    def ck(name,condition):checks.append({'name':name,'passed':bool(condition)});assert condition,name
    ck('Current model byte-identical', (candidate/'CAMPAIGN_ARCS_MODEL.json').read_bytes()==(source/'CAMPAIGN_ARCS_MODEL.json').read_bytes())
    ck('51-source ledger byte-identical',(candidate/'SOURCE_HASHES.json').read_bytes()==(source/'SOURCE_HASHES.json').read_bytes())
    ck('78 IDs/order retained',[x['id'] for x in old_cases['cases']]==[x['id'] for x in cases['cases']] and len(cases['cases'])==78)
    ck('Only three cases corrected',len(changed_cases)==3)
    ck('C02 exact original equality scenario restored',next(x for x in cases['cases'] if x['id']=='ARC15-C02')==original_byid['ARC15-C02'])
    ck('Director mappings nonempty and unique',len(mapping)>300 and len(mapping)==len({x['pointer'] for x in mapping}))
    for row in mapping:
        value=model
        for part in row['pointer'][1:].split('/'):value=value[int(part)] if isinstance(value,list) else value[part]
        text=str(value) if not isinstance(value,bool) else ('Yes' if value else 'No')
        ck('Rendered exact model field '+row['pointer'],text in director and sha(text.encode())==row['textSha256'])
    for row in b['vessel']['atmosphereInterfaces']['rows']:
        ck('Actual atmosphere identity/disposition '+row['id'],row['id'] in director and row['proposedDisposition'] in director and row['actualAccessRequired'] in director)
    for plate in c['knowledgeReward']['plates']:
        ck('Public complete plate '+plate.split(':')[0],plate.split(': ',1)[1] in player)
    ck('No erroneous held-at-zero 60-second wording','gauge has been at zero' not in player and 'gauge0 has remained' not in director)
    ck('All 14 public contract clauses',all(t.split(': ',1)[1] in player for t in c['contractHandout']))
    ck('Player relic interfaces retained',all(t in player for t in ['Shard Pendant of Xi','Concord Spear Fragment','Mirror of Potential Silence','Glove of Null Ink','Bittersap Antidote']))
    ck('Correct whole voyage arithmetic',6+18000+3726+7200+6+3168==32106 and 6+18000+2520+7200+6+3168==30900)
    ck('Physical rotation preserves orientation',0*0-(-1)*1==1)
    for e in output_manifest['files']:
        raw=(candidate/e['path']).read_bytes();ck('Output manifest '+e['path'],len(raw)==e['bytes'] and sha(raw)==e['sha256'])
    rec={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Local corrections prepared; exact GPT review pending.',
      'sourceReturn':info(A/'DD_Cosmology_Epilogue_Campaign_Arcs_01_Return_02.zip'),'sourceCheck':info(A/'COSMOLOGY_EPILOGUE_CAMPAIGN_ARCS_01_RETURN_SOURCE_CHECK_02.json'),
      'findings':findings,'caseCorrections':changed_cases,'directorOperativeLeafCount':len(mapping),'checks':checks,'checkCount':len(checks),'failureCount':0,
      'checkedScope':'Exact source/model preservation, complete field-to-prose coverage, case-ID retention, reversible player edits and selected arithmetic. No runtime or human playtest.',
      'sourceInformationDeleted':0,'newRulesAdopted':False,'runtimeTestsExecuted':0,'humanPlaytested':False}
    review.write_bytes(encoded(rec));(root/'INDEPENDENT_FINDINGS.json').write_bytes(review.read_bytes())
    (root/'README_REVIEW.txt').write_text('Review the complete candidate/ directory against the byte-exact original-return02/ and INDEPENDENT_FINDINGS.json. The model and all51-source ledger bytes are unchanged. There are78 cases with only C02 equality restored, C28 real elapsed-scope correction and C29 sixty-second vent timeline corrected. Both readable chapters are rebuilt with exact source field coverage. Independently confirm each AR2-01..06 and the entire corrected candidate as a coherent NEW provisional authored playtest reference, or return exact field/text corrections. Do not rewrite/summarize the complete chapters or regenerate unchanged source/model bytes. No canon, epoch, unresolved identity, runtime, human, balance, whole-game or publication approval is requested.\n',encoding='utf8',newline='\n')
    (root/'LOCAL_VALIDATION.json').write_bytes(encoded({'checks':len(checks),'failures':0,'directorFields':len(mapping),'runtimeTests':0,'humanPlaytests':0,'caseIds':78}))
    files=[p for p in root.rglob('*') if p.is_file()]
    (root/'PACKAGE_MANIFEST.json').write_bytes(encoded([{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]))
    with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    print(json.dumps({'archive':info(archive),'review':info(review),'checks':len(checks),'directorFields':len(mapping),'directorBytes':len(director.encode()),'playerBytes':len(player.encode())}))


def label(key):
    names={'id':'Identity','AC':'Armor Class','HP':'Hit Points','PB':'Proficiency Bonus','STR':'Strength','DEX':'Dexterity','CON':'Constitution','INT':'Intelligence','WIS':'Wisdom','CHA':'Charisma','procedure':'Procedure','proposedDisposition':'Current local disposition','sourceEvidence':'Source evidence','actualAccessRequired':'Actual access and cost requirements','readyState':'Current press readiness','safeService':'Safe service','charge':'Cell activation and stored pressure','knowledgeUse':'Using the learned procedures'}
    return names.get(key,re.sub(r'(?<=[a-z0-9])(?=[A-Z])',' ',key).replace('_',' ').capitalize())


if __name__=='__main__':main()
