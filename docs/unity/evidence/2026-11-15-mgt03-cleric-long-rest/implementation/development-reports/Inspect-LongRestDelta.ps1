param([string]$AssemblyRoot,[string]$Before,[string]$After)
foreach($part in 'Core','Persistence'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$codec=[Decennium.Foundation.SnapshotCodec]::new()
$a=$codec.Decode([IO.File]::ReadAllBytes([IO.Path]::GetFullPath($Before)));$b=$codec.Decode([IO.File]::ReadAllBytes([IO.Path]::GetFullPath($After)))
foreach($field in $a.GetType().GetFields()){
 if($field.FieldType.IsArray){
  $left=ConvertTo-Json -InputObject ($field.GetValue($a)) -Depth 12 -Compress
  $right=ConvertTo-Json -InputObject ($field.GetValue($b)) -Depth 12 -Compress
  if($left -cne $right){[pscustomobject]@{Field=$field.Name;BeforeCount=@($field.GetValue($a)).Count;AfterCount=@($field.GetValue($b)).Count;After=if($right.Length -lt 3500){$right}else{'large'}}|ConvertTo-Json -Depth 3 -Compress}
 }
}
