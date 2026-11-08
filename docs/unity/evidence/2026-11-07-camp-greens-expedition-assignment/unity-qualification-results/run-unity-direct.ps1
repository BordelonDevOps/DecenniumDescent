param(
    [Parameter(Mandatory=$true)][string]$EditorPath,
    [Parameter(Mandatory=$true)][string]$ProjectPath,
    [Parameter(Mandatory=$true)][string]$ExecuteMethod,
    [Parameter(Mandatory=$true)][string]$LogPath,
    [Parameter(Mandatory=$true)][string]$ResultPath,
    [int]$TimeoutSeconds=660
)
$startedAt = Get-Date
[Environment]::SetEnvironmentVariable("DECENNIUM_QUALIFICATION_RESULT_PATH", $ResultPath, "Process")
$argumentLine = "-batchmode -nographics -projectPath `"$ProjectPath`" -executeMethod $ExecuteMethod -logFile `"$LogPath`""
Start-Process -FilePath $EditorPath -ArgumentList $argumentLine | Out-Null
$deadline = $startedAt.AddSeconds($TimeoutSeconds)
while (-not (Test-Path -LiteralPath $ResultPath)) {
    if ((Get-Date) -gt $deadline) {
        throw "Timed out waiting for Package Manager result. Inspect $LogPath"
    }
    Start-Sleep -Seconds 1
}
$result = Get-Content -LiteralPath $ResultPath
$exitCode = [int]$result[0]
$message = $result | Select-Object -Skip 1
"UnityQualificationResult=$exitCode"
$message
$shutdownDeadline = (Get-Date).AddSeconds(30)
while ((Get-CimInstance Win32_Process -Filter "Name = 'Unity.exe'" | Where-Object { $_.CommandLine -like "*$ProjectPath*" })) {
    if ((Get-Date) -gt $shutdownDeadline) {
        throw "Editor recorded its result but remained alive for more than 30 seconds. Inspect $LogPath"
    }
    Start-Sleep -Seconds 1
}
"DurationSeconds=$([int]((Get-Date) - $startedAt).TotalSeconds)"
exit $exitCode
