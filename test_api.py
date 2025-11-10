#!/usr/bin/env python3
"""
Quick test script for the Vercel API
"""

import requests
import json
import sys


def test_api(base_url, is_local=False):
    """Test the deployed API"""
    
    print(f"\n{'='*60}")
    print(f"Testing API at: {base_url}")
    print('='*60)
    
    # Test 1: Health check
    print("\n[TEST 1] Health Check (GET /api/agent)")
    try:
        response = requests.get(f"{base_url}/api/agent")
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Simple query
    print("\n[TEST 2] Simple Query - Calculator")
    try:
        payload = {
            "query": "Calculate the square root of 144",
            "use_search_grounding": False
        }
        response = requests.post(
            f"{base_url}/api/agent",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Query: {result.get('query')}")
        print(f"Answer: {result.get('final_answer')}")
        if result.get('function_calls'):
            print(f"Tools Used: {[fc['name'] for fc in result['function_calls']]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Multiple tools
    print("\n[TEST 3] Multiple Tools")
    try:
        payload = {
            "query": "What's the weather in Tokyo and calculate 25% of 500?",
            "use_search_grounding": False
        }
        response = requests.post(
            f"{base_url}/api/agent",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Query: {result.get('query')}")
        print(f"Answer: {result.get('final_answer')}")
        if result.get('function_calls'):
            print(f"Tools Used: {[fc['name'] for fc in result['function_calls']]}")
    except Exception as e:
        print(f"Error: {e}")
    
    print(f"\n{'='*60}")
    print("Testing Complete!")
    print('='*60)


def main():
    """Main function"""
    if len(sys.argv) > 1:
        url = sys.argv[1]
        is_local = "localhost" in url or "127.0.0.1" in url
    else:
        print("\nUsage:")
        print("  Local:  python test_api.py http://localhost:3000")
        print("  Remote: python test_api.py https://your-app.vercel.app")
        print("\nDefaulting to local...")
        url = "http://localhost:3000"
        is_local = True
    
    test_api(url, is_local)


if __name__ == "__main__":
    main()
