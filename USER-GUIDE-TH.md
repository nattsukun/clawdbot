# คู่มือการใช้งาน Clawdbot

## สารบัญ
1. [แนะนำ](#แนะนำ)
2. [การเริ่มต้นใช้งาน](#การเริ่มต้นใช้งาน)
3. [คำสั่ง CLI พื้นฐาน](#คำสั่ง-cli-พื้นฐาน)
4. [Gateway Server](#gateway-server)
5. [Channels (ช่องทางการสื่อสาร)](#channels-ช่องทางการสื่อสาร)
6. [AI Providers](#ai-providers)
7. [Agents และ RPC](#agents-และ-rpc)
8. [Plugins](#plugins)
9. [การตั้งค่าขั้นสูง](#การตั้งค่าขั้นสูง)
10. [Tips & Tricks](#tips--tricks)

---

## แนะนำ

Clawdbot เป็น WhatsApp gateway CLI พร้อม Pi RPC agent ที่รองรับหลาย messaging platforms และ AI providers

### คุณสมบัติหลัก
- 🔌 รองรับหลาย messaging channels (WhatsApp, Telegram, Discord, Slack, Signal, iMessage)
- 🤖 AI agent ที่ทรงพลังด้วย RPC mode
- 🔧 ระบบ plugin แบบ modular
- 🌐 Gateway server สำหรับ remote access
- 📱 รองรับ mobile และ desktop apps

---

## การเริ่มต้นใช้งาน

### 1. ตรวจสอบการติดตั้ง

```powershell
# ตรวจสอบว่าติดตั้งแล้ว
pnpm clawdbot --version

# ดูคำสั่งที่มีให้ใช้
pnpm clawdbot --help
```

### 2. ตั้งค่าเบื้องต้น

```powershell
# ดู config ปัจจุบัน
pnpm clawdbot config list

# ตั้งค่า gateway mode
pnpm clawdbot config set gateway.mode local

# ตั้งค่า log level
pnpm clawdbot config set logging.level info
```

### 3. Login ไปยัง Provider (เช่น WhatsApp)

```powershell
# Login WhatsApp Web
pnpm clawdbot login

# Login ด้วย provider อื่น
pnpm clawdbot login --provider <provider-name>
```

---

## คำสั่ง CLI พื้นฐาน

### Config Management

```powershell
# แสดง config ทั้งหมด
pnpm clawdbot config list

# แสดง config แบบ JSON
pnpm clawdbot config list --json

# ตั้งค่า
pnpm clawdbot config set <key> <value>

# ลบค่า config
pnpm clawdbot config delete <key>

# Reset config
pnpm clawdbot config reset
```

### Channels Management

```powershell
# ดูสถานะ channels ทั้งหมด
pnpm clawdbot channels status

# ดูสถานะพร้อม probe
pnpm clawdbot channels status --probe

# ดู channels ทั้งหมด (รวมที่ไม่ได้เปิดใช้)
pnpm clawdbot channels status --all

# เปิดใช้งาน channel
pnpm clawdbot channels enable <channel-name>

# ปิดการใช้งาน channel
pnpm clawdbot channels disable <channel-name>
```

### Message Commands

```powershell
# ส่งข้อความ
pnpm clawdbot message send --to <recipient> --message "Hello!"

# ส่งข้อความพร้อมไฟล์
pnpm clawdbot message send --to <recipient> --message "Check this" --file <path>

# ส่งข้อความผ่าน channel เฉพาะ
pnpm clawdbot message send --to <recipient> --message "Hi" --channel telegram
```

### Agent Commands

```powershell
# รัน agent ในโหมด RPC
pnpm clawdbot agent --mode rpc --json

# ส่งข้อความไปยัง agent
pnpm clawdbot agent --message "What's the weather?"

# ใช้ thinking mode
pnpm clawdbot agent --message "Solve this problem" --thinking high
```

---

## Gateway Server

Gateway เป็นตัวกลางที่ทำให้สามารถ remote access ได้

### เริ่มต้น Gateway

```powershell
# รัน gateway (default port: 18789)
pnpm clawdbot gateway run

# รัน gateway กับ port เฉพาะ
pnpm clawdbot gateway run --port 3000

# รัน gateway bind กับ localhost เท่านั้น
pnpm clawdbot gateway run --bind loopback

# รัน gateway ในโหมด dev (skip channels)
$env:CLAWDBOT_SKIP_CHANNELS=1; pnpm dev gateway --dev

# Force restart gateway
pnpm clawdbot gateway run --force
```

### ตรวจสอบ Gateway

```powershell
# ตรวจสอบว่า gateway ทำงานอยู่
netstat -ano | findstr :18789

# ดู logs
Get-Content "$env:USERPROFILE\.clawdbot\logs\gateway.log" -Tail 50

# ดู logs แบบ real-time
Get-Content "$env:USERPROFILE\.clawdbot\logs\gateway.log" -Tail 50 -Wait
```

### Gateway Configuration

```powershell
# ตั้งค่า gateway mode
pnpm clawdbot config set gateway.mode local

# ตั้งค่า gateway URL (สำหรับ remote)
pnpm clawdbot config set gateway.url "https://your-gateway.com"

# ตั้งค่า gateway token
pnpm clawdbot config set gateway.token "your-secret-token"
```

---

## Channels (ช่องทางการสื่อสาร)

Clawdbot รองรับหลาย messaging platforms:

### WhatsApp (Default)
```powershell
# Login WhatsApp
pnpm clawdbot login

# ดูสถานะการเชื่อมต่อ
pnpm clawdbot channels status --probe
```

### Telegram
```powershell
# ตั้งค่า Telegram bot token
pnpm clawdbot config set telegram.token "YOUR_BOT_TOKEN"

# เปิดใช้งาน Telegram
pnpm clawdbot channels enable telegram
```

### Discord
```powershell
# ตั้งค่า Discord bot token
pnpm clawdbot config set discord.token "YOUR_BOT_TOKEN"

# เปิดใช้งาน Discord
pnpm clawdbot channels enable discord
```

### Slack
```powershell
# ตั้งค่า Slack credentials
pnpm clawdbot config set slack.token "YOUR_SLACK_TOKEN"

# เปิดใช้งาน Slack
pnpm clawdbot channels enable slack
```

### Signal
```powershell
# เปิดใช้งาน Signal (ต้องมี Signal Desktop ติดตั้งอยู่)
pnpm clawdbot channels enable signal
```

### iMessage (macOS เท่านั้น)
```powershell
# เปิดใช้งาน iMessage
pnpm clawdbot channels enable imessage
```

---

## AI Providers

### ตั้งค่า Provider

```powershell
# ตั้งค่า OpenAI
pnpm clawdbot config set provider.name openai
pnpm clawdbot config set provider.apiKey "YOUR_OPENAI_KEY"

# ตั้งค่า Anthropic (Claude)
pnpm clawdbot config set provider.name anthropic
pnpm clawdbot config set provider.apiKey "YOUR_ANTHROPIC_KEY"

# ตั้งค่า Google (Gemini)
pnpm clawdbot config set provider.name google
pnpm clawdbot config set provider.apiKey "YOUR_GOOGLE_KEY"
```

### Model Selection

```powershell
# เลือก model
pnpm clawdbot config set provider.model "gpt-4"
pnpm clawdbot config set provider.model "claude-3-opus"
pnpm clawdbot config set provider.model "gemini-pro"
```

### Provider Settings

```powershell
# ตั้งค่า temperature
pnpm clawdbot config set provider.temperature 0.7

# ตั้งค่า max tokens
pnpm clawdbot config set provider.maxTokens 2000

# ตั้งค่า system prompt
pnpm clawdbot config set provider.systemPrompt "You are a helpful assistant"
```

---

## Agents และ RPC

### Agent Modes

**Interactive Mode:**
```powershell
# รัน agent แบบ interactive
pnpm clawdbot agent
```

**RPC Mode:**
```powershell
# รัน agent ในโหมด RPC (JSON output)
pnpm clawdbot agent --mode rpc --json
```

**Message Mode:**
```powershell
# ส่ง single message
pnpm clawdbot agent --message "Explain quantum computing"
```

### Thinking Modes

```powershell
# Low thinking (fast, simple)
pnpm clawdbot agent --message "What time is it?" --thinking low

# Medium thinking (balanced)
pnpm clawdbot agent --message "Plan a trip" --thinking medium

# High thinking (deep analysis)
pnpm clawdbot agent --message "Solve complex problem" --thinking high
```

### Agent Configuration

```powershell
# ตั้งค่า default thinking mode
pnpm clawdbot config set agent.thinking medium

# ตั้งค่า agent timeout
pnpm clawdbot config set agent.timeout 60000

# เปิด/ปิด streaming
pnpm clawdbot config set agent.streaming true
```

---

## Plugins

### การจัดการ Plugins

```powershell
# ดู plugins ที่มี
ls extensions/

# แสดง plugins ที่เปิดใช้งาน
pnpm clawdbot config list | Select-String "plugins"
```

### เปิดใช้งาน Plugin

```powershell
# เปิดใช้งาน plugin
pnpm clawdbot config set plugins.entries.<plugin-name>.enabled true

# ตัวอย่าง: เปิดใช้ MS Teams
pnpm clawdbot config set plugins.entries.msteams.enabled true
```

### ติดตั้ง Plugin Dependencies

```powershell
# เข้าไปยัง plugin directory
cd extensions/<plugin-name>

# ติดตั้ง dependencies
pnpm install --prod

# กลับไปยัง root
cd ../..
```

### Plugins ที่มีให้ใช้

- **msteams** - Microsoft Teams integration
- **matrix** - Matrix protocol support
- **zalo** - Zalo messaging
- **voice-call** - Voice call support
- และอื่นๆ ใน `extensions/` directory

---

## การตั้งค่าขั้นสูง

### Environment Variables

```powershell
# Skip channels startup (faster dev)
$env:CLAWDBOT_SKIP_CHANNELS=1

# Enable live testing
$env:CLAWDBOT_LIVE_TEST=1

# Set log level
$env:CLAWDBOT_LOG_LEVEL="debug"

# Custom profile
$env:CLAWDBOT_PROFILE="dev"
```

### Custom Config Location

```powershell
# ตั้งค่า config path
$env:CLAWDBOT_CONFIG_PATH="C:\custom\path\config.json"
```

### Debug Mode

```powershell
# รัน gateway พร้อม debug logs
pnpm clawdbot config set logging.level debug
pnpm clawdbot gateway run
```

### Logging

```powershell
# ตั้งค่า log level
pnpm clawdbot config set logging.level info  # debug, info, warn, error

# ตั้งค่า log output
pnpm clawdbot config set logging.output file  # console, file, both

# ดูที่เก็บ logs
echo $env:USERPROFILE\.clawdbot\logs\
```

---

## Tips & Tricks

### การใช้งานประจำวัน

1. **Quick Gateway Start**
   ```powershell
   # สร้าง alias
   function Start-Clawdbot { pnpm clawdbot gateway run --force }
   Set-Alias -Name clawdbot-start -Value Start-Clawdbot
   ```

2. **Monitor Logs**
   ```powershell
   # Real-time log monitoring
   Get-Content "$env:USERPROFILE\.clawdbot\logs\*.log" -Tail 100 -Wait
   ```

3. **Quick Status Check**
   ```powershell
   # Check all channels
   pnpm clawdbot channels status --all
   ```

### Performance Optimization

1. **Skip Unused Channels**
   ```powershell
   # ปิด channels ที่ไม่ใช้
   pnpm clawdbot channels disable <channel-name>
   ```

2. **Use Local Gateway**
   ```powershell
   pnpm clawdbot config set gateway.mode local
   ```

3. **Reduce Logging**
   ```powershell
   pnpm clawdbot config set logging.level warn
   ```

### Troubleshooting Commands

```powershell
# Run doctor command (if available)
pnpm clawdbot doctor

# Clear sessions
Remove-Item -Recurse -Force "$env:USERPROFILE\.clawdbot\sessions\*"

# Clear cache
Remove-Item -Recurse -Force "$env:USERPROFILE\.clawdbot\cache\*"

# Reset config to defaults
pnpm clawdbot config reset
```

### Backup & Restore

```powershell
# Backup config
Copy-Item "$env:USERPROFILE\.clawdbot\config.json" "$env:USERPROFILE\.clawdbot\config.backup.json"

# Backup sessions
Copy-Item -Recurse "$env:USERPROFILE\.clawdbot\sessions" "$env:USERPROFILE\.clawdbot\sessions.backup"

# Restore config
Copy-Item "$env:USERPROFILE\.clawdbot\config.backup.json" "$env:USERPROFILE\.clawdbot\config.json"
```

---

## ตัวอย่างการใช้งานจริง

### Use Case 1: WhatsApp Bot

```powershell
# 1. Login WhatsApp
pnpm clawdbot login

# 2. ตั้งค่า AI provider
pnpm clawdbot config set provider.name openai
pnpm clawdbot config set provider.apiKey "YOUR_KEY"

# 3. Start gateway
pnpm clawdbot gateway run

# 4. ส่งข้อความทดสอบ
pnpm clawdbot message send --to "1234567890@s.whatsapp.net" --message "Hello!"
```

### Use Case 2: Multi-Channel Bot

```powershell
# 1. Setup Telegram
pnpm clawdbot config set telegram.token "YOUR_TELEGRAM_TOKEN"
pnpm clawdbot channels enable telegram

# 2. Setup Discord
pnpm clawdbot config set discord.token "YOUR_DISCORD_TOKEN"
pnpm clawdbot channels enable discord

# 3. Start gateway with all channels
pnpm clawdbot gateway run
```

### Use Case 3: AI Agent RPC

```powershell
# 1. ตั้งค่า provider
pnpm clawdbot config set provider.name anthropic
pnpm clawdbot config set provider.apiKey "YOUR_ANTHROPIC_KEY"

# 2. รัน agent ในโหมด RPC
pnpm clawdbot agent --mode rpc --json

# 3. ใช้งาน agent
pnpm clawdbot agent --message "Analyze this data: [data]" --thinking high
```

---

## การอัพเดต

```powershell
# Pull latest changes
git pull

# Update dependencies
pnpm install

# Rebuild
pnpm build

# Restart gateway
pnpm mac:restart  # macOS
# หรือ kill และ start ใหม่บน Windows
```

---

## คำถามที่พบบ่อย (FAQ)

**Q: Gateway ไม่เริ่มทำงาน?**
A: ตรวจสอบว่า port ถูกใช้งานอยู่หรือไม่ และลอง kill process แล้ว start ใหม่

**Q: WhatsApp disconnected บ่อย?**
A: ตรวจสอบ internet connection และลอง login ใหม่

**Q: Agent ตอบช้า?**
A: ตรวจสอบ thinking mode และ provider settings

**Q: Plugins ไม่ทำงาน?**
A: ตรวจสอบว่าติดตั้ง dependencies ครบและเปิดใช้งานแล้ว

---

## การขอความช่วยเหลือ

- **Documentation:** https://docs.clawd.bot
- **GitHub Issues:** https://github.com/clawdbot/clawdbot/issues
- **Debug Logs:** `$env:USERPROFILE\.clawdbot\logs\`

---

## License & Credits

ดูรายละเอียดใน LICENSE file และ README.md
