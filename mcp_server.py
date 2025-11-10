#!/usr/bin/env python3
"""
MCP Server for Grounding Agent
This exposes the grounding agent as an MCP server that can be used by AI assistants
"""

import os
import json
import asyncio
from typing import Any
from dotenv import load_dotenv
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from grounding_agent import GroundingAgent

load_dotenv()

server = Server("grounding-agent")
agent = None


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="process_query",
            description="Process a query using the grounding agent with multiple tools (calculator, weather, datetime, file ops, web scraper, text analyzer) and optional Google Search grounding. Returns a refined, factually accurate response.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to process"
                    },
                    "use_search_grounding": {
                        "type": "boolean",
                        "description": "Whether to use Google Search for grounding (default: true)",
                        "default": True
                    },
                    "skip_refinement": {
                        "type": "boolean",
                        "description": "Skip the refinement stage (default: false)",
                        "default": False
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="calculate",
            description="Evaluate a mathematical expression. Supports basic math, trigonometry, logarithms, square roots, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., 'sqrt(144)', '2 + 2', 'sin(45)')"
                    }
                },
                "required": ["expression"]
            }
        ),
        Tool(
            name="get_weather",
            description="Get weather information for a specified location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or location (e.g., 'San Francisco', 'London')"
                    },
                    "unit": {
                        "type": "string",
                        "description": "Temperature unit: 'celsius' or 'fahrenheit'",
                        "default": "celsius"
                    }
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="get_datetime",
            description="Get current date and time information",
            inputSchema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone (default: UTC)",
                        "default": "UTC"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="analyze_text",
            description="Analyze text content for word count, sentiment, or summary",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyze"
                    },
                    "analysis_type": {
                        "type": "string",
                        "description": "Type of analysis: 'word_count', 'sentiment', or 'summary'",
                        "default": "sentiment"
                    }
                },
                "required": ["text"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """Handle tool calls"""
    global agent
    
    if agent is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return [TextContent(
                type="text",
                text="Error: GEMINI_API_KEY not found in environment variables"
            )]
        agent = GroundingAgent(api_key=api_key)
    
    try:
        if name == "process_query":
            query = arguments.get("query", "")
            use_search = arguments.get("use_search_grounding", True)
            skip_refinement = arguments.get("skip_refinement", False)
            
            result = agent.process_query(query, use_search, skip_refinement)
            
            response_text = f"{result['final_answer']}\n\n"
            if result.get('function_calls'):
                response_text += f"Tools used: {', '.join([fc['name'] for fc in result['function_calls']])}\n"
            if result.get('grounding_metadata') and result['grounding_metadata'].get('grounding_chunks'):
                response_text += f"Sources: {len(result['grounding_metadata']['grounding_chunks'])} web pages\n"
            
            return [TextContent(type="text", text=response_text)]
        
        elif name == "calculate":
            from tools import calculator
            expression = arguments.get("expression", "")
            result = calculator(expression)
            return [TextContent(type="text", text=result)]
        
        elif name == "get_weather":
            from tools import get_weather
            location = arguments.get("location", "")
            unit = arguments.get("unit", "celsius")
            result = get_weather(location, unit)
            return [TextContent(type="text", text=result)]
        
        elif name == "get_datetime":
            from tools import get_current_datetime
            timezone = arguments.get("timezone", "UTC")
            result = get_current_datetime(timezone)
            return [TextContent(type="text", text=result)]
        
        elif name == "analyze_text":
            from tools import text_analyzer
            text = arguments.get("text", "")
            analysis_type = arguments.get("analysis_type", "sentiment")
            result = text_analyzer(text, analysis_type)
            return [TextContent(type="text", text=result)]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="grounding-agent",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
