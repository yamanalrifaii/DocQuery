#!/bin/bash

# RAG QA System Startup Script
# Starts both backend and frontend servers

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 RAG QA System Startup${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env and add your OpenAI API key${NC}"
    echo ""
fi

# Check if OpenAI key is set
if grep -q "your_openai_key_here" .env; then
    echo -e "${RED}❌ OpenAI API key not set in .env${NC}"
    echo -e "${YELLOW}Please edit .env and add your OpenAI API key${NC}"
    exit 1
fi

# Setup backend
echo -e "${GREEN}Setting up backend...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Check if requirements are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt > /dev/null 2>&1
fi

# Setup frontend
echo -e "${GREEN}Setting up frontend...${NC}"
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing Node dependencies..."
    cd frontend
    npm install > /dev/null 2>&1
    cd ..
fi

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""

# Start services
echo -e "${YELLOW}Starting services...${NC}"
echo ""

# Backend
echo -e "${GREEN}Backend:${NC} http://localhost:8000"
echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Start backend in background
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Start frontend
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Wait for both processes
wait

# Cleanup
kill $BACKEND_PID 2>/dev/null || true
kill $FRONTEND_PID 2>/dev/null || true
