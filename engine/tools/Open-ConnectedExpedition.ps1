param(
    [string]$AssemblyRoot,
    [string]$InputPath,
    [switch]$FishingTrap,
    [switch]$CarriedVial,
    [switch]$StowedVial,
    [switch]$TacticalVial,
    [switch]$CompanionDose,
    [switch]$CompanionStabilization,
    [switch]$WoundTreatment,
    [switch]$ConsumeDecay,
    [switch]$ShortRest,
    [switch]$FleshWarden,
    [switch]$ClericCompanion,
    [switch]$ClericRepertoire,
    [switch]$Frightened,
    [switch]$ClericSettlement,
    [switch]$ClericCasting,
    [switch]$ClericLongRest,
    [switch]$PostRecoveryEncounter
)

$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSEdition -ne 'Core') { throw 'Run with PowerShell 7 (pwsh).' }
if (@($FishingTrap,$CarriedVial,$StowedVial,$TacticalVial,$CompanionDose,$CompanionStabilization,$WoundTreatment,$ConsumeDecay,$ShortRest,$FleshWarden,$ClericCompanion,$ClericRepertoire,$Frightened,$ClericSettlement,$ClericCasting,$ClericLongRest,$PostRecoveryEncounter).Where({$_}).Count -gt 1) { throw 'Select one connected expedition profile.' }
if (-not $AssemblyRoot) {
    $buildRoot = Join-Path ([IO.Path]::GetTempPath()) 'Decennium-connected-expedition'
    $build = & (Join-Path $PSScriptRoot 'Compile-Foundation.ps1') -ResultsRoot $buildRoot
    $AssemblyRoot = Split-Path ($build -replace '^PASS: Core, Persistence and LabModel compilation; ', '')
}
foreach ($assembly in 'Core', 'Persistence', 'LabModel') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$assembly.dll")
}

$session = if ($PostRecoveryEncounter) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithPostRecoveryEncounter(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())
} elseif ($ClericLongRest) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericLongRest(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())
} elseif ($ClericCasting) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericCasting(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())
} elseif ($ClericSettlement) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericSettlement(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample())
} elseif ($Frightened) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFrightened(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample())
} elseif ($ClericRepertoire) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericRepertoire(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),
        [Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample())
} elseif ($ClericCompanion) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithClericCompanion(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample())
} elseif ($FishingTrap) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFishingTrap()
} elseif ($CarriedVial) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithCarriedVial()
} elseif ($FleshWarden) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFleshWarden()
} elseif ($ShortRest) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithShortRest()
} elseif ($ConsumeDecay) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithConsumeDecay()
} elseif ($WoundTreatment) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithWoundTreatment()
} elseif ($CompanionStabilization) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithCompanionStabilization()
} elseif ($CompanionDose) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithCompanionDose()
} elseif ($TacticalVial) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithTacticalVial()
} elseif ($StowedVial) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithStowedVial()
} else {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
}

