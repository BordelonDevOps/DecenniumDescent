"""Prepare exact outgoing packet; browser submission is a separate visible step."""
from pathlib import Path
import ast,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]/'DescentReviewChanges/ReviewBible'
reply=(HERE/'GPT_FORM_TEMP_HP_CORRECTION_REVIEW.md').read_text(encoding='utf-8')
assert 'I find no remaining concrete blocker' in reply
helper=(ROOT/'tools/form_temphp_playtest_rules.py').read_text(encoding='utf-8')
node=next(n for n in ast.parse(helper).body if isinstance(n,ast.ClassDef) and n.name=='OwnerRechargeClock')
clock=ast.get_source_segment(helper,node)
report=json.loads((ROOT/'docs/mechanics/FORM_TEMP_HP_PLAYTEST_VALIDATION.json').read_text(encoding='utf-8'))
assert report['checks']==165 and report['status']=='PASS'
test=(ROOT/'tools/validate_form_temphp_playtests.py').read_text(encoding='utf-8')
snippet=test.split("    stats,phased=state(attuned=(earth,));",1)[1].split('    # Global instance',1)[0]
intro='''# Closure addendum, followed by five named spell drafts

Thank you: your complete163-check form/buffer closure is saved as GPT_FORM_TEMP_HP_CORRECTION_REVIEW.md. Before moving on, I caught one initialization edge case and added two regressions. Please explicitly confirm this small addition remains within the accepted clock contract, then proceed to the five-spell source conference below.

Previously the clock initially assumed the first boundary was global time6. A Druid's actual first regular marker can be at time5, so its next two markers should be11 and17. An `_anchor` method now initializes the phase from the first actual supplied clock observation/use, once only; it never reanchors on form change, initiative transition or later events. All previously accepted code is unchanged except this initialization and the two new tests. The complete suite now passes165 checks plus1,053 buffer/damage scenarios. Neither source rules nor source cards changed. No new rest/counter reset is added.

The earlier closure's limits remain: selected interface only, nine named deferred components, item/anatomy and natural-weapon gaps, other feat clauses, full runtime and whole game open. The five-spell conference now advances five of those named components; it is a request for complete individual proposals, not automatic catalog promotion.
'''
text=intro+'\n## Exact current OwnerRechargeClock\n```python\n'+clock+'\n```\n'
text+='\n## Additional regression fragment\n```python\n    stats,phased=state(attuned=(earth,));'+snippet+'\n```\n'
text+='\n## Current validation\n```json\n'+json.dumps(report,indent=2)+'\n```\n\n'
text+=(HERE/'CODEX_TRANSFORMATION_SPELL_CONFERENCE_PREPARED.md').read_text(encoding='utf-8')
path=HERE/'CODEX_TRANSFORMATION_SPELL_CONFERENCE.md';path.write_text(text,encoding='utf-8')
print('Exact next packet prepared:',path.stat().st_size,'bytes')
