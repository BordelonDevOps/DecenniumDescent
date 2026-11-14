param([string]$AssemblyRoot,[string]$PublicRoot,[string]$Run)
$ErrorActionPreference = 'Stop'
$AssemblyRoot = (Resolve-Path -LiteralPath $AssemblyRoot).Path
$PublicRoot = (Resolve-Path -LiteralPath $PublicRoot).Path
$Run = (New-Item -ItemType Directory -Path $Run).FullName
function Require($condition,$message) { if (!$condition) { throw $message } }
function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
$assemblies = [ordered]@{}
foreach ($name in 'Core','Persistence','LabModel') {
    $file = Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll"
    Add-Type -Path $file
    $assembly = [AppDomain]::CurrentDomain.GetAssemblies() | Where-Object { $_.Location -eq $file }
    Require ($null -ne $assembly) "Loaded assembly identity missing: $file"
    $assemblies[$name] = @{sha256=(Digest $file); moduleId=$assembly.ManifestModule.ModuleVersionId.ToString()}
}
function TypedCommand($session,$request) {
    $seat = $request.seat ?? 'Player'
    $view = $session.View($seat)
    $actor = $request.actor ?? $view.ActingActorId
    $kind = $request.kind
    $target = $request.target ?? ''
    if ($request.op -eq 'clock') { $kind='AdvanceClock'; $actor='TEST_ONLY.actor'; $view=$session.View('Player') }
    if ($request.op -eq 'close') { $kind='EndFixedEncounter'; $actor='TEST_ONLY.actor'; $view=$session.View('Player'); $target=$request.target ?? $view.TurnId }
    $inventory = $null; $combat = $null; $mining = $null
    if ($request.inventory) {
        $i=$request.inventory
        $inventory=[Decennium.Foundation.InventoryRequest]::new(
            [Decennium.Foundation.RuleQuantity]::new($i.numerator,($i.denominator ?? 1)),($i.destination ?? ''),($i.handling ?? 'Pickup'))
    }
    if ($request.combat) {
        $c=$request.combat
        $combat=[Decennium.Foundation.CombatRequest]::new(($c.turn ?? $view.TurnId),($c.weapon ?? ''),($c.stance ?? 0),
            ($c.knockout ?? 'OrdinaryOutcome'),($c.choice ?? $false),($c.press ?? 'ArmOrReplace'))
    }
    if ($request.mining) {
        $m=$request.mining
        $mining=[Decennium.Foundation.MiningSelectionRequest]::new($m.version,[string[]]$m.categories,($m.ability ?? 'Wisdom'),
            ($m.hurried ?? $false),($m.failureVictim ?? ''),($m.criticalRecovery ?? ''),($m.assistant ?? ''))
    }
    Require ($null -ne $request.id) 'Typed command must retain an explicit input identity.'
    [Decennium.Foundation.Command]::new($request.id,$actor,($request.revision ?? $view.Revision),$kind,$target,($request.x ?? 0),($request.y ?? 0),
        $inventory,$combat,$null,$null,'None',$null,$null,$null,$null,$mining)
}
$branches=[ordered]@{}
foreach ($branch in 'completion','whole','interruption') {
    $folder=(New-Item -ItemType Directory "$Run/$branch").FullName
    $source="$PublicRoot/$branch/Restored"
    $inputs=@(Get-Content "$source/inputs.jsonl" | ForEach-Object { ConvertFrom-Json -AsHashtable $_ })
    $expected=@(Get-Content "$source/responses.jsonl" | ForEach-Object { ConvertFrom-Json -AsHashtable $_ })
    Require ($inputs.Count -eq $expected.Count) 'Retained console stream is incomplete.'
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithShortRest()
    $checks=[Collections.Generic.List[object]]::new()
    $marks=[ordered]@{}
    $unavailable=0; $duplicates=0; $conflicts=0; $unauthorized=0; $parsing=0
    for ($index=0; $index -lt $inputs.Count; $index++) {
        $request=$inputs[$index]; $reference=$expected[$index]
        $row=[ordered]@{Input=$index; Op=$request.op; Id=$request.id}
        if ($request.op -eq 'save') {
            $path=Join-Path $folder $request.path
            $session.Save($path)
            $marks[$request.path]=Digest $path
            Require ($marks[$request.path] -ceq (Digest (Join-Path $source $request.path))) "$branch typed checkpoint differs at $index."
            $row.Response='Saved'; $row.Sha256=$marks[$request.path]
        } elseif ($request.op -eq 'load') {
            $session.Restore((Join-Path $folder $request.path))
            $observedPath="$folder/restore-$index.ddsave"
            $session.Save($observedPath)
            Require ((Digest $observedPath) -ceq (Digest (Join-Path $source $request.path))) "$branch typed restore differs at $index."
            $row.Response='Restored'
        } elseif ($request.op -eq 'view') {
            $view=$session.View(($request.seat ?? 'Player'))
            Require ($view.Revision -eq $reference.Revision -and $view.Clock.Numerator -eq $reference.Clock.Numerator -and
                $view.Clock.Denominator -eq $reference.Clock.Denominator) "$branch typed view differs at $index."
            Require (($null -eq $view.ShortRest) -eq ($null -eq $reference.ShortRest)) "$branch typed view disclosure differs."
            $row.Response='ViewMatched'
        } elseif ($request.kind -eq 'BeginShortRest' -and
            (!$request.ContainsKey('x') -or !($request.x -is [int] -or $request.x -is [long]))) {
            Require ($reference.Response -eq 'Unavailable') 'Console-only malformed dice input was accepted.'
            $row.Response='ConsoleParsingOnly'; $parsing++
        } else {
            $beforePath="$folder/before-$index.ddsave"
            $session.Save($beforePath)
            $before=Digest $beforePath
            if ($request.op -eq 'auto') { $response=$session.AdvanceAutomaticDefender() }
            else {
                $command=TypedCommand $session $request
                $response=if ($request.op -in 'clock','close') { $session.SubmitSessionCommand($command) }
                    else { $session.Submit(($request.seat ?? 'Player'),$command) }
            }
            Require ($response.Response.ToString() -ceq $reference.Response) "$branch typed response differs at $index ($($request.id))."
            if ($reference.ContainsKey('Revision')) {
                Require ($response.Revision -eq $reference.Revision -and $response.Clock.Numerator -eq $reference.Clock.Numerator -and
                    $response.Clock.Denominator -eq $reference.Clock.Denominator -and $response.NextSeat.ToString() -ceq $reference.NextSeat -and
                    $response.PendingDecision.ToString() -ceq $reference.PendingDecision) "$branch typed result fields differ at $index."
            }
            $row.Response=$response.Response.ToString(); $row.Revision=$response.Revision
            if ($response.Response -ne 'Committed') {
                $afterPath="$folder/after-$index.ddsave"
                $session.Save($afterPath)
                $after=Digest $afterPath
                Require ($before -ceq $after) "$branch denied/retried typed request mutated complete state at $index."
                $row.UnchangedSha256=$after
                $row.BeforeSnapshot="before-$index.ddsave"; $row.AfterSnapshot="after-$index.ddsave"
                switch ($row.Response) {
                    'Unavailable' { $unavailable++ }
                    'Duplicate' { $duplicates++ }
                    'CommandIdConflict' { $conflicts++ }
                    'NotAuthorized' { $unauthorized++ }
                }
            }
        }
        $checks.Add($row)
    }
    Require ($unavailable -ge 5 -and $duplicates -ge 1 -and $conflicts -ge 1 -and $parsing -eq 2) "$branch did not exercise typed denials/retries and the two distinct parsing checks."
    $checks | ConvertTo-Json -Depth 7 | Set-Content "$folder/requests.json" -Encoding utf8
    $branches[$branch]=[ordered]@{Inputs=$inputs.Count; InputSha256=(Digest "$source/inputs.jsonl"); ReferenceResponsesSha256=(Digest "$source/responses.jsonl")
        DirectCheckpoints=$marks; Unavailable=$unavailable; Duplicates=$duplicates; Conflicts=$conflicts; NotAuthorized=$unauthorized
        ConsoleParsingOnly=$parsing; RequestsSha256=(Digest "$folder/requests.json")}
}
[ordered]@{Status='PASS'; Assemblies=$assemblies; Branches=$branches} | ConvertTo-Json -Depth 12 |
    Set-Content "$Run/results.json" -Encoding utf8
Write-Output "PASS: full typed request parity, denied/retried state equality and parsing distinctions in $Run"
