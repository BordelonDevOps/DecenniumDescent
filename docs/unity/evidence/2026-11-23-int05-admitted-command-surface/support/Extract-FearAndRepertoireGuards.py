"""Extract existing early-branch guards, preserving source/profile denials."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('native', Path(__file__).with_name('Extract-NativePreflight.py'))
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)

path = 'engine/com.decennium.foundation/Laboratory/Model/SharedFrightened.cs'
native.extract(path, '        private string AssessIntimidatingPresence(Snapshot state, Command command)',
    '        private CommandQueryResult QueryIntimidatingPresence(', 'IntimidatingPresenceConstraintV1',
    '        private NativeCommandConstraintV1 IntimidatingPresenceConstraintV1(Snapshot state, Command command)',
    '        private string AssessIntimidatingPresence(Snapshot state, Command command)\n'
    '            => IntimidatingPresenceConstraintV1(state, command)?.NativeCode;\n\n')

path = 'engine/com.decennium.foundation/Runtime/Core/SpellRepertoireRecords.cs'
native.extract(path, '        public static string CommandFailure(Snapshot state, Command command)',
    '        public static string AssessChoice(', 'CommandConstraintV1',
    '        public static NativeCommandConstraintV1 CommandConstraintV1(Snapshot state, Command command)',
    '        public static string CommandFailure(Snapshot state, Command command)\n'
    '            => CommandConstraintV1(state, command)?.NativeCode;\n\n', [
        ('? "OrdinarySpellcastingUnsupported"', '? new NativeCommandConstraintV1("OrdinarySpellcastingUnsupported", "'+path+'", 126)'),
        ('? "EarnedSpellAcquisitionRequiresAdvancementTransaction" : "ClericEarnedAdvancementUnavailable"',
         '? new NativeCommandConstraintV1("EarnedSpellAcquisitionRequiresAdvancementTransaction", "'+path+'", 127)'
         ' : new NativeCommandConstraintV1("ClericEarnedAdvancementUnavailable", "'+path+'", 127)'),
    ])
