# Build Windows Installer (.exe) for Clawdbot
# Uses pkg to create standalone executable

param(
    [string]$Version = "2026.1.25",
    [string]$OutputDir = "dist-installer",
    [switch]$BuildAll = $false
)

$ErrorActionPreference = "Stop"

Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Clawdbot Installer Builder                               ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Check if pkg is installed
Write-Host "➤ Checking for pkg..." -ForegroundColor Yellow
if (-not (Get-Command "pkg" -ErrorAction SilentlyContinue)) {
    Write-Host "✗ pkg not found! Installing..." -ForegroundColor Red
    npm install -g pkg
    Write-Host "✓ pkg installed!" -ForegroundColor Green
} else {
    Write-Host "✓ pkg found!" -ForegroundColor Green
}

# Create output directory
Write-Host "➤ Creating output directory..." -ForegroundColor Yellow
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}
Write-Host "✓ Output directory ready: $OutputDir" -ForegroundColor Green

# Build TypeScript first
Write-Host "➤ Building TypeScript..." -ForegroundColor Yellow
pnpm build
Write-Host "✓ TypeScript build complete!" -ForegroundColor Green

# Create installer entry point
Write-Host "➤ Creating installer entry point..." -ForegroundColor Yellow
$installerEntryPoint = @"
#!/usr/bin/env node
// Clawdbot Installer Entry Point
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { spawn } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Run setup wizard
const wizardPath = join(__dirname, 'setup-wizard.mjs');

const child = spawn('node', [wizardPath], {
  stdio: 'inherit',
  shell: true,
});

child.on('exit', (code) => {
  process.exit(code || 0);
});
"@

$installerPath = "scripts/installer-entry.mjs"
$installerEntryPoint | Out-File -FilePath $installerPath -Encoding UTF8
Write-Host "✓ Installer entry point created!" -ForegroundColor Green

# Build with pkg
Write-Host "➤ Building executable with pkg..." -ForegroundColor Yellow

if ($BuildAll) {
    # Build for all platforms
    Write-Host "Building for Windows x64..." -ForegroundColor Cyan
    pkg scripts/installer-entry.mjs --target node22-win-x64 --output "$OutputDir/clawdbot-installer-win-x64.exe"
    
    Write-Host "Building for Windows ARM64..." -ForegroundColor Cyan
    pkg scripts/installer-entry.mjs --target node22-win-arm64 --output "$OutputDir/clawdbot-installer-win-arm64.exe"
    
    Write-Host "Building for Linux x64..." -ForegroundColor Cyan
    pkg scripts/installer-entry.mjs --target node22-linux-x64 --output "$OutputDir/clawdbot-installer-linux-x64"
    
    Write-Host "Building for macOS x64..." -ForegroundColor Cyan
    pkg scripts/installer-entry.mjs --target node22-macos-x64 --output "$OutputDir/clawdbot-installer-macos-x64"
    
    Write-Host "Building for macOS ARM64..." -ForegroundColor Cyan
    pkg scripts/installer-entry.mjs --target node22-macos-arm64 --output "$OutputDir/clawdbot-installer-macos-arm64"
} else {
    # Build for Windows only (current platform)
    $arch = if ([Environment]::Is64BitOperatingSystem) { "x64" } else { "arm64" }
    Write-Host "Building for Windows $arch..." -ForegroundColor Cyan
    pkg scripts/installer-entry.mjs --target "node22-win-$arch" --output "$OutputDir/clawdbot-installer.exe"
}

Write-Host "✓ Executable(s) built successfully!" -ForegroundColor Green

# Create Inno Setup script (for advanced installer)
Write-Host "`n➤ Creating Inno Setup script..." -ForegroundColor Yellow
$innoScript = @"
; Clawdbot Installer Script for Inno Setup
; Compile with Inno Setup Compiler

#define MyAppName "Clawdbot"
#define MyAppVersion "$Version"
#define MyAppPublisher "Clawdbot Team"
#define MyAppURL "https://clawd.bot"
#define MyAppExeName "clawdbot-installer.exe"

