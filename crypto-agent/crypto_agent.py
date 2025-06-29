import os
import json
from typing import Dict, List, Any, Optional
from openai import OpenAI
from crypto_tools import CryptoTools
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

class CryptoAgent:
    """AI-powered cryptocurrency agent using OpenAI function tools"""
    
    def __init__(self):
        api_key = None
        
        try:
            if hasattr(st, 'secrets') and st.secrets.get("OPENROUTER_API_KEY"):
                api_key = st.secrets["OPENROUTER_API_KEY"]
            elif os.getenv("OPENROUTER_API_KEY"):
                api_key = os.getenv("OPENROUTER_API_KEY")
            
            if not api_key:
                raise ValueError("OpenRouter API key not found")
                
        except Exception as e:
            raise Exception(f"Failed to get API key: {str(e)}")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        # Initialize crypto tools
        self.crypto_tools = CryptoTools()
        
        # Define function tools for OpenAI
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_global_market_stats",
                    "description": "Get global cryptocurrency market statistics including total market cap, volume, Bitcoin dominance, and market trends.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_top_cryptocurrencies",
                    "description": "Get top cryptocurrencies by market capitalization.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Number of cryptocurrencies to retrieve (max 100)",
                                "default": 10,
                                "minimum": 1,
                                "maximum": 100
                            },
                            "start": {
                                "type": "integer",
                                "description": "Starting position for pagination",
                                "default": 0,
                                "minimum": 0
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_cryptocurrency_details",
                    "description": "Get detailed information for specific cryptocurrencies by their symbols.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "coin_symbols": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "List of cryptocurrency symbols (e.g., ['BTC', 'ETH'])",
                                "minItems": 1
                            }
                        },
                        "required": ["coin_symbols"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_cryptocurrencies",
                    "description": "Search for cryptocurrencies by name or symbol.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (can be partial name or symbol)",
                                "minLength": 2
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 5,
                                "minimum": 1,
                                "maximum": 20
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_cryptocurrency_markets",
                    "description": "Get top 50 exchanges and markets for a specific cryptocurrency.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "coin_symbol": {
                                "type": "string",
                                "description": "Cryptocurrency symbol (e.g., 'BTC', 'ETH')"
                            }
                        },
                        "required": ["coin_symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_social_statistics",
                    "description": "Get social statistics (Reddit and Twitter) for a specific cryptocurrency.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "coin_symbol": {
                                "type": "string",
                                "description": "Cryptocurrency symbol (e.g., 'BTC', 'ETH')"
                            }
                        },
                        "required": ["coin_symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_exchange_list",
                    "description": "Get list of top cryptocurrency exchanges by volume.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Number of exchanges to retrieve",
                                "default": 10,
                                "minimum": 1,
                                "maximum": 50
                            }
                        },
                        "required": []
                    }
                }
            }
        ]
        
        # System message for the AI
        self.system_message = """You are a helpful cryptocurrency assistant powered by AI. You have access to real-time cryptocurrency data through various API functions.

Your capabilities include:
- Getting global market statistics
- Retrieving top cryptocurrencies by market cap
- Getting detailed information about specific cryptocurrencies
- Searching for cryptocurrencies by name or symbol
- Getting market data for specific cryptocurrencies
- Retrieving social statistics for cryptocurrencies
- Getting information about cryptocurrency exchanges

When users ask questions about cryptocurrencies, use the appropriate functions to get real-time data and provide comprehensive, accurate answers. Always format numbers appropriately (e.g., use commas for large numbers, format prices and market caps properly).

Be conversational and helpful, but always base your responses on the actual data you retrieve. If you don't have access to certain information, let the user know what you can and cannot provide."""
    
    def _call_function(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call the appropriate crypto tool function based on the function name"""
        try:
            if function_name == "get_global_market_stats":
                return self.crypto_tools.get_global_market_stats()
            elif function_name == "get_top_cryptocurrencies":
                return self.crypto_tools.get_top_cryptocurrencies(**arguments)
            elif function_name == "get_cryptocurrency_details":
                return self.crypto_tools.get_cryptocurrency_details(**arguments)
            elif function_name == "search_cryptocurrencies":
                return self.crypto_tools.search_cryptocurrencies(**arguments)
            elif function_name == "get_cryptocurrency_markets":
                return self.crypto_tools.get_cryptocurrency_markets(**arguments)
            elif function_name == "get_social_statistics":
                return self.crypto_tools.get_social_statistics(**arguments)
            elif function_name == "get_exchange_list":
                return self.crypto_tools.get_exchange_list(**arguments)
            else:
                return {
                    "success": False,
                    "error": f"Unknown function: {function_name}",
                    "message": "Function not implemented"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error executing function {function_name}"
            }
    
    def chat(self, user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """Process a user message and return an AI response"""
        if conversation_history is None:
            conversation_history = []
        
        # Prepare messages for OpenAI - only include user and assistant messages
        messages = [{"role": "system", "content": self.system_message}]
        
        # Add conversation history (only user and assistant messages)
        for msg in conversation_history:
            if msg["role"] in ["user", "assistant"]:
                messages.append(msg)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Make the API call with function tools
            response = self.client.chat.completions.create(
                model="openai/gpt-4o-mini",  # Using OpenRouter with GPT-4o-mini
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=2000
            )
            
            response_message = response.choices[0].message
            
            # Check if the AI wants to call a function
            if response_message.tool_calls:
                # Add the assistant's response with tool calls to messages
                messages.append(response_message)
                
                # Process each tool call
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Call the function and get the result
                    function_result = self._call_function(function_name, function_args)
                    
                    # Add the function result to the conversation
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(function_result)
                    })
                
                # Get the final response from the AI
                final_response = self.client.chat.completions.create(
                    model="openai/gpt-4o-mini",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000
                )
                
                return final_response.choices[0].message.content
            else:
                # No function calls, return the direct response
                return response_message.content
                
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    def get_quick_stats(self) -> Dict[str, Any]:
        """Get quick market statistics for display"""
        try:
            stats = self.crypto_tools.get_global_market_stats()
            if stats["success"]:
                data = stats["data"]
                return {
                    "total_market_cap": self.crypto_tools.crypto_api.format_market_cap(str(data["total_market_cap"])),
                    "total_volume_24h": self.crypto_tools.crypto_api.format_market_cap(str(data["total_volume_24h"])),
                    "bitcoin_dominance": f"{data['bitcoin_dominance']}%",
                    "total_coins": f"{data['total_coins']:,}",
                    "active_markets": f"{data['active_markets']:,}"
                }
            return {}
        except Exception:
            return {}
    
    def get_top_coins_summary(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get a summary of top cryptocurrencies"""
        try:
            result = self.crypto_tools.get_top_cryptocurrencies(limit=limit)
            if result["success"]:
                return result["data"]["coins"]
            return []
        except Exception:
            return [] 