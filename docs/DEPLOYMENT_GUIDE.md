# 🚀 ManakAI Production & Demo Deployment Guide

This guide covers everything you need to deploy ManakAI for the **Smart India Hackathon (SIH 2026)** demo or production evaluation.

---

## 🏗️ Architecture in Docker

```
                               Internet / Browser
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │   Frontend (Port 80/3000) │  Nginx (Static SPA)
                        │   - Routes: /             │
                        │   - Proxy:  /api/* ───────┼────────┐
                        └───────────────────────────┘        │
                                                             ▼
                                                ┌───────────────────────────┐
                                                │   Backend API (Port 8080) │  Spring Boot 3.2
                                                │   - Auth, JWT, History    │
                                                └─────────┬──────────┬──────┘
                                                          │          │
                                             Internal API │          │ JDBC
                                                          ▼          ▼
                        ┌───────────────────────────┐      ┌───────────────────────────┐
                        │   RAG Service (Port 8000) │      │   PostgreSQL (Port 5432)  │
                        │   - FastAPI + ChromaDB    │      │   - Users & Logs DB       │
                        │   - Gemini 2.0 Flash      │      └───────────────────────────┘
                        └───────────────────────────┘
```

---

## ⚡ Option 1: One-Command Deployment (Docker Compose)

### 1. Requirements
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Mac/Windows) OR Docker Engine & Docker Compose (Linux).

### 2. Verify `.env` File
Ensure your `.env` file in the project root has your Gemini API key:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Build & Launch Everything
Run the following in the project root:
```bash
# Build images and start all 4 containers in the background
docker compose up -d --build
```

### 4. Verify Services
```bash
# Check status of containers
docker compose ps

# View live logs across all services
docker compose logs -f

# View logs for a specific service
docker compose logs -f rag-service
docker compose logs -f backend-api
```

### 5. Access the Platform
* **Web UI (Frontend):** [http://localhost:3000](http://localhost:3000) or [http://localhost](http://localhost)
* **Backend API Docs / Health:** [http://localhost:8080/api/actuator/health](http://localhost:8080/api/actuator/health)
* **RAG Service Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ☁️ Option 2: Deploying to a Cloud VM / VPS (AWS EC2 / DigitalOcean / GCP)

This provides a permanent public IP or domain name for evaluators and judges.

### Recommended VM Specs:
* **OS:** Ubuntu 22.04 LTS or 24.04 LTS
* **RAM:** Minimum 4 GB (or 2 GB RAM + 2 GB Swap file)
* **vCPU:** 2 vCPU

### Step-by-Step Server Setup:
1. **Connect to your server via SSH:**
   ```bash
   ssh ubuntu@<YOUR_SERVER_IP>
   ```

2. **Install Docker & Git on the server:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y git curl docker.io docker-compose-v2
   sudo systemctl enable --now docker
   sudo usermod -aG docker $USER
   # Log out and log back in so group changes take effect:
   exit
   ```

3. **Clone your repository & launch:**
   ```bash
   ssh ubuntu@<YOUR_SERVER_IP>
   git clone <YOUR_GIT_REPO_URL>
   cd SIH-2026

   # Copy and edit .env
   cp .env.example .env
   nano .env # Paste your GOOGLE_API_KEY

   # Launch everything
   docker compose up -d --build
   ```

4. **Open Firewall Ports in your Cloud Security Group:**
   Ensure inbound rules allow:
   * **Port 80 (HTTP)**
   * **Port 443 (HTTPS)**
   * **Port 22 (SSH)**

5. **(Optional) Add Free SSL via Certbot & Domain:**
   If you have a domain pointed to `<YOUR_SERVER_IP>`:
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

---

## 🛡️ Option 3: Hackathon Failsafe (Instant Cloudflare Tunnel)

If you are presenting at a venue with restricted Wi-Fi, or need an **instant public HTTPS URL** from your laptop without paying for cloud servers:

1. Install `cloudflared`:
   * **Mac:** `brew install cloudflared`
   * **Linux:** `sudo apt install cloudflared`
   * **Windows:** `winget install Cloudflare.cloudflared`

2. Start ManakAI (either via Docker or `./start_all.sh`).

3. Run the tunnel command:
   ```bash
   cloudflared tunnel --url http://localhost:3000
   ```

4. It will print a URL like:
   ```
   https://random-words-here.trycloudflare.com
   ```
   * Open this URL on your phone or share it with judges.
   * Traffic tunnels securely through Cloudflare's global edge straight to your local machine with full HTTPS and no port-forwarding needed!

---

## 🛠️ Useful Operations & Maintenance

| Action | Command |
| :--- | :--- |
| **Stop all services** | `docker compose down` |
| **Stop and wipe database (Clean reset)** | `docker compose down -v` |
| **Restart a single service** | `docker compose restart rag-service` |
| **Inspect database directly** | `docker exec -it manakai-postgres psql -U manakai_user -d manakai` |
| **Re-index ChromaDB data inside container** | `docker exec -it manakai-rag-service python add_expanded_demo_data.py` |
