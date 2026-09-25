# 🔐 ManakAI Demo Login Credentials

## ✅ **Working Demo Account**

```
Username: demo
Password: demo123
Email: demo@manakai.com
```

**Status:** ✅ Tested and Working!

---

## 🚀 **How to Login:**

### **Option 1: Use Demo Account** (Recommended)
1. Go to `http://localhost:5173`
2. Click "Login"
3. Enter:
   - Username: `demo`
   - Password: `demo123`
4. Click "Login"

### **Option 2: Register New Account**
1. Go to `http://localhost:5173`
2. Click "Register" or "Sign Up"
3. Fill in:
   - Username: (your choice)
   - Email: (your choice)
   - Password: (your choice - remember it!)
4. Click "Register"
5. Auto-login happens

---

## 🔧 **If Still Having Issues:**

### **Check Backend is Running:**
```bash
curl http://localhost:8080/api/auth/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "auth"
}
```

### **Check Frontend is Running:**
```bash
curl http://localhost:5173
```

**Should return:** HTML page

---

## 🧪 **Test Login Manually (Terminal):**

### **Test Registration:**
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123"
  }'
```

### **Test Login:**
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test123"
  }'
```

---

## 📊 **All Existing Users in Database:**

```sql
-- Run this to see all users:
psql -d manakai -c "SELECT username, email, role, created_at FROM users ORDER BY created_at DESC;"
```

**Current Users:**
1. `Saurabh` - saurabhtri621@gmail.com (password unknown)
2. `Rahul` - yarahul5777@gmail.com (password unknown)
3. `demo` - demo@manakai.com ✅ **Password: demo123**
4. Other test users (passwords unknown)

---

## ⚠️ **Why Other Users Don't Work:**

**Problem:** Password bhul gaye ya register karte waqt kuch aur enter kiya tha.

**Solution:** 
- Use `demo / demo123` account
- Or register fresh account

---

## 🎯 **For SIH Demo:**

### **Create Demo-Specific Account:**

```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "judge",
    "email": "judge@sih2026.com",
    "password": "sih2026"
  }'
```

**Then use:**
- Username: `judge`
- Password: `sih2026`

---

## 🔐 **Password Reset** (If Needed)

**Currently:** No password reset feature

**Workaround:** Create new account with different username

**Future:** Can add password reset via email

---

## ✅ **Quick Test:**

1. Backend running: `http://localhost:8080/api/auth/health` ✓
2. Frontend running: `http://localhost:5173` ✓
3. Login with: `demo / demo123` ✓
4. Should see chat interface ✓

---

**🎉 Demo Account Ready! Use `demo / demo123` to login!**
