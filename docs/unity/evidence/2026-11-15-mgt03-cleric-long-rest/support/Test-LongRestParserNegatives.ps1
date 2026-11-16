param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ReadySave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$ReadySave=(Resolve-Path -LiteralPath $ReadySave).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
foreach($part in 'Core','Persistence'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$state=[Decennium.Foundation.FileSaveStore]::new().Load($ReadySave)
if(!$state.ConnectedClericLongRest -or $state.ClericLongRests[-1].Outcome -ne 'Interrupted'){throw 'Use an actual earned, interrupted rest checkpoint.'}
$inputs=[Collections.Generic.List[object]]::new()
$inputs.Add(@{op='load';path=$ReadySave})
$inputs.Add(@{op='save';path=(Join-Path $Run 'before.ddsave')})
$negativeNames=[Collections.Generic.List[string]]::new()
foreach($mode in 'duration','hp','rp','conviction','participants','missing-x','nonzero-x','boolean-y','null-inventory','query-duration'){
 $request=@{op='submit';seat='Player';id=('long-rest.parser.'+$mode);actor='TEST_ONLY.companion';revision=$state.Revision;
  kind='BeginLongRest';target='TEST_ONLY.cleric-long-rest-berth';x=0;y=0}
 switch($mode){
  'duration'{$request.duration=1}
  'hp'{$request.hp=99}
  'rp'{$request.rp=99}
  'conviction'{$request.conviction=5}
  'participants'{$request.participants=@('TEST_ONLY.actor','TEST_ONLY.companion')}
  'missing-x'{$request.Remove('x')}
  'nonzero-x'{$request.x=1}
  'boolean-y'{$request.y=$false}
  'null-inventory'{$request.inventory=$null}
  'query-duration'{$request.op='query';$request.duration=1}
 }
 $inputs.Add($request);$negativeNames.Add($mode)
}
$inputs.Add(@{op='save';path=(Join-Path $Run 'after.ddsave')})
$inputPath=Join-Path $Run 'inputs.jsonl'
$inputs|ForEach-Object{ConvertTo-Json $_ -Depth 5 -Compress}|Set-Content -LiteralPath $inputPath -Encoding utf8
$launcher=Join-Path $repository 'engine/tools/Open-ConnectedExpedition.ps1'
$report=[ordered]@{status='FAIL';scope='Parser-only malformed choices; no engine command is expected to dispatch';startedUtc=[DateTime]::UtcNow.ToString('o');
 launcherSha256=(Digest $launcher);readySaveSha256=(Digest $ReadySave);names=@($negativeNames)}
try {
 & pwsh -NoProfile -File $launcher -ClericLongRest -AssemblyRoot $AssemblyRoot -InputPath $inputPath | Set-Content -LiteralPath (Join-Path $Run 'responses.jsonl') -Encoding utf8
 if($LASTEXITCODE-ne0){throw 'Console process failed.'}
 $responses=@(Get-Content -LiteralPath (Join-Path $Run 'responses.jsonl')|ConvertFrom-Json)
 if($responses.Count-ne$inputs.Count -or $responses[0].Response-ne'Restored' -or $responses[1].Response-ne'Saved' -or $responses[-1].Response-ne'Saved'){throw 'Console control responses differ.'}
 for($i=0;$i-lt$negativeNames.Count;$i++){if($responses[$i+2].Response-ne'Unavailable'){throw "Unexpected parser acceptance: $($negativeNames[$i])"}}
 $report.beforeSha256=Digest (Join-Path $Run 'before.ddsave');$report.afterSha256=Digest (Join-Path $Run 'after.ddsave')
 if($report.beforeSha256-cne$report.afterSha256){throw 'Rejected parser controls changed canonical state.'}
 $report.status='PASS';$report.rejected=$negativeNames.Count
} catch {$report.error=$_.ToString()}
finally {$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8}
if($report.status-ne'PASS'){throw $report.error}
Write-Output "PASS: $($negativeNames.Count) parser-only controls; unchanged state."
