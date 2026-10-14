# Canon registry

**One canonical manifest** owns domain → authoritative-file pointers. Domain facts live in those files, not in duplicate SoT documents.

| File | Role |
|------|------|
| [`CANON_MANIFEST.json`](./CANON_MANIFEST.json) | Registry: domain, paths, version, visibility, status, supersedes, notes |
| [`REPOSITORY_PROMOTION.md`](./REPOSITORY_PROMOTION.md) | main / ReviewBible / DescentReviewChanges / incoming hierarchy |

**Ops protocol** (STOP-and-ask, override tracker): [`../mechanics/CONTINUITY_SOURCE_OF_TRUTH.md`](../mechanics/CONTINUITY_SOURCE_OF_TRUTH.md)

**Assembled review build:** `DescentReviewChanges/ReviewBible/` — synchronized from main + promoted packs; not a second owner of the same domain facts.

Owner spoken locks still outrank for *intent*, but do not auto-edit locked books.
