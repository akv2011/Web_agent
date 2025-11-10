# Grounding Agent with Gemini AI

A powerful AI agent built with Google's Gemini API featuring:
- **Two-stage pipeline**: Grounding → Refinement
- **Google Search grounding** for factual accuracy
- **6+ custom tools** for various operations
- **Automatic function calling** with seamless integration

##  Features

### Two-Stage Architecture
1. **Stage 1 - Grounding**: Uses Gemini with Google Search and custom tools to gather factual, tool-augmented information
2. **Stage 2 - Refinement**: Polishes the response for clarity and presentation

### Available Tools

1. **calculator** - Evaluate mathematical expressions
   - Supports: basic math, trigonometry, logarithms, square roots, etc.
   - Example: `"Calculate sqrt(256) + 15 * 3"`

2. **get_current_datetime** - Get current date and time
   - Returns: date, time, day of week, timezone info
   - Example: `"What's today's date?"`

3. **get_weather** - Weather information for any location
   - Supports: celsius/fahrenheit, humidity, wind speed
   - Example: `"What's the weather in Tokyo?"`

4. **file_operations** - File system operations
   - Operations: read, write, list, exists
   - Example: `"List files in the current directory"`

5. **web_scraper** - Extract content from web pages
   - Extract: text, title, metadata
   - Example: `"Get the title of https://example.com"`

6. **text_analyzer** - Analyze text content
   - Analysis: word count, sentiment, summary
   - Example: `"Analyze sentiment: 'I love this product!'"`

7. **Google Search** - Built-in web grounding
   - Automatically searches and grounds responses in real-time data
   - Example: `"What was the score of the latest Olympic event?"`

##  Installation

```bash
# Clone or download the repository
cd Web_agent

# Install dependencies
pip install -r requirements.txt
```

##  Usage

### Interactive Mode

```bash
python main.py
```

This launches an interactive session where you can:
- Ask questions with natural language
- Use multiple tools in a single query
- Toggle Google Search grounding on/off
- View available commands with `help`

### Programmatic Usage

```python
from grounding_agent import GroundingAgent

# Initialize agent
agent = GroundingAgent(api_key="YOUR_API_KEY")

# Process a query
result = agent.process_query(
    "What's the weather in London and calculate 25% of 500?",
    use_search_grounding=True
)

# Display result
agent.display_result(result)
```

##  Example Queries

### Multi-Tool Queries
```
"What's the weather in San Francisco and calculate 15 * 23?"
"What's today's date and what's the square root of 144?"
```

### Web Search Grounding
```
"What are the latest developments in quantum computing?"
"What was the score of the latest NBA finals game?"
```

### Text Analysis
```
"Analyze this text: 'I absolutely love this product! It's amazing!'"
"Count words in this text: 'The quick brown fox jumps over the lazy dog'"
```

### Complex Calculations
```
"Calculate: (25 * 4) + sqrt(169) - 10"
"What's the sine of 45 degrees times pi?"
```

##  Configuration

### API Key
The API key is currently hardcoded in `main.py`. For production:
```python
API_KEY = os.getenv("GEMINI_API_KEY")  # Use environment variable
```

### Model Selection
Change the model in `grounding_agent.py`:
```python
agent = GroundingAgent(api_key=API_KEY, model="gemini-2.0-flash-exp")
```

Available models:
- `gemini-2.0-flash-exp` (default - fastest)
- `gemini-2.5-flash`
- `gemini-pro`

## Project Structure

```
Web_agent/
├── main.py                 # Interactive CLI application
├── grounding_agent.py      # Core agent with two-stage pipeline
├── tools.py                # Custom tool definitions
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

##  How It Works

### 1. Grounding Stage
```python
def grounding_stage(self, query: str, use_search_grounding: bool = True):
    # Combines custom tools + Google Search
    # Gemini automatically calls relevant tools
    # Returns grounded response with sources
```

### 2. Refinement Stage
```python
def refinement_stage(self, grounding_result: Dict[str, Any]):
    # Takes grounded response
    # Refines for clarity and structure
    # Returns polished final answer
```

### 3. Tool Integration
Tools are Python functions with docstrings. Gemini automatically:
- Parses function signatures and docstrings
- Determines which tools to call
- Executes tools and integrates results

##  Interactive Commands

When running `main.py`:
- `help` - Show available commands
- `tools` - List all tools with descriptions
- `examples` - Show example queries
- `search on/off` - Toggle Google Search grounding
- `clear` - Clear the screen
- `quit` or `exit` - Exit application

##  Response Metadata

Each response includes:
- **Grounded Response**: Initial tool-augmented answer
- **Refined Response**: Polished final answer
- **Function Calls**: List of tools used
- **Grounding Metadata**: Web sources (if search enabled)

##  Error Handling

The agent gracefully handles:
- API errors
- Tool execution failures
- Network issues
- Invalid inputs

## Notes

- **Mock Data**: Weather data is currently mocked. Integrate a real weather API (OpenWeatherMap, WeatherAPI) for production.
- **Web Scraping**: Basic implementation. Use BeautifulSoup for better HTML parsing.
- **Security**: File operations are unrestricted. Add path validation for production.


##  License

This project is provided as-is for educational purposes.

