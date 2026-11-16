param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$CompatibilityRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$evidence=Join-Path $repository 'docs/unity/evidence'
$accepted=Join-Path $evidence '2026-11-15-tac08-cleric-casting/implementation-amended'
$oldLaunch=Get-Content -LiteralPath (Join-Path $accepted 'regression/launch.json') -Raw|ConvertFrom-Json -AsHashtable
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
$oldRoot=Join-Path $Run 'accepted-predecessor-assemblies'
Expand-Archive -LiteralPath (Join-Path $accepted 'execution-assemblies.zip') -DestinationPath $oldRoot
function Digest($path){(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
foreach($part in 'Core','Persistence','LabModel'){
    $file="Decennium.Foundation.$part.dll"
    if((Digest (Join-Path $oldRoot $file))-cne$oldLaunch.assemblies[$file]){throw 'Accepted predecessor binary changed'}
}
$oldScript=Join-Path $Run 'accepted-predecessor-console.ps1'
& git -C $repository show '0e5928bddd5abce47c16ff86172f5613423a2460:engine/tools/Open-ConnectedExpedition.ps1'|Set-Content -LiteralPath $oldScript -Encoding utf8
if($LASTEXITCODE-ne0){throw 'Could not retain accepted console'}
$newScript=Join-Path $repository 'engine/tools/Open-ConnectedExpedition.ps1'
$compat=Get-Content -LiteralPath (Join-Path $CompatibilityRoot 'results.json') -Raw|ConvertFrom-Json
if($compat.Status-ne'PASS'-or$compat.Cases.Count-ne25){throw 'Authentic compatibility run must pass first'}
$rows=[Collections.Generic.List[object]]::new()
foreach($case in $compat.Cases){
    $folder=(New-Item -ItemType Directory -Path (Join-Path $Run ('case-'+$rows.Count+'-wire'+$case.Wire))).FullName
    $inputPath=Join-Path $folder 'inputs.jsonl'
    @(@{op='view';seat='Player'},@{op='view';seat='FirstOpponent'},
      @{op='load';path=(Join-Path $evidence $case.Source)},@{op='view';seat='Player'},@{op='view';seat='FirstOpponent'})|
        ForEach-Object{ConvertTo-Json $_ -Compress}|Set-Content -LiteralPath $inputPath -Encoding utf8
    [string[]]$flags=@(if($case.Factory-ne'Start'){'-'+$case.Factory.Substring(9)})
    [string[]]$oldArguments=@('-NoProfile','-File',$oldScript,'-AssemblyRoot',$oldRoot,'-InputPath',$inputPath)+$flags
    [string[]]$newArguments=@('-NoProfile','-File',$newScript,'-AssemblyRoot',$AssemblyRoot,'-InputPath',$inputPath)+$flags
    @{old=$oldArguments;current=$newArguments}|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $folder 'invocations.json') -Encoding utf8
    & pwsh @oldArguments|Set-Content -LiteralPath (Join-Path $folder 'old.jsonl') -Encoding utf8
    if($LASTEXITCODE-ne0){throw 'Accepted console failed'}
    & pwsh @newArguments|Set-Content -LiteralPath (Join-Path $folder 'new.jsonl') -Encoding utf8
    if($LASTEXITCODE-ne0){throw 'Current console failed'}
    $old=@(Get-Content -LiteralPath (Join-Path $folder 'old.jsonl')|ConvertFrom-Json -AsHashtable)
    $new=@(Get-Content -LiteralPath (Join-Path $folder 'new.jsonl')|ConvertFrom-Json -AsHashtable)
    if($old.Count-ne5-or$new.Count-ne5-or$old[2].Response-ne'Restored'-or$new[2].Response-ne'Restored'){
        throw 'Console did not restore the authentic save'
    }
    foreach($index in 0,1,3,4){
        # Ordered serialization is stable for these source-derived public DTOs;
        # compare complete property names and values, not just property counts.
        $a=ConvertTo-Json $old[$index] -Depth 30 -Compress
        $b=ConvertTo-Json $new[$index] -Depth 30 -Compress
        if($a-cne$b){throw "Old public projection differs: wire$($case.Wire), view $index"}
    }
    $rows.Add(@{wire=$case.Wire;source=$case.Source;views=4;oldOutputSha256=(Digest (Join-Path $folder 'old.jsonl'));
        newOutputSha256=(Digest (Join-Path $folder 'new.jsonl'))})
}
@{status='PASS';scope='Exact old public property shapes and values at initial and authentic continued checkpoints for both seats';
    predecessorCommit='0e5928bddd5abce47c16ff86172f5613423a2460';oldConsoleSha256=(Digest $oldScript);
    newConsoleSha256=(Digest $newScript);cases=@($rows)}|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output "PASS: $($rows.Count*4) authentic old public projections across wire95-109."
