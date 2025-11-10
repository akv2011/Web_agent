#!/usr/bin/env python3
"""
Simple HTTP server wrapper for the MCP server
This makes it easier to deploy to platforms like Railway, Render, Heroku
"""

import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from grounding_agent import GroundingAgent
from tools import (
    calculator,
    get_current_datetime,
    get_weather,
    text_analyzer
)

load_dotenv()

app = Flask(__name__)
agent = None


def get_agent():
    """Get or create agent instance"""
    global agent
    if agent is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        agent = GroundingAgent(api_key=api_key)
    return agent


@app.route("/")
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "Grounding Agent MCP Server",
        "version": "1.0.0",
        "tools": [
            "process_query",
            "calculate",
            "get_weather",
            "get_datetime",
            "analyze_text"
        ]
    })


@app.route("/health")
def health():
    """Health check"""
    return jsonify({"status": "healthy"})


@app.route("/mcp", methods=["POST"])
def mcp_endpoint():
    """Main MCP endpoint for tool calls"""
    try:
        data = request.get_json()
        tool_name = data.get("tool")
        arguments = data.get("arguments", {})
        
        if tool_name == "process_query":
            query = arguments.get("query", "")
            use_search = arguments.get("use_search_grounding", True)
            skip_refinement = arguments.get("skip_refinement", False)
            
            agent = get_agent()
            result = agent.process_query(query, use_search, skip_refinement)
            
            return jsonify({
                "success": True,
                "result": result
            })
        
        elif tool_name == "calculate":
            expression = arguments.get("expression", "")
            result = calculator(expression)
            return jsonify({
                "success": True,
                "result": result
            })
        
        elif tool_name == "get_weather":
            location = arguments.get("location", "")
            unit = arguments.get("unit", "celsius")
            result = get_weather(location, unit)
            return jsonify({
                "success": True,
                "result": result
            })
        
        elif tool_name == "get_datetime":
            timezone = arguments.get("timezone", "UTC")
            result = get_current_datetime(timezone)
            return jsonify({
                "success": True,
                "result": result
            })
        
        elif tool_name == "analyze_text":
            text = arguments.get("text", "")
            analysis_type = arguments.get("analysis_type", "sentiment")
            result = text_analyzer(text, analysis_type)
            return jsonify({
                "success": True,
                "result": result
            })
        
        else:
            return jsonify({
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }), 400
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/tools", methods=["GET"])
def list_tools():
    """List available tools"""
    return jsonify({
        "tools": [
            {
                "name": "process_query",
                "description": "Process query with all tools + Google Search grounding",
                "parameters": {
                    "query": "string (required)",
                    "use_search_grounding": "boolean (default: true)",
                    "skip_refinement": "boolean (default: false)"
                }
            },
            {
                "name": "calculate",
                "description": "Evaluate mathematical expression",
                "parameters": {
                    "expression": "string (required)"
                }
            },
            {
                "name": "get_weather",
                "description": "Get weather information",
                "parameters": {
                    "location": "string (required)",
                    "unit": "string (celsius|fahrenheit, default: celsius)"
                }
            },
            {
                "name": "get_datetime",
                "description": "Get current date and time",
                "parameters": {
                    "timezone": "string (default: UTC)"
                }
            },
            {
                "name": "analyze_text",
                "description": "Analyze text content",
                "parameters": {
                    "text": "string (required)",
                    "analysis_type": "string (word_count|sentiment|summary, default: sentiment)"
                }
            }
        ]
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
