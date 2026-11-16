param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$OutputDirectory)
$ErrorActionPreference='Stop'
$repo=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
if(Test-Path -LiteralPath $OutputDirectory){throw 'Use a new output directory; preserve earlier probe evidence.'}
$run=(New-Item -ItemType Directory -Path $OutputDirectory).FullName
$bindings=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'pressure-probe/bindings.json') -Raw | ConvertFrom-Json
foreach($entry in $bindings.assemblies){
    $file=Join-Path $AssemblyRoot $entry.name
    if((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant() -cne $entry.sha256){throw ('Frozen binary mismatch: '+$entry.name)}
}
$source=Join-Path $repo $bindings.input
if((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant() -cne $bindings.inputSha256){throw 'Authentic input save differs.'}
$requests=@(
    @{op='load';path=$source},@{op='view';seat='Player'},
    @{op='clock';id='bishop.probe.to230400';x=57600;y=1},@{op='view';seat='Player'},
    @{op='submit';id='bishop.probe.third-rest';actor='TEST_ONLY.companion';kind='BeginLongRest';target='TEST_ONLY.cleric-long-rest-berth';x=0;y=0},
    @{op='clock';id='bishop.probe.to259200';x=28800;y=1},@{op='view';seat='Player'},
    @{op='save';path=(Join-Path $run 'after259200.ddsave')}
)
$requests | ForEach-Object {ConvertTo-Json -InputObject $_ -Depth 5 -Compress} | Set-Content -LiteralPath (Join-Path $run 'inputs.jsonl') -Encoding utf8
& pwsh -NoProfile -File (Join-Path $repo 'engine/tools/Open-ConnectedExpedition.ps1') -AssemblyRoot $AssemblyRoot -ClericLongRest -InputPath (Join-Path $run 'inputs.jsonl') > (Join-Path $run 'outputs.jsonl')
if($LASTEXITCODE -ne 0){throw 'Existing-engine probe failed.'}
$rows=@(Get-Content -LiteralPath (Join-Path $run 'outputs.jsonl') | ForEach-Object {$_ | ConvertFrom-Json})
if($rows.Count -ne 8 -or $rows[0].Response -ne 'Restored' -or $rows[2].Response -ne 'Committed' -or $rows[4].Response -ne 'Committed' -or $rows[5].Response -ne 'Committed' -or $rows[7].Response -ne 'Saved'){throw 'A probe command did not execute.'}
$hero=$rows[6].Actors | Where-Object {$_.Position.Id -eq 'TEST_ONLY.actor'}
$companion=$rows[6].Actors | Where-Object {$_.Position.Id -eq 'TEST_ONLY.companion'}
if($rows[6].Clock.Numerator -ne 259200 -or $rows[6].Clock.Denominator -ne 1 -or !$hero.Dead -or $companion.Dead -or $rows[6].LongRest.Settlements[-1].Benefit -ne 'Eligible'){throw 'Observed pressure branch differs; inspect retained output.'}
Write-Output ('REPRODUCED: genuine third rest eligible; hero dead at259200. Existing wire110 only; not Bishop execution. '+$run)
