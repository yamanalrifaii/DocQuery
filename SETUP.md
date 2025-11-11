# Setup Guide

Complete step-by-step guide to get the RAG QA System running.

## Quick Start (5 minutes)

### 1. Get OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API keys section
4. Create new secret key
5. Copy and save it (you won't see it again)

### 2. Backend Setup

```bash
# Navigate to project
cd qa-system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your OpenAI key
# Open .env in editor and set:
# OPENAI_API_KEY=sk-your-key-here

# Start backend
cd backend
python main.py
```

Server should start at `http://localhost:8000`

### 3. Frontend Setup (New Terminal)

```bash
cd qa-system/frontend

npm install

npm start
```

Open `http://localhost:3000` in browser

## Detailed Setup

### Backend Requirements

- Python 3.10 or higher
- pip (Python package manager)
- At least 4GB RAM (for embeddings)
- OpenAI API key (free trial available)

### Frontend Requirements

- Node.js 16 or higher
- npm (comes with Node.js)

### Optional: GPU Support

For faster embeddings (if you have CUDA):

```bash
pip uninstall faiss-cpu
pip install faiss-gpu
```

## Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# Required
OPENAI_API_KEY=sk-...

# Optional
MODEL_NAME=gpt-3.5-turbo
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Backend Config

Edit `backend/config.py`:

```python
# Chunk size for document splitting
chunk_size: int = 1000

# Overlap between chunks for context
chunk_overlap: int = 200

# Number of documents to retrieve
max_documents: int = 50
```

## Verification

### Test Backend

```bash
# In new terminal
curl http://localhost:8000/status

# Should return:
# {"initialized":false,"documents_indexed":0,"message":"No documents indexed yet"}
```

### Test Frontend

Visit `http://localhost:3000` - should see the RAG QA interface

## First Test

1. Open web UI at `http://localhost:3000`
2. Create a test file `test.txt`:
   ```
   The capital of France is Paris.
   Paris is located in the north-central part of France.
   It is known for the Eiffel Tower, museums, and art.
   ```
3. Click upload and select the file
4. Ask: "What is the capital of France?"
5. Should get answer with sources

## Troubleshooting Setup

### "ModuleNotFoundError"
```bash
# Make sure venv is activated
source venv/bin/activate
# Reinstall
pip install -r requirements.txt
```

### "OpenAI API key not found"
```bash
# Check .env file exists and has correct key
cat .env
# Or set directly
export OPENAI_API_KEY=sk-...
python main.py
```

### "Connection refused" on port 8000
- Backend not running
- Or port already in use
- Try: `python main.py --port 8001`

### "Port 3000 already in use"
```bash
# Either kill process or use different port
npm start -- --port 3001
```

### "npm: command not found"
- Node.js not installed
- Download from nodejs.org
- Restart terminal after install

### Slow embeddings
- First run downloads model (~400MB)
- Subsequent runs use cache
- Consider GPU version for speed

## Next Steps

1. **Upload Sample Documents**
   - Create `.txt`, `.pdf`, or `.md` files
   - Use the UI to upload

2. **Ask Questions**
   - Try questions about document content
   - System retrieves relevant excerpts

3. **Customize**
   - Adjust chunk size for better context
   - Change embedding model for speed
   - Modify LLM parameters

4. **Deploy**
   - See DEPLOYMENT.md for production setup

## Development

### Backend Development

```bash
cd backend

# Install dev dependencies
pip install pytest black flake8

# Format code
black *.py

# Lint
flake8 *.py

# Tests (if added)
pytest
```

### Frontend Development

```bash
cd frontend

# Format
npx prettier --write src/

# Lint
npm run lint

# Build
npm run build
```

## Database Integration (Optional)

For production, replace file-based storage:

1. **PostgreSQL for metadata:**
   ```bash
   pip install psycopg2-binary sqlalchemy
   ```

2. **Redis for caching:**
   ```bash
   pip install redis
   ```

See advanced documentation for implementation.

## Production Deployment

For deploying to AWS/GCP/Azure, see DEPLOYMENT.md

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Slow first response | Model download in progress, be patient |
| Out of memory | Reduce chunk size or restart |
| Incorrect answers | Add more documents or adjust k value |
| API rate limit | Wait or upgrade OpenAI plan |

## Support

- Check backend logs: `python main.py` output
- Check frontend console: Browser DevTools
- Check network: `curl http://localhost:8000/status`
- Check processes: `ps aux \| grep python`

## Next: See README.md for usage documentation
