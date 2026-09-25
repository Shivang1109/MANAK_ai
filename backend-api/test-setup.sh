#!/bin/bash

# ManakAI Backend API - Setup Test Script
# This script tests if the backend can be built successfully

set -e  # Exit on error

echo "=================================="
echo "ManakAI Backend API - Setup Test"
echo "=================================="
echo ""

# Check Java
echo "✓ Checking Java installation..."
if ! command -v java &> /dev/null; then
    echo "❌ Java not found. Please install Java 17+"
    exit 1
fi
java -version
echo ""

# Check Maven
echo "✓ Checking Maven installation..."
if ! command -v mvn &> /dev/null; then
    echo "❌ Maven not found. Please install Maven 3.6+"
    exit 1
fi
mvn -version
echo ""

# Check PostgreSQL
echo "✓ Checking PostgreSQL installation..."
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found. Install with: brew install postgresql@14"
    echo "   (Not critical for build test, but needed for runtime)"
else
    psql --version
fi
echo ""

# Build project
echo "✓ Building Spring Boot application..."
echo "   (This may take a few minutes on first run)"
cd "$(dirname "$0")"
mvn clean compile -q

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed!"
    exit 1
fi
echo ""

# Check for controllers
echo "✓ Verifying controllers exist..."
CONTROLLERS=(
    "src/main/java/com/manakai/controllers/AuthController.java"
    "src/main/java/com/manakai/controllers/ChatController.java"
    "src/main/java/com/manakai/controllers/FeedbackController.java"
)

for controller in "${CONTROLLERS[@]}"; do
    if [ -f "$controller" ]; then
        echo "   ✓ $(basename $controller)"
    else
        echo "   ❌ $(basename $controller) missing!"
        exit 1
    fi
done
echo ""

# Check for services
echo "✓ Verifying services exist..."
SERVICES=(
    "src/main/java/com/manakai/services/AuthService.java"
    "src/main/java/com/manakai/services/ChatService.java"
    "src/main/java/com/manakai/services/FeedbackService.java"
)

for service in "${SERVICES[@]}"; do
    if [ -f "$service" ]; then
        echo "   ✓ $(basename $service)"
    else
        echo "   ❌ $(basename $service) missing!"
        exit 1
    fi
done
echo ""

# Summary
echo "=================================="
echo "✅ BACKEND API READY"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Setup PostgreSQL database (see SETUP.md)"
echo "2. Create .env file from .env.example"
echo "3. Start RAG service (port 8000)"
echo "4. Run: mvn spring-boot:run"
echo ""
echo "Full guide: backend-api/SETUP.md"
