# Final Word discovery and catalog byte correspondence 476 Repack02

This read-only Final Word source-discovery pass found no qualifying changed evidence for DR217-B01. The current catalog/index still hold Final Word; the Chronicle and F51 entries are historical or adventure hooks, and the reviewed W07 Guard is explicitly a TEST_ONLY fixture at HP 0 in a dying state. The Director's retained minimum witness remains unsatisfied.

The catalog report resolves the raw hash discrepancy: the Queue476 SHA binds the exact LF snapshot in the W06 packet. On this Windows checkout, `core.autocrlf=true` produces a CRLF working-tree copy whose raw hash differs. Replacing CRLF with LF exactly reproduces the archived snapshot byte for byte. The root path and archived member point to the same Git blob at the pinned commit. No catalog, index, or queue file was changed or normalized.

The 468 caster-premise and 448 W13 owner adoptions remain exactly branch-scoped as recorded in their existing owner records. They do not accept or apply an identity and do not change Queue476. Elemental Shell remains the next queue priority; its separate B01/B02 owner-adoption gate remains unresolved.

Run the verifier from the repository root:

```powershell
python -B docs/audit/2026-10-08/full-game/director-spell-review-129/final_word_discovery_and_catalog_binding_476_repack02/VERIFY_476_REPACK02.py
```

Build the Director packet with the same source snapshots, byte-bound manifest, and reproducible ZIP:

```powershell
python -B docs/audit/2026-10-08/full-game/director-spell-review-129/final_word_discovery_and_catalog_binding_476_repack02/BUILD_PACKET_476_REPACK02.py
```

The packet includes the exact current and archived catalog/index representations, Queue476 and its pending audit, the retained Director hold, source excerpts and full bound files, and the two owner-adoption records supplied for context.
