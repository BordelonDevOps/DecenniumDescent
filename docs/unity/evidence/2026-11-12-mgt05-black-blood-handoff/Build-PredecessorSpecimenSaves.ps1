param([Parameter(Mandatory)][string]$OutputRoot)
$ErrorActionPreference = 'Stop'
$old = Join-Path $PSScriptRoot '../2026-11-12-mgt09-connected-formula-research'
$bindings = Get-Content -LiteralPath (Join-Path $old 'BINDINGS.json') -Raw | ConvertFrom-Json
foreach ($input in $bindings.exactExecutedAssemblies) {
    $path = Join-Path $old "focused/assemblies/$($input.name)"
    if ((Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() -cne $input.sha256) {
        throw "Accepted predecessor assembly changed: $($input.name)"
    }
}
foreach ($name in 'Core','Persistence','LabModel','HeadlessTests') {
    Add-Type -Path (Join-Path $old "focused/assemblies/Decennium.Foundation.$name.dll")
}
$null = New-Item -ItemType Directory -Force -Path $OutputRoot
$t = [Decennium.Foundation.Tests.FoundationCases]
$f = [Reflection.BindingFlags]'NonPublic,Static'
function Call([string]$Name,[object[]]$Arguments) {
    try { $t.GetMethod($Name,$f).Invoke($null,$Arguments) } catch { throw "$Name failed: $($_.Exception.GetBaseException().Message)" }
}
$codec = [Decennium.Foundation.SnapshotCodec]::new()
$worker = [Decennium.Foundation.Laboratory.TestOnlyPolicy]::ActorId
$seed = Call 'HarvestTreatmentSeed' @($true)
$records = [Collections.Generic.List[object]]::new()
function Retain([string]$Name, $Simulation, [uint32]$Seed, [string]$Target) {
    $s = $Simulation.Capture()
    $path = Join-Path $OutputRoot ($Name + '.ddsave')
    [IO.File]::WriteAllBytes($path,$codec.Encode($s))
    $records.Add([ordered]@{name=$Name;wire=$s.WireSchemaVersion;base=$s.SchemaVersion;seed=$Seed;target=$Target
        time=$s.RuleClock.ToString();revision=$s.Revision;sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()})
}
foreach ($mode in 'wire75-mid-treatment','wire76-clean-open') {
    $prep = [object[]]@([uint32]$seed,$false,$null,$null,$null,$false,($mode -eq 'wire76-clean-open'))
    $sim = Call 'PreparedHarvestTreatment' $prep
    $target = [string]$prep[3]
    $start = Call 'StartHarvestTreatment' @($sim,$target)
    $null = Call 'WorldCommit' @($sim,$start)
    if ($mode -eq 'wire75-mid-treatment') {
        $null = Call 'WorldAdvance' @($sim,600,1)
    } else {
        $null = Call 'WorldAdvance' @($sim,1800,1)
        $s = $sim.Capture()
        $open = [Decennium.Foundation.Command]::new('wire76.authentic.open',$worker,$s.Revision,
            [Decennium.Foundation.CommandKind]::OpenPortableContainer,'TEST_ONLY.preservation.sealable-vessel')
        $null = Call 'WorldCommit' @($sim,$open)
        $null = Call 'WorldAdvance' @($sim,30,1)
    }
    Retain $mode $sim $seed $target
}
$policy = Call 'Recipe14ManufacturePolicy' @([uint32]1,$null,$null)
$oldRecipe = Call 'World' @($policy)
$null = Call 'WorldAdvance' @($oldRecipe,11584,1)
Retain 'wire18-recipe14' $oldRecipe 1 'manufacture.recipe14.set0.component2'
[ordered]@{sourceCommit=$bindings.implementationCommit;executedAssemblies=$bindings.exactExecutedAssemblies;saves=@($records.ToArray())}
    | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $OutputRoot 'origin.json') -Encoding utf8
