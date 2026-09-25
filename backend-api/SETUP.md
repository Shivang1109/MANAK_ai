# Backend API Setup Guide

## Overview
Spring Boot backend that connects React frontend to FastAPI RAG service.

## Prerequisites

1. **Java 17+**
   ```bash
   java -version
   ```

2. **Maven 3.6+**
   ```bash
   mvn -version
   ```

3. **PostgreSQL 14+**
   ```bash
   # Install PostgreSQL (macOS)
   brew install postgresql@14
   brew services start postgresql@14
   ```

4. **RAG Service Running**
   - Must be running on http://localhost:8000
   - See `/rag-service/README_MILESTONE.md`

## Database Setup

### 1. Create Database

```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE manakai;
CREATE USER manakai_user WITH PASSWORD 'manakai_password';
GRANT ALL PRIVILEGES ON DATABASE manakai TO manakai_user;

# Exit
\q
```

### 2. Initialize Schema

```bash
cd /Users/shivangpathak/SIH-2026/backend-api

# Run schema SQL
psql -U manakai_user -d manakai -f src/main/resources/schema.sql
```

## Configuration

### 1. Environment Variables

Create `.env` file in `backend-api/` directory:

```bash
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=manakai
POSTGRES_USER=manakai_user
POSTGRES_PASSWORD=manakai_password

# JWT
JWT_SECRET=your-super-secret-jwt-key-minimum-256-bits-change-in-production

# RAG Service
RAG_SERVICE_URL=http://localhost:8000

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# Server
SERVER_PORT=8080
```

### 2. Load Environment Variables

```bash
# Export variables
export $(cat .env | xargs)

# Or use direnv (recommended)
brew install direnv
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
direnv allow
```

## Build & Run

### Option 1: Maven

```bash
cd /Users/shivangpathak/SIH-2026/backend-api

# Build
mvn clean package -DskipTests

# Run
mvn spring-boot:run
```

### Option 2: JAR

```bash
# Build JAR
mvn clean package -DskipTests

# Run JAR
java -jar target/backend-api-1.0.0.jar
```

### Option 3: IDE (IntelliJ/Eclipse)

1. Open project in IDE
2. Configure environment variables in Run Configuration
3. Run `ManakaiApplication.java`

## API Endpoints

Server runs on: http://localhost:8080/api

### Authentication

```bash
# Register
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'

# Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'

# Response includes JWT token
# Save token as: TOKEN="your-jwt-token-here"
```

### Chat

```bash
# Send message
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "query": "What are the cement strength requirements?",
    "conversationId": null
  }'

# Get conversations
curl -X GET http://localhost:8080/api/chat/conversations \
  -H "Authorization: Bearer $TOKEN"

# Get conversation history
curl -X GET http://localhost:8080/api/chat/history/{conversationId} \
  -H "Authorization: Bearer $TOKEN"

# Delete conversation
curl -X DELETE http://localhost:8080/api/chat/conversations/{conversationId} \
  -H "Authorization: Bearer $TOKEN"
```

### Feedback

```bash
# Submit feedback
curl -X POST http://localhost:8080/api/feedback \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "messageId": "message-uuid",
    "rating": 5,
    "comment": "Very helpful!",
    "feedbackType": "positive"
  }'

# Get my feedback
curl -X GET http://localhost:8080/api/feedback/my \
  -H "Authorization: Bearer $TOKEN"
```

### Health Checks

```bash
# Auth health
curl http://localhost:8080/api/auth/health

# Chat health
curl http://localhost:8080/api/chat/health

# Feedback health
curl http://localhost:8080/api/feedback/health

# Actuator health
curl http://localhost:8080/api/actuator/health
```

## Testing Full Flow

### 1. Start All Services

```bash
# Terminal 1: Start PostgreSQL
brew services start postgresql@14

# Terminal 2: Start RAG Service (with OpenAI API key)
cd /Users/shivangpathak/SIH-2026/rag-service
export OPENAI_API_KEY="sk-..."
python3 src/main.py

# Terminal 3: Start Backend API
cd /Users/shivangpathak/SIH-2026/backend-api
export $(cat .env | xargs)
mvn spring-boot:run
```

