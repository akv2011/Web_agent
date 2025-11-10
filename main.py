"""Interactive Grounding Agent CLI"""

import sys
import os
from dotenv import load_dotenv
from grounding_agent import GroundingAgent


def print_banner():
    """Print a nice banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            GEMINI GROUNDING AGENT                      ║
║                                                              ║
║  Two-Stage AI Agent with Multiple Tools & Grounding          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_help():
    """Print help information"""
    help_text = """
Available Commands:
  - Type your query and press Enter
  - 'help' - Show this help message
  - 'tools' - List available tools
  - 'examples' - Show example queries
  - 'search on/off' - Toggle Google Search grounding
  - 'clear' - Clear screen
  - 'quit' or 'exit' - Exit the application

Available Tools:
  1. calculator - Evaluate mathematical expressions
  2. get_current_datetime - Get current date/time
  3. get_weather - Get weather for a location
  4. file_operations - Read/write files
  5. web_scraper - Scrape web pages
  6. text_analyzer - Analyze text content
  7. Google Search - Web grounding for factual queries

Example Queries:
  - "What's 25% of 450 and what's the weather in London?"
  - "Calculate the square root of 256 and tell me today's date"
  - "What are the latest AI developments?" (uses web search)
  - "Analyze this text: 'I love this product! It's amazing!'"
"""
    print(help_text)


def print_examples():
    """Print example queries"""
    examples = """
Example Queries:

1. Multiple Tools:
   "What's the weather in San Francisco and calculate 15 * 23?"

2. Date & Math:
   "What's today's date and what's the square root of 144?"

3. Web Search (requires search grounding):
   "What was the score of the latest Lakers game?"

4. Text Analysis:
   "Analyze this text: 'This is a wonderful day! I feel great!'"

5. Weather & Time:
   "What's the weather in Tokyo and what time is it now?"

6. Complex Math:
   "Calculate: (25 * 4) + sqrt(169) - 10"
"""
    print(examples)


def main():
    """Main interactive loop"""
    print_banner()
    
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not API_KEY:
        print("\n❌ Error: GEMINI_API_KEY not found in environment variables")
        print("Please create a .env file with GEMINI_API_KEY=your_key_here")
        return
    
    try:
        agent = GroundingAgent(api_key=API_KEY)
    except Exception as e:
        print(f"\n❌ Error initializing agent: {e}")
        print("\nPlease check your API key and internet connection.")
        return
    
    print("\n✓ Agent ready! Type 'help' for commands.\n")
    
    use_search = True
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            elif user_input.lower() == 'help':
                print_help()
                continue
            
            elif user_input.lower() == 'tools':
                print("\n🛠️  Available Tools:")
                from tools import get_tool_descriptions
                print(get_tool_descriptions())
                continue
            
            elif user_input.lower() == 'examples':
                print_examples()
                continue
            
            elif user_input.lower() == 'search on':
                use_search = True
                print("\n✓ Google Search grounding enabled")
                continue
            
            elif user_input.lower() == 'search off':
                use_search = False
                print("\n✓ Google Search grounding disabled")
                continue
            
            elif user_input.lower() == 'clear':
                print("\033[2J\033[H")
                print_banner()
                continue
            
            result = agent.process_query(user_input, use_search_grounding=use_search)
            agent.display_result(result)
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.\n")


if __name__ == "__main__":
    main()
