param(
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$ReportPath,
    [Parameter(Mandatory)][string]$ExpectedCode
)
$ErrorActionPreference='Stop'
$assemblies=@('Core','Persistence','LabModel','HeadlessTests' | ForEach-Object {
    (Resolve-Path (Join-Path $AssemblyRoot "Decennium.Foundation.$_.dll")).Path
})
$assemblies | ForEach-Object { Add-Type -Path $_ }
$type=[Decennium.Foundation.Tests.FoundationCases]
$flags=[Reflection.BindingFlags]'Static,NonPublic'
function Invoke-CaseHelper([string]$Name,[object[]]$Arguments) {
    $type.GetMethod($Name,$flags).Invoke($null,$Arguments)
}
$actor=[Decennium.Foundation.Laboratory.TestOnlyExpeditionBillProfile]::WorkerId
$meal=[Decennium.Foundation.Laboratory.TestOnlyHavenMealProfile]::OfferVersionId
$lot=[Decennium.Foundation.Laboratory.TestOnlyHavenMealProfile]::MealLotId
$bill=[Decennium.Foundation.Laboratory.TestOnlyExpeditionBillProfile]::BillVersionId
$hostAuthority=Invoke-CaseHelper 'HavenSaleHost' @()
$baseline=Invoke-CaseHelper 'MealAtCounter' @($null,$false)
Invoke-CaseHelper 'SaleCommit' @($baseline,(Invoke-CaseHelper 'PurchaseMeal' @($baseline,$meal,$actor)))
$endpoint=$baseline.Capture().RuleClock.AddSeconds(1800)
$conditions=Invoke-CaseHelper 'BillEndpointConditions' @($endpoint)
$policy=Invoke-CaseHelper 'BillPolicy' @($null,$conditions,$null)
$run=Invoke-CaseHelper 'PortableWorld' @($policy)
foreach($eventName in 'bill-endpoint-stun','bill-ward'){
    Invoke-CaseHelper 'SaleCommit' @($run,(Invoke-CaseHelper 'CCCommand' @($run,$eventName,$actor)))
}
Invoke-CaseHelper 'EarnMealTender' @($run,$false)
Invoke-CaseHelper 'SaleCommit' @($run,(Invoke-CaseHelper 'PurchaseMeal' @($run,$meal,$actor)))
Invoke-CaseHelper 'SaleCommit' @($run,(Invoke-CaseHelper 'BillCommand' @($run,[Decennium.Foundation.CommandKind]::StartExpeditionBill,$bill,$actor)))
Invoke-CaseHelper 'WorldAdvance' @($run,1800,1)
$pending=$run.Capture().ExpeditionBills[0]
if ($pending.Status -ne 'PendingCompletion' -or $pending.UpdatedAt -ne $endpoint) { throw 'The legacy scenario did not reach the exact pending endpoint.' }
Invoke-CaseHelper 'SaleCommit' @($run,(Invoke-CaseHelper 'CCCommand' @($run,'bill-endpoint-cure',$actor)))
Invoke-CaseHelper 'WorldAdvance' @($run,6,1)
Invoke-CaseHelper 'EatMeal' @($run,[Decennium.Foundation.RuleQuantity]::new(2,3),$lot)
$command=Invoke-CaseHelper 'BillCommand' @($run,[Decennium.Foundation.CommandKind]::FinalizeExpeditionBill,$pending.Id,$actor)
$codec=[Decennium.Foundation.SnapshotCodec]::new()
$state=$run.Capture()
$before=$codec.Encode($state)
$query=$run.QueryCommand($hostAuthority,$command)
$afterQuery=$codec.Encode($run.Capture())
$result=$run.Execute($hostAuthority,$command)
$after=$codec.Encode($run.Capture())
function ByteHash([byte[]]$bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
}
$report=[ordered]@{
    status='FAIL'; schema=$state.SchemaVersion; fingerprint=$state.ContentFingerprint; revision=$state.Revision
    clock=$state.RuleClock.ToString(); pendingAt=$endpoint.ToString(); billStatus=$pending.Status.ToString()
    intakeStatus=$state.Intakes[0].Status.ToString(); intakeLot=$state.Intakes[0].LotId
    querySupported=$query.Supported; queryAdmissible=$query.Admissible; queryCode=$query.Code
    executionOutcome=$result.Outcome.ToString(); executionCode=$result.Code
    beforeSha256=(ByteHash $before); afterQuerySha256=(ByteHash $afterQuery); afterExecutionSha256=(ByteHash $after)
    assemblyHashes=@($assemblies | ForEach-Object { @{name=(Split-Path -Leaf $_);sha256=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant()} })
}
if ($state.SchemaVersion -eq 81 -and $state.Intakes[0].Status -eq 'Working' -and $state.Intakes[0].LotId -eq $lot -and $query.Supported -and !$query.Admissible -and $query.Code -eq $ExpectedCode -and $result.Outcome -eq 'Rejected' -and $result.Code -eq $ExpectedCode -and $report.beforeSha256 -eq $report.afterQuerySha256 -and $report.beforeSha256 -eq $report.afterExecutionSha256) {
    $report.status='PASS'
}
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ReportPath -Encoding utf8
if ($report.status -ne 'PASS') { throw "Unexpected busy result: $($query.Code) / $($result.Code)." }
"PASS: schema81 query and execution preserved exact bytes and returned $ExpectedCode."
