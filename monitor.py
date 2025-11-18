# #!/usr/bin/env python3
# """
# Network Health Monitor - CLI tool
# Checks: ping, DNS (nslookup), traceroute (first hops), and ports (80,443)
# Writes time-stamped results to logs/monitor.log
# """

import subprocess
import socket
import sys
import json
import time
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "monitor.log"

DEFAULT_PORTS = [80, 443]
INTERVAL = 60  # seconds between checks

def run_ping(host, count=3, timeout=3):
    try:
        res = subprocess.run(["ping", "-c", str(count), host],
                             capture_output=True, text=True, timeout=10)
        out = res.stdout + res.stderr
        success = ("0% packet loss" in out) or (" 0.0% packet loss" in out) or (res.returncode == 0)
        avg_ms = None
        for line in out.splitlines():
            if "avg" in line or "min/avg" in line or "round-trip" in line or "rtt" in line:
                parts = line.replace("=", "").replace(":", "").split()
                for p in parts:
                    if "/" in p and p.count("/") >= 2:
                        vals = p.split("/")
                        try:
                            avg_ms = float(vals[1])
                        except Exception:
                            avg_ms = None
                break
        return {"success": success, "raw": out.strip(), "avg_ms": avg_ms}
    except subprocess.TimeoutExpired:
        return {"success": False, "raw": "ping timed out", "avg_ms": None}

def run_nslookup(host):
    try:
        res = subprocess.run(["nslookup", host], capture_output=True, text=True, timeout=8)
        out = res.stdout + res.stderr
        resolved = ("Address" in out) or ("Non-authoritative answer" in out) or ("Name:" in out)
        return {"resolved": resolved, "raw": out.strip()}
    except subprocess.TimeoutExpired:
        return {"resolved": False, "raw": "nslookup timed out"}

def run_traceroute(host, max_hops=6):
    try:
        res = subprocess.run(["traceroute", "-m", str(max_hops), host], capture_output=True, text=True, timeout=15)
        out = res.stdout + res.stderr
        return {"raw": out.strip()}
    except Exception as e:
        return {"raw": f"traceroute error: {e}"}

def check_port(host, port, timeout=3):
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        return True
    except Exception:
        return False

def check_host(host, ports=None):
    ports = ports or DEFAULT_PORTS
    now = datetime.now().isoformat(sep=" ", timespec="seconds")
    result = {"host": host, "time": now, "ping": None, "dns": None, "ports": {}, "traceroute": None}
    ping = run_ping(host)
    result["ping"] = ping
    dns = run_nslookup(host)
    result["dns"] = dns
    tr = run_traceroute(host)
    result["traceroute"] = tr
    for p in ports:
        result["ports"][p] = check_port(host if dns["resolved"] else host, p)
    if ping["success"] and dns["resolved"]:
        status = "UP"
    elif ping["success"] and not dns["resolved"]:
        status = "DNS_ISSUE"
    elif not ping["success"]:
        status = "DOWN"
    else:
        status = "UNKNOWN"
    result["status"] = status
    return result

def write_log(obj):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(obj) + "\n")

def pretty_print(obj):
    print(f"\n[{obj['time']}] Host: {obj['host']}  Status: {obj['status']}")
    ping = obj["ping"]
    dns = obj["dns"]
    if ping:
        print("  Ping:", "Success" if ping["success"] else "Failed", f"Avg_ms={ping.get('avg_ms')}")
    if dns:
        print("  DNS:", "Resolved" if dns["resolved"] else "Failed")
    for p, ok in obj["ports"].items():
        print(f"  Port {p}:", "Open" if ok else "Closed/Blocked")
    print("  (Details logged in logs/monitor.log)\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python monitor.py host1 [host2 host3 ...]")
        sys.exit(1)
    hosts = sys.argv[1:]
    print(f"🚀 Starting continuous monitoring for hosts: {hosts}")
    while True:
        for h in hosts:
            print(f"Checking {h} ...")
            r = check_host(h)
            pretty_print(r)
            write_log(r)
        print(f"Sleeping {INTERVAL} seconds before next check...\n")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
