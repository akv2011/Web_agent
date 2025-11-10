# Deploying Grounding Agent as MCP Server

This guide shows how to deploy the Grounding Agent as an MCP (Model Context Protocol) server that can be used by AI assistants like Claude, ChatGPT, or other MCP-compatible clients.

## What is MCP?

MCP (Model Context Protocol) is a standard for connecting AI assistants to external tools and data sources. By deploying this agent as an MCP server, you can use it from any MCP-compatible AI assistant.

## Setup Options

### Option 1: Local MCP Server (Recommended for Testing)

1. **Install MCP Dependencies**:
```bash
pip install mcp python-dotenv
```

2. **Set Environment Variable**:
```bash
# Add to your .env file
GEMINI_API_KEY=your_api_key_here
```

3. **Test the MCP Server Locally**:
```bash
python mcp_server.py
```

4. **Configure in AI Assistant** (example for Claude Desktop):

Edit your Claude Desktop config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:
```json
{
  "mcpServers": {
    "grounding-agent": {
      "command": "python",
      "args": ["/absolute/path/to/Web_agent/mcp_server.py"],
      "env": {
        "GEMINI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Option 2: Deploy to Remote Server

#### Using Railway.app (Recommended)

1. **Create Railway Account**: Sign up at https://railway.app

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account and select this repository

3. **Set Environment Variables**:
   - Go to project settings
   - Add variable: `GEMINI_API_KEY=your_key_here`

4. **Configure Start Command**:
   - In settings, set start command: `python mcp_server.py`

5. **Deploy**:
   - Railway will automatically deploy
   - You'll get a public URL

6. **Connect to AI Assistant**:
```json
{
  "mcpServers": {
    "grounding-agent": {
      "url": "https://your-app.railway.app",
      "protocol": "stdio"
    }
  }
}
```

#### Using Heroku

1. **Install Heroku CLI**:
```bash
brew install heroku/brew/heroku
```

2. **Login to Heroku**:
```bash
heroku login
```

3. **Create Heroku App**:
```bash
heroku create grounding-agent-mcp
```

4. **Set Environment Variables**:
```bash
heroku config:set GEMINI_API_KEY=your_key_here
```

5. **Deploy**:
```bash
git push heroku main
```

#### Using Render.com

1. **Create Render Account**: https://render.com

2. **Create New Web Service**:
   - Connect GitHub repository
   - Select this repo

3. **Configure Service**:
   - **Name**: grounding-agent
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt && pip install mcp`
   - **Start Command**: `python mcp_server.py`

4. **Add Environment Variables**:
   - Key: `GEMINI_API_KEY`
   - Value: `your_key_here`

5. **Deploy**: Render will auto-deploy

### Option 3: Deploy to Cloud Provider

#### AWS Lambda (Serverless)

Create `lambda_handler.py`:
```python
import json
import os
from grounding_agent import GroundingAgent

def lambda_handler(event, context):
    api_key = os.environ['GEMINI_API_KEY']
    agent = GroundingAgent(api_key=api_key)
    
    body = json.loads(event['body'])
    query = body.get('query', '')
    use_search = body.get('use_search_grounding', True)
    
    result = agent.process_query(query, use_search)
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

Deploy:
```bash
# Create deployment package
zip -r function.zip . -x "*.git*" "*.pyc" "__pycache__/*"

# Upload to AWS Lambda
aws lambda create-function \
  --function-name grounding-agent \
  --runtime python3.11 \
  --handler lambda_handler.lambda_handler \
  --zip-file fileb://function.zip \
  --environment Variables={GEMINI_API_KEY=your_key_here}
