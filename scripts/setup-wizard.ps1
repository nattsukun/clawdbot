# Clawdbot Setup Wizard for Windows
# PowerShell Interactive Installer

$ErrorActionPreference = "Stop"

# Colors
$Color = @{
    Info    = "Cyan"
    Success = "Green"
    Warning = "Yellow"
    Error   = "Red"
    Header  = "Magenta"
}

function Write-Header {
    param([string]$Text)
    Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor $Color.Header
    Write-Host "║  $($Text.PadRight(56)) ║" -ForegroundColor $Color.Header
    Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor $Color.Header
}

function Write-Step {
    param([string]$Text)
    Write-Host "➤ $Text" -ForegroundColor $Color.Info
}

function Write-Success {
    param([string]$Text)
    Write-Host "✓ $Text" -ForegroundColor $Color.Success
}

function Write-ErrorMsg {
    param([string]$Text)
    Write-Host "✗ $Text" -ForegroundColor $Color.Error
}

function Write-WarningMsg {
    param([string]$Text)
    Write-Host "⚠ $Text" -ForegroundColor $Color.Warning
}

function Test-CommandExists {
    param([string]$Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    } catch {
        return $false
    }
}

function Get-UserInput {
    param(
        [string]$Prompt,
        [string]$Default = ""
    )
    
    if ($Default) {
        $input = Read-Host "$Prompt [$Default]"
        return if ($input) { $input } else { $Default }
    } else {
        return Read-Host $Prompt
    }
}

function Confirm-Action {
    param([string]$Message)
    
    $response = Read-Host "$Message (Y/n)"
    return ($response -eq "" -or $response -eq "Y" -or $response -eq "y")
}

# Main Setup Wizard
Write-Header "Clawdbot Setup Wizard"
Write-Host "Welcome to Clawdbot installation wizard!`n" -ForegroundColor White

# Step 1: Check Prerequisites
Write-Header "Step 1: Checking Prerequisites"

# Check Node.js
Write-Step "Checking Node.js installation..."
if (Test-CommandExists "node") {
    $nodeVersion = node --version
    Write-Success "Node.js found: $nodeVersion"
    
    # Parse version
    $versionNumber = [int]($nodeVersion -replace 'v(\d+)\..*', '$1')
    if ($versionNumber -lt 22) {
        Write-WarningMsg "Node.js version 22 or higher is recommended. Current: $nodeVersion"
        if (Confirm-Action "Continue anyway?") {
            # Continue
        } else {
            Write-Host "Please upgrade Node.js and run setup again."
            exit 1
        }
    }
} else {
    Write-ErrorMsg "Node.js not found!"
    Write-Host "`nPlease install Node.js 22+ from: https://nodejs.org/"
    if (Confirm-Action "Open download page in browser?") {
        Start-Process "https://nodejs.org/"
    }
    exit 1
}

# Check pnpm
Write-Step "Checking pnpm installation..."
if (Test-CommandExists "pnpm") {
    $pnpmVersion = pnpm --version
    Write-Success "pnpm found: v$pnpmVersion"
} else {
    Write-WarningMsg "pnpm not found!"
    if (Confirm-Action "Install pnpm now?") {
        Write-Step "Installing pnpm..."
        npm install -g pnpm
        Write-Success "pnpm installed successfully!"
    } else {
        Write-Host "pnpm is required. Please install it manually: npm install -g pnpm"
        exit 1
    }
}

# Check Git
Write-Step "Checking Git installation..."
if (Test-CommandExists "git") {
    $gitVersion = git --version
    Write-Success "Git found: $gitVersion"
} else {
    Write-WarningMsg "Git not found (optional for development)"
}

# Step 2: Installation Type
Write-Header "Step 2: Installation Type"
Write-Host "1. Install from current directory (development)"
Write-Host "2. Install globally from npm"
Write-Host "3. Clone from repository`n"

$installType = Get-UserInput "Choose installation type (1-3)" "1"

switch ($installType) {
    "1" {
        # Install from current directory
        Write-Header "Step 3: Installing from Current Directory"
        
        if (-not (Test-Path "package.json")) {
            Write-ErrorMsg "package.json not found in current directory!"
            exit 1
        }
        
        Write-Step "Installing dependencies..."
        pnpm install
        Write-Success "Dependencies installed!"
        
        Write-Step "Building project..."
        pnpm build
        Write-Success "Build completed!"
        
        $installPath = Get-Location
    }
    "2" {
        # Install globally
        Write-Header "Step 3: Installing Globally"
        
        Write-Step "Installing clawdbot from npm..."
        npm install -g clawdbot
        Write-Success "Clawdbot installed globally!"
        
        $installPath = npm root -g
    }
    "3" {
        # Clone from repository
        Write-Header "Step 3: Cloning Repository"
        
        $repoUrl = Get-UserInput "Repository URL" "https://github.com/clawdbot/clawdbot.git"
        $installDir = Get-UserInput "Installation directory" "$env:USERPROFILE\clawdbot"
        
        Write-Step "Cloning repository..."
        git clone $repoUrl $installDir
        Set-Location $installDir
        
        Write-Step "Installing dependencies..."
        pnpm install
        Write-Success "Dependencies installed!"
        
        Write-Step "Building project..."
        pnpm build
        Write-Success "Build completed!"
        
        $installPath = $installDir
    }
}

