param([string]$AssemblyRoot,[string[]]$Sources,[string]$Class,[string]$Method,[string[]]$Arguments,[string]$Run,[string]$TestsAssembly)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path;$Run=[IO.Path]::GetFullPath($Run)
if(Test-Path -LiteralPath $Run){throw 'Use a fresh output folder.'}
$refs=@(Get-ChildItem -LiteralPath (Join-Path $PSHOME 'ref') -Filter '*.dll'|ForEach-Object FullName)
$dlls=@();foreach($part in 'Core','Persistence','LabModel','HeadlessTests'){$dll=if($part-eq'HeadlessTests'-and$TestsAssembly){(Resolve-Path -LiteralPath $TestsAssembly).Path}else{Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll"};Add-Type -Path $dll;$refs+=$dll;$dlls+=$dll}
$null=New-Item -ItemType Directory -Path $Run
$Sources=@($Sources|ForEach-Object{(Resolve-Path -LiteralPath $_).Path})
foreach($source in $Sources){Copy-Item -LiteralPath $source -Destination $Run};Copy-Item -LiteralPath $PSCommandPath -Destination $Run
$report=[ordered]@{status='FAIL';startedUtc=[DateTime]::UtcNow.ToString('o');sourceRun=$AssemblyRoot;class=$Class;method=$Method;arguments=$Arguments;sourceHashes=@($Sources|ForEach-Object{@{path=$_;sha256=(Get-FileHash -LiteralPath $_).Hash.ToLowerInvariant()}});assemblyHashes=@($dlls|ForEach-Object{@{path=$_;sha256=(Get-FileHash -LiteralPath $_).Hash.ToLowerInvariant()}})}
try{Add-Type -Path $Sources -ReferencedAssemblies $refs -CompilerOptions @('/langversion:9.0','/warnaserror');$type=$Class-as[type];$argsArray=[object[]]@($Run,[string[]]$Arguments);$return=$type.GetMethod($Method).Invoke($null,$argsArray);if($null-ne$return-and$return-ne0){throw "Probe returned $return"};$report.status='PASS'}
catch{$report.error=$_.Exception.ToString()}
finally{$report.finishedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $Run 'execution.json');Write-Output ($report.status+': '+$Run)}
if($report.status-ne'PASS'){throw $report.error}
