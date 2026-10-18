# Verifier execution notes

The independent verifier reads the supplied archives directly and never imports or executes their project scripts. All eight accepted artifacts remain unmodified.

An initial verifier draft classified index membership by substring and therefore treated the existing `receipt-only-post-push-cosmology` Blink entry as an unknown category. Inspection of the full index showed 525 `reviewed-authored-operational-playtest`, 322 `pending-authored-procedure`, and one receipt-only entry with a null procedure pointer and `blocked-pending-operational-review` source status. The verifier was corrected to count that explicitly blocked receipt-only record as pending and to fail on any unknown status; no source/index change or cosmology approval was made. The final run has 704 checks and zero failures.

Checks on procedure/case equality and chapter flow use full JSON objects, full procedure strings, complete access tables, full routed shared appendices, complete rendered metadata outlines and full parsed Director case JSON. They are not ID censuses. Count arithmetic, equality and hashing are not gameplay or balance tests.

Optional original archives anchor all ten prior-return members, 72 frozen conference sources and 34 accepted-context sources. When those archives are omitted, the verifier explicitly records those extra anchors as not checked and has fewer checks; it still verifies the pinned Exact13 ZIP and its internal complete-value lineage.
