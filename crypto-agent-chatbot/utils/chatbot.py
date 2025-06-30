import streamlit as st
from openai import OpenAI
import json
from . import api

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
    default_headers={
        "HTTP-Referer": "https://github.com/AyeshaMughal20/crypto-agent-chatbot",
        "X-Title": "Crypto AI Dashboard"
    }
)

def get_coin_id(coin_name):
    """Helper to find a coin's ID by its name or symbol."""
    coins_response = api.get_top_coins(limit=1000) 
    if coins_response and 'data' in coins_response:
        for coin in coins_response['data']:
            if coin['name'].lower() == coin_name.lower() or coin['symbol'].lower() == coin_name.lower():
                return coin['id']
    return None

def get_crypto_price(coin_name):
    """Get current price for a cryptocurrency."""
    coin_id = get_coin_id(coin_name)
    if not coin_id:
        return f"Could not find cryptocurrency '{coin_name}'"
    details = api.get_coin_details(coin_id)
    if details and 'price_usd' in details:
        return f"The current price of {coin_name} is ${float(details['price_usd']):,.2f}"
    return f"Could not fetch price for {coin_name}"

def get_top_cryptocurrencies(limit=10):
    """Get list of top cryptocurrencies."""
    response = api.get_top_coins(limit)
    if not response or 'data' not in response:
        return "Could not fetch cryptocurrency data"
    
    coins = response['data'][:limit]
    result = "Here are the top {} cryptocurrencies by market cap:\n\n".format(limit)
    for coin in coins:
        result += f"• {coin['name']} ({coin['symbol']}): ${float(coin['price_usd']):,.2f}\n"
    return result

def get_global_stats():
    """Get global market statistics."""
    stats = api.get_global_stats()
    if not stats:
        return "Could not fetch global market statistics"
    
    stats = stats[0]
    return f"""Here are the current global cryptocurrency market statistics:

• Total Market Cap: ${float(stats['total_mcap']):,.2f}
• 24h Trading Volume: ${float(stats['total_volume']):,.2f}
• Bitcoin Dominance: {stats['btc_d']}%
• Active Markets: {stats['active_markets']:,}
• Total Coins: {stats['coins_count']:,}"""

def get_coin_details(coin_name):
    """Get detailed information about a cryptocurrency."""
    coin_id = get_coin_id(coin_name)
    if not coin_id:
        return f"Could not find cryptocurrency '{coin_name}'"
    
    details = api.get_coin_details(coin_id)
    if not details:
        return f"Could not fetch details for {coin_name}"
    
    markets = api.get_coin_markets(coin_id)
    exchanges = len(markets) if markets else 0
    
    return f"""Here's what I found about {details['name']} ({details['symbol']}):

• Current Price: ${float(details['price_usd']):,.2f}
• Market Cap Rank: #{details['rank']}
• Market Cap: ${float(details['market_cap_usd']):,.2f}
• 24h Volume: ${float(details['volume24']):,.2f}
• 24h Change: {details['percent_change_24h']}%
• Available on {exchanges} exchanges
• Circulating Supply: {float(details['csupply']):,.0f} {details['symbol']}"""

def run_conversation(messages):
    """Runs the conversation with the model."""
    try:
        # Get the user's last message
        user_message = messages[-1]['content'].lower()
        
        # Prepare system context
        if len(messages) == 1:  # If this is the first user message
            messages.insert(0, {
                "role": "system",
                "content": """You are a cryptocurrency expert assistant. You help users get information about cryptocurrencies, 
                prices, market statistics, and more. Keep your responses concise and focused on the data."""
            })
        
        # Check for common patterns and get data directly
        if "price" in user_message and ("bitcoin" in user_message or "btc" in user_message):
            return {"role": "assistant", "content": get_crypto_price("BTC")}
        
        elif "price" in user_message:
            # Extract coin name after "price of" or similar patterns
            for coin in ["eth", "ethereum", "bnb", "binance", "xrp", "doge", "dogecoin"]:
                if coin in user_message:
                    return {"role": "assistant", "content": get_crypto_price(coin)}
        
        elif "top" in user_message and any(str(i) for i in range(1, 101) if str(i) in user_message):
            # Extract number after "top"
            for i in range(1, 101):
                if str(i) in user_message:
                    return {"role": "assistant", "content": get_top_cryptocurrencies(i)}
            return {"role": "assistant", "content": get_top_cryptocurrencies(10)}
        
        elif "global" in user_message or "market" in user_message or "stats" in user_message:
            return {"role": "assistant", "content": get_global_stats()}
        
        elif any(coin in user_message for coin in ["bitcoin", "btc", "ethereum", "eth", "bnb", "xrp", "doge"]):
            for coin in ["btc", "eth", "bnb", "xrp", "doge"]:
                if coin in user_message:
                    return {"role": "assistant", "content": get_coin_details(coin)}
        
        # If no pattern matched, get a general response from the model
        response = client.chat.completions.create(
            model="anthropic/claude-2",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return {
            "role": "assistant",
            "content": response.choices[0].message.content
        }

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return {
            "role": "assistant",
            "content": "I apologize, but I encountered an error. Please try asking your question in a different way."
        } 