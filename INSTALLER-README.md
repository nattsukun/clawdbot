# Clawdbot Installer Documentation

## สำหรับผู้ใช้งาน (Users)

### วิธีติดตั้งแบบ Setup Wizard

#### Windows (PowerShell)
```powershell
# ดาวน์โหลด setup wizard script
# จากนั้นรัน:
.\scripts\setup-wizard.ps1
```

#### Cross-platform (Node.js)
```bash
# ต้องมี Node.js ติดตั้งอยู่แล้ว
node scripts/setup-wizard.mjs
```

### คุณสมบัติของ Setup Wizard

Setup Wizard จะนำคุณผ่านขั้นตอนต่อไปนี้:

1. **ตรวจสอบ Prerequisites**
   - Node.js (version 22+)
   - pnpm package manager
   - Git (optional)

2. **เลือกประเภทการติดตั้ง**
   - ติดตั้งจาก directory ปัจจุบัน (development)
   - ติดตั้งแบบ global จาก npm
   - Clone repository แล้วติดตั้ง

3. **ตั้งค่าเบื้องต้น**
   - Gateway mode (local/remote)
   - AI Provider (OpenAI, Anthropic, Google)
   - Log level
   - API keys

4. **สร้าง Shortcuts**
   - PowerShell profile shortcuts
   - Desktop shortcuts
   - Shell aliases

5. **เสร็จสิ้น**
   - เริ่มต้น gateway ทันที (optional)
   - แสดงคำสั่งที่มีประโยชน์

### Shortcuts ที่ถูกสร้าง

หลังจากติดตั้งเสร็จ คุณจะได้ shortcuts เหล่านี้:

- `clawdbot` - รันคำสั่ง clawdbot
- `clawdbot-start` - เริ่มต้น gateway
- `clawdbot-status` - ตรวจสอบสถานะ channels
- `clawdbot-logs` - ดู logs แบบ real-time
- `cb` - alias สำหรับ clawdbot

---

## สำหรับ Developers

### การสร้าง Installer

#### 1. PowerShell Setup Wizard
Setup wizard สำหรับ Windows ที่ใช้ PowerShell:

```powershell
# รันโดยตรง
.\scripts\setup-wizard.ps1

# หรือส่งต่อให้ผู้อื่นรัน
# แชร์ไฟล์ setup-wizard.ps1
```

**คุณสมบัติ:**
- Interactive UI สีสัน
- ตรวจสอบ prerequisites อัตโนมัติ
- ติดตั้ง dependencies ที่ขาด
- สร้าง PowerShell profile shortcuts
- สร้าง desktop shortcut

#### 2. Node.js Setup Wizard
Setup wizard แบบ cross-platform:

```bash
# รันโดยตรง
node scripts/setup-wizard.mjs

# ทำให้ executable ได้ (Linux/Mac)
chmod +x scripts/setup-wizard.mjs
./scripts/setup-wizard.mjs
```

**คุณสมบัติ:**
- ทำงานได้ทุก platform (Windows, Linux, macOS)
- Interactive UI
- รองรับ shell configuration (bash, zsh)

#### 3. Build Standalone Executable

สร้าง `.exe` installer ด้วย `pkg`:

```powershell
# Build สำหรับ Windows ปัจจุบัน
.\scripts\build-installer.ps1

# Build สำหรับทุก platform
.\scripts\build-installer.ps1 -BuildAll

# ระบุ version และ output directory
.\scripts\build-installer.ps1 -Version "2026.1.25" -OutputDir "release"
```

**Output files:**
- `clawdbot-installer.exe` - Standalone installer สำหรับ Windows
- `clawdbot-installer.iss` - Inno Setup script (สำหรับ advanced installer)
- `clawdbot-installer.nsi` - NSIS script (alternative)

### การสร้าง Advanced Installer

#### ใช้ Inno Setup (แนะนำ)

1. ดาวน์โหลด Inno Setup: https://jrsoftware.org/isinfo.php
2. Build base installer ก่อน:
   ```powershell
   .\scripts\build-installer.ps1
   ```
3. เปิด Inno Setup Compiler
4. Load script: `dist-installer/clawdbot-installer.iss`
5. Compile

**ผลลัพธ์:**
- Installer ที่สมบูรณ์พร้อม wizard UI
- รองรับ uninstaller
- Registry entries
- Start menu shortcuts
- Desktop icon

#### ใช้ NSIS (Alternative)

1. ดาวน์โหลด NSIS: https://nsis.sourceforge.io/
2. Build base installer
3. Compile script: `dist-installer/clawdbot-installer.nsi`

### โครงสร้างไฟล์

```
scripts/
├── setup-wizard.ps1          # PowerShell setup wizard
├── setup-wizard.mjs          # Node.js setup wizard
├── build-installer.ps1       # Build standalone installer
└── installer-entry.mjs       # Entry point (generated)

dist-installer/               # Output directory (generated)
├── clawdbot-installer.exe    # Standalone executable
├── clawdbot-installer.iss    # Inno Setup script
└── clawdbot-installer.nsi    # NSIS script
```

### ปรับแต่ง Setup Wizard

#### แก้ไข PowerShell Wizard

แก้ไขไฟล์ `scripts/setup-wizard.ps1`:

```powershell
# เปลี่ยนค่า default
$defaultGatewayMode = "local"
$defaultLogLevel = "info"

# เพิ่มขั้นตอนใหม่
Write-Header "Step X: Custom Step"
# ... your code
```

#### แก้ไข Node.js Wizard

แก้ไขไฟล์ `scripts/setup-wizard.mjs`:

