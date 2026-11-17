param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$InputPath,[Parameter(Mandatory)][string]$Run)
$ErrorActionPreference='Stop'
$repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$geometrySourceInputPath=(Resolve-Path -LiteralPath $InputPath).Path
if(Test-Path -LiteralPath $Run){throw 'Use a fresh geometry baseline output directory.'}
$Run=(New-Item -ItemType Directory -Path $Run).FullName
. (Join-Path $PSScriptRoot 'Execution-SourceBinding.ps1')
$executionSourceBinding=Start-GeometryExecutionBinding $Run @($PSCommandPath,(Join-Path $repository 'engine/tools/Open-ConnectedExpedition.ps1'),$geometrySourceInputPath)
Copy-Item -LiteralPath $geometrySourceInputPath -Destination (Join-Path $Run 'source-inputs.jsonl')
$empty=Join-Path $Run 'empty.jsonl';[IO.File]::WriteAllText($empty,'')
. (Join-Path $repository 'engine/tools/Open-ConnectedExpedition.ps1') -DeclaredGeometry -AssemblyRoot $AssemblyRoot -InputPath $empty
$report=[ordered]@{status='FAIL';scope='Fresh declared-geometry execution of retained Bishop command route; no beyond-boundary claim';commands=0;saves=0;startedUtc=[DateTime]::UtcNow.ToString('o')}
$report.assemblies=@(foreach($part in 'Core','Persistence','LabModel'){
    $file=Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll";$loaded=[Reflection.Assembly]::LoadFrom($file)
    if($loaded.Location-cne$file){throw 'Unexpected loaded baseline assembly'}
    @{name=$part;sha256=(Get-FileHash -LiteralPath $file).Hash.ToLowerInvariant();moduleId=$loaded.ManifestModule.ModuleVersionId.ToString()}
})
$inputWriter=[IO.StreamWriter]::new((Join-Path $Run 'executed-inputs.jsonl'))
$responseWriter=[IO.StreamWriter]::new((Join-Path $Run 'responses.jsonl'))
Push-Location $Run
try {
    foreach($line in [IO.File]::ReadAllLines($geometrySourceInputPath)){
        $request=ConvertFrom-Json -AsHashtable $line
        if($request.op-eq'submit'-and$request.kind-eq'CastKnownSpell'-and$request.spellCast.spellId-eq'dispel-magic-lesser'){
            # Aura observation tokens are profile-bound public identities, never copied from another profile.
            $choices=@($session.DiscoverCastingCommands('Player',$request.actor)|Where-Object {
                $_.Query.Admissible-and$_.Command.Kind-eq'CastKnownSpell'-and$_.Command.SpellCast.SpellId-eq'dispel-magic-lesser'
            })
            if($choices.Count-ne1){throw 'Expected one current public Dispel choice on the retained route.'}
            $request.target=$choices[0].Command.Target
            $line=ConvertTo-Json -InputObject $request -Depth 12 -Compress
        }
        $inputWriter.WriteLine($line);$inputWriter.Flush()
        $response=Write-SessionResponse $line
        $responseWriter.WriteLine($response);$responseWriter.Flush()
        $parsed=$response|ConvertFrom-Json
        if($request.op-eq'save'){
            if($parsed.Response-ne'Saved'){throw "Save failed: $response"}
            $report.saves++
        } else {
            if($parsed.Response-ne'Committed'){throw "Command failed: $line / $response"}
            $report.commands++
            if($parsed.Revision-ne$report.commands){throw "Unexpected command revision: $response"}
        }
    }
    $session.Save((Join-Path $Run 'final.ddsave'))
    $snapshot=[Decennium.Foundation.FileSaveStore]::new().Load((Join-Path $Run 'final.ddsave'))
    $report.finalRevision=$snapshot.Revision;$report.finalWire=$snapshot.WireSchemaVersion
    $report.finalFingerprint=$snapshot.ContentFingerprint;$report.finalClock=$snapshot.RuleClock
    if($report.commands-ne457-or$report.finalWire-ne113){throw 'Incomplete geometry baseline route.'}
    $report.status='PASS'
} catch {$report.error=$_.ToString();throw}
finally {
    Pop-Location;$inputWriter.Dispose();$responseWriter.Dispose()
    Complete-GeometryExecutionBinding $Run $executionSourceBinding
    $report.finishedUtc=[DateTime]::UtcNow.ToString('o')
    $report|ConvertTo-Json -Depth 10|Set-Content -LiteralPath (Join-Path $Run 'results.json') -Encoding utf8
}
$report|ConvertTo-Json -Depth 10
