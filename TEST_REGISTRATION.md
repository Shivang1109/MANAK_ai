# 🔍 Registration Issue Investigation

## ✅ **What's Working:**

### Backend API:
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser123",
    "email": "test123@example.com",
    "password": "test123"
  }'
```

**Result:** ✅ **WORKS PERFECTLY**
```json
{
  "token": "eyJ...",
  "userId": "...",
  "username": "testuser123",
  "email": "test123@example.com",
  "role": "USER"
}
```

---

## ⚠️ **Potential Issues:**

### 1. **Frontend Running on Different Port**

Your frontend is running on:
- **Port 3000** ✅ (Try: http://localhost:3000)
- **Port 3001** ✅ (Try: http://localhost:3001)

**NOT** on port 5173!

### 2. **Browser Console Errors**

Open browser console (F12) and check for:
- CORS errors
- Network errors
- API call failures

---

## 🔧 **How to Fix:**

### **Step 1: Find Correct Frontend URL**

```bash
# Check which port frontend is on
lsof -i -P | grep node | grep LISTEN

# Output shows:
# node on localhost:3000 (LISTEN)
# node on localhost:3001 (LISTEN)
```

**Try these URLs:**
1. http://localhost:3000
2. http://localhost:3001
3. http://localhost:5173

### **Step 2: Stop Duplicate Frontends**

```bash
# Kill all Vite processes
lsof -ti:3000,3001,5173 | xargs kill -9

# Start fresh
cd /Users/shivangpathak/SIH-2026/frontend
npm run dev
```

### **Step 3: Check Frontend Logs**

```bash
cd /Users/shivangpathak/SIH-2026/frontend

# Look at terminal where npm run dev is running
# Should show:
# VITE v5.x.x  ready in XXX ms
# ➜  Local:   http://localhost:XXXX/
```

---

## 🧪 **Test Registration Step-by-Step:**

### 1. **Open Browser DevTools (F12)**

### 2. **Go to Network Tab**

### 3. **Try Registration:**
- Username: `testuser999`
- Email: `test999@test.com`
- Password: `test123`
- Confirm: `test123`

### 4. **Check Network Request:**

**Look for POST to `/api/auth/register`:**

**If status 200:** Registration worked, frontend issue

**If status 400/500:** Backend error, check response

**If no request:** Frontend not sending, check console errors

---

## 🔍 **Common Issues & Solutions:**

### **Issue 1: "Network Error"**
**Cause:** Backend not reachable

**Fix:**
```bash
# Check backend running
curl http://localhost:8080/api/auth/health

# If not running, start it
cd /Users/shivangpathak/SIH-2026/backend-api
mvn spring-boot:run
```

---

### **Issue 2: "Username already exists"**
**Cause:** User already registered

**Fix:**
```bash
# Use different username
# Or delete existing user
psql -d manakai -c "DELETE FROM users WHERE username='testuser';"
```

---

### **Issue 3: CORS Error**
**Cause:** Frontend/Backend port mismatch

**Fix:**
```bash
# Check backend CORS config
# File: backend-api/src/main/resources/application.yml
# Should have your frontend port in allowed-origins
```

---

### **Issue 4: "Passwords do not match"**
**Cause:** Frontend validation

**Fix:**
- Type same password in both fields
- Must be at least 6 characters

---

### **Issue 5: Email Validation**
**Cause:** Invalid email format

**Fix:**
- Use format: `name@domain.com`
- Must have @ and domain

---

## 🎯 **Quick Test (Works 100%):**

### **Method 1: Direct API Call (Bypasses Frontend)**

```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "quicktest",
    "email": "quick@test.com",
    "password": "test123"
  }'
```

**Then login with:**
- Username: `quicktest`
- Password: `test123`

---

### **Method 2: Use Demo Account**

**Skip registration, use existing account:**
- Username: `demo`
- Password: `demo123`

---

## 📊 **Diagnostic Commands:**

```bash
# 1. Check all services
echo "Backend:" && curl -s http://localhost:8080/api/auth/health | jq -r '.status'
echo "Frontend ports:" && lsof -i -P | grep node | grep LISTEN

# 2. Check database
psql -d manakai -c "SELECT COUNT(*) as total_users FROM users;"

# 3. Test registration
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"diagnostic","email":"diag@test.com","password":"test123"}' \
  && echo "✅ Backend registration works!"

# 4. Check logs
tail -20 /Users/shivangpathak/SIH-2026/backend-api/logs/*.log
```

---

## 🚨 **What Exact Error Are You Seeing?**

### **Error on screen says:**

1. **"Username already exists"**
   - Try different username
   - Or use demo/demo123

2. **"Network Error"** or **"Cannot connect"**
   - Check backend running: `curl http://localhost:8080/api/auth/health`
   - Restart backend if needed

3. **"Passwords do not match"**
   - Type carefully in both password fields
   - Must be same

4. **"Invalid email"**
   - Use proper format: name@domain.com

5. **Just loading forever / spinning**
   - Backend might be slow or not responding
   - Check backend logs
   - Restart backend

6. **"Registration failed. Please try again."**
   - Generic error
   - Check browser console (F12)
   - Look for actual error message

---

## ✅ **Immediate Solution:**

### **Option 1: Use Demo Account (Fastest)**
```
Username: demo
Password: demo123
```
Go to login page, use these credentials.

### **Option 2: Create via API**
```bash
# Create new user
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myuser",
    "email": "my@email.com",
    "password": "mypass123"
  }'

# Then login on frontend with: myuser / mypass123
```

### **Option 3: Fix Frontend**
1. Find correct frontend URL (check port)
2. Open browser DevTools (F12)
3. Try registration again
4. Check Console tab for errors
5. Check Network tab for failed requests

---

## 📞 **Tell Me:**

**What exact error message you're seeing?**
- Screenshot
- Text from error box
- Browser console error

**Then I can give exact solution!**

---

## 💡 **Pro Tip:**

**Frontend might be cached!**

Try:
1. Hard refresh: `Cmd + Shift + R` (Mac) or `Ctrl + Shift + R` (Windows)
2. Clear cache: Go to DevTools → Application → Clear storage
3. Restart frontend

```bash
# Kill and restart frontend
lsof -ti:3000,3001,5173 | xargs kill -9
cd /Users/shivangpathak/SIH-2026/frontend
npm run dev
```

---

**🎯 Most likely:** Frontend is on port 3000 or 3001, not 5173!

**Try:** http://localhost:3000 or http://localhost:3001
