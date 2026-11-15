param([Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$Run=(Resolve-Path -LiteralPath $Run).Path
$launch=Get-Content -LiteralPath (Join-Path $Run 'launch.json') -Raw|ConvertFrom-Json
$workers=@(Get-Content -LiteralPath (Join-Path $Run 'processes.json') -Raw|ConvertFrom-Json)
$last=''
while($true){
    $total=0;$finished=[Collections.Generic.List[string]]::new();$live=[Collections.Generic.List[int]]::new()
    foreach($worker in $workers){
        $group=$worker.group
        $rows=@(Get-Content -LiteralPath (Join-Path $Run ($group+'.jsonl'))|ForEach-Object{$_|ConvertFrom-Json})
        $failed=@($rows|Where-Object {!$_.Passed-or$_.Error})
        if($failed.Count){$failed|ConvertTo-Json -Compress;throw "Original regression failure in $group"}
        $total+=$rows.Count
        $done=Join-Path $Run ($group+'.done')
        if(Test-Path -LiteralPath $done){
            $record=Get-Content -LiteralPath (Join-Path $Run ($group+'.execution.json')) -Raw|ConvertFrom-Json
            if($record.runId-cne$launch.runId-or$record.pid-ne$worker.pid-or$rows.Count-ne$worker.cases-or
                $record.journalSha256-cne(Get-FileHash -LiteralPath (Join-Path $Run ($group+'.jsonl'))).Hash.ToLowerInvariant()-or
                (Get-Content -LiteralPath $done)-cne'DONE'){throw "Invalid completed worker $group"}
            $finished.Add($group)
        }else{
            $process=Get-Process -Id $worker.pid -ErrorAction SilentlyContinue
            if($null-eq$process){throw "Original worker missing without completion: $group PID $($worker.pid)"}
            # ConvertFrom-Json preserves the UTC DateTime. Cast it directly; parsing
            # its localized display string would lose the UTC offset.
            $started=[DateTimeOffset]$launch.startedUtc
            if([Math]::Abs(($process.StartTime.ToUniversalTime()-$started.UtcDateTime).TotalSeconds)-gt20){throw "Original worker PID reused: $group"}
            $live.Add($process.Id)
        }
    }
    $status=[ordered]@{runId=$launch.runId;passed=$total;required=$launch.requiredCount;failed=0;completedWorkers=@($finished);liveOriginalPids=@($live)}|ConvertTo-Json -Compress
    if($status-cne$last){Write-Output $status;$last=$status}
    if($finished.Count-eq$workers.Count){if($total-ne$launch.requiredCount){throw 'Final count mismatch'};Write-Output 'ORIGINAL_REGRESSION_COMPLETE';break}
    Start-Sleep -Seconds 45
}
