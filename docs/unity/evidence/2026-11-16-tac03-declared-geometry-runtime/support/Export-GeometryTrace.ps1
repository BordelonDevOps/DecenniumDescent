param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$FinalSource,[Parameter(Mandatory)][string]$MarksDirectory,[Parameter(Mandatory)][string]$Output)
$ErrorActionPreference='Stop'
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
. (Join-Path $PSScriptRoot '../../2026-11-16-chr03-bishop-runtime/support/Bishop-TypedCommand.ps1')
. (Join-Path $PSScriptRoot 'Geometry-TraceCommand.ps1')
if(Test-Path -LiteralPath $Output){throw 'Use a fresh export directory'}
$Output=(New-Item -ItemType Directory -Path $Output).FullName
$store=[Decennium.Foundation.FileSaveStore]::new();$final=$store.Load((Resolve-Path -LiteralPath $FinalSource).Path)
if($final.WireSchemaVersion-ne113){throw 'Expected genuine declared geometry source'}
$marks=[Collections.Generic.List[object]]::new()
foreach($file in Get-ChildItem -LiteralPath $MarksDirectory -File -Filter '*.ddsave'){
    $s=$store.Load($file.FullName)
    if($s.WireSchemaVersion-ne113-or$s.Revision-gt$final.Revision){continue}
    $prefix=$true
    for($i=0;$i-lt$s.Receipts.Length;$i++){
        $a=$s.Receipts[$i];$b=$final.Receipts[$i]
        if($a.Id-cne$b.Id-or$a.Principal-cne$b.Principal-or$a.Fingerprint-cne$b.Fingerprint){$prefix=$false;break}
    }
    if($prefix){$marks.Add(@{name=$file.Name;revision=$s.Revision;sha256=(Get-FileHash -LiteralPath $file.FullName).Hash.ToLowerInvariant()})}
}
if(!@($marks|Where-Object revision -eq $final.Revision).Count){throw 'No final authentic checkpoint'}
$requests=[Collections.Generic.List[object]]::new()
function Add-Marks($revision){foreach($mark in @($marks|Where-Object revision -eq $revision|Sort-Object name)){$requests.Add(@{op='save';path=$mark.name})}}
Add-Marks 0
foreach($receipt in $final.Receipts){$requests.Add((ConvertTo-GeometryRequest $receipt));Add-Marks $receipt.Revision}
$requests|ForEach-Object{ConvertTo-Json -InputObject $_ -Depth 12 -Compress}|Set-Content -LiteralPath (Join-Path $Output 'inputs.jsonl') -Encoding utf8
[ordered]@{scope='Exact public requests exported from genuine development receipts; no execution claimed';source=(Resolve-Path -LiteralPath $FinalSource).Path;sourceSha256=(Get-FileHash -LiteralPath $FinalSource).Hash.ToLowerInvariant();revision=$final.Revision;marks=$marks.ToArray()}
    |ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $Output 'source-marks.json') -Encoding utf8
Write-Output "Exported $($final.Revision) requests and $($marks.Count) genuine prefix checkpoints."
