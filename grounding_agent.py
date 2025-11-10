import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import (
    calculator,
    get_current_datetime,
    get_weather,
    file_operations,
    web_scraper,
    text_analyzer,
    AVAILABLE_TOOLS
)


class GroundingAgent:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash-lite"):
        self.api_key = api_key
        self.model = model
        self.client = genai.Client(api_key=api_key)
        self.tools = AVAILABLE_TOOLS
        
        print(f"✓ Grounding Agent initialized with model: {model}")
        print(f"✓ Loaded {len(self.tools)} tools: {[t.__name__ for t in self.tools]}")
    
    def _create_google_search_tool(self) -> types.Tool:
        return types.Tool(google_search=types.GoogleSearch())
    
    def grounding_stage(self, query: str, use_search_grounding: bool = True) -> Dict[str, Any]:
        print("\n" + "="*60)
        print("STAGE 1: GROUNDING WITH TOOLS")
        print("="*60)
        
        tools_list = self.tools.copy()
        
        if use_search_grounding:
            tools_list.append(self._create_google_search_tool())
            print("✓ Google Search grounding enabled")
        
        print(f"✓ Using {len(tools_list)} tools")
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=query,
                config=types.GenerateContentConfig(
                    tools=tools_list,
                    temperature=0.7,
                )
            )
            
            result = {
                "query": query,
                "grounded_response": response.text,
                "function_calls": [],
                "grounding_metadata": None
            }
            
            if hasattr(response, 'function_calls') and response.function_calls:
                result["function_calls"] = [
                    {
                        "name": fc.name,
                        "args": dict(fc.args) if hasattr(fc, 'args') else {}
                    }
                    for fc in response.function_calls
                ]
                print(f"\n✓ Function calls made: {len(result['function_calls'])}")
                for fc in result["function_calls"]:
                    print(f"  - {fc['name']}({fc['args']})")
            
            if hasattr(response, 'candidates') and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if hasattr(candidate, 'grounding_metadata'):
                    metadata = candidate.grounding_metadata
                    result["grounding_metadata"] = {
                        "web_search_queries": getattr(metadata, 'web_search_queries', []),
                        "grounding_chunks": []
                    }
                    
                    if hasattr(metadata, 'grounding_chunks'):
                        for chunk in metadata.grounding_chunks:
                            if hasattr(chunk, 'web'):
                                result["grounding_metadata"]["grounding_chunks"].append({
                                    "title": getattr(chunk.web, 'title', 'N/A'),
                                    "uri": getattr(chunk.web, 'uri', 'N/A')
                                })
                    
                    if result["grounding_metadata"]["web_search_queries"]:
                        print(f"\n✓ Search queries: {result['grounding_metadata']['web_search_queries']}")
                    if result["grounding_metadata"]["grounding_chunks"]:
                        print(f"✓ Sources found: {len(result['grounding_metadata']['grounding_chunks'])}")
            
            print(f"\n✓ Grounded response generated ({len(response.text)} chars)")
            
            return result
        
        except Exception as e:
            print(f"\n✗ Error in grounding stage: {str(e)}")
            return {
                "query": query,
                "grounded_response": f"Error: {str(e)}",
                "function_calls": [],
                "grounding_metadata": None,
                "error": str(e)
            }
    
    def refinement_stage(self, grounding_result: Dict[str, Any]) -> str:
        """Stage 2: Refine the grounded response for better presentation"""
        print("\n" + "="*60)
        print("STAGE 2: REFINEMENT")
        print("="*60)
        
        context_parts = [
            "You are a helpful assistant that refines and improves responses.",
            f"\nOriginal Query: {grounding_result['query']}",
            f"\nGrounded Response: {grounding_result['grounded_response']}"
        ]
        
        if grounding_result.get('function_calls'):
            context_parts.append("\nTools Used:")
            for fc in grounding_result['function_calls']:
                context_parts.append(f"  - {fc['name']}")
        
        if grounding_result.get('grounding_metadata') and grounding_result['grounding_metadata'].get('grounding_chunks'):
            context_parts.append("\nSources:")
            for chunk in grounding_result['grounding_metadata']['grounding_chunks'][:3]:
                context_parts.append(f"  - {chunk['title']}")
        
        context_parts.append(
            "\nPlease refine this response to be:\n"
            "1. Clear and well-structured\n"
            "2. Concise but informative\n"
            "3. Easy to understand\n"
            "4. Properly formatted\n\n"
            "Provide ONLY the refined response, without any meta-commentary."
        )
        
        refinement_prompt = "\n".join(context_parts)
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=refinement_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                )
            )
            
            print(f"✓ Refined response generated ({len(response.text)} chars)")
            return response.text
        
        except Exception as e:
            print(f"\n✗ Error in refinement stage: {str(e)}")
            return grounding_result['grounded_response']
    
    def process_query(self, query: str, use_search_grounding: bool = True, 
                     skip_refinement: bool = False) -> Dict[str, Any]:
        print("\n" + ""*60)
        print("GROUNDING AGENT - QUERY PROCESSING")
        print(""*60)
        print(f"\nQuery: {query}")
        
        grounding_result = self.grounding_stage(query, use_search_grounding)
        
        refined_response = None
        if not skip_refinement and "error" not in grounding_result:
            refined_response = self.refinement_stage(grounding_result)
        
        final_result = {
            "query": query,
            "grounded_response": grounding_result["grounded_response"],
            "refined_response": refined_response,
            "function_calls": grounding_result.get("function_calls", []),
            "grounding_metadata": grounding_result.get("grounding_metadata"),
            "final_answer": refined_response if refined_response else grounding_result["grounded_response"]
        }
        
        print("\n" + "="*60)
        print("PROCESSING COMPLETE")
        print("="*60)
        
        return final_result
    
    def display_result(self, result: Dict[str, Any]):
        """Display the result in a user-friendly format"""
        print("\n" + "▓"*60)
        print("FINAL RESULT")
        print("▓"*60)
        print(f"\n{result['final_answer']}")
        
        if result.get('function_calls'):
            print(f"\nTools used: {', '.join([fc['name'] for fc in result['function_calls']])}")
        
        if result.get('grounding_metadata') and result['grounding_metadata'].get('grounding_chunks'):
            print(f"\nSources: {len(result['grounding_metadata']['grounding_chunks'])} web pages")
        
        print("\n" + ""*60)


def main():
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not API_KEY:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return
    
    agent = GroundingAgent(api_key=API_KEY)
    
    example_queries = [
        "What's the weather like in San Francisco and what's 25% of 450?",
        "What's the current date and time? Also calculate the square root of 144.",
        "Tell me about the latest developments in AI (use web search)",
    ]
    
    print("\n" + "🤖 GROUNDING AGENT DEMO" + "\n")
    
    query = example_queries[0]
    result = agent.process_query(query, use_search_grounding=False)
    agent.display_result(result)


if __name__ == "__main__":
    main()
