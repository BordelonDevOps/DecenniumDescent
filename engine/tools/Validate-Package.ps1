param([string]$ResultsRoot = (Join-Path $PSScriptRoot '../artifacts'))
$ErrorActionPreference = 'Stop'
$engineRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$packageRoot = Join-Path $engineRoot 'com.decennium.foundation'
$outputDirectory = Join-Path ([IO.Path]::GetFullPath($ResultsRoot)) ('static-' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ') + '-' + [Guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory -Path $outputDirectory | Out-Null
$checks = [Collections.Generic.List[object]]::new()
function Check([bool]$condition, [string]$name) {
    $checks.Add(@{ name=$name; passed=$condition })
    if (-not $condition) { throw $name }
}
$report = [ordered]@{status='FAIL';scope='Static package structure only; not Unity import, compilation or release-build validation';checks=$checks}
try {
    $package = Get-Content -Raw -LiteralPath (Join-Path $packageRoot 'package.json') | ConvertFrom-Json
    Check ($package.name -eq 'com.decennium.foundation') 'Package identity parses and matches assembly paths'
    $items = @(Get-ChildItem -LiteralPath $packageRoot -Recurse -Force)
    $assets = @($items | Where-Object { $_.Extension -ne '.meta' })
    Check (@($assets | Where-Object { -not (Test-Path -LiteralPath ($_.FullName + '.meta') -PathType Leaf) }).Count -eq 0) 'Every package asset and subdirectory has metadata'
    $metas = @($items | Where-Object { -not $_.PSIsContainer -and $_.Extension -eq '.meta' })
    $guids = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($meta in $metas) {
        if (-not (Test-Path -LiteralPath $meta.FullName.Substring(0,$meta.FullName.Length-5))) { throw ('Orphan metadata: ' + $meta.FullName) }
        $match = [regex]::Match((Get-Content -Raw -LiteralPath $meta.FullName),'(?m)^guid: ([0-9a-f]{32})\s*$')
        if (-not $match.Success -or -not $guids.Add($match.Groups[1].Value)) { throw ('Invalid or duplicate GUID: ' + $meta.FullName) }
    }
    Check $true 'Metadata has unique valid GUIDs and no orphans'
    $assemblies = @{}
    foreach ($file in @($items | Where-Object Extension -eq '.asmdef')) {
        $definition = Get-Content -Raw -LiteralPath $file.FullName | ConvertFrom-Json
        if ($assemblies.ContainsKey($definition.name)) { throw 'Duplicate assembly name' }
        $assemblies[$definition.name] = $definition
    }
    Check ($assemblies.Count -eq 7) 'Seven distinct assembly definitions parse'
    foreach ($assembly in $assemblies.Values) {
        foreach ($reference in $assembly.references) {
            if (-not $assemblies.ContainsKey($reference)) { throw ('Unresolved package assembly reference: ' + $reference) }
        }
    }
    function Visit([string]$name, [string[]]$ancestors) {
        if ($ancestors -contains $name) { throw ('Assembly cycle: ' + $name) }
        foreach ($reference in $assemblies[$name].references) { Visit $reference ($ancestors + $name) }
    }
    foreach ($name in $assemblies.Keys) { Visit $name @() }
    Check $true 'Assembly references resolve without cycles'
    Check ($assemblies['Decennium.Foundation.Core'].noEngineReferences -and $assemblies['Decennium.Foundation.Core'].references.Count -eq 0 -and
        $assemblies['Decennium.Foundation.Persistence'].noEngineReferences -and
        ($assemblies['Decennium.Foundation.Persistence'].references -join ',') -eq 'Decennium.Foundation.Core') 'Core and persistence enforce engine-free dependency boundaries'
    $pureSources = @(Get-ChildItem -LiteralPath (Join-Path $packageRoot 'Runtime') -Recurse -Filter '*.cs')
    $forbidden = @($pureSources | Select-String -Pattern 'UnityEngine|UnityEditor|DateTime|Stopwatch|System\.Random')
    Check ($forbidden.Count -eq 0) 'Authoritative code has no Unity, wall-clock or System.Random dependency'
    foreach ($name in @('Decennium.Foundation.LabModel','Decennium.Foundation.UnityLaboratory')) {
        $constraints = $assemblies[$name].defineConstraints
        if ($constraints -notcontains 'DECENNIUM_TEST_ONLY' -or $constraints -notcontains 'UNITY_EDITOR || DEVELOPMENT_BUILD') { throw ('Missing laboratory exclusion: ' + $name) }
    }
    foreach ($name in @('Decennium.Foundation.Editor','Decennium.Foundation.LabBuilder','Decennium.Foundation.Tests')) {
        if (($assemblies[$name].includePlatforms -join ',') -ne 'Editor') { throw ('Editor-only assembly escapes: ' + $name) }
    }
    Check $true 'Laboratory assemblies require opt-in and editor/development; editor and test assemblies are editor-only'
    $report.status = 'PASS'
    $report.packageAssets = $assets.Count
    $report.uniqueGuids = $guids.Count
    $report.sourceHashes = @($items | Where-Object { -not $_.PSIsContainer } | ForEach-Object {
        @{ path=[IO.Path]::GetRelativePath($engineRoot,$_.FullName); sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
} catch { $report.error = $_.ToString() }
finally {
    $report.finishedUtc = [DateTime]::UtcNow.ToString('o')
    $resultFile = Join-Path $outputDirectory 'results.json'
    $report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $resultFile -Encoding utf8
    Write-Output ($report.status + ': static package checks; ' + $resultFile)
}
if ($report.status -ne 'PASS') { Write-Error $report.error; exit 1 }
