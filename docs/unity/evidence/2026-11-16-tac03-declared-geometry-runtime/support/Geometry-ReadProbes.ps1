. (Join-Path $PSScriptRoot '../../2026-11-16-chr03-bishop-runtime/support/Bishop-ReadProbes.ps1')
. (Join-Path $PSScriptRoot 'Geometry-TraceCommand.ps1')
function New-GeometryProbes($snapshot,$markName) {
    New-BishopProbes $snapshot $markName
    foreach($seat in 'Player','FirstOpponent','RecoveryOpponent'){
        @{op='discover';seat=$seat;actor='TEST_ONLY.actor';evidenceRead=$markName+'.'+$seat+'.hero-discovery.json'}
        foreach($kind in 'BeginWorldStep','SuspendWorldStep','ResumeWorldStep','TacticalStep'){
            $target=if($kind-eq'BeginWorldStep'){'walk'}elseif($kind-eq'TacticalStep'){$snapshot.Encounter.CurrentTurnId ?? 'TEST_ONLY.no-turn'}else{''}
            @{op='query';seat=$seat;id='probe.geometry.'+$kind+'.'+$snapshot.Revision;actor='TEST_ONLY.actor';revision=$snapshot.Revision;kind=$kind;target=$target;x=$(if($kind-eq'TacticalStep'){($snapshot.Actors|Where-Object Id -eq 'TEST_ONLY.actor').X+1}elseif($kind-eq'BeginWorldStep'){1}else{0});y=$(if($kind-eq'TacticalStep'){($snapshot.Actors|Where-Object Id -eq 'TEST_ONLY.actor').Y}else{0});evidenceRead=$markName+'.'+$seat+'.'+$kind+'.json'}
        }
        @{op='query';seat=$seat;id='probe.geometry.run.'+$snapshot.Revision;actor='TEST_ONLY.actor';revision=$snapshot.Revision;kind='BeginWorldStep';target='run';x=1;y=0;evidenceRead=$markName+'.'+$seat+'.run.json'}
        @{op='query';seat=$seat;id='probe.geometry.bounds.'+$snapshot.Revision;actor='TEST_ONLY.actor';revision=$snapshot.Revision;kind='BeginWorldStep';target='walk';x=[int]::MaxValue;y=0;evidenceRead=$markName+'.'+$seat+'.invalid-direction.json'}
    }
    $movement=$snapshot.Receipts|Where-Object Principal -eq 'TEST_ONLY.host'|Where-Object {
        ([Decennium.Foundation.CommandHistory]::Read($_)).Kind-in'BeginWorldStep','SuspendWorldStep','ResumeWorldStep','TacticalStep'
    }|Select-Object -Last 1
    if($movement){
        foreach($seat in 'Player','FirstOpponent','RecoveryOpponent'){
            $r=ConvertTo-GeometryRequest $movement;$r.op='submit';$r.seat=$seat
            $r.evidenceRead=$markName+'.'+$seat+'.movement-duplicate.json'
            $r.expectedResponse=if($seat-eq'Player'){'Duplicate'}else{'NotAuthorized'}
            $r
        }
    }
}
