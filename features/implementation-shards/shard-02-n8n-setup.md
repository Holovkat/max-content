# Shard 02: n8n Installation & Configuration - ✅ COMPLETE

## Content Repurposing Engine

**Status:** ✅ Completed  
**Est. Time:** 20-30 minutes  
**Outcome:** n8n running and accessible

---

## Completion Summary

### Tasks Completed

- [x] Docker installed on VPS
- [x] Docker Compose installed
- [x] n8n directory structure created
- [x] docker-compose.yml configured
- [x] n8n container running
- [x] Web interface accessible
- [x] Basic auth working
- [x] Data persistence verified

### Verification ✅

| Check          | Status                   |
| -------------- | ------------------------ |
| Docker running | ✅ Container "Up"        |
| n8n accessible | ✅ Browser loads         |
| Login works    | ✅ Dashboard shows       |
| Persistence    | ✅ Data survives restart |

---

## Reference (Original Instructions)

<details>
<summary>Click to expand original shard content</summary>

### 2.1 Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl start docker
sudo systemctl enable docker
docker --version
```

### 2.2 Install Docker Compose

```bash
sudo apt install -y docker-compose-plugin
docker compose version
```

### 2.3 Create n8n Directory

```bash
mkdir -p ~/n8n-docker
cd ~/n8n-docker
mkdir -p n8n-data
```

### 2.4 Docker Compose Configuration

```yaml
version: "3.8"

services:
  n8n:
    image: n8nio/n8n
    container_name: n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your-secure-password-here
      - N8N_HOST=YOUR_VPS_IP
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://YOUR_VPS_IP:5678/
      - GENERIC_TIMEZONE=UTC
      - N8N_SECURE_COOKIE=false
    volumes:
      - ./n8n-data:/home/node/.n8n
```

### 2.5 Start n8n

```bash
docker compose up -d
docker ps
```

</details>

---

**→ Next: Shard 03: Google Credentials (also complete)**
