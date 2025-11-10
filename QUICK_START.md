# Quick Start Guide - Deploying to Vercel

## What You've Built

A **Grounding Agent** with:
- ✅ 6 custom tools (calculator, weather, datetime, file ops, web scraper, text analyzer)
- ✅ Google Search grounding capability
- ✅ Two-stage pipeline (grounding → refinement)
- ✅ Vercel-ready serverless API
- ✅ Environment variable support

## Files Created

```
Web_agent/
├── api/
│   ├── agent.py              ✅ Serverless function handler
│   └── requirements.txt      ✅ API dependencies
├── grounding_agent.py        ✅ Core agent logic
├── tools.py                  ✅ 6 tool definitions
├── main.py                   ✅ CLI interface
├── test_agent.py             ✅ Local testing
├── demo.py                   ✅ Demo mode
├── test_api.py               ✅ API testing
├── vercel.json               ✅ Vercel config
├── .env                      ✅ Local env vars
├── .gitignore                ✅ Git ignore rules
└── requirements.txt          ✅ Root dependencies
```

## Option 1: Deploy via Vercel Dashboard (EASIEST)

### Step 1: Push to GitHub
```bash
cd /Users/arunkumarv/Documents/ArmorIO/Web_agent

# Initialize git if not done
git init
git add .
git commit -m "Initial commit: Grounding Agent"

# Push to GitHub
git remote add origin https://github.com/akv2011/Web_agent.git
git branch -M main
git push -u origin main
```

### Step 2: Import to Vercel
1. Go to https://vercel.com
2. Click "Import Project"
3. Import from GitHub: `akv2011/Web_agent`
4. Framework Preset: **Other**
5. Root Directory: `./`
6. Click "Deploy"

### Step 3: Add Environment Variable
1. Go to Project Settings → Environment Variables
2. Add variable:
   - Name: `GEMINI_API_KEY`
   - Value: `AIzaSyBDii7ENqZigrLoFtn4y2FnJOQ8_1udz-A`
   - Environments: Production, Preview, Development
3. Save
4. Redeploy (Deployments → ... → Redeploy)

### Step 4: Test Your API
Your URL will be: `https://web-agent-xxx.vercel.app`

```bash
# Health check
curl https://your-url.vercel.app/api/agent

# Test query
curl -X POST https://your-url.vercel.app/api/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "Calculate sqrt(144) and weather in Tokyo", "use_search_grounding": false}'
```

## Option 2: Deploy via CLI (If you have Node.js)

### Install Vercel CLI
```bash
npm install -g vercel
# or
yarn global add vercel
```

### Deploy
```bash
cd /Users/arunkumarv/Documents/ArmorIO/Web_agent

# Login
vercel login

# Add environment variable
vercel env add GEMINI_API_KEY production
# Paste: AIzaSyBDii7ENqZigrLoFtn4y2FnJOQ8_1udz-A

# Deploy to production
vercel --prod
```

## Option 3: Test Locally First

### Without Vercel CLI
```bash
cd /Users/arunkumarv/Documents/ArmorIO/Web_agent

# Test with the CLI interface
python main.py

# Test with demo mode
python demo.py

# Test individual components
python test_agent.py
```

### With Vercel CLI
```bash
vercel dev
# Then test: http://localhost:3000/api/agent
```

## Using Your Deployed Agent

Once deployed, you'll get a URL like: `https://web-agent-abc123.vercel.app`

### In the Form (from your image):

Fill in the "Add AI Agent" form:
- **Server Name**: Grounding Agent
- **Environment**: Production  
- **Server URL**: `https://web-agent-abc123.vercel.app/api/agent`
- **Port**: (leave empty)
- **Protocol Version**: HTTP/1.1
- **Authentication Method**: None (or API Key if you add auth)
- **Version**: 1.0.0
- **Repository URL**: https://github.com/akv2011/Web_agent
- **Description**: Multi-tool AI agent with grounding and refinement

### API Usage Examples

**Health Check:**
```bash
curl https://your-url.vercel.app/api/agent
```

**Calculator:**
```bash
curl -X POST https://your-url.vercel.app/api/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "Calculate 25% of 500"}'
```

**Weather:**
```bash
curl -X POST https://your-url.vercel.app/api/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather in London?"}'
```

**Multiple Tools:**
```bash
curl -X POST https://your-url.vercel.app/api/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "What time is it and what is 15 * 23?"}'
```

**With Search Grounding:**
```bash
curl -X POST https://your-url.vercel.app/api/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "Latest AI news", "use_search_grounding": true}'
```

## Response Format

```json
{
  "query": "What is the weather in Tokyo?",
  "grounded_response": "Raw response from grounding stage...",
  "refined_response": "Polished response from refinement stage...",
  "final_answer": "The final user-friendly answer",
  "function_calls": [
    {"name": "get_weather", "args": {"location": "Tokyo"}}
  ],
  "grounding_metadata": {
    "web_search_queries": [],
    "grounding_chunks": []
  }
}
```

## Troubleshooting

### Error: GEMINI_API_KEY not configured
- Add the environment variable in Vercel dashboard
- Redeploy after adding

### Error: Module not found
- Check `api/requirements.txt` has all dependencies
- Redeploy

### API returns 500
- Check Vercel logs: Project → Logs
- Verify API key is valid
- Check if you've hit rate limits

## What's Next?

1. ✅ Deploy to Vercel
2. ✅ Get your deployment URL
3. ✅ Test the API endpoints
4. ✅ Add to your agent registry
5. 🚀 Start using remotely!

## Commands Summary

```bash
# Test locally
python main.py                    # Interactive CLI
python demo.py                    # Demo mode
python test_agent.py              # Run tests

# Deploy
git push                          # Auto-deploy (if connected)
vercel --prod                     # Manual deploy (CLI)

# Test remote
curl https://your-url.vercel.app/api/agent
python test_api.py https://your-url.vercel.app
```

## Need Help?

- Vercel Docs: https://vercel.com/docs
- Gemini API: https://ai.google.dev/docs
- GitHub Repo: https://github.com/akv2011/Web_agent

Your agent is ready to deploy! 🚀
