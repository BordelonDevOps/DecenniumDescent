param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$CaseName)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$run=New-Item -ItemType Directory -Path (Join-Path $PSScriptRoot ('case-'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')))
$assemblies=@('Core','Persistence','LabModel','HeadlessTests')
foreach($part in $assemblies){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$started=[DateTime]::UtcNow.ToString('o')
$results=@([Decennium.Foundation.Tests.FoundationCases]::Run($CaseName,(Join-Path $run.FullName 'saves')))
$failed=@($results|Where-Object {-not $_.Passed})
$build=Get-Content -LiteralPath (Join-Path $AssemblyRoot 'results.json') -Raw|ConvertFrom-Json
[ordered]@{status=$(if($results.Count-eq1-and$failed.Count-eq0){'PASS'}else{'FAIL'});startedUtc=$started;
    finishedUtc=[DateTime]::UtcNow.ToString('o');compiledSourceReport=(Join-Path $AssemblyRoot 'results.json');
    assemblies=@($assemblies|ForEach-Object{@{name=$_;sha256=(Get-FileHash -LiteralPath (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll")).Hash.ToLowerInvariant()}});
    sourceHashes=$build.sourceHashes;passed=$results.Count-$failed.Count;failed=$failed.Count;cases=$results
}|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $run.FullName 'results.json') -Encoding utf8
Write-Output ("Connected case: $($results.Count-$failed.Count)/$($results.Count); $($run.FullName)")
if($failed.Count-ne0){$failed|Format-List;exit 1}
