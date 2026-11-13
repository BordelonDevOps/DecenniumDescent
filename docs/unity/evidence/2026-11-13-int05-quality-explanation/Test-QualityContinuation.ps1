param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$Run=(New-Item -ItemType Directory -Path $Run).FullName
$AssemblyRoot=(Resolve-Path $AssemblyRoot).Path
$reference=(Resolve-Path "$PSScriptRoot/../2026-11-13-int04-recipe4-parity/execution").Path
foreach($name in 'Core','Persistence','LabModel') {
    $file=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    $a=[Reflection.Assembly]::LoadFrom($file)
    if ($a.Location -cne $file) { throw "Unexpected assembly location for $name" }
}
function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
function Require($value,$message) { if (!$value) { throw $message } }
function Result-Json($value) { ConvertTo-Json -InputObject $value -Depth 8 -EnumsAsStrings -Compress }
$s=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
$fixture=Join-Path $reference 'Restored/r106.ddsave'
$s.Restore($fixture)
$v=$s.View('Player')
$beforeView=Result-Json ($v | Select-Object * -ExcludeProperty KnownTargets)
$viewTargets=@($v.KnownTargets.GetEnumerator() | Sort-Object Key | ForEach-Object { "$($_.Key)=$($_.Value)" })
$times=[Collections.Generic.List[double]]::new()
for($i=0;$i -lt 21;$i++) {
    $clock=[Diagnostics.Stopwatch]::StartNew()
    $e=$s.ExplainManufacturingQuality('Player',$v.Revision,$v.DecisionId)
    $clock.Stop()
    $times.Add($clock.Elapsed.TotalMilliseconds)
    Require ($e.Alternatives.Count -eq 2) 'Expected both admissible choices.'
    if($i -eq 0) { $json=Result-Json $e }
    Require ((Result-Json $e) -ceq $json) 'Repeated explanation changed.'
}
$permitted=$s.View('Player')
Require ((Result-Json ($permitted | Select-Object * -ExcludeProperty KnownTargets)) -ceq $beforeView -and
    (@($permitted.KnownTargets.GetEnumerator() | Sort-Object Key | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join '|') -ceq ($viewTargets -join '|')) 'Permitted view changed.'
$s.Save("$Run/pending-after-queries.ddsave")
Require ((Digest "$Run/pending-after-queries.ddsave") -ceq (Digest $fixture)) 'Explaining changed authentic pending bytes.'
$json | Set-Content "$Run/explanation.json" -Encoding utf8
$expectedTop=@('Alternatives','DecisionId','HealingEffect','Quality','RecipeId','RecipeSourceBlobId','RecipeSourcePointer',
    'RecipeSourceRevision','ReviewedPublicRecipeReference','Revision','TestOnly','WorkerId')
$expectedAlternative=@('Choice','DoseCount','SupplementaryVialsConsumed','SupplementaryVialsReleased','VialMaximumStructuralHp','VialStructuralHp')
Require ((@($e.GetType().GetProperties().Name | Sort-Object) -join '|') -ceq (($expectedTop | Sort-Object) -join '|') -and
    (@($e.Alternatives[0].GetType().GetProperties().Name | Sort-Object) -join '|') -ceq (($expectedAlternative | Sort-Object) -join '|')) 'Unexpected public shape.'
$store=[Decennium.Foundation.FileSaveStore]::new()
$expected=$store.Load((Join-Path $reference 'Restored/r165.ddsave'))
$checkpoints=[ordered]@{}
foreach($receipt in $expected.Receipts | Where-Object Revision -GT 106) {
    $command=[Decennium.Foundation.CommandHistory]::Read($receipt)
    $result=if($receipt.Principal -eq 'TEST_ONLY.tac10-later-defender.v1') { $s.AdvanceAutomaticDefender() }
        elseif($command.Kind -in 'AdvanceClock','EndFixedEncounter') { $s.SubmitSessionCommand($command) }
        else { $s.Submit('Player',$command) }
    Require ($result.Response -eq 'Committed' -and $result.Revision -eq $receipt.Revision) "Continuation failed at $($receipt.Revision)."
    if($receipt.Revision -in 107,115,165) {
        $file=Join-Path $Run "r$($receipt.Revision).ddsave"
        $s.Save($file)
        $sha=Digest $file
        Require ($sha -ceq (Digest (Join-Path $reference "Restored/r$($receipt.Revision).ddsave"))) "Canonical change at $($receipt.Revision)."
        $checkpoints[$receipt.Revision.ToString()]=$sha
    }
}
$atDose=$store.Load("$Run/r115.ddsave")
$dose=$atDose.AlchemyDoses | Where-Object Spent
Require (@($dose).Count -eq 1 -and $dose.FirstD4 -eq 4 -and $dose.SecondD4 -eq 1 -and $dose.PotentialHealing -eq 7 -and
    $dose.ActualHealing -eq 3 -and ($atDose.WorldIntervals | Where-Object ActorId -eq $dose.UserId).ActionSpent) 'Native dose behavior changed.'
$warm=@($times | Select-Object -Skip 1 | Sort-Object)
[ordered]@{Status='PASS'; Profile=$expected.ContentFingerprint; Wire=$expected.WireSchemaVersion; Revision=$v.Revision
    PendingHash=(Digest $fixture); Checkpoints=$checkpoints; PermittedViewUnchanged=$true; PublicShape=$expectedTop
    AlternativeShape=$expectedAlternative; Dose=$dose; FirstQueryMs=$times[0]; WarmCount=$warm.Count
    WarmP95Ms=$warm[[int][Math]::Ceiling(0.95*$warm.Count)-1]; RawQueryMs=$times} |
    ConvertTo-Json -Depth 8 -EnumsAsStrings | Set-Content "$Run/results.json" -Encoding utf8
Get-Content "$Run/results.json" -TotalCount 13
