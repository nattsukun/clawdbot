# Protected Installer Documentation

## สำหรับผู้ใช้งาน

### การติดตั้ง Clawdbot ด้วย Protected Installer

#### Windows GUI Installer
1. ดาวน์โหลด `ClawdBot-Installer-v2026.1.25.exe`
2. Double-click เพื่อรัน
3. ทำตาม wizard (มี GUI สวยงาม)
4. เสร็จสิ้น!

**คุณสมบัติ:**
- ✨ GUI แบบ wizard ใช้งานง่าย
- 🔒 Code ถูก obfuscate และ encrypt
- 📦 Single .exe file ไม่ต้องติดตั้ง Python
- 🛡️ Protected จาก reverse engineering

---

## สำหรับ Developers

### วิธีสร้าง Protected Installer

#### ข้อกำหนด
- Python 3.8+
- Node.js 22+
- PyInstaller
- PyArmor (สำหรับ obfuscation)
- UPX (optional, สำหรับ compression)

#### การติดตั้ง Tools

```powershell
# Python packages
pip install pyinstaller pyarmor pyminifier

# JavaScript obfuscator
npm install -g javascript-obfuscator pkg

# UPX (optional)
# Download from: https://upx.github.io/
```

### สร้าง Protected Installer

#### Method 1: Python GUI Installer (แนะนำ)

```powershell
# Build with obfuscation (default)
.\scripts\build-protected-installer.ps1

# Build without obfuscation (faster, less secure)
.\scripts\build-protected-installer.ps1 -Obfuscate:$false

# Specify version
.\scripts\build-protected-installer.ps1 -Version "2026.2.1"

# Custom output directory
.\scripts\build-protected-installer.ps1 -OutputDir "release"
```

**Output:**
- `ClawdBot-Installer-v2026.1.25.exe` - Protected Python installer
- `ClawdBot-Installer-JS-v2026.1.25.exe` - Protected JavaScript installer
- `CHECKSUMS.txt` - SHA256 checksums

#### Method 2: แยกขั้นตอน (Advanced)

**Step 1: Obfuscate Python code**

```powershell
# Using PyArmor (Best protection)
pyarmor init --src scripts
pyarmor obfuscate `
    --exact `
    --restrict 0 `
    --output scripts/obfuscated `
    scripts/setup-wizard-gui.py

# Using Pyminifier (Alternative)
pyminifier `
    --obfuscate-variables `
    --obfuscate-functions `
    --obfuscate-classes `
    --obfuscate-builtins `
    scripts/setup-wizard-gui.py > scripts/setup-wizard-gui.obf.py
```

**Step 2: Build with PyInstaller**

```powershell
pyinstaller `
    --name=ClawdBot-Installer `
    --onefile `
    --windowed `
    --noconsole `
    --key="ClawdBotSecretKey2026" `
    --strip `
    --clean `
    scripts/obfuscated/setup-wizard-gui.py
```

**Step 3: Obfuscate JavaScript**

```powershell
javascript-obfuscator scripts/setup-wizard.mjs `
    --output scripts/setup-wizard.obf.mjs `
    --compact true `
    --control-flow-flattening true `
    --dead-code-injection true `
    --debug-protection true `
    --self-defending true `
    --string-array-encoding rc4 `
    --string-array-threshold 0.75
```

**Step 4: Build JavaScript installer**

```powershell
pkg scripts/setup-wizard.obf.mjs `
    --target node22-win-x64 `
    --output ClawdBot-Installer.exe `
    --compress Brotli
```

### Protection Levels

#### Level 1: Basic (Fast build)
```powershell
# No obfuscation, just compilation
pyinstaller --onefile scripts/setup-wizard-gui.py
```
- ⏱️ Build time: ~30 seconds
- 🔒 Protection: Low (bytecode only)
- 📦 Size: ~15 MB

#### Level 2: Standard (Recommended)
```powershell
.\scripts\build-protected-installer.ps1
```
- ⏱️ Build time: ~2 minutes
- 🔒 Protection: Medium-High
- 📦 Size: ~18 MB
- Features:
  - PyArmor obfuscation
  - String encryption
  - Code flow obfuscation
  - Binary compilation

#### Level 3: Maximum (Paranoid)
```powershell
.\scripts\build-protected-installer.ps1 -Obfuscate

# Then add:
# - Code signing certificate
# - Anti-debugging tricks
# - VM detection
# - Custom packer
```
- ⏱️ Build time: ~5 minutes
- 🔒 Protection: Very High
- 📦 Size: ~20 MB

### Protection Features

#### Python Protection (PyArmor)

