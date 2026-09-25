# ⚡ ManakAI - Quick Commands Cheat Sheet

**One-page reference for all terminal commands**

---

## 🚀 **START SERVICES**

```bash
# Terminal 1 - RAG Service (Port 8000)
cd /Users/shivangpathak/SIH-2026/rag-service
export PYTHONPATH="/Users/shivangpathak/SIH-2026/rag-service/src:$PYTHONPATH"
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2 - Backend (Port 8080)
cd /Users/shivangpathak/SIH-2026/backend-api
mvn spring-boot:run

# Terminal 3 - Frontend (Port 5173)
cd /Users/shivangpathak/SIH-2026/frontend
npm run dev
```

---

## 🛑 **STOP SERVICES**

```bash
# Kill by port
lsof -ti:8000 | xargs kill -9  # RAG
lsof -ti:8080 | xargs kill -9  # Backend
lsof -ti:5173 | xargs kill -9  # Frontend

# Or use script
./STOP_ALL_SERVICES.sh
```

---

## ✅ **CHECK STATUS**

```bash
# Health checks
curl http://localhost:8000/health           # RAG
curl http://localhost:8080/api/auth/health  # Backend
curl http://localhost:5173                  # Frontend

# Check ports
lsof -i :8000  # RAG
lsof -i :8080  # Backend
lsof -i :5173  # Frontend
```

---

## 🔐 **LOGIN/REGISTER**

```bash
# Login (get token)
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'

# Register new user
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123"}'
```

**Demo Account:**
- Username: `demo`
- Password: `demo123`

---

## 💬 **TEST CHAT**

```bash
# Get token first
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}' | jq -r '.token')

# Send query
curl -X POST http://localhost:8080/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"What are LED lamp safety requirements?","conversationId":null}'
```

---

## 📊 **DATABASE**

```bash
# View users
psql -d manakai -c "SELECT username, email FROM users LIMIT 5;"

# Count records
psql -d manakai -c "SELECT COUNT(*) FROM users;"
psql -d manakai -c "SELECT COUNT(*) FROM conversations;"
psql -d manakai -c "SELECT COUNT(*) FROM messages;"

# Check DB size
psql -d manakai -c "SELECT pg_size_pretty(pg_database_size('manakai'));"
```

---

## 🔍 **CHROMADB**

```bash
# Stats
curl http://localhost:8000/api/collection/stats

# Check size
du -sh /Users/shivangpathak/SIH-2026/rag-service/data/chroma_db
```

---

## 📝 **LOGS**

```bash
# View logs
tail -f /Users/shivangpathak/SIH-2026/rag-service/logs/*.log
tail -f /Users/shivangpathak/SIH-2026/backend-api/logs/*.log

# Or inline logs
cd backend-api && mvn spring-boot:run  # Shows logs directly
```

---

## 🧪 **QUICK TESTS**

```bash
# 5 Test Questions
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login -H "Content-Type: application/json" -d '{"username":"demo","password":"demo123"}' | jq -r '.token')

# Q1
curl -s -X POST http://localhost:8080/api/chat -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"query":"LED lamp safety?","conversationId":null}' | jq -r '.answer'

# Q2
curl -s -X POST http://localhost:8080/api/chat -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"query":"ECG equipment testing?","conversationId":null}' | jq -r '.answer'

# Q3
curl -s -X POST http://localhost:8080/api/chat -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"query":"Drinking water quality IS 10500?","conversationId":null}' | jq -r '.answer'

# Q4 (Abstention test)
curl -s -X POST http://localhost:8080/api/chat -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"query":"Flying cars certification?","conversationId":null}' | jq -r '.answer'
```

---

## 🚨 **EMERGENCY RESTART**

```bash
# One-liner to restart everything
lsof -ti:8000,8080,5173 | xargs kill -9 && sleep 5 && \
cd /Users/shivangpathak/SIH-2026/rag-service && \
nohup /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m uvicorn main:app --port 8000 > rag.log 2>&1 & \
sleep 10 && \
cd /Users/shivangpathak/SIH-2026/backend-api && \
nohup mvn spring-boot:run > backend.log 2>&1 & \
sleep 60 && \
cd /Users/shivangpathak/SIH-2026/frontend && \
nohup npm run dev > frontend.log 2>&1 &
```

---

## 🎯 **PRE-DEMO CHECK**

```bash
# Run this 10 minutes before demo
echo "=== Checking Services ===" && \
curl -f http://localhost:8000/health && echo "✅ RAG OK" || echo "❌ RAG FAIL" && \
curl -f http://localhost:8080/api/auth/health && echo "✅ Backend OK" || echo "❌ Backend FAIL" && \
curl -f http://localhost:5173 && echo "✅ Frontend OK" || echo "❌ Frontend FAIL" && \
echo "=== Testing Login ===" && \
curl -s -X POST http://localhost:8080/api/auth/login -H "Content-Type: application/json" -d '{"username":"demo","password":"demo123"}' | jq -r '.token' && echo "✅ Login OK" || echo "❌ Login FAIL" && \
echo "=== All Systems Ready! ==="
```

---

## 📱 **URLS**

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8080 |
| RAG API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 🔧 **COMMON FIXES**

```bash
# Port already in use?
lsof -ti:8000 | xargs kill -9

# PostgreSQL not running?
brew services restart postgresql@14

# Frontend dependencies issue?
cd frontend && rm -rf node_modules && npm install

# Backend build issue?
cd backend-api && mvn clean install -DskipTests

# ChromaDB corrupted?
rm -rf rag-service/data/chroma_db && python scripts/load_csvs.py
```

---

## 🎬 **DEMO SCRIPT COMMANDS**

```bash
# Create judge account
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"judge","email":"judge@sih.com","password":"sih2026"}'

# Time a query (should be < 5 seconds)
time curl -s -X POST http://localhost:8080/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"LED safety requirements?","conversationId":null}'
```

---

## 💾 **BACKUP**

```bash
# Backup database
pg_dump manakai > ~/manakai_backup_$(date +%Y%m%d).sql

# Backup ChromaDB
tar -czf ~/chromadb_backup_$(date +%Y%m%d).tar.gz \
  /Users/shivangpathak/SIH-2026/rag-service/data/chroma_db
```

---

## 📦 **BUILD FOR PRODUCTION**

```bash
# Backend JAR
cd backend-api && mvn clean package -DskipTests

# Frontend build
cd frontend && npm run build

# Files ready:
# - backend-api/target/*.jar
# - frontend/dist/*
```

---

**💡 Pro Tip:** Bookmark this file for quick reference during demo!

**📋 Full commands:** See `START_COMMANDS.md` for detailed explanations
