import os
import sys
import time
import socket
import struct
import json
from pathlib import Path

# Load .env
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

HOST = os.getenv("SURVIVAL_SSH_HOST", "45.154.27.246")
GAME_PORT = 25566

def ping_server(host=HOST, port=GAME_PORT, timeout=5.0):
    start = time.perf_counter()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        latency_ms = (time.perf_counter() - start) * 1000
        
        # Handshake
        host_bytes = host.encode('utf-8')
        data = b'\x00' + b'\xff\xff\xff\xff\x0f' + struct.pack('>B', len(host_bytes)) + host_bytes + struct.pack('>H', port) + b'\x01'
        data = struct.pack('>B', len(data)) + data
        s.sendall(data)
        
        # Status request
        s.sendall(b'\x01\x00')
        
        resp = b''
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            resp += chunk
            if len(resp) > 5 and b'{' in resp:
                try:
                    start_idx = resp.find(b'{')
                    parsed = json.loads(resp[start_idx:].decode('utf-8', errors='ignore'))
                    return {
                        "online": True,
                        "latency_ms": round(latency_ms, 2),
                        "data": parsed
                    }
                except Exception:
                    pass
        return {"online": True, "latency_ms": round(latency_ms, 2), "raw": resp}
    except Exception as e:
        return {"online": False, "error": str(e)}
    finally:
        s.close()

if __name__ == "__main__":
    res = ping_server()
    if res.get("online"):
        d = res.get("data", {})
        players = d.get("players", {})
        version = d.get("version", {})
        print(f"=== Survival Server Status ({HOST}:{GAME_PORT}) ===")
        print(f"Status   : ONLINE")
        print(f"Latency  : {res.get('latency_ms')} ms")
        print(f"Version  : {version.get('name')} (protocol {version.get('protocol')})")
        print(f"Players  : {players.get('online', 0)} / {players.get('max', 0)}")
    else:
        print(f"=== Survival Server Status ({HOST}:{GAME_PORT}) ===")
        print(f"Status   : OFFLINE / UNREACHABLE")
        print(f"Error    : {res.get('error')}")
