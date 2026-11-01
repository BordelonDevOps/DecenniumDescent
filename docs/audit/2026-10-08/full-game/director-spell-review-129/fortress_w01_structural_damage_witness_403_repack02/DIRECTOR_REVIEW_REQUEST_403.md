# Director review request: PG328-W01 damage sub-witness 403 Repack02

This is a narrow corrective repack of reviewed Witness403. R1–R5 remain unchanged. The correction updates three derived carried-item sweep envelopes in W01_GEOMETRY_403.json: focus-A y=[6,11.5], pack-A y=[6,11.5], and cargo-A y=[6,12]. Each sweep is computed from all three recorded actor poses [25,10,0], [25,11,0], and [25,6,0], including the intermediate one-foot excursion. The corrected envelopes still clear the wall. No new geometry premise or rule is added.

Please verify the three R6 values, geometry verification, regenerated manifest/archive hashes, and whether any other partial-witness defect remains. This packet is for partial review only.

Current authority is Queue404: 829 applied / 19 pending / 0 accepted-unapplied. Queue counts embedded in the historical replay remain historical. This remains PARTIAL_WITNESS / NO_SEAL: do not seal W01, accept or apply Fortress, mutate canon/fixture/queue, or change other holds/seals. Geometry405's support and usable-volume proposal remains PROPOSAL_ONLY / NOT ADOPTED. Report the corrected partial-witness review and exact remaining predicates only.
