# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Run Locally

```bash
# 1. Clone/download the project
cd Web_agent

# 2. Install dependencies
pip install google-genai requests

# 3. Run the interactive CLI
python main.py
```

### Option 2: Deploy to Vercel (Serverless API)

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Deploy
vercel

# 3. Set environment variable
vercel env add GEMINI_API_KEY
# Enter your API key

# 4. Redeploy
vercel --prod
```

### Option 3: Run Demo (No API Key Needed)

```bash
python demo.py
```

## 📝 Example Queries

Try these in the interactive CLI (`main.py`):

```
# Multiple tools
What's the weather in Tokyo and calculate 15 * 23?

# Date and calculations
What's today's date and what's the square root of 144?

# Text analysis
Analyze sentiment: "I absolutely love this product!"

# Web search (requires search grounding)
What are the latest AI developments?
```

## 🔧 Configuration

### API Key

The API key is currently hardcoded. For production:

**Environment Variable (Recommended)**:
```python
import os
API_KEY = os.environ.get("GEMINI_API_KEY", "default-key")
```

**Vercel Deployment**:
```bash
vercel env add GEMINI_API_KEY
```

### Change Model

Edit `grounding_agent.py`:
```python
agent = GroundingAgent(api_key=API_KEY, model="gemini-2.5-flash-lite")
```

Available models:
- `gemini-2.5-flash-lite` (default - fast, lower quota)
- `gemini-2.5-flash` (balanced)
- `gemini-pro` (most powerful)

## 📡 API Usage (After Vercel Deployment)

**Endpoint**: `POST /api/agent`

**Request**:
```bash
curl -X POST https://your-project.vercel.app/api/agent \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Calculate 25 * 4 and tell me the weather in London",
    "use_search_grounding": false
  }'
```

**Response**:
```json
{
  "query": "...",
  "final_answer": "...",
  "function_calls": [...],
  "grounding_metadata": null
}
```

## 🛠️ Available Tools

1. **calculator** - Math expressions (`sqrt(144)`, `sin(45)`, etc.)
2. **get_current_datetime** - Current date/time
3. **get_weather** - Weather for any location (mock data)
4. **file_operations** - Read/write/list files
5. **web_scraper** - Extract content from URLs
6. **text_analyzer** - Sentiment analysis, word count
7. **Google Search** - Web grounding (toggle with `search on/off`)

## 📂 Project Structure

```
Web_agent/
├── main.py              # Interactive CLI
├── grounding_agent.py   # Core agent logic
├── tools.py             # Tool definitions
├── demo.py              # Demo mode (no API calls)
├── test_agent.py        # Test suite
├── api/
│   └── agent.py         # Vercel serverless function
├── vercel.json          # Vercel config
├── requirements.txt     # Dependencies
└── README.md            # Full documentation
```

## 🎯 Common Commands

```bash
# Interactive CLI
python main.py

# Run demo
python demo.py

# Run tests
python test_agent.py

# Deploy to Vercel
vercel

# View Vercel logs
vercel logs
```

## ⚠️ Troubleshooting

**Rate Limit Error**:
- Wait 60 seconds or change model in `grounding_agent.py`

**Import Error**:
```bash
pip install google-genai requests
```

**API Key Error**:
- Check the API key is correct
- Verify quota at https://ai.dev/usage

## 📚 Full Documentation

- [README.md](README.md) - Complete documentation
- [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) - Deployment guide

## 💡 Need Help?

- Check example queries in the demo
- Run `help` in interactive mode
- View tool descriptions with `tools` command
