"""Render the exact supplied procedures plus reviewed overlay decisions."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]


def main():
 data=json.loads((ROOT/'data/playtest/control_state_bindings.json').read_text(encoding='utf-8'))
 lines=['# Control source bindings','',f"**{data['status']} — {len(data['bindings'])} supplied passages.** This is not exhaustive whole-game semantic coverage.",'',
 '[Operational guide](CONTROL_STATES_PLAYTEST.md) · [Coverage](CONTROL_STATE_COVERAGE.md) · [Source checks](CONTROL_STATE_SOURCE_VALIDATION.json)','',
 'Each source procedure below remains conditional on its own mode, costs, eligibility, saves, target caps, use limits and source ending. Component IDs identify pieces; they never grant simultaneous application of alternative modes. Historical conference context is preserved in the JSON and audit files, not rendered as competing operational rules.','']
 for b in data['bindings']:
  lines.extend([f"## {b['bindingId']}",'',f"Classification: **{b['classification']}**. Source: `{b['sourcePath']}` / `{b['sourceId']}`. SHA256 `{b['sourceSha256']}`.",'',
    'Application components: '+(', '.join(f'`{c}`' for c in b['componentIds']) or 'None applied directly by this binding.')+'.',''])
  if b.get('modifiesComponents'):lines.extend(['Modifies/authorizes later application: '+', '.join(f'`{c}`' for c in b['modifiesComponents'])+'.',''])
  if b.get('referencesComponents'):lines.extend(['Reader/bookkeeping references: '+', '.join(f'`{c}`' for c in b['referencesComponents'])+'.',''])
  for key,value in b['sourceProcedure'].items():
   if value is not None:
    rendered=', '.join(value) if isinstance(value,list) else str(value)
    lines.extend([f'**{key}:** {rendered}',''])
  if b.get('operationalOverrides'):
   lines.extend(['**Reviewed overlay:** '+ ' '.join(b['operationalOverrides']),''])
 (ROOT/'docs/mechanics/CONTROL_SOURCE_BINDINGS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print(f"Rendered {len(data['bindings'])} exact source procedures with overlays.")


if __name__=='__main__':main()
