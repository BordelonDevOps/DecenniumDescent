param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Campaigns,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run=[IO.Directory]::CreateDirectory([IO.Path]::GetFullPath($Run)).FullName
$rows=[Collections.Generic.List[object]]::new()
foreach($campaign in (Get-Content -LiteralPath $Campaigns -Raw|ConvertFrom-Json)) {
    $folder=[IO.Directory]::CreateDirectory((Join-Path $Run $campaign.name)).FullName
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot 'Export-PostRecoveryTrace.ps1') -AssemblyRoot $AssemblyRoot -FinalSave $campaign.final -CheckpointDirectory $campaign.checkpoints -Run (Join-Path $folder 'trace')|Tee-Object -FilePath (Join-Path $folder 'export.log')
    if($LASTEXITCODE-ne0){throw "Export failed: $($campaign.name)"}
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot 'Test-PostRecoveryPaths.ps1') -AssemblyRoot $AssemblyRoot -TraceRoot (Join-Path $folder 'trace') -Run (Join-Path $folder 'paths')|Tee-Object -FilePath (Join-Path $folder 'paths.log')
    if($LASTEXITCODE-ne0){throw "Paths failed: $($campaign.name)"}
    $rows.Add(@{name=$campaign.name;report=(Join-Path $folder 'paths/results.json')})
    $rows|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $Run 'progress.json') -Encoding utf8
}
@{status='PASS';scope='Development connected campaigns; final frozen source qualification is separate';campaigns=@($rows)}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
