param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$ParentSave,[Parameter(Mandatory)][string]$Run,
    [Parameter(Mandatory)][ValidateSet('MiningBoundary','ResearchResume','ResearchCancelZero','ResearchCancelPositive','ResearchCancelTactical','ManufacturingResume','ManufacturingCancelZero','ManufacturingCancelPositive')][string]$Case)
$ErrorActionPreference='Stop';$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path;$ParentSave=(Resolve-Path -LiteralPath $ParentSave).Path;$Run=[IO.Path]::GetFullPath($Run)
if(Test-Path -LiteralPath $Run){throw 'Use a fresh branch evidence directory.'};$null=New-Item -ItemType Directory -Path $Run
Copy-Item -LiteralPath $PSCommandPath -Destination $Run
$report=[ordered]@{status='RUNNING';case=$Case;scope='Genuine public-host branch of a retained fresh work-control campaign; distinct from useful-product principal';parentSave=$ParentSave;parentSha256=(Get-FileHash -LiteralPath $ParentSave).Hash.ToLowerInvariant();commands=0;strictRestorePairs=0;startedUtc=[DateTime]::UtcNow.ToString('o');driverSha256=(Get-FileHash -LiteralPath $PSCommandPath).Hash.ToLowerInvariant()}
function Require([bool]$ok,[string]$why){if(!$ok){throw $why}}
function Json($value){ConvertTo-Json -InputObject $value -Depth 12 -Compress -EnumsAsStrings}
function Digest($path){(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
try {
    foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
    function New-Session {[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithConnectedWorkControl(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())}
    $script:session=New-Session;$session.Restore($ParentSave);$store=[Decennium.Foundation.FileSaveStore]::new()
    $hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
    function State {$session.Save((Join-Path $Run 'latest.ddsave'));$store.Load((Join-Path $Run 'latest.ddsave'))}
    $initial=State
    $job=if($Case-eq'MiningBoundary'){$initial.MiningAttempts[0]}elseif($Case.StartsWith('Research')){$initial.FormulaWork[0]}else{$initial.ManufacturingOrders[0]}
    $worker=$job.WorkerId;$jobId=$job.Id;$report.jobId=$jobId
    function CurrentJob {$s=State;if($Case-eq'MiningBoundary'){$s.MiningAttempts[0]}elseif($Case.StartsWith('Research')){@($s.FormulaWork|Where-Object Id -eq $jobId)[0]}else{$s.ManufacturingOrders[0]}}
    function Command([string]$kind,[string]$target=$jobId,[int]$x=0,[int]$y=0) {
        $r=$session.View('Player').Revision;[Decennium.Foundation.Command]::new("wc.branch.$r",$worker,$r,$kind,$target,$x,$y)
    }
    function Commit($command) {
        $session.Save((Join-Path $Run 'before-query.ddsave'));$hash=Digest (Join-Path $Run 'before-query.ddsave')
        $query=$session.QueryCommand('Player',$command);$options=@($session.DiscoverCommands('Player',$command.Actor));$observation=$session.ObserveWork('Player',$command.Actor)
        $session.Save((Join-Path $Run 'after-query.ddsave'));Require ($hash-eq(Digest (Join-Path $Run 'after-query.ddsave'))) 'Query/discovery/observation mutated the branch.'
        Require ($query.Supported-and$query.Admissible) "Native query denied $($command.Kind): $($query.Code)"
        Require (@($options|Where-Object{$_.Command.Kind-eq$command.Kind-and$_.Command.Target-eq$command.Target-and$_.Query.Admissible}).Count-gt0) "No matching admissible discovery for $($command.Kind)"
        $result=$session.Submit('Player',$command);[IO.File]::AppendAllText((Join-Path $Run 'commands.jsonl'),(Json @{command=$command;query=$query;result=$result})+"`n")
        Require ($result.Response.ToString()-eq'Committed') "Submission denied $($command.Kind) after available query."
        $report.commands++;$null=State
    }
    function Deny($command) {
        $null=State;$before=Digest (Join-Path $Run 'latest.ddsave');$query=$session.QueryCommand('Player',$command);$result=$session.Submit('Player',$command);$null=State
        Require (!$query.Admissible-and$result.Response.ToString()-eq'Unavailable'-and$before-eq(Digest (Join-Path $Run 'latest.ddsave'))) 'Expected denial changed state or was available.'
        [IO.File]::AppendAllText((Join-Path $Run 'denials.jsonl'),(Json @{command=$command;query=$query;result=$result;unchanged=$true})+"`n")
    }
    function Clock([int]$n,[int]$d=1) {
        Require ($n-gt0) 'Nonpositive labor advancement.';$r=$session.View('Player').Revision
        $command=[Decennium.Foundation.Command]::new("wc.branch.$r",$hero,$r,'AdvanceClock','',$n,$d)
        $result=$session.SubmitSessionCommand($command);[IO.File]::AppendAllText((Join-Path $Run 'commands.jsonl'),(Json @{command=$command;result=$result})+"`n")
        Require ($result.Response.ToString()-eq'Committed') 'Clock rejected branch advancement.';$report.commands++;$null=State
    }
    function Witness([string]$name) {
        $p=Join-Path $Run ($name+'.ddsave');$session.Save($p)
        $view=$session.ObserveWork('Player',$worker);[IO.File]::WriteAllText((Join-Path $Run ($name+'.work.json')),(Json $view))
        $restored=New-Session;$restored.Restore($p);$restored.Save($p+'.restored')
        Require ((Digest $p)-eq(Digest ($p+'.restored'))) 'Strict restore changed canonical bytes.'
        Require ((Json $view)-eq(Json ($restored.ObserveWork('Player',$worker)))) 'Restored work observation differs.'
        $script:session=$restored;$report.strictRestorePairs++
    }
    Witness 'initial'
    if($Case-eq'MiningBoundary') {
        Require ($job.WorkDone-eq[Decennium.Foundation.RuleTime]::new(0)) 'Mining branch must begin before labor.'
        Commit (Command 'PauseMining');Witness 'zero-paused';Clock 6;Commit (Command 'ResumeMining')
        Clock $job.SetupSeconds;$boundary=CurrentJob
        Require ($null-eq$boundary.CommittedAt-and$boundary.WorkDone-eq[Decennium.Foundation.RuleTime]::new($job.SetupSeconds)) 'Setup boundary incorrectly committed extraction.'
        Witness 'exact-setup-boundary';Commit (Command 'PauseMining');Commit (Command 'ResumeMining');Clock 1 2
        $positive=CurrentJob;Require ($null-ne$positive.CommittedAt) 'First positive removal did not commit selection.'
        Commit (Command 'PauseMining');Witness 'positive-paused';Clock 6
        Require ((CurrentJob).WorkDone-eq$positive.WorkDone) 'Paused mining credited labor.'
        Commit (Command 'ResumeMining');$left=2*$job.DurationSeconds-2*$job.SetupSeconds-1;Clock $left 2
        $done=CurrentJob;Require ($done.Status.ToString()-notin@('Working','Paused','AwaitingCheck')-and$done.WorkDone-eq[Decennium.Foundation.RuleTime]::new($job.DurationSeconds)) 'Mining did not complete its native result.'
        $report.nativeResult=$done.Status.ToString();$report.setupSeconds=$job.SetupSeconds;$report.commitBoundary='null at exact setup, present after first positive1/2-second removal'
    } elseif($Case.StartsWith('Research')) {
        if($Case-ne'ResearchCancelZero'){Clock 1 2}
        if($Case-eq'ResearchCancelTactical') {
            Commit (Command 'PauseFormulaWork');Clock 6
            for($step=0;$step-lt2;$step++){Commit (Command 'BeginWorldStep' 'walk' -1 0);Clock 6}
            $r=$session.View('Player').Revision
            Commit ([Decennium.Foundation.Command]::new("wc.branch.$r",$hero,$r,'BeginWorldStep','walk',-1,0));Clock 12
            Require ((State).InventoryCombat) 'Research cancellation branch did not reach actual tactical context.'
            Witness 'tactical-paused';Commit (Command 'CancelFormulaWork')
            Require ((CurrentJob).Status.ToString()-eq'Cancelled') 'Lawful tactical research cancellation did not commit.'
        } elseif($Case-eq'ResearchResume') {
            Commit (Command 'PauseFormulaWork');Witness 'paused';Clock 6
            Require ((CurrentJob).Work.Retained-eq[Decennium.Foundation.RuleTime]::new(1,2)) 'Research lost retained knowledge labor.'
            Commit (Command 'ResumeFormulaWork');$s=State
            Clock ([int](28800*$s.RuleClock.Denominator-$s.RuleClock.Numerator)) ([int]$s.RuleClock.Denominator)
            Require ((CurrentJob).Status.ToString()-eq'Paused') 'Research did not pause at the exact first absolute work-window end.'
            Witness 'absolute-window-boundary';Commit (Command 'ResumeFormulaWork');$left=(CurrentJob).Work.Remaining;Clock ([int]$left.Numerator) ([int]$left.Denominator)
            Require ((CurrentJob).Status.ToString()-in@('Success','Failure')) 'Research did not resolve its native result.'
        } else {
            Commit (Command 'CancelFormulaWork');Witness 'cancelled'
            $expected=if($Case-eq'ResearchCancelZero'){[Decennium.Foundation.RuleTime]::new(0)}else{[Decennium.Foundation.RuleTime]::new(1,2)}
            Require ((CurrentJob).Work.Labor-eq$expected-and(CurrentJob).Work.Retained-eq$expected) 'Research cancellation erased its historical labor.'
            Clock 6;Commit (Command 'StartFormulaResearch' 'research.guild-notes');$s=State;$new=@($s.FormulaWork|Where-Object Id -ne $jobId)[0]
            Require ($new.Work.Labor-eq[Decennium.Foundation.RuleTime]::new(0)-and$new.Work.Remaining-eq$job.Work.Required) 'Cancellation transferred progress into a replacement research attempt.'
        }
    } else {
        if($Case-ne'ManufacturingCancelZero'){Clock 1 2;Commit (Command 'PauseManufacturing');Witness 'partial-phase-lost'
            Require ((CurrentJob).Work.Labor-eq[Decennium.Foundation.RuleTime]::new(1,2)-and(CurrentJob).Work.Retained-eq[Decennium.Foundation.RuleTime]::new(0)) 'Manufacturing pause failed to retain labor while losing unfinished phase.'}
        if($Case-eq'ManufacturingResume') {
            Clock 6;Commit (Command 'ResumeManufacturing');Clock 900;Witness 'stabilized-phase';Clock 13500
            $pending=CurrentJob;Require ($pending.Status.ToString()-eq'AwaitingChoice'-and$pending.Work.Remaining-eq[Decennium.Foundation.RuleTime]::new(0)) 'Native manufacturing quality choice was not reached.'
            Witness 'awaiting-quality';$view=@($session.ObserveWork('Player',$worker).Jobs|Where-Object Id -eq $jobId)[0]
            Require ($view.AwaitingChoice-and@($view.Controls|Where-Object{$_.Command.Kind.ToString()-ne'ResolveManufacturingQuality'}).Count-eq0) 'Pending quality exposed ordinary pause/resume/cancel controls.'
            Commit (Command 'ResolveManufacturingQuality' $jobId 1 0)
            Require ((CurrentJob).Work.Labor-eq[Decennium.Foundation.RuleTime]::new(28801,2)-and(CurrentJob).Work.Retained-eq[Decennium.Foundation.RuleTime]::new(14400)) 'Completion confused lost labor with retained work.'
        } else {
            Commit (Command 'CancelManufacturing');Witness 'cancelled';$s=State;$claims=@($s.Work.Reservations|Where-Object JobId -eq $jobId)
            $ingredients=@($claims|Where-Object Id -ne ($jobId+'.packaging'));$pack=@($claims|Where-Object Id -eq ($jobId+'.packaging'))
            $want=if($Case-eq'ManufacturingCancelZero'){'Released'}else{'Consumed'}
            Require ($ingredients.Count-gt0-and@($ingredients|Where-Object{$_.Status.ToString()-ne$want}).Count-eq0) 'Manufacturing cancellation mis-settled ingredients.'
            Require ($pack.Count-eq1-and$pack[0].Status.ToString()-eq'Released') 'Manufacturing cancellation did not release packaging.'
            Clock 6;Deny (Command 'StartManufacturing' 'recipe-4' 0 2)
            Require ((State).AlchemyDoses.Count-eq0) 'Cancelled batch produced output or permitted a replacement order.'
        }
    }
    Witness 'final';$s=State;$report.finalRevision=$s.Revision;$report.finalClock=$s.RuleClock;$report.finalRng=$s.RandomState
    $report.assemblyHashes=@(Get-ChildItem -LiteralPath $AssemblyRoot -Filter '*.dll'|ForEach-Object{@{name=$_.Name;sha256=(Digest $_.FullName)}})
    $report.status='PASS'
} catch {$report.status='FAIL';$report.error=$_.Exception.ToString()}
finally {$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8;Write-Output ("$($report.status): $Run")}
if($report.status-ne'PASS'){exit 1}
