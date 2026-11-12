param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run
)
$ErrorActionPreference = 'Stop'
$launcher = (Resolve-Path (Join-Path $PSScriptRoot '../../../../engine/tools/Open-ConnectedExpedition.ps1')).Path
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
New-Item -ItemType Directory -Path $Run | Out-Null
$Run = (Resolve-Path -LiteralPath $Run).Path
$launch = [Diagnostics.ProcessStartInfo]::new((Get-Command pwsh).Source)
foreach ($argument in '-NoProfile','-File',$launcher,'-AssemblyRoot',$AssemblyRoot) {
    $launch.ArgumentList.Add($argument)
}
$launch.WorkingDirectory = $Run
$launch.UseShellExecute = $false
$launch.CreateNoWindow = $true
$launch.RedirectStandardInput = $true
$launch.RedirectStandardOutput = $true
$launch.RedirectStandardError = $true
$process = [Diagnostics.Process]::Start($launch)
$errors = $process.StandardError.ReadToEndAsync()
$inputs = Join-Path $Run 'inputs.jsonl'
$responses = Join-Path $Run 'responses.jsonl'
$hero = 'TEST_ONLY.actor'
$opponent = 'TEST_ONLY.third-combatant'

function Send($request, [string]$expected = '') {
    $json = ConvertTo-Json -InputObject $request -Depth 5 -Compress
    Add-Content -LiteralPath $inputs -Value $json -Encoding utf8
    $process.StandardInput.WriteLine($json)
    $process.StandardInput.Flush()
    $read = $process.StandardOutput.ReadLineAsync()
    if (-not $read.Wait([TimeSpan]::FromSeconds(30))) { throw 'Timed out waiting for the interactive console response.' }
    $reply = $read.Result
    if ([string]::IsNullOrEmpty($reply)) { throw 'The interactive console closed before answering.' }
    Add-Content -LiteralPath $responses -Value $reply -Encoding utf8
    $result = ConvertFrom-Json $reply
    if ($expected -ne '' -and $result.Response -ne $expected) {
        throw "Expected $expected, got $($result.Response) for $json"
    }
    $result
}

function Read-SeatChoice([string]$seat, [string]$other, [string]$kind, [string]$actor) {
    $view = Send @{op='view'; seat=$seat}
    $otherView = Send @{op='view'; seat=$other}
    if ($view.PendingDecision -ne $kind -or $view.ActingActorId -ne $actor -or
        $view.NextSeat -ne $seat -or $view.TurnId -eq '' -or $view.DecisionId -eq '' -or
        $otherView.DecisionId -ne '' -or $otherView.ActingActorId -ne '') {
        throw "The $kind response was not visible to exactly the authorized actor's seat."
    }
    $view
}

