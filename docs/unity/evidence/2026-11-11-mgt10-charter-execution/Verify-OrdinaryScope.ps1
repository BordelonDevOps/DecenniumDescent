param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$ReportPath
)
$ErrorActionPreference = 'Stop'
$assemblies = @('Core', 'Persistence', 'LabModel', 'HeadlessTests' | ForEach-Object {
    (Resolve-Path (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll")).Path
})
$assemblies | ForEach-Object { Add-Type -Path $_ }
$cases = [Decennium.Foundation.Tests.FoundationCases]
$flags = [Reflection.BindingFlags]'Static,NonPublic'
function Invoke-Fixture([string]$Name, [object[]]$Arguments) {
    $cases.GetMethod($Name, $flags).Invoke($null, $Arguments)
}
function Assert-True([bool]$Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}
function Attempt-Result($State) {
    $attempt = $State.CharterAttempt
    $actor = $State.Actors | Where-Object Id -EQ $attempt.Authority.HeroId
    [ordered]@{
        clock = $State.RuleClock.ToString()
        revision = $State.Revision
        position = @($actor.X, $actor.Y)
        outcome = $attempt.Outcome.ToString()
        events = @($attempt.Events | ForEach-Object {
            [ordered]@{ kind = $_.Kind.ToString(); clock = $_.At.ToString(); revision = $_.Revision; reason = $_.Reason }
        })
    }
}

$scope = Invoke-Fixture 'AttemptReady' @($null)
$baseline = $scope.Capture()
$hero = $baseline.NextCharterAgreement.Terms.ParticipantId
$policy = Invoke-Fixture 'AttemptPolicy' @($null, $null, $null)
$earlyReturn = [Decennium.Foundation.Simulation]::new($policy, $baseline, [Decennium.Foundation.ExecutionProfile]::Laboratory)

Invoke-Fixture 'StartAttempt' @($scope)
Invoke-Fixture 'PlanWalk' @($scope, -1, 0, $hero)
$left = $scope.Capture()
Assert-True ($left.CharterAttempt.Stop.Kind.ToString() -eq 'ScopeLeft') 'Unrelated movement left the attempt open.'
Assert-True (($left.Actors | Where-Object Id -EQ $hero).X -eq 1) 'The unrelated ordinary step did not resolve.'
foreach ($direction in @(1, 1, -1)) {
    Invoke-Fixture 'PlanWalk' @($scope, $direction, 0, $hero)
}
$ordinary = $scope.Capture()
Assert-True ($null -eq $ordinary.CharterAttempt.OutboundStarted -and $null -eq $ordinary.CharterAttempt.Returned) 'Later ordinary passage received objective credit.'
Assert-True (($ordinary.Actors | Where-Object Id -EQ $hero).X -eq 2) 'Ordinary travel did not return the hero to staging.'

Invoke-Fixture 'StartAttempt' @($earlyReturn)
Invoke-Fixture 'WorldStep' @($earlyReturn, 1, 0, $false, $hero)
Invoke-Fixture 'WorldAdvance' @($earlyReturn, 3, 2)
Invoke-Fixture 'WorldStep' @($earlyReturn, -1, 0, $false, $hero)
Invoke-Fixture 'WorldAdvance' @($earlyReturn, 3, 2)
$returned = $earlyReturn.Capture()
Assert-True ($null -ne $returned.CharterAttempt.OutboundArrived -and $null -eq $returned.CharterAttempt.Observed) 'The return control did not keep actual arrival and missing observation separate.'
Assert-True ($returned.CharterAttempt.Outcome.ToString() -eq 'ReturnedIncomplete' -and $returned.CharterAttempt.Stop.Reason -eq 'CharterReturnedWithoutObservation') 'Returning before observation received successful objective credit.'

[ordered]@{
    status = 'PASS'
    authority = 'TEST_ONLY'
    schema = $returned.SchemaVersion
    leftScope = Attempt-Result $left
    ordinaryTravelAfterScopeLeft = Attempt-Result $ordinary
    physicalReturnWithoutObservation = Attempt-Result $returned
    assemblyHashes = @($assemblies | ForEach-Object {
        [ordered]@{ name = Split-Path $_ -Leaf; sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ReportPath -Encoding utf8
