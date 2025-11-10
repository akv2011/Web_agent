import math
import os
import json
from datetime import datetime
from typing import Dict, Any
import requests


def calculator(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result.
    
    Args:
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "sqrt(16)")
    """
    try:
        safe_namespace = {
            'abs': abs, 'round': round, 'min': min, 'max': max,
            'sum': sum, 'pow': pow,
            'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
            'tan': math.tan, 'log': math.log, 'log10': math.log10,
            'exp': math.exp, 'pi': math.pi, 'e': math.e,
            'floor': math.floor, 'ceil': math.ceil
        }
        result = eval(expression, {"__builtins__": {}}, safe_namespace)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating expression: {str(e)}"


def get_current_datetime(timezone: str = "UTC") -> str:
    """Returns the current date and time information.
    
    Args:
        timezone: Timezone name (default is UTC)
    """
    now = datetime.now()
    return json.dumps({
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day_of_week": now.strftime("%A"),
        "timezone": timezone,
        "timestamp": now.timestamp(),
        "iso_format": now.isoformat()
    }, indent=2)


def get_weather(location: str, unit: str = "celsius") -> str:
    """Gets weather information for a specified location (mock data).
    
    Args:
        location: City name (e.g., "San Francisco", "London")
        unit: Temperature unit - "celsius" or "fahrenheit"
    """
    mock_weather = {
        "san francisco": {"temp": 18, "condition": "Partly Cloudy", "humidity": 65, "wind_speed": 15},
        "london": {"temp": 12, "condition": "Rainy", "humidity": 80, "wind_speed": 20},
        "new york": {"temp": 8, "condition": "Cold and Clear", "humidity": 45, "wind_speed": 10},
        "tokyo": {"temp": 15, "condition": "Sunny", "humidity": 55, "wind_speed": 8},
        "mumbai": {"temp": 30, "condition": "Hot and Humid", "humidity": 75, "wind_speed": 12}
    }
    
    location_key = location.lower().split(',')[0].strip()
    weather_data = mock_weather.get(location_key, {
        "temp": 20, "condition": "Unknown", "humidity": 50, "wind_speed": 10
    })
    
    temp = weather_data["temp"]
    if unit.lower() == "fahrenheit":
        temp = (temp * 9/5) + 32
    
    return json.dumps({
        "location": location,
        "temperature": f"{temp}°{unit[0].upper()}",
        "condition": weather_data["condition"],
        "humidity": f"{weather_data['humidity']}%",
        "wind_speed": f"{weather_data['wind_speed']} km/h"
    }, indent=2)


def file_operations(operation: str, filepath: str, content: str = "") -> str:
    """Performs file operations like read, write, or list files.
    
    Args:
        operation: "read", "write", "list", or "exists"
        filepath: Path to the file or directory
        content: Content to write (for write operation)
    """
    try:
        if operation == "read":
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    file_content = f.read()
                return f"File content:\n{file_content}"
            else:
                return f"Error: File '{filepath}' does not exist"
        
        elif operation == "write":
            with open(filepath, 'w') as f:
                f.write(content)
            return f"Successfully wrote to '{filepath}'"
        
        elif operation == "list":
            if os.path.isdir(filepath):
                files = os.listdir(filepath)
                return f"Files in '{filepath}':\n" + "\n".join(f"  - {f}" for f in files)
            else:
                return f"Error: '{filepath}' is not a directory"
        
        elif operation == "exists":
            exists = os.path.exists(filepath)
            return f"Path '{filepath}' {'exists' if exists else 'does not exist'}"
        
        else:
            return f"Error: Unknown operation '{operation}'"
    
    except Exception as e:
        return f"Error performing file operation: {str(e)}"


def web_scraper(url: str, extract: str = "text") -> str:
    """Fetches content from a URL and extracts information.
    
    Args:
        url: The URL to scrape
        extract: "text", "title", or "metadata"
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        if extract == "text":
            text = response.text[:500]
            return f"Preview of webpage content:\n{text}..."
        
        elif extract == "title":
            import re
            title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
            title = title_match.group(1) if title_match else "No title found"
            return f"Page title: {title}"
        
        elif extract == "metadata":
            return json.dumps({
                "url": url,
                "status_code": response.status_code,
                "content_type": response.headers.get('content-type', 'unknown'),
                "content_length": len(response.content),
                "encoding": response.encoding
            }, indent=2)
        
        else:
            return f"Extraction type '{extract}' not supported"
    
    except requests.RequestException as e:
        return f"Error fetching URL: {str(e)}"
    except Exception as e:
        return f"Error scraping webpage: {str(e)}"


def text_analyzer(text: str, analysis_type: str = "summary") -> str:
    """Analyzes text and provides insights.
    
    Args:
        text: The text to analyze
        analysis_type: "summary", "word_count", or "sentiment"
    """
    try:
        if analysis_type == "word_count":
            words = text.split()
            chars = len(text)
            sentences = text.count('.') + text.count('!') + text.count('?')
            return json.dumps({
                "words": len(words),
                "characters": chars,
                "sentences": max(1, sentences),
                "avg_word_length": round(chars / max(1, len(words)), 2)
            }, indent=2)
        
        elif analysis_type == "summary":
            words = text.split()[:100]
            return f"Summary (first 100 words):\n{' '.join(words)}..."
        
        elif analysis_type == "sentiment":
            positive_words = ['good', 'great', 'excellent', 'happy', 'love', 'wonderful', 'amazing']
            negative_words = ['bad', 'terrible', 'awful', 'hate', 'poor', 'worst', 'horrible']
            
            text_lower = text.lower()
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            if pos_count > neg_count:
                sentiment = "Positive"
            elif neg_count > pos_count:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            
            return json.dumps({
                "sentiment": sentiment,
                "positive_indicators": pos_count,
                "negative_indicators": neg_count
            }, indent=2)
        
        else:
            return f"Analysis type '{analysis_type}' not supported"
    
    except Exception as e:
        return f"Error analyzing text: {str(e)}"


AVAILABLE_TOOLS = [
    calculator,
    get_current_datetime,
    get_weather,
    file_operations,
    web_scraper,
    text_analyzer
]


def get_tool_descriptions() -> str:
    """Returns a formatted description of all available tools"""
    descriptions = []
    for tool in AVAILABLE_TOOLS:
        descriptions.append(f"- {tool.__name__}: {tool.__doc__.strip().split(chr(10))[0]}")
    return "\n".join(descriptions)
