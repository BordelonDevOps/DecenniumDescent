# Direct request verifier development probes

These are development failures, not final passing verification. The engine source and the full regression assemblies were unchanged throughout.

The first direct request run stopped while identifying loaded assemblies: Roslyn assembly names do not match the artifact filenames. The verifier now identifies each loaded assembly by its exact `Location` and retains its SHA-256 and module ID.

The second run completed the partitioned `completion` branch and then stopped in `whole` while saving a pre-request snapshot over the repeatedly reused `before-request.ddsave` filename. PowerShell reported at `Test-DirectRequestParity.ps1:80`:

> Exception calling "Save" with "1" argument(s): "Unable to remove the file to be replaced."

The verifier now uses a distinct pre-request, post-request and restored-observation file for each input index. This preserves each rejected/retried state's evidence independently. It does not establish or repair the cause of the earlier OS file replacement exception. No automatic retry, file deletion, persistence source change or save-format change was introduced.

A separate repeated-destination probe uses the same uninstrumented Core and Persistence assemblies. It alternates the actual pending and completed Short Rest snapshots through 32 writes to one path and verifies all 31 backups equal the immediately preceding complete snapshot. This probe passed and did not reproduce the exception. Its results are retained separately; a non-reproduction is not an explanation of the original I/O failure.

The first launch of that diagnostic used the wrong C# namespace for `FileSaveStore` and stopped before loading state or saving files. The corrected launch uses `Decennium.Foundation.FileSaveStore`.
