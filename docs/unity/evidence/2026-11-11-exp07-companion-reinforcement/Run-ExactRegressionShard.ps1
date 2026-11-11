param([string]$Run,[string]$Focus,[string]$Group)
$ErrorActionPreference='Stop'
foreach($name in 'Core','Persistence','LabModel','HeadlessTests'){
    Add-Type -Path (Join-Path $Focus "Decennium.Foundation.$name.dll")
}
$historical=[System.Collections.Generic.HashSet[string]]::new([string[]](Get-Content -LiteralPath "$Run/historical-names.txt"),[StringComparer]::Ordinal)
$names=@([Decennium.Foundation.Tests.FoundationCases]::Names())
if($names.Count -ne 1424){throw "Unexpected discovered case count $($names.Count)"}
if(@($names | Where-Object {$historical.Contains($_)}).Count -ne 457){throw 'The exact historical names are unavailable'}
$journal=Join-Path $Run "$Group.jsonl"
$existing=[System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
if(Test-Path $journal){Get-Content $journal | ForEach-Object {$null=$existing.Add(($_|ConvertFrom-Json).Name)}}
foreach($name in $names){
    if($historical.Contains($name) -ne ($Group -eq 'historical') -or $existing.Contains($name)){continue}
    $r=[Decennium.Foundation.Tests.FoundationCases]::Run($name,(Join-Path "$Run/saves" $name))
    $r | ConvertTo-Json -Compress | Add-Content -LiteralPath $journal -Encoding utf8
}
'DONE' | Set-Content -LiteralPath (Join-Path $Run "$Group.done")
