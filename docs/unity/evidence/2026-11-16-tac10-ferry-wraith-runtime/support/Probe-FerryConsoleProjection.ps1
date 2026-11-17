param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$Run,[switch]$ExpectInheritedProjection)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$launcher=Join-Path $repository 'engine/tools/Open-ConnectedExpedition.ps1'
if(Test-Path -LiteralPath $Run){throw 'Use a fresh projection probe directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Require($condition,$message){if(!$condition){throw $message}}
$report=[ordered]@{status='FAIL';scope='Public console versus public typed Ferry genesis projection; no gameplay or module acceptance claim';assemblies=@();seats=@();startedUtc=[DateTime]::UtcNow.ToString('o')}
try {
    foreach($name in 'Core','Persistence','LabModel'){$path=Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll";Add-Type -Path $path;$report.assemblies+=@{name=$name;sha256=(Digest $path)}}
    $report.script=@{path=$PSCommandPath;sha256=(Digest $PSCommandPath)}
    $report.launcher=@{path=$launcher;sha256=(Digest $launcher)}
    Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $Run 'Probe-FerryConsoleProjection.executed.ps1')
    Copy-Item -LiteralPath $launcher -Destination (Join-Path $Run 'Open-ConnectedExpedition.executed.ps1')
    $seats=@('Player','FirstOpponent','RecoveryOpponent','FerryOpponent')
    $inputs=Join-Path $Run 'inputs.jsonl'
    $seats|ForEach-Object {ConvertTo-Json -InputObject @{op='view';seat=$_} -Compress}|Set-Content -LiteralPath $inputs -Encoding utf8
    & pwsh -NoProfile -File $launcher -FerryWraith -AssemblyRoot $AssemblyRoot -InputPath $inputs > (Join-Path $Run 'console.jsonl') 2> (Join-Path $Run 'console.stderr.txt')
    Require ($LASTEXITCODE-eq0) 'Console process failed.'
    $console=@(Get-Content -LiteralPath (Join-Path $Run 'console.jsonl')|ForEach-Object {ConvertFrom-Json -AsHashtable $_})
    Require ($console.Count-eq$seats.Count) 'Console view count differs.'
    $session=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::StartWithFerryWraith(
        [Decennium.Foundation.Laboratory.ClericInitialSelection]::AuthoredExample(),[Decennium.Foundation.Laboratory.ClericRepertoireSelection]::AuthoredExample(),
        [Decennium.Foundation.ClericMilestoneDeclaration]::AuthoredExample(),[Decennium.Foundation.BishopEntryRecord]::Announced())
    $session.Save((Join-Path $Run 'before.ddsave'))
    for($i=0;$i-lt$seats.Count;$i++) {
        $seat=$seats[$i];$view=$session.View($seat)
        $targets=[ordered]@{};foreach($target in $view.KnownTargets.GetEnumerator()){$targets[$target.Key.ToString()]=$target.Value}
        $view=$view|Select-Object -Property * -ExcludeProperty KnownTargets,FleshWarden,ShortRest
        $view|Add-Member -NotePropertyName KnownTargets -NotePropertyValue $targets
        $json=ConvertTo-Json -InputObject $view -Depth 8 -Compress -EnumsAsStrings
        [IO.File]::WriteAllText((Join-Path $Run ($seat+'.typed-public.json')),$json)
        $expected=$json|ConvertFrom-Json -AsHashtable
        $missing=@('LongRest'|Where-Object {!$console[$i].ContainsKey($_)})
        foreach($actor in $expected.Actors) {
            $actual=@($console[$i].Actors|Where-Object {$_.Position.Id-eq$actor.Position.Id})
            Require ($actual.Count-eq1) 'Public actor identity differs.'
            foreach($property in 'Cleric','Repertoire','ClericSettlement','Casting','TemporaryHp','TemporaryHpUntil') {
                if(!$actual[0].ContainsKey($property)){$missing+=($actor.Position.Id+'.'+$property)}
            }
        }
        $report.seats+=@{seat=$seat;missing=$missing;typedActors=$expected.Actors.Count;consoleActors=$console[$i].Actors.Count}
        if($ExpectInheritedProjection){Require ($missing.Count-eq0) "Inherited public fields missing for $seat";Require (($json|ConvertFrom-Json -AsHashtable|ConvertTo-Json -Depth 30 -Compress)-ceq($console[$i]|ConvertTo-Json -Depth 30 -Compress)) "Public projection differs for $seat"}
        else{Require ($missing-contains'LongRest') "Expected omission not reproduced for $seat"}
    }
    $session.Save((Join-Path $Run 'after.ddsave'));Require ((Digest (Join-Path $Run 'before.ddsave'))-ceq(Digest (Join-Path $Run 'after.ddsave'))) 'Public typed view changed state.'
    Require ((Digest $launcher)-ceq$report.launcher.sha256) 'Console launcher changed during execution.'
    $report.status=if($ExpectInheritedProjection){'PASS_INHERITED_PUBLIC_FERRY_CONSOLE_PROJECTION'}else{'PASS_REPRODUCED_FERRY_CONSOLE_PROFILE_OMISSION'}
} catch {$report.error=$_.Exception.ToString()}
$report.completedUtc=[DateTime]::UtcNow.ToString('o');$report|ConvertTo-Json -Depth 15|Set-Content -LiteralPath (Join-Path $Run 'RESULT.json') -Encoding utf8
Write-Output "$($report.status): $Run"
if($report.status-eq'FAIL'){throw $report.error}
