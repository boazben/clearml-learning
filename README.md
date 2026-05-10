
# ClearML — System Startup Guide

> **Environment:** WSL2 / Ubuntu on Windows, Docker Desktop
> **Server:** `/opt/clearml/`
> **Agent venv:** `~/.venvs/clearml-agent`

---

## Step 1 — Stop All Containers

```bash
cd /opt/clearml
docker compose down
```

Verify everything stopped:

```bash
docker ps
# Expected: empty list
```

---

## Step 2 — Start All Containers

```bash
cd /opt/clearml
docker compose up -d
```

Wait ~20 seconds, then verify all 6 containers are `Up`:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

Expected output:

```
NAMES                STATUS
clearml-webserver    Up X seconds
clearml-apiserver    Up X seconds
clearml-fileserver   Up X seconds
clearml-redis        Up X seconds
clearml-elastic      Up X seconds
clearml-mongo        Up X seconds
```

If any container shows `Restarting` or `Exit`, wait another 10 seconds and run again.

---

## Step 3 — Log in to the UI

Open in browser: **http://localhost:8080**

Log in with your credentials. You should see the dashboard with your projects and tasks.

> If the dashboard looks empty after login, do a hard refresh: `Ctrl + Shift + R`

---

## Step 4 — Start 2 Agents (3 Queues)

Open **two separate terminals** in WSL.

### Prerequisites — verify `~/.clearml/clearml.conf` contains:

```hocon
agent {
    cuda_version: ""
    cudnn_version: ""
    extra_docker_arguments: [
        "--network=host",
        "-e", "CLEARML_API_HOST=http://host.docker.internal:8008",
        "-e", "CLEARML_WEB_HOST=http://host.docker.internal:8080",
        "-e", "CLEARML_FILES_HOST=http://host.docker.internal:8081"
    ]
}
```

### Terminal 1 — Agent listening on `default` + `cpu` queues (Docker mode)

```bash
source ~/.venvs/clearml-agent/bin/activate
NVIDIA_VISIBLE_DEVICES=none clearml-agent daemon --queue default cpu --docker python:3.11
```

### Terminal 2 — Agent listening on `gpu-sim` queue (Docker mode)

```bash
source ~/.venvs/clearml-agent/bin/activate
NVIDIA_VISIBLE_DEVICES=none clearml-agent daemon --queue gpu-sim --docker python:3.11
```

### Verify agents are connected

1. Go to **http://localhost:8080**
2. Click **"Manage Workers and Queues"** (bottom right of the dashboard)
3. You should see **2 workers** listed, each showing status **online**

---

## Shutdown

```bash
# In each agent terminal:
Ctrl+C

# Then stop the server:
cd /opt/clearml && docker compose down
```
