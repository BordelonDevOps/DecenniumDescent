param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$WeightedSource,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
if(Test-Path -LiteralPath $Run){throw 'Use a fresh spatial control directory'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
. (Join-Path $PSScriptRoot 'Execution-SourceBinding.ps1')
$binding=Start-GeometryExecutionBinding $Run @($PSCommandPath)
function Require($value,$message){if(!$value){throw $message}}
function Digest($path){(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
$loaded=[ordered]@{}
foreach($part in 'Core','Persistence','LabModel'){$file=(Resolve-Path -LiteralPath (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")).Path;$a=[Reflection.Assembly]::LoadFrom($file);Require ($a.Location-ceq$file) 'Unexpected loaded binary';$loaded[$part]=@{sha256=(Digest $file);moduleId=$a.ManifestModule.ModuleVersionId.ToString()}}
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithDeclaredGeometry([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
$simulation=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic').GetValue($session)
$initial=$simulation.Capture()
$report=[ordered]@{status='FAIL';assemblies=$loaded;mechanicalScope='Detached copied poses only for independent channel controls. No gameplay, saving or authority is claimed for these probe states.';rays=@();actualCommandDenials=@()}
try {
    foreach($case in @(
        @{name='inherited-sight-only';fromX=1;fromY=1;toX=3;toY=1;sight=$false;effect=$true},
        @{name='declared-sight-only';fromX=6;fromY=0;toX=8;toY=0;sight=$false;effect=$true},
        @{name='declared-effect-only';fromX=8;fromY=0;toX=10;toY=0;sight=$true;effect=$false},
        @{name='movement-blocker-does-not-block-rays';fromX=5;fromY=1;toX=7;toY=1;sight=$true;effect=$true},
        @{name='two-side-movement-corner-has-independent-ray-channel';fromX=6;fromY=0;toX=7;toY=1;sight=$false;effect=$true}
    )){
        $s=$initial.Copy();$hero=$s.Actors|Where-Object Id -eq 'TEST_ONLY.actor';$companion=$s.Actors|Where-Object Id -eq 'TEST_ONLY.companion'
        $hero.X=$case.fromX;$hero.Y=$case.fromY;$companion.X=$case.toX;$companion.Y=$case.toY
        $sight=[Decennium.Foundation.Laboratory.ObservationGeometry]::CanSee($s,'TEST_ONLY.actor','TEST_ONLY.companion')
        $effect=[Decennium.Foundation.Laboratory.ObservationGeometry]::LineOfEffectClear($s,'TEST_ONLY.actor','TEST_ONLY.companion')
        Require ($sight-eq$case.sight-and$effect-eq$case.effect) "Independent channel result differs: $($case.name)"
        $report.rays+=@{input=$case;actualSight=$sight;actualEffect=$effect}
    }
    $session.Restore((Resolve-Path -LiteralPath $WeightedSource).Path)
    $simulation=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic').GetValue($session)
    $state=$simulation.Capture();$hero=$state.Actors|Where-Object Id -eq 'TEST_ONLY.actor'
    Require ($hero.X-eq5-and$hero.Y-eq2-and$state.Encounter.CurrentActor-eq'TEST_ONLY.actor') 'Control needs genuine acting-hero weighted checkpoint'
    $before=Join-Path $Run 'before.ddsave';$session.Save($before);$stable=Digest $before
    foreach($case in @(@{name='map-blocker';x=6;y=1;code='BlockedTacticalStep'},@{name='actual-opponent-occupancy';x=5;y=3;code='OccupiedTacticalStep'})){
        $command=[Decennium.Foundation.Command]::new('geometry.denial.'+$case.name,'TEST_ONLY.actor',$state.Revision,'TacticalStep',$state.Encounter.CurrentTurnId,$case.x,$case.y)
        $query=$session.QueryCastingCommand('Player',$command);Require (!$query.Admissible-and$query.Code-eq$case.code) "Unexpected actual movement query: $($query.Code)"
        $response=$session.Submit('Player',$command);Require ($response.Response-eq'Unavailable') 'Blocked actual movement was committed'
        $after=Join-Path $Run ($case.name+'.after.ddsave');$session.Save($after);Require ((Digest $after)-ceq$stable) 'Denied actual move modified state'
        $report.actualCommandDenials+=@{input=$case;query=$query;response=$response;unchangedSha256=(Digest $after)}
    }
    $report.status='PASS'
}catch{$report.error=$_.ToString()}
finally{Complete-GeometryExecutionBinding $Run $binding;$report|ConvertTo-Json -Depth 9|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8}
if($report.status-ne'PASS'){throw $report.error}
Write-Output 'PASS: five mechanical independent-channel probes and two actual public movement denials.'
