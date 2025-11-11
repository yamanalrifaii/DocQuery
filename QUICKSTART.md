# Quick Start Guide

Get the RAG QA System running in 5 minutes.

## Prerequisites

- Python 3.10+
- Node.js 16+
- OpenAI API Key (get from [platform.openai.com](https://platform.openai.com))

## Step 1: Clone & Configure

```bash
cd qa-system
cp .env.example .env

# Edit .env and add your OpenAI key
# OPENAI_API_KEY=sk-...
```

## Step 2: Start Backend

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
cd backend
python main.py
```

**Output:** `INFO:     Uvicorn running on http://0.0.0.0:8000`

## Step 3: Start Frontend (New Terminal)

```bash
cd qa-system/frontend

npm install
npm start
```

**Opens:** `http://localhost:3000`

## Step 4: Test the System

### Option A: Using Web UI

1. Create a test file `sample.txt`:
```
Python is a programming language.
It was created by Guido van Rossum in 1991.
Python is known for its simple, readable syntax.
It is widely used in data science, web development, and automation.
```

2. Upload the file using the Web UI
3. Ask: "Who created Python?"
4. Get answer with source

### Option B: Using cURL

```bash
# Upload document
curl -X POST http://localhost:8000/upload \
  -F "file=@sample.txt"

# Ask question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Who created Python?"}'
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Activate venv: `source venv/bin/activate` |
| `OPENAI_API_KEY not found` | Add key to `.env` file |
| `Connection refused` | Backend not running on port 8000 |
| `npm: command not found` | Install Node.js from nodejs.org |

## Next Steps

- See [README.md](README.md) for full documentation
- See [SETUP.md](SETUP.md) for detailed setup guide
- Check API endpoints in [README.md#api-endpoints](README.md#api-endpoints)

## Common Questions

**Q: Where does it store documents?**
A: In `./data/documents/` and vector index in `./data/faiss_index/`

**Q: Can I use different models?**
A: Yes, edit `backend/config.py` or `.env` file

**Q: Is there a database?**
A: Currently uses file-based storage. See README for database integration.

**Q: How do I deploy to production?**
A: Use Docker: `docker-compose up`

## Useful Commands

```bash
# Check backend status
curl http://localhost:8000/status

# View backend logs (while running)
# Check terminal where you ran `python main.py`

# View frontend logs
# Check browser console (F12)

# Kill processes if needed
# Backend: Ctrl+C in that terminal
# Frontend: Ctrl+C in that terminal
```

## Example Questions

After uploading documents:

- "What is the main topic?"
- "When was X mentioned?"
- "How does Y work?"
- "What are the key points?"
- "Summarize the content"
- "Who is responsible for X?"

## System Status

Both services are working if:

```bash
# Backend responds
curl http://localhost:8000/status
# {"initialized":false,"documents_indexed":0,"message":"..."}

# Frontend loads
open http://localhost:3000
```

## What's Next?

1. **Upload real documents** - PDFs, text files, markdown
2. **Customize settings** - Edit `backend/config.py`
3. **Deploy to production** - Use `docker-compose.yml`
4. **Add more features** - See README.md

---

For full documentation, see [README.md](README.md)
