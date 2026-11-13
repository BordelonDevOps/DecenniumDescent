param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$Run=(New-Item -ItemType Directory -Path $Run).FullName
$prior=(Resolve-Path "$PSScriptRoot/../2026-11-13-mgt01-finished-vial/public/Restored").Path
foreach($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
function Require($value,$message) { if (!$value) { throw $message } }
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithCarriedVial()
$session.Restore("$prior/remote.ddsave")
$session.Save("$Run/wire96-roundtrip.ddsave")
Require ((Digest "$Run/wire96-roundtrip.ddsave") -ceq (Digest "$prior/remote.ddsave")) 'Authentic wire96 load changed bytes.'
$selected=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithStowedVial()
$before="$Run/new-before.ddsave"
$selected.Save($before)
$rejected=$false
try { $selected.Restore("$prior/remote.ddsave") } catch [ArgumentException] { $rejected=$true }
$selected.Save("$Run/new-after.ddsave")
Require ($rejected -and (Digest $before) -ceq (Digest "$Run/new-after.ddsave")) 'Cross-profile wire96 load was not atomic.'
$store=[Decennium.Foundation.FileSaveStore]::new()
$final=$store.Load("$prior/vial-continued.ddsave")
$matched=[ordered]@{}
foreach($receipt in $final.Receipts | Where-Object Revision -GT 115) {
    $command=[Decennium.Foundation.CommandHistory]::Read($receipt)
    $result=if($receipt.Principal -eq 'TEST_ONLY.tac10-later-defender.v1') { $session.AdvanceAutomaticDefender() }
        elseif($command.Kind -in 'AdvanceClock','EndFixedEncounter') { $session.SubmitSessionCommand($command) }
        else { $session.Submit('Player',$command) }
    Require ($result.Response -eq 'Committed' -and $result.Revision -eq $receipt.Revision) "Historical continuation failed at $($receipt.Revision)."
    if($receipt.Revision -in 116,164) {
        $mark=if($receipt.Revision -eq 116){'remote-used'}else{'vial-continued'}
        $session.Save("$Run/$mark.ddsave")
        $matched[$mark]=Digest "$Run/$mark.ddsave"
        Require ($matched[$mark] -ceq (Digest "$prior/$mark.ddsave")) "Historical bytes differ at $mark."
    }
}
[ordered]@{Status='PASS'; Wire=96; Authentic=(Digest "$prior/remote.ddsave"); Continuation=$matched; CrossProfileAtomic=$true} |
    ConvertTo-Json -Depth 6 | Set-Content "$Run/results.json" -Encoding utf8
Get-Content "$Run/results.json"
