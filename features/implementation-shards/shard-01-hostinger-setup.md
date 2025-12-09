# Shard 01: Hostinger VPS Setup

## Content Repurposing Engine

**Estimated Time:** 30-45 minutes  
**Dependencies:** None  
**Outcome:** Running VPS with SSH access

---

## Prerequisites

- [ ] Hostinger account (create at hostinger.com if needed)
- [ ] Payment method for VPS (hackathon may provide credits)
- [ ] SSH client (Terminal on Mac, or VSCode Remote SSH)

---

## Tasks

### 1.1 Purchase/Provision VPS

- [ ] Log into Hostinger (hostinger.com)
- [ ] Navigate to **Hosting** → **VPS Hosting**
- [ ] Select **KVM 2** plan (recommended for n8n)
  - 2 vCPU
  - 8 GB RAM
  - 100 GB NVMe SSD
- [ ] Choose **Ubuntu 24.04 64bit** as OS
- [ ] Select datacenter closest to you
- [ ] Complete purchase

### 1.2 Access VPS Information

Once provisioned (usually 1-5 minutes):

- [ ] Go to **hPanel** → **VPS** → Select your VPS
- [ ] Note down the following:

```
VPS IP Address: ___________________
Root Password: ____________________
SSH Port: 22 (default)
```

### 1.3 Connect via SSH

Open Terminal and connect:

```bash
ssh root@YOUR_VPS_IP
```

- [ ] Accept the fingerprint (type `yes`)
- [ ] Enter your root password
- [ ] Confirm you see the Ubuntu command prompt

### 1.4 Initial Server Updates

Run these commands:

```bash
# Update package lists
apt update

# Upgrade existing packages
apt upgrade -y

# Install essential tools
apt install -y curl wget git nano ufw
```

- [ ] All commands complete without errors

### 1.5 Configure Firewall

```bash
# Allow SSH
ufw allow 22

# Allow HTTP
ufw allow 80

# Allow HTTPS
ufw allow 443

# Allow n8n port
ufw allow 5678

# Enable firewall
ufw enable
```

- [ ] Type `y` to confirm
- [ ] Verify with `ufw status` - should show all rules active

### 1.6 (Optional) Create Non-Root User

For better security:

```bash
# Create user
adduser n8nadmin

# Add to sudo group
usermod -aG sudo n8nadmin

# Switch to new user
su - n8nadmin
```

- [ ] User created (or skip if using root)

---

## Verification Checklist

Run these checks before marking shard complete:

| Check        | Command              | Expected Result           |
| ------------ | -------------------- | ------------------------- |
| SSH Access   | `ssh root@YOUR_IP`   | Login successful          |
| OS Version   | `lsb_release -a`     | Ubuntu 24.04              |
| Firewall     | `ufw status`         | Ports 22,80,443,5678 open |
| Internet     | `curl -I google.com` | HTTP 301 response         |
| Docker Ready | (next shard)         | -                         |

---

## Troubleshooting

### Can't connect via SSH

- Check if VPS is fully provisioned (wait 5 min)
- Verify IP address is correct
- Try: `ssh -v root@YOUR_IP` for verbose output

### Firewall issues

- If locked out: Access via Hostinger hPanel console
- Run: `ufw disable` then reconfigure

### Package update fails

- Try: `apt clean && apt update`
- Check internet: `ping google.com`

---

## Completion Checklist

- [ ] VPS provisioned and running
- [ ] SSH access working
- [ ] System packages updated
- [ ] Firewall configured with required ports
- [ ] Ready for n8n installation

---

## Next Shard

Once all items checked, proceed to:
**→ Shard 02: n8n Installation & Configuration**

---

_Record your VPS IP - you'll need it for every remaining shard._
