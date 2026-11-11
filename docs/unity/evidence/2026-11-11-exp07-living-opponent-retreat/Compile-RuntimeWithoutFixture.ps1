param([string]$PackageRoot,[string]$OutputRoot)
$ErrorActionPreference='Stop'
New-Item -ItemType Directory -Path $OutputRoot | Out-Null
$options=@('/langversion:9.0','/warnaserror')
$refs=@(Get-ChildItem -LiteralPath (Join-Path $PSHOME 'ref') -Filter '*.dll' | ForEach-Object FullName)
$source=foreach($group in 'Core','Persistence'){
    $dll=Join-Path $OutputRoot "Decennium.Foundation.$group.dll"
    $files=@(Get-ChildItem -Path (Join-Path $PackageRoot "Runtime/$group/*.cs") -File)
    Add-Type -Path $files.FullName -OutputAssembly $dll -ReferencedAssemblies $refs -CompilerOptions $options
    Add-Type -Path $dll
    $refs+=$dll
    $files | ForEach-Object {
        [ordered]@{path='com.decennium.foundation/'+[IO.Path]::GetRelativePath($PackageRoot,$_.FullName).Replace('\','/');sha256=(Get-FileHash -LiteralPath $_.FullName).Hash.ToLowerInvariant()}
    }
}
[ordered]@{status='PASS';language='C# 9';compilerOptions=$options;profile='Runtime Core and Persistence without TEST_ONLY or HEADLESS_TESTS';sourceHashes=@($source)} |
    ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $OutputRoot 'results.json') -Encoding utf8
"PASS: $($source.Count) runtime source files without laboratory defines."
