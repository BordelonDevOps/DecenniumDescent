"""Portable minimal source-derived mechanical records for the audit probes.
These are NOT reconstructed full source cards or game-world facts.
"""
from pathlib import Path
from fractions import Fraction as F
import json
_payload=json.loads(Path(__file__).with_name('source_register_mechanical_inputs.json').read_text(encoding='utf-8'))
CARDS=_payload['cards'];REGISTER=_payload['register']
BODY_GP={k:F(v) for k,v in _payload['bodyGp'].items()};BODY_LB=_payload['bodyLb']
assert len(CARDS)==44
