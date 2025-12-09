# Shard 02: n8n Installation & Configuration

## Content Repurposing Engine

**Estimated Time:** 20-30 minutes  
**Dependencies:** Shard 01 (VPS running)  
**Outcome:** n8n accessible via browser

---

## Prerequisites

- [ ] Shard 01 complete (VPS running with SSH access)
- [ ] VPS IP address noted
- [ ] SSH connection active

---

## Tasks

### 2.1 Install Docker

Connect to your VPS and run:

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
```

- [ ] Docker version displayed (should be 24.x or higher)

### 2.2 Install Docker Compose

```bash
# Install Docker Compose
sudo apt install -y docker-compose-plugin

# Verify
docker compose version
```

- [ ] Docker Compose version displayed

### 2.3 Create n8n Directory Structure

```bash
# Create directories
mkdir -p ~/n8n-docker
cd ~/n8n-docker

# Create data directory for persistence
mkdir -p n8n-data
```

- [ ] Directories created

### 2.4 Create Docker Compose File

```bash
nano docker-compose.yml
```

Paste this configuration:

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

**IMPORTANT:** Replace:

- `YOUR_VPS_IP` with your actual VPS IP (2 places)
- `your-secure-password-here` with a strong password

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

- [ ] docker-compose.yml created with your VPS IP

### 2.5 Start n8n

```bash
# Start n8n in background
docker compose up -d

# Check it's running
docker ps
```

- [ ] Container "n8n" shows "Up" status

### 2.6 Access n8n Web Interface

Open browser and navigate to:

```
http://YOUR_VPS_IP:5678
```

- [ ] n8n login page appears
- [ ] Login with:
  - Username: `admin`
  - Password: (what you set in step 2.4)
- [ ] n8n dashboard loads successfully

### 2.7 Complete Initial Setup

On first login:

1. [ ] Skip or complete the onboarding tour
2. [ ] Verify you can create a new workflow
3. [ ] Verify you can access Settings → Credentials

---

## Verification Checklist

| Check          | Method                                    | Expected Result    |
| -------------- | ----------------------------------------- | ------------------ |
| Docker running | `docker ps`                               | n8n container "Up" |
| n8n accessible | Browser → http://IP:5678                  | Login page shown   |
| Login works    | Enter credentials                         | Dashboard loads    |
| Persistence    | Restart container, check workflows remain | Data persists      |

### Test Persistence

```bash
docker compose down
docker compose up -d
```

- [ ] Reload browser - n8n should still have your session

---

## Troubleshooting

### n8n not loading in browser

```bash
# Check container logs
docker logs n8n

# Check if port is listening
netstat -tlnp | grep 5678
```

### Container keeps restarting

```bash
# Check logs for errors
docker logs n8n --tail 50
```

### Permission denied errors

```bash
# Fix n8n-data permissions
sudo chown -R 1000:1000 ~/n8n-docker/n8n-data
docker compose restart
```

### Can't access from browser

- Verify firewall: `ufw status` (port 5678 should be open)
- Try: `ufw allow 5678 && ufw reload`

---

## Security Notes

For the hackathon, HTTP with basic auth is sufficient. For production:

- Set up HTTPS with Let's Encrypt
- Use a reverse proxy (nginx/traefik)
- Use stronger passwords

---

## Completion Checklist

- [ ] Docker installed and running
- [ ] docker-compose.yml configured
- [ ] n8n container running
- [ ] Web interface accessible
- [ ] Basic auth working
- [ ] Data persistence verified

---

## Record These Values

```
n8n URL: http://________________:5678
n8n Username: admin
n8n Password: ________________
```

---

## Next Shard

Once all items checked, proceed to:
**→ Shard 03: Google Credentials Setup**

---

_Your n8n instance is now ready for workflow building!_
