"""One-time exact prefix extraction. Candidate records and payment stay execution-only."""
import re
import runpy
import subprocess
from pathlib import Path

h=runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
extract=h['extract']; root=h['ROOT']; lab='engine/com.decennium.foundation/Laboratory/Model/'

def baseline(path):
 return subprocess.check_output(['git','show',h['BASE']+':'+path],cwd=root).decode('utf8').replace('\r\n','\n')
def typed(source,fragment,path):
 at=source.index(fragment);first=source[:at].count('\n')+1
 return ''.join(re.sub(r'return "([A-Za-z][A-Za-z0-9]+)";',
  lambda m:'return new NativeCommandConstraintV1("'+m[1]+'", "'+path+'", '+str(first+i)+');',line)
  for i,line in enumerate(fragment.splitlines(keepends=True)))
def replace_native(path,old,new):
 p=root/path;current=p.read_text(encoding='utf8');assert current.count(old)==1,path
 p.write_bytes(current.replace(old,new,1).encode('utf8'))
def constraint(source,path,guard,code):
 a=source.index(guard);at=source.index('return "'+code+'";',a)
 return 'new NativeCommandConstraintV1("'+code+'", "'+path+'", '+str(source[:at].count('\n')+1)+')'

extract(lab+'SharedShortRest.cs','        private string ShortRestAccess(Snapshot state, ShortRestRecord active)',
 '        private string ResolveShortRest(', 'ShortRestAccessConstraintV1',
 '        private NativeCommandConstraintV1 ShortRestAccessConstraintV1(Snapshot state, ShortRestRecord active)',
 '        private string ShortRestAccess(Snapshot state, ShortRestRecord active)\n            => ShortRestAccessConstraintV1(state, active)?.NativeCode;\n\n')
extract(lab+'SharedFleshWarden.cs','        private static string MutationRestAccess(Snapshot state, string mutation)',
 '        private static void AddMutationRestChoice(', 'MutationRestConstraintV1',
 '        private static NativeCommandConstraintV1 MutationRestConstraintV1(Snapshot state, string mutation)',
 '        private static string MutationRestAccess(Snapshot state, string mutation)\n            => MutationRestConstraintV1(state, mutation)?.NativeCode;\n\n')
extract(lab+'SharedWoundTreatment.cs','        private string WoundTreatmentAccess(Snapshot state, WoundTreatmentRecord active)',
 '        private string ResolveWoundTreatment(', 'WoundTreatmentAccessConstraintV1',
 '        private NativeCommandConstraintV1 WoundTreatmentAccessConstraintV1(Snapshot state, WoundTreatmentRecord active)',
 '        private string WoundTreatmentAccess(Snapshot state, WoundTreatmentRecord active)\n            => WoundTreatmentAccessConstraintV1(state, active)?.NativeCode;\n\n')

path=lab+'SharedShortRest.cs';source=baseline(path)
a=source.index('        private string ResolveShortRest(');b=source.index('        private void ReconcileShortRest(',a)
old=source[a:b];split=old.index('            var rest = new ShortRestRecord(')
opening=typed(source,old[:split],path).replace('private string ResolveShortRest','private NativeCommandConstraintV1 ShortRestOpeningConstraintV1',1)
opening=opening.replace('                EndShortRest(state, active, command, ShortRestInterruption.Explicit);\n','')
opening=opening.replace('string failure = MutationRestAccess(state, command.Target);','var failure = MutationRestConstraintV1(state, command.Target);')
opening=opening.replace('string access = ShortRestAccess(state, null);','var access = ShortRestAccessConstraintV1(state, null);')
opening+='            return null;\n        }\n\n'
window_start='            if (state.Work.WorkerIntervals.Any(x => x.WorkerId == command.Actor'
wa=old.index(window_start);wb=old.index('            state.Work = state.Work.Reserve(',wa)
window=old[wa:wb];origin=constraint(source,path,window_start,'ShortRestActorOccupied')
helpers='''        private static NativeCommandConstraintV1 ShortRestWindowConstraintV1(Snapshot state, string actor, RuleTime startedAt)
        {
            // Same lazy arithmetic as ShortRestRecord.DueAt inside the native overlap predicate.
            return state.Work.WorkerIntervals.Any(x => x.WorkerId == actor
                && x.Start < startedAt.AddSeconds(ShortRestBerth.DurationSeconds) && x.End > startedAt)
                ? ORIGIN : null;
        }

        private NativeCommandConstraintV1 ShortRestConstraintV1(Snapshot state, Command command)
        {
            var failure = ShortRestOpeningConstraintV1(state, command);
            return failure != null || command.Kind == CommandKind.InterruptShortRest ? failure
                : ShortRestWindowConstraintV1(state, command.Actor, state.RuleClock);
        }

'''.replace('ORIGIN',origin)
execute='''        private string ResolveShortRest(Snapshot state, Command command)
        {
            var failure = ShortRestOpeningConstraintV1(state, command);
            if (failure != null) return failure.NativeCode;
            if (command.Kind == CommandKind.InterruptShortRest) {
                EndShortRest(state, ShortRestBerth.Active(state), command, ShortRestInterruption.Explicit);
                return null;
            }
            bool mutation = command.Kind == CommandKind.BeginMutationShortRest;
'''+old[split:].replace(window,'''            var window = ShortRestWindowConstraintV1(state, command.Actor, rest.StartedAt);
            if (window != null) return window.NativeCode;
''',1)
replace_native(path,old,opening+helpers+execute)

