"""Static host-kind/profile audit; not an executable gameplay qualification."""
import hashlib
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
MODEL = ROOT / 'engine/com.decennium.foundation/Laboratory/Model'
CORE = ROOT / 'engine/com.decennium.foundation/Runtime/Core'
BASELINE = 'c807ada65b296c4bde582808cd6c19a07babedda'


def read(p):
    return p.read_text(encoding='utf-8-sig')


def write(name, value):
    (OUT / name).write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))


def block(text, start):
    # Ignore comments, normal/verbatim strings and chars while matching C# braces.
    tokens = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[{}]')
    depth = 0
    for match in tokens.finditer(text, start):
        token = match.group()
        if token == '{': depth += 1
        elif token == '}':
            depth -= 1
            if depth == 0: return text[start:match.end()]
    raise AssertionError('unclosed method')


sources = {p: read(p) for p in MODEL.glob('*.cs')}
session_path = MODEL / 'ConnectedExpeditionSession.cs'
session = sources[session_path]
methods = {}
for path, text in sources.items():
    for match in re.finditer(r'(?:public|internal|private)\s+TestOnlySharedWorldPolicy\s+(Enable\w+)\s*\(', text):
        brace = text.find('{', match.end())
        arrow = text.find('=>', match.end())
        if arrow >= 0 and arrow < brace:
            body = text[match.start():text.index(';', arrow)+1]
            implementation = body[body.index('=>'):]
        else:
            assert brace >= 0
            body = text[match.start():brace] + block(text, brace)
            implementation = body[body.index('{'):]
        name = match.group(1)
        declaration = {'source': path.relative_to(ROOT).as_posix(),
                         'line': text[:match.start()].count('\n') + 1,
                         'normalizedMethodSha256': hashlib.sha256(body.encode('utf-8')).hexdigest()}
        entry = methods.setdefault(name, {'declarations': [], 'calls': []})
        entry['declarations'].append(declaration)
        entry['calls'] = sorted(set(entry['calls']) | set(re.findall(r'\b(Enable\w+)\s*\(', implementation)))


def closure(roots):
    result = set()
    pending = list(roots)
    while pending:
        name = pending.pop()
        if name in result: continue
        assert name in methods, name
        result.add(name)
        pending.extend(methods[name]['calls'])
    return sorted(result)


base = re.search(r'private static TestOnlySharedWorldPolicy ExpeditionPolicy\(\)\s*=>[\s\S]*?;', session).group()
base_direct = re.findall(r'\b(Enable\w+)\s*\(', base)
base_closure = closure(base_direct)
inventory = json.loads(read(OUT / 'OPERATION_INVENTORY.json'))
universe = {x['kind'] for x in inventory['operations']}


def region(begin, end):
    return session[session.index(begin):session.index(end, session.index(begin))]


def kinds(text):
    return set(re.findall(r'CommandKind\.(\w+)', text))


helper_paths = set()
def helper(path, method):
    helper_paths.add(path.relative_to(ROOT).as_posix())
    expression = re.search(r'(?:public|internal) static bool ' + re.escape(method)
                           + r'\(CommandKind kind\)\s*=>[^;]+;', read(path))
    assert expression, (path, method)
    return kinds(expression.group())