```

## Configuring in AI Assistants

### For Claude Desktop

1. Open config file:
```bash
# macOS
open ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Windows
notepad %APPDATA%\Claude\claude_desktop_config.json
```

2. Add server configuration:
```json
{
  "mcpServers": {
    "grounding-agent": {
      "command": "python",
      "args": ["/path/to/Web_agent/mcp_server.py"],
      "env": {
        "GEMINI_API_KEY": "your_key_here"
      }
    }
  }
}
```

3. Restart Claude Desktop

4. Test by asking: "Use the grounding-agent to calculate sqrt(144)"

### For Custom AI Registry (as shown in your image)

Based on the "Add AI Agent" form you showed:

1. **Server Name**: `grounding-agent`
2. **Environment**: `Production`
3. **Server URL**: `https://your-deployed-url.com/mcp` or `http://localhost:8080` for local
4. **Port**: `8080` (or your configured port)
5. **Protocol Version**: `MCP 1.0`
6. **Authentication Method**: `API Key`
7. **API Key**: Your Gemini API key
8. **API Key Name**: `GEMINI_API_KEY`
9. **Version**: `v1.0.0`
10. **Repository URL**: `https://github.com/yourusername/Web_agent`
11. **Description**: 
```
AI grounding agent with multiple tools (calculator, weather, datetime, file ops, 
web scraper, text analyzer) and Google Search grounding. Two-stage pipeline: 
grounding → refinement for accurate, well-formatted responses.
```

## Available Tools

Once deployed, the MCP server exposes these tools:

1. **process_query**: Main agent with all tools + Google Search
2. **calculate**: Mathematical expression evaluation
3. **get_weather**: Weather information for locations
4. **get_datetime**: Current date and time
5. **analyze_text**: Text analysis (sentiment, word count, summary)

## Testing the Deployment

### Test Locally

```bash
# Start the server
python mcp_server.py

# In another terminal, test with MCP client
python test_mcp_client.py
```

### Test Remote Deployment

```bash
# Test the endpoint
curl -X POST https://your-app-url.com/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "calculate",
    "arguments": {
      "expression": "sqrt(144)"
    }
  }'
```

## Security Considerations

1. **Never commit API keys**: Always use environment variables
2. **Use HTTPS**: For production deployments
3. **Rate limiting**: Consider adding rate limits
4. **Authentication**: Add authentication for public deployments
5. **Input validation**: All inputs are validated before processing

## Monitoring

### Railway.app
- Check logs in Railway dashboard
- Monitor resource usage
- Set up alerts

### Heroku
```bash
heroku logs --tail
```

### AWS Lambda
- Check CloudWatch logs
- Set up CloudWatch alarms

## Troubleshooting

### Issue: API Key Not Found
- Verify `.env` file exists
- Check environment variable is set correctly
- For deployed servers, verify env vars in dashboard

### Issue: Connection Refused
- Check server is running: `ps aux | grep mcp_server`
- Verify port is correct
- Check firewall settings

### Issue: Import Errors
- Install all dependencies: `pip install -r requirements.txt`
- Install MCP: `pip install mcp`

### Issue: Rate Limiting
- Gemini API has rate limits
- Check quota at: https://ai.dev/usage

## Cost Considerations

- **Gemini API**: Check pricing at https://ai.google.dev/pricing
- **Railway**: $5/month for Hobby plan
- **Heroku**: $7/month for Basic Dyno
- **Render**: Free tier available
- **AWS Lambda**: Pay per request

## Next Steps

1. Deploy to your preferred platform
2. Configure in your AI assistant
3. Test with sample queries
4. Monitor usage and performance
5. Add custom tools as needed

## Support

For issues or questions:
- Check logs for error messages
- Verify API key is valid
- Ensure all dependencies are installed
- Check network connectivity

## Example Usage

Once deployed and configured:

```
User: Use grounding-agent to process this query: "What's the weather in Tokyo and calculate 15 * 23?"

AI Assistant: [Calls grounding-agent MCP server]

Response: 
Weather in Tokyo: 15°C, Sunny, 55% humidity
Calculation: 15 × 23 = 345

Tools used: get_weather, calculator
```
