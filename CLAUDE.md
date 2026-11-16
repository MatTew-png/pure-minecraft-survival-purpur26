# Pure Minecraft Survival Server (Purpur 26.3 / Java 25)

## 📌 Architecture & Environment Context
- **Domain**: Dedicated High-Performance Minecraft Survival Server (Pure Vanilla+ / Zero Cobblemon).
- **Engine**: **Purpur 26.3** (Build 2658) on **Java 25 LTS** (`Eclipse Adoptium Temurin 25.0.5+8`).
- **Host**: Dedicated Windows Server `45.154.27.246` (i9-12900K, 64 GB RAM).
- **Remote Directory**: `C:\Users\Administrator\Desktop\survival`
- **Memory Allocation**: Min 8G / Max 12G (Aikar's G1GC flags for Java 25).

## 🛡️ Network & Port Coexistence Rules (CRITICAL)
This server runs concurrently with Cobblemon Network on the same physical host.
- **Survival Game Port**: `25566` (TCP / UDP)
- **Survival RCON Port**: `25577` (Password in `.env`)
- ⚠️ **Strict Coexistence Shield**:
  - **NEVER** bind, modify, or kill processes on:
    - `25565` (Velocity Proxy)
    - `11782` / `25576` (Lobby Server)
    - `32517` / `25575` (Cobblemon Server)
  - All survival processes must stay inside `C:\Users\Administrator\Desktop\survival`.

## 🛠️ Management & Automation CLI
All scripts load credentials automatically from `.env` (or environment variables).
- **RCON Command**:
  ```bash
  python scripts/rcon_cli.py "tps"
  python scripts/rcon_cli.py "say Hello Survivors"
  ```
- **Remote Process Status**:
  ```bash
  python scripts/remote_ops.py status
  ```
- **Remote PowerShell Execution**:
  ```bash
  python scripts/remote_ops.py ps "Get-Service MariaDB"
  ```
- **Upload / Staging**:
  ```bash
  python scripts/remote_ops.py upload ./plugins/MyPlugin.jar "C:\Users\Administrator\Desktop\survival\update_staging\MyPlugin.jar"
  ```

## 📜 Development & Engineering Protocols
1. **Empirical Verification First**:
   - Always verify server state using RCON or process checks (`tps`, `version`, `plugins`) before and after configuration changes.
2. **Surgical Config Editing**:
   - Never overwrite entire YAML/properties files blindly. Preserve existing comments and tunings.
3. **Graceful Reload / Restart**:
   - Plugins should be placed in `update_staging\` and loaded, or server restarted gracefully via `#Start.bat` / RCON `stop`.
