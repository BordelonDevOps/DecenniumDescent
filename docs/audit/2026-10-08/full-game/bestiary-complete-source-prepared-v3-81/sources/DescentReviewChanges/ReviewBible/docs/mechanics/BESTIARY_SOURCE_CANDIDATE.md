# Bestiary source candidate

**Prepared for review; not installed in the companion and not operationally approved.**

This candidate preserves all 67 Known Descent source dossiers, including 66 stat blocks and one historical record. It retains the exact UTF-8 source text and file hash for every dossier. The player projection includes only the 26 dossiers explicitly marked public by the existing build-filter index. The internal registry also retains 39 restricted dossiers, two dossiers lacking filter routes, and metadata for the five sealed routes; sealed contents are not transformed or reviewed.

Each stat-bearing record includes the printed body/CR/XP/AC/HP/speed/Save DC fields, all six ability scores and printed modifiers, resistance/immunity labels, tactical-vulnerability text, traits and actions. These are source fields, not executable combat rules. Tactical vulnerability is not automatically a damage vulnerability; the four disease immunity labels remain literal source labels awaiting an effect-category binding.

All 178 harvest-component occurrences remain in source order. Of these, 148 print a percentage and gp base value; 30 say Director-set and retain null numeric values. Crystal Shardling and Pact Automaton Sentinel provide no harvest skill/DC/base time, so those fields remain null. No output quantity, percentage roll procedure, availability, extraction weight or market price rule is inferred.

The historical disaster record has statBlock: null and retains its existing restricted route. It cannot become a creature through default Medium/Unknown/CR0 values. Both Fracture-Kin compatibility aliases are retained with their existing V6 provenance; the classic-label source dossiers remain separate, preserving the identity question for migration review.

Three source tactics references remain unresolved: Cave Bear/Bite, Dimetrodon/Tail Sweep and Giant Constrictor Snake/Constrict. No action was fabricated. The candidate also records two missing publication routes, two alias/source overlaps, four immunity-label mappings and two missing harvest procedures. Complete action timing, targeting, costs, encounter integration and balance remain open.

The live 707-record dataset, its workbooks, current consumers and all original source dossiers are unchanged. Candidate generation does not call the existing ingestion or combat-generation scripts. Do not swap this file into the companion until GPT review, saved-identity migration, loot conversion and public/licensed/Director routing are resolved and validated.

- Public candidate: `data/playtest/bestiary_public_source_candidate.json`.
- Internal source registry: `data/director/bestiary_source_candidate_internal.json`.
- Source and field validation: `docs/audit/2026-10-08/full-game/BESTIARY_SOURCE_CANDIDATE_VALIDATION.json`.
- Rebuild with `tools/build_bestiary_source_candidate.py`; rebuilding refuses to overwrite altered candidate artifacts or a reviewed revision.

No source deletion or GitHub push has occurred. Cosmology remains deferred until after verified delivery.
