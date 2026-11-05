param(
    [string]$ResultsRoot = (Join-Path $PSScriptRoot '../artifacts'),
    [switch]$RefreshSourceBindings
)
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$runRoot = Join-Path ([IO.Path]::GetFullPath($ResultsRoot)) ('class-advancement-' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ') + '-' + [Guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory -Path $runRoot | Out-Null
$sourceRevision = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
$manifestRelative = 'DescentReviewChanges/ReviewBible/data/public/class_playtests/manifest.json'
$report = [ordered]@{status='FAIL';sourceRevision=$sourceRevision;sources=0;structuredRows=0;narrativeExceptionRows=0;totalRows=0;cardOptions=0;sourceBindingsRefreshed=$false}

function Get-GitBlobBytes([string]$Blob) {
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = 'git'
    $start.Arguments = 'cat-file blob ' + $Blob
    $start.UseShellExecute = $false
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    if (-not $process.Start()) { throw ('Could not start git cat-file for blob ' + $Blob) }
    $stream = [IO.MemoryStream]::new()
    $process.StandardOutput.BaseStream.CopyTo($stream)
    $errorText = $process.StandardError.ReadToEnd()
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) { throw ('git cat-file failed for blob ' + $Blob + ': ' + $errorText) }
    $bytes = $stream.ToArray()
    $stream.Dispose()
    $process.Dispose()
    return ,$bytes
}

function Get-PinnedBlob([string]$Revision, [string]$RelativePath) {
    $spec = $Revision + ':' + $RelativePath
    $blob = (git rev-parse --verify $spec).Trim()
    if ($LASTEXITCODE -ne 0 -or $blob -notmatch '^[0-9a-f]{40}$') { throw ('Could not resolve pinned Git source ' + $spec) }
    return $blob
}

function Source-JsonField($Object,[string]$Name) {
    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) { return 'null' }
    return ConvertTo-Json -InputObject $property.Value -Depth 32 -Compress
}

function Source-Base64([string]$Value) {
    return [Convert]::ToBase64String([Text.UTF8Encoding]::new($false).GetBytes($Value))
}

