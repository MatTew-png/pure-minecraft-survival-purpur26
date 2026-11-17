# 🌲 Pure Survival Server — Purpur 26.3 & Java 25

[![Minecraft](https://img.shields.io/badge/Minecraft-Purpur%2026.3-5A9E32?logo=minecraft)](https://purpurmc.org/)
[![Java](https://img.shields.io/badge/Java-25%20LTS-ED8B00?logo=openjdk)](https://adoptium.net/)
[![Hardware](https://img.shields.io/badge/Host-i9--12900K%20%7C%2064GB-0071C5?logo=intel)](https://intel.com)
[![Status](https://img.shields.io/badge/Live%20TPS-20.0-success)](#)
[![Handover Specification](https://img.shields.io/badge/Blueprint-Handover%20Docs-blue)](docs/HANDOVER_SPECIFICATION.md)
[![Data Truth Engine](https://img.shields.io/badge/Google%20Sheets-Data%20Engine-brightgreen)](https://docs.google.com/spreadsheets/d/11hZOHenib5-hMHXeg4HUWR_QvEE462qON4LtOZMkdvY/edit?usp=sharing)

A dedicated, production-grade Minecraft Survival server infrastructure engineered for **Pure Vanilla+ & Semi-Community Experience** (Zero Cobblemon / Pokemon dependencies), co-existing safely on a high-spec bare-metal host.

---

## 📘 เอกสารส่งมอบและระบบควบคุม (Project Blueprint & Operations)
- ⚔️ **[แผนผังการออกแบบระบบเกมเชิงลึก (GAME_DESIGN_SPECIFICATION.md)](docs/GAME_DESIGN_SPECIFICATION.md)**: สเปกระบบเกม MMORPG-Survival Hybrid ฉบับสมบูรณ์ (Gameloop, เศรษฐกิจ, อาชีพรอง 6 สาย, สกิล Free-build, ตีบวก/รูน, เอนแชนต์ Gathering)
- 🖥️ **[Interactive Handover Dashboard (เปิดในเบราว์เซอร์)](docs/dashboard.html)**: แดชบอร์ดสรุปสถานะเซิร์ฟเวอร์แบบอินเตอร์แอคทีฟ, ตัวกรองบทบาทงาน RACI (มด & นิว), แผงคำสั่งลัด
- 📑 **[เล่มส่งมอบระบบฉบับสมบูรณ์ (HANDOVER_SPECIFICATION.md)](docs/HANDOVER_SPECIFICATION.md)**: สถาปัตยกรรมระบบ, ข้อตกลงการแบ่งงาน RACI (มด & นิว), ตาราง Port Matrix, ขั้นตอนปฏิบัติงานทีละสเต็ป
- 📊 **[Google Sheets Data Truth Engine](https://docs.google.com/spreadsheets/d/11hZOHenib5-hMHXeg4HUWR_QvEE462qON4LtOZMkdvY/edit?usp=sharing)**: ตารางติดตามงาน Task Matrix, รายการปลั๊กอิน, ราคากลางไอเทม, และสิทธิ์ LuckPerms Ranks
- 📈 **[ตารางค่าตัวเลขระบบเกม (06_game_systems_matrix.csv)](data_sheets/06_game_systems_matrix.csv)**: ตัวเลขสมดุลเศรษฐกิจ, อัตราความสำเร็จตีบวก, สเปก Resource Nodes, และอัตราดรอปบอส

---

## 🏗️ Architecture & Network Layout

| Component | Port | Host Directory | Description |
| :--- | :--- | :--- | :--- |
| **Survival Game Engine** | `25566` (TCP/UDP) | `C:\Users\Administrator\Desktop\survival` | Purpur 26.3 (Build 2658) on Java 25 LTS |
| **Survival RCON** | `25577` (TCP) | Remote Console | Management interface |
| **MySQL (MariaDB)** | `3306` (Localhost) | Host Service | Dedicated database storage (`survival_*`) |
| **Redis Cache** | `6379` (Localhost) | `C:\Users\Administrator\Desktop\Redis...` | Fast caching / cross-session memory |

> **Coexistence Shield**: Isolated from the existing Cobblemon network (`25565`, `11782`, `32517`) to prevent resource and port contention.

---

## ⚡ Key Optimizations & Engineering Features

1. **Purpur Engine & Paper Performance**:
   - `ALTERNATE_CURRENT` redstone engine for 10x lower tick overhead.
   - Disabled TPS catchup to prevent severe tick freezes after spikes.
   - Alternate keepalive protocol enabled to drastically reduce false timeout kicks.
2. **JVM Tuning (Aikar's G1GC on Java 25)**:
   - Configured with `AlwaysPreTouch`, `SurvivorRatio=32`, and 8MB heap regions.
   - Dedicated memory envelope: Min 8 GB / Max 12 GB.
3. **Windows QuickEdit Prevention**:
   - Built-in console trap disabling to eliminate terminal freezing on mouse selection.
4. **Auto-Deploy Staging Pipeline**:
   - Built-in staging mechanism (`update_staging\*.jar` $\rightarrow$ `plugins\` on startup).

---

## 🚀 Quick Management Shortcuts

### 1. Interactive RCON Console
```cmd
:: Quick command via batch shortcut
.\rcon.bat tps
.\rcon.bat "say Welcome to Pure Survival!"

:: Interactive terminal session
python scripts/rcon_cli.py
```

### 2. Fast Server Ping & Health Check
```cmd
.\status.bat
```
Output:
```
=== Survival Server Status (45.154.27.246:25566) ===
Status   : ONLINE
Latency  : ~7.8 ms
Version  : Purpur 26.3
Players  : 0 / 100
```

### 3. Deploy Plugins to Staging
```cmd
:: Automatically stages plugin into update_staging\ on remote host
.\deploy.bat path\to\MyPlugin.jar
```

---

## 📂 Repository Structure

```
Survival/
├── .env.example            # Environment configuration template
├── .gitignore              # Git ignore rules (secrets, venv, temporary files)
├── AGENTS.md               # Agentic guidance bridge
├── CLAUDE.md               # Server handbook & operating invariants
├── README.md               # Main project documentation
├── rcon.bat                # Fast RCON CLI shortcut
├── status.bat              # Fast Server Ping & status shortcut
├── deploy.bat              # Remote staging upload shortcut
└── scripts/
    ├── ping_status.py      # SLP server list ping status checker
    ├── rcon_cli.py         # Standalone Minecraft RCON commander
    └── remote_ops.py       # SSH / SFTP remote management automation
```
