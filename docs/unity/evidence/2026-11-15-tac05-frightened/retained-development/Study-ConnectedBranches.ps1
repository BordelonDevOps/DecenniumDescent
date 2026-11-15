param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$CheckRepeatSave,[Parameter(Mandatory)][string]$RechargedSave)
$ErrorActionPreference='Stop'
foreach($part in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$run=New-Item -ItemType Directory -Path (Join-Path $PSScriptRoot ('branch-study-'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')))
$flags=[Reflection.BindingFlags]'Static,NonPublic'
$caseType=[Decennium.Foundation.Tests.FoundationCases]
$hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
$ally=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Companion
$npc=[Decennium.Foundation.FrightenedProfile]::Actor
function Call([string]$Name,[object[]]$Arguments){
    try{$caseType.GetMethod($Name,$flags).Invoke($null,$Arguments)}catch{throw $_.Exception.InnerException}
}
function Capture($Session){Call 'ShortRestCapture' @($Session)}
function Command($Session,$Actor,$Kind,$Target='',[int]$X=0,[int]$Y=0,$Combat=$null){
    Call 'ClericCommit' @($Session,$Actor,[Decennium.Foundation.CommandKind]$Kind,$Target,$X,$Y,$Combat)
}
function Report($Session,[string]$Name){
    $s=Capture $Session
    $Session.Save((Join-Path $run.FullName ($Name+'.ddsave')))
    [pscustomobject]@{name=$Name;revision=$s.Revision;clock=$s.RuleClock.ToString();rng=$s.RandomState;
        current=$s.Encounter.CurrentActor;combat=$s.InventoryCombat;
        hp=@($s.Lives|Select-Object ActorId,Hp,Dead);
        fear=@($s.FrightenedSaves|Select-Object TargetId,Repeat,Natural,Success,ApplicationId);
        attacks=@($s.MeleeAttacks|Select-Object -Last 2)} | ConvertTo-Json -Depth 5 -Compress
}
$session=Call 'NewFrightenedExpedition' @()
$session.Restore((Resolve-Path -LiteralPath $CheckRepeatSave).Path)
Call 'ClericDefender' @($session)
Call 'ClericGuard' @($session,$ally)
Call 'ClericEnd' @($session,$ally)
Call 'ClericGuard' @($session,$hero)
Report $session 'before-final-end'
Call 'ClericEnd' @($session,$hero)
Report $session 'after-final-end'
$session=Call 'NewFrightenedExpedition' @()
$session.Restore((Resolve-Path -LiteralPath $RechargedSave).Path)
Call 'ClericGuard' @($session,$ally)
Call 'ClericEnd' @($session,$ally)
Call 'ClericGuard' @($session,$hero)
Call 'ClericEnd' @($session,$hero)
$s=Capture $session
$request=[Decennium.Foundation.IntimidatingPresenceRequest]::new([string[]]@($hero,$ally))
$command=[Decennium.Foundation.Command]::new('fear.branch.fourth',$npc,$s.Revision,[Decennium.Foundation.CommandKind]::UseIntimidatingPresence,'',0,0,$null,$null,$null,$null,[Decennium.Foundation.OverwatchRider]::None,$null,$null,$null,$null,$null,$null,$null,$request)
$result=$session.SubmitDefenderIntimidatingPresence([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),$command)
if($result.Response-ne'Committed'){throw ($result|ConvertTo-Json -Depth 4)}
Report $session 'fourth-use'
Call 'ClericDefender' @($session)
Call 'ClericGuard' @($session,$ally)
Call 'ClericEnd' @($session,$ally)
Call 'ClericGuard' @($session,$hero)
$view=$session.View([Decennium.Foundation.Laboratory.ExpeditionSeat]::Player)
$combat=[Decennium.Foundation.CombatRequest]::new($view.TurnId,'TEST_ONLY.actor-club')
Command $session $hero 'AttackClub' $npc -Combat $combat
Report $session 'hero-attacked-source'
if((Capture $session).Lives.Where({$_.ActorId-eq$npc})[0].Hp-eq0){
    Command $session $hero 'EndFixedEncounter' $session.View([Decennium.Foundation.Laboratory.ExpeditionSeat]::Player).TurnId
    Report $session 'closed-after-source-death'
}
