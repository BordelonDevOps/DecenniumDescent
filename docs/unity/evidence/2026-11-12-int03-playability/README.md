# INT-03 P1 engineering packet

The accepted TAC-10 assemblies ran 40 sequential measurements with no competing regression or compilation jobs. The inputs are prefixes reconstructed from the authentic 165-receipt continued save. The full reconstructed bytes matched the original. Every measured command then ran through the public `Simulation.Execute` path and matched its next recorded state. The test fixture factory supplies the original selected content. The measured commands and storage use the normal runtime APIs. [Measurement script](Measure-AcceptedCommandPath.ps1) · [Raw measurements](BASELINE_RESULTS.json)

The machine is an Intel Core i5-4590 at 3.30 GHz with four logical processors, Windows 10.0.19045 and .NET 10.0.14. Each checkpoint has five measurements after one discarded warm-up. Values below are elapsed milliseconds. The maximum is retained alongside each execute median because five samples provide a limited distribution.

| Workload | Starting revision | Resolver median | Full policy validation median | Public execute median | Public execute maximum |
| --- | ---: | ---: | ---: | ---: | ---: |
| Opening step | 0 | 0.398 | 3.487 | 3.138 | 5.062 |
| First encounter attack | 9 | 0.736 | 11.191 | 13.092 | 13.838 |
| Mid-expedition clock advance | 49 | 30.420 | 682.002 | 796.248 | 1,239.489 |
| Actual stabilization milestone | 104 | 99.495 | 4,887.168 | 5,146.580 | 5,527.166 |
| Off-turn opportunity | 113 | 1.007 | 5,536.047 | 5,635.477 | 5,701.766 |
| Defender stance | 116 | 0.355 | 5,538.864 | 5,549.519 | 5,678.018 |
| Defender tactical step | 117 | 0.848 | 5,450.482 | 5,659.150 | 5,909.583 |
| Ordinary continuation | 164 | 2.270 | 5,526.356 | 5,608.590 | 5,916.818 |

At revision 113 the median detached copy was 0.034 ms, structural validation 0.803 ms, projection 0.246 ms, pre-roll admission 0.171 ms, canonical encoding 1.738 ms, disk save 15.683 ms, disk load with decoding 2.283 ms, and full restore validation 5,607.948 ms. Independent history reconstruction tracked the several-second policy validation cost. Its timing includes the PowerShell replay loop and omits the final byte comparison. The components are independent samples, and policy validation includes replay and canonical encoding, so their timings cannot be added together.

The report binds the exact accepted implementation, source archive, four assemblies and input save. Its SHA-256 is `a4d079e93388aafd052427d95ae3ca33f71e17daa3d6578be1e1f0485f7df55f`. The proposed live validation contract keeps full external restoration and proves each successor using canonical bytes from a sealed prior checkpoint. The session reconciliation names the separately supported behavior and the current first-opponent authority gap. [Validation proposal](VALIDATION_PROPOSAL.md) · [Session scope](SESSION_SCOPE.md)