function New-SessionCommand($request, $view, $kind) {
    if ($kind -eq 'BeginLongRest' -or $kind -eq 'InterruptLongRest') {
        $allowed=@('op','kind','id','actor','revision','target','seat','x','y')
        if (@($request.Keys | Where-Object { $_ -cnotin $allowed }).Count) {
            throw 'Long Rest accepts identities and explicit zero coordinates only.'
        }
    }
    if (($kind -eq 'BeginLongRest' -or $kind -eq 'InterruptLongRest') -and (
        !$request.ContainsKey('x') -or !$request.ContainsKey('y') -or
        !($request.x -is [int] -or $request.x -is [long]) -or $request.x -ne 0 -or
        !($request.y -is [int] -or $request.y -is [long]) -or $request.y -ne 0)) {
        throw 'Long Rest requires explicit x:0 and y:0; duration and recovery are source-bound.'
    }
    if (($kind -eq 'BeginShortRest' -or $kind -eq 'BeginMutationShortRest') -and (!$request.ContainsKey('x') -or
        !($request.x -is [int] -or $request.x -is [long]) -or $request.x -ne 0 -or
        ($request.ContainsKey('y') -and (!($request.y -is [int] -or $request.y -is [long]) -or $request.y -ne 0)))) {
        throw 'Short Rest requires an explicit zero Hit Dice selection.'
    }
    if ($kind -eq 'BeginMutationShortRest' -and !$request.ContainsKey('y')) { throw 'Mutation rest requires explicit x:0 and y:0.' }
    $id = $request.id ?? ('local.' + [guid]::NewGuid().ToString('N'))
    $actor = $request.actor ?? $view.ActingActorId
    $revision = $request.revision ?? $view.Revision
    $target = $request.target ?? ''
    $inventory = $null
    $combat = $null
    $mining = $null
    $intimidation = $null
    $advancement = $null
    $healingRite = $null
    $spellCast = $null
    $guidance = $null
    $sanctuaryResponse = $null
    if ($request.ContainsKey('spellCast')) {
        $details = $request.spellCast
        if ($null -eq $details -or @($details.Keys).Count -ne 4 -or !$details.ContainsKey('spellId') -or
            !$details.ContainsKey('focusItemId') -or !$details.ContainsKey('willingTarget') -or !$details.ContainsKey('electFocusedDc') -or
            $details.spellId -isnot [string] -or $details.focusItemId -isnot [string] -or
            $details.willingTarget -isnot [bool] -or $details.electFocusedDc -isnot [bool]) { throw 'Invalid explicit spell choices.' }
        $spellCast = [Decennium.Foundation.SpellCastRequest]::new($details.spellId,$details.focusItemId,$details.willingTarget,$details.electFocusedDc)
    }
    if ($request.ContainsKey('guidance')) {
        $details = $request.guidance
        if ($null -eq $details -or @($details.Keys).Count -ne 1 -or !$details.ContainsKey('effectId') -or
            $details.effectId -isnot [string]) { throw 'Invalid pre-check Guidance choice.' }
        $guidance = [Decennium.Foundation.GuidanceChoice]::new($details.effectId)
    }
    if ($request.ContainsKey('sanctuaryResponse')) {
        $details = $request.sanctuaryResponse
        if ($null -eq $details -or @($details.Keys).Count -ne 2 -or !$details.ContainsKey('kind') -or !$details.ContainsKey('targetId') -or
            $details.kind -isnot [string] -or $details.kind -cnotin @('Retarget','Forgo') -or $details.targetId -isnot [string]) {
            throw 'Invalid Sanctuary continuation choice.'
        }
        $sanctuaryResponse = [Decennium.Foundation.SanctuaryResponseRequest]::new($details.kind,$details.targetId)
    }
    if ($request.ContainsKey('advancement')) {
        $details = $request.advancement
        if ($null -eq $details -or @($details.Keys).Count -ne 3 -or !$details.ContainsKey('features') -or
            !$details.ContainsKey('invocationPath') -or !$details.ContainsKey('earnedSpell') -or $details.features -is [string] -or
            @($details.features | Where-Object { $_ -isnot [string] }).Count -ne 0 -or
            $details.invocationPath -isnot [string] -or $details.earnedSpell -isnot [string]) { throw 'Invalid earned Cleric choices.' }
        $advancement = [Decennium.Foundation.CharacterAdvancementRequest]::new([string[]]$details.features,
            [string]$details.invocationPath, [string]$details.earnedSpell)
    }
    if ($request.ContainsKey('healingRite')) {
        $details = $request.healingRite
        if ($null -eq $details -or @($details.Keys).Count -ne 1 -or !$details.ContainsKey('curePreference') -or
            $details.curePreference -isnot [string] -or $details.curePreference -cnotin @('None','Frightened','Poisoned')) {
            throw 'Invalid conditional Radiance cure preference.'
        }
        $healingRite = [Decennium.Foundation.HealingRiteRequest]::new($details.curePreference)
    }
    if ($request.ContainsKey('intimidatingPresence')) {
        $details = $request.intimidatingPresence
        if ($null -eq $details -or !$details.ContainsKey('targets') -or @($details.Keys).Count -ne 1 -or
            $details.targets -is [string] -or @($details.targets | Where-Object { $_ -isnot [string] }).Count -ne 0) {
            throw 'Intimidating Presence requires only a target identity array.'
        }
        $intimidation = [Decennium.Foundation.IntimidatingPresenceRequest]::new([string[]]$details.targets)
    }
    if ($null -ne $request.inventory) {
        $details = $request.inventory
        $amount = [Decennium.Foundation.RuleQuantity]::new($details.numerator, ($details.denominator ?? 1))
        $inventory = [Decennium.Foundation.InventoryRequest]::new($amount, ($details.destination ?? ''),
            ($details.handling ?? 'Pickup'))
    }
    if ($null -ne $request.combat) {
        $details = $request.combat
        $combat = [Decennium.Foundation.CombatRequest]::new(($details.turn ?? $view.TurnId),
            ($details.weapon ?? ''), ($details.stance ?? 0), ($details.knockout ?? 'OrdinaryOutcome'),
            ($details.choice ?? $false), ($details.press ?? 'ArmOrReplace'))
    }
    if ($null -ne $request.mining) {
        $details = $request.mining
        $mining = [Decennium.Foundation.MiningSelectionRequest]::new($details.version, [string[]]$details.categories,
            ($details.ability ?? 'Wisdom'), ($details.hurried ?? $false), ($details.failureVictim ?? ''),
            ($details.criticalRecovery ?? ''), ($details.assistant ?? ''))
    }
    [Decennium.Foundation.Command]::new($id, $actor, $revision, $kind, $target, ($request.x ?? 0), ($request.y ?? 0),
        $inventory, $combat, $advancement, $null, 'None', $null, $null, $null, $null, $mining, $null, $null, $intimidation, $healingRite,
        $spellCast,$guidance,$sanctuaryResponse)
}

