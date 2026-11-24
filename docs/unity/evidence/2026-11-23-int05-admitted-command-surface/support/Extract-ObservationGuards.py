"""Share exact ordinary and tactical observation guards, preserving source origins."""
import re
import runpy
import subprocess
from pathlib import Path

h = runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
root = h['ROOT']; extract = h['extract']; lab = 'engine/com.decennium.foundation/Laboratory/Model/'

def baseline(path):
    return subprocess.check_output(['git', 'show', h['BASE']+':'+path], cwd=root).decode().replace('\r\n','\n')

def replace(path, old, new):
    p=root/path; raw=p.read_bytes(); eol='\r\n' if raw.count(b'\n')==raw.count(b'\r\n') else '\n'
    current=p.read_text(encoding='utf8'); assert current.count(old)==1, (path,old)
    p.write_bytes(current.replace(old,new,1).replace('\n',eol).encode())

configs = [
    ('SharedExplorationSearch.cs', 'private string AssessExplorationSearch(Snapshot state, Command command, out WorldActivityIntervalRecord activity)', '        private string BeginExplorationSearch(', 'ExplorationSearchConstraintV1', 'state, command, out activity'),
    ('SharedExplorationSearch.cs', 'private static string AssessCancelExplorationSearch(Snapshot state, Command command)', '        private static string CancelExplorationSearch(', 'CancelExplorationSearchConstraintV1', 'state, command'),
    ('SharedExplorationHide.cs', 'private string AssessExplorationHide(Snapshot state, Command command, out WorldIntervalRecord interval,\n            out ExplorationSearchCell anchor, out RuleTime due)', '        private string BeginExplorationHide(', 'ExplorationHideConstraintV1', 'state, command, out interval, out anchor, out due'),
    ('SharedExplorationHide.cs', 'private string AssessCancelExplorationHide(Snapshot state, Command command)', '        private string CancelExplorationHide(', 'CancelExplorationHideConstraintV1', 'state, command'),
    ('SharedObservationActions.cs', 'private string AssessObservationAction(Snapshot s, Command c, out WorldIntervalRecord interval)', '        /// <summary>Pure public Search-request', 'ObservationActionConstraintV1', 's, c, out interval'),
    ('SharedObservationActions.cs', 'private string AssessSearchRequest(Snapshot s, Command c, out ObservationPoint candidateCell)', '        private CommandQueryResult QueryObservationSearchCommand(', 'SearchRequestConstraintV1', 's, c, out candidateCell'),
]
for file, signature, end, name, args in configs:
    path=lab+file; source=baseline(path); start='        '+signature
    a=source.index(start); b=source.index(end,a); fragment=source[a:b]
    oldname=signature.split('string ')[1].split('(')[0]; edits=[]
    for m in re.finditer(r'([?:]\s*)"([A-Z][A-Za-z0-9]+)"',fragment):
        line=source[:a+m.start()].count('\n')+1
        edits.append((m[0],m[1]+'new NativeCommandConstraintV1("'+m[2]+'", "'+path+'", '+str(line)+')'))
    extract(path,start,end,name,start.replace('string '+oldname,'NativeCommandConstraintV1 '+name),
        start+'\n            => '+name+'('+args+')?.NativeCode;\n\n',edits)

path=lab+'SharedObservationActions.cs'; source=baseline(path)
a=source.index('        private string ResolveHide('); b=source.index('        private static int HideModifier(',a)
original=source[a:b]
prefix=original[:original.index('            if(assessOnly)return null;\n            modifier=')]
no_observer_a=prefix.index('            if (observers.Length == 0)')
no_observer_b=prefix.index('            int modifier =',no_observer_a)
prefix=prefix[:no_observer_a]+'            if (observers.Length == 0) return null;\n\n'+prefix[no_observer_b:]
prefix=prefix.replace('private string ResolveHide(Snapshot s, Command c, bool assessOnly=false)',
    'private NativeCommandConstraintV1 HideConstraintV1(Snapshot s, Command c, out ActorState selectedActor,\n            out ObservationPoint selectedPosition, out ActorState[] selectedObservers, out int selectedModifier, out int selectedDisadvantage,\n            out (string Actor, ObservationPoint Position, int Dc)[] selectedObserverFacts)')
# The native Actor record type is filled from the source model, not guessed at runtime.
prefix=prefix.replace('        {\n','        {\n            selectedActor=null; selectedPosition=default; selectedObservers=null; selectedModifier=0; selectedDisadvantage=0; selectedObserverFacts=null;\n',1)
prefix=prefix.replace('            if (observers.Length == 0) return null;',
    '            selectedActor=actor; selectedPosition=position; selectedObservers=observers;\n            if (observers.Length == 0) return null;')
# Remove execution-record identity calculations from the read-only prefix.
identity='''            long revision = s.Revision + 1;
            string attemptId = "observation." + revision.ToString(System.Globalization.CultureInfo.InvariantCulture) + ".hide";
            RuleTime at = s.RuleClock;
'''
assert identity in prefix; prefix=prefix.replace(identity,'')
for code in re.findall(r'return "([A-Za-z][A-Za-z0-9]+)";',prefix):
    hit='return "'+code+'";'; line=source[:source.index(hit,a)].count('\n')+1
    prefix=prefix.replace(hit,'return new NativeCommandConstraintV1("'+code+'", "'+path+'", '+str(line)+');')
prefix+='            selectedModifier=modifier; selectedDisadvantage=disadvantage; selectedObserverFacts=observerFacts;\n            return null;\n        }\n\n'
execution='''        private string ResolveHide(Snapshot s, Command c, bool assessOnly=false)
        {
            var failure=HideConstraintV1(s,c,out var actor,out var position,out var observers,
                out var modifier,out var disadvantage,out var observerFacts);
            if(failure!=null)return failure.NativeCode;
            if(assessOnly)return null;
'''+identity
execution+=original[original.index('            if (observers.Length == 0)'):original.index('            int modifier =')].replace('                if(assessOnly)return null;\n','')
execution+=original[original.index('            modifier=checked(modifier+ConsumeGuidance'):]
replace(path,original,prefix+execution)
