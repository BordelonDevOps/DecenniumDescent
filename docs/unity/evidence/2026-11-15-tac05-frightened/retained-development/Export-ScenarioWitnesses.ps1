param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$store=[Decennium.Foundation.FileSaveStore]::new();$rows=[Collections.Generic.List[object]]::new()
foreach($trace in 'trace-main-20261115T093745297Z','trace-ability-check','trace-sight-loss'){
    $folder=Join-Path $PSScriptRoot $trace;$manifest=Get-Content -LiteralPath (Join-Path $folder 'manifest.json') -Raw|ConvertFrom-Json
    foreach($mark in $manifest.marks){
        $path=Join-Path (Join-Path $folder 'reference') $mark.name
        $hash=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant();if($hash-cne$mark.sha256){throw 'Changed reference checkpoint'}
        $s=$store.Load($path)
        $actors=@($s.Actors|ForEach-Object{
            $id=$_.Id;$life=@($s.Lives|Where-Object ActorId -eq $id)[0]
            $ledger=[Decennium.Foundation.Laboratory.TestOnlyClubAttackPolicy]::ConditionsFor($s,$id)
            @{id=$id;x=$_.X;y=$_.Y;hp=$life.Hp;dead=$life.Dead;
                fear=@($ledger.Applications|Where-Object {$_.Application.Kind.ToString()-eq'Frightened'}|ForEach-Object{
                    @{id=$_.Id;present=$_.Present($ledger.Now);suppressed=$_.Suppressed;endedAt=$_.EndedAt;relationship=$_.Application.Fear;expires=$_.Application.Expires}
                })}
        })
        $receipts=@($s.Receipts|Select-Object -Last 8|ForEach-Object{
            $c=[Decennium.Foundation.CommandHistory]::Read($_)
            @{revision=$_.Revision;id=$c.Id;kind=$c.Kind.ToString();actor=$c.Actor;target=$c.Target;x=$c.X;y=$c.Y}
        })
        $rows.Add([ordered]@{route=$trace;checkpoint=$mark.name;sha256=$hash;revision=$s.Revision;clock=$s.RuleClock.ToString();rng=$s.RandomState;
            schema=$s.WireSchemaVersion;combat=$s.InventoryCombat;currentActor=$s.Encounter.CurrentActor;closedEncounters=$s.ClosedEncounters;
            actors=$actors;sourceUses=$s.FrightenedUses;saves=$s.FrightenedSaves;timings=$s.FrightenedTimings;recharge=$s.AbilityRecharges;
            intervals=@($s.WorldIntervals|ForEach-Object{@{actor=$_.ActorId;actionSpent=$_.ActionSpent;interactions=$_.Interactions;movementSpent=$_.MovementSpent.ToString()}});
            knownSpells=$s.KnownSpells;resonance=$s.ResonancePools;unspentDoses=@($s.AlchemyDoses|Where-Object {!$_.Spent}).Count;
            recentAttacks=@($s.MeleeAttacks|Select-Object -Last 2);cacheAttempts=$s.SupplyCacheAttempts;recentObservation=@($s.ObservationActions|Select-Object -Last 2);recentCommands=$receipts})
    }
}
[ordered]@{status='PASS';scope='Read-only extraction from hash-bound canonical connected checkpoints, not a new gameplay run';assemblyRoot=$AssemblyRoot;checkpoints=@($rows)}|
    ConvertTo-Json -Depth 16|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output "Extracted $($rows.Count) actual checkpoint witnesses."
