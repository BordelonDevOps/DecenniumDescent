param([Parameter(Mandatory)][string]$AssemblyRoot,[Parameter(Mandatory)][string]$BeforeApproachSave,[Parameter(Mandatory)][string]$ActiveSave)
$ErrorActionPreference='Stop'
foreach($part in 'Core','Persistence','LabModel','HeadlessTests'){Add-Type -Path (Join-Path $AssemblyRoot "Decennium.Foundation.$part.dll")}
$type=[Decennium.Foundation.Tests.FoundationCases];$flags=[Reflection.BindingFlags]'Static,NonPublic'
function Call([string]$Name,[object[]]$Arguments){try{$type.GetMethod($Name,$flags).Invoke($null,$Arguments)}catch{throw $_.Exception.InnerException}}
$session=Call 'NewFrightenedExpedition' @()
$session.Restore((Resolve-Path -LiteralPath $BeforeApproachSave).Path)
$hero=[Decennium.Foundation.Laboratory.ConnectedExpeditionSession]::Hero
$turn=$session.View([Decennium.Foundation.Laboratory.ExpeditionSeat]::Player).TurnId
Call 'ClericCommit' @($session,$hero,[Decennium.Foundation.CommandKind]::TacticalStep,$turn,0,2,$null)
Call 'ClericEnd' @($session,$hero)
$ready=Call 'ShortRestCapture' @($session)
$policy=Call 'ClericPolicy' @($session)
Call 'FrightenedDetachedSourceControls' @($policy,$ready)
$active=[Decennium.Foundation.FileSaveStore]::new().Load((Resolve-Path -LiteralPath $ActiveSave).Path)
Call 'FrightenedDetachedSuppressedRepeat' @($active)
Write-Output 'PASS: detached source preflight, immunity/payment and suppressed repeat controls.'