[Setup]
AppId={{CLAWDBOT-INSTALLER-2026}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\LICENSE
OutputDir=$OutputDir
OutputBaseFilename=clawdbot-setup-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "$OutputDir\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\INSTALLATION-TH.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\USER-GUIDE-TH.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  // Check if Node.js is installed
  if not RegKeyExists(HKLM, 'SOFTWARE\Node.js') and 
     not RegKeyExists(HKCU, 'SOFTWARE\Node.js') then
  begin
    if MsgBox('Node.js is required but not found. Do you want to download it now?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://nodejs.org/', '', '', SW_SHOW, ewNoWait, ResultCode);
    end;
    Result := False;
  end
  else
    Result := True;
end;
"@

$innoScript | Out-File -FilePath "$OutputDir/clawdbot-installer.iss" -Encoding UTF8
Write-Host "✓ Inno Setup script created: $OutputDir/clawdbot-installer.iss" -ForegroundColor Green

# Create NSIS script (alternative)
Write-Host "➤ Creating NSIS script..." -ForegroundColor Yellow
$nsisScript = @'
; Clawdbot Installer Script for NSIS
; Compile with NSIS (Nullsoft Scriptable Install System)

!define PRODUCT_NAME "Clawdbot"
!define PRODUCT_VERSION "2026.1.25"
!define PRODUCT_PUBLISHER "Clawdbot Team"
!define PRODUCT_WEB_SITE "https://clawd.bot"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "clawdbot-setup-nsis.exe"
InstallDir "$PROGRAMFILES\Clawdbot"
InstallDirRegKey HKLM "Software\Clawdbot" "Install_Dir"

RequestExecutionLevel admin

Page directory
Page instfiles

Section "Install"
  SetOutPath $INSTDIR
  
  File "clawdbot-installer.exe"
  File "..\README.md"
  File "..\INSTALLATION-TH.md"
  File "..\USER-GUIDE-TH.md"
  File "..\LICENSE"
  
  WriteRegStr HKLM "Software\Clawdbot" "Install_Dir" "$INSTDIR"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Clawdbot" "DisplayName" "Clawdbot"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Clawdbot" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Clawdbot" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Clawdbot" "NoRepair" 1
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
  CreateDirectory "$SMPROGRAMS\Clawdbot"
  CreateShortcut "$SMPROGRAMS\Clawdbot\Clawdbot.lnk" "$INSTDIR\clawdbot-installer.exe"
  CreateShortcut "$SMPROGRAMS\Clawdbot\Uninstall.lnk" "$INSTDIR\uninstall.exe"
  CreateShortcut "$DESKTOP\Clawdbot.lnk" "$INSTDIR\clawdbot-installer.exe"
SectionEnd

Section "Uninstall"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Clawdbot"
  DeleteRegKey HKLM "Software\Clawdbot"
  
  Delete "$INSTDIR\*.*"
  Delete "$SMPROGRAMS\Clawdbot\*.*"
  RMDir "$SMPROGRAMS\Clawdbot"
  RMDir "$INSTDIR"
SectionEnd
'@

$nsisScript | Out-File -FilePath "$OutputDir/clawdbot-installer.nsi" -Encoding UTF8
Write-Host "✓ NSIS script created: $OutputDir/clawdbot-installer.nsi" -ForegroundColor Green

# Summary
Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  Build Complete!                                          ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "Output files:" -ForegroundColor Cyan
Get-ChildItem $OutputDir -Filter "clawdbot-*" | ForEach-Object {
    Write-Host "  - $($_.Name)" -ForegroundColor White
}

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Test the installer: .\$OutputDir\clawdbot-installer.exe"
Write-Host "  2. (Optional) Compile Inno Setup script for advanced installer"
Write-Host "  3. (Optional) Compile NSIS script for alternative installer"
Write-Host "`nInno Setup Compiler: https://jrsoftware.org/isinfo.php"
Write-Host "NSIS: https://nsis.sourceforge.io/`n"