```javascript
// เพิ่ม provider ใหม่
const providers = ['openai', 'anthropic', 'google', 'custom'];

// เปลี่ยนสี
const colors = {
  // ... custom colors
};
```

#### แก้ไข Build Script

แก้ไขไฟล์ `scripts/build-installer.ps1`:

```powershell
# เปลี่ยน default version
param(
    [string]$Version = "2026.2.1",  # <-- เปลี่ยนตรงนี้
    ...
)

# เพิ่ม target platform
pkg scripts/installer-entry.mjs --target node22-linux-arm64 --output ...
```

### การทดสอบ Installer

#### ทดสอบ Setup Wizard

```powershell
# ทดสอบบน Windows
.\scripts\setup-wizard.ps1

# ทดสอบบน Linux/Mac
node scripts/setup-wizard.mjs

# ทดสอบแบบ dry-run (ไม่ติดตั้งจริง)
# แก้ไข script เพิ่ม -WhatIf หรือ --dry-run flag
```

#### ทดสอบ Standalone Installer

```powershell
# Build
.\scripts\build-installer.ps1

# รัน
.\dist-installer\clawdbot-installer.exe

# ทดสอบบน VM หรือ clean environment
```

#### ทดสอบ Advanced Installer

```powershell
# Build Inno Setup installer
# Compile ด้วย Inno Setup Compiler

# ทดสอบ silent install
.\clawdbot-setup-2026.1.25.exe /SILENT

# ทดสอบ very silent install
.\clawdbot-setup-2026.1.25.exe /VERYSILENT

# ทดสอบ uninstall
.\unins000.exe /SILENT
```

### CI/CD Integration

#### GitHub Actions Example

```yaml
name: Build Installer

on:
  release:
    types: [created]

jobs:
  build:
    runs-on: windows-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '22'
      
      - name: Install pnpm
        run: npm install -g pnpm
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Build project
        run: pnpm build
      
      - name: Build installer
        run: .\scripts\build-installer.ps1 -BuildAll
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: installers
          path: dist-installer/clawdbot-installer*.exe
```

### การแจกจ่าย (Distribution)

#### 1. GitHub Releases

```powershell
# สร้าง release และ upload installer
gh release create v2026.1.25 `
  dist-installer/clawdbot-installer.exe `
  dist-installer/clawdbot-setup-2026.1.25.exe `
  --title "Clawdbot v2026.1.25" `
  --notes "Release notes here"
```

#### 2. Website Download

```html
<!-- Download page -->
<a href="https://clawd.bot/downloads/clawdbot-installer.exe">
  Download Clawdbot for Windows
</a>
```

#### 3. Package Managers

```powershell
# Chocolatey (Windows)
choco install clawdbot

# Scoop (Windows)
scoop install clawdbot

# Homebrew (macOS)
brew install clawdbot
```

### Code Signing (Optional)

สำหรับ production installer ควร sign code:

```powershell
# ใช้ signtool (Windows SDK)
signtool sign /f cert.pfx /p password /t http://timestamp.digicert.com dist-installer/clawdbot-installer.exe

# หรือใช้ SignPath (CI/CD)
# https://about.signpath.io/
```

### Tips & Best Practices

1. **Always test on clean environment** - ใช้ VM หรือ Docker
2. **Version everything** - installer, script, package
3. **Log installation process** - เก็บ log สำหรับ debug
4. **Provide uninstall** - ต้องมี uninstaller เสมอ
5. **Check prerequisites early** - ตรวจสอบก่อนเริ่มติดตั้ง
6. **Graceful failure** - แสดง error message ที่ชัดเจน
7. **Silent mode support** - รองรับ `/SILENT` flag
8. **Update mechanism** - วางแผนสำหรับ auto-update

### Troubleshooting

#### Installer ไม่รัน

```powershell
# ตรวจสอบ execution policy
Get-ExecutionPolicy

# อนุญาต script
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### pkg build ล้มเหลว

```powershell
# ติดตั้ง pkg version ล่าสุด
npm install -g pkg@latest

# ใช้ Node.js version ที่รองรับ
nvm use 22
```

#### Missing dependencies

```powershell
# ติดตั้ง dependencies ใหม่
Remove-Item -Recurse node_modules
pnpm install
```

---

## FAQ

**Q: สามารถสร้าง installer สำหรับ macOS ได้ไหม?**

A: ได้! ใช้ `build-installer.ps1 -BuildAll` แล้วสร้าง `.app` bundle หรือ `.pkg` ด้วย:
- `pkgbuild` และ `productbuild` (built-in macOS)
- `electron-builder` (สำหรับ Electron apps)
- `create-dmg` (สำหรับ DMG files)

**Q: Installer มีขนาดใหญ่มากทำไง?**

A: pkg bundle ทั้ง Node.js runtime เข้าไป ถ้าต้องการเล็กกว่านี้:
- ใช้ `nexe` แทน `pkg`
- แยก dependencies ออก
- ใช้ external Node.js (require Node.js pre-installed)

**Q: สามารถ auto-update ได้ไหม?**

A: ได้! เพิ่ม update mechanism:
- ใช้ `electron-updater` (for Electron apps)
- ใช้ `pkg-updater` (custom solution)
- Check GitHub releases API

**Q: มี virus/malware warning ทำไง?**

A: Code sign installer ด้วย valid certificate จาก:
- DigiCert
- Sectigo
- GlobalSign

---

## License

Setup wizards และ installer scripts อยู่ภายใต้ license เดียวกับ Clawdbot project
