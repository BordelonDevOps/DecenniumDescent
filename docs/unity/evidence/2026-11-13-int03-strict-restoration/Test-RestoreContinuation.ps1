param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Run
)
$ErrorActionPreference='Stop'
$Run=(New-Item -ItemType Directory -Force $Run).FullName
$AssemblyRoot=(Resolve-Path $AssemblyRoot).Path
$launcher=(Resolve-Path (Join-Path $PSScriptRoot '../../../../engine/tools/Open-ConnectedExpedition.ps1')).Path
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
function Require([bool]$ok,[string]$message) { if (-not $ok) { throw $message } }
function Digest([string]$file) { (Get-FileHash -LiteralPath $file).Hash.ToLowerInvariant() }
$results=[ordered]@{}
foreach ($profile in 'Default','FishingTrap') {
    $trap=$profile -eq 'FishingTrap'
    $accepted=if ($trap) {'2026-11-12-mgt06-connected-trap'} else {'2026-11-12-exp05-local-mining'}
    $source=(Resolve-Path (Join-Path $PSScriptRoot "../$accepted/connected")).Path
    $folder=(New-Item -ItemType Directory -Force (Join-Path $Run $profile)).FullName
    $checks=if ($trap) { 'pending-setup','away-pending','pending-retrieval','trap-continued' } else { 'partial-edge','travel-continued' }
    Push-Location $folder
    try { & $launcher -FishingTrap:$trap -AssemblyRoot $AssemblyRoot -InputPath "$source/walkthrough.jsonl" |
        Set-Content 'responses.jsonl' -Encoding utf8 }
    finally { Pop-Location }
    $reference=(Resolve-Path (Join-Path $PSScriptRoot "../2026-11-13-int03-active-work-performance/connected/$profile/responses.jsonl")).Path
    Require ((Digest $reference) -ceq (Digest "$folder/responses.jsonl")) "$profile complete console transcript changed."
    $expected=@(Get-Content $reference | ForEach-Object { ConvertFrom-Json $_ })
    $actual=@(Get-Content "$folder/responses.jsonl" | ForEach-Object { ConvertFrom-Json $_ })
    Require ($expected.Count -eq $actual.Count) "$profile transcript is incomplete."
    for ($i=0;$i -lt $actual.Count;$i++) {
        Require ($expected[$i].Response -ceq $actual[$i].Response -and $expected[$i].Revision -eq $actual[$i].Revision -and
            $expected[$i].Clock.Numerator -eq $actual[$i].Clock.Numerator -and
            $expected[$i].Clock.Denominator -eq $actual[$i].Clock.Denominator) "$profile public response differs at input $i."
    }
    $digests=[ordered]@{}
    foreach ($name in $checks) {
        $digests[$name]=Digest "$folder/$name.ddsave"
        Require ($digests[$name] -ceq (Digest "$source/$name.ddsave")) "$profile canonical checkpoint differs: $name."
    }
    $session=if ($trap) {[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFishingTrap()}
        else {[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()}
    $last=@($checks)[-1]
    $session.Restore("$source/$last.ddsave")
    $session.Save("$folder/authentic.ddsave")
    Require ((Digest "$folder/authentic.ddsave") -ceq $digests[$last]) "$profile authentic save changed."
    if ($trap) {
        $session.Save("$folder/before-reject.ddsave")
        $rejected=$false
        try { $session.Restore("$source/forged-history.ddsave") } catch [ArgumentException] { $rejected=$true }
        $session.Save("$folder/after-reject.ddsave")
        Require ($rejected -and (Digest "$folder/before-reject.ddsave") -ceq (Digest "$folder/after-reject.ddsave")) 'Altered history replaced live state.'
    }
    $results[$profile]=[ordered]@{Inputs=$actual.Count; Committed=@($actual | Where-Object Response -eq 'Committed').Count
        Checkpoints=$digests; Authentic=(Digest "$folder/authentic.ddsave"); TranscriptSha256=(Digest $reference)}
}
[ordered]@{Status='PASS'; Profiles=$results} | ConvertTo-Json -Depth 8 | Set-Content "$Run/results.json" -Encoding utf8
Get-Content "$Run/results.json"
