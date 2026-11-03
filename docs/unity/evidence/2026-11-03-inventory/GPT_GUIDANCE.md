# Inventory scheduling guidance

Source: [Unity Rules Engine Development](https://chatgpt.com/c/6ae59513-3008-83e9-a5c4-8b6c5c5b4206), response `50e05aed-5887-52f3-a014-ac653b03ed81`, 2026-11-03. Codex asked for source interpretation after the owner adopted ordinary handling, portioning and intake. This response does not create additional owner approval. The bounded host supplies a fixed waterskin for drinking; vessel handover and filling remain explicitly unsupported pending their physical-container implementation.

**Correct, with two scope qualifications: FL-05 names skins/flasks specifically, and transaction atomicity must not imply uninterrupted world time.** I checked the receipt and sources at Engine `596aa5c8`.

**Filling versus handover**

[FL-05](https://github.com/BordelonDevOps/DecenniumDescent/blob/596aa5c8/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-05) establishes **one active minute to fill one skin/flask**. Transferring only part of the water still constitutes filling; the source supplies no proportional-time discount. It does not establish a universal one-minute procedure for every vessel type or volume.

Your bounded distinction is sound:

- Readied food bundles and intact filled vessels can use ordinary handling when they meet the [adopted eligibility requirements](https://github.com/BordelonDevOps/DecenniumDescent/blob/596aa5c8/docs/unity/INVENTORY_RULE_DECISIONS.md#a-ordinary-handling--adopted-prototype-policy).
- Pouring into another container uses its applicable filling profile and actual remaining capacity.
- Unsupported container relationships reject explicitly.
- Handing over a filled vessel must preserve its contents’ location/custody relationship, ownership and reservations. Moving the container cannot bypass the restriction on transferring reserved contents.

**The bounded scheduling shape is compatible with the sources**, provided these constraints hold:

1. **Book actual exclusive labor.** [FL-02/03](https://github.com/BordelonDevOps/DecenniumDescent/blob/596aa5c8/DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md#fl-03) prohibits incompatible activities during the same seconds. An actor cannot perform the handling second while also receiving intake or other incompatible labor credit. Independent companions can continue their own activities.

2. **Process the complete interval, including its endpoint.** Advance eligible continuous work to each boundary, apply the applicable boundary rules, and validate the custody change against the resulting state. A freshness deadline exactly at handling completion cannot leave the transferred food marked fresh. Expiry does not itself erase the physical item. The [crop-local ordering rules](https://github.com/BordelonDevOps/DecenniumDescent/blob/596aa5c8/docs/unity/PROTOTYPE_RULE_DECISIONS.md#camp-greens-boundary-and-failure-completion--adopted) remain local; they do not establish priority over every other event.

3. **Advance every enabled clock once.** Crop/intake processing is sufficient only where other timed systems are explicitly outside the host’s supported state. Preserve existing absolute deadlines and captured markers. In later real-time integration, the command’s second must not also be charged again by the exploration clock.

4. **Enforce the event limitation.** A fixture excluding destructive hazards and mid-operation combat entry is a legitimate bounded host. If an unsupported interruption is known to occur within the interval, stop/reject before executing beyond that supported boundary. Documenting the limitation alone would not justify completing through the event.

Tactical handling spending the existing allowance without independently advancing time is consistent. Persisted intake interruption, expiry and combat-entry behavior also match the adopted receipt.

There is **no source requirement for a separately saved intermediate handling state** in this restricted one-second host. Atomic persistence is an engineering choice; full interruption handling remains an explicit integration dependency.
