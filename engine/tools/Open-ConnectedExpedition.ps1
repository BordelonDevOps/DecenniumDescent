param(
    [string]$AssemblyRoot,
    [string]$InputPath,
    [switch]$FishingTrap
)

$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSEdition -ne 'Core') { throw 'Run with PowerShell 7 (pwsh).' }
if (-not $AssemblyRoot) {
    $buildRoot = Join-Path ([IO.Path]::GetTempPath()) 'Decennium-connected-expedition'
    $build = & (Join-Path $PSScriptRoot 'Compile-Foundation.ps1') -ResultsRoot $buildRoot
    $AssemblyRoot = Split-Path ($build -replace '^PASS: Core, Persistence and LabModel compilation; ', '')
}
foreach ($assembly in 'Core', 'Persistence', 'LabModel') {
    Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$assembly.dll")
}

$session = if ($FishingTrap) {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFishingTrap()
} else {
    [Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Start()
}

function New-SessionCommand($request, $view, $kind) {
    $id = $request.id ?? ('local.' + [guid]::NewGuid().ToString('N'))
    $actor = $request.actor ?? $view.ActingActorId
    $revision = $request.revision ?? $view.Revision
    $target = $request.target ?? ''
    $inventory = $null
    $combat = $null
    $mining = $null
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
        $inventory, $combat, $null, $null, 'None', $null, $null, $null, $null, $mining)
}

function Get-SessionFilePath([string]$path) {
    $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($path)
}

function Invoke-SessionInput($request) {
    switch ($request.op) {
        'view' { return $session.View(($request.seat ?? 'Player')) }
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
        [Console]::WriteLine('Files: {"op":"save","path":"expedition.ddsave"}. Use "load" to restore and "recover" to validate and recover the backup.')
    } elseif (-not [string]::IsNullOrWhiteSpace($line)) {
        Write-SessionResponse $line
    }
}
