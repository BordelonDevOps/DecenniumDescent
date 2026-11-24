"""Share mining initial checks; no work, rolls, claims or hidden result publication."""
from pathlib import Path
import re,runpy,subprocess
h=runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
path='engine/com.decennium.foundation/Laboratory/Model/SharedMining.cs'
source=subprocess.check_output(['git','show',h['BASE']+':'+path],cwd=h['ROOT']).decode().replace('\r\n','\n')
for name,end,args in [
 ('MiningAccess','        private string MiningAssistantAccess(', 's,actor,deposit,exceptJob,selectedUnitIds'),
 ('MiningAssistantAccess','        private bool Recipe347MiningToolPhysicallyEligible(', 's,actor,deposit,exceptJob'),
 ('AssessMiningCommand','        private string ResolveMining(', 's,c,out facts')]:
 a=source.index('        private string '+name+'(');brace=source.index('{',a);sig=source[a:brace].rstrip();part=source[a:source.index(end,a)]
 edits=[]
 if name=='AssessMiningCommand':
  for dep in ['MiningAccess','MiningAssistantAccess']:
   edits.extend([(dep+'(',dep+'ConstraintV1(')]*part.count(dep+'('))
  for variable in ['access','assistantAccess','resumeAccess']:
   edits.extend([('string '+variable+'=','var '+variable+'=')]*part.count('string '+variable+'='))
 h['extract'](path,sig,end,name+'ConstraintV1',sig.replace('string '+name,'NativeCommandConstraintV1 '+name+'ConstraintV1'),
   sig+'\n            => '+name+'ConstraintV1('+args+')?.NativeCode;\n\n',edits)
p=h['ROOT']/'engine/com.decennium.foundation/Laboratory/Model/SharedCommandAssessmentV1.cs';s=p.read_text()
s=s.replace('|| ManufacturingCommand(kind) || FormulaCommand(kind)', '|| miningFixture!=null && (kind==CommandKind.StartMining || kind==CommandKind.PauseMining || kind==CommandKind.ResumeMining)\n                || ManufacturingCommand(kind) || FormulaCommand(kind)',1)
s=s.replace('                case CommandKind.StartManufacturing:', '''                case CommandKind.StartMining:
                case CommandKind.PauseMining:
                case CommandKind.ResumeMining:
                    return BeforeWorkBranchConstraintV1(current,command) ?? AssessMiningCommandConstraintV1(current,command,out _);
                case CommandKind.StartManufacturing:''',1)
s=s.replace('formula and manufacturing commands','selected mining, formula and manufacturing commands');p.write_text(s,newline='\n')
print('Selected mining initial routing complete; missing-profile native fallback remains separate.')