try {
    $banner = $process.StandardOutput.ReadLineAsync()
    if (-not $banner.Wait([TimeSpan]::FromSeconds(30)) -or $banner.Result -notmatch 'TEST_ONLY connected expedition') {
        throw 'The interactive console did not start.'
    }
    for ($step=0; $step -lt 3; $step++) {
        $null = Send @{op='submit'; id="choice.walk.$step"; actor=$hero; kind='BeginWorldStep'; target='walk'; x=1} 'Committed'
        if ($step -lt 2) {
            $null = Send @{op='clock'; id="choice.clock.$step"; x=2; y=1} 'Committed'
        }
    }
    $third = Send @{op='view'; seat='FirstOpponent'}
    $null = Send @{op='submit'; id='choice.third.stance'; seat='FirstOpponent'; kind='SelectCombatStance';
        combat=@{stance=1}} 'Committed'
    $null = Send @{op='submit'; id='choice.third.approach'; seat='FirstOpponent'; kind='TacticalStep';
        target=$third.TurnId; x=3} 'Committed'
    $null = Send @{op='save'; path='fork.ddsave'} 'Saved'

    $null = Send @{op='submit'; id='choice.third.depart'; seat='FirstOpponent'; kind='TacticalStep';
        target=$third.TurnId; x=4} 'Committed'
    $null = Send @{op='save'; path='opportunity.ddsave'} 'Saved'
    $null = Send @{op='load'; path='opportunity.ddsave'} 'Restored'
    $reaction = Read-SeatChoice Player FirstOpponent Opportunity $hero
    if ($reaction.TurnId -ne $third.TurnId) { throw 'Player reaction did not occur on the first opponent turn.' }
    $strike = @{op='submit'; id='choice.hero.reaction'; seat='FirstOpponent'; actor=$reaction.ActingActorId;
        revision=$reaction.Revision; kind='RespondOpportunityAttack'; target=$reaction.DecisionId;
        combat=@{weapon='TEST_ONLY.actor-club'; knockout='AskIfEligible'; choice=$true}}
    $null = Send $strike 'NotAuthorized'
    $strike.seat = 'Player'
    $result = Send $strike 'Committed'
    if ($result.PendingDecision -ne 'Knockout' -or $result.OpportunityPending) {
        throw 'A deferred knockout must supersede the interrupted move.'
    }
    $null = Send @{op='save'; path='knockout.ddsave'} 'Saved'
    $null = Send @{op='load'; path='knockout.ddsave'} 'Restored'
    $knockout = Read-SeatChoice Player FirstOpponent Knockout $hero
    $null = Send $strike 'Duplicate'
    $resolve = @{op='submit'; id='choice.hero.knockout'; seat='FirstOpponent'; actor=$knockout.ActingActorId;
        revision=$knockout.Revision; kind='ResolveKnockout'; target=$knockout.DecisionId; combat=@{choice=$false}}
    $null = Send $resolve 'NotAuthorized'
    $resolve.seat = 'Player'
    $result = Send $resolve 'Committed'
    if ($result.PendingDecision -ne 'None') { throw 'The knockout response did not release the suspended move.' }

    $null = Send @{op='load'; path='fork.ddsave'} 'Restored'
    $null = Send @{op='submit'; id='choice.third.attack'; seat='FirstOpponent'; kind='AttackClub'; target=$hero;
        combat=@{weapon='TEST_ONLY.third-club'}} 'Committed'
    $null = Send @{op='submit'; id='choice.third.end'; seat='FirstOpponent'; kind='EndRegularTurn'; target=$third.TurnId} 'Committed'
    $player = Send @{op='view'; seat='Player'}
    $null = Send @{op='submit'; id='choice.hero.stance'; seat='Player'; kind='SelectCombatStance'; combat=@{stance=1}} 'Committed'
    $null = Send @{op='submit'; id='choice.hero.depart'; seat='Player'; kind='TacticalStep'; target=$player.TurnId; x=1} 'Committed'
    $opportunity = Read-SeatChoice FirstOpponent Player Opportunity $opponent
    if ($opportunity.TurnId -ne $player.TurnId) { throw 'Director reaction did not occur on the player turn.' }
    $null = Send @{op='submit'; id='choice.third.reaction'; seat='FirstOpponent'; kind='RespondOpportunityAttack';
        target=$opportunity.DecisionId; combat=@{choice=$false}} 'Committed'
    $null = Send @{op='save'; path='press.ddsave'} 'Saved'
    $null = Send @{op='load'; path='press.ddsave'} 'Restored'
    $press = Read-SeatChoice FirstOpponent Player Press $opponent
    $follow = @{op='submit'; id='choice.third.press'; seat='Player'; actor=$press.ActingActorId;
        revision=$press.Revision; kind='RespondPress'; target=$press.DecisionId; combat=@{choice=$true}}
    $null = Send $follow 'NotAuthorized'
    $follow.seat = 'FirstOpponent'
    $result = Send $follow 'Committed'
    # Exact retries include the turn resolved for the original submission.
    $follow.combat.turn = $press.TurnId
    $null = Send $follow 'Duplicate'
    $director = Send @{op='view'; seat='FirstOpponent'}
    if ($result.PendingDecision -ne 'None' -or $director.Actors[0].Position.X -ne 2) {
        throw 'The actual Press step did not commit once and return control.'
    }
    $process.StandardInput.WriteLine('quit')
    $process.StandardInput.Close()
    if (-not $process.WaitForExit(10000) -or $process.ExitCode -ne 0 -or $errors.Result -ne '') {
        throw 'The console did not terminate successfully.'
    }
    [ordered]@{Status='PASS'; Scenarios=@('Human off-turn opportunity','Deferred knockout','Press follow');
        DecisionSaves=@('opportunity.ddsave','knockout.ddsave','press.ddsave'); ConsoleSuppliedTurnForPendingResponses=$true;
        WrongSeatRejected=3; DuplicateReactionsOrFollows=2; FinalRevision=$director.Revision} |
        ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$Run/results.json" -Encoding utf8
    Get-Content -LiteralPath "$Run/results.json"
} finally {
    if (-not $process.HasExited) { $process.Kill() }
    $process.Dispose()
}
