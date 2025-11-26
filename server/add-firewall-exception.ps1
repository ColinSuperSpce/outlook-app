# Windows Firewall Exception Script for Outlook Auto Attach Server
# This script adds a firewall rule to allow the server to accept connections on port 8765
# Must be run as Administrator

Write-Host "Outlook Auto Attach Server - Firewall Exception Setup" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host ""
    Write-Host "To run as Administrator:" -ForegroundColor Yellow
    Write-Host "1. Right-click on PowerShell" -ForegroundColor Yellow
    Write-Host "2. Select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host "3. Navigate to this folder and run this script again" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Or, right-click this script and select 'Run with PowerShell' (Administrator)" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

$port = 8765
$ruleName = "Outlook Auto Attach Server - Port $port"

Write-Host "Adding firewall exception for port $port..." -ForegroundColor Yellow

# Remove existing rule if it exists
$existingRule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
if ($existingRule) {
    Write-Host "Removing existing firewall rule..." -ForegroundColor Yellow
    Remove-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
}

# Add new firewall rule for inbound connections on port 8765 (localhost only)
try {
    New-NetFirewallRule -DisplayName $ruleName `
        -Direction Inbound `
        -Protocol TCP `
        -LocalPort $port `
        -Action Allow `
        -Description "Allows Outlook Auto Attach Server to receive connections on localhost:8765" `
        -Profile Domain,Private,Public `
        -ErrorAction Stop
    
    Write-Host ""
    Write-Host "Firewall exception added successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Rule details:" -ForegroundColor Cyan
    Write-Host "  Name: $ruleName" -ForegroundColor White
    Write-Host "  Port: $port (TCP)" -ForegroundColor White
    Write-Host "  Direction: Inbound" -ForegroundColor White
    Write-Host "  Action: Allow" -ForegroundColor White
    Write-Host ""
    Write-Host "The server should now be able to accept connections from Chrome extension." -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to add firewall rule!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "You may need to manually add the exception:" -ForegroundColor Yellow
    Write-Host "1. Open Windows Defender Firewall" -ForegroundColor Yellow
    Write-Host "2. Advanced settings" -ForegroundColor Yellow
    Write-Host "3. Inbound Rules → New Rule" -ForegroundColor Yellow
    Write-Host "4. Port → TCP → Specific local ports: $port" -ForegroundColor Yellow
    Write-Host "5. Allow the connection → Check all profiles → Name: '$ruleName'" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


