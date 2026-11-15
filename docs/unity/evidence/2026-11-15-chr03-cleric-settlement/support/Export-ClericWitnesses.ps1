param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$PrimaryTrace,[Parameter(Mandatory)][string]$AlternateTrace,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Require($test,$message){if(!$test){throw $message}}
$store=[Decennium.Foundation.FileSaveStore]::new()
$rows=[Collections.Generic.List[object]]::new()
foreach($route in @(@{name='primary';path=$PrimaryTrace},@{name='alternate';path=$AlternateTrace})){
    $manifest=Get-Content -LiteralPath (Join-Path $route.path 'manifest.json') -Raw|ConvertFrom-Json
    foreach($mark in $manifest.marks|Sort-Object revision,name){
        $path=Join-Path (Join-Path $route.path 'reference') $mark.name
        Require ((Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()-ceq$mark.sha256) 'Changed campaign checkpoint'
        $s=$store.Load((Resolve-Path -LiteralPath $path).Path)
        $actors=@($s.Characters|Where-Object{$_.ActorId-in'TEST_ONLY.actor','TEST_ONLY.companion'}|ForEach-Object{
            $character=$_;$life=$s.Lives|Where-Object ActorId -eq $character.ActorId
            @{id=$character.ActorId;levels=$character.Levels;hp=$life.Hp;maximumHp=$life.MaximumHp;dead=$life.Dead;
                hitDice=@($s.CharacterHitDice|Where-Object ActorId -eq $character.ActorId)}
        })
        $epoch=[Decennium.Foundation.WorldTiming]::ForActor($s,[Decennium.Foundation.ClericRpProfile]::Actor)
        $calendar=if($null-eq$epoch){$null}else{@{id=$epoch.Id;processedSlot=$epoch.ProcessedSlot;
            slotAtClock=$epoch.SlotAt($s.RuleClock);order=$epoch.Order;phaseFirstTurn=$s.Reinforcement.Admission.Phase.FirstTurn}}
        $rows.Add([ordered]@{route=$route.name;checkpoint=$mark.name;sha256=$mark.sha256;revision=$s.Revision;
            clock=$s.RuleClock.ToString();rng=$s.RandomState;wire=$s.WireSchemaVersion;actors=$actors;
            declaration=$s.ClericMilestone;objective=$s.ClericObjective;awards=$s.CharacterMilestones;advancements=$s.CharacterAdvancements;
            grants=$s.CharacterFeatureGrants;invocation=$s.ClericInvocationPath;conviction=$s.ConvictionCapacity;
            resonance=$s.ResonancePools;healingRites=$s.HealingRites;radiance=$s.RadianceUses;knownSpells=$s.KnownSpells;
            batch=$s.ConnectedBatch;unspentDoses=@($s.AlchemyDoses|Where-Object{!$_.Spent}).Count;
            closedEncounters=$s.ClosedEncounters;owningCalendar=$calendar;
            intervals=@($s.WorldIntervals|ForEach-Object{@{actor=$_.ActorId;lastStart=$_.LastStart;actionSpent=$_.ActionSpent}})})
    }
}
$primary=@($rows|Where-Object{$_.route-eq'primary'-and$_.checkpoint-eq'cleric-advanced.ddsave'})[0]
$alternate=@($rows|Where-Object{$_.route-eq'alternate'-and$_.checkpoint-eq'cleric-after-radiance.ddsave'})[0]
Require ($primary.resonance[0].Current-eq1-and$primary.resonance[0].Maximum-eq4-and$primary.unspentDoses-eq6) 'Primary resource witness differs'
Require ($alternate.radiance[0].AdditionalGain-eq1-and$alternate.resonance[0].Current-eq1-and$alternate.unspentDoses-eq6) 'Actual positive Radiance witness differs'
@{status='PASS';scope='Read-only extraction from exact connected checkpoint bytes; not a new gameplay run';
    conditionPresentPostAdvancementCure='not demonstrated; explicitly accepted CHR-03 evidence scope';checkpoints=@($rows)}|
    ConvertTo-Json -Depth 18|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output "PASS: $($rows.Count) hash-bound campaign checkpoint witnesses."
