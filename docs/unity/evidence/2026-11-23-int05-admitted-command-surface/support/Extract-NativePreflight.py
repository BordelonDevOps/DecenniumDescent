"""One-time exact guard extraction from the accepted native baseline; no rule rewriting."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = '67f3d201b202ab2f815ab69940682f04e78c511c'

def extract(path, start, end, name, signature, wrapper, edits=()):
    target=ROOT/path
    old=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT).decode('utf8').replace('\r\n','\n')
    current=target.read_text(encoding='utf8')
    a=old.index(start); b=old.index(end,a)
    method=old[a:b]
    assert method in current, ('native body differs',path,name)
    lines=method.splitlines(keepends=True)
    first=old[:a].count('\n')+1
    for i,line in enumerate(lines):
        line=re.sub(r'return "([A-Za-z][A-Za-z0-9]+)";',
            lambda m:'return new NativeCommandConstraintV1("'+m[1]+'", "'+path+'", '+str(first+i)+');',line)
        lines[i]=line
    updated=''.join(lines).replace(start,signature,1)
    for before,after in edits:
        assert before in updated, (path,before)
        updated=updated.replace(before,after,1)
    target.write_bytes(current.replace(method,wrapper+updated,1).encode('utf8'))
    print(path,name)

if __name__ == '__main__':
    core='engine/com.decennium.foundation/Runtime/Core/'
    extract(core+'SpellCastingProfile.cs',
        '        public static string PayloadFailure(Snapshot s, Command c)', '\n    }\n}',
        'PayloadConstraintV1','        internal static NativeCommandConstraintV1 PayloadConstraintV1(Snapshot s, Command c)',
        '        public static string PayloadFailure(Snapshot s, Command c)\n            => PayloadConstraintV1(s, c)?.NativeCode;\n\n')
    extract(core+'DivineInvocationRecords.cs',
        '        public static string InvocationPayloadFailure(Snapshot s,Command c)',
        '        public static bool QualifiesInvocationCure(',
        'InvocationPayloadConstraintV1','        internal static NativeCommandConstraintV1 InvocationPayloadConstraintV1(Snapshot s,Command c)',
        '        public static string InvocationPayloadFailure(Snapshot s,Command c)\n            => InvocationPayloadConstraintV1(s,c)?.NativeCode;\n\n',
        [('?"InvocationSelectionRequired":null','?new NativeCommandConstraintV1("InvocationSelectionRequired", "'+core+'DivineInvocationRecords.cs", 99):null'),
         ('?"UnexpectedInvocationPayload":null','?new NativeCommandConstraintV1("UnexpectedInvocationPayload", "'+core+'DivineInvocationRecords.cs", 105):null')])
    extract(core+'Simulation.cs',
        '        private string ValidateCommandAndAuthority(Authority authority, Command command)',
        '        private bool AcceptedClockAwaitingChoice(',
        'AssessCommandAndAuthorityV1','        private NativeCommandConstraintV1 AssessCommandAndAuthorityV1(Authority authority, Command command)',
        '        private string ValidateCommandAndAuthority(Authority authority, Command command)\n            => AssessCommandAndAuthorityV1(authority, command)?.NativeCode;\n\n',
        [('string invocationShape = BishopProfile.InvocationPayloadFailure(state,command);','var invocationShape = BishopProfile.InvocationPayloadConstraintV1(state,command);'),
         ('string spellShape = SpellCastingProfile.PayloadFailure(state, command);','var spellShape = SpellCastingProfile.PayloadConstraintV1(state, command);')])
    extract(core+'Simulation.cs',
        '        private string PreflightCommand(Authority authority, Command command, out CommandReceipt previous)',
        '        public CommandAdmission AssessCommandAdmission(',
        'AssessCommandAfterAuthorityV1','        private NativeCommandConstraintV1 AssessCommandAfterAuthorityV1(Authority authority, Command command, out CommandReceipt previous)',
        '        private string PreflightCommand(Authority authority, Command command, out CommandReceipt previous)\n        {\n            previous = null;\n            return (AssessCommandAndAuthorityV1(authority, command)\n                ?? AssessCommandAfterAuthorityV1(authority, command, out previous))?.NativeCode;\n        }\n\n',
        [('            string failure = ValidateCommandAndAuthority(authority, command);\n            if (failure != null) return failure;\n',''),
         ('? null : "CommandIdConflict"','? null : new NativeCommandConstraintV1("CommandIdConflict", "'+core+'Simulation.cs", 1563)')])
