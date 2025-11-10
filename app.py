"""
Flask API Server - For local testing
Run this to test the agent locally before deploying to Vercel
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from grounding_agent import GroundingAgent

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get('GEMINI_API_KEY')


@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "Grounding Agent API - Local Server",
        "endpoints": {
            "GET /": "This help message",
            "GET /health": "Health check",
            "POST /api/agent": "Process a query"
        }
    })


@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "api_key_configured": bool(API_KEY)
    })


@app.route('/api/agent', methods=['GET', 'POST', 'OPTIONS'])
def agent():
    if request.method == 'OPTIONS':
        return '', 200
    
    if request.method == 'GET':
        return jsonify({
            "status": "ok",
            "message": "Grounding Agent API is running",
            "usage": {
                "method": "POST",
                "endpoint": "/api/agent",
                "body": {
                    "query": "Your question here",
                    "use_search_grounding": False
                }
            },
            "example": {
                "query": "Calculate sqrt(144) and weather in Tokyo",
                "use_search_grounding": False
            }
        })
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            if not data or 'query' not in data:
                return jsonify({
                    "success": False,
                    "error": "Missing 'query' parameter"
                }), 400
            
            query = data['query']
            use_search = data.get('use_search_grounding', False)
            
            if not API_KEY:
                return jsonify({
                    "success": False,
                    "error": "GEMINI_API_KEY not configured in .env"
                }), 500
            
            agent = GroundingAgent(api_key=API_KEY)
            result = agent.process_query(query, use_search_grounding=use_search)
            
            response = {
                "success": True,
                "query": result['query'],
                "answer": result['final_answer'],
                "grounded_response": result['grounded_response'],
                "refined_response": result.get('refined_response'),
                "tools_used": [fc['name'] for fc in result.get('function_calls', [])],
                "sources": len(result.get('grounding_metadata', {}).get('grounding_chunks', [])) if result.get('grounding_metadata') else 0
            }
            
            return jsonify(response)
        
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500


if __name__ == '__main__':
    if not API_KEY:
        print("\n⚠️  WARNING: GEMINI_API_KEY not found in .env file")
        print("Please add your API key to .env\n")
    else:
        print("\n✅ API Key configured")
        print("🚀 Starting server at http://localhost:3000")
        print("\nTest with:")
        print("  curl http://localhost:3000/api/agent")
        print('  curl -X POST http://localhost:3000/api/agent -H "Content-Type: application/json" -d \'{"query":"Calculate sqrt(144)"}\'')
        print("\n")
    
    app.run(host='0.0.0.0', port=3000, debug=True)
