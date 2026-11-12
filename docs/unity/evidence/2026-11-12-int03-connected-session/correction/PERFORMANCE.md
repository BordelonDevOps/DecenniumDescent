# Corrected public session timings

The exact corrected assemblies ran 30 measured walkthroughs after one complete warm-up on the Intel Core i5-4590 Windows host using PowerShell 7.6.9 and .NET 10.0.14. The earlier regression ended before the benchmark started. The corrected regression began after the measurements and console walkthrough. Every warm run committed all 165 public inputs and reached final SHA-256 `6f1bc7afa0f5727e76dccc26d0d33911682f791a3ca3e971ca1350c64dcdd521`. The session measures actual C# submission through commitment and a permitted view. The p95 uses nearest rank. [Exact bindings](BINDINGS.json) · [Measured results](performance/results.json) · [Raw 4,950 samples](performance/samples.csv)

| Reference input | Starting revision | Median ms | P95 ms | Max ms | P95 budget ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| Opening step | 0 | 5.048 | 6.871 | 7.968 | 150 |
| First encounter attack | 9 | 5.330 | 11.571 | 23.505 | 150 |
| Mid-expedition clock advance | 49 | 72.631 | 130.112 | 168.983 | 150 |
| Stabilization milestone | 104 | 223.587 | 236.987 | 251.650 | 350 |
| Off-turn opportunity | 113 | 13.508 | 25.027 | 28.879 | 150 |
| Defender stance | 116 | 10.574 | 18.711 | 21.126 | 150 |
| Defender tactical step | 117 | 13.132 | 20.983 | 26.160 | 150 |
| Ordinary continuation | 164 | 18.680 | 50.686 | 286.319 | 150 |

The single contended correctness sample remains retained, including its 1,133.642 ms stabilization miss, 8,210.284 ms long work advance and 14,619.955 ms full restore. The isolated distribution met all eight p95 thresholds, and GPT accepted the timing evidence. Its recorded maxima include routine samples above 150 ms. [Contended sample](connected/results.json) · [GPT timing disposition](GPT_PERFORMANCE_REVIEW.md)

The isolated charter-plan submission had p95 1,463.167 ms. The three long work advances had p95 values from 3,659.727 to 3,861.787 ms. Their exact gameplay and timing remain visible for broader P1. [Full route timing](performance/results.json)

Cold start with the first view took 651.953 ms after 88.067 ms assembly loading. Warm startup median was 6.454 ms. The pending save took 20.156 ms, file load and decode 2.756 ms, and complete pending restore 7,750.837 ms. The console processed 172 lines in 25,028.232 ms, including the full pending restore. The 165 console commits match both canonical save digests. [Console result](console/results.json)