combat = kinds(region('private static readonly CommandKind[] CombatCommands', 'private static readonly IReadOnlyDictionary'))
party = kinds(region('private static readonly IReadOnlyDictionary', 'private static SupplyCacheRecord ReachableCache'))
assert len(combat) == 7
short = helper(CORE/'ShortRestRecord.cs', 'IsCommand')
repertoire = helper(CORE/'SpellRepertoireRecords.cs', 'IsCommand')
utilities = helper(CORE/'SpellCastingProfile.cs', 'IsUtilityCommand')
long_rest = helper(CORE/'ClericLongRestValidation.cs', 'IsCommand')
wound = helper(CORE/'WoundTreatmentRecord.cs', 'IsCommand')
fill = helper(MODEL/'TestOnlyFillingPolicy.cs', 'IsWaterFillCommand')
work_text = read(MODEL/'ConnectedWorkControlHost.cs')
work = fill | kinds(re.search(r'private static bool WorkControlCommand\(CommandKind kind\)\s*=>[^;]+;', work_text).group())
wire = dict(zip('Start StartWithCarriedVial StartWithStowedVial StartWithTacticalVial StartWithCompanionDose StartWithCompanionStabilization StartWithWoundTreatment StartWithConsumeDecay StartWithShortRest StartWithFleshWarden StartWithClericCompanion StartWithClericRepertoire StartWithFrightened StartWithClericSettlement StartWithClericCasting StartWithClericLongRest StartWithPostRecoveryEncounter StartWithBishopEntry StartWithDeclaredGeometry StartWithFerryWraith StartWithConsecration StartWithOrdinaryMagicalActivity'.split(), range(95,117)))
wire.update(StartWithFishingTrap=95, StartWithConnectedWorkControl=116)
rows = []
for item in inventory['factories']:
    factory, declaration = item['id'], item['exactDeclaration']
    assert declaration in session
    direct = re.findall(r'\b(Enable\w+)\s*\(', declaration)
    selected = closure(direct)
    enabled = set(base_closure + selected)
    def has(suffix): return 'Enable' + suffix in enabled
    player = combat | party
    if has('ConnectedWorkControl'): player |= work
    if has('FerryWraith'): player |= {'EncounterDash','TearExposedSeal'}
    if has('DeclaredGeometry'): player |= {'SuspendWorldStep','ResumeWorldStep'}
    if has('ConnectedClericRepertoire'): player |= repertoire
    if has('ConnectedClericCasting'): player |= utilities | {'EquipPortableItem','RemovePortableItem','HandleVessel'}
    if has('ConnectedClericSettlement'): player |= {'AwardCharacterMilestone','AdvanceCharacterLevel'}
    if has('ConnectedCompanionDose') or has('ConnectedCleric'): player |= {'BeginReinforcementApproach'}
    if has('ConnectedCleric'): player |= {'UseHealingRite'} | short
    if has('Consecration'): player |= {'UseConsecrate'}
    if has('BishopEntry'): player |= {'UseDivineInvocation'}
    if has('ConnectedClericLongRest'): player |= long_rest | {'ResolveExpeditionStrainRecovery'}
    if has('ConnectedCompanionStabilization') or has('ConnectedClericCasting'): player |= {'StabilizeCompanion'}
    if has('ConnectedWoundTreatment'): player |= wound
    if has('ConnectedConsumeDecay'): player |= {'ConsumeDecay'}
    if has('ConnectedShortRest'): player |= short
    recovery = combat | ({'UseIntimidatingPresence','RespondSanctuary'} if has('PostRecoveryEncounter') else set())
    ferry = combat | ({'AttackCreatureFeature','RespondSanctuary'} if has('FerryWraith') else set())
    assert player | recovery | ferry <= universe
    selected_consent = 'caller companionConsents/directorAuthorizes' if 'bool companionConsents' in declaration or 'bool companionConsents=' in declaration else 'not a public selection'
    caveats = [
        'Exposed kind is only the first host gate; actor/seat enablement, payload, fresh known target, core authority and native context still apply.',
        'Common base fixes reinforcement and earlier physical reengagement authorizations; selected later encounter flags do not replace them.',
        'Ordinary observation and cache work have actual stage/position gates; no currently hidden target is a discovery entitlement.',
        'Actual policy/root and records identify the setup; wire/prefix alone cannot authorize capabilities.'
    ]
    if not has('ConnectedFishingTrap'): caveats.append('Fishing Trap Interact branches fail KnownTrapInteraction: no trap records in this factory.')
    if has('ConnectedCleric'):
        caveats += ['Cleric selection accepts only authored scores 10,10,10,10,14,10; medicine/religion; exact selected cards; Club. Alternate builds are constructor rejection.',
                    'This Cleric chain does not inherit the carried/stowed/tactical/Companion-dose or noncasting care chain.',
                    'BeginShortRest reaches native ClassRecoveryUnsupported; InterruptShortRest and BeginMutationShortRest fail host KnownTarget. Initial Consecrate ownership does not admit its producer.']
    elif has('ConnectedShortRest') and not has('ConnectedFleshWarden'):
        caveats.append('BeginMutationShortRest is kind-exposed but fails KnownTarget without ConnectedFleshWarden.')
    if has('ConnectedClericRepertoire'):
        caveats.append('Only fixed initial 3 rank-0 / 2 rank-1 spell selection; AcquireEarnedSpell remains explicit native transaction-only/unavailable denial.')
        if not has('ConnectedClericCasting'): caveats.append('CastKnownSpell remains OrdinarySpellcastingUnsupported; knowledge is not casting coverage.')
    if has('ConnectedClericLongRest'): caveats.append('Long rest needs actual earned Cleric 2 and settled closure; profile selection alone is insufficient.')
    if has('BishopEntry'): caveats.append('Bishop declaration does not award rank 3; Invocation/Dispel need the actual earned advancement.')
    if has('ConnectedClericCasting'): caveats.append('Casting stabilization targets Hero-to-Companion in the selected original reinforced encounter, not arbitrary Recovery/Ferry encounters.')
    if has('ConnectedWorkControl'): caveats.append('KnownWorkControlTarget overrides KnownServices for these 16 kinds: observed mining, selected Companion research/recipe, actual owned jobs.')
    rows.append({'factory':factory,'source':item['source'],'line':item['line'],'exactDeclaration':declaration,
                 'explicitEnableCalls':direct,'transitiveSelectedEnables':selected,'commonBaseEnables':'commonBase.transitiveEnables',
                 'inMemorySchema':90,'wireEnvelope':wire[factory],
                 'selectedParameterBinding':{'publicConsentArguments':selected_consent,
                     'recoveryEncounterConsent':('fixed true/true via EnableBishopEntry defaults' if has('FerryWraith') else 'caller arguments' if has('PostRecoveryEncounter') else 'not selected'),
                     'ferryEncounterConsent':'caller arguments' if has('FerryWraith') else 'not selected'},
                 'kindGateCandidates':{'Player':sorted(player),'FirstOpponent':sorted(combat),'RecoveryOpponent':sorted(recovery),'FerryOpponent':sorted(ferry)},
                 'seatExistenceAndFreshContext':{'FirstOpponent':'actual first encounter','RecoveryOpponent':'selected recovery record + active recovery encounter','FerryOpponent':'selected Ferry record + active Ferry encounter'},
                 'nativeTargetPayloadCaveats':caveats,
                 'fullOperationPayloadClauseWitnessMatrix':'OPEN; this artifact closes bounded inheritance and static kind-gate audit only',
                 'executed':False})