function Get-SessionFilePath([string]$path) {
    $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($path)
}

function Invoke-SessionInput($request) {
    switch ($request.op) {
        'view' { return $session.View(($request.seat ?? 'Player')) }
        'query' {
            $seat = $request.seat ?? 'Player'
            $command = New-SessionCommand $request ($session.View($seat)) $request.kind
            return $session.QueryCastingCommand($seat,$command)
        }
        'discover' { return $session.DiscoverCastingCommands(($request.seat ?? 'Player'),$request.actor) }
        'submit' {
            $seat = $request.seat ?? 'Player'
            $command = New-SessionCommand $request ($session.View($seat)) $request.kind
            return $session.Submit($seat, $command)
        }
        'clock' {
            $request.actor = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
            $command = New-SessionCommand $request ($session.View('Player')) 'AdvanceClock'
            return $session.SubmitSessionCommand($command)
        }
        'close' {
            $request.actor = [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
            $view = $session.View('Player')
            $request.target = $request.target ?? $view.TurnId
            $command = New-SessionCommand $request $view 'EndFixedEncounter'
            return $session.SubmitSessionCommand($command)
        }
        'auto' { return $session.AdvanceAutomaticDefender() }
        'defender-presence' {
            if (!$Frightened -and !$ClericSettlement -and !$ClericCasting -and !$ClericLongRest -and !$PostRecoveryEncounter) { return @{ Response = 'Unavailable' } }
            $command = New-SessionCommand $request ($session.View('Player')) 'UseIntimidatingPresence'
            return $session.SubmitDefenderIntimidatingPresence(
                [Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(), $command)
        }
        'defender-sanctuary' {
            if (!$ClericCasting -and !$ClericLongRest -and !$PostRecoveryEncounter) { return @{ Response = 'Unavailable' } }
            $command = New-SessionCommand $request ($session.View('Player')) 'RespondSanctuary'
            return $session.SubmitDefenderSanctuary(
                [Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),$command)
        }
        'save' { $session.Save((Get-SessionFilePath $request.path)); return @{ Response = 'Saved' } }
        'load' { $session.Restore((Get-SessionFilePath $request.path)); return @{ Response = 'Restored' } }
        'recover' { return @{ Response = 'Recovered'; DisplacedPrimary = $session.RecoverBackup((Get-SessionFilePath $request.path)) } }
        default { return @{ Response = 'Unavailable' } }
    }
}

function Write-SessionResponse([string]$line) {
    try {
        $request = ConvertFrom-Json -AsHashtable -InputObject $line
        $response = Invoke-SessionInput $request
        if ($response -is [Decennium.Foundation.Laboratory.ExpeditionSeatView]) {
            $targets = [ordered]@{}
            foreach ($target in $response.KnownTargets.GetEnumerator()) { $targets[$target.Key.ToString()] = $target.Value }
            $response = $response | Select-Object -Property * -ExcludeProperty KnownTargets
            $response | Add-Member -NotePropertyName KnownTargets -NotePropertyValue $targets
            if (!$ClericCompanion -and !$ClericRepertoire -and !$Frightened -and !$ClericSettlement -and !$ClericCasting -and !$ClericLongRest -and !$PostRecoveryEncounter) { $response.Actors = @($response.Actors | Select-Object -Property * -ExcludeProperty Cleric) }
            if (!$ClericRepertoire -and !$Frightened -and !$ClericSettlement -and !$ClericCasting -and !$ClericLongRest -and !$PostRecoveryEncounter) { $response.Actors = @($response.Actors | Select-Object -Property * -ExcludeProperty Repertoire) }
            if (!$ClericSettlement -and !$ClericCasting -and !$ClericLongRest -and !$PostRecoveryEncounter) { $response.Actors = @($response.Actors | Select-Object -Property * -ExcludeProperty ClericSettlement) }
            if (!$ClericCasting -and !$ClericLongRest -and !$PostRecoveryEncounter) { $response.Actors = @($response.Actors | Select-Object -Property * -ExcludeProperty Casting) }
            if (!$ClericLongRest -and !$PostRecoveryEncounter) { $response = $response | Select-Object -Property * -ExcludeProperty LongRest }
            if (!$FleshWarden) { $response = $response | Select-Object -Property * -ExcludeProperty FleshWarden }
            if (!$ShortRest -and !$FleshWarden) { $response = $response | Select-Object -Property * -ExcludeProperty ShortRest }
            if (!$ConsumeDecay -and !$ShortRest -and !$FleshWarden -and !$ClericLongRest -and !$PostRecoveryEncounter) {
                $response.Actors = @($response.Actors | Select-Object -Property * -ExcludeProperty TemporaryHp,TemporaryHpUntil)
            }
        }
        ConvertTo-Json -InputObject $response -Depth 8 -Compress -EnumsAsStrings
    } catch {
        # The resolver and save validator may know private state. The console only emits the bounded result.
        '{"Response":"Unavailable"}'
    }
}

if ($InputPath) {
    foreach ($line in [IO.File]::ReadLines((Resolve-Path -LiteralPath $InputPath).Path)) {
        if (-not [string]::IsNullOrWhiteSpace($line)) { Write-SessionResponse $line }
    }
    return
}

[Console]::WriteLine('Decennium Descent TEST_ONLY connected expedition. One JSON input per line. Type help or quit.')
while ($null -ne ($line = [Console]::ReadLine()) -and $line -ne 'quit') {
    if ($line -eq 'help') {
        [Console]::WriteLine('View: {"op":"view","seat":"Player"} or use "FirstOpponent".')
        [Console]::WriteLine('Walk: {"op":"submit","actor":"TEST_ONLY.actor","kind":"BeginWorldStep","target":"walk","x":1,"y":0}')
        [Console]::WriteLine('Advance 2 seconds: {"op":"clock","x":2,"y":1}. Use "auto" for one automatic defender action and "close" for a legal encounter exit.')
        [Console]::WriteLine('Use the in-reach Cache view for its target. Interact x=2 starts a pick, x=3 opens, x=4 interrupts. HandleInventory picks up visible stock.')
        [Console]::WriteLine('Use Observation for the hero Hide start and companion Search start. Search takes candidate x/y. To cancel, target the actor''s pending attempt with CancelExplorationHide or CancelExplorationSearch.')
        if ($FishingTrap) {
            [Console]::WriteLine('Use FishingTrap for the companion''s site and receiver. Interact x=1 sets it. Interact x=6 retrieves it with inventory numerator=0, handling=Retrieve and the displayed receiver as destination.')
        }
        if ($CarriedVial) {
            [Console]::WriteLine('Use the Player item view for the produced vial. Pick it up with HandlePortableEquipment when in reach, then use UseAlchemyDose on the hero''s regular turn.')
        }
        if ($CompanionStabilization) {
            [Console]::WriteLine('Use StabilizeCompanion on the dying companion during the hero''s regular turn, with a free hand and within 5 feet.')
        }
        if ($ConsumeDecay -or $ShortRest -or $FleshWarden) {
            [Console]::WriteLine('Use ConsumeDecay on the hero''s regular turn within reach of its known decay bed.')
        }
        if ($ShortRest -or $FleshWarden) {
            [Console]::WriteLine('At the ShortRest berth, submit BeginShortRest with its SiteId and explicit x:0. Advance the shared clock for one uninterrupted hour. InterruptShortRest targets its ActiveIntervalId; a restart requires the full hour.')
        }
        if ($FleshWarden) {
            [Console]::WriteLine('Choose a card from FleshWarden.EligibleMutations as BeginMutationShortRest target with explicit x:0,y:0. Equipment changes only at completed rest. Two beneficial completions are admitted.')
        }
        if ($CompanionDose -or $CompanionStabilization) {
            [Console]::WriteLine('Use BeginReinforcementApproach with the companion and its known target. After admission, the hero can use the held vial on the eligible companion within 5 feet.')
        }
        if ($TacticalVial -or $CompanionDose -or $CompanionStabilization) {
            [Console]::WriteLine('During the hero''s later encounter turn, open the packed vial''s Explorer pack if closed, retrieve the vial, and use it when the hero has an Action.')
        }
        if ($StowedVial) {
            [Console]::WriteLine('Use HandlePortableEquipment to stow the held vial in the open Explorer pack and retrieve it before tactical use.')
        }
        [Console]::WriteLine('Files: {"op":"save","path":"expedition.ddsave"}. Use "load" to restore and "recover" to validate and recover the backup.')
        if ($PostRecoveryEncounter) {
            [Console]::WriteLine('The new defender exists from the start. RecoveryOpponent is its separate seat for view, query, discover and submit. After recovery, stage the companion at (3,4) and approach with the hero from (3,2) to (3,3) at the exact original later-defender Start. Mistimed contact spends travel and requires a fresh approach.')
        }
        if ($ClericLongRest -or $PostRecoveryEncounter) {
            [Console]::WriteLine('After earned Cleric level 2 and encounter closure, arrive at LongRest.SiteX,SiteY. BeginLongRest targets LongRest.SiteId with explicit x:0,y:0. Advance the shared clock for eight uninterrupted hours.')
            [Console]::WriteLine('InterruptLongRest targets LongRest.ActiveIntervalId with explicit x:0,y:0. Restarting requires the full eight hours. Daily provisioning and Rest Debt still apply to both companions.')
            [Console]::WriteLine('LongRest shows attempts and settled recovery. Conviction stays unavailable until the first eligible completion. Use query and discover for current legality.')
        }
        if ($ClericCasting -or $ClericLongRest -or $PostRecoveryEncounter) {
            [Console]::WriteLine('Use query or discover for current target legality. CastKnownSpell takes spellCast:{spellId,focusItemId,willingTarget,electFocusedDc}; all four fields are explicit.')
            [Console]::WriteLine('Before an eligible Hide, Search or Medicine check choose guidance:{effectId}. Casting.Auras exposes opaque IDs for a later FocusDetectedAura Action.')
            [Console]::WriteLine('RespondSanctuary takes sanctuaryResponse:{kind:"Retarget" or "Forgo",targetId}. Use auto for the defender controller, or the trusted defender-sanctuary path for an explicit response.')
        }
    } elseif (-not [string]::IsNullOrWhiteSpace($line)) {
        Write-SessionResponse $line
    }
}
