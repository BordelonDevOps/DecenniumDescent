param([string]$AssemblyRoot,[string]$Launcher,[string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Launcher=(Resolve-Path -LiteralPath $Launcher).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
function Require($condition,$message) { if (!$condition) { throw $message } }
function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
$session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericRepertoire(
    [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
    [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample())
$session.Save("$Run/before.ddsave")
$simulation=$session.GetType().GetField('simulation',[Reflection.BindingFlags]'Instance,NonPublic').GetValue($session)
$grant=[Decennium.Foundation.Authority]::new('TEST_ONLY.host',[string[]]@('TEST_ONLY.companion'))
$controls=[Collections.Generic.List[object]]::new()
foreach ($kind in 'CastKnownSpell','AcquireEarnedSpell') {
    $ids=if ($kind -eq 'CastKnownSpell') { [Decennium.Foundation.SpellSourceCatalog]::Definitions.Id } else { @('detect-magic') }
    foreach ($spell in $ids) {
        $command=[Decennium.Foundation.Command]::new("boundary.$kind.$spell",'TEST_ONLY.companion',0,$kind,$spell)
        $query=$simulation.QueryCommand($grant,$command)
        $result=$simulation.Execute($grant,$command)
        $expected=if ($kind -eq 'CastKnownSpell') {'OrdinarySpellcastingUnsupported'} else {'ClericEarnedAdvancementUnavailable'}
        Require ($query.Supported -and !$query.Admissible -and $query.Code -eq $expected -and $query.Costs.Count -eq 0 -and
            $result.Outcome -eq 'Rejected' -and $result.Code -eq $expected) 'Typed shared-boundary denial did not reach the explicit capability rule.'
        $session.Save("$Run/after-$kind-$spell.ddsave")
        Require ((Digest "$Run/before.ddsave") -ceq (Digest "$Run/after-$kind-$spell.ddsave")) 'Rejected engine request changed complete state.'
        $controls.Add([ordered]@{Kind=$kind;Spell=$spell;Query=$query;Result=$result;UnchangedSha256=(Digest "$Run/before.ddsave")})
    }
}
$source=[Decennium.Foundation.SpellSourceCatalog]::Definitions
$source | ConvertTo-Json -Depth 14 | Set-Content "$Run/runtime-source-bindings.json" -Encoding utf8
# Retain authentic prior public projection equality, including property absence rather than null backfill.
$legacyInitial=(Resolve-Path "$PSScriptRoot/../2026-11-15-chr02-shared-rp/public/Restored/initial.ddsave").Path
@(@{op='load';path=$legacyInitial},@{op='view';seat='Player'}) | ForEach-Object { ConvertTo-Json $_ -Compress } |
    Set-Content "$Run/legacy-view-input.jsonl" -Encoding utf8
& $Launcher -ClericCompanion -AssemblyRoot $AssemblyRoot -InputPath "$Run/legacy-view-input.jsonl" |
    Set-Content "$Run/legacy-view-response.jsonl" -Encoding utf8
$prior=Get-Content "$PSScriptRoot/../2026-11-15-chr02-shared-rp/public/Restored/responses.jsonl" |
    ForEach-Object { ConvertFrom-Json $_ } | Where-Object { $null -ne $_.Actors -and $_.Revision -eq 0 -and $_.Actors.Count -eq 2 } | Select-Object -First 1
$observed=Get-Content "$Run/legacy-view-response.jsonl" | ForEach-Object { ConvertFrom-Json $_ } | Where-Object { $null -ne $_.Actors }
Require ($null -ne $prior -and $null -ne $observed.Actors) 'Legacy projection evidence missing.'
Require (($prior | ConvertTo-Json -Depth 30 -Compress) -ceq ($observed | ConvertTo-Json -Depth 30 -Compress)) 'Wire105 public projection shape or values changed.'
[ordered]@{Status='PASS';BoundaryControls=$controls;RuntimeSourceSha256=(Digest "$Run/runtime-source-bindings.json")
    LegacyProjectionIdentical=$true;LegacyProjectionSha256=(Digest "$Run/legacy-view-response.jsonl")} |
    ConvertTo-Json -Depth 16 -EnumsAsStrings | Set-Content "$Run/results.json" -Encoding utf8
Write-Output 'PASS: exact source registry, shared query/execution denials and unchanged legacy public projection.'
