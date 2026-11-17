param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$InputPath,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$sourceInputPath=(Resolve-Path -LiteralPath $InputPath).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh reference output directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
. (Join-Path $PSScriptRoot '../../2026-11-16-tac03-declared-geometry-runtime/support/Execution-SourceBinding.ps1')
$executionSourceBinding=Start-GeometryExecutionBinding $Run @((Join-Path $PSScriptRoot '../../2026-11-16-tac03-declared-geometry-runtime/support/Geometry-ReadProbes.ps1'),(Join-Path $PSScriptRoot '../../2026-11-16-tac03-declared-geometry-runtime/support/Geometry-TraceCommand.ps1'),$PSCommandPath,(Join-Path $PSScriptRoot 'Ferry-ReadProbes.ps1'),(Join-Path $PSScriptRoot 'Ferry-TraceCommand.ps1'),(Join-Path $PSScriptRoot '../../2026-11-16-chr03-bishop-runtime/support/Bishop-ReadProbes.ps1'),(Join-Path $PSScriptRoot 'Ferry-TypedCommand.ps1'),(Join-Path $PSScriptRoot '../../../../../engine/tools/Open-ConnectedExpedition.ps1'))
. (Join-Path $PSScriptRoot 'Ferry-TypedCommand.ps1')
. (Join-Path $PSScriptRoot 'Ferry-ReadProbes.ps1')
$empty=Join-Path $Run 'empty.jsonl';[IO.File]::WriteAllText($empty,'')
. (Join-Path $repository 'engine/tools/Open-ConnectedExpedition.ps1') -FerryWraith -AssemblyRoot $AssemblyRoot -InputPath $empty
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$requests=@(Get-Content -LiteralPath $sourceInputPath|ForEach-Object{ConvertFrom-Json -AsHashtable $_})
$marks=[Collections.Generic.List[object]]::new();$retained=[Collections.Generic.List[object]]::new();$responses=[Collections.Generic.List[string]]::new()
$store=[Decennium.Foundation.FileSaveStore]::new();$revision=0;$names=[Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
function Dispatch-Reference($request) {
    $line=ConvertTo-Json -InputObject $request -Depth 12 -Compress
    $response=Write-SessionResponse $line
    $retained.Add($request);$responses.Add($response)
    return $response
}
Push-Location $Run
try {
    foreach($request in $requests){
        if($request.op-in'view','load','query','discover'-or$request.evidenceRead){continue}
        if($request.op-eq'save'){
            $name=[IO.Path]::GetFileName($request.path)
            if($name.EndsWith('.after-probes.ddsave')-or!$names.Add($name)){continue}
            $saved=Dispatch-Reference @{op='save';path=$name}|ConvertFrom-Json
            if($saved.Response-ne'Saved'){throw "Save failed: $name"}
            $snapshot=$store.Load((Join-Path $Run $name));$views=[ordered]@{};$probes=[Collections.Generic.List[object]]::new()
            foreach($seat in 'Player','FirstOpponent','RecoveryOpponent','FerryOpponent'){
                $viewName=$name+'.'+$seat+'.view.json';$requestView=@{op='view';seat=$seat;evidenceView=$viewName}
                $view=Dispatch-Reference $requestView;[IO.File]::WriteAllText((Join-Path $Run $viewName),$view)
                $views[$seat]=@{name=$viewName;sha256=(Digest (Join-Path $Run $viewName))}
            }
            foreach($probe in @(New-FerryProbes $snapshot $name)){
                $response=Dispatch-Reference $probe;[IO.File]::WriteAllText((Join-Path $Run $probe.evidenceRead),$response)
                if($probe.expectedResponse-and($response|ConvertFrom-Json).Response-ne$probe.expectedResponse){throw "Unexpected probe response $($probe.evidenceRead): $response"}
                $probes.Add(@{request=$probe;sha256=(Digest (Join-Path $Run $probe.evidenceRead))})
            }
            $null=Dispatch-Reference @{op='save';path=$name+'.after-probes.ddsave'}
            if((Digest (Join-Path $Run $name))-cne(Digest (Join-Path $Run ($name+'.after-probes.ddsave')))){throw "Reads/denials changed $name"}
            $null=Dispatch-Reference @{op='load';path=$name}
            $marks.Add(@{name=$name;revision=$snapshot.Revision;sha256=(Digest (Join-Path $Run $name));views=$views;probes=$probes.ToArray()})
            continue
        }
        if($request.op-eq'clock'){$request.kind='AdvanceClock';$request.actor='TEST_ONLY.actor';$request.target=''}
        if($request.op-eq'close'){$request.kind='EndFixedEncounter';$request.actor='TEST_ONLY.actor'}
        if($request.op-ne'auto'){
            if(!$request.ContainsKey('revision')){$request.revision=$revision}
            if(!$request.ContainsKey('x')){$request.x=0};if(!$request.ContainsKey('y')){$request.y=0}
        }
        $response=Dispatch-Reference $request|ConvertFrom-Json
        $revision++
        if($response.Response-ne'Committed'-or$response.Revision-ne$revision){throw "Reference failed at $revision`: $($request|ConvertTo-Json -Compress) / $($response|ConvertTo-Json -Compress)"}
    }
    $final=$marks[-1]
    $source=Get-Content -LiteralPath (Join-Path (Split-Path $sourceInputPath) 'source.json') -Raw|ConvertFrom-Json
    if($final.sha256-cne$source.sourceSha256){throw 'Fresh console replay differs from the genuine completed source.'}
    if($final.revision-ne$revision){throw 'Final checkpoint does not cover all commands.'}
    $retained|ForEach-Object{ConvertTo-Json -InputObject $_ -Depth 12 -Compress}|Set-Content -LiteralPath (Join-Path $Run 'inputs.jsonl') -Encoding utf8
    $responses|Set-Content -LiteralPath (Join-Path $Run 'responses.jsonl') -Encoding utf8
    [ordered]@{status='PASS_REFERENCE';scope='Fresh Ferry console reference through genuine completed r463; five independent qualification paths still required';revision=$revision;
        inputSource=$sourceInputPath;inputSha256=(Digest $sourceInputPath);finalSource=(Join-Path $Run $final.name);finalSha256=$final.sha256;marks=$marks.ToArray();
        assemblies=@('Core','Persistence','LabModel'|ForEach-Object{@{name=$_;sha256=(Digest (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll"))}})
    }|ConvertTo-Json -Depth 16|Set-Content -LiteralPath (Join-Path $Run 'manifest.json') -Encoding utf8
    Write-Output "Reference passed $revision commands and $($marks.Count) checkpoints."
}finally{Pop-Location;Complete-GeometryExecutionBinding $Run $executionSourceBinding}
