param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ClosedSave,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path;$ClosedSave=(Resolve-Path -LiteralPath $ClosedSave).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh after-exit retry directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Actual paid Dash receipt survives genuine source death/closure; exact retry succeeds and fresh post-exit requests reject without mutation';assemblies=@();checks=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel'){$path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path;$report.assemblies+=@{name=$name;sha256=(Digest $path)}}
    $report.compilationReport=@{path=(Join-Path $AssemblyRoot 'results.json');sha256=(Digest (Join-Path $AssemblyRoot 'results.json'))}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryAfterExitRetry.executed.ps1')
    $report.input=@{path=$ClosedSave;sha256=(Digest $ClosedSave)};Copy-Item -LiteralPath $ClosedSave -Destination (Join-Path $Run 'original-closed.ddsave')
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Restore($ClosedSave)
    $field=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic');$codec=[Decennium.Foundation.SnapshotCodec]::new()
    function Capture {$field.GetValue($session).Capture()}
    function Bytes {[Convert]::ToBase64String($codec.Encode((Capture)))}
    $initial=Capture;Require (!$initial.InventoryCombat-and$null-eq$initial.Encounter-and($initial.Lives|Where-Object ActorId -eq 'TEST_ONLY.ferry-wraith').Dead) 'Input did not genuinely close the defeated source encounter.'
    $receipt=@($initial.Receipts|Where-Object {$_.Id.StartsWith('ferry.exit.dash.')})
    Require ($receipt.Count-eq1) 'Actual pre-exit paid Dash receipt is missing or duplicated.'
    $receipt=$receipt[0];$dash=[Decennium.Foundation.CommandHistory]::Read($receipt)
    Require ($dash.Kind-eq'EncounterDash'-and$dash.Actor-eq'TEST_ONLY.actor') 'Retained source command is not the actual hero Dash.'
    $session.Save((Join-Path $Run 'verified-closed.ddsave'));Require ((Digest (Join-Path $Run 'verified-closed.ddsave'))-ceq$report.input.sha256) 'Strict replay changed the actual closed input.'
    $stable=Bytes;$report.exactQuery=$session.QueryCastingCommand('Player',$dash);$report.exactResponse=$session.Submit('Player',$dash)
    Require ($report.exactQuery.Code-eq'AlreadyCommitted'-and$report.exactResponse.Response-eq'Duplicate'-and$stable-ceq(Bytes)) 'Post-exit exact retry failed or repaid Dash.'
    $fresh=[Decennium.Foundation.Command]::new('ferry.exit.new',$dash.Actor,$initial.Revision,'EncounterDash',$dash.Target)
    $report.freshQuery=$session.QueryCastingCommand('Player',$fresh);$report.freshResponse=$session.Submit('Player',$fresh)
    Require ($report.freshQuery.Supported-and!$report.freshQuery.Admissible-and$report.freshQuery.Code-eq'FerryDashRequiresPartyCombat'-and$report.freshResponse.Response-eq'Unavailable'-and$stable-ceq(Bytes)) 'Fresh post-exit Dash reused historical combat admission.'
    $view=$session.View('Player');$discovery=@($session.DiscoverCastingCommands('Player',$dash.Actor)|Where-Object {$_.Command.Kind-eq'EncounterDash'})
    Require ($view.Commands-notcontains[Decennium.Foundation.CommandKind]::EncounterDash-and$discovery.Count-eq0-and$stable-ceq(Bytes)) 'Post-exit command view/discovery offered fresh Dash.'
    $conflict=[Decennium.Foundation.Command]::new($dash.Id,$dash.Actor,$dash.ExpectedRevision,'EncounterDash','TEST_ONLY.conflicting-turn')
    $report.conflictQuery=$session.QueryCastingCommand('Player',$conflict);$report.conflictResponse=$session.Submit('Player',$conflict)
    Require ($report.conflictQuery.Code-eq'CommandIdConflict'-and$report.conflictResponse.Response-eq'CommandIdConflict'-and$stable-ceq(Bytes)) 'Post-exit conflicting retry bypassed receipt identity.'
    $session.SetSeatEnabled('Player',$false)
    $report.revokedQuery=$session.QueryCastingCommand('Player',$dash);$report.revokedResponse=$session.Submit('Player',$dash)
    Require ($report.revokedQuery.Code-eq'NotAuthorized'-and$report.revokedResponse.Response-eq'NotAuthorized'-and$stable-ceq(Bytes)) 'Revoked post-exit retry exposed old authority.'
    $session.SetSeatEnabled('Player',$true)
    $report.otherSeatResponse=$session.Submit('FerryOpponent',$dash);Require ($report.otherSeatResponse.Response-eq'NotAuthorized'-and$stable-ceq(Bytes)) 'Source opponent stole the old party receipt.'
    $session.Save((Join-Path $Run 'after-probes.ddsave'));$session.Restore((Join-Path $Run 'after-probes.ddsave'));$session.Save((Join-Path $Run 'after-probes-restored.ddsave'))
    Require ((Digest (Join-Path $Run 'after-probes.ddsave'))-ceq$report.input.sha256-and(Digest (Join-Path $Run 'after-probes-restored.ddsave'))-ceq$report.input.sha256) 'Post-exit probes changed authoritative bytes or strict continuation.'
    $report.originalDash=$dash;$report.originalReceipt=$receipt;$report.closedEncounters=$initial.ClosedEncounters
    $report.finalRevision=$initial.Revision;$report.finalClock=$initial.RuleClock;$report.finalRandom=$initial.RandomState;$report.finalResonance=$initial.ResonancePools
    $report.status='PASS_GENUINE_POST_EXIT_DASH_RETRY_AND_FRESH_DENIAL_ONLY'
} catch {$report.error=$_.Exception.ToString()}
$report.completedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 70|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
