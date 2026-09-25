# 🔧 ManakAI - Troubleshooting Guide

**Common problems and their solutions**

---

## 🚨 **Problem: Services won't start**

### RAG Service (Port 8000) not starting

**Symptoms:**
- `Address already in use` error
- Port 8000 is occupied

**Solutions:**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
lsof -ti:8000 | xargs kill -9

# Try starting again
cd /Users/shivangpathak/SIH-2026/rag-service
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m uvicorn main:app --port 8000
```

---

### Backend (Port 8080) not starting

**Symptoms:**
- `Port 8080 already in use`
- Maven build fails

**Solutions:**
```bash
# Kill existing process
lsof -ti:8080 | xargs kill -9

# Clean and rebuild
cd /Users/shivangpathak/SIH-2026/backend-api
mvn clean install -DskipTests

# Start again
mvn spring-boot:run
```

---

### Frontend (Port 5173) not starting

**Symptoms:**
- `EADDRINUSE` error
- Vite fails to start

**Solutions:**
```bash
# Kill existing process
lsof -ti:5173 | xargs kill -9

# Reinstall dependencies if needed
cd /Users/shivangpathak/SIH-2026/frontend
rm -rf node_modules package-lock.json
npm install

# Start again
npm run dev
```

---

## 🔐 **Problem: Login not working**

### "Invalid username or password"

**Cause:** Password incorrect or user doesn't exist

**Solutions:**
```bash
# Option 1: Use demo account
Username: demo
Password: demo123

# Option 2: Check if user exists
psql -d manakai -c "SELECT username, email FROM users WHERE username='yourusername';"

# Option 3: Create new account
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser","email":"new@test.com","password":"newpass123"}'
```

---

### "Cannot connect to backend"

**Cause:** Backend not running or wrong URL

**Solutions:**
```bash
# Check backend is running
curl http://localhost:8080/api/auth/health

# If not running, start it
cd /Users/shivangpathak/SIH-2026/backend-api
mvn spring-boot:run

# Check frontend is pointing to correct URL
# File: frontend/src/services/api.ts
# Should have: baseURL: 'http://localhost:8080/api'
```

---

## 💬 **Problem: Chat not responding**

### Queries timeout or return errors

**Symptoms:**
- Spinning loader never stops
- "Request timeout" error
- Empty responses

**Solutions:**

**Step 1: Check RAG service**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}

# If not, restart RAG service
lsof -ti:8000 | xargs kill -9
cd /Users/shivangpathak/SIH-2026/rag-service
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m uvicorn main:app --port 8000
```

**Step 2: Check ChromaDB loaded**
```bash
curl http://localhost:8000/api/collection/stats
# Should show: total_documents > 0

# If 0, reload data
cd /Users/shivangpathak/SIH-2026/rag-service
python scripts/load_csvs.py
```

**Step 3: Check backend can reach RAG**
```bash
# Look at backend logs for connection errors
tail -f /Users/shivangpathak/SIH-2026/backend-api/logs/*.log
```

**Step 4: Test query directly**
```bash
# Test RAG service directly
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What are LED lamp requirements?"}'

# Should return answer with sources
```

---

### "No sources found"

**Cause:** Query doesn't match any documents in ChromaDB

**Solutions:**
```bash
# Check what data is loaded
curl http://localhost:8000/api/collection/stats

# Check available topics
psql -d manakai -c "SELECT DISTINCT metadata->>'industry' FROM documents LIMIT 10;"

# Try queries from DEMO_QUESTIONS.md - those are guaranteed to work

# Example working queries:
- "What are LED lamp safety requirements?"
- "ECG equipment testing standards?"
- "IS 10500 drinking water quality?"
- "Concrete strength requirements IS 456?"
```

---

## 📊 **Problem: Database issues**

### "Database connection failed"

**Symptoms:**
- Backend can't connect to PostgreSQL
- `Connection refused` errors

**Solutions:**
```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# If not running, start it
brew services start postgresql@14

# Wait 5 seconds, then restart backend
cd /Users/shivangpathak/SIH-2026/backend-api
mvn spring-boot:run
```

---

### "Table does not exist"

**Symptoms:**
- SQL errors about missing tables
- Fresh database setup

**Solutions:**
```bash
# Check if database exists
psql -l | grep manakai

# If doesn't exist, create it
createdb manakai

# Backend will auto-create tables on first run
cd /Users/shivangpathak/SIH-2026/backend-api
mvn spring-boot:run
```

---

### "Duplicate key error"

**Symptoms:**
- Can't register same username/email twice

**Solutions:**
```bash
# Use different username/email
# Or delete existing user
psql -d manakai -c "DELETE FROM users WHERE username='duplicate_username';"
```

---

## 🔍 **Problem: ChromaDB issues**

### "Collection not found"

**Cause:** ChromaDB not initialized or corrupted

**Solutions:**
```bash
# Check ChromaDB directory exists
ls -la /Users/shivangpathak/SIH-2026/rag-service/data/chroma_db

# If empty or corrupted, reload data
cd /Users/shivangpathak/SIH-2026/rag-service
python scripts/load_csvs.py

# Wait for completion (takes 5-10 minutes for all CSVs)
```

---

### "Embedding model not loaded"

**Symptoms:**
- First query is very slow (>30 seconds)
- "Model loading" errors

**Solutions:**
```bash
# Wait for model to fully load (first startup takes ~10 seconds)
# Check RAG logs
tail -f /Users/shivangpathak/SIH-2026/rag-service/logs/*.log

# Should see: "Loaded sentence transformer model"

# If model fails to load, check Python packages
cd /Users/shivangpathak/SIH-2026/rag-service
pip install -r requirements.txt
```