**Features:**
- Obfuscate Python bytecode (.pyc)
- Encrypt string constants
- Protect against:
  - Decompilation (uncompyle6, decompyle3)
  - AST inspection
  - Bytecode modification
  - Dynamic tracing

**How it works:**
```
Source Code (.py)
    ↓
Obfuscated Code (.py)
    ↓
Encrypted Bytecode (.pyc)
    ↓
Runtime Decryption (in memory)
    ↓
Execution
```

#### JavaScript Protection

**Features:**
- String array encoding (RC4)
- Control flow flattening
- Dead code injection
- Self-defending code
- Debug protection
- Identifier renaming (hexadecimal)

**Example:**
```javascript
// Original
function hello(name) {
  console.log("Hello, " + name);
}

// Obfuscated (simplified)
var _0x4a2b=['log','Hello,\x20'];
(function(_0x3f1c42,_0x4a2b85){...})();
function _0x2c4a(_0x4f3d1a,_0x12a463){...}
function _0x5e2a(_0x1a2b,_0x3c4d){...}
```

### Advanced Protection Techniques

#### 1. Anti-Debugging

เพิ่มใน Python code:

```python
import sys
import ctypes

def is_debugger_present():
    """Check if debugger is attached (Windows)"""
    return ctypes.windll.kernel32.IsDebuggerPresent() != 0

def anti_debug():
    """Exit if debugger detected"""
    if is_debugger_present():
        sys.exit(1)

# Call at start
anti_debug()
```

#### 2. VM Detection

```python
import platform
import subprocess

def is_virtual_machine():
    """Detect if running in VM"""
    # Check manufacturer
    try:
        result = subprocess.check_output(
            'wmic bios get manufacturer',
            shell=True
        ).decode()
        
        vm_vendors = ['vmware', 'virtualbox', 'qemu', 'xen']
        return any(vendor in result.lower() for vendor in vm_vendors)
    except:
        return False

if is_virtual_machine():
    print("Virtual machine detected!")
```

#### 3. Integrity Check

```python
import hashlib
import sys

def check_integrity():
    """Verify executable hasn't been modified"""
    expected_hash = "abc123..."  # Compute during build
    
    with open(sys.executable, 'rb') as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()
    
    if actual_hash != expected_hash:
        sys.exit(1)
```

#### 4. Custom Packer

```powershell
# Use UPX for compression + obfuscation
upx --best --ultra-brute ClawdBot-Installer.exe

# Or use Themida, VMProtect, etc. (commercial)
```

### Code Signing

เพื่อป้องกัน Windows SmartScreen และเพิ่มความน่าเชื่อถือ:

#### สร้าง Self-Signed Certificate (Dev)

```powershell
# Create certificate
$cert = New-SelfSignedCertificate `
    -Type CodeSigningCert `
    -Subject "CN=Clawdbot Developer" `
    -CertStoreLocation Cert:\CurrentUser\My

# Export to PFX
$password = ConvertTo-SecureString -String "password" -Force -AsPlainText
Export-PfxCertificate `
    -Cert $cert `
    -FilePath cert.pfx `
    -Password $password
```

#### Sign Executable

```powershell
# Using PowerShell
$cert = Get-PfxCertificate -FilePath cert.pfx
Set-AuthenticodeSignature `
    -FilePath ClawdBot-Installer.exe `
    -Certificate $cert `
    -TimestampServer "http://timestamp.digicert.com"

# Or using signtool (Windows SDK)
signtool sign /f cert.pfx /p password `
    /t http://timestamp.digicert.com `
    ClawdBot-Installer.exe
```

#### Get Real Certificate (Production)

1. ซื้อจาก Certificate Authority:
   - DigiCert ($474/year)
   - Sectigo ($212/year)
   - GlobalSign ($319/year)

2. Submit installer for verification
3. Sign with trusted certificate
4. No more SmartScreen warnings!

### Testing Protected Installer

#### 1. Functional Testing

```powershell
# Run installer
.\dist-protected\ClawdBot-Installer-v2026.1.25.exe

# Verify installation
clawdbot --version

# Check config
clawdbot config list
```

#### 2. Security Testing

**Test reverse engineering difficulty:**

```powershell
# Try to decompile Python
uncompyle6 ClawdBot-Installer.exe
# Should fail with PyArmor protection

# Try to extract
7z x ClawdBot-Installer.exe
# Can extract, but code is obfuscated