path=lab+'SharedConsumeDecay.cs';source=baseline(path)
a=source.index('        private string ResolveConsumeDecay(');b=source.index('        private static RuleTime? NextConsumeDecayDeadline(',a)
old=source[a:b];split=old.index('            var life = state.Lives.Single(')
opening=typed(source,old[:split],path).replace('private string ResolveConsumeDecay','private NativeCommandConstraintV1 ConsumeDecayConstraintV1',1)
opening+='            return null;\n        }\n\n'
execute='''        private string ResolveConsumeDecay(Snapshot state, Command command)
        {
            var failure = ConsumeDecayConstraintV1(state, command);
            if (failure != null) return failure.NativeCode;
            var interval = Interval(state, command.Actor);
            var actor = state.Actors.Single(x => x.Id == command.Actor);
'''+old[split:]
replace_native(path,old,opening+execute)

path=lab+'SharedWoundTreatment.cs';source=baseline(path)
a=source.index('        private string ResolveWoundTreatment(');b=source.index('        private void ReconcileWoundTreatment(',a)
old=source[a:b];split=old.index('            var patient = state.Lives.Single(')
opening=typed(source,old[:split],path).replace('private string ResolveWoundTreatment','private NativeCommandConstraintV1 WoundTreatmentOpeningConstraintV1',1)
opening=opening.replace('                EndWoundTreatment(state, active, command, WoundTreatmentOutcome.Interrupted);\n','')
opening=opening.replace('var access = WoundTreatmentAccess(state, null);','var access = WoundTreatmentAccessConstraintV1(state, null);')
opening+='            return null;\n        }\n\n'
sa=old.index('            var inputs = new[]');sb=old.index('            if (state.Work.WorkerIntervals.Any',sa)
supplies=old[sa:sb]
supply_helper='''        private static NativeCommandConstraintV1 WoundTreatmentSupplyConstraintV1(Snapshot state, int basket, out ResourceLot[] inputs)
        {
'''+typed(source,supplies,path).replace('var inputs =','inputs =',1).replace('Stock(job.Basket)','Stock(basket)')+'            return null;\n        }\n\n'
wa=sb;wb=old.index('            var intervals = ',wa);window=old[wa:wb]
origin=constraint(source,path,window,'WoundTreatmentParticipantOccupied')
helpers='''        private static NativeCommandConstraintV1 WoundTreatmentWindowConstraintV1(Snapshot state, Command command, RuleTime startedAt)
        {
            // Same lazy arithmetic as WoundTreatmentRecord.DueAt; no candidate job or claims.
            return state.Work.WorkerIntervals.Any(x => (x.WorkerId == command.Actor || x.WorkerId == command.Target)
                && x.Start < startedAt.AddSeconds(WoundTreatmentStation.DurationSeconds) && x.End > startedAt)
                ? ORIGIN : null;
        }

        private NativeCommandConstraintV1 WoundTreatmentConstraintV1(Snapshot state, Command command)
        {
            var failure = WoundTreatmentOpeningConstraintV1(state, command);
            if (failure != null || command.Kind == CommandKind.InterruptWoundTreatment) return failure;
            return WoundTreatmentSupplyConstraintV1(state, state.WoundTreatments.Length, out _)
                ?? WoundTreatmentWindowConstraintV1(state, command, state.RuleClock);
        }

'''.replace('ORIGIN',origin)
execute='''        private string ResolveWoundTreatment(Snapshot state, Command command)
        {
            var failure = WoundTreatmentOpeningConstraintV1(state, command);
            if (failure != null) return failure.NativeCode;
            if (command.Kind == CommandKind.InterruptWoundTreatment) {
                EndWoundTreatment(state, WoundTreatmentStation.Active(state), command, WoundTreatmentOutcome.Interrupted);
                return null;
            }
'''+old[split:].replace(supplies,'''            var supply = WoundTreatmentSupplyConstraintV1(state, job.Basket, out var inputs);
            if (supply != null) return supply.NativeCode;
''',1).replace(window,'''            var window = WoundTreatmentWindowConstraintV1(state, command, job.StartedAt);
            if (window != null) return window.NativeCode;
''',1)
replace_native(path,old,opening+supply_helper+helpers+execute)
print('Extracted native prefixes; creation, reservations, payment and settlement remain in legacy execution.')
