import os
import sys
import socket
import struct
import time
import argparse
from pathlib import Path

# Load .env file if present
def load_dotenv():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

load_dotenv()

DEFAULT_HOST = os.getenv("SURVIVAL_RCON_HOST", "45.154.27.246")
DEFAULT_PORT = int(os.getenv("SURVIVAL_RCON_PORT", "25577"))
DEFAULT_PASS = os.getenv("SURVIVAL_RCON_PASS", "survival_admin_2026")

def send_rcon(cmd: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, password: str = DEFAULT_PASS, timeout: float = 5.0) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        # Auth packet: id=1, type=3
        auth_payload = password.encode("utf-8")
        s.sendall(struct.pack("<iii", 10 + len(auth_payload), 1, 3) + auth_payload + b"\x00\x00")
        auth_resp = s.recv(4096)
        if len(auth_resp) < 12:
            return "[ERROR] Empty auth response from server."
        
        # Exec packet: id=2, type=2
        cmd_payload = cmd.encode("utf-8")
        s.sendall(struct.pack("<iii", 10 + len(cmd_payload), 2, 2) + cmd_payload + b"\x00\x00")
        time.sleep(0.2)
        resp = s.recv(8192)
        if len(resp) >= 12:
            body = resp[12:-2].decode("utf-8", errors="replace")
            # Strip Minecraft color/formatting codes for clean terminal output if desired
            return body.strip()
        return "[WARN] No response payload received."
    except Exception as e:
        return f"[ERROR] RCON Exception: {e}"
    finally:
        s.close()

def main():
    parser = argparse.ArgumentParser(description="Survival Minecraft RCON Client")
    parser.add_argument("command", nargs="*", help="Minecraft server command to execute")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Server host IP")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="RCON port")
    parser.add_argument("--password", default=DEFAULT_PASS, help="RCON password")
    
    args = parser.parse_args()
    
    if args.command:
        cmd_str = " ".join(args.command)
        out = send_rcon(cmd_str, host=args.host, port=args.port, password=args.password)
        print(out)
    else:
        print(f"Connected to RCON {args.host}:{args.port}. Enter commands (type 'exit' or 'quit' to close):")
        while True:
            try:
                line = input("mc-survival> ").strip()
                if not line:
                    continue
                if line.lower() in ("exit", "quit"):
                    break
                out = send_rcon(line, host=args.host, port=args.port, password=args.password)
                print(out)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting RCON session.")
                break

if __name__ == "__main__":
    main()
