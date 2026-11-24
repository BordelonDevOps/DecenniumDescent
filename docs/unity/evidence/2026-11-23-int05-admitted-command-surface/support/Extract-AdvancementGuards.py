"""Share existing advancement prerequisites without creating future character state."""
import re
import runpy
import subprocess
from pathlib import Path

h = runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
extract = h['extract']; root = h['ROOT']; lab = 'engine/com.decennium.foundation/Laboratory/Model/'
def baseline(path):
    return subprocess.check_output(['git', 'show', h['BASE']+':'+path], cwd=root).decode().replace('\r\n','\n')
def replace(path, old, new):
    p=root/path;raw=p.read_bytes();eol='\r\n' if raw.count(b'\n') and raw.count(b'\r\n')==raw.count(b'\n') else '\n'
    current=p.read_text(encoding='utf8');assert current.count(old)==1,path
    p.write_bytes(current.replace(old,new,1).replace('\n',eol).encode())
def typed(path,source,fragment):
    first=source[:source.index(fragment)].count('\n')+1
    return ''.join(re.sub(r'return "([A-Za-z][A-Za-z0-9]+)";',
        lambda m:'return new NativeCommandConstraintV1("'+m[1]+'", "'+path+'", '+str(first+i)+');',line)
        for i,line in enumerate(fragment.splitlines(keepends=True)))
def ternaries(path,start,end):
    source=baseline(path);a=source.index(start);b=source.index(end,a);fragment=source[a:b]
    return [(m[0],m[1]+'new NativeCommandConstraintV1("'+m[2]+'", "'+path+'", '+str(source[:a+m.start()].count('\n')+1)+')')
        for m in re.finditer(r'([?:]\s*)"([A-Z][A-Za-z0-9]+)"',fragment)]

for file,oldname,newname,end in [
    ('SharedBishopEntry.cs','AssessBishopAdvancement','BishopAdvancementConstraintV1','        private static void SettleBishopAdvancement('),
    ('SharedClericSettlement.cs','AssessClericAdvancement','ClericAdvancementConstraintV1','        private string ResolveClericAdvancement('),
]:
    path=lab+file;source=baseline(path)
    start=next(line for line in source.splitlines() if 'private string '+oldname+'(' in line)
    edits=ternaries(path,start,end)
    if oldname=='AssessClericAdvancement':edits.append(('return AssessBishopAdvancement(s,c);','return BishopAdvancementConstraintV1(s,c);'))
    extract(path,start,end,newname,start.replace('string '+oldname,'NativeCommandConstraintV1 '+newname),
        start+'\n            => '+newname+'(s,c)?.NativeCode;\n\n',edits)

path=lab+'SharedHavenMeal.cs';start='        private string HavenMealServingCommandFailure(Snapshot s, Command command)';end='\n    }\n}'
extract(path,start,end,'HavenMealServingConstraintV1',start.replace('string HavenMealServingCommandFailure','NativeCommandConstraintV1 HavenMealServingConstraintV1'),
    start+'\n            => HavenMealServingConstraintV1(s, command)?.NativeCode;\n\n',ternaries(path,start,end))

path=lab+'TestOnlySharedWorldPolicy.cs';source=baseline(path)
a=source.index('            var openRoute = routeTravelFixture == null ? null : OpenRouteTravel(s, c.Actor);',source.index('        private string ResolveCore('))
b=source.index('            if (c.Kind == CommandKind.Hide || c.Kind == CommandKind.Search)',a);guards=source[a:b]
replace(path,guards,'            var routeTravelOuter = RouteTravelOuterConstraintV1(s, c);\n'
    '            if (routeTravelOuter != null) return routeTravelOuter.NativeCode;\n')
helper='        private NativeCommandConstraintV1 RouteTravelOuterConstraintV1(Snapshot s, Command c)\n        {\n'+typed(path,source,guards)+'            return null;\n        }\n\n'
anchor='        private static NativeCommandConstraintV1 WoundTreatmentOuterConstraintV1(Snapshot s, Command c)'
replace(lab+'SharedCommandAssessmentV1.cs',anchor,helper+anchor)

# Preserve the native fallback too. Its read path shares prerequisites only; the legacy
# assessor retains its future-level/capacity calculations and execution carrier stage.
path=lab+'SharedCharacterAdvancement.cs';source=baseline(path)
start='        private static string AssessRowChoices(Snapshot s,ActorCharacterRecord character,CharacterAdvancementRequest request,'
end='        private static string Assess(Snapshot s,Command c,out AdvancementAssessment assessment)'
wrapper=start+'\n            int classLevel,System.Collections.Generic.IEnumerable<string> previouslySelectedAdvancementFeatures,out string[] features)\n'
wrapper+='            => RowChoicesConstraintV1(s,character,request,classLevel,previouslySelectedAdvancementFeatures,out features)?.NativeCode;\n\n'
extract(path,start,end,'RowChoicesConstraintV1',start.replace('string AssessRowChoices','NativeCommandConstraintV1 RowChoicesConstraintV1'),wrapper,ternaries(path,start,end))
a=source.index(end);b=source.index('            var previousLevels=',a);opening=source[a:b]
pure=typed(path,source,opening)
pure=pure.replace(end,'''        private static NativeCommandConstraintV1 AdvancementOpeningConstraintV1(Snapshot s,Command c,
            out ActorCharacterRecord character,out int nextClassLevel,out string[] features,
            out int[] abilitiesBefore,out int[] abilitiesAfter)''',1)