# Try to debug
# Should be detected and blocked
```

**Test with tools:**
- **PEiD** - Check packer/compiler
- **Detect It Easy** - Identify protections
- **IDA Pro / Ghidra** - Attempt disassembly
- **x64dbg** - Try debugging

#### 3. Antivirus Testing

Test with multiple AV engines:

```powershell
# VirusTotal
# Upload to https://www.virustotal.com/

# Local testing
Windows Defender Scan
Malwarebytes
Kaspersky
```

**If false positives:**
- Add code signing certificate
- Submit to AV vendors for whitelisting
- Reduce obfuscation level

### Comparison with Other Methods

| Method | Protection | Size | Build Time | Pros | Cons |
|--------|-----------|------|------------|------|------|
| **PyInstaller** | Low | 15 MB | 30s | Fast, simple | Easy to decompile |
| **PyInstaller + PyArmor** | High | 18 MB | 2m | Good protection | Slower |
| **Nuitka** | Medium | 12 MB | 5m | Fast execution | Less obfuscation |
| **Cython** | Medium-High | 10 MB | 10m | Very fast | Complex build |
| **pkg (JS)** | Low | 40 MB | 1m | Easy | Large size |
| **pkg + Obfuscator** | Medium-High | 42 MB | 3m | Good JS protection | Large size |

### Distribution

#### 1. GitHub Releases

```powershell
# Create release
gh release create v2026.1.25 `
    dist-protected/ClawdBot-Installer-v2026.1.25.exe `
    dist-protected/CHECKSUMS.txt `
    --title "Clawdbot v2026.1.25" `
    --notes "Release notes"
```

#### 2. Direct Download

```html
<a href="https://clawd.bot/downloads/ClawdBot-Installer.exe">
  Download ClawdBot Installer (18 MB)
</a>
```

#### 3. Auto-Update

Implement update check in installer:

```python
import requests
import json

def check_for_updates():
    """Check GitHub for newer version"""
    url = "https://api.github.com/repos/clawdbot/clawdbot/releases/latest"
    response = requests.get(url)
    
    if response.status_code == 200:
        latest = response.json()['tag_name']
        current = "v2026.1.25"
        
        if latest > current:
            return True, latest
    
    return False, None
```

### Troubleshooting

#### Build Errors

**PyArmor license error:**
```powershell
# Register (free for personal use)
pyarmor register
```

**UPX not found:**
```powershell
# Download and add to PATH
# Or specify path in build script
```

**Import errors in built exe:**
```powershell
# Add hidden imports
pyinstaller --hidden-import=<module> ...
```

#### Runtime Errors

**DLL missing:**
```powershell
# Include DLLs
pyinstaller --add-binary="path/to/dll;." ...
```

**Permission denied:**
- Run as administrator
- Check antivirus
- Disable Windows SmartScreen temporarily

### Best Practices

1. **Always test on clean VM** before distribution
2. **Keep obfuscation keys secret** - don't commit to Git
3. **Use different keys per version** for better security
4. **Sign with valid certificate** in production
5. **Monitor AV false positives** and submit whitelisting
6. **Version everything** consistently
7. **Provide checksums** (SHA256) for verification
8. **Keep build scripts** in private repo if containing secrets
9. **Regular security updates** - obfuscation improves over time
10. **Document build process** for reproducibility

---

## Legal & Ethical Considerations

⚖️ **Important:** Code obfuscation is legal when:
- You own the code
- You're protecting intellectual property
- Not violating license terms
- Not hiding malicious behavior

❌ **Do NOT use obfuscation to:**
- Hide malware or viruses
- Bypass security software
- Violate software licenses
- Steal credentials or data

✅ **Legitimate uses:**
- Protect proprietary algorithms
- Prevent casual reverse engineering
- Secure API keys in binary
- Commercial software protection

---

## FAQ

**Q: ทำไมต้อง obfuscate?**
A: ป้องกันการ reverse engineer, ปกป้อง intellectual property, และซ่อน sensitive data (API keys)

**Q: Obfuscation ปลอดภัย 100% ไหม?**
A: ไม่มีอะไรปลอดภัย 100% แต่ทำให้ยากมากขึ้นสำหรับผู้โจมตีทั่วไป

**Q: ใช้เวลา build นานไหม?**
A: ~2-5 นาที ขึ้นอยู่กับ protection level

**Q: ขนาดไฟล์ใหญ่ขึ้นเยอะไหม?**
A: เพิ่มขึ้น ~20% จาก base installer

**Q: มี false positive จาก antivirus ไหม?**
A: อาจมีบ้าง แก้ด้วย code signing + whitelist submission

**Q: รองรับ Linux/Mac ไหม?**
A: ได้! เปลี่ยน target platform ใน build script

---

## macOS Installation

### สำหรับผู้ใช้งาน macOS

#### ติดตั้งจาก DMG (แนะนำ)

1. ดาวน์โหลด `ClawdBot-Installer-v2026.1.25.dmg`
2. Double-click เพื่อ mount
3. ลาก Clawdbot Installer.app ไปที่ Applications
4. เปิด Clawdbot Installer จาก Applications
5. ทำตาม Setup Wizard

#### ติดตั้งจาก PKG

```bash
# Double-click หรือใช้ command line
sudo installer -pkg ClawdBot-Installer-v2026.1.25.pkg -target /
```

#### ติดตั้งจาก Python Script

```bash
# ดาวน์โหลด script
curl -O https://clawd.bot/setup-wizard-gui-mac.py

