param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$SaveRoot,
    [Parameter(Mandatory)][string]$OutputPath
)
$ErrorActionPreference = 'Stop'
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$tests = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'NonPublic,Static'
$argsIn = [object[]]::new(1)
$argsIn[0] = [Decennium.Foundation.Laboratory.ConditionFixtureEvent[]]@()
$policy = $tests.GetMethod('ConnectedObservationPolicy',$flags).Invoke($null,$argsIn).EnableConnectedFormulaResearch().EnableConnectedBloodSpecimen()
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$profile = [Decennium.Foundation.ExecutionProfile]::Laboratory
$source = Join-Path $SaveRoot 'mgt05-connected-blood-delivered-open.ddsave'
$bytes = [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $source).Path)
$authentic = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($bytes),$profile).Capture()
function Reject([string]$Name,[scriptblock]$Change) {
    $copy = $authentic.Copy()
    & $Change $copy
    $stage = 'encode'
    try {
        $forged = $codec.Encode($copy)
        $stage = 'policy restore'
        $null = [Decennium.Foundation.Simulation]::new($policy,$codec.Decode($forged),$profile)
    } catch {
        $errorCause = $_.Exception.GetBaseException()
        if ($errorCause -isnot [ArgumentException]) { throw }
        return [ordered]@{name=$Name; stage=$stage; rejection=$errorCause.Message}
    }
    throw "Restored forged evidence: $Name"
}
$records = @(
    Reject 'specimen removed from its bound vessel' {
        param($state)
        $state.PortableEquipment = @($state.PortableEquipment | ForEach-Object {
            if ($_.Id -ceq $state.BloodSpecimen.LotId) {
                $_.With($_.CustodianId,'',[Decennium.Foundation.PortablePlacement]::Ground,$null,3,3,$null)
            } else { $_ }
        })
    }
    Reject 'successful treatment with altered natural roll' {
        param($state)
        $a = $state.HarvestPreservationTreatmentAttempts[0]
        $state.HarvestPreservationTreatmentAttempts = @($a.Complete($a.CompletedAt,$a.Work,$a.Status,$a.AbilityModifier,
            $a.ProficiencyRank,$a.ProficiencyBonus,$a.Natural + 1,$a.Degree,$a.RandomBefore,$a.RandomAfter,$a.RandomWordsConsumed))
    }
    Reject 'controlled opening cutoff moved one second earlier' {
        param($state)
        $a = $state.HarvestPreservationEvidence[0]
        $state.HarvestPreservationEvidence = @([Decennium.Foundation.HarvestPreservationEvidenceRecord]::new(
            $a.Id,$a.Kind,$a.TreatmentAttemptId,$a.VesselId,$a.CommandId,$a.AppliedRevision,[Decennium.Foundation.RuleTime]::new($a.At.Numerator - $a.At.Denominator,$a.At.Denominator),
            $a.PortableHandlingId,$a.ToolId,$a.CleanToolFactId,'','','',[Decennium.Foundation.HarvestPreservationExposureCause]::None))
    }
    Reject 'controlled opening receipt fingerprint replaced' {
        param($state)
        $a = $state.HarvestPreservationEvidence[0]
        $receipt = $state.Receipts | Where-Object Revision -eq $a.AppliedRevision
        $receipt.Fingerprint = ($state.Receipts | Where-Object Fingerprint -cne $receipt.Fingerprint | Select-Object -First 1).Fingerprint
    }
)
@{status='PASS'; source=$source; sha256=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
    forgeries=$records} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputPath -Encoding utf8
