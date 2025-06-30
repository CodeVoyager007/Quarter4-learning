import requests
import streamlit as st

COINLORE_API_URL = "https://api.coinlore.net/api"

def handle_api_request(url):
    """Handles API requests and returns JSON response."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

def get_global_stats():
    """Fetches global cryptocurrency market statistics."""
    url = f"{COINLORE_API_URL}/global/"
    return handle_api_request(url)

def get_top_coins(limit=100):
    """Fetches a list of top cryptocurrencies."""
    url = f"{COINLORE_API_URL}/tickers/?start=0&limit={limit}"
    data = handle_api_request(url)
    return data if data else {'data': [], 'info': {}}

def get_coin_details(coin_id):
    """Fetches detailed information for a specific coin."""
    url = f"{COINLORE_API_URL}/ticker/?id={coin_id}"
    data = handle_api_request(url)
    return data[0] if data else None

def get_coin_markets(coin_id):
    """Fetches market data for a specific coin."""
    url = f"{COINLORE_API_URL}/coin/markets/?id={coin_id}"
    return handle_api_request(url)

def get_coin_social_stats(coin_id):
    """Fetches social media statistics for a specific coin."""
    url = f"{COINLORE_API_URL}/coin/social_stats/?id={coin_id}"
    return handle_api_request(url) 