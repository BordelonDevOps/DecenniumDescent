param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$TraceRoot,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$TraceRoot=(Resolve-Path -LiteralPath $TraceRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach($part in 'Core','Persistence','LabModel'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$store=[Decennium.Foundation.FileSaveStore]::new()
$rows=[Collections.Generic.List[object]]::new()
foreach($campaign in 'sanctuary','purify','detect','guidance','concentration','focus','refrain','sanctuary-forgo'){
    $folder=Join-Path $TraceRoot $campaign
    $manifest=Get-Content -LiteralPath (Join-Path $folder 'manifest.json') -Raw|ConvertFrom-Json
    foreach($mark in $manifest.marks){
        $path=Join-Path (Join-Path $folder 'reference') $mark.name
        if((Digest $path)-cne$mark.sha256){throw 'Canonical witness source changed'}
        $state=$store.Load($path)
        $witness=[ordered]@{
            campaign=$campaign;checkpoint=$mark.name;sha256=$mark.sha256;wire=$state.WireSchemaVersion
            revision=$state.Revision;clock=$state.RuleClock.ToString();randomState=$state.RandomState
            testOnly=$state.TestOnly;productionAuthority=$false;inventoryCombat=$state.InventoryCombat
            activeEncounter=$state.Encounter.Id;closedEncounterCount=$state.ClosedEncounters.Count
            actorLife=@($state.Lives|Select-Object ActorId,MaximumHp,Hp,TemporaryHp,Stable,Dead)
            pools=@($state.ResonancePools|Select-Object ActorId,Current,Maximum)
            strain=@($state.CastingStrain|Select-Object ActorId,Dissonance,LastSpellId,Refrain)
            knownSpells=@($state.KnownSpells|Select-Object ActorId,SpellId,AcquiredRevision)
            earnedObjective=$state.ClericObjective;characterAdvancements=$state.CharacterAdvancements
            casts=@($state.SpellCasts|ForEach-Object{[ordered]@{
                command=$_.CommandId;revision=$_.Revision;actor=$_.ActorId;target=$_.TargetId;spell=$_.SpellId;at=$_.At.ToString()
                classLevel=$_.ClassLevel;rank=$_.Rank;dc=$_.SpellDc;focused=$_.FocusedDcElected;focus=$_.FocusItemId;turn=$_.Turn
                rpBefore=$_.RpBefore;baseRp=$_.BaseRp;surcharge=$_.Surcharge;rpAfter=$_.RpAfter
                strainBefore=$_.DissonanceBefore;strainAfter=$_.DissonanceAfter;refrain=$_.AppliedRefrain
                randomBefore=$_.RandomBefore;randomAfter=$_.RandomAfter;words=$_.WordsConsumed
            }})
            effects=@($state.SpellEffects|ForEach-Object{[ordered]@{
                id=$_.Id;cast=$_.CastId;spell=$_.SpellId;caster=$_.CasterId;target=$_.TargetId;present=$_.Present
                starts=$_.StartedAt.ToString();expires=$_.ExpiresAt.ToString();reason=$_.EndReason.ToString();concentration=$_.RequiresConcentration
            }})
            saves=@($state.SpellSaves|Select-Object Id,Kind,EffectId,SubjectId,Revision,Damage,Dc,Modifier,First,Second,Natural,Success,RandomBefore,RandomAfter,WordsConsumed)
            pendingSanctuary=@($state.SanctuaryAdmissions|Where-Object Pending|Select-Object Id,ActorId,OriginalTargetId)
            guidanceUses=$state.GuidanceUses;detectFocuses=$state.DetectMagicFocuses;contamination=$state.ConsumableContamination
            stocks=@($state.Work.Lots|ForEach-Object{[ordered]@{id=$_.Id;unit=$_.UnitId;amount=$_.Amount.ToString();location=$_.LocationId;custodian=$_.CustodianId}})
            focus=@($state.PortableEquipment|Where-Object Id -EQ 'TEST_ONLY.cleric-casting.holy-symbol'|Select-Object Id,OwnerId,CustodianId,Placement,HeldHands,GroundX,GroundY)
            clubs=$state.Clubs;heldItems=@($state.Lives|Select-Object ActorId,HeldItems)
            clubHandling=@($state.PortableHandling|Where-Object ItemId -eq 'TEST_ONLY.companion-club')
            clubLabor=@($state.Work.WorkerIntervals|Where-Object {$_.JobId -in @($state.PortableHandling|Where-Object ItemId -eq 'TEST_ONLY.companion-club'|ForEach-Object Id)})
            casterBurden=[Decennium.Foundation.Laboratory.PortableEquipmentRules]::CarriedBurden($state,[Decennium.Foundation.ClericRpProfile]::Actor)
            attacks=$state.MeleeAttacks;intervals=$state.WorldIntervals;casterEnds=$state.CastingTurnEnds
            intakes=$state.Intakes;manufacturing=$state.ManufacturingOrders
        }
        $name=$campaign+'-'+[IO.Path]::GetFileNameWithoutExtension($mark.name)+'.json'
        $witness|ConvertTo-Json -Depth 12 -EnumsAsStrings|Set-Content -LiteralPath (Join-Path $Run $name) -Encoding utf8
        $rows.Add(@{campaign=$campaign;checkpoint=$mark.name;revision=$state.Revision;canonicalSha256=$mark.sha256;witness=$name;sha256=(Digest (Join-Path $Run $name))})
    }
}
@{status='PASS';scope='Readable projections of retained genuine checkpoints, not independent gameplay or production authority';checkpoints=@($rows)}|
    ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
Write-Output "PASS: $($rows.Count) readable casting checkpoint witnesses"