# Step 4: Configuration
Write-Header "Step 4: Initial Configuration"

if (Confirm-Action "Configure Clawdbot now?") {
    
    # Gateway mode
    Write-Host "`nGateway Mode:"
    Write-Host "1. local  - Run gateway on this machine"
    Write-Host "2. remote - Connect to remote gateway"
    $gatewayMode = Get-UserInput "Choose gateway mode (1-2)" "1"
    $mode = if ($gatewayMode -eq "1") { "local" } else { "remote" }
    
    pnpm clawdbot config set gateway.mode $mode
    Write-Success "Gateway mode set to: $mode"
    
    # AI Provider
    if (Confirm-Action "`nConfigure AI Provider?") {
        Write-Host "`nAvailable Providers:"
        Write-Host "1. openai    - OpenAI (GPT)"
        Write-Host "2. anthropic - Anthropic (Claude)"
        Write-Host "3. google    - Google (Gemini)"
        Write-Host "4. skip      - Configure later`n"
        
        $providerChoice = Get-UserInput "Choose provider (1-4)" "4"
        
        $providerMap = @{
            "1" = "openai"
            "2" = "anthropic"
            "3" = "google"
        }
        
        if ($providerMap.ContainsKey($providerChoice)) {
            $provider = $providerMap[$providerChoice]
            pnpm clawdbot config set provider.name $provider
            
            $apiKey = Get-UserInput "`nEnter API Key (or press Enter to skip)"
            if ($apiKey) {
                pnpm clawdbot config set provider.apiKey $apiKey
                Write-Success "Provider configured: $provider"
            }
        }
    }
    
    # Logging level
    Write-Host "`nLog Level:"
    Write-Host "1. debug - Verbose logging"
    Write-Host "2. info  - Standard logging"
    Write-Host "3. warn  - Warnings only"
    Write-Host "4. error - Errors only`n"
    
    $logChoice = Get-UserInput "Choose log level (1-4)" "2"
    $logLevels = @{
        "1" = "debug"
        "2" = "info"
        "3" = "warn"
        "4" = "error"
    }
    
    if ($logLevels.ContainsKey($logChoice)) {
        $logLevel = $logLevels[$logChoice]
        pnpm clawdbot config set logging.level $logLevel
        Write-Success "Log level set to: $logLevel"
    }
}

# Step 5: Create shortcuts/aliases
Write-Header "Step 5: Create Shortcuts"

if (Confirm-Action "Create PowerShell profile shortcuts?") {
    
    $profilePath = $PROFILE
    
    if (-not (Test-Path $profilePath)) {
        New-Item -Path $profilePath -ItemType File -Force | Out-Null
    }
    
    $shortcuts = @"

# Clawdbot Shortcuts (Added by setup wizard)
function clawdbot { pnpm --dir '$installPath' clawdbot @args }
function clawdbot-start { pnpm --dir '$installPath' clawdbot gateway run --force }
function clawdbot-status { pnpm --dir '$installPath' clawdbot channels status --all }
function clawdbot-logs { Get-Content '$env:USERPROFILE\.clawdbot\logs\*.log' -Tail 50 -Wait }
Set-Alias -Name cb -Value clawdbot

"@
    
    Add-Content -Path $profilePath -Value $shortcuts
    Write-Success "Shortcuts added to PowerShell profile!"
    Write-Host "  - clawdbot         : Run clawdbot command"
    Write-Host "  - clawdbot-start   : Start gateway"
    Write-Host "  - clawdbot-status  : Check status"
    Write-Host "  - clawdbot-logs    : Watch logs"
    Write-Host "  - cb               : Alias for clawdbot"
}

# Step 6: Desktop shortcut
if (Confirm-Action "`nCreate desktop shortcut for gateway?") {
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "Clawdbot Gateway.lnk"
    
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = "powershell.exe"
    $Shortcut.Arguments = "-NoExit -Command `"cd '$installPath'; pnpm clawdbot gateway run`""
    $Shortcut.WorkingDirectory = $installPath
    $Shortcut.Description = "Start Clawdbot Gateway"
    $Shortcut.Save()
    
    Write-Success "Desktop shortcut created!"
}

# Step 7: Completion
Write-Header "Installation Complete!"

Write-Host "Clawdbot has been successfully installed!`n" -ForegroundColor Green

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Restart PowerShell to load new shortcuts"
Write-Host "  2. Run 'clawdbot login' to login to WhatsApp"
Write-Host "  3. Run 'clawdbot-start' to start the gateway"
Write-Host "  4. Check status with 'clawdbot-status'`n"

Write-Host "Useful commands:" -ForegroundColor Cyan
Write-Host "  clawdbot --help           - Show help"
Write-Host "  clawdbot config list      - View configuration"
Write-Host "  clawdbot channels status  - Check channels"
Write-Host "  clawdbot-logs             - Watch logs`n"

Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "  Installation Guide: INSTALLATION-TH.md"
Write-Host "  User Guide: USER-GUIDE-TH.md"
Write-Host "  Online Docs: https://docs.clawd.bot`n"

if (Confirm-Action "Start gateway now?") {
    Write-Step "Starting gateway..."
    Set-Location $installPath
    pnpm clawdbot gateway run
} else {
    Write-Host "`nSetup complete! Run 'clawdbot-start' when ready." -ForegroundColor Green
}
