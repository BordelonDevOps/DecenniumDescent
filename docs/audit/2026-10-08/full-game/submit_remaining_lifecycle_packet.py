"""Materialize next conference after confirmed creature closure; does not transmit."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
reply=(HERE/'GPT_CREATURE_LIFECYCLE_FINAL_CLOSURE.md').read_text(encoding='utf-8')
assert reply.startswith('# GPT confirmed creature lifecycle closure')
text=(HERE/'CODEX_REMAINING_LIFECYCLE_CONFERENCE_PREPARED.md').read_text(encoding='utf-8')
text=text.replace('# Remaining class lifecycle source conference — prepared, not yet sent','# Remaining class lifecycle source conference —80 exact passages+5 shared supports',1)
intro='''The preceding selected100+5 creature interface now has your explicit final closure (121 checks/2,800 Ranger conversion states). This next source conference must preserve its accepted body identity, shared command/offense, attached phase, source-owner provenance and hard-denial principles, adding only exact source exceptions or explicitly labeled NEW integrations. The separate device74+3 interface is likewise reviewed; ordinary object names alone do not grant all Tinker repair/reconstruction permissions. No new source below is pre-approved merely by that continuity.

'''
text=text.replace('Codex → Calibration Review. ', 'Codex → Calibration Review. '+intro,1)
(HERE/'CODEX_REMAINING_LIFECYCLE_CONFERENCE.md').write_text(text,encoding='utf-8')
print(f'Materialized next80+5 conference:{len(text)} characters; browser submission required.')
