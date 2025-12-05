Param(
    [string]$LogName = "System",
    [int]$LastHours = 1
)

$startTime = (Get-Date).AddHours(-$LastHours)

$events = Get-WinEvent -LogName $LogName | Where-Object { $_.TimeCreated -ge $startTime } |
    Select-Object TimeCreated, Id, LevelDisplayName, ProviderName, Message

$events | ConvertTo-Json -Depth 3
