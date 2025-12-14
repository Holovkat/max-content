# Shard 01: Hostinger VPS Setup - ✅ COMPLETE

## Content Repurposing Engine

**Status:** ✅ Completed  
**Est. Time:** 30-45 minutes  
**Outcome:** Running VPS with n8n

---

## Completion Summary

### Tasks Completed

- [x] Hostinger account created
- [x] VPS provisioned (KVM 2 plan)
- [x] Ubuntu OS installed
- [x] SSH access configured
- [x] System packages updated
- [x] Firewall configured (ports 22, 80, 443, 5678)
- [x] Ready for n8n installation

### Verification ✅

| Check      | Status        |
| ---------- | ------------- |
| SSH Access | ✅ Working    |
| OS Version | ✅ Ubuntu     |
| Firewall   | ✅ Ports open |
| Internet   | ✅ Connected  |

---

## Reference (Original Instructions)

<details>
<summary>Click to expand original shard content</summary>

### 1.1 Purchase/Provision VPS

1. Log into Hostinger (hostinger.com)
2. Navigate to **Hosting** → **VPS Hosting**
3. Select **KVM 2** plan:
   - 2 vCPU
   - 8 GB RAM
   - 100 GB NVMe SSD
4. Choose **Ubuntu 24.04 64bit** as OS
5. Select datacenter closest to you
6. Complete purchase

### 1.2 Access VPS Information

Once provisioned:

- Go to **hPanel** → **VPS** → Select your VPS
- Note VPS IP Address and Root Password

### 1.3 Connect via SSH

```bash
ssh root@YOUR_VPS_IP
```

### 1.4 Initial Server Updates

```bash
apt update
apt upgrade -y
apt install -y curl wget git nano ufw
```

### 1.5 Configure Firewall

```bash
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 5678
ufw enable
```

</details>

---

**→ Next: Shard 02: n8n Installation (also complete)**
