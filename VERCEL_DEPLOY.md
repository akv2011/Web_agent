# Vercel Deployment Guide

## Prerequisites

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

## Step 1: Add Environment Variable to Vercel

You have two options:

### Option A: Via Vercel Dashboard (Recommended for the image you shared)
1. Go to your project on Vercel dashboard
2. Navigate to Settings → Environment Variables
3. Add:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: `AIzaSyBDii7ENqZigrLoFtn4y2FnJOQ8_1udz-A`
   - **Environment**: Production, Preview, Development (all)

### Option B: Via CLI
```bash
vercel env add GEMINI_API_KEY
# When prompted, paste: AIzaSyBDii7ENqZigrLoFtn4y2FnJOQ8_1udz-A
# Select: Production, Preview, Development
```

## Step 2: Test Locally

```bash
cd /Users/arunkumarv/Documents/ArmorIO/Web_agent

vercel dev
```

This will start a local server at http://localhost:3000

Test the API:
```bash
curl -X POST http://localhost:3000/api/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "Calculate 25% of 500", "use_search_grounding": false}'
```

## Step 3: Deploy to Vercel

### First-time Deployment
```bash
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? Choose your account
- Link to existing project? **N**
- Project name? **web-agent** (or press Enter)
- In which directory is your code? **./** (press Enter)
- Want to override settings? **N**

### Production Deployment
```bash
vercel --prod
```

## Step 4: Test Remote Deployment

After deployment, you'll get a URL like: `https://web-agent-xxx.vercel.app`

Test the API:
```bash
# Health check
curl https://your-deployment-url.vercel.app/api/agent

# Query the agent
curl -X POST https://your-deployment-url.vercel.app/api/agent \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the weather in Tokyo and calculate sqrt(144)?",
    "use_search_grounding": false
  }'
```

## API Endpoints

### GET /api/agent
Health check endpoint
```bash
curl https://your-deployment-url.vercel.app/api/agent
```

Response:
```json
{
  "status": "ok",
  "message": "Grounding Agent API is running",
  "endpoints": {
    "POST /api/agent": "Process a query with the grounding agent"
  }
}
```

### POST /api/agent
Process a query with the agent

Request:
```json
{
  "query": "Your question here",
  "use_search_grounding": true
}
```

Response:
```json
{
  "query": "What is the weather in Tokyo?",
  "grounded_response": "...",
  "refined_response": "...",
  "final_answer": "...",
  "function_calls": [...],
  "grounding_metadata": {...}
}
```

## Project Structure

```
Web_agent/
├── api/
│   ├── agent.py              # Vercel serverless function
│   └── requirements.txt      # Python dependencies for API
├── grounding_agent.py        # Main agent logic
├── tools.py                  # Tool definitions
├── main.py                   # CLI interface
├── vercel.json              # Vercel configuration
├── .env                     # Local environment variables
└── requirements.txt         # Root dependencies
```

## Troubleshooting

### Error: GEMINI_API_KEY not configured
Make sure you've added the environment variable in Vercel dashboard or via CLI.

### Error: Module not found
Check that `api/requirements.txt` includes all dependencies:
```
google-genai>=1.0.0
requests>=2.31.0
python-dotenv>=1.0.0
```

### Deployment fails
1. Check logs: `vercel logs`
2. Ensure vercel.json is properly configured
3. Verify Python version compatibility (3.9+)

### Local dev not working
```bash
vercel dev --debug
```

## Using the Deployed Agent in the Form (from your image)

Based on the "Add AI Agent" form you showed:

1. **Server Name**: Web Agent
2. **Environment**: Production
3. **Server URL**: `https://your-deployment-url.vercel.app`
4. **Port**: Leave empty (uses HTTPS default 443)
5. **Protocol Version**: HTTP/REST API
6. **Authentication Method**: API Key (if required)
7. **API Key**: Your Gemini key (if backend validation needed)
8. **Version**: 1.0.0
9. **Repository URL**: https://github.com/akv2011/Web_agent
10. **Description**: AI agent with grounding, multiple tools, and two-stage refinement

## Next Steps

1. Deploy: `vercel --prod`
2. Get your deployment URL
3. Test with curl or Postman
4. Add the URL to your agent registry form
5. Start using the agent remotely!

## Continuous Deployment

Connect your GitHub repository to Vercel for automatic deployments:
1. Go to Vercel dashboard
2. Import your GitHub repo
3. Every push to main will auto-deploy
