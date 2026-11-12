param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$SaveRoot,
    [Parameter(Mandatory)][string]$OutputPath
)
$ErrorActionPreference = 'Stop'
foreach ($name in 'Core','Persistence','LabModel') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$defender = [Decennium.Foundation.Laboratory.TestOnlySharedWorldPolicy]::LaterDefenderId
$hero = [Decennium.Foundation.Laboratory.TestOnlyPolicy]::ActorId
$principal = [Decennium.Foundation.Laboratory.LaterDefenderController]::Principal
$states = @(foreach ($file in Get-ChildItem -LiteralPath $SaveRoot -Filter 'tac10-*.ddsave' | Sort-Object Name) {
    $bytes = [IO.File]::ReadAllBytes($file.FullName)
    $state = $codec.Decode($bytes)
    $move = [Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::PendingMove($state)
    [ordered]@{
        file = $file.Name
        sha256 = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
        clock = $state.RuleClock.ToString()
        revision = $state.Revision
        wire = $state.WireSchemaVersion
        fingerprint = $state.ContentFingerprint
        tactical = $state.InventoryCombat
        currentActor = $state.Encounter.CurrentActor
        hero = @($state.Actors | Where-Object Id -ceq $hero | Select-Object X,Y)
        defender = @($state.Actors | Where-Object Id -ceq $defender | Select-Object X,Y)
        pendingResponder = if ($move) { $move.Reactors[$move.ResponseIndex] } else { $null }
        copper = $state.HavenSales[0].PaymentCopper
        manufacturedDoses = $state.AlchemyDoses.Length
        spentDoses = @($state.AlchemyDoses | Where-Object Spent | Select-Object Id,ActualHealing,PotentialHealing)
        defenderAttacks = @($state.MeleeAttacks | Where-Object AttackerId -ceq $defender |
            ForEach-Object { [ordered]@{revision=$_.Revision;opportunity=$_.Opportunity;target=$_.TargetId;at=$_.At.ToString()} })
        defenderReceipts = @($state.Receipts | Where-Object Principal -ceq $principal |
            ForEach-Object { [ordered]@{
                revision = $_.Revision
                id = $_.Id
                kind = ([Decennium.Foundation.CommandKind]([int]($_.Fingerprint.Split('|')[0]))).ToString()
            } })
    }
})
if ($states.Count -eq 0) { throw 'No controller saves were measured.' }
@{status='PASS';states=$states} | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $OutputPath -Encoding utf8
