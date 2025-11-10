"""Vercel Serverless Function - Grounding Agent API"""

import os
import sys
import json
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from grounding_agent import GroundingAgent


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            query = request_data.get('query', '')
            use_search = request_data.get('use_search_grounding', True)
            
            if not query:
                self.send_error(400, "Missing 'query' parameter")
                return
            
            api_key = os.environ.get('GEMINI_API_KEY')
            if not api_key:
                self.send_error(500, "GEMINI_API_KEY not configured")
                return
            
            agent = GroundingAgent(api_key=api_key)
            result = agent.process_query(query, use_search_grounding=use_search)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(result).encode('utf-8'))
        
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_GET(self):
        """Health check endpoint"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "ok",
            "message": "Grounding Agent API is running",
            "endpoints": {
                "POST /api/agent": "Process a query with the grounding agent"
            },
            "example_request": {
                "query": "What is the weather in London?",
                "use_search_grounding": False
            }
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