---

## 🌐 **Problem: CORS errors**

### "Access-Control-Allow-Origin" errors

**Symptoms:**
- Browser console shows CORS errors
- Frontend can't call backend

**Solutions:**
```bash
# Check backend CORS configuration
# File: backend-api/src/main/resources/application.yml
# Should have:
# manakai:
#   cors:
#     allowed-origins: http://localhost:5173

# If changed, restart backend
cd /Users/shivangpathak/SIH-2026/backend-api
mvn spring-boot:run
```

---

## ⚡ **Problem: Slow responses**

### Queries take > 10 seconds

**Causes & Solutions:**

**1. First query is always slow (model loading)**
- Normal: First query takes 10-15 seconds
- Subsequent queries should be < 5 seconds

**2. Too many documents retrieved**
```bash
# Check RAG config
# File: rag-service/config/rag_config.yaml
# Reduce top_k value if needed:
# retrieval:
#   top_k: 5  # Try reducing to 3
```

**3. Database query slow**
```bash
# Check PostgreSQL connections
psql -d manakai -c "SELECT count(*) FROM pg_stat_activity WHERE datname='manakai';"

# Should be < 10 connections
# If many connections, restart backend
```

**4. ChromaDB performance**
```bash
# Check ChromaDB size
du -sh /Users/shivangpathak/SIH-2026/rag-service/data/chroma_db

# If > 1GB, consider:
# - Reducing document count
# - Using smaller embedding model
# - Adding indexes
```

---

## 🖥️ **Problem: Frontend display issues**

### Blank page / White screen

**Solutions:**
```bash
# Check browser console for errors (F12)

# Clear browser cache
# Chrome: Cmd+Shift+Delete

# Rebuild frontend
cd /Users/shivangpathak/SIH-2026/frontend
rm -rf node_modules .vite dist
npm install
npm run dev
```

---

### "Why this answer?" not working

**Symptoms:**
- Button doesn't appear
- Panel doesn't open
- No sources shown

**Solutions:**
```bash
# Check if sources are being sent from backend
# Look at network tab in browser (F12)
# Check /api/chat response has "sources" array

# If sources empty, check RAG service
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query":"LED safety?"}'

# Should return sources with metadata
```

---

## 🔋 **Problem: High CPU/Memory usage**

### RAG Service using too much memory

**Solutions:**
```bash
# Check memory usage
ps aux | grep uvicorn

# Reduce batch size in RAG config
# File: rag-service/config/rag_config.yaml
# Change batch_size to smaller value

# Restart RAG service
lsof -ti:8000 | xargs kill -9
cd /Users/shivangpathak/SIH-2026/rag-service
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m uvicorn main:app --port 8000
```

---

### Backend using too much CPU

**Solutions:**
```bash
# Check for infinite loops in logs
tail -f /Users/shivangpathak/SIH-2026/backend-api/logs/*.log

# Restart backend
lsof -ti:8080 | xargs kill -9
cd /Users/shivangpathak/SIH-2026/backend-api
mvn spring-boot:run
```

---

## 🚀 **Quick Reset Everything**

**When nothing works, reset all:**

```bash
# Stop all services
lsof -ti:8000,8080,5173 | xargs kill -9

# Wait
sleep 5

# Clear logs
rm -f /Users/shivangpathak/SIH-2026/rag-service/logs/*.log
rm -f /Users/shivangpathak/SIH-2026/backend-api/logs/*.log

# Restart PostgreSQL
brew services restart postgresql@14
sleep 5

# Start RAG service
cd /Users/shivangpathak/SIH-2026/rag-service
export PYTHONPATH="/Users/shivangpathak/SIH-2026/rag-service/src:$PYTHONPATH"
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m uvicorn main:app --port 8000 &
sleep 15

# Start backend
cd /Users/shivangpathak/SIH-2026/backend-api
mvn spring-boot:run &
sleep 60

# Start frontend
cd /Users/shivangpathak/SIH-2026/frontend
npm run dev &

echo "All services restarted! Check http://localhost:5173"
```

---

## 📞 **Still Having Issues?**

### Check logs systematically:

```bash
# 1. RAG Service logs
tail -50 /Users/shivangpathak/SIH-2026/rag-service/logs/*.log

# 2. Backend logs
tail -50 /Users/shivangpathak/SIH-2026/backend-api/logs/*.log

# 3. PostgreSQL logs
tail -50 /usr/local/var/log/postgresql@14.log

# 4. Browser console (F12 in browser)
```

### Verify each component:

```bash
# Test each service individually
echo "=== Testing RAG ===" && \
curl http://localhost:8000/health

echo "=== Testing Backend ===" && \
curl http://localhost:8080/api/auth/health

echo "=== Testing Database ===" && \
psql -d manakai -c "SELECT 1;"

echo "=== Testing Frontend ===" && \
curl -I http://localhost:5173
```

---

## ✅ **Prevention Tips**

1. **Always start in order:** RAG → Backend → Frontend
2. **Wait for each service** to fully start before starting next
3. **Check logs** regularly for warnings
4. **Use health endpoints** to verify status
5. **Test with demo account** before creating new users
6. **Use demo questions** first - they're guaranteed to work
7. **Backup database** before making changes
8. **Keep scripts handy** for quick restarts

---

**💡 Pro Tip:** Create a "demo_ready" script that runs all health checks automatically!

**🆘 Emergency Contact:** Check `START_COMMANDS.md` for full command reference
