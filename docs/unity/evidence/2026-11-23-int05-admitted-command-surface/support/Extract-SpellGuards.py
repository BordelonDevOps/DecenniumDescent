"""One-time shared spell guard extraction from the accepted native baseline."""
import runpy
import subprocess
from pathlib import Path

helpers = runpy.run_path(str(Path(__file__).with_name('Extract-NativePreflight.py')))
extract = helpers['extract']
core = 'engine/com.decennium.foundation/Runtime/Core/'
lab = 'engine/com.decennium.foundation/Laboratory/Model/'


def literal_origin(path, text, code):
    source = subprocess.check_output(
        ['git', 'show', helpers['BASE'] + ':' + path], cwd=helpers['ROOT']).decode('utf8')
    hits = [i for i, line in enumerate(source.splitlines(), 1) if text in line]
    assert len(hits) == 1, (path, text, hits)
    return 'new NativeCommandConstraintV1("' + code + '", "' + path + '", ' + str(hits[0]) + ')'


extract(core + 'SpellRepertoireRecords.cs',
    '        public static string AssessChoice(string spell, int actualClericLevel, bool bishop = false)',
    '        public static string ValidateInitialChoices(',
    'ChoiceConstraintV1',
    '        public static NativeCommandConstraintV1 ChoiceConstraintV1(string spell, int actualClericLevel, bool bishop = false)',
    '        public static string AssessChoice(string spell, int actualClericLevel, bool bishop = false)\n'
    '            => ChoiceConstraintV1(spell, actualClericLevel, bishop)?.NativeCode;\n\n',
    [('? "SpellClassLevelDenied" : null', '? ' + literal_origin(core + 'SpellRepertoireRecords.cs',
        'return access.MinimumClassLevel', 'SpellClassLevelDenied') + ' : null')])

extract(lab + 'SharedBishopDispel.cs',
    '        private static string BishopDispelFailure(Snapshot s,Command c,out SpellEffectRecord effect)',
    '        private static void ResolveBishopDispel(',
    'BishopDispelConstraintV1',
    '        private static NativeCommandConstraintV1 BishopDispelConstraintV1(Snapshot s,Command c,out SpellEffectRecord effect)',
    '        private static string BishopDispelFailure(Snapshot s,Command c,out SpellEffectRecord effect)\n'
    '            => BishopDispelConstraintV1(s,c,out effect)?.NativeCode;\n\n',
    [('?"DispelHistoryFull":null', '?' + literal_origin(lab + 'SharedBishopDispel.cs',
        'return s.BishopEntry.Dispels.Count', 'DispelHistoryFull') + ':null')])

extract(lab + 'SharedSpellCasting.cs',
    '        private static string PurifyBatchFailure(Snapshot s,Command c)',
    '        private static void RecordCastingActivity(',
    'PurifyBatchConstraintV1',
    '        private static NativeCommandConstraintV1 PurifyBatchConstraintV1(Snapshot s,Command c)',
    '        private static string PurifyBatchFailure(Snapshot s,Command c)\n'
    '            => PurifyBatchConstraintV1(s,c)?.NativeCode;\n\n')

extract(lab + 'SharedSpellCasting.cs',
    '        private string AssessSpellCast(Snapshot s,Command c)',
    '        private static string PurifyBatchFailure(',
    'SpellCastConstraintV1',
    '        private NativeCommandConstraintV1 SpellCastConstraintV1(Snapshot s,Command c)',
    '        private string AssessSpellCast(Snapshot s,Command c)\n'
    '            => SpellCastConstraintV1(s,c)?.NativeCode;\n\n',
    [('string shape=SpellCastingProfile.PayloadFailure(s,c);', 'var shape=SpellCastingProfile.PayloadConstraintV1(s,c);'),
     ('string action=CastingActionFailure(s,c);', 'var action=CastingActionConstraintV1(s,c);'),
     ('string access=ClericRepertoireProfile.AssessChoice(spell,level,BishopProfile.Earned(s));',
      'var access=ClericRepertoireProfile.ChoiceConstraintV1(spell,level,BishopProfile.Earned(s));'),
     ('string dispel=BishopDispelFailure(s,c,out _);', 'var dispel=BishopDispelConstraintV1(s,c,out _);'),
     ('string batch=PurifyBatchFailure(s,c);', 'var batch=PurifyBatchConstraintV1(s,c);')])
