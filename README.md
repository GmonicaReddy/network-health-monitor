# 🖥️ Network Health Monitor

A simple Python-based Network Health Monitoring tool that continuously checks the health of servers and websites. The application performs network diagnostics such as ping checks, DNS resolution, traceroute, and port availability checks. The project is containerized using Docker, making it easy to run on any system.

## Features

-  Monitors multiple hosts continuously
- Checks host availability using Ping
- Verifies DNS resolution using nslookup
- Performs traceroute analysis
- Checks common ports (80 and 443)
- Logs all monitoring results with timestamps
- Dockerized for easy deployment and portability

## Tech Stack

- Python
- Docker
- Networking Tools (Ping, DNS, Traceroute)
- JSON Logging

## Project Structure

```
network-monitor/
├── monitor.py
├── app.py
├── Dockerfile
├── requirements.txt
├── logs/
│   └── monitor.log
└── templates/
```

## How to Run

### 1. Clone the Repository

```bash
git clone <repository-url>
cd network-monitor
```

### 2. Build the Docker Image

```bash
docker build -t network-monitor .
```

### 3. Run the Application

```bash
docker run -it -v $(pwd)/logs:/app/logs network-monitor
```

The monitor will start checking the configured hosts continuously.

### 4. Stop the Application

Press:

```bash
Ctrl + C
```

to stop monitoring.

## View Logs

Monitoring results are stored in:

```bash
logs/monitor.log
```

Each entry contains:
- Timestamp
- Host name
- Ping status
- DNS status
- Port status
- Traceroute details
- Overall host status

## Sample Output

```text
Starting continuous monitoring...

[2026-06-11 10:30:00] Host: google.com  Status: UP
Ping: Success
DNS: Resolved
Port 80: Open
Port 443: Open

Sleeping before next check...
```


