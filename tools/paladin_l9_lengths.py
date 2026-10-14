"""Measure Paladin L9 revelation spell string lengths."""
from __future__ import annotations

spells = [
    ("mercy", "Channel Life — transfer HP from self to ally"),
    ("vengeance", "Sentence of Doom — smite deals max dice vs marked"),
    ("dominion", "Law's Weight — slow and −AC to lawbreakers"),
    ("flame", "Purge the Tainted — zone damages undead each round"),
    ("ancients", "Echo of Ages — advantage vs charmed/frightened"),
    ("silence", "Wordless Ward — shield ally without verbal components"),
    ("chain", "Martyr's Share — take half ally's damage as reaction"),
    ("grief", "Memorial Flame — light that reveals undead"),
    ("chains-broken", "Shatter Shackles — dispel magical restraint in area"),
    ("martyr-king", "Burden Shared — distribute damage among willing allies"),
]

mercy_len = len(spells[0][1])
print(f"Mercy L9 baseline: {mercy_len}")
for oid, s in spells:
    flag = " THIN" if len(s) <= mercy_len and oid != "mercy" else ""
    print(f"{len(s):3d} | {oid:15s} | {s}{flag}")
