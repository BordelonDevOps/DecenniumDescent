. (Join-Path $PSScriptRoot '../../2026-11-16-tac03-declared-geometry-runtime/support/Geometry-ReadProbes.ps1')
. (Join-Path $PSScriptRoot 'Ferry-TraceCommand.ps1')
function Get-FerryProbeJson($session,$request) {
    if($request.op-eq'ferry'){$result=$session.ObserveFerryDecision($request.seat)}
    elseif($request.op-eq'seal'){$result=$session.ObserveExposedSeal($request.seat,$request.actor)}
    else{return Get-BishopProbeJson $session $request}
    ConvertTo-Json -InputObject $result -Depth 8 -Compress -EnumsAsStrings
}
function New-FerryProbes($snapshot,$markName) {
    New-GeometryProbes $snapshot $markName
    $turn=$snapshot.Encounter.CurrentTurnId ?? 'TEST_ONLY.no-turn'
    foreach($seat in 'Player','FirstOpponent','RecoveryOpponent','FerryOpponent') {
        foreach($actor in 'TEST_ONLY.actor','TEST_ONLY.companion','TEST_ONLY.ferry-wraith') {
            @{op='discover';seat=$seat;actor=$actor;evidenceRead=$markName+'.'+$seat+'.ferry-'+$actor+'.discovery.json'}
        }
        @{op='ferry';seat=$seat;evidenceRead=$markName+'.'+$seat+'.ferry-decision.json'}
        @{op='seal';seat=$seat;actor='TEST_ONLY.actor';evidenceRead=$markName+'.'+$seat+'.seal-observation.json'}
        @{op='query';seat=$seat;id='probe.ferry.dash.'+$snapshot.Revision;actor='TEST_ONLY.actor';revision=$snapshot.Revision;kind='EncounterDash';target=$turn;x=0;y=0;evidenceRead=$markName+'.'+$seat+'.dash-query.json'}
        @{op='query';seat=$seat;id='probe.ferry.seal.'+$snapshot.Revision;actor='TEST_ONLY.actor';revision=$snapshot.Revision;kind='TearExposedSeal';target='TEST_ONLY.ferry-seal';x=0;y=0;evidenceRead=$markName+'.'+$seat+'.seal-query.json'}
        $attack=@{op='query';seat=$seat;id='probe.ferry.claw.'+$snapshot.Revision;actor='TEST_ONLY.ferry-wraith';revision=$snapshot.Revision;kind='AttackCreatureFeature';target='TEST_ONLY.actor';x=0;y=0;
            combat=@{turn=$turn;weapon='';stance=0;knockout='OrdinaryOutcome';choice=$false;press='ArmOrReplace';feature='TEST_ONLY.ferry-wraith.hellfire-claw'};evidenceRead=$markName+'.'+$seat+'.claw-query.json'}
        $attack
        if($seat-ne'FerryOpponent') {
            $denial=$attack.Clone();$denial.op='submit';$denial.id='probe.ferry.denied.'+$snapshot.Revision;$denial.evidenceRead=$markName+'.'+$seat+'.claw-denial.json';$denial.expectedResponse='NotAuthorized';$denial
        }
        foreach($kind in 'RespondPress','ResolveKnockout') {
            @{op='query';seat=$seat;id='probe.ferry.pending.'+$kind+'.'+$snapshot.Revision;actor='TEST_ONLY.ferry-wraith';revision=$snapshot.Revision;kind=$kind;target=($snapshot.Encounter.CurrentTurnId ?? 'TEST_ONLY.no-decision');x=0;y=0;evidenceRead=$markName+'.'+$seat+'.'+$kind+'-query.json'}
        }
    }
    $dash=$snapshot.Receipts|Where-Object Id -eq 'ferry.exit.dash.356'|Select-Object -First 1
    if($dash) {
        $original=ConvertTo-FerryRequest $dash
        foreach($seat in 'Player','FirstOpponent','RecoveryOpponent','FerryOpponent') {
            $duplicate=$original.Clone();$duplicate.seat=$seat;$duplicate.evidenceRead=$markName+'.'+$seat+'.dash-duplicate.json'
            $duplicate.expectedResponse=if($seat-eq'Player'){'Duplicate'}else{'NotAuthorized'};$duplicate
        }
    }
}