pure=pure.replace('            assessment=null;','            character=null;nextClassLevel=0;features=Array.Empty<string>();abilitiesBefore=null;abilitiesAfter=null;',1)
pure=pure.replace('var character=s.Characters.SingleOrDefault','character=s.Characters.SingleOrDefault',1)
pure=pure.replace('                assessment=new AdvancementAssessment{AwardMilestone=true,Character=character,MilestoneId=c.Target};\n','',1)
pure=pure.replace('int nextClassLevel=character.Levels.Count+1;','nextClassLevel=character.Levels.Count+1;',1)
pure=pure.replace('string rowError=AssessRowChoices','var rowError=RowChoicesConstraintV1',1).replace('out var features);','out features);',1)
pure=pure.replace('int[] abilitiesBefore=character.Abilities.ToArray();int[] abilitiesAfter=abilitiesBefore.ToArray();','abilitiesBefore=character.Abilities.ToArray();abilitiesAfter=abilitiesBefore.ToArray();',1)
pure+='            return null;\n        }\n\n'
health='            if(life.MaximumHp!=maximumBefore)return "AdvancementHealthBasisMismatch";'
runtime='            if(priorRuntime!=null&&priorRuntime.LastRegularStart!=lastStart)return "FeatureRuntimeStartMismatch";'
health_guard=typed(path,source,health).strip().replace('if(life.MaximumHp!=maximumBefore)return ','return life.MaximumHp!=maximumBefore ? ').rstrip(';')+' : null;'
runtime_guard=typed(path,source,runtime).strip().replace('if(priorRuntime!=null&&priorRuntime.LastRegularStart!=lastStart)return ','return priorRuntime!=null&&priorRuntime.LastRegularStart!=lastStart ? ').rstrip(';')+' : null;'
helpers='''        private static NativeCommandConstraintV1 AdvancementHealthBasisConstraintV1(ActorLifeRecord life,long maximumBefore)
        {
            HEALTH
        }
        private static NativeCommandConstraintV1 AdvancementRuntimeStartConstraintV1(CharacterFeatureRuntimeRecord priorRuntime,int lastStart)
        {
            RUNTIME
        }

        internal static NativeCommandConstraintV1 InitialConstraintV1(Snapshot s,Command c)
        {
            var failure=AdvancementOpeningConstraintV1(s,c,out var character,out _,out _,out var abilitiesBefore,out _);
            if(failure!=null||c.Kind==CommandKind.AwardCharacterMilestone)return failure;
            var life=s.Lives.Single(x=>x.ActorId==c.Actor);
            var previousLevels=character.Levels.Select(x=>new CharacterLevelRecord(x.ClassName,x.BaseHp)).ToArray();
            long maximumBefore=PlaytestCharacters.BaseMaximumHp(previousLevels,abilitiesBefore[(int)CharacterAbility.Constitution]).BaseMaximum;
            var health=AdvancementHealthBasisConstraintV1(life,maximumBefore);if(health!=null)return health;
            var priorRuntime=Runtime(s,c.Actor);
            int lastStart=checked((int)s.WorldIntervals.Single(x=>x.ActorId==c.Actor).LastStart);
            return AdvancementRuntimeStartConstraintV1(priorRuntime,lastStart);
        }

'''.replace('HEALTH',health_guard).replace('RUNTIME',runtime_guard)
execution=end+'''
        {
            assessment=null;
            var failure=AdvancementOpeningConstraintV1(s,c,out var character,out int nextClassLevel,out var features,
                out var abilitiesBefore,out var abilitiesAfter);
            if(failure!=null)return failure.NativeCode;
            if(c.Kind==CommandKind.AwardCharacterMilestone) {
                assessment=new AdvancementAssessment{AwardMilestone=true,Character=character,MilestoneId=c.Target};
                return null;
            }
            var request=c.Advancement;
            var life=s.Lives.Single(x=>x.ActorId==c.Actor);
'''
replace(path,opening,pure+helpers+execution)
replace(path,health,'            var health=AdvancementHealthBasisConstraintV1(life,maximumBefore);if(health!=null)return health.NativeCode;')
replace(path,runtime,'            var runtime=AdvancementRuntimeStartConstraintV1(priorRuntime,lastStart);if(runtime!=null)return runtime.NativeCode;')
