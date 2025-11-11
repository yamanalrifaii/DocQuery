# Getting Started with RAG QA System

Welcome! This guide will have you up and running in 5 minutes.

## What You Need

- **Python 3.10+** (check: `python3 --version`)
- **Node.js 16+** (check: `node --version`)
- **OpenAI API Key** (free tier available at [platform.openai.com](https://platform.openai.com))

## 5-Minute Setup

### 1. Get Your OpenAI API Key (2 minutes)

1. Visit https://platform.openai.com/account/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (it only shows once!)

### 2. Configure the System (1 minute)

```bash
# Go to project directory
cd /Users/yamanalrifai/Desktop/QA/qa-system

# Create environment file from template
cp .env.example .env

# Edit .env file and add your API key
# Open .env in your text editor and change:
# OPENAI_API_KEY=sk-...
```

### 3. Start Backend (1 minute)

```bash
# Create Python environment (first time only)
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the backend server
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Start Frontend (1 minute, new terminal)

```bash
cd /Users/yamanalrifai/Desktop/QA/qa-system/frontend

# Install dependencies (first time only)
npm install

# Start React development server
npm start
```

Browser should automatically open to `http://localhost:3000`

## Your First Question

### Test It

1. **Create a test file** - Copy this into a file called `test.txt`:

```
The capital of France is Paris.
Paris is located in the north-central part of France.
It is known for the Eiffel Tower, Arc de Triomphe, and museums.
The Eiffel Tower was built for the 1889 World's Fair.
```

2. **Upload the file**
   - In the web UI, click "Upload Documents"
   - Select your `test.txt` file
   - Wait for "✓ Documents indexed"

3. **Ask a question**
   - Type: "What is the capital of France?"
   - Click "Ask"
   - You should get an answer with sources

**Success!** You have a working RAG QA system.

## Next Steps

### Try Different Questions

After uploading documents, try asking:
- "What are the main topics?"
- "When was X mentioned?"
- "How does Y work?"
- "Summarize the key points"

### Test with Real Documents

Try uploading:
- PDF files (annual reports, research papers)
- Markdown files (documentation)
- Text files (articles, essays)

### Use Different Models

Edit `backend/config.py` or `.env`:
- Change `MODEL_NAME` to `gpt-4` for better answers (costs more)
- Different embedding models for speed/quality trade-off

### Deploy to Production

```bash
# Using Docker Compose (requires Docker)
docker-compose up
```

See [README.md](README.md) for cloud deployment options.

## Common Issues

### "Module not found" Error
```bash
# Make sure you activated the environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "OpenAI API key not found"
- Check .env file exists: `cat .env`
- Check it has your key: `grep OPENAI .env`
- Restart backend after editing .env

### "Connection refused" on port 8000
- Backend not running
- Run: `cd backend && python main.py` in another terminal

### "Port 3000 already in use"
- Another app is using port 3000
- Either kill the other app or start on different port:
  ```bash
  PORT=3001 npm start
  ```

### Slow First Request
- First run downloads embedding model (~400MB)
- Subsequent requests are much faster

## Understanding the System

### What Happens When You Upload a Document?

```
Your PDF/TXT file
    ↓
Extract text
    ↓
Split into chunks (1000 tokens each)
    ↓
Create embeddings (vector representations)
    ↓
Store in FAISS (fast search database)
    ↓
Ready for questions
```

### What Happens When You Ask a Question?

```
Your question
    ↓
Convert to embedding
    ↓
Search FAISS for similar chunks
    ↓
Get top 4 most relevant chunks
    ↓
Send to OpenAI GPT with context
    ↓
GPT generates answer
    ↓
Show answer + sources
```

## Key Features

✅ **Semantic Search** - Finds content by meaning, not just keywords
✅ **Source Attribution** - Shows exactly where answers come from
✅ **Multiple Formats** - Works with PDF, TXT, and Markdown
✅ **Modern UI** - Clean, responsive web interface
✅ **Production Ready** - Handles errors gracefully

## Useful Links

| What | Link |
|------|------|
| Full Documentation | [README.md](README.md) |
| Detailed Setup | [SETUP.md](SETUP.md) |
| System Architecture | [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) |
| API Reference | [README.md#api-endpoints](README.md#api-endpoints) |
| Project Files | [INDEX.md](INDEX.md) |
| Project Summary | [PROJECT_SUMMARY.txt](PROJECT_SUMMARY.txt) |

## Need Help?

### Check Status
```bash
# Is backend running?
curl http://localhost:8000/status

# Is frontend loading?
open http://localhost:3000

# Check Python version
python3 --version

# Check Node version
node --version
```

### View Logs
- **Backend logs**: Terminal where you ran `python main.py`
- **Frontend logs**: Terminal where you ran `npm start`
- **Browser logs**: Press F12, click Console tab

### Reset Everything
```bash
# Stop both servers (Ctrl+C in each terminal)

# Clear the vector store
rm -rf ./data/

# Restart both servers
cd backend && python main.py
# (in another terminal)
cd frontend && npm start
```

## What to Try Next

1. **Upload sample_document.txt** (included in project)
2. **Ask**: "What is machine learning?"
3. **Ask**: "Name the types of machine learning"
4. **Ask**: "What are the applications?"

These questions should all get good answers from the sample document.

## Production Deployment

When ready to deploy:

1. **Ensure you have OpenAI API key** (costs money in production)
2. **Use Docker Compose**:
   ```bash
   docker-compose up -d
   ```
3. **Use environment variables** instead of .env file
4. **Set up monitoring** and logging
5. **Add authentication** if needed

See [README.md](README.md) for detailed deployment instructions.

## Performance Tips

- **Faster answers**: Reduce `chunk_size` in config.py (trade accuracy)
- **Better answers**: Increase `chunk_size` (trade speed)
- **More context**: Increase `k` parameter (more source documents)
- **Use GPU**: Install `faiss-gpu` if you have CUDA

## What's Happening Behind the Scenes?

### Backend Technologies
- **FastAPI**: Web framework
- **LangChain**: LLM orchestration
- **FAISS**: Vector database (fast similarity search)
- **HuggingFace**: Embeddings
- **OpenAI**: Language model

### Frontend Technologies
- **React**: UI framework
- **Axios**: HTTP communication
- **CSS3**: Beautiful styling
- **Markdown**: Answer formatting

## You're Ready!

Everything is set up and working. Start asking questions about your documents!

**Quick reference:**
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Docs: See markdown files in this directory

For more details, see [README.md](README.md)

---

**Questions?** Check the [Troubleshooting](README.md#troubleshooting) section in README.md
