"""One-use, preserved helper follow-through of GPT's explicit FAA-03/FS-02 ruling."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
A = G / 'docs/audit/2026-10-08/full-game'
target = R / 'tools/feat_exact_01_weapon_profile_choices.py'
out = A / 'FEAT335_FAA03_PROFILE_BRIDGE_DERIVED_OPERATIONS.json'
folder = A / 'before-feat335-faa03-profile-bridge'
assert not out.exists() and not folder.exists(), 'Preserved operations are one-use'

def info(path):
    data = path.read_bytes()
    return {'path': path.relative_to(G).as_posix(), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}

before = target.read_bytes()
text = before.decode('utf-8')
edits = [
    ('        self.conditional_profiles = {}',
     '        self.conditional_profiles = {}\n        self.source_unarmed_profiles = {}'),
    ('        if profile not in self.weapon_choices and profile not in self.conditional_profiles:\n'
     "            if not (sid == 'weaponFocus' and profile == UNARMED and profile in self.equipment):",
     '        if (profile not in self.weapon_choices and profile not in self.conditional_profiles\n'
     "                and profile not in getattr(self, 'source_unarmed_profiles', {})):\n"
     '            if not (profile == UNARMED and profile in self.equipment):'),
    ('    def profile(self, profile):\n        if profile in self.weapon_choices:',
     '    def profile(self, profile):\n'
     "        if profile in getattr(self, 'source_unarmed_profiles', {}):\n"
     '            return self.source_unarmed_profiles[profile]\n'
     '        if profile in self.weapon_choices:'),
    ('                     conditionalProfiles=deepcopy(getattr(self, \'conditional_profiles\', {})))',
     '                     conditionalProfiles=deepcopy(getattr(self, \'conditional_profiles\', {})),\n'
     '                     sourceUnarmedProfiles=deepcopy(getattr(self, \'source_unarmed_profiles\', {})))'),
]
# Preserve the existing file's newline convention exactly outside guarded edits.
newline = '\r\n' if '\r\n' in text else '\n'
normalized = text.replace('\r\n', '\n')
for old, new in edits:
    assert normalized.count(old) == 1, old
    normalized = normalized.replace(old, new, 1)
updated = normalized.replace('\n', newline).encode('utf-8')
folder.mkdir()
copy = folder / target.name
copy.write_bytes(before)
old_binding = info(target)
old_binding['preservedCopy'] = copy.relative_to(G).as_posix()
assert copy.read_bytes() == before
target.write_bytes(updated)
receipt = {'createdUtc': datetime.now(timezone.utc).isoformat(),
           'authority': 'FEAT335-ACQUISITION-AUDIT-01 FAA-03; accepted FS-02 exact guarded replacement',
           'scope': 'Admit trained ordinary unarmed for Mastery and explicit authenticated specific unarmed profiles. Acquisition/use predicates unchanged; no Weapon Master menu change.',
           'changes': [{'before': old_binding, 'after': info(target), 'guardedEdits': edits}]}
out.write_text(json.dumps(receipt, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
(folder / 'PRESERVATION_MANIFEST.json').write_text(json.dumps({'preserved': [old_binding]}, indent=2)+'\n', encoding='utf-8')
print(json.dumps(info(out)))
