# Vercel Deployment Guide

## Overview
This guide explains how to deploy the Gemini Grounding Agent as a serverless API on Vercel.

## Prerequisites
- Vercel account ([sign up](https://vercel.com))
- Vercel CLI installed: `npm i -g vercel`
- Gemini API key

## Project Structure for Vercel

```
Web_agent/
├── api/                    # Vercel serverless functions directory
│   └── agent.py           # Main API endpoint
├── tools.py               # Tool definitions (imported by agent.py)
├── grounding_agent.py     # Agent logic (imported by agent.py)
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
└── README.md
```

## Deployment Steps

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Configure Environment Variables

In your Vercel project dashboard or via CLI:

```bash
vercel env add GEMINI_API_KEY
# Enter your API key when prompted
```

### 3. Deploy

```bash
# Login to Vercel
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

## API Usage

Once deployed, your API will be available at:

```
https://your-project.vercel.app/api/agent
```

### Example Request

```bash
curl -X POST https://your-project.vercel.app/api/agent \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the weather in London and calculate 15 * 23?",
    "use_search_grounding": false
  }'
```

### Response Format

```json
{
  "query": "What is the weather in London and calculate 15 * 23?",
  "grounded_response": "...",
  "refined_response": "...",
  "final_answer": "...",
  "function_calls": [
    {
      "name": "get_weather",
      "args": {"location": "London"}
    },
    {
      "name": "calculator",
      "args": {"expression": "15 * 23"}
    }
  ],
  "grounding_metadata": null
}
```

## Configuration Files

### vercel.json

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.9",
      "maxDuration": 30
    }
  }
}
```

### requirements.txt

Ensure all dependencies are listed:
```
google-genai>=1.0.0
requests>=2.31.0
```

## Environment Variables

Set these in Vercel dashboard or via CLI:

- `GEMINI_API_KEY` - Your Google Gemini API key (required)

## Limitations

- Maximum execution time: 30 seconds (Pro plan)
- Maximum payload size: 4.5MB
- Bundle size limit: 250MB

## Troubleshooting

### Import Errors

If you get import errors, ensure:
1. All dependencies are in `requirements.txt`
2. Files are in the correct directory structure
3. No relative imports that break in serverless context

### Timeout Errors

If requests timeout:
1. Increase `maxDuration` in `vercel.json` (max 30s on Pro)
2. Consider caching frequently used results
3. Optimize tool execution

### API Key Errors

If API key is not found:
1. Check environment variable is set: `vercel env ls`
2. Redeploy after adding environment variables

## Testing Locally

Test before deployment:

```bash
# Install Vercel dev dependencies
vercel dev

# Your API will be available at:
# http://localhost:3000/api/agent
```

## Monitoring

View logs and metrics in the Vercel dashboard:
- Real-time logs: `vercel logs`
- View in dashboard: https://vercel.com/dashboard

## Cost Considerations

- **Hobby Plan**: Free tier with limitations
- **Pro Plan**: $20/month for production apps
- Pricing based on function execution time and bandwidth

## Security

- Never commit API keys to git
- Use environment variables for secrets
- Enable Vercel's Security features:
  - Deployment Protection
  - Edge Middleware for auth
  - Rate limiting

## Useful Commands

```bash
# View deployment logs
vercel logs

# List environment variables
vercel env ls

# Remove a deployment
vercel remove <deployment-id>

# Switch projects
vercel switch

# Get project info
vercel inspect
```

## Additional Resources

- [Vercel Python Functions Docs](https://vercel.com/docs/functions/runtimes/python)
- [Vercel CLI Reference](https://vercel.com/docs/cli)
- [Environment Variables Guide](https://vercel.com/docs/environment-variables)
