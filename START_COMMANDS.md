# 🚀 ManakAI - Individual Start Commands

Run these commands in **separate terminal windows/tabs**:

---

## Terminal 1: RAG Service (Port 8000)

```bash
cd /Users/shivangpathak/SIH-2026/rag-service
export PYTHONPATH="/Users/shivangpathak/SIH-2026/rag-service/src:$PYTHONPATH"
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Wait:** ~10 seconds for embedding model to load

---

## Terminal 2: Backend API (Port 8080)

```bash
cd /Users/shivangpathak/SIH-2026/backend-api
export POSTGRES_DB=manakai
export POSTGRES_USER=manakai_user
export POSTGRES_PASSWORD=password
mvn spring-boot:run
```

**Expected Output:**
```
Started ManakaiApplication in X.XXX seconds
```

**Wait:** ~45-60 seconds for Spring Boot to fully start

---

## Terminal 3: Frontend (Port 3000)

```bash
cd /Users/shivangpathak/SIH-2026/frontend
npm run dev
```

**Expected Output:**
```
VITE v5.x.x  ready in XXX ms
➜  Local:   http://localhost:3000/
```

**Wait:** ~5 seconds for Vite to start

---

## ✅ Verification

After starting all 3, run in a **4th terminal**:

```bash
cd /Users/shivangpathak/SIH-2026
./check_all_ports.sh
```

Expected: All 3 services should show ✅ ACTIVE

---

## 🛑 To Stop

Press `Ctrl+C` in each terminal window to stop that service.

Or run in any terminal:
```bash
cd /Users/shivangpathak/SIH-2026
./STOP_ALL_SERVICES.sh
```

---

## 📝 Start Order (Recommended)

1. **First:** Start RAG Service (Terminal 1) - Wait 10 seconds
2. **Second:** Start Backend API (Terminal 2) - Wait 60 seconds  
3. **Third:** Start Frontend (Terminal 3) - Wait 5 seconds
4. **Finally:** Open browser → http://localhost:3000

---

## 🔍 Troubleshooting

### RAG Service won't start?
```bash
# Check if port is already in use
lsof -i :8000

# Kill existing process
lsof -ti:8000 | xargs kill -9

# Try again
```

### Backend API won't start?
```bash
# Check if port is already in use
lsof -i :8080

# Kill existing process
lsof -ti:8080 | xargs kill -9

# Try again
```

### Frontend won't start?
```bash
# Check if port is already in use
lsof -i :3000

# Kill existing process
lsof -ti:3000 | xargs kill -9

# Try again
```

---

## 📊 Database Info

- **ChromaDB:** Already loaded with 4,029 chunks
- **PostgreSQL:** Auto-connects on backend startup
- **No manual setup needed!**

---

## 🌐 Access URLs

- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8080
- **RAG API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## 💡 Quick Test After Startup

```bash
# Test RAG Service
curl http://localhost:8000/health

# Test Backend API
curl http://localhost:8080/actuator/health

# Test Frontend
curl http://localhost:3000

# All should return 200 OK responses
```

---

---

## 🔐 **Login Credentials**

### Demo Account (Already Created):
```
Username: demo
Password: demo123
Email: demo@manakai.com
```

### Create New Account:
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "yourname",
    "email": "your@email.com",
    "password": "yourpassword"
  }'
```

---

## 📊 **Database Commands**

### View All Users:
```bash
psql -d manakai -c "SELECT username, email, role, created_at FROM users ORDER BY created_at DESC LIMIT 10;"
```

### Check ChromaDB Collection:
```bash
curl http://localhost:8000/api/collection/stats
```

### View Conversations:
```bash
psql -d manakai -c "SELECT id, title, created_at FROM conversations ORDER BY created_at DESC LIMIT 5;"
```

### Check Feedback:
```bash
psql -d manakai -c "SELECT * FROM feedback ORDER BY created_at DESC LIMIT 5;"
```