### 2. Test Authentication

```bash
# Register user
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "email": "demo@example.com",
    "password": "demo123"
  }'

# Expected: 201 Created with JWT token
```

### 3. Test Chat

```bash
# Login and get token
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "password": "demo123"
  }' | jq -r '.token')

# Send chat message
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "query": "What are the compressive strength requirements for cement?",
    "conversationId": null
  }' | jq

# Expected: Response with answer, sources, confidence
```

## Troubleshooting

### PostgreSQL Connection Issues

```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Test connection
psql -U manakai_user -d manakai -c "SELECT 1;"
```

### RAG Service Connection Issues

```bash
# Check if RAG service is running
curl http://localhost:8000/health

# Expected: {"status": "healthy", ...}
```

### Port Already in Use

```bash
# Check what's using port 8080
lsof -i :8080

# Kill process if needed
kill -9 <PID>
```

### JWT Token Invalid

- Ensure JWT_SECRET is set and consistent
- Token expires after 24 hours (configured in application.yml)
- Get new token with `/api/auth/login`

## Architecture

```
┌─────────────┐
│   React     │  ← Next step (Milestone 4)
│  Frontend   │
│  Port 3000  │
└──────┬──────┘
       │ HTTP + JWT
       ↓
┌─────────────┐
│ Spring Boot │  ← YOU ARE HERE (Milestone 3)
│   Backend   │
│  Port 8080  │
│             │
│ Components: │
│ - AuthController
│ - ChatController
│ - FeedbackController
│ - JWT Security
│ - PostgreSQL
└──────┬──────┘
       │ HTTP
       ↓
┌─────────────┐
│  FastAPI    │  ← Complete (Milestone 2)
│ RAG Service │
│  Port 8000  │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  ChromaDB   │  ← Complete (Milestone 1)
│  947 docs   │
└─────────────┘
```

## Project Structure

```
backend-api/
├── src/main/java/com/manakai/
│   ├── ManakaiApplication.java       # Main entry point
│   ├── config/
│   │   ├── SecurityConfig.java       # JWT + Security
│   │   ├── WebConfig.java            # CORS
│   │   └── RestTemplateConfig.java   # HTTP client
│   ├── controllers/                  # ✅ NEW
│   │   ├── AuthController.java       # /auth/register, /auth/login
│   │   ├── ChatController.java       # /chat
│   │   └── FeedbackController.java   # /feedback
│   ├── services/                     # ✅ NEW
│   │   ├── AuthService.java          # User auth logic
│   │   ├── ChatService.java          # RAG proxy + conversation mgmt
│   │   └── FeedbackService.java      # Feedback collection
│   ├── models/
│   │   ├── User.java
│   │   ├── Conversation.java
│   │   ├── Message.java
│   │   ├── QueryLog.java
│   │   └── Feedback.java
│   ├── dto/
│   │   ├── AuthResponse.java
│   │   ├── ChatRequest.java
│   │   ├── ChatResponse.java
│   │   ├── LoginRequest.java
│   │   ├── RegisterRequest.java
│   │   └── FeedbackRequest.java
│   ├── repositories/
│   │   ├── UserRepository.java
│   │   ├── ConversationRepository.java
│   │   ├── MessageRepository.java
│   │   ├── QueryLogRepository.java
│   │   └── FeedbackRepository.java
│   └── security/
│       ├── JwtUtil.java
│       ├── JwtAuthenticationFilter.java
│       └── UserDetailsServiceImpl.java
├── src/main/resources/
│   ├── application.yml               # Configuration
│   └── schema.sql                    # Database schema
└── pom.xml                           # Maven dependencies
```

## Next Steps

1. ✅ **Backend API** - Complete (you are here)
2. ⏳ **Frontend** - Build React UI (Milestone 4)
3. ⏳ **Deployment** - Docker Compose (Milestone 5)

---

**Status:** Backend API ready for testing with RAG service  
**Last Updated:** September 12, 2026
