# คู่มือการติดตั้ง Clawdbot

## ข้อกำหนดของระบบ

### ซอฟต์แวร์ที่จำเป็น
- **Node.js** เวอร์ชัน 22 หรือสูงกว่า
- **pnpm** (แนะนำ) หรือ npm
- **Git** สำหรับ clone repository

### สำหรับ Windows
- PowerShell 5.1 หรือสูงกว่า
- Visual Studio Build Tools (สำหรับ compile native modules)

---

## วิธีการติดตั้ง

### 1. ติดตั้ง Node.js และ pnpm

#### ติดตั้ง Node.js
ดาวน์โหลดและติดตั้งจาก: https://nodejs.org/ (เลือก LTS version)

ตรวจสอบการติดตั้ง:
```powershell
node --version
```

#### ติดตั้ง pnpm
```powershell
npm install -g pnpm
```

ตรวจสอบการติดตั้ง:
```powershell
pnpm --version
```

### 2. Clone Repository

```powershell
git clone <repository-url>
cd clawdbot
```

### 3. ติดตั้ง Dependencies

```powershell
pnpm install
```

คำสั่งนี้จะติดตั้ง dependencies ทั้งหมดที่จำเป็น รวมถึง:
- TypeScript และ dev tools
- Framework libraries
- Plugin dependencies

### 4. Build โปรเจค

```powershell
pnpm build
```

คำสั่งนี้จะทำการ:
- Bundle canvas A2UI components
- Compile TypeScript เป็น JavaScript
- Copy จำเป็นไฟล์ไปยัง `dist/` directory
- สร้าง build metadata

---

## การรัน Clawdbot

### รันในโหมด Development

#### Gateway Mode (แนะนำสำหรับพัฒนา)
```powershell
# รัน gateway พร้อม auto-reload
pnpm gateway:watch

# หรือรัน gateway แบบข้าม channels (เร็วกว่า)
$env:CLAWDBOT_SKIP_CHANNELS=1; pnpm dev gateway --dev
```

#### CLI Mode
```powershell
# รัน CLI โดยตรง
pnpm dev

# หรือใช้ clawdbot command
pnpm clawdbot <command>
```

### รันในโหมด Production

หลังจาก build เสร็จแล้ว:
```powershell
node dist/entry.js gateway run
```

---

## การตั้งค่า (Configuration)

### ไฟล์ Config หลัก
Clawdbot ใช้ไฟล์ config ที่อยู่ในตำแหน่ง:
```
%USERPROFILE%\.clawdbot\config.json
```

### ตั้งค่าผ่าน CLI
```powershell
# ดู config ปัจจุบัน
pnpm clawdbot config list

# ตั้งค่า gateway mode
pnpm clawdbot config set gateway.mode local

# ตั้งค่า provider
pnpm clawdbot config set provider.name <provider-name>
```

---

## การแก้ปัญหาเบื้องต้น

### ปัญหา: Environment Variable ไม่ทำงานใน PowerShell
**วิธีแก้:**
```powershell
# ใช้ไวยากรณ์ PowerShell
$env:VARIABLE_NAME="value"; pnpm command

# หรือตั้งค่าถาวร
[System.Environment]::SetEnvironmentVariable('VARIABLE_NAME', 'value', 'User')
```

### ปัญหา: Build ล้มเหลว
**วิธีแก้:**
```powershell
# ลบ node_modules และ dist
Remove-Item -Recurse -Force node_modules, dist

# ติดตั้งใหม่
pnpm install
pnpm build
```

### ปัญหา: Gateway ไม่เริ่มทำงาน
**วิธีแก้:**
```powershell
# ตรวจสอบว่า port ถูกใช้งานหรือไม่
netstat -ano | findstr :18789

# Kill process ที่ใช้ port (ถ้ามี)
Stop-Process -Id <PID> -Force
```

### ปัญหา: TypeScript Compilation Error
**วิธีแก้:**
```powershell
# Clear TypeScript cache
Remove-Item -Recurse -Force dist

# Build ใหม่
npx tsc -p tsconfig.json
```

---

## การทดสอบ

### รัน Unit Tests
```powershell
pnpm test
```

### รัน Tests พร้อม Coverage
```powershell
pnpm test:coverage
```

### รัน Live Tests (ต้องการ API keys)
```powershell
$env:CLAWDBOT_LIVE_TEST=1; pnpm test:live
```

---

## การ Lint และ Format Code

### ตรวจสอบ Code Style
```powershell
# Lint
pnpm lint

# Format check
pnpm format
```

### แก้ไข Code Style อัตโนมัติ
```powershell
# Fix lint issues
pnpm lint:fix

# Format code
pnpm format:fix
```

---

## โครงสร้างไดเรกทอรีสำคัญ

```
clawdbot/
├── src/              # Source code
│   ├── cli/          # CLI commands
│   ├── gateway/      # Gateway server
│   ├── channels/     # Messaging channels
│   ├── providers/    # AI providers
│   └── ...
├── dist/             # Compiled output
├── docs/             # Documentation
├── apps/             # Mobile/Desktop apps
│   ├── android/
│   ├── ios/
│   └── macos/
├── extensions/       # Plugin extensions
├── scripts/          # Build and utility scripts
└── test/             # Test files
```

---

## ข้อมูลเพิ่มเติม

- **เวอร์ชันปัจจุบัน:** 2026.1.25
- **Repository:** https://github.com/clawdbot/clawdbot
- **เอกสารเพิ่มเติม:** https://docs.clawd.bot

---

## การติดตั้งบน Platform อื่นๆ

### macOS
```bash
# ใช้ Homebrew (if available)
brew install clawdbot

# หรือ install globally ด้วย npm
npm install -g clawdbot
```

### Linux
```bash
# Install globally
npm install -g clawdbot

# หรือใช้ install script
curl -fsSL https://clawd.bot/install.sh | sh
```

---

## License
ดูรายละเอียดใน LICENSE file
