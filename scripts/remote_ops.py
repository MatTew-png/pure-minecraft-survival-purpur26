import os
import sys
import base64
from pathlib import Path
import paramiko

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

HOST = os.getenv("SURVIVAL_SSH_HOST", "45.154.27.246")
PORT = int(os.getenv("SURVIVAL_SSH_PORT", "22"))
USER = os.getenv("SURVIVAL_SSH_USER", "Administrator")
PASS = os.getenv("SURVIVAL_SSH_PASS", "0IGd$K#jrv#j")
SURVIVAL_DIR = os.getenv("SURVIVAL_REMOTE_DIR", r"C:\Users\Administrator\Desktop\survival")

def run_remote_ps(ps_script: str):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=10)
    
    encoded = base64.b64encode(ps_script.encode("utf-16le")).decode("ascii")
    cmd = f"powershell -NoProfile -ExecutionPolicy Bypass -EncodedCommand {encoded}"
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    ssh.close()
    return out, err

def get_survival_status():
    ps = f"""
    $proc = Get-Process -Name java -ErrorAction SilentlyContinue | Where-Object {{
        $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
        $cmd -match "survival" -or $cmd -match "purpur-26.3.jar"
    }}
    if ($proc) {{
        [PSCustomObject]@{{
            Status = 'RUNNING'
            PID = $proc.Id
            WorkingSetMB = [math]::Round($proc.WorkingSet64 / 1MB, 2)
            StartTime = $proc.StartTime
        }} | ConvertTo-Json
    }} else {{
        [PSCustomObject]@{{ Status = 'STOPPED' }} | ConvertTo-Json
    }}
    """
    out, err = run_remote_ps(ps)
    return out.strip()

def upload_file(local_path: str, remote_path: str):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=10)
    sftp = ssh.open_sftp()
    print(f"Uploading {local_path} -> {remote_path}...")
    sftp.put(local_path, remote_path)
    sftp.close()
    ssh.close()
    print("Upload completed.")

def download_file(remote_path: str, local_path: str):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=10)
    sftp = ssh.open_sftp()
    print(f"Downloading {remote_path} -> {local_path}...")
    sftp.get(remote_path, local_path)
    sftp.close()
    ssh.close()
    print("Download completed.")

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    if action == "status":
        print(get_survival_status())
    elif action == "ps" and len(sys.argv) > 2:
        out, err = run_remote_ps(sys.argv[2])
        if out:
            print(out)
        if err:
            print("[STDERR]", err, file=sys.stderr)
    elif action == "upload" and len(sys.argv) > 3:
        upload_file(sys.argv[2], sys.argv[3])
    elif action == "download" and len(sys.argv) > 3:
        download_file(sys.argv[2], sys.argv[3])
    else:
        print("Usage: python remote_ops.py [status|ps <script>|upload <local> <remote>|download <remote> <local>]")
