"""Share filling admission and ordinary management gates without reservations or time."""
from pathlib import Path
import re,runpy,subprocess
h=runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
b='engine/com.decennium.foundation/Laboratory/Model/'
for file,name,end,args,deps in [
 ('WaterFilling.cs','CarryAfterTransfer','        internal static string Prerequisite(', 's,actor,source,destination,amount',[]),
 ('WaterFilling.cs','Prerequisite','        private static void Replace(', 's,actor,source,destination,amount,existingJob',['CarryAfterTransfer']),
 ('TestOnlyFillingPolicy.cs','FillRecordCapacity','        public string Resolve(', 's,starting',[]),
 ('TestOnlyFillingPolicy.cs','AssessWaterFill','        private static string FillRecordCapacity(', 's,c,out job',['WaterFilling.Prerequisite','FillRecordCapacity'])]:
 path=b+file;source=subprocess.check_output(['git','show',h['BASE']+':'+path],cwd=h['ROOT']).decode().replace('\r\n','\n')
 a=source.index('string '+name+'(');a=source.rfind('\n',0,a)+1;brace=source.index('{',a);sig=source[a:brace].rstrip();part=source[a:source.index(end,a)]
 edits=[]
 for m in re.finditer(r'([?:]\s*)"([A-Z][A-Za-z0-9]+)"',part):
  edits.append((m[0],m[1]+'new NativeCommandConstraintV1("'+m[2]+'", "'+path+'", '+str(source[:a+m.start()].count('\n')+1)+')'))
 for dep in deps:edits.extend([(dep+'(',dep+'ConstraintV1(')]*part.count(dep+'('))
 for v in ['carrying','error']:edits.extend([('string '+v+'=','var '+v+'=')]*part.count('string '+v+'='))
 h['extract'](path,sig,end,name+'ConstraintV1',sig.replace('string '+name,'NativeCommandConstraintV1 '+name+'ConstraintV1'),
  sig+'\n            => '+name+'ConstraintV1('+args+')?.NativeCode;\n\n',edits)
path=b+'TestOnlySharedWorldPolicy.cs';p=h['ROOT']/path;s=p.read_text();source=subprocess.check_output(['git','show',h['BASE']+':'+path],cwd=h['ROOT']).decode().replace('\r\n','\n')
a=source.index('            // None of these procedures may authorize access using a stale integer grid anchor.');z=source.index('            // Handling has its own one-second synchronous cost.',a);block=source[a:z]
typed=''.join(re.sub(r'return "([A-Za-z0-9]+)";',lambda m:'return new NativeCommandConstraintV1("'+m[1]+'", "'+path+'", '+str(source[:a].count('\n')+i+1)+');',line) for i,line in enumerate(block.splitlines(keepends=True)))
assert block in s;s=s.replace(block,'            var managementFailure=OrdinaryManagementConstraintV1(s,c);\n            if(managementFailure!=null)return managementFailure.NativeCode;\n',1)
def origin(code):return str(source[:source.index('return "'+code+'"',source.index('private string ResolveCore'))].count('\n')+1)
s=s.replace('if (c.Combat != null) return "SharedCombatHandoffNotImplemented";', 'if (c.Combat != null) return SharedUnimplementedConstraintV1(c).NativeCode;',1)
s=s.replace('if (!management) return "SharedCommandNotImplemented";','if (!management) return SharedUnimplementedConstraintV1(c).NativeCode;',1);p.write_text(s,newline='\n')
p=h['ROOT']/(b+'SharedCommandAssessmentV1.cs');s=p.read_text();i=s.index('        private NativeCommandConstraintV1 WorldOpeningConstraintV1(')
s=s[:i]+'''        private NativeCommandConstraintV1 OrdinaryManagementConstraintV1(Snapshot s,Command c)
        {
'''+typed+'''            return null;
        }

        private static NativeCommandConstraintV1 SharedUnimplementedConstraintV1(Command c)
            => c.Combat!=null
                ?new NativeCommandConstraintV1("SharedCombatHandoffNotImplemented", "'''+path+'", '+origin('SharedCombatHandoffNotImplemented')+''')
                :new NativeCommandConstraintV1("SharedCommandNotImplemented", "'''+path+'", '+origin('SharedCommandNotImplemented')+''');

        private NativeCommandConstraintV1 UnimplementedBranchConstraintV1(Snapshot s,Command c)
            => connectedCombat!=null && s.InventoryCombat ? UnimplementedCalendarConstraintV1(s,c)
                : SharedUnimplementedConstraintV1(c);

        private NativeCommandConstraintV1 WaterFillBranchConstraintV1(Snapshot s,Command c)
        {
            var failure=BeforeWorkBranchConstraintV1(s,c);
            if(failure!=null)return failure;
            if(connectedCombat!=null && s.InventoryCombat)return UnimplementedCalendarConstraintV1(s,c);
            if(c.Combat!=null)return SharedUnimplementedConstraintV1(c);
            return OrdinaryManagementConstraintV1(s,c) ?? inventory.AssessWaterFillConstraintV1(s,c,out _);
        }

'''+s[i:]
s=s.replace('|| kind == CommandKind.CancelExplorationSearch && explorationSearchDefinition != null','|| kind == CommandKind.CancelExplorationSearch',1)
s=s.replace('|| miningFixture!=null && (kind==CommandKind.StartMining || kind==CommandKind.PauseMining || kind==CommandKind.ResumeMining)','|| TestOnlyFillingPolicy.IsWaterFillCommand(kind)\n                || kind==CommandKind.StartMining || kind==CommandKind.PauseMining || kind==CommandKind.ResumeMining',1)
s=s.replace('return BeforeWorkBranchConstraintV1(current,command) ?? AssessMiningCommandConstraintV1(current,command,out _);','return BeforeWorkBranchConstraintV1(current,command) ?? (IsMiningCommand(command)\n                        ?AssessMiningCommandConstraintV1(current,command,out _):UnimplementedBranchConstraintV1(current,command));',1)
s=s.replace('                case CommandKind.StartMining:', '''                case CommandKind.StartWaterFill:
                case CommandKind.PauseWaterFill:
                case CommandKind.ResumeWaterFill:
                case CommandKind.CancelWaterFill:
                    return WaterFillBranchConstraintV1(current,command);
                case CommandKind.StartMining:''',1)
anchor='            if (current.ExplorationSearch != null && command.Kind == CommandKind.CancelExplorationSearch)'
s=s.replace(anchor,'''            if(current.ExplorationSearch==null && command.Kind==CommandKind.CancelExplorationSearch)
                return BeforeWorkBranchConstraintV1(current,command) ?? UnimplementedBranchConstraintV1(current,command);
'''+anchor,1)
p.write_text(s,newline='\n')
print('Filling, missing search and missing mining native routes wired.')
