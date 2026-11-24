"""Extract shared native work prefix guards with original source coordinates."""
from pathlib import Path
import runpy,subprocess,re
h=runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
b='engine/com.decennium.foundation/Laboratory/Model/'
h['extract'](b+'SourceContentResolution.cs','        public string ValidateCommand(Snapshot state, Command command)',
 '        public string ValidatePortableSnapshot(', 'CommandConstraintV1',
 '        internal NativeCommandConstraintV1 CommandConstraintV1(Snapshot state, Command command)',
 '        public string ValidateCommand(Snapshot state, Command command)\n            => CommandConstraintV1(state, command)?.NativeCode;\n\n')
h['extract'](b+'SharedRecipe347.cs','        private string Recipe347WatchAdmission(Snapshot s,string actor)',
 '        private static bool Recipe347WorkStartCommand(', 'Recipe347WatchConstraintV1',
 '        private NativeCommandConstraintV1 Recipe347WatchConstraintV1(Snapshot s,string actor)',
 '        private string Recipe347WatchAdmission(Snapshot s,string actor)\n            => Recipe347WatchConstraintV1(s,actor)?.NativeCode;\n\n')
h['extract'](b+'SharedRecipe347.cs','        private string Recipe347WorkWatchCommandFailure(Snapshot s,Command c)',
 '        private void InitializeRecipe347(', 'Recipe347WorkWatchConstraintV1',
 '        private NativeCommandConstraintV1 Recipe347WorkWatchConstraintV1(Snapshot s,Command c)',
 '        private string Recipe347WorkWatchCommandFailure(Snapshot s,Command c)\n            => Recipe347WorkWatchConstraintV1(s,c)?.NativeCode;\n\n',
 [('Recipe347WatchAdmission(s,c.Actor)','Recipe347WatchConstraintV1(s,c.Actor)')]*2)
path=b+'TestOnlySharedWorldPolicy.cs';original=subprocess.check_output(['git','show',h['BASE']+':'+path],cwd=h['ROOT']).decode().replace('\r\n','\n')
a=original.index('            if (IsOffCalendarActivity(s, c.Actor) && StartsOrResumesActivityWork(c)');z=original.index('            if((c.Kind==CommandKind.RespondOverwatch',a);block=original[a:z]
line=original[:original.index('return "OffCalendarActionAlreadySpent"',a)].count('\n')+1
typed=block.replace('return "OffCalendarActionAlreadySpent"','return new NativeCommandConstraintV1("OffCalendarActionAlreadySpent", "'+path+'", '+str(line)+')')
q=h['ROOT']/path;s=q.read_text();assert block in s;s=s.replace(block,'            var activityWorkFailure = OffCalendarWorkConstraintV1(s,c);\n            if(activityWorkFailure!=null)return activityWorkFailure.NativeCode;\n');q.write_text(s,newline='\n')
assessment=h['ROOT']/(b+'SharedCommandAssessmentV1.cs');s=assessment.read_text();insert=s.index('        private NativeCommandConstraintV1 WorldOpeningConstraintV1(')
s=s[:insert]+'''        // Used for formula commands only until the other families are wired to this exact prefix.
        private NativeCommandConstraintV1 BeforeFormulaBranchConstraintV1(Snapshot s, Command c)
            => BeforeStabilizationBranchConstraintV1(s,c) ?? HavenMealServingConstraintV1(s,c)
                ?? RouteTravelOuterConstraintV1(s,c) ?? OffCalendarWorkConstraintV1(s,c)
                ?? contentManifest?.CommandConstraintV1(s,c) ?? Recipe347WorkWatchConstraintV1(s,c)
                ?? (ManufacturingChoicePending(s) ? new NativeCommandConstraintV1("ManufacturingChoicePending",
                    "'''+path+'''", '''+str(original[:original.index('return "ManufacturingChoicePending"',original.index('string recipeWatchFailure'))].count('\n')+1)+''') : null);

        private NativeCommandConstraintV1 OffCalendarWorkConstraintV1(Snapshot s, Command c)
        {
'''+typed+'''            return null;
        }

'''+s[insert:]
s=s.replace('|| kind == CommandKind.CloseExpeditionEpisode','|| FormulaCommand(kind)\n                || kind == CommandKind.CloseExpeditionEpisode',1)
anchor='                case CommandKind.CloseExpeditionEpisode:'
line=original[:original.index('?"TacticalChoicePending":ResolveFormulaWork')].count('\n')+1
s=s.replace(anchor,'''                case CommandKind.StartFormulaResearch:
                case CommandKind.StartFormulaCopy:
                case CommandKind.PauseFormulaWork:
                case CommandKind.ResumeFormulaWork:
                case CommandKind.CancelFormulaWork:
                    return BeforeFormulaBranchConstraintV1(current,command)
                        ?? (connectedCombat!=null && PendingCalendarChoice(current)
                            ? new NativeCommandConstraintV1("TacticalChoicePending", "'''+path+'''", '''+str(line)+''')
                            : FormulaWorkConstraintV1(current,command,out _,out _,out _,out _));
'''+anchor,1)
assessment.write_text(s,newline='\n')
print('Work outer guard extraction complete.')
