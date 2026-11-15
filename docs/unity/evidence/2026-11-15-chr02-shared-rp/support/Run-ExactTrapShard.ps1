param(
    [Parameter(Mandatory)][string]$Run,
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Group
)

$ErrorActionPreference = 'Stop'
$launch = Get-Content -LiteralPath "$Run/launch.json" -Raw | ConvertFrom-Json -AsHashtable
$assignment = "$Run/$Group-names.txt"
$journal = "$Run/$Group.jsonl"
if (Test-Path -LiteralPath $journal) { throw 'Start a fresh run for this shard.' }
function Digest([string]$path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
if ((Digest "$Run/all-names.txt") -cne $launch.inventorySha256 -or
    (Digest $assignment) -cne $launch.assignments[$Group]) { throw 'The launch inventory or assignment changed.' }

$loaded = [ordered]@{}
foreach ($name in $launch.assemblies.Keys) {
    $path = (Resolve-Path -LiteralPath (Join-Path $AssemblyRoot $name)).Path
    if ((Digest $path) -cne $launch.assemblies[$name]) { throw "Unexpected launch assembly $name." }
    $assembly = [Reflection.Assembly]::LoadFrom($path)
    if ($assembly.Location -cne $path -or (Digest $assembly.Location) -cne $launch.assemblies[$name]) {
        throw "Unexpected loaded assembly $name."
    }
    $loaded[$name] = [ordered]@{sha256=(Digest $assembly.Location); moduleId=$assembly.ManifestModule.ModuleVersionId.ToString()}
}
$names = @([Decennium.Foundation.Tests.FoundationCases]::Names())
$inventory = @(Get-Content -LiteralPath "$Run/all-names.txt")
$groupNames = @(Get-Content -LiteralPath $assignment)
if ([string]::Join("`n", $names) -cne [string]::Join("`n", $inventory) -or
    $groupNames.Count -eq 0 -or @($groupNames | Where-Object { $_ -cnotin $names }).Count -ne 0) {
    throw 'The loaded test inventory differs from the launch inventory.'
}
$execution = [ordered]@{runId=$launch.runId; group=$Group; pid=$PID; assemblies=$loaded
    inventorySha256=$launch.inventorySha256; assignmentSha256=$launch.assignments[$Group]
    startedUtc=[DateTime]::UtcNow.ToString('o')}
$execution | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath "$Run/$Group.started.json" -Encoding utf8
foreach ($name in $groupNames) {
    $folder = Join-Path (Join-Path $Run 'saves') $name
    [Decennium.Foundation.Tests.FoundationCases]::Run($name, $folder) |
        ConvertTo-Json -Compress | Add-Content -LiteralPath $journal -Encoding utf8
}
foreach ($name in $loaded.Keys) {
    if ((Digest (Join-Path $AssemblyRoot $name)) -cne $loaded[$name].sha256) { throw "Assembly $name changed during execution." }
}
$execution['journalSha256'] = Digest $journal
$execution['cases'] = $groupNames.Count
$execution['completedUtc'] = [DateTime]::UtcNow.ToString('o')
$execution | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath "$Run/$Group.execution.json" -Encoding utf8
'DONE' | Set-Content -LiteralPath "$Run/$Group.done"
