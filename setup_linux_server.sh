#!/usr/bin/env bash
# ==============================================================================
# ManakAI - Complete Linux Server Setup & Installation Script
# Supported OS: Ubuntu 20.04 / 22.04 / 24.04 LTS, Debian 11 / 12
# Run as: sudo bash setup_linux_server.sh
# ==============================================================================

set -e

echo "=========================================================="
echo "🇮🇳  Setting up ManakAI Environment on Linux Server..."
echo "=========================================================="

# 1. Update APT repositories
echo "📦 [1/6] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# 2. Install System Dependencies & Build Tools
echo "📦 [2/6] Installing build-essential, git, curl, and tools..."
sudo apt install -y build-essential curl wget git lsof unzip software-properties-common

# 3. Install Java 17 & Maven (for Spring Boot Backend)
echo "☕ [3/6] Installing OpenJDK 17 and Maven..."
sudo apt install -y openjdk-17-jdk maven
java -version
mvn -version

# 4. Install Node.js 20.x & npm (for React Frontend)
echo "⚡ [4/6] Installing Node.js 20 LTS..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install -y nodejs
fi
node -v
npm -v

# 5. Install Python 3.11+, pip, and venv (for FastAPI RAG Service)
echo "🐍 [5/6] Installing Python 3, pip, and venv..."
sudo apt install -y python3 python3-pip python3-venv python3-dev
python3 --version

# 6. Install PostgreSQL & Set up Database
echo "🐘 [6/6] Installing PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib

# Configure Postgres User and Database
echo "   Configuring PostgreSQL database 'manakai'..."
sudo -u postgres psql -c "CREATE USER manakai_user WITH PASSWORD 'password';" || true
sudo -u postgres psql -c "CREATE DATABASE manakai OWNER manakai_user;" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE manakai TO manakai_user;" || true

# ==============================================================================
# Installing Project Package Dependencies
# ==============================================================================
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "----------------------------------------------------------"
echo "📥 Installing Frontend Dependencies (Node.js)..."
cd "$PROJECT_ROOT/frontend"
npm install

echo "----------------------------------------------------------"
echo "📥 Installing RAG Service Dependencies (Python)..."
cd "$PROJECT_ROOT/rag-service"
# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
# Install CPU-only torch to save disk space and bandwidth on server
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
deactivate

echo "----------------------------------------------------------"
echo "📥 Building Backend API (Spring Boot Maven)..."
cd "$PROJECT_ROOT/backend-api"
mvn clean package -DskipTests

echo "=========================================================="
echo "🎉 ALL PACKAGES & DEPENDENCIES INSTALLED SUCCESSFULLY!"
echo "=========================================================="
echo "To start services:"
echo "1. Activate python venv: source rag-service/venv/bin/activate"
echo "2. Run: ./start_all.sh"
echo "=========================================================="
