param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run=[IO.Path]::GetFullPath($Run)
if(Test-Path -LiteralPath $Run){throw 'Use a new evidence directory.'}
$null=New-Item -ItemType Directory -Path $Run
Copy-Item -LiteralPath $PSCommandPath -Destination $Run
$repo=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$hostScript=Join-Path $repo 'engine/tools/Open-ConnectedExpedition.ps1'
$report=[ordered]@{status='RUNNING';scope='Bounded new-profile console/typed fill, observations, discovery and save/restore parity; not full module qualification';startedUtc=[DateTime]::UtcNow.ToString('o');assemblyRoot=$AssemblyRoot;consoleSha256=(Get-FileHash -LiteralPath $hostScript).Hash.ToLowerInvariant();driverSha256=(Get-FileHash -LiteralPath $PSCommandPath).Hash.ToLowerInvariant();comparisons=0}
function Json($value){ConvertTo-Json -InputObject $value -Depth 8 -Compress -EnumsAsStrings}
try {
    foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithConnectedWorkControl(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $actor=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Companion
    $hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
    $supply=[Decennium.Foundation.Laboratory.TestOnlyFillingPolicy]::SupplyId
    $skin=[Decennium.Foundation.Laboratory.TestOnlyFillingPolicy]::CompanionSkinId
    $start=@{op='submit';id='console.fill.start';actor=$actor;revision=0;kind='StartWaterFill';target=$supply;inventory=@{numerator=1;denominator=2;destination=$skin}}
    $requests=@(
        @{op='view'},@{op='work';actor=$actor},@{op='discover';actor=$actor},
        ($start+@{}),@{op='clock';id='console.fill.half';revision=1;x=1;y=2},@{op='work';actor=$actor},
        @{op='submit';id='console.fill.pause';actor=$actor;revision=2;kind='PauseWaterFill';target='inventory.1.fill'},
        @{op='work';actor=$actor},@{op='discover';actor=$actor},
        @{op='save';path=(Join-Path $Run 'console-paused.ddsave')},@{op='load';path=(Join-Path $Run 'console-paused.ddsave')},
        @{op='submit';id='console.fill.resume';actor=$actor;revision=3;kind='ResumeWaterFill';target='inventory.1.fill'},
        @{op='clock';id='console.fill.finish';revision=4;x=119;y=2},@{op='work';actor=$actor},@{op='view'},
        @{op='query';id=$start.id;actor=$actor;revision=0;kind=$start.kind;target=$supply;inventory=$start.inventory},
        @{op='save';path=(Join-Path $Run 'console-final.ddsave')})
    $inputFile=Join-Path $Run 'inputs.jsonl';$expected=Join-Path $Run 'typed.jsonl';$output=Join-Path $Run 'console.jsonl'
    [IO.File]::WriteAllLines($inputFile,[string[]]@($requests|ForEach-Object{Json $_}))
    $answers=[Collections.Generic.List[string]]::new()
    foreach($request in $requests) {
        $value=switch($request.op) {
            'view' {$session.View('Player');break}
            'work' {$session.ObserveWork('Player',$request.actor);break}
            'discover' {
                ,@($session.DiscoverCommands('Player',$request.actor)|ForEach-Object{
                    $projected=$_.Command|Select-Object -Property *
                    $center=$_.Command.GetConsecrateRequest()
                    if($null-ne$center){$projected|Add-Member -NotePropertyName Consecrate -NotePropertyValue $center}
                    [pscustomobject]@{Command=$projected;Query=$_.Query}
                });break
            }
            'save' {$session.Save((Join-Path $Run ('typed-'+[IO.Path]::GetFileName($request.path))));@{Response='Saved'};break}
            'load' {$session.Restore((Join-Path $Run ('typed-'+[IO.Path]::GetFileName($request.path))));@{Response='Restored'};break}
            default {
                $inventory=if($request.inventory){[Decennium.Foundation.InventoryRequest]::new([Decennium.Foundation.RuleQuantity]::new(1,2),$skin)}else{$null}
                $command=[Decennium.Foundation.Command]::new($request.id,($request.actor??$hero),$request.revision,
                    $(if($request.op-eq'clock'){'AdvanceClock'}else{$request.kind}),($request.target??''),($request.x??0),($request.y??0),$inventory)
                if($request.op-eq'query'){$session.QueryCommand('Player',$command)}
                elseif($request.op-eq'clock'){$session.SubmitSessionCommand($command)}
                else{$session.Submit('Player',$command)}
            }
        }
        if($request.op-in@('submit','clock')-and$value.Response.ToString()-ne'Committed'){throw "Typed command failed: $($request.id)/$($value.Response)"}
        # The console intentionally projects old compatibility fields. Compare inherited actor
        # details/LongRest and work summaries rather than inventing a new old-view contract.
        if($request.op-eq'view'){$value=[ordered]@{Actors=$value.Actors;LongRest=$value.LongRest;Work=$value.Work;Commands=$value.Commands}}
        $answers.Add((Json $value))
    }
    [IO.File]::WriteAllLines($expected,$answers)
    $lines=@(& pwsh -NoProfile -File $hostScript -AssemblyRoot $AssemblyRoot -InputPath $inputFile -ConnectedWorkControl)
    if($LASTEXITCODE-ne0){throw 'Console process failed.'}
    [IO.File]::WriteAllLines($output,[string[]]$lines)
    $compare=@'
import json,sys,pathlib
base=pathlib.Path(sys.argv[1]); req=[json.loads(x) for x in (base/'inputs.jsonl').read_text(encoding='utf-8-sig').splitlines()]
left=[json.loads(x) for x in (base/'typed.jsonl').read_text(encoding='utf-8-sig').splitlines()]
right=[json.loads(x) for x in (base/'console.jsonl').read_text(encoding='utf-8-sig').splitlines()]
assert len(req)==len(left)==len(right), 'Response count differs'
for i,(r,a,b) in enumerate(zip(req,left,right)):
 if r['op']=='view':
  for actor in b['Actors']:
   assert all(k in actor for k in ('Cleric','Repertoire','ClericSettlement','Casting','TemporaryHp','TemporaryHpUntil')), 'Inherited actor fields stripped'
  assert 'LongRest' in b, 'Inherited LongRest stripped'
  b={k:b[k] for k in ('Actors','LongRest','Work','Commands')}
 assert a==b, f'Typed/console mismatch at {i} ({r["op"]})'
assert (base/'typed-console-final.ddsave').read_bytes()==(base/'console-final.ddsave').read_bytes(), 'Final snapshots differ'
assert (base/'typed-console-paused.ddsave').read_bytes()==(base/'console-paused.ddsave').read_bytes(), 'Paused snapshots differ'
print('PASS: '+str(len(req))+' complete response comparisons and two snapshot pairs')
'@
    $comparison=@(& python -B -X utf8 -c $compare $Run)
    if($LASTEXITCODE-ne0){throw 'Typed/console comparison failed.'}
    $report.comparisons=$requests.Count;$report.snapshotPairs=2;$report.status='PASS';$report.comparisonOutput=$comparison
    $report.assemblyHashes=@(Get-ChildItem -LiteralPath $AssemblyRoot -Filter '*.dll'|ForEach-Object{@{name=$_.Name;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash.ToLowerInvariant()}})
} catch {$report.status='FAIL';$report.error=$_.Exception.ToString()}
finally {$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8;Write-Output ("$($report.status): $Run")}
if($report.status-ne'PASS'){exit 1}
