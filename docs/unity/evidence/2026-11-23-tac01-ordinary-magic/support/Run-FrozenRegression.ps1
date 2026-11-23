param([string]$AssemblyRoot,[string]$Run,[int]$Worker,[int]$Workers=4)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run=[IO.Path]::GetFullPath($Run)
if($Worker-lt0-or$Worker-ge$Workers){throw 'Invalid worker partition.'}
if(Test-Path -LiteralPath $Run){throw 'Use a new worker directory.'}
$null=New-Item -ItemType Directory -Path $Run
$baseline=Get-Content -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Raw|ConvertFrom-Json
if($baseline.coreCompilation-ne'PASS'){throw 'Missing successful frozen compilation.'}
foreach($part in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$names=[Decennium.Foundation.Tests.FoundationCases]::Names()
$selected=@(for($i=$Worker;$i-lt$names.Length;$i+=$Workers){$names[$i]})
$report=[ordered]@{status='RUNNING';runner='Frozen C#9 compiled FoundationCases; deterministic disjoint name partitions';worker=$Worker;workers=$Workers;totalDiscovered=$names.Length;assigned=$selected.Count;completed=0;passed=0;failed=0;startedUtc=[DateTime]::UtcNow.ToString('o');sourceRun=$AssemblyRoot;sourceHashes=$baseline.sourceHashes;assemblyHashes=@(Get-ChildItem -LiteralPath $AssemblyRoot -Filter '*.dll'|ForEach-Object{@{name=$_.Name;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash.ToLowerInvariant()}});cases=@();unityCompilation='NOT RUN';moduleAcceptance='OPEN'}
$selected|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $Run 'assigned.json') -Encoding utf8
Copy-Item -LiteralPath $PSCommandPath -Destination $Run
try{
    foreach($name in $selected){
        $caseDir=Join-Path $Run ('cases/'+$name)
        $null=New-Item -ItemType Directory -Path $caseDir -Force
        @{status='RUNNING';name=$name;completed=$report.completed;assigned=$selected.Count;startedUtc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $Run 'progress.json') -Encoding utf8
        $watch=[Diagnostics.Stopwatch]::StartNew()
        $case=[Decennium.Foundation.Tests.FoundationCases]::Run($name,$caseDir)
        $watch.Stop()
        $row=[ordered]@{Name=$case.Name;Passed=$case.Passed;Error=$case.Error;elapsedMilliseconds=$watch.ElapsedMilliseconds}
        $row|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $caseDir 'result.json') -Encoding utf8
        $report.cases+=,$row;$report.completed++
        if($case.Passed){$report.passed++}else{$report.failed++;Write-Output ('FAIL '+$name+': '+$case.Error)}
        $report|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
        if($report.completed%25-eq0){Write-Output ("Worker$Worker $($report.completed)/$($selected.Count), failures$($report.failed)")}
    }
    $report.status=if($report.completed-eq$selected.Count-and$selected.Count-gt0-and$report.failed-eq0){'PASS'}else{'FAIL'}
}catch{$report.status='FAIL';$report.error=$_.Exception.ToString()}
finally{$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8;Write-Output ($report.status+': '+$Run)}
if($report.status-ne'PASS'){exit 1}
