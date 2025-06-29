import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import time

class CoinLoreAPI:
    """CoinLore API client for cryptocurrency data"""
    
    BASE_URL = "https://api.coinlore.net/api"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoAgent/1.0'
        })
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a request to the CoinLore API"""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def get_global_stats(self) -> Dict[str, Any]:
        """Get global cryptocurrency market statistics"""
        data = self._make_request("/global/")
        if data and len(data) > 0:
            stats = data[0]
            return {
                "total_coins": stats.get("coins_count", 0),
                "active_markets": stats.get("active_markets", 0),
                "total_market_cap": stats.get("total_mcap", 0),
                "total_volume_24h": stats.get("total_volume", 0),
                "bitcoin_dominance": stats.get("btc_d", "0"),
                "ethereum_dominance": stats.get("eth_d", "0"),
                "market_cap_change_24h": stats.get("mcap_change", "0"),
                "volume_change_24h": stats.get("volume_change", "0"),
                "average_change_percent": stats.get("avg_change_percent", "0"),
                "volume_ath": stats.get("volume_ath", 0),
                "market_cap_ath": stats.get("mcap_ath", 0)
            }
        return {}
    
    def get_top_coins(self, start: int = 0, limit: int = 100) -> Dict[str, Any]:
        """Get top cryptocurrencies by market cap"""
        params = {"start": start, "limit": limit}
        data = self._make_request("/tickers/", params)
        
        if "data" in data:
            coins = []
            for coin in data["data"]:
                coins.append({
                    "id": coin.get("id", ""),
                    "symbol": coin.get("symbol", ""),
                    "name": coin.get("name", ""),
                    "rank": coin.get("rank", 0),
                    "price_usd": coin.get("price_usd", "0"),
                    "price_change_24h": coin.get("percent_change_24h", "0"),
                    "price_change_1h": coin.get("percent_change_1h", "0"),
                    "price_change_7d": coin.get("percent_change_7d", "0"),
                    "market_cap_usd": coin.get("market_cap_usd", "0"),
                    "volume_24h": coin.get("volume24", 0),
                    "circulating_supply": coin.get("csupply", "0"),
                    "total_supply": coin.get("tsupply", "0"),
                    "max_supply": coin.get("msupply", "0")
                })
            
            return {
                "coins": coins,
                "total_coins": data.get("info", {}).get("coins_num", 0),
                "timestamp": data.get("info", {}).get("time", 0)
            }
        return {"coins": [], "total_coins": 0, "timestamp": 0}
    
    def get_coin_details(self, coin_ids: List[str]) -> List[Dict[str, Any]]:
        """Get detailed information for specific coins"""
        if not coin_ids:
            return []
        
        coin_id_str = ",".join(coin_ids)
        data = self._make_request(f"/ticker/?id={coin_id_str}")
        
        coins = []
        for coin in data:
            coins.append({
                "id": coin.get("id", ""),
                "symbol": coin.get("symbol", ""),
                "name": coin.get("name", ""),
                "rank": coin.get("rank", 0),
                "price_usd": coin.get("price_usd", "0"),
                "price_change_24h": coin.get("percent_change_24h", "0"),
                "price_change_1h": coin.get("percent_change_1h", "0"),
                "price_change_7d": coin.get("percent_change_7d", "0"),
                "market_cap_usd": coin.get("market_cap_usd", "0"),
                "volume_24h": coin.get("volume24", "0"),
                "volume_24h_native": coin.get("volume24_native", "0"),
                "circulating_supply": coin.get("csupply", "0"),
                "total_supply": coin.get("tsupply", "0"),
                "max_supply": coin.get("msupply", "0"),
                "price_btc": coin.get("price_btc", "0")
            })
        
        return coins
    
    def get_coin_markets(self, coin_id: str) -> List[Dict[str, Any]]:
        """Get top 50 exchanges and markets for a specific coin"""
        data = self._make_request(f"/coin/markets/?id={coin_id}")
        
        markets = []
        for market in data:
            markets.append({
                "exchange": market.get("name", ""),
                "base": market.get("base", ""),
                "quote": market.get("quote", ""),
                "price": market.get("price", 0),
                "price_usd": market.get("price_usd", 0),
                "volume": market.get("volume", 0),
                "volume_usd": market.get("volume_usd", 0),
                "timestamp": market.get("time", 0)
            })
        
        return markets
    
    def get_exchanges(self) -> Dict[str, Dict[str, Any]]:
        """Get all cryptocurrency exchanges"""
        data = self._make_request("/exchanges/")
        
        exchanges = {}
        for exchange_id, exchange_data in data.items():
            exchanges[exchange_id] = {
                "id": exchange_data.get("id", ""),
                "name": exchange_data.get("name", ""),
                "name_id": exchange_data.get("name_id", ""),
                "volume_usd": exchange_data.get("volume_usd", 0),
                "active_pairs": exchange_data.get("active_pairs", 0),
                "url": exchange_data.get("url", ""),
                "country": exchange_data.get("country", "")
            }
        
        return exchanges
    
    def get_exchange_details(self, exchange_id: str) -> Dict[str, Any]:
        """Get specific exchange details with top 100 pairs"""
        data = self._make_request(f"/exchange/?id={exchange_id}")
        
        exchange_info = {}
        pairs = []
        
        for key, value in data.items():
            if key == "pairs":
                for pair in value:
                    pairs.append({
                        "base": pair.get("base", ""),
                        "quote": pair.get("quote", ""),
                        "volume": pair.get("volume", 0),
                        "price": pair.get("price", 0),
                        "price_usd": pair.get("price_usd", 0),
                        "timestamp": pair.get("time", 0)
                    })
            else:
                exchange_info[key] = value
        
        return {
            "exchange_info": exchange_info,
            "pairs": pairs
        }
    
    def get_social_stats(self, coin_id: str) -> Dict[str, Any]:
        """Get social statistics for a specific coin"""
        data = self._make_request(f"/coin/social_stats/?id={coin_id}")
        
        return {
            "reddit": {
                "avg_active_users": data.get("reddit", {}).get("avg_active_users", 0),
                "subscribers": data.get("reddit", {}).get("subscribers", 0)
            },
            "twitter": {
                "followers_count": data.get("twitter", {}).get("followers_count", 0),
                "status_count": data.get("twitter", {}).get("status_count", 0)
            }
        }
    
    def search_coins(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for coins by name or symbol"""
        # Get top coins and filter by query
        data = self.get_top_coins(start=0, limit=1000)
        query_lower = query.lower()
        
        matching_coins = []
        for coin in data.get("coins", []):
            if (query_lower in coin["name"].lower() or 
                query_lower in coin["symbol"].lower()):
                matching_coins.append(coin)
                if len(matching_coins) >= limit:
                    break
        
        return matching_coins
    
    def format_price(self, price: str) -> str:
        """Format price for display"""
        try:
            price_float = float(price)
            if price_float >= 1:
                return f"${price_float:,.2f}"
            elif price_float >= 0.01:
                return f"${price_float:.4f}"
            else:
                return f"${price_float:.8f}"
        except (ValueError, TypeError):
            return price
    
    def format_market_cap(self, market_cap: str) -> str:
        """Format market cap for display"""
        try:
            market_cap_float = float(market_cap)
            if market_cap_float >= 1e12:
                return f"${market_cap_float/1e12:.2f}T"
            elif market_cap_float >= 1e9:
                return f"${market_cap_float/1e9:.2f}B"
            elif market_cap_float >= 1e6:
                return f"${market_cap_float/1e6:.2f}M"
            else:
                return f"${market_cap_float:,.0f}"
        except (ValueError, TypeError):
            return market_cap 