Write-Output "Running basic remediation..."
Write-Output "1) Flushing DNS cache"
ipconfig /flushdns | Out-Null

Write-Output "2) Checking network configuration"
ipconfig

Write-Output "3) Pinging default gateway"
$gateway = (Get-NetRoute -DestinationPrefix "0.0.0.0/0" | Select-Object -First 1).NextHop
if ($gateway) {
    ping $gateway -n 2
} else {
    Write-Output "No default gateway found."
}

Write-Output "Remediation script finished."
