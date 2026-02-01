# Build Protected Installer - Python + Obfuscation
# Creates .exe with obfuscated code that's hard to reverse engineer

param(
    [string]$Version = "2026.1.25",
    [string]$OutputDir = "dist-protected",
    [ValidateSet("pyinstaller", "nuitka", "pyarmor")]
    [string]$Method = "pyinstaller",
    [switch]$Obfuscate = $true
)

$ErrorActionPreference = "Stop"

Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Clawdbot Protected Installer Builder                    ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Create output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

# Check Python
Write-Host "➤ Checking Python..." -ForegroundColor Yellow
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from: https://www.python.org/"
    exit 1
}
Write-Host "✓ Python found!" -ForegroundColor Green

# Install required packages
Write-Host "➤ Installing required packages..." -ForegroundColor Yellow

$packages = @("pyinstaller", "tkinter")

if ($Obfuscate) {
    $packages += @("pyarmor", "pyminifier")
}

foreach ($pkg in $packages) {
    Write-Host "  Installing $pkg..." -ForegroundColor Cyan
    python -m pip install -q $pkg
}
Write-Host "✓ Packages installed!" -ForegroundColor Green

# Obfuscate code if requested
if ($Obfuscate) {
    Write-Host "➤ Obfuscating Python code..." -ForegroundColor Yellow
    
    $sourceFile = "scripts/setup-wizard-gui.py"
    $obfuscatedFile = "scripts/setup-wizard-gui.obf.py"
    
    # Method 1: PyArmor (Best protection)
    Write-Host "  Using PyArmor for obfuscation..." -ForegroundColor Cyan
    
    # Initialize PyArmor
    if (-not (Test-Path "scripts/.pyarmor")) {
        pyarmor init --src scripts
    }
    
    # Obfuscate with PyArmor
    pyarmor obfuscate --exact `
        --restrict 0 `
        --output "scripts/obfuscated" `
        $sourceFile
    
    $obfuscatedFile = "scripts/obfuscated/setup-wizard-gui.py"
    
    Write-Host "✓ Code obfuscated!" -ForegroundColor Green
} else {
    $obfuscatedFile = "scripts/setup-wizard-gui.py"
}

# Build with PyInstaller
Write-Host "➤ Building executable with PyInstaller..." -ForegroundColor Yellow

$pyinstallerArgs = @(
    "--name=ClawdBot-Installer"
    "--onefile"
    "--windowed"
    "--icon=assets/icon.ico"  # Optional: add icon
    "--add-data=INSTALLATION-TH.md;."
    "--add-data=USER-GUIDE-TH.md;."
    "--add-data=LICENSE;."
    "--noconsole"
    "--clean"
)

# Advanced protection options
if ($Obfuscate) {
    $pyinstallerArgs += @(
        "--key=ClawdBotSecretKey2026"  # Encryption key
        "--upx-dir=C:\upx"  # UPX compression (if installed)
        "--strip"  # Strip symbols
    )
}

# Add version info
$versionFile = @"
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=($($Version.Replace('.', ','))),
    prodvers=($($Version.Replace('.', ','))),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Clawdbot Team'),
        StringStruct(u'FileDescription', u'Clawdbot Setup Wizard'),
        StringStruct(u'FileVersion', u'$Version'),
        StringStruct(u'InternalName', u'clawdbot-installer'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2026'),
        StringStruct(u'OriginalFilename', u'ClawdBot-Installer.exe'),
        StringStruct(u'ProductName', u'Clawdbot'),
        StringStruct(u'ProductVersion', u'$Version')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"@

$versionFile | Out-File -FilePath "scripts/version.txt" -Encoding UTF8

$pyinstallerArgs += "--version-file=scripts/version.txt"

# Run PyInstaller
Write-Host "  Building..." -ForegroundColor Cyan
pyinstaller $pyinstallerArgs $obfuscatedFile

# Move output
Move-Item "dist/ClawdBot-Installer.exe" "$OutputDir/ClawdBot-Installer-v$Version.exe" -Force

Write-Host "✓ Executable built!" -ForegroundColor Green

# Build JavaScript obfuscated installer (optional)
Write-Host "`n➤ Building JavaScript obfuscated installer..." -ForegroundColor Yellow

# Install javascript-obfuscator
npm install -g javascript-obfuscator

# Obfuscate setup wizard
$jsSource = "scripts/setup-wizard.mjs"
$jsObfuscated = "scripts/setup-wizard.obf.mjs"

Write-Host "  Obfuscating JavaScript..." -ForegroundColor Cyan
javascript-obfuscator $jsSource `
    --output $jsObfuscated `
    --compact true `
    --control-flow-flattening true `
    --control-flow-flattening-threshold 0.75 `
    --dead-code-injection true `
    --dead-code-injection-threshold 0.4 `
    --debug-protection true `
    --debug-protection-interval true `
    --disable-console-output true `
    --identifier-names-generator hexadecimal `
    --log false `
    --numbers-to-expressions true `
    --rename-globals true `
    --self-defending true `
    --simplify true `
    --split-strings true `
    --split-strings-chunk-length 10 `
    --string-array true `
    --string-array-calls-transform true `
    --string-array-encoding rc4 `
    --string-array-index-shift true `
    --string-array-rotate true `
    --string-array-shuffle true `
    --string-array-wrappers-count 2 `
    --string-array-wrappers-chained-calls true `
    --string-array-wrappers-parameters-max-count 4 `
    --string-array-wrappers-type function `
    --string-array-threshold 0.75 `
    --transform-object-keys true `
    --unicode-escape-sequence true

Write-Host "✓ JavaScript obfuscated!" -ForegroundColor Green

# Build with pkg
Write-Host "  Building with pkg..." -ForegroundColor Cyan
pkg $jsObfuscated `
    --target node22-win-x64 `
    --output "$OutputDir/ClawdBot-Installer-JS-v$Version.exe" `
    --compress Brotli

Write-Host "✓ JavaScript installer built!" -ForegroundColor Green

# Optional: Add digital signature (requires certificate)
Write-Host "`n➤ Digital Signature (Optional)..." -ForegroundColor Yellow
if (Test-Path "cert.pfx") {
    Write-Host "  Signing executable..." -ForegroundColor Cyan
    
    $cert = Get-PfxCertificate -FilePath "cert.pfx"
    Set-AuthenticodeSignature `
        -FilePath "$OutputDir/ClawdBot-Installer-v$Version.exe" `
        -Certificate $cert `
        -TimestampServer "http://timestamp.digicert.com"
    
    Write-Host "✓ Executable signed!" -ForegroundColor Green
} else {
    Write-Host "  ⚠ No certificate found (cert.pfx)" -ForegroundColor Yellow
    Write-Host "  Skipping code signing..." -ForegroundColor Yellow
}

# Cleanup
Write-Host "`n➤ Cleaning up..." -ForegroundColor Yellow
Remove-Item -Recurse -Force "build", "dist" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "scripts/obfuscated" -ErrorAction SilentlyContinue
Remove-Item -Force "*.spec" -ErrorAction SilentlyContinue
Write-Host "✓ Cleanup complete!" -ForegroundColor Green

# Create checksums
Write-Host "`n➤ Creating checksums..." -ForegroundColor Yellow
Get-ChildItem "$OutputDir/*.exe" | ForEach-Object {
    $hash = Get-FileHash $_.FullName -Algorithm SHA256
    "$($hash.Hash)  $($_.Name)" | Out-File -Append "$OutputDir/CHECKSUMS.txt"
}
Write-Host "✓ Checksums created!" -ForegroundColor Green

# Summary
Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  Build Complete!                                          ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "Protected installers created:" -ForegroundColor Cyan
Get-ChildItem "$OutputDir/*.exe" | ForEach-Object {
    $size = [math]::Round($_.Length / 1MB, 2)
    Write-Host "  - $($_.Name) ($size MB)" -ForegroundColor White
}

Write-Host "`nProtection features applied:" -ForegroundColor Yellow
if ($Obfuscate) {
    Write-Host "  ✓ Code obfuscation (PyArmor)" -ForegroundColor Green
    Write-Host "  ✓ String encryption" -ForegroundColor Green
    Write-Host "  ✓ Control flow flattening" -ForegroundColor Green
    Write-Host "  ✓ Dead code injection" -ForegroundColor Green
    Write-Host "  ✓ Self-defending code" -ForegroundColor Green
    Write-Host "  ✓ Debug protection" -ForegroundColor Green
}
Write-Host "  ✓ Single executable (no source)" -ForegroundColor Green
Write-Host "  ✓ Binary compilation" -ForegroundColor Green

Write-Host "`nSecurity notes:" -ForegroundColor Cyan
Write-Host "  • Python bytecode is obfuscated and encrypted"
Write-Host "  • JavaScript is heavily obfuscated with RC4 encryption"
Write-Host "  • Executables are compressed and stripped"
Write-Host "  • No source code is included in output"
Write-Host "  • Reverse engineering is significantly harder"
Write-Host "`n  Note: No protection is 100% unbreakable, but these"
Write-Host "  methods make it very difficult for casual attackers.`n"

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Test installer: .\$OutputDir\ClawdBot-Installer-v$Version.exe"
Write-Host "  2. Verify checksum: Get-FileHash .\$OutputDir\ClawdBot-Installer-v$Version.exe"
Write-Host "  3. (Optional) Add code signing certificate"
Write-Host "  4. Distribute installer`n"
