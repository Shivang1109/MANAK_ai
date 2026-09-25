# 📚 ManakAI - Complete Commands Documentation

**Your one-stop guide for all terminal commands**

---

## 📖 **Documentation Files**

| File | Purpose | When to Use |
|------|---------|-------------|
| **START_COMMANDS.md** | Complete startup guide with all details | Starting services, detailed explanations |
| **QUICK_COMMANDS_CHEATSHEET.md** | One-page quick reference | Demo day, need fast command lookup |
| **TROUBLESHOOTING.md** | Problem-solution guide | When something isn't working |
| **DEMO_LOGIN_CREDENTIALS.md** | Login accounts and testing | Login issues, creating test users |
| **DEMO_QUESTIONS.md** | Test questions and validation | Testing queries, demo preparation |

---

## 🚀 **Quick Start (30 Seconds)**

```bash
# Terminal 1
cd /Users/shivangpathak/SIH-2026/rag-service && \
export PYTHONPATH="$PWD/src:$PYTHONPATH" && \
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m uvicorn main:app --port 8000

# Terminal 2 (wait 10 seconds after Terminal 1)
cd /Users/shivangpathak/SIH-2026/backend-api && mvn spring-boot:run

# Terminal 3 (wait 60 seconds after Terminal 2)
cd /Users/shivangpathak/SIH-2026/frontend && npm run dev

# Then open: http://localhost:5173
# Login: demo / demo123
```

---

## 📋 **Most Used Commands**

### Start Services:
```bash
# See START_COMMANDS.md for details
./START_ALL_SERVICES.sh  # If script exists
# Or manually start each in separate terminals
```

### Stop Services:
```bash
lsof -ti:8000,8080,5173 | xargs kill -9
```

### Check Status:
```bash
curl http://localhost:8000/health && \
curl http://localhost:8080/api/auth/health && \
curl http://localhost:5173
```

### Test Login:
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'
```

### Test Chat:
```bash
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}' | jq -r '.token')

curl -X POST http://localhost:8080/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"What are LED lamp safety requirements?","conversationId":null}'
```

---

## 🎯 **Use Cases**

### "I need to start the system"
→ Read **START_COMMANDS.md**

### "Services are running, need quick command"
→ Use **QUICK_COMMANDS_CHEATSHEET.md**

### "Something is broken"
→ Check **TROUBLESHOOTING.md**

### "Can't login"
→ See **DEMO_LOGIN_CREDENTIALS.md**

### "Need test questions for demo"
→ Use **DEMO_QUESTIONS.md**

---

## 🔥 **Emergency Commands**

### Nuclear Option (Reset Everything):
```bash
# Stop all
lsof -ti:8000,8080,5173 | xargs kill -9

# Restart PostgreSQL
brew services restart postgresql@14

# Wait 5 seconds
sleep 5

# Restart all services
# (See START_COMMANDS.md for full restart procedure)
```

### Quick Health Check:
```bash
echo "RAG: $(curl -s http://localhost:8000/health | jq -r '.status')"
echo "Backend: $(curl -s http://localhost:8080/api/auth/health | jq -r '.status')"
echo "Frontend: $(curl -Is http://localhost:5173 | head -1)"
```

---

## 📱 **Important URLs**

```
Frontend:    http://localhost:5173
Backend:     http://localhost:8080
RAG API:     http://localhost:8000
API Docs:    http://localhost:8000/docs
```

---

## 🔐 **Demo Credentials**

```
Username: demo
Password: demo123
```

See **DEMO_LOGIN_CREDENTIALS.md** for more accounts.

---

## 🧪 **Pre-Demo Checklist**

Run this 10 minutes before demo:

```bash
# 1. All services running?
curl -f http://localhost:8000/health || echo "❌ RAG FAILED"
curl -f http://localhost:8080/api/auth/health || echo "❌ Backend FAILED"
curl -f http://localhost:5173 || echo "❌ Frontend FAILED"

# 2. Can login?
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}' | grep -q "token" && \
  echo "✅ Login OK" || echo "❌ Login FAILED"

# 3. Can query?
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}' | jq -r '.token')

curl -X POST http://localhost:8080/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"LED safety?","conversationId":null}' | grep -q "answer" && \
  echo "✅ Chat OK" || echo "❌ Chat FAILED"

echo "=== Pre-Demo Check Complete ==="
```

---

## 📚 **Full Documentation Structure**

```
/Users/shivangpathak/SIH-2026/
│
├── START_COMMANDS.md              ← Complete startup guide
├── QUICK_COMMANDS_CHEATSHEET.md   ← One-page reference
├── TROUBLESHOOTING.md             ← Problem solutions
├── DEMO_LOGIN_CREDENTIALS.md      ← Login info
├── DEMO_QUESTIONS.md              ← Test questions
├── DEMO_PREPARATION_CHECKLIST.md  ← Demo prep tasks
├── WHY_THIS_ANSWER_FEATURE.md     ← Feature explanation
│
├── START_ALL_SERVICES.sh          ← Auto-start script
├── STOP_ALL_SERVICES.sh           ← Auto-stop script
├── check_all_ports.sh             ← Status check script
│
└── README_COMMANDS.md             ← This file (index)
```

---

## 💡 **Tips for Demo Day**

1. **Print or save** QUICK_COMMANDS_CHEATSHEET.md for quick reference
2. **Bookmark** http://localhost:5173 in browser
3. **Test login** with demo/demo123 before judges arrive
4. **Have** TROUBLESHOOTING.md open in another tab
5. **Run** pre-demo checklist 10 minutes before
6. **Keep** terminal windows organized (label them!)
7. **Backup plan**: Have screenshots/video ready

---

## 🆘 **Quick Help**

**Command not working?**
1. Check TROUBLESHOOTING.md
2. Verify service is running: `lsof -i :PORT`
3. Check logs: `tail -f logs/*.log`
4. Try restart: Kill and restart service

**Service won't start?**
1. Kill existing process: `lsof -ti:PORT | xargs kill -9`
2. Check port free: `lsof -i :PORT` (should show nothing)
3. Check logs for errors
4. Try again

**Demo not working?**
1. Restart everything
2. Test with demo questions from DEMO_QUESTIONS.md
3. Use demo/demo123 login
4. Check all 3 services are running

---

## ✅ **Success Indicators**

When everything is working:
- ✅ 3 terminal windows showing running services
- ✅ Health checks return "healthy"
- ✅ Can login with demo/demo123
- ✅ Can ask questions and get answers
- ✅ Response time < 5 seconds
- ✅ Sources shown with IS numbers
- ✅ "Why this answer?" button works

---

## 📞 **Command Categories**

| Category | File |
|----------|------|
| Starting/Stopping | START_COMMANDS.md |
| Testing | QUICK_COMMANDS_CHEATSHEET.md |
| Database | START_COMMANDS.md (Database section) |
| Troubleshooting | TROUBLESHOOTING.md |
| Demo Prep | DEMO_PREPARATION_CHECKLIST.md |
| Login/Auth | DEMO_LOGIN_CREDENTIALS.md |

---

**🎉 You're all set! Pick the right file for what you need!**

**⚡ For demo day → Use QUICK_COMMANDS_CHEATSHEET.md**

**📖 For learning → Read START_COMMANDS.md**

**🔧 For problems → Check TROUBLESHOOTING.md**
