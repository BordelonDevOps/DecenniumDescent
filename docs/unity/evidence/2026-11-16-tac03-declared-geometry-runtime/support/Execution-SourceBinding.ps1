function Start-GeometryExecutionBinding([string]$Run,[string[]]$Paths) {
    $repository=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../../..')).Path
    $rows=@(foreach($path in @($Paths)+$PSCommandPath|Sort-Object -Unique){
        $resolved=(Resolve-Path -LiteralPath $path).Path
        $item=Get-Item -LiteralPath $resolved
        [ordered]@{path=[IO.Path]::GetRelativePath($repository,$resolved).Replace('\','/');absolutePath=$resolved;bytes=$item.Length;sha256=(Get-FileHash -LiteralPath $resolved).Hash.ToLowerInvariant()}
    })
    [ordered]@{phase='before-execution';at=[DateTime]::UtcNow.ToString('o');pid=$PID;files=$rows}|ConvertTo-Json -Depth 6|
        Set-Content -LiteralPath (Join-Path $Run 'execution-sources.before.json') -Encoding utf8
    return ,$rows
}
function Complete-GeometryExecutionBinding([string]$Run,$Binding) {
    foreach($row in $Binding){
        if((Get-Item -LiteralPath $row.absolutePath).Length-ne$row.bytes-or(Get-FileHash -LiteralPath $row.absolutePath).Hash.ToLowerInvariant()-cne$row.sha256){throw "Execution source changed: $($row.path)"}
    }
    [ordered]@{phase='after-execution';status='PASS';at=[DateTime]::UtcNow.ToString('o');pid=$PID;files=$Binding}|ConvertTo-Json -Depth 6|
        Set-Content -LiteralPath (Join-Path $Run 'execution-sources.after.json') -Encoding utf8
}
