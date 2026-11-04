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
function Get-ContentManifestDigest($manifest) {
    $operationOrder = @{ PortableInteraction=0; PortableEquipment=1; ClubAttack=2; FormulaResearch=3; FormulaCopy=4; Manufacture=5; UseProducedItem=6; ToolRepair=7 }
    $authorityOrder = @{ CanonicalSource=0; ReviewedAuthoredPlaytest=1; PrototypeFixture=2 }
    $visibilityOrder = @{ Public=0; Internal=1 }
    $accessOrder = @{ VisibleWithoutGrant=0; RequiresExistingKnowledge=1; InternalOnly=2 }
    $valueOrder = @{ Value=0; Unknown=1; Null=2; NotApplicable=3; Unsupported=4 }
    $canonicalEntries = [Collections.Generic.List[string]]::new()
    foreach ($entry in $manifest.entries) {
        $handlers = @($entry.handlers | Sort-Object { [int]$operationOrder[$_.operation] } | ForEach-Object {
            [string]$operationOrder[$_.operation] + '@' + $_.id + '@' + $_.version.ToString([Globalization.CultureInfo]::InvariantCulture)
        }) -join ','
        $operations = @($entry.operations | ForEach-Object { [int]$operationOrder[$_] } | Sort-Object | ForEach-Object { $_.ToString([Globalization.CultureInfo]::InvariantCulture) }) -join ','
        $aliases = [string[]]@($entry.runtimeAliases); [Array]::Sort($aliases,[StringComparer]::Ordinal)
        $authority = [string[]]@($entry.authorityReferences); [Array]::Sort($authority,[StringComparer]::Ordinal)
        $sourceMass = [string]$valueOrder[$entry.sourceMass.state] + ':' + $entry.sourceMass.value
        $operationalMass = [string]$valueOrder[$entry.operationalMass.state] + ':' + $entry.operationalMass.value
        $testOnly = if ([bool]$entry.testOnly) { '1' } else { '0' }
        $fields = @($entry.domain,$entry.semanticId,$entry.sourceRevision,$entry.sourcePath,$entry.sourceBlobId,$entry.jsonPointer,
            ([string]$authorityOrder[$entry.authorityStatus]),([string]$visibilityOrder[$entry.visibility]),([string]$accessOrder[$entry.viewerAccess]),
            $sourceMass,$operationalMass,$handlers,$testOnly,$operations,($aliases -join ','),($authority -join ','))
        $canonicalEntries.Add(($fields -join '|'))
    }
    $canonicalArray = $canonicalEntries.ToArray(); [Array]::Sort($canonicalArray,[StringComparer]::Ordinal)
    $bytes = [Text.Encoding]::UTF8.GetBytes('content-manifest-v1|' + $manifest.schemaVersion + '|' + ($canonicalArray -join "`n"))
    $sha = [Security.Cryptography.SHA256]::Create()
    try { [Convert]::ToHexString($sha.ComputeHash($bytes)).ToLowerInvariant() } finally { $sha.Dispose() }
}
function Test-AuthorityReference([string]$reference, [string]$repositoryRoot) {
    $match = [regex]::Match($reference,'^(?<revision>[^:]+):(?<path>.+)@(?<blob>[0-9a-f]{40})(?:#.*)?$')
    if (-not $match.Success) { return $false }
    $spec = $match.Groups['revision'].Value + ':' + $match.Groups['path'].Value
    $actualLines = @(& git -C $repositoryRoot rev-parse $spec 2>$null)
    $gitExit = $LASTEXITCODE
    if ($gitExit -ne 0 -or $actualLines.Count -ne 1) { return $false }
    return ([string]$actualLines[0]).Trim() -ceq $match.Groups['blob'].Value
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
    $contentManifestPath = Join-Path $packageRoot 'Laboratory/Content/test-only-content-manifest.json'
    $contentManifest = Get-Content -Raw -LiteralPath $contentManifestPath | ConvertFrom-Json
    $resolverSource = Get-Content -Raw -LiteralPath (Join-Path $packageRoot 'Laboratory/Model/SourceContentResolution.cs')
    $trustedDigest = [regex]::Match($resolverSource,'TrustedDigest = "([0-9a-f]{64})"')
    Check ($trustedDigest.Success -and $contentManifest.manifestDigest -eq $trustedDigest.Groups[1].Value -and
        $contentManifest.schemaVersion -eq 1 -and $contentManifest.entries.Count -le 64) 'Finite source manifest matches trusted build digest'
    Check ((Get-ContentManifestDigest $contentManifest) -eq $contentManifest.manifestDigest) 'Serialized content bindings reproduce their immutable manifest digest'
    Check ($contentManifest.executionScope -eq 'TEST_ONLY' -and -not $contentManifest.releaseApproved -and
        -not $contentManifest.runtimeSelectionEnabled -and $contentManifest.playerKnowledgeGrants.Count -eq 0 -and
        $contentManifest.entries.Where({$_.domain -eq 'crafting-review'}).Count -eq 1 -and
        $contentManifest.entries.Where({$_.domain -eq 'recipe-result' -and $_.semanticId -eq '' -and $_.jsonPointer -eq '/recipes/3/resultItem'}).Count -eq 1) 'Manifest keeps test-only scope, internal visibility, result pointer and knowledge grants separate'
    $repositoryRoot = Split-Path -Parent $engineRoot
    $authorityReferences = @($contentManifest.entries | ForEach-Object { $_.authorityReferences } | Sort-Object -Unique)
    if ($authorityReferences.Count -eq 0) { throw 'Manifest has no pinned authority references' }
    foreach ($reference in $authorityReferences) {
        if (-not (Test-AuthorityReference ([string]$reference) $repositoryRoot)) { throw ('Manifest authority reference mismatch: ' + $reference) }
    }
    $firstReference = [string]$authorityReferences[0]
    $wrongBlob = if ($firstReference -match '@0{40}(?:#|$)') { 'f' * 40 } else { '0' * 40 }
    $mismatchedReference = [regex]::Replace($firstReference,'@[0-9a-f]{40}(?=#|$)','@' + $wrongBlob)
    Check (-not (Test-AuthorityReference $mismatchedReference $repositoryRoot)) 'Authority-reference verification rejects a mismatched pinned Git blob'
    Check $true 'Every authority-reference locator resolves to its pinned Git blob'
    $sourceGroups = @($contentManifest.entries | Group-Object sourceRevision,sourcePath,sourceBlobId)
    foreach ($group in $sourceGroups) {
        $entry = $group.Group[0]
        $actualBlobLines = @(& git -C $repositoryRoot rev-parse ($entry.sourceRevision + ':' + $entry.sourcePath) 2>$null)
        $gitExit = $LASTEXITCODE
        $actualBlob = if ($actualBlobLines.Count -eq 1) { [string]$actualBlobLines[0] } else { '' }
        if ($gitExit -ne 0 -or $actualBlob.Trim() -ne $entry.sourceBlobId) { throw ('Manifest source blob mismatch: ' + $entry.sourcePath) }
    }
    Check ($sourceGroups.Count -ge 4) 'Every source locator resolves to its pinned Git blob'
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
