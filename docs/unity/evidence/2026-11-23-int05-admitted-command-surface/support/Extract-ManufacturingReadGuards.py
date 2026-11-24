"""Extract manufacturing and vial admission without executing work or rolls."""
from pathlib import Path
import re,runpy,subprocess
h=runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
b='engine/com.decennium.foundation/Laboratory/Model/'
def old(file):return subprocess.check_output(['git','show',h['BASE']+':'+b+file],cwd=h['ROOT']).decode().replace('\r\n','\n')
def extract(file,name,end,args,deps=()):
 source=old(file);a=source.index('string '+name+'(');a=source.rfind('        private ',0,a);brace=source.index('{',a);signature=source[a:brace].rstrip();fragment=source[a:source.index(end,a)]
 edits=[]
 for m in re.finditer(r'([?:]\s*)"([A-Z][A-Za-z0-9]+)"',fragment):
  line=source[:a+m.start()].count('\n')+1
  edits.append((m[0],m[1]+'new NativeCommandConstraintV1("'+m[2]+'", "'+b+file+'", '+str(line)+')'))
 for dep in deps:
  edits.extend([(dep+'(',dep+'ConstraintV1(')]*fragment.count(dep+'('))
 for variable in ['access','specimenFailure']:
  if 'string '+variable+' =' in fragment:edits.append(('string '+variable+' =','var '+variable+' ='))
  if 'string '+variable+'=' in fragment:edits.append(('string '+variable+'=','var '+variable+'='))
 h['extract'](b+file,signature,end,name+'ConstraintV1',signature.replace('string '+name,'NativeCommandConstraintV1 '+name+'ConstraintV1'),
  signature+'\n            => '+name+'ConstraintV1('+args+')?.NativeCode;\n\n',edits)
extract('SharedManufacturing.cs','ManufacturingAccess','        private static void BookManufacturing(', 's,actor,window,checking,recipeId')
extract('SharedConnectedBloodSpecimen.cs','AssessBloodIngredient','        private IEnumerable<Command> DiscoverBloodTreatment(', 's,actor,lotId,recipe')
extract('SharedConnectedVial.cs','CompanionDoseDeliveryFailure','        private static void RegisterConnectedVial(', 'state,user,recipient')
extract('SharedManufacturing.cs','AssessManufacturingQualityChoice','        private CommandQueryResult QueryManufacturingControl(', 's,c,out current,out choice,out catalyst')
extract('SharedManufacturing.cs','AssessManufacturingControl','        private IEnumerable<string> ManufacturingOwners(', 's,c,out current',['ManufacturingAccess'])
extract('SharedManufacturing.cs','AssessManufacturingStart','        private string ResolveManufacturing(', 's,c,out recipe,specimenLotId',['ManufacturingAccess','AssessBloodIngredient'])
extract('SharedConnectedRecipe4Batch.cs','AssessConnectedRecipe4Start','        private bool IsConnectedRecipe4InjuryDispatch(', 's,c,out recipe',['AssessManufacturingStart'])
extract('SharedConnectedFormulaResearch.cs','AssessConnectedManufacturing','        private IEnumerable<Command> DiscoverConnectedFormulaWork(', 'state,command',['AssessManufacturingStart'])
# Above method also has a null-coalescing denial; preserve its original origin.
p=h['ROOT']/(b+'SharedConnectedFormulaResearch.cs');s=p.read_text();s=s.replace('AssessManufacturingStartConstraintV1(state, command, out _) ?? "ConnectedManufacturingNotSelected"',
 'AssessManufacturingStartConstraintV1(state, command, out _) ?? new NativeCommandConstraintV1("ConnectedManufacturingNotSelected", "'+b+'SharedConnectedFormulaResearch.cs", 72)');p.write_text(s,newline='\n')
source=old('SharedManufacturing.cs');p=h['ROOT']/(b+'SharedManufacturing.cs');s=p.read_text()
a=source.index('        private string UseAlchemy(');end=source.index('\n    }\n}',a);original=source[a:end]
split=original.index('            if(assessOnly)return null;');guard=original[:split]
guard=''.join(re.sub(r'return "([A-Za-z][A-Za-z0-9]+)";',lambda m:'return new NativeCommandConstraintV1("'+m[1]+'", "'+b+'SharedManufacturing.cs", '+str(source[:a].count('\n')+i+1)+');',line)
 for i,line in enumerate(guard.splitlines(keepends=True)))
guard=guard.replace('private string UseAlchemy(Snapshot s,Command c,bool assessOnly=false)',
 'private NativeCommandConstraintV1 AlchemyUseConstraintV1(Snapshot s,Command c,out AlchemyDoseRecord validatedDose,out ActorState validatedRecipient,out ActorLifeRecord beforeLife)')
guard=guard.replace('        {\n','        {\n            validatedDose=null;validatedRecipient=null;beforeLife=null;\n',1)
guard=guard.replace('string failure = CompanionDoseDeliveryFailure(', 'var failure = CompanionDoseDeliveryFailureConstraintV1(')
guard+='            validatedDose=dose;validatedRecipient=recipient;beforeLife=before;\n            return null;\n        }\n'
effects=original[split+len('            if(assessOnly)return null;\n'):]
execution='''        private string UseAlchemy(Snapshot s,Command c,bool assessOnly=false)
        {
            var failure=AlchemyUseConstraintV1(s,c,out var dose,out var recipient,out var before);
            if(failure!=null||assessOnly)return failure?.NativeCode;
'''+effects
assert original in s;s=s.replace(original,guard+'\n'+execution)
start=source.index('            if(manufacturing==null)return "ManufacturingNotSelected";',source.index('        private string ResolveManufacturing('));end=source.index('            if(c.Kind==CommandKind.StartManufacturing)',start)
prefix=source[start:end];typed=''.join(re.sub(r'return "([A-Za-z][A-Za-z0-9]+)";',lambda m:'return new NativeCommandConstraintV1("'+m[1]+'", "'+b+'SharedManufacturing.cs", '+str(source[:start].count('\n')+i+1)+');',line)
 for i,line in enumerate(prefix.splitlines(keepends=True)))
typed=typed.replace('return UseAlchemy(s,c,assessOnly)','return null')
method='''        private NativeCommandConstraintV1 ManufacturingPrefixConstraintV1(Snapshot s,Command c)
        {
'''+typed+'''            return null;
        }

'''
assert prefix in s;s=s.replace(prefix,'''            var initial=ManufacturingPrefixConstraintV1(s,c);
            if(initial!=null)return initial.NativeCode;
            if(c.Kind==CommandKind.UseAlchemyDose)return UseAlchemy(s,c,assessOnly);
''',1)
s=s.replace('        private string ResolveManufacturing(',method+'        private string ResolveManufacturing(',1)
p.write_text(s,newline='\n')
print('Manufacturing guards and vial effects split.')
