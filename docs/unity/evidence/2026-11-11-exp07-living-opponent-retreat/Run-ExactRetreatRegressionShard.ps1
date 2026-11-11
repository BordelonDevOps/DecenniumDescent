param(
    [Parameter(Mandatory)][string]$Run,
    [Parameter(Mandatory)][string]$AssemblyRoot,
    [Parameter(Mandatory)][string]$Group
)
$ErrorActionPreference = 'Stop'
foreach ($name in 'Core', 'Persistence', 'LabModel', 'HeadlessTests') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll")
}
$names = @([Decennium.Foundation.Tests.FoundationCases]::Names())
$inventory = [string[]](Get-Content -LiteralPath (Join-Path $Run 'all-names.txt'))
if ([string]::Join("`n", $names) -cne [string]::Join("`n", $inventory)) {
    throw 'The exact compiled test inventory differs from the recorded inventory.'
}
$groupNames = [string[]](Get-Content -LiteralPath (Join-Path $Run "$Group-names.txt"))
if ($groupNames.Count -eq 0 -or @($groupNames | Where-Object { $_ -cnotin $names }).Count -ne 0) {
    throw 'The group contains no cases or includes an unknown case.'
}
$journal = Join-Path $Run "$Group.jsonl"
$finished = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
if (Test-Path -LiteralPath $journal) {
    Get-Content -LiteralPath $journal | ForEach-Object {
        $prior = $_ | ConvertFrom-Json
        if ($prior.Name -cnotin $groupNames -or -not $finished.Add($prior.Name)) {
            throw 'The existing journal contains an unexpected or repeated case.'
        }
    }
}
foreach ($name in $groupNames) {
    if ($finished.Contains($name)) { continue }
    $folder = Join-Path (Join-Path $Run 'saves') $name
    $result = [Decennium.Foundation.Tests.FoundationCases]::Run($name, $folder)
    $result | ConvertTo-Json -Compress | Add-Content -LiteralPath $journal -Encoding utf8
}
'DONE' | Set-Content -LiteralPath (Join-Path $Run "$Group.done")
