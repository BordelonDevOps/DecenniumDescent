# Corrected Ferry runtime: terminal full regression

Original run `72f6bdda13924fad8eb5b516ec19018b` completed **1,584/1,584 cases with zero failures**. All six original workers wrote their terminal records and exited. No restart, replacement shard or substituted case set was used.

This qualifies C# tree `c8ffee78d5047131317ff923c8e3a575b6c51f3a`, including the public Dash correction. The original1,576 predecessor cases retain their authenticated names/order/shard membership; eight substantive Ferry cases are added. The earlier db91/1,583 result remains separate historical evidence.

[Retention metadata](dash-regression-checkpoint/RETENTION.json) reconciles all original launch/worker identities, ordered journals, terminal counts and journal hashes,468 Git-bound compilation inputs, and four frozen assembly hashes/MVID bindings against the retained public-Dash build. All252 artifact files from the eight new cases are included. Earlier predecessor artifact trees remain local rather than being duplicated. The current engine-path difference from the frozen tree is only the separately qualified console host script; no C# source changed during this run.

[Archive](dash-regression-checkpoint/full-regression.zip):1,892,991 bytes;312 members; SHA256 `478870d5fb2ca619e3401db25a4488d68cbb9606c1c401b2374501d8a89ce771`. [Member manifest](dash-regression-checkpoint/MEMBERS.json). [Collector](support/Retain-FerryDashRegression.py) SHA256 `e35adc1b74b7b807fa5bd25a53a71adc6960b85db826ed8fae96f1d62455eb93`.

The collector's `fivePaths:false` describes its own regression-only scope. The separately retained [five-path packet](FIVE_PATH_CHECKPOINT.md) passed. These passes do not close the remaining actual acceptance-gap review or constitute TAC-10/whole-engine acceptance. The owner requires finishing TAC-10 and then stopping; no successor work is authorized.
