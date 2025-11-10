"""
Test script for the Grounding Agent
Run this to test various features
"""

from grounding_agent import GroundingAgent


def test_calculator():
    """Test calculator tool"""
    print("\n" + "="*60)
    print("TEST 1: Calculator Tool")
    print("="*60)
    
    API_KEY = "AIzaSyBDii7ENqZigrLoFtn4y2FnJOQ8_1udz-A"
    agent = GroundingAgent(api_key=API_KEY)
    
    query = "Calculate the square root of 144 and 25% of 500"
    result = agent.process_query(query, use_search_grounding=False)
    agent.display_result(result)


def test_weather_and_time():
    """Test weather and datetime tools"""
    print("\n" + "="*60)
    print("TEST 2: Weather and DateTime Tools")
    print("="*60)
    
    API_KEY = "AIzaSyBDii7ENqZigrLoFtn4y2FnJOQ8_1udz-A"
    agent = GroundingAgent(api_key=API_KEY)
    
    query = "What's the weather in London and what's today's date?"
    result = agent.process_query(query, use_search_grounding=False)
    agent.display_result(result)


def test_multiple_tools():
    """Test multiple tools in one query"""
    print("\n" + "="*60)
    print("TEST 3: Multiple Tools")
    print("="*60)
    
    API_KEY = "AIzaSyBDii7ENqZigrLoFtn4y2FnJOQ8_1udz-A"
    agent = GroundingAgent(api_key=API_KEY)
    
    query = "What's the weather in San Francisco, calculate 15 times 23, and tell me the current time?"
    result = agent.process_query(query, use_search_grounding=False)
    agent.display_result(result)


def test_text_analysis():
    """Test text analyzer tool"""
    print("\n" + "="*60)
    print("TEST 4: Text Analysis")
    print("="*60)
    
    API_KEY = "AIzaSyBDii7ENqZigrLoFtn4y2FnJOQ8_1udz-A"
    agent = GroundingAgent(api_key=API_KEY)
    
    query = "Analyze the sentiment of this text: 'I love this product! It's absolutely amazing and wonderful!'"
    result = agent.process_query(query, use_search_grounding=False)
    agent.display_result(result)


def test_grounding_search():
    """Test with Google Search grounding"""
    print("\n" + "="*60)
    print("TEST 5: Google Search Grounding")
    print("="*60)
    
    API_KEY = "AIzaSyBDii7ENqZigrLoFtn4y2FnJOQ8_1udz-A"
    agent = GroundingAgent(api_key=API_KEY)
    
    query = "What are the latest developments in artificial intelligence?"
    result = agent.process_query(query, use_search_grounding=True)
    agent.display_result(result)


def run_all_tests():
    """Run all tests"""
    print("\n" + "█"*60)
    print("GROUNDING AGENT - AUTOMATED TESTS")
    print("█"*60)
    
    tests = [
        ("Calculator", test_calculator),
        ("Weather & DateTime", test_weather_and_time),
        ("Multiple Tools", test_multiple_tools),
        ("Text Analysis", test_text_analysis),
        ("Search Grounding", test_grounding_search)
    ]
    
    print("\nSelect test to run:")
    for i, (name, _) in enumerate(tests, 1):
        print(f"  {i}. {name}")
    print(f"  {len(tests) + 1}. Run all tests")
    print("  0. Exit")
    
    try:
        choice = input("\nEnter your choice (0-6): ").strip()
        choice_num = int(choice)
        
        if choice_num == 0:
            print("\n👋 Goodbye!\n")
            return
        elif choice_num == len(tests) + 1:
            for name, test_func in tests:
                print(f"\n\n{'█'*60}")
                print(f"Running: {name}")
                print('█'*60)
                try:
                    test_func()
                except Exception as e:
                    print(f"\n❌ Test failed: {e}")
                input("\nPress Enter to continue...")
        elif 1 <= choice_num <= len(tests):
            name, test_func = tests[choice_num - 1]
            test_func()
        else:
            print("\n❌ Invalid choice")
    
    except ValueError:
        print("\n❌ Invalid input")
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    run_all_tests()
