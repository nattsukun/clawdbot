# 📚 คู่มือ Clawdbot ฉบับสมบูรณ์

**เวอร์ชัน:** 2026.1.25  
**ภาษา:** ไทย  
**อัพเดทล่าสุด:** 1 กุมภาพันธ์ 2026

---

## 📑 สารบัญ

### ส่วนที่ 1: การติดตั้ง
- [1.1 ข้อกำหนดของระบบ](#11-ข้อกำหนดของระบบ)
- [1.2 การติดตั้งบน Windows](#12-การติดตั้งบน-windows)
- [1.3 การติดตั้งบน macOS](#13-การติดตั้งบน-macos)
- [1.4 การติดตั้งบน Linux](#14-การติดตั้งบน-linux)
- [1.5 Setup Wizard (แนะนำ)](#15-setup-wizard)

### ส่วนที่ 2: การใช้งานพื้นฐาน
- [2.1 การเริ่มต้นใช้งาน](#21-การเริ่มต้นใช้งาน)
- [2.2 คำสั่ง CLI หลัก](#22-คำสั่ง-cli-หลัก)
- [2.3 Gateway Server](#23-gateway-server)
- [2.4 Channels](#24-channels)

### ส่วนที่ 3: การใช้งานขั้นสูง
- [3.1 AI Providers](#31-ai-providers)
- [3.2 Agents & RPC](#32-agents--rpc)
- [3.3 Plugins](#33-plugins)
- [3.4 Automation & Hooks](#34-automation--hooks)

### ส่วนที่ 4: Protected Installer
- [4.1 การสร้าง Installer](#41-การสร้าง-installer)
- [4.2 Code Obfuscation](#42-code-obfuscation)
- [4.3 Code Signing](#43-code-signing)

### ส่วนที่ 5: การแก้ปัญหา
- [5.1 ปัญหาทั่วไป](#51-ปัญหาทั่วไป)
- [5.2 Debug & Logs](#52-debug--logs)
- [5.3 FAQ](#53-faq)

---

## ส่วนที่ 1: การติดตั้ง

### 1.1 ข้อกำหนดของระบบ

#### ระบบปฏิบัติการ
- **Windows:** 10/11 (64-bit)
- **macOS:** 11.0 (Big Sur) หรือสูงกว่า
- **Linux:** Ubuntu 20.04+, Debian 10+, CentOS 8+

#### ซอฟต์แวร์ที่จำเป็น
- **Node.js:** เวอร์ชัน 22 หรือสูงกว่า
- **pnpm:** Package manager (แนะนำ) หรือ npm
- **Git:** สำหรับ clone repository (optional)

#### ฮาร์ดแวร์แนะนำ
- **RAM:** 4 GB ขึ้นไป
- **Storage:** 2 GB available space
- **Network:** Internet connection

---

### 1.2 การติดตั้งบน Windows

#### วิธีที่ 1: Setup Wizard (แนะนำ)

**ติดตั้ง Python Version:**
```powershell
# ดาวน์โหลด setup wizard
curl -O https://clawd.bot/setup-wizard-gui.py

# รัน
python setup-wizard-gui.py
```

**ติดตั้ง PowerShell Version:**
```powershell
# ดาวน์โหลด
curl -O https://clawd.bot/setup-wizard.ps1

# รัน
.\setup-wizard.ps1
```

#### วิธีที่ 2: ติดตั้งด้วยมือ

**ขั้นตอนที่ 1: ติดตั้ง Node.js**
```powershell
# ดาวน์โหลดจาก
https://nodejs.org/

# หรือใช้ winget
winget install OpenJS.NodeJS

# ตรวจสอบ
node --version
```

**ขั้นตอนที่ 2: ติดตั้ง pnpm**
```powershell
npm install -g pnpm
pnpm --version
```

**ขั้นตอนที่ 3: Clone Repository**
```powershell
git clone https://github.com/clawdbot/clawdbot.git
cd clawdbot
```

**ขั้นตอนที่ 4: ติดตั้ง Dependencies**
```powershell
pnpm install
```

**ขั้นตอนที่ 5: Build**
```powershell
pnpm build
```

**ขั้นตอนที่ 6: ตั้งค่าเบื้องต้น**
```powershell
# ตั้งค่า gateway mode
pnpm clawdbot config set gateway.mode local

# ตั้งค่า log level
pnpm clawdbot config set logging.level info
```

#### วิธีที่ 3: Global Installation
```powershell
npm install -g clawdbot
clawdbot --version
```

---

### 1.3 การติดตั้งบน macOS

#### วิธีที่ 1: Setup Wizard (แนะนำ)

```bash
# ดาวน์โหลด
curl -O https://clawd.bot/setup-wizard-gui-mac.py

# รัน
python3 setup-wizard-gui-mac.py
```

#### วิธีที่ 2: Homebrew

```bash
# ติดตั้ง Homebrew (ถ้ายังไม่มี)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# ติดตั้ง Clawdbot
brew install clawdbot

# หรือใช้ Cask (สำหรับ GUI app)
brew install --cask clawdbot
```

#### วิธีที่ 3: ติดตั้งด้วยมือ

```bash
# ติดตั้ง Node.js
brew install node

# ติดตั้ง pnpm
npm install -g pnpm

# Clone repository
git clone https://github.com/clawdbot/clawdbot.git
cd clawdbot

# Install & Build
pnpm install
pnpm build

# Configure
pnpm clawdbot config set gateway.mode local
```

#### วิธีที่ 4: DMG Installer

1. ดาวน์โหลด `ClawdBot-Installer-v2026.1.25.dmg`
2. Double-click เพื่อ mount
3. ลาก Clawdbot ไปที่ Applications
4. เปิดจาก Applications folder

---

### 1.4 การติดตั้งบน Linux

#### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# ติดตั้ง Node.js
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# ติดตั้ง pnpm
npm install -g pnpm

# Clone & Install
git clone https://github.com/clawdbot/clawdbot.git
cd clawdbot
pnpm install
pnpm build
```

#### CentOS/RHEL

```bash
# ติดตั้ง Node.js
curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo bash -
sudo yum install -y nodejs

# ติดตั้ง pnpm
npm install -g pnpm

# Clone & Install
git clone https://github.com/clawdbot/clawdbot.git
cd clawdbot
pnpm install
pnpm build
```

#### Arch Linux

```bash
# ติดตั้ง Node.js
sudo pacman -S nodejs npm

# ติดตั้ง pnpm
npm install -g pnpm

# Clone & Install
git clone https://github.com/clawdbot/clawdbot.git
cd clawdbot
pnpm install
pnpm build
```

---

### 1.5 Setup Wizard

Setup Wizard ช่วยติดตั้งอัตโนมัติพร้อม GUI

#### คุณสมบัติ

✅ ตรวจสอบ prerequisites อัตโนมัติ  
✅ ติดตั้ง dependencies ที่ขาด  
✅ Configuration wizard  
✅ สร้าง shortcuts/aliases  
✅ Desktop shortcuts (Windows/macOS)  
✅ LaunchAgent (macOS)  

#### การใช้งาน

**Windows (PowerShell):**
```powershell
.\scripts\setup-wizard.ps1
```

**Windows (Python GUI):**
```powershell
python scripts\setup-wizard-gui.py
```

**macOS (Python GUI):**
```bash
python3 scripts/setup-wizard-gui-mac.py
```

**Cross-platform (Node.js):**
```bash
node scripts/setup-wizard.mjs
```

#### Shortcuts ที่ถูกสร้าง

หลังติดตั้งจะได้:
- `clawdbot` - รันคำสั่ง clawdbot
- `clawdbot-start` - เริ่ม gateway
- `clawdbot-status` - ตรวจสอบสถานะ
- `clawdbot-logs` - ดู logs
- `cb` - alias สำหรับ clawdbot

---

## ส่วนที่ 2: การใช้งานพื้นฐาน

### 2.1 การเริ่มต้นใช้งาน

#### ตรวจสอบการติดตั้ง

```bash
# ตรวจสอบ version
clawdbot --version
# หรือ
pnpm clawdbot --version

# ดู help
clawdbot --help
```

#### Login WhatsApp

```bash
# Login (จะแสดง QR code)
clawdbot login

# Login with specific profile
clawdbot login --profile production
```

#### เริ่ม Gateway

```bash
# Start gateway
clawdbot gateway run

# Start with custom port
clawdbot gateway run --port 3000

# Start with localhost binding only
clawdbot gateway run --bind loopback

# Force restart
clawdbot gateway run --force
```

---

### 2.2 คำสั่ง CLI หลัก

#### Config Management

```bash
# ดู config ทั้งหมด
clawdbot config list

# ดูแบบ JSON
clawdbot config list --json

# ตั้งค่า
clawdbot config set <key> <value>

# ตัวอย่าง
clawdbot config set gateway.mode local
clawdbot config set logging.level info
clawdbot config set provider.name openai

# ลบค่า
clawdbot config delete <key>

# Reset config
clawdbot config reset
```

#### Channels Management

```bash
# ดูสถานะ channels
clawdbot channels status

# ดูพร้อม probe (ทดสอบการเชื่อมต่อ)
clawdbot channels status --probe

# ดูทั้งหมด (รวมที่ปิดใช้งาน)
clawdbot channels status --all

# แสดงแบบ JSON
clawdbot channels status --json

# เปิดใช้งาน channel
clawdbot channels enable <channel>

# ตัวอย่าง
clawdbot channels enable telegram
clawdbot channels enable discord

# ปิดใช้งาน channel
clawdbot channels disable <channel>
```

#### Message Commands

```bash
# ส่งข้อความ
clawdbot message send --to <recipient> --message "Hello!"

# ส่งพร้อมไฟล์
clawdbot message send --to <recipient> --message "Check this" --file <path>

# ส่งผ่าน channel เฉพาะ
clawdbot message send --to <recipient> --message "Hi" --channel telegram

# ส่งหลายคน
clawdbot message send --to user1,user2,user3 --message "Broadcast"
```

#### Agent Commands

```bash
# รัน agent แบบ interactive
clawdbot agent

# ส่ง single message
clawdbot agent --message "What's the weather?"

# RPC mode
clawdbot agent --mode rpc --json

# ใช้ thinking mode
clawdbot agent --message "Complex task" --thinking high

# Thinking levels:
# - low: เร็ว, ง่าย
# - medium: สมดุล (default)
# - high: วิเคราะห์ลึก, ช้ากว่า
```

---

### 2.3 Gateway Server

Gateway เป็นตัวกลางที่ให้ remote access

#### การตั้งค่า Gateway

```bash
# ตั้งค่า mode
clawdbot config set gateway.mode local   # รันบนเครื่องนี้
clawdbot config set gateway.mode remote  # เชื่อมต่อ remote

# ตั้งค่า URL (สำหรับ remote)
clawdbot config set gateway.url "https://gateway.example.com"

# ตั้งค่า token
clawdbot config set gateway.token "your-secret-token"

# ตั้งค่า port
clawdbot config set gateway.port 18789
```

#### รัน Gateway

```bash
# รันแบบ production
clawdbot gateway run

# รันแบบ development (skip channels)
CLAWDBOT_SKIP_CHANNELS=1 clawdbot gateway --dev

# Windows PowerShell:
$env:CLAWDBOT_SKIP_CHANNELS=1; pnpm dev gateway --dev

# รันพร้อม watch mode (auto-reload)
pnpm gateway:watch

# Background (Linux/Mac)
nohup clawdbot gateway run > gateway.log 2>&1 &

# Background (Windows)
Start-Process -NoNewWindow powershell -ArgumentList "clawdbot gateway run"
```

#### ตรวจสอบ Gateway

```bash
# Linux/Mac
netstat -tuln | grep 18789
ss -ltnp | grep 18789

# Windows
netstat -ano | findstr :18789

# ตรวจสอบ process
# Linux/Mac
ps aux | grep clawdbot

# Windows
Get-Process | Where-Object {$_.ProcessName -like "*node*"}
```

#### ดู Logs

```bash
# Linux/Mac
tail -f ~/.clawdbot/logs/gateway.log

# Windows
Get-Content $env:USERPROFILE\.clawdbot\logs\gateway.log -Tail 50 -Wait

# ดู error logs
tail -f ~/.clawdbot/logs/gateway-error.log
```

---

### 2.4 Channels

Clawdbot รองรับหลาย messaging platforms

#### WhatsApp (Default)

```bash
# Login
clawdbot login

# ตรวจสอบสถานะ
clawdbot channels status --probe

# ส่งข้อความ
clawdbot message send --to "1234567890@s.whatsapp.net" --message "Hello"
```

#### Telegram

```bash
# ตั้งค่า bot token
clawdbot config set telegram.token "YOUR_BOT_TOKEN"

# เปิดใช้งาน
clawdbot channels enable telegram

# ตรวจสอบ
clawdbot channels status

# Configuration options:
# - telegram.token: Bot token จาก @BotFather
# - telegram.allowlist: รายชื่อผู้ใช้ที่อนุญาต (optional)
```

#### Discord

```bash
# ตั้งค่า bot token
clawdbot config set discord.token "YOUR_BOT_TOKEN"

# เปิดใช้งาน
clawdbot channels enable discord

# Configuration:
# - discord.token: Bot token จาก Discord Developer Portal
# - discord.clientId: Application ID
# - discord.guildId: Server ID (optional)
```

#### Slack

```bash
# ตั้งค่า credentials
clawdbot config set slack.token "YOUR_SLACK_TOKEN"
clawdbot config set slack.appToken "YOUR_APP_TOKEN"

# เปิดใช้งาน
clawdbot channels enable slack

# Configuration:
# - slack.token: Bot User OAuth Token
# - slack.appToken: App-Level Token
# - slack.signingSecret: Signing Secret
```

#### Signal

```bash
# ต้องมี Signal Desktop ติดตั้งอยู่

# เปิดใช้งาน
clawdbot channels enable signal

# ตั้งค่า phone number
clawdbot config set signal.phone "+1234567890"
```

#### iMessage (macOS only)

```bash
# เปิดใช้งาน
clawdbot channels enable imessage

# ต้องมี Messages app และ iCloud enabled
```

#### LINE

```bash
# ตั้งค่า
clawdbot config set line.channelSecret "YOUR_CHANNEL_SECRET"
clawdbot config set line.channelAccessToken "YOUR_ACCESS_TOKEN"

# เปิดใช้งาน
clawdbot channels enable line
```

---

## ส่วนที่ 3: การใช้งานขั้นสูง

### 3.1 AI Providers

#### OpenAI

```bash
# ตั้งค่า
clawdbot config set provider.name openai
clawdbot config set provider.apiKey "sk-..."
clawdbot config set provider.model "gpt-4"

# Options:
# - gpt-4
# - gpt-4-turbo
# - gpt-3.5-turbo

# Advanced settings:
clawdbot config set provider.temperature 0.7
clawdbot config set provider.maxTokens 2000
clawdbot config set provider.topP 1.0
```

#### Anthropic (Claude)

```bash
# ตั้งค่า
clawdbot config set provider.name anthropic
clawdbot config set provider.apiKey "sk-ant-..."
clawdbot config set provider.model "claude-3-opus-20240229"

# Models:
# - claude-3-opus-20240229 (most capable)
# - claude-3-sonnet-20240229 (balanced)
# - claude-3-haiku-20240307 (fast)
```

#### Google (Gemini)

```bash
# ตั้งค่า
clawdbot config set provider.name google
clawdbot config set provider.apiKey "AIza..."
clawdbot config set provider.model "gemini-pro"

# Models:
# - gemini-pro
# - gemini-pro-vision
```

#### Custom Provider

```bash
# ตั้งค่า custom endpoint
clawdbot config set provider.name custom
clawdbot config set provider.baseUrl "https://api.example.com"
clawdbot config set provider.apiKey "your-key"
```

---

### 3.2 Agents & RPC

#### Agent Modes

**Interactive Mode:**
```bash
clawdbot agent
# จะเข้าสู่โหมด chat
```

**Message Mode:**
```bash
clawdbot agent --message "Your question here"
```

**RPC Mode:**
```bash
# Output เป็น JSON
clawdbot agent --mode rpc --json
```

#### Thinking Modes

```bash
# Low (fast, simple)
clawdbot agent --message "What time is it?" --thinking low

# Medium (balanced) - default
clawdbot agent --message "Plan my day"

# High (deep analysis)
clawdbot agent --message "Solve complex problem" --thinking high
```

#### Agent Configuration

```bash
# ตั้งค่า default thinking
clawdbot config set agent.thinking medium

# ตั้งค่า timeout (milliseconds)
clawdbot config set agent.timeout 60000

# เปิด/ปิด streaming
clawdbot config set agent.streaming true

# System prompt
clawdbot config set agent.systemPrompt "You are a helpful assistant..."
```

---

### 3.3 Plugins

#### ดู Plugins ที่มี

```bash
# List all plugins
ls extensions/

# ตัวอย่าง plugins:
# - msteams/       # Microsoft Teams
# - matrix/        # Matrix protocol
# - zalo/          # Zalo messaging
# - voice-call/    # Voice calls
```

#### เปิดใช้งาน Plugin

```bash
# เปิดใช้
clawdbot config set plugins.entries.<plugin-name>.enabled true

# ตัวอย่าง
clawdbot config set plugins.entries.msteams.enabled true
clawdbot config set plugins.entries.matrix.enabled true
```

#### ติดตั้ง Plugin Dependencies

```bash
# เข้าไปยัง plugin directory
cd extensions/<plugin-name>

# ติดตั้ง dependencies
pnpm install --prod

# กลับไปยัง root
cd ../..

# Restart gateway
clawdbot gateway run --force
```

#### สร้าง Plugin ใหม่

```bash
# สร้าง plugin template
clawdbot plugin create my-plugin

# โครงสร้าง:
extensions/my-plugin/
├── package.json
├── src/
│   └── index.ts
├── README.md
└── tsconfig.json
```

---

### 3.4 Automation & Hooks

#### Hooks

Clawdbot รองรับ hooks สำหรับ automation

```javascript
// ~/.clawdbot/hooks/onMessage.js
module.exports = async (context) => {
  const { message, sender, reply } = context;
  
  // Auto-reply
  if (message.toLowerCase().includes('hello')) {
    await reply('Hello! How can I help you?');
  }
  
  // Forward to channel
  if (sender.isAdmin) {
    await context.forward('telegram', message);
  }
};
```

#### Cron Jobs

```bash
# ตั้งค่า cron jobs
clawdbot config set cron.enabled true
clawdbot config set cron.jobs '[
  {
    "schedule": "0 9 * * *",
    "command": "message send --to admin --message \"Daily report\""
  }
]'
```

#### Auto-Reply

```bash
# เปิดใช้งาน
clawdbot config set autoReply.enabled true

# ตั้งค่า rules
clawdbot config set autoReply.rules '[
  {
    "trigger": "hello|hi|hey",
    "response": "Hi there! 👋"
  },
  {
    "trigger": "bye|goodbye",
    "response": "Goodbye! See you later."
  }
]'
```

---

## ส่วนที่ 4: Protected Installer

### 4.1 การสร้าง Installer

#### Windows

```powershell
# ติดตั้ง tools
pip install pyinstaller pyarmor pyminifier
npm install -g javascript-obfuscator pkg

# Build protected installer
.\scripts\build-protected-installer.ps1

# Output: dist-protected/
# - ClawdBot-Installer-v2026.1.25.exe
# - ClawdBot-Installer-JS-v2026.1.25.exe
```

#### macOS

```bash
# ติดตั้ง tools
pip3 install pyinstaller pyarmor pyminifier

# Build
chmod +x scripts/build-protected-installer-mac.sh
./scripts/build-protected-installer-mac.sh

# Output: dist-protected-mac/
# - Clawdbot Installer.app
# - ClawdBot-Installer-v2026.1.25.dmg
# - ClawdBot-Installer-v2026.1.25.pkg
```

---

### 4.2 Code Obfuscation

#### Python (PyArmor)

```bash
# Obfuscate code
pyarmor obfuscate --exact --restrict 0 \
    --output scripts/obfuscated \
    scripts/setup-wizard-gui.py

# Features:
# ✓ Bytecode encryption
# ✓ String obfuscation
# ✓ Anti-decompiler
# ✓ Runtime decryption
```

#### JavaScript

```bash
# Obfuscate
javascript-obfuscator scripts/setup-wizard.mjs \
    --output scripts/setup-wizard.obf.mjs \
    --compact true \
    --control-flow-flattening true \
    --string-array-encoding rc4 \
    --self-defending true

# Features:
# ✓ String encryption (RC4)
# ✓ Control flow flattening
# ✓ Dead code injection
# ✓ Debug protection
```

---

### 4.3 Code Signing

#### Windows

```powershell
# สร้าง self-signed cert (dev)
$cert = New-SelfSignedCertificate `
    -Type CodeSigningCert `
    -Subject "CN=Clawdbot" `
    -CertStoreLocation Cert:\CurrentUser\My

# Export
$password = ConvertTo-SecureString -String "password" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath cert.pfx -Password $password

# Sign
$cert = Get-PfxCertificate -FilePath cert.pfx
Set-AuthenticodeSignature -FilePath installer.exe -Certificate $cert
```

#### macOS

```bash
# หา signing identity
security find-identity -v -p codesigning

# Sign app
codesign --force --deep --sign "Developer ID Application: Your Name" \
    --options runtime \
    "Clawdbot Installer.app"

# Verify
codesign -vvv --deep --strict "Clawdbot Installer.app"

# Notarize
xcrun notarytool submit installer.dmg \
    --keychain-profile "AC_PASSWORD" \
    --wait

# Staple
xcrun stapler staple installer.dmg
```

---

## ส่วนที่ 5: การแก้ปัญหา

### 5.1 ปัญหาทั่วไป

#### Gateway ไม่เริ่มทำงาน

**Windows:**
```powershell
# ตรวจสอบ port
netstat -ano | findstr :18789

# Kill process
Stop-Process -Id <PID> -Force

# Start ใหม่
clawdbot gateway run --force
```

**macOS/Linux:**
```bash
# ตรวจสอบ port
lsof -i :18789

# Kill process
kill -9 <PID>

# Start ใหม่
clawdbot gateway run --force
```

#### WhatsApp Disconnected

```bash
# Login ใหม่
clawdbot login

# ตรวจสอบ session
ls ~/.clawdbot/sessions/

# ลบ session เก่า
rm -rf ~/.clawdbot/sessions/*

# Login again
clawdbot login
```

#### Config ไม่ทำงาน

```bash
# ดู config ปัจจุบัน
clawdbot config list

# Reset config
clawdbot config reset

# ตั้งค่าใหม่
clawdbot config set <key> <value>
```

#### Build ล้มเหลว

```bash
# ลบ node_modules และ dist
rm -rf node_modules dist

# Install ใหม่
pnpm install

# Build
pnpm build
```

#### Dependencies Error

```bash
# Clear cache
pnpm store prune

# Remove lock file
rm pnpm-lock.yaml

# Install again
pnpm install
```

---

### 5.2 Debug & Logs

#### เปิด Debug Mode

```bash
# ตั้งค่า log level
clawdbot config set logging.level debug

# หรือใช้ environment variable
export CLAWDBOT_LOG_LEVEL=debug  # Linux/Mac
$env:CLAWDBOT_LOG_LEVEL="debug"  # Windows

# รัน gateway
clawdbot gateway run
```

#### ดู Logs

```bash
# Gateway logs
tail -f ~/.clawdbot/logs/gateway.log

# Error logs
tail -f ~/.clawdbot/logs/gateway-error.log

# Agent logs
tail -f ~/.clawdbot/logs/agent.log

# Windows:
Get-Content $env:USERPROFILE\.clawdbot\logs\*.log -Tail 50 -Wait
```

#### Export Logs

```bash
# Export all logs
tar -czf clawdbot-logs.tar.gz ~/.clawdbot/logs/

# Windows:
Compress-Archive -Path $env:USERPROFILE\.clawdbot\logs\* -DestinationPath clawdbot-logs.zip
```

#### Run Doctor

```bash
# ตรวจสอบระบบ
clawdbot doctor

# จะตรวจสอบ:
# - Node.js version
# - Dependencies
# - Configuration
# - Permissions
# - Network
```

---

### 5.3 FAQ

**Q: รองรับภาษาไทยไหม?**
A: ใช่! Clawdbot รองรับ UTF-8 ครบถ้วน

**Q: ใช้ RAM เท่าไหร่?**
A: ~200-500 MB ขึ้นอยู่กับ channels ที่เปิดใช้

**Q: รองรับกี่ channels พร้อมกัน?**
A: ไม่จำกัด แต่แนะนำไม่เกิน 10 channels เพื่อ performance

**Q: ปลอดภัยไหม?**
A: ใช่! Clawdbot ไม่ส่งข้อมูลออกนอกเครื่องคุณ (ยกเว้น AI providers)

**Q: ต้องใช้ API key เสมอไหม?**
A: ไม่! ถ้าไม่ใช้ AI features ก็ไม่ต้องใช้ API key

**Q: สามารถรันหลาย instance ได้ไหม?**
A: ได้! ใช้ `--profile` flag เพื่อแยก config

```bash
clawdbot gateway run --profile production
clawdbot gateway run --profile development --port 18790
```

**Q: Backup ข้อมูลยังไง?**
A: Backup folder `~/.clawdbot/`:

```bash
# Linux/Mac
tar -czf clawdbot-backup.tar.gz ~/.clawdbot/

# Windows
Compress-Archive -Path $env:USERPROFILE\.clawdbot -DestinationPath clawdbot-backup.zip
```

**Q: Update ยังไง?**
A: 

```bash
# ถ้าติดตั้งแบบ global
npm update -g clawdbot

# ถ้าติดตั้งแบบ local
cd clawdbot
git pull
pnpm install
pnpm build
```

**Q: Uninstall ยังไง?**
A:

```bash
# Global installation
npm uninstall -g clawdbot

# Remove config
rm -rf ~/.clawdbot/

# Windows
Remove-Item -Recurse -Force $env:USERPROFILE\.clawdbot
```

---

## 📞 การขอความช่วยเหลือ

### Documentation
- **Online:** https://docs.clawd.bot
- **Installation:** INSTALLATION-TH.md
- **User Guide:** USER-GUIDE-TH.md
- **Installer:** PROTECTED-INSTALLER-README.md

### Support
- **GitHub Issues:** https://github.com/clawdbot/clawdbot/issues
- **Discord:** https://discord.gg/clawdbot
- **Email:** support@clawd.bot

### Debug Information

เมื่อรายงานปัญหา โปรดแนบ:

```bash
# System info
clawdbot --version
node --version
pnpm --version

# Config
clawdbot config list --json

# Logs
clawdbot doctor
tail -n 100 ~/.clawdbot/logs/gateway-error.log
```

---

## 📝 License & Credits

**License:** MIT  
**Author:** Clawdbot Team  
**Contributors:** See CONTRIBUTORS.md  
**Repository:** https://github.com/clawdbot/clawdbot

---

## 🎉 Thank You!

ขอบคุณที่ใช้ Clawdbot! 

สนับสนุนโปรเจค:
- ⭐ Star on GitHub
- 🐛 Report bugs
- 💡 Suggest features
- 🤝 Contribute code

**Happy Clawdbotting! 🤖**

---

**Last Updated:** February 1, 2026  
**Version:** 2026.1.25  
**Document Version:** 1.0