### Clear All Users (BE CAREFUL!):
```bash
psql -d manakai -c "TRUNCATE TABLE users CASCADE;"
```

---

## 🧪 **Testing Commands**

### Test RAG Service Query:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are LED lamp safety requirements?"
  }'
```

### Test Backend Chat:
```bash
# First login to get token
TOKEN=$(curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}' \
  | jq -r '.token')

# Then send chat message
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "query": "What are cement quality requirements?",
    "conversationId": null
  }'
```

### Test All Health Endpoints:
```bash
echo "=== RAG Service ===" && curl http://localhost:8000/health
echo -e "\n=== Backend API ===" && curl http://localhost:8080/api/auth/health
echo -e "\n=== Backend Actuator ===" && curl http://localhost:8080/actuator/health
```

---

## 🔍 **Monitoring Commands**

### Check All Running Processes:
```bash
ps aux | grep -E 'uvicorn|mvn|vite' | grep -v grep
```

### Check Port Usage:
```bash
lsof -i :8000  # RAG Service
lsof -i :8080  # Backend API
lsof -i :5173  # Frontend (Vite uses 5173, not 3000!)
```

### View RAG Service Logs:
```bash
tail -f /Users/shivangpathak/SIH-2026/rag-service/logs/*.log
```

### View Backend Logs:
```bash
tail -f /Users/shivangpathak/SIH-2026/backend-api/logs/*.log
```

### Monitor PostgreSQL Connections:
```bash
psql -d manakai -c "SELECT count(*) as active_connections FROM pg_stat_activity WHERE datname='manakai';"
```

---

## 🛠️ **Maintenance Commands**

### Rebuild Backend:
```bash
cd /Users/shivangpathak/SIH-2026/backend-api
mvn clean install -DskipTests
```

### Rebuild Frontend:
```bash
cd /Users/shivangpathak/SIH-2026/frontend
npm install
npm run build
```

### Reset ChromaDB (Delete All Data):
```bash
# BE CAREFUL! This deletes all your loaded documents
rm -rf /Users/shivangpathak/SIH-2026/rag-service/data/chroma_db/*
```

### Reload CSV Data to ChromaDB:
```bash
cd /Users/shivangpathak/SIH-2026/rag-service
python scripts/load_csvs.py
```

### Backup PostgreSQL Database:
```bash
pg_dump manakai > ~/manakai_backup_$(date +%Y%m%d).sql
```

### Restore PostgreSQL Database:
```bash
psql -d manakai < ~/manakai_backup_YYYYMMDD.sql
```

---

## 🚨 **Emergency Commands**

### Kill All ManakAI Processes:
```bash
# Kill RAG Service
lsof -ti:8000 | xargs kill -9

# Kill Backend API
lsof -ti:8080 | xargs kill -9

# Kill Frontend
lsof -ti:5173 | xargs kill -9

# Or use script
cd /Users/shivangpathak/SIH-2026
./STOP_ALL_SERVICES.sh
```

### Restart PostgreSQL:
```bash
brew services restart postgresql@14
```

### Check PostgreSQL Status:
```bash
brew services list | grep postgresql
```

### Start PostgreSQL if Stopped:
```bash
brew services start postgresql@14
```

---

## 📈 **Performance Commands**

### Check ChromaDB Size:
```bash
du -sh /Users/shivangpathak/SIH-2026/rag-service/data/chroma_db
```

### Check Database Size:
```bash
psql -d manakai -c "SELECT pg_size_pretty(pg_database_size('manakai'));"
```

### Count Documents in ChromaDB:
```bash
curl http://localhost:8000/api/collection/stats | jq '.total_documents'
```

### Count Users:
```bash
psql -d manakai -c "SELECT COUNT(*) as total_users FROM users;"
```

### Count Conversations:
```bash
psql -d manakai -c "SELECT COUNT(*) as total_conversations FROM conversations;"
```

### Count Messages:
```bash
psql -d manakai -c "SELECT COUNT(*) as total_messages FROM messages;"
```

---

## 🎯 **Demo-Specific Commands**

### Create Demo Users:
```bash
# Judge account
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"judge","email":"judge@sih.com","password":"sih2026"}'

# Team account
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"team","email":"team@sih.com","password":"team2026"}'
```

### Test 5 Demo Questions:
```bash
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}' | jq -r '.token')

# Q1: LED Safety
curl -X POST http://localhost:8080/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"What are LED lamp safety requirements?","conversationId":null}'

# Q2: ECG Testing
curl -X POST http://localhost:8080/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"ECG equipment testing standards?","conversationId":null}'

# Q3: Water Quality
curl -X POST http://localhost:8080/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"IS 10500 drinking water quality?","conversationId":null}'

# Q4: Concrete Strength
curl -X POST http://localhost:8080/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"Concrete strength requirements IS 456?","conversationId":null}'

# Q5: Abstention Test
curl -X POST http://localhost:8080/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"Is BIS certification mandatory for flying cars?","conversationId":null}'
```

---

## 🔄 **Quick Restart All Services**

```bash
# Stop all
lsof -ti:8000 | xargs kill -9
lsof -ti:8080 | xargs kill -9
lsof -ti:5173 | xargs kill -9

# Wait 5 seconds
sleep 5

# Start RAG Service
cd /Users/shivangpathak/SIH-2026/rag-service
export PYTHONPATH="/Users/shivangpathak/SIH-2026/rag-service/src:$PYTHONPATH"
nohup /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 > rag.log 2>&1 &

# Wait 10 seconds
sleep 10

# Start Backend
cd /Users/shivangpathak/SIH-2026/backend-api
nohup mvn spring-boot:run > backend.log 2>&1 &

# Wait 60 seconds
sleep 60

# Start Frontend
cd /Users/shivangpathak/SIH-2026/frontend
nohup npm run dev > frontend.log 2>&1 &

echo "All services starting... Check logs in rag.log, backend.log, frontend.log"
```

---

## 📱 **Access URLs Summary**

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | Main UI |
| **Backend API** | http://localhost:8080 | REST API |
| **RAG Service** | http://localhost:8000 | Python RAG Engine |
| **RAG API Docs** | http://localhost:8000/docs | Swagger UI |
| **Backend Health** | http://localhost:8080/api/auth/health | Health Check |
| **RAG Health** | http://localhost:8000/health | Health Check |

---

## 🎓 **Git Commands** (If Needed)

### Save Current State:
```bash
cd /Users/shivangpathak/SIH-2026
git add .
git commit -m "Working demo version"
git push origin main
```

### View Changes:
```bash
git status
git diff
```

### Discard Changes:
```bash
git reset --hard HEAD
```

---

## 📦 **Package/Build for Demo**

### Build Backend JAR:
```bash
cd /Users/shivangpathak/SIH-2026/backend-api
mvn clean package -DskipTests
# JAR will be in target/ folder
```

### Build Frontend for Production:
```bash
cd /Users/shivangpathak/SIH-2026/frontend
npm run build
# Build files will be in dist/ folder
```

---

## 🎬 **Pre-Demo Checklist Commands**

Run these 1 hour before demo:

```bash
# 1. Check all services
curl http://localhost:8000/health
curl http://localhost:8080/api/auth/health
curl http://localhost:5173

# 2. Test login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'

# 3. Test chat query
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}' | jq -r '.token')

curl -X POST http://localhost:8080/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"What are LED lamp safety requirements?","conversationId":null}'

# 4. Check response time (should be < 5 seconds)
time curl -X POST http://localhost:8080/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"ECG equipment testing?","conversationId":null}'

# 5. Verify ChromaDB loaded
curl http://localhost:8000/api/collection/stats

# 6. Check database users
psql -d manakai -c "SELECT count(*) FROM users;"

echo "✅ All checks passed! Ready for demo!"
```

---

**Happy Coding! 🎉**

**Need help? Check logs or run health checks above!**
