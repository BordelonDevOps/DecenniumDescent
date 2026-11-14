param([string]$AssemblyRoot,[string]$PendingSave,[string]$CompletedSave,[string]$Run)
$ErrorActionPreference='Stop'
$AssemblyRoot=(Resolve-Path -LiteralPath $AssemblyRoot).Path
$Run=(New-Item -ItemType Directory -Path $Run).FullName
foreach ($name in 'Core','Persistence') { Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$name.dll") }
function Digest($path) { (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
$store=[Decennium.Foundation.FileSaveStore]::new()
$states=@($store.Load((Resolve-Path -LiteralPath $PendingSave).Path),$store.Load((Resolve-Path -LiteralPath $CompletedSave).Path))
$digests=@((Digest $PendingSave),(Digest $CompletedSave))
$path=Join-Path $Run 'repeated.ddsave'
$rows=[Collections.Generic.List[object]]::new()
$previous=$null
for ($index=0; $index -lt 32; $index++) {
    $selected=$index % 2
    $store.Save($path,$states[$selected])
    $primary=Digest $path
    $backup=if ($index -gt 0) { Digest ($path+'.bak') } else { $null }
    if ($primary -cne $digests[$selected] -or $backup -cne $previous) { throw "Save/backup bytes differ at replacement $index." }
    $rows.Add(@{Iteration=$index;PrimarySha256=$primary;BackupSha256=$backup})
    $previous=$primary
}
[ordered]@{Status='PASS'; Writes=$rows.Count; Replacements=($rows.Count-1); Inputs=$digests
    CoreSha256=(Digest (Join-Path $AssemblyRoot 'Decennium.Foundation.Core.dll'))
    PersistenceSha256=(Digest (Join-Path $AssemblyRoot 'Decennium.Foundation.Persistence.dll'))
    Scope='Repeated same-destination diagnostic after a prior OS replacement exception; does not establish its cause.'
    Observations=$rows} | ConvertTo-Json -Depth 5 | Set-Content "$Run/results.json" -Encoding utf8
Write-Output 'PASS: 32 same-destination writes and 31 exact previous-state backups.'