# รัน
python3 setup-wizard-gui-mac.py
```

### สำหรับ Developers (macOS)

#### ข้อกำหนด

- macOS 11.0 (Big Sur) หรือสูงกว่า
- Python 3.8+
- Xcode Command Line Tools
- Homebrew (แนะนำ)

#### ติดตั้ง Dependencies

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python packages
pip3 install pyinstaller pyarmor pyminifier

# Install command line tools
xcode-select --install
```

#### สร้าง Protected Installer

```bash
# Make script executable
chmod +x scripts/build-protected-installer-mac.sh

# Build (no code signing)
./scripts/build-protected-installer-mac.sh

# Build with specific version
./scripts/build-protected-installer-mac.sh 2026.2.1

# Build with code signing
export SIGN_IDENTITY="Developer ID Application: Your Name (TEAMID)"
./scripts/build-protected-installer-mac.sh
```

#### Output Files

```
dist-protected-mac/
├── Clawdbot Installer.app     # App bundle
├── ClawdBot-Installer-v2026.1.25.dmg  # DMG installer
├── ClawdBot-Installer-v2026.1.25.pkg  # PKG installer
└── CHECKSUMS.txt              # SHA256 checksums
```

### macOS-Specific Features

#### 1. App Bundle (.app)

```bash
# Created in /Applications
open "/Applications/Clawdbot Installer.app"

# Structure:
Clawdbot Installer.app/
├── Contents/
│   ├── Info.plist
│   ├── MacOS/
│   │   └── clawdbot (executable)
│   └── Resources/
```

#### 2. LaunchAgent (Auto-start)

Installer สร้าง LaunchAgent plist:

```xml
<!-- ~/Library/LaunchAgents/bot.clawd.gateway.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>bot.clawd.gateway</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/pnpm</string>
        <string>clawdbot</string>
        <string>gateway</string>
        <string>run</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

จัดการ LaunchAgent:

```bash
# Load (start)
launchctl load ~/Library/LaunchAgents/bot.clawd.gateway.plist

# Unload (stop)
launchctl unload ~/Library/LaunchAgents/bot.clawd.gateway.plist

# Check status
launchctl list | grep clawd
```

#### 3. Dock Integration

Installer เพิ่ม icon ไปที่ Dock อัตโนมัติ

Remove manually:

```bash
# Right-click icon in Dock → Options → Remove from Dock
```

### Code Signing & Notarization

#### Get Developer Certificate

1. Enroll in Apple Developer Program ($99/year)
2. Create certificates in Xcode or Developer Portal
3. Download and install certificate

#### Find Your Signing Identity

```bash
# List all code signing identities
security find-identity -v -p codesigning

# Should show something like:
# 1) ABC123... "Developer ID Application: Your Name (TEAMID)"
```

#### Sign Application

```bash
# Sign app bundle
codesign --force --deep --sign "Developer ID Application: Your Name (TEAMID)" \
    --options runtime \
    "dist-protected-mac/Clawdbot Installer.app"

# Verify signature
codesign -vvv --deep --strict "dist-protected-mac/Clawdbot Installer.app"

# Check what's signed
codesign -d --entitlements - "dist-protected-mac/Clawdbot Installer.app"
```

#### Sign DMG and PKG

```bash
# Sign DMG
codesign --force --sign "Developer ID Application: Your Name (TEAMID)" \
    "dist-protected-mac/ClawdBot-Installer-v2026.1.25.dmg"

# Sign PKG
productsign --sign "Developer ID Installer: Your Name (TEAMID)" \
    "dist-protected-mac/ClawdBot-Installer-v2026.1.25.pkg" \
    "dist-protected-mac/ClawdBot-Installer-v2026.1.25-signed.pkg"
