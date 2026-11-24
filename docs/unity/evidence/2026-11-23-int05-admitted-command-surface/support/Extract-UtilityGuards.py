"""One-time shared utility guard extraction; exact original rules and origin coordinates."""
import runpy
from pathlib import Path
extract=runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))['extract']
core='engine/com.decennium.foundation/Runtime/Core/'
lab='engine/com.decennium.foundation/Laboratory/Model/'
extract(core+'OrdinaryMagicProfile.cs',
    '        public static string ContextFailure(Snapshot s, string actor)',
    '        public static MagicalActivityContextRecord Activity(',
    'ContextConstraintV1','        public static NativeCommandConstraintV1 ContextConstraintV1(Snapshot s, string actor)',
    '        public static string ContextFailure(Snapshot s, string actor)\n            => ContextConstraintV1(s, actor)?.NativeCode;\n\n')
extract(lab+'SharedOrdinaryMagic.cs',
    '        private static string AssessMagicalActivityContext(Snapshot s, string actor)',
    '        private static void CloseMagicalSegment(',
    'MagicalActivityContextConstraintV1','        private static NativeCommandConstraintV1 MagicalActivityContextConstraintV1(Snapshot s, string actor)',
    '        private static string AssessMagicalActivityContext(Snapshot s, string actor)\n            => MagicalActivityContextConstraintV1(s, actor)?.NativeCode;\n\n',
    [('string failure = OrdinaryMagicProfile.ContextFailure(s, actor);','var failure = OrdinaryMagicProfile.ContextConstraintV1(s, actor);'),
     ('? "MagicalAccountingHistoryFull" : null','? new NativeCommandConstraintV1("MagicalAccountingHistoryFull", "'+lab+'SharedOrdinaryMagic.cs", 32) : null')])
extract(lab+'SharedSpellCasting.cs',
    '        private string CastingActionFailure(Snapshot s,Command c)',
    '        private static bool UsesSpellFocus(',
    'CastingActionConstraintV1','        private NativeCommandConstraintV1 CastingActionConstraintV1(Snapshot s,Command c)',
    '        private string CastingActionFailure(Snapshot s,Command c)\n            => CastingActionConstraintV1(s,c)?.NativeCode;\n\n',
    [('string context=AssessMagicalActivityContext(s,c.Actor);','var context=MagicalActivityContextConstraintV1(s,c.Actor);'),
     ('?"CastingHistoryFull":null','?new NativeCommandConstraintV1("CastingHistoryFull", "'+lab+'SharedSpellCasting.cs", 103):null')])
