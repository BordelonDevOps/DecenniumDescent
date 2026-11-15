param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
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
    @(107,'StartWithFrightened','2026-11-15-tac05-frightened/retained-development/trace-main-20261115T093745297Z/reference/frightened-continued.ddsave'),
    @(108,'StartWithClericSettlement','2026-11-15-chr03-cleric-settlement/implementation/focused/chr03_primary_genuine_earned_settlement/cleric-primary-continued.ddsave'),
    @(108,'StartWithClericSettlement','2026-11-15-chr03-cleric-settlement/implementation/focused/chr03_alternate_genuine_paid_radiance_and_continuation/cleric-alternate-continued.ddsave')
)
$store=[Decennium.Foundation.FileSaveStore]::new(); $checks=[Collections.Generic.List[object]]::new()
$type=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]
function New-OldSession($wire,$factory){
    $initial=[Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample()
    $repertoire=[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample()
    if($wire-eq108){return [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericSettlement($initial,$repertoire,[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())}
    if($wire-eq107){return [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFrightened($initial,$repertoire)}
    if($wire-eq106){return [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericRepertoire($initial,$repertoire)}
    if($wire-eq105){return [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericCompanion($initial)}
    return $type.GetMethod($factory).Invoke($null,@())
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
    $known=if($wire-eq108){6}elseif($wire-ge106){5}else{0}
    Require ($final.WireSchemaVersion-eq$wire-and!$final.ConnectedClericCasting-and($final.ConnectedClericSettlement-eq($wire-eq108))-and
        ($final.ConnectedFrightened-eq($wire-ge107))-and$final.KnownSpells.Count-eq$known-and
        ($final.ConnectedClericRepertoire-eq($wire-ge106))) "Authentic input has wrong schema: $source"
    $folder=(New-Item -ItemType Directory "$Run/case-$($checks.Count)-wire$wire").FullName
    $session=New-OldSession $wire $factory
    $session.Restore($source); $session.Save("$folder/roundtrip.ddsave")
    Require ((Digest "$folder/roundtrip.ddsave") -ceq (Digest $source)) "Authentic wire$wire roundtrip changed."
    $candidates=@(Get-ChildItem (Split-Path $source) -File -Filter '*.ddsave' | ForEach-Object {
        $snapshot=$store.Load($_.FullName)
        if ($snapshot.Revision -lt $final.Revision -and $snapshot.WireSchemaVersion -eq $wire) {
            [pscustomobject]@{Path=$_.FullName;State=$snapshot}
        }
    } | Sort-Object -Property @{Expression={$_.State.Revision};Descending=$true},Path)
    Require ($candidates.Count -gt 0) "No authentic earlier checkpoint for $source"
    $before=$candidates[0];$session=New-OldSession $wire $factory;$session.Restore($before.Path)
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
$new=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericCasting([Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),[Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())
$new.Save("$Run/new-before.ddsave")
foreach ($case in $cases) {
    $rejected=$false; try { $new.Restore((Resolve-Path "$EvidenceRoot/$($case[2])").Path) } catch { $rejected=$true }
    Require $rejected "Wire109 accepted wire$($case[0]) from an incompatible profile."
}
$new.Save("$Run/new-after.ddsave")
Require ((Digest "$Run/new-before.ddsave") -ceq (Digest "$Run/new-after.ddsave")) 'Cross-profile rejection mutated the new session.'
[ordered]@{Status='PASS';Cases=$checks;NewProfileRejections=$cases.Count;UnchangedNewStateSha256=(Digest "$Run/new-after.ddsave")} |
    ConvertTo-Json -Depth 7 | Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: $($checks.Count) authentic wire95-108 roundtrips and exact continued states."
