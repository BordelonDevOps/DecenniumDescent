param([string]$AssemblyRoot,[string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
$old=(Resolve-Path "$PSScriptRoot/../2026-11-14-mgt03-short-rest").Path
$launcher=(Resolve-Path "$PSScriptRoot/../../../../engine/tools/Open-ConnectedExpedition.ps1").Path
function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
function Require($test,$message) { if (!$test) { throw $message } }
& "$old/Test-ShortRestWalkthrough.ps1" -AssemblyRoot $AssemblyRoot -Launcher $launcher -Run "$Run/wire103"
$accepted=Get-Content "$old/public/results.json" -Raw | ConvertFrom-Json -AsHashtable
$current=Get-Content "$Run/wire103/results.json" -Raw | ConvertFrom-Json -AsHashtable
$checks=[ordered]@{}
foreach ($branch in 'completion','whole','interruption') {
    $hashes=[ordered]@{}
    foreach ($key in $accepted.Branches[$branch].DirectCheckpoints.Keys) {
        Require ($current.Branches[$branch].DirectCheckpoints[$key] -ceq $accepted.Branches[$branch].DirectCheckpoints[$key]) "Authentic wire103 $branch/$key bytes changed."
        $hashes[$key]=$current.Branches[$branch].DirectCheckpoints[$key]
    }
    foreach ($mode in 'Restored','Uninterrupted') {
        Require ((Digest "$Run/wire103/$branch/$mode/responses.jsonl") -ceq (Digest "$old/public/$branch/$mode/responses.jsonl")) "Authentic wire103 $branch/$mode transcript changed."
    }
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithShortRest()
    $roundtrips=[ordered]@{}
    foreach ($point in 'rest-pending','rest-completed','rest-continued') {
        $source="$old/public/$branch/Restored/$point.ddsave"
        $session.Restore($source)
        $target="$Run/wire103/$branch/authentic-$point.ddsave"
        $session.Save($target)
        Require ((Digest $target) -ceq (Digest $source)) "Authentic wire103 $branch/$point roundtrip changed."
        $roundtrips[$point]=Digest $target
    }
    $checks[$branch]=@{Checkpoints=$hashes;AuthenticRoundtrips=$roundtrips}
}
$calendar=(Resolve-Path "$PSScriptRoot/../2026-11-14-mgt03-rest-calendar").Path
& "$calendar/Test-RestCalendarWalkthrough.ps1" -AssemblyRoot $AssemblyRoot -Launcher $launcher -Run "$Run/wire103-calendar"
$calendarAccepted=Get-Content "$calendar/public/results.json" -Raw | ConvertFrom-Json -AsHashtable
$calendarCurrent=Get-Content "$Run/wire103-calendar/results.json" -Raw | ConvertFrom-Json -AsHashtable
foreach ($branch in 'split','whole') {
    foreach ($key in $calendarAccepted.Branches[$branch].DirectCheckpoints.Keys) {
        Require ($calendarCurrent.Branches[$branch].DirectCheckpoints[$key] -ceq $calendarAccepted.Branches[$branch].DirectCheckpoints[$key]) "Corrected wire103 $branch/$key changed."
    }
    foreach ($mode in 'Restored','Uninterrupted') {
        Require ((Digest "$Run/wire103-calendar/$branch/$mode/responses.jsonl") -ceq (Digest "$calendar/public/$branch/$mode/responses.jsonl")) "Corrected wire103 transcript changed."
    }
}
# Cross-profile restoration must leave the new session unchanged.
$newSession=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFleshWarden()
$newSession.Save("$Run/new-before.ddsave")
$rejected=$false
try { $newSession.Restore("$old/public/completion/Restored/rest-pending.ddsave") } catch { $rejected=$true }
Require $rejected 'The wire104 profile accepted an authentic wire103 save.'
$newSession.Save("$Run/new-after.ddsave")
Require ((Digest "$Run/new-before.ddsave") -ceq (Digest "$Run/new-after.ddsave")) 'Cross-profile denial changed new session.'
& "$old/Test-PreviousProfiles.ps1" -AssemblyRoot $AssemblyRoot -Run "$Run/wire96-102"
& "$PSScriptRoot/../2026-11-13-int03-strict-restoration/Test-RestoreContinuation.ps1" -AssemblyRoot $AssemblyRoot -Run "$Run/wire95"
[ordered]@{Status='PASS';Wire103=$checks;Wire103Calendar=$calendarCurrent;Wire104RejectsWire103=$true;Wire96Through102=(Get-Content "$Run/wire96-102/results.json" -Raw | ConvertFrom-Json)
    Wire95=(Get-Content "$Run/wire95/results.json" -Raw | ConvertFrom-Json)} |
    ConvertTo-Json -Depth 20 | Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: authentic wire95-103 compatibility and accepted wire103 branches in $Run"