```

#### Notarize with Apple

ป้องกัน Gatekeeper warnings:

```bash
# Step 1: Store credentials (one-time setup)
xcrun notarytool store-credentials "AC_PASSWORD" \
    --apple-id "your@email.com" \
    --team-id "TEAMID" \
    --password "app-specific-password"

# Step 2: Submit for notarization
xcrun notarytool submit "dist-protected-mac/ClawdBot-Installer-v2026.1.25.dmg" \
    --keychain-profile "AC_PASSWORD" \
    --wait

# Step 3: Check status
xcrun notarytool log <submission-id> --keychain-profile "AC_PASSWORD"

# Step 4: Staple notarization ticket
xcrun stapler staple "dist-protected-mac/ClawdBot-Installer-v2026.1.25.dmg"

# Step 5: Verify
xcrun stapler validate "dist-protected-mac/ClawdBot-Installer-v2026.1.25.dmg"
spctl -a -t open --context context:primary-signature -v \
    "dist-protected-mac/Clawdbot Installer.app"
```

### Universal Binary (Intel + Apple Silicon)

Build script สร้าง universal binary อัตโนมัติ:

```bash
# Check architecture
lipo -info "dist-protected-mac/Clawdbot Installer.app/Contents/MacOS/clawdbot"

# Should show: x86_64 arm64
```

### Homebrew Distribution (Optional)

สร้าง Homebrew Cask:

```ruby
# clawdbot.rb
cask "clawdbot" do
  version "2026.1.25"
  sha256 "checksum_here"

  url "https://clawd.bot/downloads/ClawdBot-Installer-v#{version}.dmg"
  name "Clawdbot Installer"
  desc "WhatsApp gateway with AI capabilities"
  homepage "https://clawd.bot"

  app "Clawdbot Installer.app"

  zap trash: [
    "~/Library/Application Support/Clawdbot",
    "~/Library/Preferences/bot.clawd.installer.plist",
    "~/Library/Caches/Clawdbot",
    "~/.clawdbot",
  ]
end
```

Install:

```bash
brew install --cask clawdbot
```

### Troubleshooting macOS

#### "App is damaged and can't be opened"

```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine "/Applications/Clawdbot Installer.app"

# Or for DMG
xattr -d com.apple.quarantine "ClawdBot-Installer-v2026.1.25.dmg"
```

#### Gatekeeper Issues

```bash
# Check Gatekeeper status
spctl --status

# Allow app temporarily
xattr -cr "/Applications/Clawdbot Installer.app"

# Or disable Gatekeeper (not recommended)
sudo spctl --master-disable
```

#### Permission Denied

```bash
# Fix permissions
chmod +x "/Applications/Clawdbot Installer.app/Contents/MacOS/clawdbot"

# Or use installer
sudo installer -pkg ClawdBot-Installer-v2026.1.25.pkg -target /
```

#### LaunchAgent Not Starting

```bash
# Check logs
tail -f ~/Library/Logs/bot.clawd.gateway.log

# Reload
launchctl unload ~/Library/LaunchAgents/bot.clawd.gateway.plist
launchctl load ~/Library/LaunchAgents/bot.clawd.gateway.plist

# Debug
launchctl error 125  # Get error description
```

### macOS Protection Comparison

| Feature | Windows | macOS |
|---------|---------|-------|
| Code Obfuscation | PyArmor | PyArmor |
| Code Signing | Authenticode | Developer ID |
| Notarization | N/A | Apple Notary |
| App Format | .exe | .app bundle |
| Installer | .msi/.exe | .dmg/.pkg |
| Auto-update | ClickOnce | Sparkle |
| Sandboxing | Optional | Required for App Store |

### Best Practices (macOS)

1. **Always code sign** for distribution
2. **Notarize** to avoid Gatekeeper warnings
3. **Test on both** Intel and Apple Silicon
4. **Use universal binaries** when possible
5. **Follow Apple guidelines** strictly
6. **Provide DMG and PKG** options
7. **Include uninstaller** or zap in Homebrew Cask
8. **Test Gatekeeper** on clean macOS install
9. **Document permissions** needed
10. **Keep Developer ID** certificate current

---

## Resources

- **PyArmor**: https://pyarmor.readthedocs.io/
- **PyInstaller**: https://pyinstaller.org/
- **JavaScript Obfuscator**: https://obfuscator.io/
- **UPX**: https://upx.github.io/
- **Code Signing (Windows)**: https://docs.microsoft.com/en-us/windows/win32/seccrypto/signtool
- **Code Signing (macOS)**: https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution
- **Apple Notarization**: https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution
- **Homebrew Cask**: https://docs.brew.sh/Cask-Cookbook

---

License: Same as Clawdbot project
