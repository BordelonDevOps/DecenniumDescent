param(
    [string]$Bindings = (Join-Path $PSScriptRoot '../../docs/unity/evidence/2026-11-04-repeating-crossbow-combat/SOURCE_BINDINGS.json'),
    [string]$ResultsRoot = (Join-Path $PSScriptRoot '../artifacts')
)
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$bindingRoot = Split-Path ([IO.Path]::GetFullPath($Bindings))
$runRoot = Join-Path ([IO.Path]::GetFullPath($ResultsRoot)) ('bindings-' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ') + '-' + [Guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory -Path $runRoot | Out-Null
$report = [ordered]@{status='FAIL';scope='Exact source snapshot, profile projection and named-test evidence validation; not full semantic or release certification';sources=0;profiles=0;rpCells=0;boundTests=0}
try {
    $binding = Get-Content -Raw -LiteralPath $Bindings | ConvertFrom-Json
    $report.bindingsSha256=(Get-FileHash -LiteralPath $Bindings -Algorithm SHA256).Hash.ToLowerInvariant()
    foreach ($source in $binding.sources) {
        $snapshot = Join-Path $bindingRoot $source.snapshot
        if ((Get-FileHash -LiteralPath $snapshot -Algorithm SHA256).Hash.ToLowerInvariant() -ne $source.sha256) { throw ('Source snapshot changed: '+$source.snapshot) }
        $report.sources++
    }
    $profileSource = @($binding.sources | Where-Object { $_.path -ceq 'DescentReviewChanges/ReviewBible/data/playtest/character_foundation.json' })
    if ($profileSource.Count -ne 1) { throw 'Exactly one character profile source binding required.' }
    $data = Get-Content -Raw -LiteralPath (Join-Path $bindingRoot $profileSource[0].snapshot) | ConvertFrom-Json
    $code = Get-Content -Raw -LiteralPath (Join-Path $repoRoot 'engine/com.decennium.foundation/Laboratory/Model/CharacterProfiles.cs')
    $rows = [regex]::Matches($code, 'case "([^"]+)": return new ClassProfile\(new\[\] \{ ([^}]+) \}, WeaveTier\.(\w+), new\[\] \{ ([^}]+) \}\);')
    if ($rows.Count -ne 17 -or $data.classes.Count -ne 17) { throw 'Expected exactly 17 class projections.' }
    $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($row in $rows) {
        $name = $row.Groups[1].Value
        if (-not $seen.Add($name)) { throw ('Duplicate profile: '+$name) }
        $profile = @($data.classes | Where-Object { $_.class -ceq $name })
        if ($profile.Count -ne 1) { throw ('Unknown profile: '+$name) }
        $prerequisites = @([regex]::Matches($row.Groups[2].Value, '"([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
        $sourcePrerequisites = @($profile[0].multiclassPrerequisites.PSObject.Properties.Name)
        if (($prerequisites -join ',') -cne ($sourcePrerequisites -join ',') -or @($profile[0].multiclassPrerequisites.PSObject.Properties | Where-Object Value -NE 13).Count -ne 0) { throw ('Prerequisite mismatch: '+$name) }
        if ($row.Groups[3].Value.ToLowerInvariant() -cne $profile[0].weaveTier) { throw ('Tier mismatch: '+$name) }
        $pools = @($row.Groups[4].Value.Split(',') | ForEach-Object { [int]$_.Trim() })
        if ($pools.Count -ne 20 -or ($pools -join ',') -cne ($profile[0].rpByClassLevel -join ',')) { throw ('RP table mismatch: '+$name) }
        $report.profiles++; $report.rpCells += $pools.Count
    }
    $tests = Get-Content -Raw -LiteralPath (Join-Path $bindingRoot $binding.validation.headless) | ConvertFrom-Json
    if ($tests.status -ne 'PASS' -or $tests.failed -ne 0 -or $tests.testsDiscovered -le 0) { throw 'Passing nonempty headless result required.' }
    foreach ($file in $tests.sourceHashes) {
        $actual = (Get-FileHash -LiteralPath (Join-Path $repoRoot ('engine/'+$file.path)) -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actual -ne $file.sha256) { throw ('Tested source changed: '+$file.path) }
    }
    $names = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($implementation in $binding.implementations) {
        if ($implementation.tests.Count -eq 0) { throw 'Implementation has no named tests.' }
        foreach ($name in $implementation.tests) {
            if (-not $names.Add($name)) { throw ('Repeated binding: '+$name) }
            $case = @($tests.cases | Where-Object { $_.Name -ceq $name })
            if ($case.Count -ne 1 -or -not $case[0].Passed) { throw ('Missing/failing test: '+$name) }
            $report.boundTests++
        }
        foreach ($path in $implementation.code) {
            if (-not (Test-Path -LiteralPath (Join-Path $repoRoot ('engine/com.decennium.foundation/'+$path)))) { throw ('Missing implementation: '+$path) }
        }
    }
    $report.status='PASS'
} catch { $report.error=$_.ToString() }
finally {
    $report.finishedUtc=[DateTime]::UtcNow.ToString('o')
    $outputFile=Join-Path $runRoot 'results.json'
    $report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $outputFile -Encoding utf8
    Write-Output ($report.status+': rule bindings; '+$outputFile)
}
if ($report.status -ne 'PASS') { Write-Error $report.error; exit 1 }
