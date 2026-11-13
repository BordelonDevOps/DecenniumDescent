param([string]$AssemblyRoot,[string]$Run)
$ErrorActionPreference = 'Stop'
$Run = (New-Item -ItemType Directory -Path $Run).FullName
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
function Require($condition,$message) { if (!$condition) { throw $message } }
function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
$store = [Decennium.Foundation.FileSaveStore]::new()
$new = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithTacticalVial()
$new.Save("$Run/new-before.ddsave")
$profiles = [ordered]@{
    Wire96 = @{Folder='../2026-11-13-mgt01-finished-vial/public/Restored'; Entry='remote'; Marks=@('remote-used','vial-continued')}
    Wire97 = @{Folder='../2026-11-13-mgt01-vial-stow/public/Restored'; Entry='away'; Marks=@('remote','remote-used','stow-continued')}
}
$results = [ordered]@{}
foreach ($profile in $profiles.Keys) {
    $spec = $profiles[$profile]
    $source = (Resolve-Path "$PSScriptRoot/$($spec.Folder)").Path
    $entry = "$source/$($spec.Entry).ddsave"
    $session = if ($profile -eq 'Wire96') {
        [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithCarriedVial()
    } else {
        [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithStowedVial()
    }
    $folder = (New-Item -ItemType Directory "$Run/$profile").FullName
    $rejected = $false
    try { $new.Restore($entry) } catch [ArgumentException] { $rejected = $true }
    $new.Save("$folder/cross-profile.ddsave")
    Require ($rejected -and (Digest "$folder/cross-profile.ddsave") -ceq (Digest "$Run/new-before.ddsave")) "$profile cross-profile restore changed the session."
    $session.Restore($entry)
    $session.Save("$folder/roundtrip.ddsave")
    Require ((Digest "$folder/roundtrip.ddsave") -ceq (Digest $entry)) "$profile changed authentic save bytes."
    $revision = $session.View('Player').Revision
    $marks = @{}
    foreach ($point in $spec.Marks) { $marks[$store.Load("$source/$point.ddsave").Revision] = $point }
    $final = $store.Load("$source/$($spec.Marks[-1]).ddsave")
    $matched = [ordered]@{}
    foreach ($receipt in $final.Receipts | Where-Object Revision -gt $revision) {
        $command = [Decennium.Foundation.CommandHistory]::Read($receipt)
        $result = if ($receipt.Principal -eq 'TEST_ONLY.tac10-later-defender.v1') { $session.AdvanceAutomaticDefender() }
            elseif ($command.Kind -in 'AdvanceClock','EndFixedEncounter') { $session.SubmitSessionCommand($command) }
            else { $session.Submit('Player',$command) }
        Require ($result.Response -eq 'Committed' -and $result.Revision -eq $receipt.Revision) "$profile continuation failed at $($receipt.Revision)."
        if (!$marks.ContainsKey($receipt.Revision)) { continue }
        $point = $marks[$receipt.Revision]
        $session.Save("$folder/$point.ddsave")
        $matched[$point] = Digest "$folder/$point.ddsave"
        Require ($matched[$point] -ceq (Digest "$source/$point.ddsave")) "$profile continuation differs at $point."
    }
    $results[$profile] = [ordered]@{EntryRevision=$revision; Entry=(Digest $entry); Checkpoints=$matched; CrossProfileAtomic=$true}
}
[ordered]@{Status='PASS'; Profiles=$results} | ConvertTo-Json -Depth 8 | Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: authentic wire96 and wire97 round-trip and continuation in $Run"
