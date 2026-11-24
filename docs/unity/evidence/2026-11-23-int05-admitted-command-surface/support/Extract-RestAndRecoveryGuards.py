"""One-time exact shared extraction for long rest and existing magical recovery abilities."""
import runpy
import subprocess
from pathlib import Path

h=runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
extract=h['extract']; lab='engine/com.decennium.foundation/Laboratory/Model/'

def origin(path, text, code):
    source=subprocess.check_output(['git','show',h['BASE']+':'+path],cwd=h['ROOT']).decode('utf8')
    hits=[i for i,line in enumerate(source.splitlines(),1) if text in line]
    assert len(hits)==1,(path,text,hits)
    return 'new NativeCommandConstraintV1("'+code+'", "'+path+'", '+str(hits[0])+')'

extract(lab+'SharedClericLongRest.cs',
    '        private string ClericLongRestAccess(Snapshot s, ClericLongRestRecord active)',
    '        private string AssessClericLongRest(',
    'ClericLongRestAccessConstraintV1',
    '        private NativeCommandConstraintV1 ClericLongRestAccessConstraintV1(Snapshot s, ClericLongRestRecord active)',
    '        private string ClericLongRestAccess(Snapshot s, ClericLongRestRecord active)\n'
    '            => ClericLongRestAccessConstraintV1(s, active)?.NativeCode;\n\n')
extract(lab+'SharedClericLongRest.cs',
    '        private string AssessClericLongRest(Snapshot s, Command c)',
    '        private System.Collections.Generic.IEnumerable<Command> DiscoverClericLongRest(',
    'ClericLongRestConstraintV1',
    '        private NativeCommandConstraintV1 ClericLongRestConstraintV1(Snapshot s, Command c)',
    '        private string AssessClericLongRest(Snapshot s, Command c)\n'
    '            => ClericLongRestConstraintV1(s, c)?.NativeCode;\n\n',
    [('? "NoMatchingActiveLongRest" : null','? '+origin(lab+'SharedClericLongRest.cs','return active == null || c.Target','NoMatchingActiveLongRest')+' : null'),
     ('return ClericLongRestAccess(s,null);','return ClericLongRestAccessConstraintV1(s,null);')])
extract(lab+'SharedRadiance.cs',
    '        internal static string OwnTurnFailure(Snapshot s, string actor)',
    '        internal static ConditionStamp TargetStamp(',
    'OwnTurnConstraintV1',
    '        internal static NativeCommandConstraintV1 OwnTurnConstraintV1(Snapshot s, string actor)',
    '        internal static string OwnTurnFailure(Snapshot s, string actor)\n'
    '            => OwnTurnConstraintV1(s, actor)?.NativeCode;\n\n',
    [('string context=OrdinaryMagicProfile.ContextFailure(s,actor);','var context=OrdinaryMagicProfile.ContextConstraintV1(s,actor);')])
extract(lab+'SharedRadiance.cs',
    '        private static string RadiancePreflight(Snapshot state, Command command)',
    '        private static void SettleRadiance(',
    'RadianceConstraintV1',
    '        private static NativeCommandConstraintV1 RadianceConstraintV1(Snapshot state, Command command)',
    '        private static string RadiancePreflight(Snapshot state, Command command)\n'
    '            => RadianceConstraintV1(state, command)?.NativeCode;\n\n',
    [('string context = RadianceRules.OwnTurnFailure(state,command.Actor);','var context = RadianceRules.OwnTurnConstraintV1(state,command.Actor);')])
extract(lab+'SharedResonance.cs',
    '        private string AssessHealingRite(Snapshot state, Command command)',
    '        private string ResolveHealingRite(',
    'HealingRiteConstraintV1',
    '        private NativeCommandConstraintV1 HealingRiteConstraintV1(Snapshot state, Command command)',
    '        private string AssessHealingRite(Snapshot state, Command command)\n'
    '            => HealingRiteConstraintV1(state, command)?.NativeCode;\n\n',
    [('string context=AssessMagicalActivityContext(state,command.Actor);','var context=MagicalActivityContextConstraintV1(state,command.Actor);'),
     ('string context = RadianceRules.OwnTurnFailure(state,command.Actor);','var context = RadianceRules.OwnTurnConstraintV1(state,command.Actor);'),
     ('? RadiancePreflight(state,command) : null','? RadianceConstraintV1(state,command) : null')])
extract(lab+'SharedDivineInvocation.cs',
    '        private string AssessDivineInvocation(Snapshot s,Command c)',
    '        private CommandQueryResult QueryDivineInvocation(',
    'DivineInvocationConstraintV1',
    '        private NativeCommandConstraintV1 DivineInvocationConstraintV1(Snapshot s,Command c)',
    '        private string AssessDivineInvocation(Snapshot s,Command c)\n'
    '            => DivineInvocationConstraintV1(s,c)?.NativeCode;\n\n',
    [('string shape=BishopProfile.InvocationPayloadFailure(s,c);','var shape=BishopProfile.InvocationPayloadConstraintV1(s,c);'),
     ('string context=RadianceRules.OwnTurnFailure(s,c.Actor);','var context=RadianceRules.OwnTurnConstraintV1(s,c.Actor);'),
     ('string action=CastingActionFailure(s,c);','var action=CastingActionConstraintV1(s,c);')])
extract(lab+'SharedConsecration.cs',
    '        private string AssessConsecrate(Snapshot s, Command c)',
    '        private string ResolveConsecrate(',
    'ConsecrateConstraintV1',
    '        private NativeCommandConstraintV1 ConsecrateConstraintV1(Snapshot s, Command c)',
    '        private string AssessConsecrate(Snapshot s, Command c)\n'
    '            => ConsecrateConstraintV1(s,c)?.NativeCode;\n\n',
    [('string context=AssessMagicalActivityContext(s,c.Actor);','var context=MagicalActivityContextConstraintV1(s,c.Actor);')])
