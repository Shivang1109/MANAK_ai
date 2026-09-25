#!/usr/bin/env bash
# ==============================================================================
# ManakAI - Unified Launch Script
# Starts: RAG Service (8000), Backend API (8080), and Frontend (5173)
# ==============================================================================

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================================="
echo "🇮🇳  Starting ManakAI Platform Services..."
echo "=========================================================="

# 1. Kill any existing processes holding the ports
echo "🧹 Checking & clearing ports 8000, 8080, 5173..."
for port in 8000 8080 5173; do
    pid=$(lsof -ti :$port 2>/dev/null)
    if [ -n "$pid" ]; then
        echo "   Killing PID $pid on port $port"
        kill -9 $pid 2>/dev/null || true
    fi
done

# Cleanup function to kill all background jobs when Ctrl+C is pressed
cleanup() {
    echo -e "\n🛑 Stopping all ManakAI services..."
    trap - SIGINT SIGTERM EXIT
    kill $(jobs -p) 2>/dev/null || true
    for port in 8000 8080 5173; do
        lsof -ti :$port 2>/dev/null | xargs kill -9 2>/dev/null || true
    done
    echo "✅ All services stopped."
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# 2. Determine Python 3 executable (check local venv first, then Mac Python, then system python)
PYTHON_CMD="python3"
if [ -d "$PROJECT_ROOT/rag-service/venv" ] && [ -x "$PROJECT_ROOT/rag-service/venv/bin/python3" ]; then
    PYTHON_CMD="$PROJECT_ROOT/rag-service/venv/bin/python3"
elif [ -x "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3" ]; then
    PYTHON_CMD="/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"
else
    # Check if uvicorn is installed in global python3, if not create venv automatically
    if ! python3 -c "import uvicorn" 2>/dev/null; then
        echo "⚠️  uvicorn not found in system python. Setting up venv in rag-service..."
        python3 -m venv "$PROJECT_ROOT/rag-service/venv" || true
        if [ -x "$PROJECT_ROOT/rag-service/venv/bin/pip" ]; then
            "$PROJECT_ROOT/rag-service/venv/bin/pip" install --upgrade pip
            "$PROJECT_ROOT/rag-service/venv/bin/pip" install -r "$PROJECT_ROOT/rag-service/requirements.txt"
            PYTHON_CMD="$PROJECT_ROOT/rag-service/venv/bin/python3"
        else
            pip3 install uvicorn fastapi pydantic pydantic-settings chromadb google-genai sentence-transformers
        fi
    fi
fi

# 3. Start RAG Service (Port 8000)
echo "🚀 [1/3] Starting RAG Service on http://localhost:8000..."
(
    cd "$PROJECT_ROOT/rag-service"
    export PYTHONPATH="$PROJECT_ROOT/rag-service/src:$PYTHONPATH"
    exec "$PYTHON_CMD" -m uvicorn main:app --host 0.0.0.0 --port 8000
) &
RAG_PID=$!

# Wait for RAG service to be responsive
echo "   Waiting for RAG Service to initialize..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        echo "   ✅ RAG Service ready!"
        break
    fi
    sleep 1
done

# 4. Start Backend API (Port 8080)
echo "🚀 [2/3] Starting Spring Boot Backend API on http://localhost:8080..."
(
    cd "$PROJECT_ROOT/backend-api"
    export POSTGRES_DB=${POSTGRES_DB:-manakai}
    export POSTGRES_USER=${POSTGRES_USER:-manakai_user}
    export POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-password}
    export JWT_SECRET=${JWT_SECRET:-manakai-super-secret-jwt-key-for-sih-2026-demo-change-in-production}
    export RAG_SERVICE_URL=${RAG_SERVICE_URL:-http://localhost:8000}
    exec mvn spring-boot:run -Dspring-boot.run.profiles=local
) &
BACKEND_PID=$!

# 5. Start Frontend (Port 5173)
echo "🚀 [3/3] Starting React Frontend on http://localhost:5173..."
(
    cd "$PROJECT_ROOT/frontend"
    exec npm run dev
) &
FRONTEND_PID=$!

echo "=========================================================="
echo "🌟 All services launched in background!"
echo "   - Frontend: http://localhost:5173"
echo "   - Backend:  http://localhost:8080"
echo "   - RAG API:  http://localhost:8000"
echo "   - Press [Ctrl + C] in this window to stop everything."
echo "=========================================================="

# Keep script running and wait on all child processes
wait
