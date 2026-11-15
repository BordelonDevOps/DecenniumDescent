param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ActiveSave)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$ActiveSave=(Resolve-Path -LiteralPath $ActiveSave).Path
$run=(New-Item -ItemType Directory -Force -Path (Join-Path $PSScriptRoot 'console-source-probe')).FullName
foreach($name in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot ("Decennium.Foundation.$name.dll"))}
$snapshot=[Decennium.Foundation.FileSaveStore]::new().Load($ActiveSave)
$use=$snapshot.FrightenedUses[-1]
$targets=@($use.TargetIds)
$inputFile=Join-Path $run 'inputs.jsonl'
$outputFile=Join-Path $run 'responses.jsonl'
$trace=@(
    @{op='view'},
    @{op='load';path=$ActiveSave},
    @{op='view'},
    @{op='save';path=(Join-Path $run 'restored.ddsave')},
    @{op='submit';seat='Player';kind='UseIntimidatingPresence';actor=$use.ActorId;id='fear.console.unauthorized';revision=$snapshot.Revision;intimidatingPresence=@{targets=$targets}},
    @{op='save';path=(Join-Path $run 'unauthorized.ddsave')},
    @{op='defender-presence';actor=$use.ActorId;id='fear.console.spent';revision=$snapshot.Revision;intimidatingPresence=@{targets=$targets}},
    @{op='save';path=(Join-Path $run 'spent.ddsave')},
    @{op='defender-presence';actor=$use.ActorId;id=$use.CommandId;revision=($use.Revision-1);intimidatingPresence=@{targets=$targets}},
    @{op='save';path=(Join-Path $run 'duplicate.ddsave')}
)
$trace | ForEach-Object {ConvertTo-Json $_ -Depth 6 -Compress} | Set-Content -LiteralPath $inputFile -Encoding utf8
$launcher=Join-Path $PSScriptRoot '../../../tools/Open-ConnectedExpedition.ps1'
& $launcher -Frightened -AssemblyRoot $AssemblyRoot -InputPath $inputFile | Set-Content -LiteralPath $outputFile -Encoding utf8
$responses=@(Get-Content -LiteralPath $outputFile | ConvertFrom-Json)
if($responses.Count-ne$trace.Count){throw 'Console response count mismatch.'}
if($responses[4].Response-ne'NotAuthorized'-or$responses[6].Response-ne'Unavailable'-or$responses[8].Response-ne'Duplicate'){
    throw ('Unexpected actual console denial/retry response: '+($responses | ConvertTo-Json -Depth 2 -Compress))
}
$expected=(Get-FileHash -LiteralPath $ActiveSave -Algorithm SHA256).Hash
$files=@('restored','unauthorized','spent','duplicate') | ForEach-Object {
    $path=Join-Path $run ($_+'.ddsave');$hash=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    if($hash-ne$expected){throw ('Console changed snapshot: '+$_)}
    @{name=$_;sha256=$hash.ToLowerInvariant()}
}
if(@($responses[2].Actors | Where-Object {$_.Conditions-contains'Frightened'}).Count-ne2){throw 'Owned fear projection missing.'}
[ordered]@{status='PASS';scope='Development console restore/authority/payment/retry probe; not the required full four-path walkthrough';
    atUtc=[DateTime]::UtcNow.ToString('o');assemblyRoot=$AssemblyRoot;activeSave=$ActiveSave;revision=$snapshot.Revision;
    inputs=$trace.Count;files=$files;responses=@($responses[4].Response,$responses[6].Response,$responses[8].Response)
} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $run 'results.json') -Encoding utf8
Write-Output 'PASS: console source probe, 4 byte-identical saves and 3 authority/payment/retry responses.'
