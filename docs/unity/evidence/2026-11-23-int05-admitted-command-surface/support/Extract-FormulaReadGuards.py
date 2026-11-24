"""Split formula admission from mutation, preserving original branch order and origins."""
from pathlib import Path
import re, runpy, subprocess
h=runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
base='engine/com.decennium.foundation/Laboratory/Model/'
def extract(name,file,end,args,edits=()):
    old=subprocess.check_output(['git','show',h['BASE']+':'+base+file],cwd=h['ROOT']).decode().replace('\r\n','\n')
    a=old.index('        private string '+name+'('); b=old.index('{',a); signature=old[a:b].rstrip()
    h['extract'](base+file,signature,end,name+'ConstraintV1',signature.replace('string '+name,'NativeCommandConstraintV1 '+name+'ConstraintV1'),
        signature+'\n            => '+name+'ConstraintV1('+args+')?.NativeCode;\n\n',edits)
extract('ResearchAccess','SharedFormulaResearch.cs','        private static void BookFormula(',
        's, actor, requireWindow, requiresPrimaryTool')
extract('ConnectedResearchAdmission','SharedConnectedFormulaResearch.cs','        private bool ConnectedResearchWorkshopAvailable(',
        'state, command', [('? null : "ConnectedResearchStageClosed"','? null : new NativeCommandConstraintV1("ConnectedResearchStageClosed", "'+base+'SharedConnectedFormulaResearch.cs", 56)')])
path=base+'SharedFormulaResearch.cs';p=h['ROOT']/path
source=subprocess.check_output(['git','show',h['BASE']+':'+path],cwd=h['ROOT']).decode().replace('\r\n','\n')
a=source.index('        private string ResolveFormulaWork(');end=source.index('\n    }\n}',a);original=source[a:end]
# Record every literal denial at its original occurrence before removing effects.
guard=''.join(re.sub(r'return "([A-Za-z][A-Za-z0-9]+)";',lambda m:'return new NativeCommandConstraintV1("'+m[1]+'", "'+path+'", '+str(source[:a].count('\n')+i+1)+');',line)
    for i,line in enumerate(original.splitlines(keepends=True)))
guard=guard.replace('private string ResolveFormulaWork(Snapshot s, Command c, bool assessOnly = false)',
    'private NativeCommandConstraintV1 FormulaWorkConstraintV1(Snapshot s, Command c, out string recipeId, out bool copy, out string method, out FormulaWorkRecord current)')
guard=guard.replace('        {\n','        {\n            recipeId = null; copy = false; method = null; current = null;\n',1)
guard=guard.replace('string failure = ConnectedResearchAdmission(', 'var failure = ConnectedResearchAdmissionConstraintV1(')
guard=guard.replace('string access = ResearchAccess(', 'var access = ResearchAccessConstraintV1(')
guard=guard.replace('string recipeId=','recipeId=').replace('bool copy =','copy =').replace('string method =','method =').replace('var current =','current =')
# Out parameters cannot be captured in LINQ; use ordinary local aliases.
guard=guard.replace('recipeId=SharedResearchFixture.RecipeForSelector(c.Y);','recipeId=SharedResearchFixture.RecipeForSelector(c.Y);\n                string selectedRecipeId=recipeId;')
guard=guard.replace('x.RecipeId==recipeId','x.RecipeId==selectedRecipeId')
guard=guard.replace('x.MethodId == method','x.MethodId == (copy ? "method.transcription" : c.X == 0 ? "method.sequence-analysis" : "method.independent-comparison")')
# The failure-evidence predicate only runs in the !copy branch; use c.Kind instead of capturing out copy.
guard=guard.replace('(copy ? "method.transcription" : c.X == 0 ? "method.sequence-analysis" : "method.independent-comparison")','(c.Kind == CommandKind.StartFormulaCopy ? "method.transcription" : c.X == 0 ? "method.sequence-analysis" : "method.independent-comparison")')
x=guard.index('                if (assessOnly) return null;');y=guard.index('\n            }',x)
guard=guard[:x]+'                return null;'+guard[y:]
guard=guard.replace('                if (!assessOnly) PauseFormula(s, current);\n','')
x=guard.index('                if (assessOnly) return null;');y=guard.index('\n            }',x)
guard=guard[:x]+'                return null;'+guard[y:]
x=guard.index('                if (assessOnly) return null;');y=guard.index('\n            }',x)
guard=guard[:x]+'                return null;'+guard[y:]
start_effects=original[original.index('                var prior ='):original.index('\n            }',original.index('                var prior ='))]
cancel_effects=original[original.index('                s.Work = s.Work.CancelFutureWork'):original.index('\n            }',original.index('                s.Work = s.Work.CancelFutureWork'))]
resume_effects=original[original.index('                if (current.Status == FormulaWorkStatus.AwaitingCheck) { FinishFormulaCheck'):original.index('\n            }',original.index('                if (current.Status == FormulaWorkStatus.AwaitingCheck) { FinishFormulaCheck'))]
execution='''        private string ResolveFormulaWork(Snapshot s, Command c, bool assessOnly = false)
        {
            var failure = FormulaWorkConstraintV1(s, c, out var recipeId, out bool copy, out var method, out var current);
            if (failure != null || assessOnly) return failure?.NativeCode;
            if (c.Kind == CommandKind.StartFormulaResearch || c.Kind == CommandKind.StartFormulaCopy) {
'''+start_effects+'''
            }
            if (c.Kind == CommandKind.PauseFormulaWork) { PauseFormula(s, current); return null; }
            if (c.Kind == CommandKind.CancelFormulaWork) {
'''+cancel_effects+'''
            }
            if (c.Kind == CommandKind.ResumeFormulaWork) {
'''+resume_effects+'''
            }
            throw new InvalidOperationException("Formula admission did not select an execution branch.");
        }
'''
current=p.read_text();assert original in current
p.write_text(current.replace(original,guard+'\n'+execution),newline='\n')
print('Shared formula admission and unchanged native effects extracted.')
