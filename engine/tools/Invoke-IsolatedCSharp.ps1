param(
    [Parameter(Mandatory)][string[]]$Sources,
    [Parameter(Mandatory)][string[]]$References,
    [Parameter(Mandatory)][string[]]$CompilerOptions,
    [Parameter(Mandatory)][string]$OutputAssembly,
    [Parameter(Mandatory)][string]$CompilerPath,
    [string]$DotNetHost = 'dotnet'
)
$ErrorActionPreference = 'Stop'
$compiler = (Resolve-Path -LiteralPath $CompilerPath).Path
$responsePath = $OutputAssembly + '.rsp'
$arguments = @('-nologo', '-target:library') + $CompilerOptions + @('-out:' + $OutputAssembly) +
    @($References | ForEach-Object { '-reference:' + $_ }) + $Sources
if (@($arguments | Where-Object { $_.Contains('"') -or $_.Contains("`r") -or $_.Contains("`n") }).Count) {
    throw 'Compiler response arguments cannot contain quotes or line breaks.'
}
[IO.File]::WriteAllLines($responsePath, [string[]]@($arguments | ForEach-Object { '"' + $_ + '"' }), [Text.UTF8Encoding]::new($false))
$diagnostics = @(& $DotNetHost $compiler ('@' + $responsePath) 2>&1)
$compilerExit = $LASTEXITCODE
$diagnostics | Set-Content -LiteralPath ($OutputAssembly + '.compile.log') -Encoding utf8
if ($compilerExit -ne 0 -or !(Test-Path -LiteralPath $OutputAssembly) -or (Get-Item -LiteralPath $OutputAssembly).Length -eq 0) {
    throw ('Isolated C# compilation failed (exit ' + $compilerExit + '): ' + ($diagnostics -join "`n"))
}
