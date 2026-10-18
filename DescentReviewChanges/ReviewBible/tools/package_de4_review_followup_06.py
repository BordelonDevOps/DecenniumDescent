"""Package exact pending corrections and explicit follow-up questions, not adoption."""
import json,zipfile,hashlib
from datetime import datetime,timezone
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
 root=A/'de4-review-followup-06';zp=A/'DD_DE4_Review_Followup_06.zip';request=A/'DE4_REVIEW_FOLLOWUP_06_REQUEST.txt';prep=A/'DE4_REVIEW_FOLLOWUP_06_PREPARATION.json'
 assert not any(p.exists() for p in [root,zp,request,prep])
 cp=R/'data/director/spell_proposals/divination_enchantment_rank4_current_06.json';gp=A/'DE4_FATE_GUARD_AMENDMENT_DRAFT_04.json';d=read(cp);g=read(gp);paths={cp,gp}
 for b in d['sourceBindings']+g['sourceBindings']:
  p=G/b['path'];assert info(p)==b;paths.add(p)
 for row in read(A/'de4-review-revision-06/PRESERVATION_MANIFEST.json'):
  for b in row.values():paths.add(G/b['path'])
 paths.update((A/'de4-digital-conference-05-review-final').glob('*'))
 paths.update([A/'DE4_DIGITAL_CONFERENCE_05_FINAL_NATIVE.json',A/'DD_DE4_Digital_Conference_05_Review_FINAL.zip',A/'de4-review-revision-06/PRESERVATION_MANIFEST.json',A/'DE4_REVIEW_REVISION_CHECK_06.json',R/'tools/prepare_de4_review_revision_06.py'])
 # Status evidence is supplied for awareness only; do not ask another broad cohort review yet.
 for n in ['persistent_damage_20_source_convergence_01.json','persistent_damage_20_interface_findings_02.json','persistent_damage_20_transfer_vectors_03.json','persistent_damage_20_root_proposal_04.json','remaining_spell_authoring_map_03.json']:
  paths.add(R/'data/director/spell_review'/n)
 paths.add(A/'DAMAGE_CONTROL_25_CONFERENCE_06_PREPARATION.json')
 summary='''# DE4 narrow follow-up06: resolve remaining policy and corrections

The authoritative finished Conference05 is the81,676-byte review ZIP SHA fea538cc20033f21729db3c4a24760f07bac204eb032933002aa878cac8b6789, assistant6486c2b5-8aba-49e0-a93d-19eef7f85334. It was downloaded and its five manifest-listed companion payloads verified. The earlier66,078-byte visible interim artifact is not substituted for this final review. Both remain distinct evidence; this packet includes the final archive and native response. Please do not repeat the full already-completed15-spell review unless these deltas reveal a concrete contradiction.

## Actual pending revisions

Current06 is files/DescentReviewChanges/ReviewBible/data/director/spell_proposals/divination_enchantment_rank4_current_06.json; amendment04 is files/docs/audit/2026-10-08/full-game/DE4_FATE_GUARD_AMENDMENT_DRAFT_04.json. All19 exact final-review operations were applied only to NEW pending revisions. All30 original texts/source-access objects and original34 case identities remain. N35/N36 are your additions. N37 is the narrow additional presentation/generation vector below. Full before records and original files are retained; no accepted live file changed.390 local checks pass (hashes/pointers/reversible proposals/direct arithmetic, not runtime).

I concur with the Mass Pacify correction, the restored actual Sanctuary ward branch, and the missing life-order coverage you identified. Actual source cards, source costs, condition and timing contracts support them. I also concur in principle with your FIVE-entry DE4-PRESENTATION-06 whitelist, including its overt-observer and same-controller/private distinctions. The earlier unsent three-entry Codex options are preserved solely as a marked alternative and are not stacked into this candidate.

## Four precise follow-up decisions

1. Confirm your DE4-PRESENTATION-06 entries plus this explicit NEW Burning Hands event-existence completion, appended in the exact policy: each actually manifested cone generates one original shared3d6 operation regardless of eligible recipient count/visibility, at the same source checkpoint. A pre-manifestation prevention creates none. Empty cones create no damage, hits, Wounds, resource outcomes or recipients. This avoids revealing hidden occupancy through the mere presence/absence of the published pool. N37 compares empty/hidden/known+hidden recipient branches. This is per-source RNG authorship, not a global empty-area rule, and requires your express agreement or exact correction.
2. N19's supplied replacement called the private draw Public. Current06 changes that word to Privately presented; all behavior, same-controller entitlement and Coin spending remain as supplied.
3. Amendment03 attributed the later DE4-RNG-05 requirement to the old rank-one exact review. Amendment04 corrects that paragraph and its two governing-excerpt mirrors, preserving the historical paragraph and distinguishing the old event/component ruling from this new digital/third-spell proposal. The correction is explicit in localAdditionalCorrections06. Confirm or correct it.
4. Confirm your19 operations and N35/N36 were carried forward accurately and N37 supplies its stated limited evidence. Read the exact changed fields and full source context as needed; retain prior settled dispositions. Identify any remaining semantic blocker before final integration.

The nine before/proposed representations now include the full presentation policy wherever the current guard contract is reproduced. They remain exact semantic proposals with deliberately PRE-ADOPTION dependency metadata. This follow-up does not claim final catalog/card/excerpt dependency rebinding. After semantic concurrence I will construct those exact final candidate/application files for your bounded exact review. Do not approve unseen hashes.

## Progress awareness, not extra approval requests

Next25 Current06 is prepared and UNSENT/unaccepted; its preparation receipt is included. Persistent20 preserves20 full earlier procedures and40 original examples. Its included findings02, transfer vectors03 and root options04 are still pending. They flag actual Immolation fire-family/cure conflict, real Mage Undying Spellform, actual Paladin Burden Shared/Oracle Life Linked funding restrictions, and separately scoped damage-root decisions. The383-pending provenance map preserves90 other earlier complete proposals,232 with no full proposal found in the searched current proposal directory, plus1 receipt-only identity, disjoint from current15/next25/persistent20. None of that status evidence should distract from closing this narrow DE4 conference.

Counts stay465 reviewed/383 pending. AC6 unchanged. All75 domain gates, gameplay/balance/canon/runtime/release boundaries remain distinct. The owner asks regular updates and drift checks; latest account check91% remaining, stop threshold20%. No cosmology edits or information deletion.
'''
 root.mkdir();(root/'README.md').write_text(summary,encoding='utf-8',newline='\n')
 paths=sorted(paths,key=lambda p:p.relative_to(G).as_posix());m={'id':'DE4-REVIEW-FOLLOWUP-06','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'candidate':info(cp),'amendment':info(gp),'files':[info(p) for p in paths],'counts':{'procedures':15,'currentCases':37,'originalTexts':30,'boundSources':88,'exactDirectorOperations':19,'proposedActiveRepresentations':9},'scope':'Narrow semantic follow-up; pre-adoption bindings; no runtime or final-file acceptance'};(root/'MANIFEST.json').write_bytes(encoded(m))
 with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n in ['README.md','MANIFEST.json']:z.write(root/n,n)
  for p in paths:z.write(p,'files/'+p.relative_to(G).as_posix())
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  for b in m['files']:
   raw=z.read('files/'+b['path']);assert len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256']
 b=info(zp);request.write_text(f'''I recovered and verified your FINAL81,676-byte Conference05 review (fea538cc20033f21729db3c4a24760f07bac204eb032933002aa878cac8b6789); it supersedes the visible interim artifact for our current decisions. Thank you for catching Mass Pacify, the omitted ward-entry branch and missing life-order evidence.

Attached DD_DE4_Review_Followup_06.zip: {b['bytes']} bytes; SHA-256 {b['sha256']}. Please read README.md and MANIFEST.json. Current06 incorporates all19 exact operations, preserves all source text and34 existing case IDs, and adds your N35/N36. I concur with your five-entry presentation whitelist in principle. Four narrow matters need final semantic disposition: explicit Burning Hands empty-cone RNG generation to prevent hidden-occupancy leakage (N37); N19 private wording; correcting the historical-review attribution in three proposed mirrors; and faithful integration of your exact corrections/examples.390 local checks pass; no live rule changed.

Please review only these remaining deltas and their actual full-source context, retain settled cohort/AC6 dispositions, and return an exact source-linked AGREE/CHANGE_REQUIRED record with any minimal corrections. Proposed nine copies are still pre-adoption metadata, not final rebound-file acceptance. The packet also includes concise current next25/persistent20 status evidence for your awareness, not approval. Counts465/383 unchanged. The owner asks us to stay in regular conference and guard against drift.''',encoding='utf-8',newline='\n')
 prep.write_bytes(encoded({'archive':b,'manifest':info(root/'MANIFEST.json'),'request':info(request),'fileCount':len(paths),'allMemberHashesVerified':True,'status':'Prepared; not yet submitted'}));print(json.dumps(read(prep)))

if __name__=='__main__':main()
