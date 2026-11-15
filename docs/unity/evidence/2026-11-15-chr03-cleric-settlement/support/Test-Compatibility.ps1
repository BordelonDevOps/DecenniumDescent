param([string]$AssemblyRoot,[string]$Run,[string]$ResumeVerified)
$ErrorActionPreference='Stop'
$EvidenceRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../..')).Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach ($name in 'Core','Persistence','LabModel') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
function Require($condition,$message) { if (!$condition) { throw $message } }
function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
$cases=@(
    @(95,'Start','2026-11-13-int03-strict-restoration/connected/Default/travel-continued.ddsave'),
    @(95,'StartWithFishingTrap','2026-11-13-int03-strict-restoration/connected/FishingTrap/trap-continued.ddsave'),
    @(96,'StartWithCarriedVial','2026-11-13-mgt01-finished-vial/public/Restored/vial-continued.ddsave'),
    @(97,'StartWithStowedVial','2026-11-13-mgt01-vial-stow/public/Restored/stow-continued.ddsave'),
    @(98,'StartWithTacticalVial','2026-11-13-mgt01-tactical-vial/public/closed/Restored/continued.ddsave'),
    @(98,'StartWithTacticalVial','2026-11-13-mgt01-tactical-vial/public/open/Restored/continued.ddsave'),
    @(99,'StartWithCompanionDose','2026-11-13-tac06-companion-dose/public/walkthrough/Restored/continued.ddsave'),
    @(100,'StartWithCompanionStabilization','2026-11-13-tac06-companion-stabilization/public/success/Restored/continued.ddsave'),
    @(100,'StartWithCompanionStabilization','2026-11-13-tac06-companion-stabilization/public/failure/Restored/continued.ddsave'),
    @(101,'StartWithWoundTreatment','2026-11-13-tac06-wound-treatment/public/success/Restored/continued.ddsave'),
    @(102,'StartWithConsumeDecay','2026-11-14-tac06-temporary-hp/public/early/Restored/continued.ddsave'),
    @(102,'StartWithConsumeDecay','2026-11-14-tac06-temporary-hp/public/late/Restored/continued.ddsave'),
    @(103,'StartWithShortRest','2026-11-14-mgt03-short-rest/public/completion/Restored/rest-continued.ddsave'),
    @(103,'StartWithShortRest','2026-11-14-mgt03-short-rest/public/interruption/Restored/rest-continued.ddsave'),
    @(103,'StartWithShortRest','2026-11-14-mgt03-short-rest/public/whole/Restored/rest-continued.ddsave'),
    @(104,'StartWithFleshWarden','2026-11-14-tac06-maximum-hp/public/split/Restored/rest-continued.ddsave'),
    @(104,'StartWithFleshWarden','2026-11-14-tac06-maximum-hp/public/whole/Restored/rest-continued.ddsave'),
    @(105,'StartWithClericCompanion','2026-11-15-chr02-shared-rp/public/Restored/continued.ddsave'),
    @(106,'StartWithClericRepertoire','2026-11-15-tac07-cleric-repertoire/public/Restored/continued.ddsave'),
    @(107,'StartWithFrightened','2026-11-15-tac05-frightened/retained-development/trace-main-20261115T093745297Z/reference/frightened-active.ddsave'),
    @(107,'StartWithFrightened','2026-11-15-tac05-frightened/retained-development/trace-main-20261115T093745297Z/reference/frightened-continued.ddsave')
)
$store=[Decennium.Foundation.FileSaveStore]::new(); $checks=[Collections.Generic.List[object]]::new()
$type=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]
if($ResumeVerified){
    $ResumeVerified=(Resolve-Path -LiteralPath $ResumeVerified).Path
    $prior=@(Get-Content -LiteralPath (Join-Path $ResumeVerified 'progress.json') -Raw|ConvertFrom-Json)
    Require ($prior.Count-eq19) 'Only the completed original wire95-106 cases may be resumed.'
    for($index=0;$index-lt$prior.Count;$index++){
        $row=$prior[$index];$case=$cases[$index];$name="case-$index-wire$($row.Wire)"
        Require ($row.Wire-eq$case[0]-and$row.Source-ceq$case[2]-and$row.Commands-gt0-and
            (Digest (Join-Path $EvidenceRoot $row.Source))-ceq$row.SourceSha256-and
            (Digest (Join-Path $EvidenceRoot $row.Earlier))-ceq$row.EarlierSha256-and
            (Digest (Join-Path $ResumeVerified "$name/roundtrip.ddsave"))-ceq$row.SourceSha256-and
            (Digest (Join-Path $ResumeVerified "$name/continued.ddsave"))-ceq$row.SourceSha256) 'Original completed compatibility evidence changed.'
        Copy-Item -LiteralPath (Join-Path $ResumeVerified $name) -Destination (Join-Path $Run $name) -Recurse
        $checks.Add($row)
    }
    @{originalRun=$ResumeVerified;originalProgressSha256=(Digest (Join-Path $ResumeVerified 'progress.json'));
        retainedCompletedCases=19;reason='The original harness substituted an automatic stance for an explicit wire107 Presence receipt; only the two affected wire107 continuations are rerun.'}|
        ConvertTo-Json|Set-Content -LiteralPath (Join-Path $Run 'resume-provenance.json') -Encoding utf8
}
foreach ($case in @($cases|Select-Object -Skip $checks.Count)) {
    $wire=$case[0]; $factory=$case[1]; $source=(Resolve-Path "$EvidenceRoot/$($case[2])").Path
    $final=$store.Load($source)
    $presentFear=0
    if($wire -eq 107){
        foreach($actor in $final.Actors){
            $ledger=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($final,$actor.Id)
            $presentFear+=@($ledger.Applications|Where-Object{$_.Application.Kind.ToString()-eq'Frightened'-and$_.Present($ledger.Now)}).Count
        }
        Require (($source.EndsWith('frightened-active.ddsave')-and$presentFear-gt0)-or
            ($source.EndsWith('frightened-continued.ddsave')-and$presentFear-eq0)) 'Wire107 fear-state witness differs.'
    }
    Require ($final.WireSchemaVersion -eq $wire -and !$final.ConnectedClericSettlement -and ($final.ConnectedFrightened -eq ($wire -eq 107)) -and (($wire -lt 106 -and $final.KnownSpells.Count -eq 0 -and !$final.ConnectedClericRepertoire) -or ($wire -ge 106 -and $final.KnownSpells.Count -eq 5 -and $final.ConnectedClericRepertoire))) "Authentic input has wrong schema: $source"
    $folder=(New-Item -ItemType Directory "$Run/case-$($checks.Count)-wire$wire").FullName
    $session=if ($wire -eq 107) { [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFrightened([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample()) } elseif ($wire -eq 106) { [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericRepertoire([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample()) } elseif ($wire -eq 105) { [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericCompanion([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample()) } else { $type.GetMethod($factory).Invoke($null,@()) }
    $session.Restore($source); $session.Save("$folder/roundtrip.ddsave")
    Require ((Digest "$folder/roundtrip.ddsave") -ceq (Digest $source)) "Authentic wire$wire roundtrip changed."
    $candidates=@(Get-ChildItem (Split-Path $source) -File -Filter '*.ddsave' | ForEach-Object {
        $snapshot=$store.Load($_.FullName)
        if ($snapshot.Revision -lt $final.Revision -and $snapshot.WireSchemaVersion -eq $wire) {
            [pscustomobject]@{Path=$_.FullName;State=$snapshot}
        }
    } | Sort-Object -Property @{Expression={$_.State.Revision};Descending=$true},Path)
    Require ($candidates.Count -gt 0) "No authentic earlier checkpoint for $source"
    $before=$candidates[0]; $session=if ($wire -eq 107) { [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFrightened([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample()) } elseif ($wire -eq 106) { [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericRepertoire([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample()) } elseif ($wire -eq 105) { [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericCompanion([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample()) } else { $type.GetMethod($factory).Invoke($null,@()) }; $session.Restore($before.Path)
    $count=0
    foreach ($receipt in $final.Receipts | Where-Object { $_.Revision -gt $before.State.Revision }) {
        $command=[Decennium.Foundation.CommandHistory]::Read($receipt)
        if ($receipt.Principal -eq 'TEST_ONLY.tac10-later-defender.v1' -and $command.Id.StartsWith('tac10.')) { $response=$session.AdvanceAutomaticDefender() }
        elseif ($command.Kind -eq 'UseIntimidatingPresence') { $response=$session.SubmitDefenderIntimidatingPresence([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),$command) }
        elseif ($command.Kind -in 'AdvanceClock','EndFixedEncounter') { $response=$session.SubmitSessionCommand($command) }
        else { $seat=if ($command.Actor -eq 'TEST_ONLY.third-combatant') {'FirstOpponent'} else {'Player'}; $response=$session.Submit($seat,$command) }
        Require ($response.Response -eq 'Committed' -and $response.Revision -eq $receipt.Revision) "Authentic wire$wire continuation failed at $($receipt.Revision)."
        $count++
    }
    $session.Save("$folder/continued.ddsave")
    Require ($count -gt 0 -and (Digest "$folder/continued.ddsave") -ceq (Digest $source)) "Authentic wire$wire continuation bytes changed."
    $checks.Add([ordered]@{Wire=$wire;Factory=$factory;Source=$case[2];SourceSha256=(Digest $source);PresentFear=$presentFear
        Earlier=[IO.Path]::GetRelativePath($EvidenceRoot,$before.Path);EarlierSha256=(Digest $before.Path)
        FromRevision=$before.State.Revision;ToRevision=$final.Revision;Commands=$count;RoundtripSha256=(Digest "$folder/roundtrip.ddsave")
        ContinuedSha256=(Digest "$folder/continued.ddsave")})
    $checks | ConvertTo-Json -Depth 5 | Set-Content "$Run/progress.json" -Encoding utf8
}
$new=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericSettlement([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())
$new.Save("$Run/new-before.ddsave")
foreach ($case in $cases) {
    $rejected=$false; try { $new.Restore((Resolve-Path "$EvidenceRoot/$($case[2])").Path) } catch { $rejected=$true }
    Require $rejected "Wire108 accepted wire$($case[0]) from an incompatible profile."
}
$new.Save("$Run/new-after.ddsave")
Require ((Digest "$Run/new-before.ddsave") -ceq (Digest "$Run/new-after.ddsave")) 'Cross-profile rejection mutated the new session.'
[ordered]@{Status='PASS';Cases=$checks;NewProfileRejections=$cases.Count;UnchangedNewStateSha256=(Digest "$Run/new-after.ddsave")} |
    ConvertTo-Json -Depth 7 | Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: $($checks.Count) authentic wire95-107 roundtrips and exact continued states."
