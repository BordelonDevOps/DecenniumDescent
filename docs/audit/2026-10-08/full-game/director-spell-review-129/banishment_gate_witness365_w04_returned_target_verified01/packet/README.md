# Banishment Gate W04 — returned target and later crossing (TEST_ONLY)

This witness forks the exact successful Guard admission at W06 event `BG-W06-365:7` from Director-sealed Repack06 (5f39d612332ffbfa6d64b888e6ae481c886cd2fa79e1d24f30825a4d464061f6). The same living Guard, original Gate creator W20, encounter ID, cell, admission receipt, and already-spent creator/target/encounter claim are carried forward.

At the target's independent 60-second cell deadline, the mandatory closure returns that same living identity to the fixed origin anchor. The parent Gate remains active until its separate 600-second deadline. On Guard's scheduled turn at 62.0, it then pays five feet to cross the portal in the opposite direction. The already-spent claim prevents a second cell; the movement completes, with no new claim. A duplicate delivery of the later crossing ID and a delayed duplicate of the original successful crossing both return their existing receipts without state mutation or renewed admission.

The case is a hypothetical continuation of the existing explicitly authorized TEST_ONLY W06 fixture. It asserts no campaign event, changes no canon, accepts/applies no spell identity, and leaves Queue361 unchanged. Director W04 review is required.
