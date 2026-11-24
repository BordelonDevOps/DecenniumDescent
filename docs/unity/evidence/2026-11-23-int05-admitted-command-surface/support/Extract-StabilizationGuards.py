"""Share stabilization guards and the non-dispatch prefix at its native position."""
import re
import runpy
import subprocess
from pathlib import Path

h = runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
extract = h['extract']; root = h['ROOT']; lab = 'engine/com.decennium.foundation/Laboratory/Model/'
def baseline(path):
    return subprocess.check_output(['git', 'show', h['BASE'] + ':' + path], cwd=root).decode().replace('\r\n', '\n')
def replace(path, old, new):
    p = root / path; raw = p.read_bytes(); eol = '\r\n' if raw.count(b'\n') and raw.count(b'\r\n') == raw.count(b'\n') else '\n'
    current = p.read_text(encoding='utf8'); assert current.count(old) == 1, path
    p.write_bytes(current.replace(old, new, 1).replace('\n', eol).encode())
def typed(path, source, fragment):
    first = source[:source.index(fragment)].count('\n') + 1
    return ''.join(re.sub(r'return "([A-Za-z][A-Za-z0-9]+)";',
        lambda m: 'return new NativeCommandConstraintV1("'+m[1]+'", "'+path+'", '+str(first+i)+');', line)
        for i, line in enumerate(fragment.splitlines(keepends=True)))

configs = [
    ('SharedExplorationSearch.cs', 'private static string SearchActivityConflict(Snapshot state, Command command)', '\n    }\n}', 'SearchActivityConstraintV1', 'state, command'),
    ('SharedExplorationHide.cs', 'private static string HideActivityConflict(Snapshot state, Command command)', '        private static void RecordHideRelocation(', 'HideActivityConstraintV1', 'state, command'),
    ('SharedRetreat.cs', 'private static string RetreatHostileAttackFailure(Snapshot s, Command c)', '        private static void ReconcileRetreat(', 'RetreatHostileAttackConstraintV1', 's, c'),
    ('SharedStrainRecovery.cs', 'private string PendingRecoveryChoiceFailure(Snapshot s, Command c)', '        private string RecordProvisioningGateUpdates(', 'PendingRecoveryChoiceConstraintV1', 's, c'),
    ('SharedHavenCare.cs', 'private string HavenCareActorCommandFailure(Snapshot s, Command c)', '        private bool IsHavenCarePatient(', 'HavenCareActorConstraintV1', 's, c'),
    ('SharedMoraleRest.cs', 'private string MoraleRestingActorCommandFailure(Snapshot s, Command c)', '        private string AssessMoraleRestCommand(', 'MoraleRestingActorConstraintV1', 's, c'),
    ('SharedRestDebt.cs', 'private string RestingActorCommandFailure(Snapshot s, Command c)', '        private RuleTime WatchStart(', 'RestingActorConstraintV1', 's, c'),
]
for file, signature, end, name, args in configs:
    path = lab + file; source = baseline(path); start = '        ' + signature
    a = source.index(start); b = source.index(end, a); fragment = source[a:b]
    old_name = signature.split('string ')[1].split('(')[0]
    edits = []
    for m in re.finditer(r'([?:]\s*)"([A-Z][A-Za-z0-9]+)"', fragment):
        line = source[:a+m.start()].count('\n') + 1
        edits.append((m[0], m[1]+'new NativeCommandConstraintV1("'+m[2]+'", "'+path+'", '+str(line)+')'))
    extract(path, start, end, name, start.replace('string '+old_name, 'NativeCommandConstraintV1 '+name),
        start+'\n            => '+name+'('+args+')?.NativeCode;\n\n', edits)

path = lab + 'TestOnlySharedWorldPolicy.cs'; source = baseline(path)
a = source.index('            if (s.ConnectedWoundTreatment && WoundTreatmentStation.IsStationId(c.Target))')
b = source.index('            var searchActivityConflict', a); guards = source[a:b]
replace(path, guards, '            var woundOuter = WoundTreatmentOuterConstraintV1(s, c);\n'
    '            if (woundOuter != null) return woundOuter.NativeCode;\n')
helper = '        private static NativeCommandConstraintV1 WoundTreatmentOuterConstraintV1(Snapshot s, Command c)\n        {\n' \
    + typed(path, source, guards) + '            return null;\n        }\n\n'
assessment = lab + 'SharedCommandAssessmentV1.cs'
anchor = '        private static NativeCommandConstraintV1 ClassRecoveryConstraintV1(Snapshot s, Command c)'
replace(assessment, anchor, helper+anchor)

path = lab + 'SharedCompanionStabilization.cs'; source = baseline(path)
a = source.index('        private string ResolveCompanionStabilization(')
b = source.index('            if(assessOnly)return null;', a)
opening = source[a:b]
pure = typed(path, source, opening).replace('private string ResolveCompanionStabilization(Snapshot state, Command command,bool assessOnly=false)',
    'private NativeCommandConstraintV1 CompanionStabilizationConstraintV1(Snapshot state, Command command)', 1)
pure += '            return null;\n        }\n\n'
execution = '''        private string ResolveCompanionStabilization(Snapshot state, Command command,bool assessOnly=false)
        {
            var failure = CompanionStabilizationConstraintV1(state, command);
            if (failure != null) return failure.NativeCode;
'''
replace(path, opening, pure+execution)
anchor = '            if(assessOnly)return null;\n'
replace(path, anchor, anchor+'''            var interval = Interval(state, command.Actor);
            var actor = state.Actors.Single(x => x.Id == command.Actor);
            var patient = state.Actors.Single(x => x.Id == command.Target);
            var before = state.Lives.Single(x => x.ActorId == patient.Id);
''')