assert len(rows)==24 and set(wire)=={x['factory'] for x in rows}
assert set().union(*(set(v) for row in rows for v in row['kindGateCandidates'].values()))==universe
used = set(base_closure) | set().union(*(set(x['transitiveSelectedEnables']) for x in rows))
pins = {d['source'] for x in used for d in methods[x]['declarations']} | helper_paths | {session_path.relative_to(ROOT).as_posix(),
    'engine/com.decennium.foundation/Laboratory/Model/VerifiedSharedWorldCheckpoint.cs',
    'engine/com.decennium.foundation/Laboratory/Model/ConnectedWorkControlHost.cs',
    'engine/com.decennium.foundation/Laboratory/Model/SharedCraftingConsequences.cs',
    'engine/com.decennium.foundation/Runtime/Core/Simulation.cs',
    'engine/com.decennium.foundation/Runtime/Core/SpellRepertoireRecords.cs'}
write('PROFILE_ADMISSION_MATRIX.json', {'schemaVersion':1,'baseline':BASELINE,
    'status':'BOUNDED_STATIC_INHERITANCE_AND_KIND_GATE_AUDIT; FULL_NATIVE_MATRIX_OPEN',
    'notQualification':'No simulation, construction, gameplay, tests or build executed. Candidate sets are not executable permission sets.',
    'reviewer':'/root/review_consecration; bounded inheritance findings independently reviewed against source; generated expanded kind matrix still requires review',
    'commonBase':{'source':session_path.relative_to(ROOT).as_posix(),'line':170,'exactDeclaration':base,'directEnables':base_direct,'transitiveEnables':base_closure},
    'factories':rows,'enableMethods':{x:methods[x] for x in sorted(used)},
    'sourcePins':[{'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in sorted(pins)]})
print(json.dumps({'factories':len(rows),'candidateUnion':len(universe),'enableMethods':len(used),'sourcePins':len(pins),'runtimeExecuted':False}))