function Decode-CSharpLiteral([string]$Value) {
    $builder = [Text.StringBuilder]::new()
    for ($i=0; $i -lt $Value.Length; $i++) {
        if ($Value[$i] -ne '\') { [void]$builder.Append($Value[$i]); continue }
        $i++
        if ($i -ge $Value.Length) { throw 'Incomplete C# string escape in generated option catalog.' }
        switch ($Value[$i]) {
            'n' { [void]$builder.Append("`n") }
            'r' { [void]$builder.Append("`r") }
            't' { [void]$builder.Append("`t") }
            '\' { [void]$builder.Append('\') }
            '"' { [void]$builder.Append('"') }
            default { throw ('Unknown C# string escape: \' + $Value[$i]) }
        }
    }
    return $builder.ToString()
}

try {
    $manifestBlob = Get-PinnedBlob $sourceRevision $manifestRelative
    $manifestBytes = Get-GitBlobBytes $manifestBlob
    $manifestText = [Text.UTF8Encoding]::new($false,$true).GetString($manifestBytes)
    $manifest = $manifestText | ConvertFrom-Json
    if ($manifest.classes.Count -ne 17) { throw 'Expected the pinned 17-class manifest.' }

    $expectedSources = [Collections.Generic.List[string]]::new()
    $expectedRows = [Collections.Generic.List[string]]::new()
    $expectedOptions = [Collections.Generic.List[string]]::new()
    foreach ($entry in $manifest.classes) {
        $slug = ($entry.class -replace ' ','-').ToLowerInvariant()
        $relative = if ($entry.class -eq 'Bard') {
            'DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Bard_Playtest_v0_1.json'
        } else {
            'DescentReviewChanges/ReviewBible/data/public/class_playtests/' + $slug + '.json'
        }
        $blob = Get-PinnedBlob $sourceRevision $relative
        $bytes = Get-GitBlobBytes $blob
        $sha = [BitConverter]::ToString([Security.Cryptography.SHA256]::HashData($bytes)).Replace('-','').ToLowerInvariant()
        $sourceText = [Text.UTF8Encoding]::new($false,$true).GetString($bytes)
        $source = $sourceText | ConvertFrom-Json
        $expectedSources.Add($entry.class + '|' + $relative + '|' + $sha + '|' + $blob + '|' + $source.status)
        $report.sources++
        if ($source.schedule -and @($source.schedule).Count -gt 0) {
            $index = 0
            foreach ($row in $source.schedule) {
                $bands = if ($row.bands.Count -gt 0) { $row.bands -join ',' } else { '-' }
                $asi = if ($row.asiOrFeat) { '1' } else { '0' }
                $expectedRows.Add('S|' + $entry.class + '|' + $row.classLevel + '|' + $row.choose + '|' + $bands + '|' +
                    $row.minimumActives + '|' + $asi + '|/schedule/' + $index)
                $index++
                $report.structuredRows++
            }
        } elseif ($source.exceptionSchedule) {
            foreach ($property in ($source.exceptionSchedule.PSObject.Properties | Sort-Object { [int]$_.Name })) {
                $expectedRows.Add('E|' + $entry.class + '|' + [int]$property.Name + '|/exceptionSchedule/' + [int]$property.Name)
                $report.narrativeExceptionRows++
            }
        } else { throw ('No structured or narrative schedule exists for ' + $entry.class) }
        for ($cardIndex=0; $cardIndex -lt @($source.cards).Count; $cardIndex++) {
            $card = $source.cards[$cardIndex]
            $kindProperty = if ($null -ne $card.PSObject.Properties['sourceKind']) { 'sourceKind' }
                elseif ($null -ne $card.PSObject.Properties['kind']) { 'kind' } else { '' }
            $kindValue = if ($kindProperty -eq '') { '' } else { [string]$card.$kindProperty }
            $minimumLevel = if ($null -eq $card.minimumClassLevel) { 1 } else { [int]$card.minimumClassLevel }
            $fields = @(
                [string]$entry.class,[string]$card.id,[string]$card.name,[string]$card.band,[string]$card.path,
                $minimumLevel.ToString([Globalization.CultureInfo]::InvariantCulture),[string]$card.acquisition,$kindProperty,$kindValue,
                [string]$card.activation,(Source-Base64 (Source-JsonField $card 'prerequisite')),
                (Source-Base64 (Source-JsonField $card 'prerequisites')),[string]$card.designStatus,$relative,
                ('/cards/' + $cardIndex.ToString([Globalization.CultureInfo]::InvariantCulture))
            )
            $expectedOptions.Add($fields -join '|')
        }
    }

    $codePath = Join-Path $repoRoot 'engine/com.decennium.foundation/Laboratory/Model/ClassAdvancementScheduleCatalog.cs'
    $code = [IO.File]::ReadAllText($codePath)
    $sourceStart = $code.IndexOf('        private const string SourceFilesData=',[StringComparison]::Ordinal)
    $rowsStart = $code.IndexOf('        private static readonly string[] EncodedRows=',[StringComparison]::Ordinal)
    if ($sourceStart -lt 0 -or $rowsStart -le $sourceStart) { throw 'Generated catalog source sections were not found.' }

    if ($RefreshSourceBindings) {
        $builder = [Text.StringBuilder]::new()
        [void]$builder.AppendLine('        private const string SourceFilesData=')
        for ($i=0; $i -lt $expectedSources.Count; $i++) {
            $suffix = if ($i -lt $expectedSources.Count - 1) { '" +' } else { '";' }
            [void]$builder.AppendLine('            "' + $expectedSources[$i] + ';' + $suffix)
        }
        $replacement = $builder.ToString()
        $code = $code.Substring(0,$sourceStart) + $replacement + $code.Substring($rowsStart)
        [IO.File]::WriteAllText($codePath,$code,[Text.UTF8Encoding]::new($false))
        $report.sourceBindingsRefreshed = $true
    }

    $sourceStart = $code.IndexOf('        private const string SourceFilesData=',[StringComparison]::Ordinal)
    $rowsStart = $code.IndexOf('        private static readonly string[] EncodedRows=',[StringComparison]::Ordinal)
    $sourceBlock = $code.Substring($sourceStart,$rowsStart-$sourceStart)
    $sourceData = @([regex]::Matches($sourceBlock,'"([^"\r\n]+)"') | ForEach-Object { $_.Groups[1].Value })
    $actualSources = @($sourceData | ForEach-Object { $_.Split(';',[StringSplitOptions]::RemoveEmptyEntries) })
    $rowsEnd = $code.IndexOf('        };',$rowsStart,[StringComparison]::Ordinal)
    if ($rowsEnd -le $rowsStart) { throw 'Generated schedule row terminator was not found.' }
    $rowsBlock = $code.Substring($rowsStart,$rowsEnd-$rowsStart)
    $actualRows = @([regex]::Matches($rowsBlock,'"([SE]\|[^"\r\n]+)"') | ForEach-Object { $_.Groups[1].Value })
    $optionsCodePath = Join-Path $repoRoot 'engine/com.decennium.foundation/Laboratory/Model/ClassAdvancementOptionCatalog.cs'
    $optionsCode = [IO.File]::ReadAllText($optionsCodePath)
    $optionsStart = $optionsCode.IndexOf('        private static readonly string[] EncodedOptions=',[StringComparison]::Ordinal)
    if ($optionsStart -lt 0) { throw 'Generated class-card option section was not found.' }
    $optionsEnd = $optionsCode.IndexOf('        };',$optionsStart,[StringComparison]::Ordinal)
    if ($optionsEnd -le $optionsStart) { throw 'Generated class-card option section terminator was not found.' }
    $optionsBlock = $optionsCode.Substring($optionsStart,$optionsEnd-$optionsStart)
    $actualOptions = @([regex]::Matches($optionsBlock,'"((?:\\.|[^"\\])*)"') | ForEach-Object { Decode-CSharpLiteral $_.Groups[1].Value })

    if ([string]::Join("`n",$actualSources) -cne [string]::Join("`n",$expectedSources.ToArray())) { throw 'Embedded source paths, raw-byte SHA-256 hashes, Git blobs, statuses, or manifest order differ from the pinned Git sources.' }
    if ([string]::Join("`n",$actualRows) -cne [string]::Join("`n",$expectedRows.ToArray())) { throw 'Embedded 340-row schedule projection differs from the pinned JSON.' }
    if ([string]::Join("`n",$actualOptions) -cne [string]::Join("`n",$expectedOptions.ToArray())) { throw 'Embedded class-card options differ from the pinned class JSON.' }
    $report.totalRows = $actualRows.Count
    $report.cardOptions = $actualOptions.Count
    if ($report.sources -ne 17 -or $report.structuredRows -ne 280 -or $report.narrativeExceptionRows -ne 60 -or $report.totalRows -ne 340) {
        throw 'The class schedule projection is incomplete.'
    }
    if ($report.cardOptions -ne 1223) { throw 'The class-card option projection is incomplete.' }
    $report.status = 'PASS'
} catch { $report.error = $_.ToString() }
finally {
    $report.finishedUtc = [DateTime]::UtcNow.ToString('o')
    $outputFile = Join-Path $runRoot 'results.json'
    $report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $outputFile -Encoding utf8
    Write-Output ($report.status + ': class advancement source projection; ' + $outputFile)
}
if ($report.status -ne 'PASS') { Write-Error $report.error; exit 1 }
