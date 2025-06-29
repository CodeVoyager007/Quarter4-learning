from openai import OpenAI
from typing import Dict, List, Any, Optional
from crypto_api import CoinLoreAPI
import json

class CryptoTools:
    """OpenAI function tools for cryptocurrency data retrieval"""
    
    def __init__(self):
        self.crypto_api = CoinLoreAPI()
    
    def get_global_market_stats(self) -> Dict[str, Any]:
        """
        Get global cryptocurrency market statistics including total market cap, 
        volume, Bitcoin dominance, and market trends.
        
        Returns:
            Dict containing global market statistics
        """
        try:
            stats = self.crypto_api.get_global_stats()
            return {
                "success": True,
                "data": stats,
                "message": "Global market statistics retrieved successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve global market statistics"
            }
    
    def get_top_cryptocurrencies(self, limit: int = 10, start: int = 0) -> Dict[str, Any]:
        """
        Get top cryptocurrencies by market capitalization.
        
        Args:
            limit: Number of cryptocurrencies to retrieve (max 100)
            start: Starting position for pagination
            
        Returns:
            Dict containing list of top cryptocurrencies
        """
        try:
            # Parameter validation - this shows how parameters are handled
            if limit > 100:
                limit = 100
            if limit < 1:
                limit = 10
            if start < 0:
                start = 0
            
            data = self.crypto_api.get_top_coins(start=start, limit=limit)
            
            # Format the data for better display
            formatted_coins = []
            for coin in data.get("coins", []):
                formatted_coins.append({
                    "rank": coin["rank"],
                    "symbol": coin["symbol"],
                    "name": coin["name"],
                    "price_usd": self.crypto_api.format_price(coin["price_usd"]),
                    "price_change_24h": f"{coin['price_change_24h']}%",
                    "market_cap": self.crypto_api.format_market_cap(coin["market_cap_usd"]),
                    "volume_24h": self.crypto_api.format_market_cap(str(coin["volume_24h"]))
                })
            
            return {
                "success": True,
                "data": {
                    "coins": formatted_coins,
                    "total_coins": data.get("total_coins", 0),
                    "timestamp": data.get("timestamp", 0)
                },
                "message": f"Retrieved top {len(formatted_coins)} cryptocurrencies"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve top cryptocurrencies"
            }
    
    def get_cryptocurrency_details(self, coin_symbols: List[str]) -> Dict[str, Any]:
        """
        Get detailed information for specific cryptocurrencies by their symbols.
        
        Args:
            coin_symbols: List of cryptocurrency symbols (e.g., ["BTC", "ETH"])
            
        Returns:
            Dict containing detailed information for the specified cryptocurrencies
        """
        try:
            # Parameter validation and symbol lookup
            if not coin_symbols:
                return {
                    "success": False,
                    "error": "No cryptocurrency symbols provided",
                    "message": "Please provide at least one cryptocurrency symbol"
                }
            
            # First, search for the coins to get their IDs
            coin_ids = []
            for symbol in coin_symbols:
                search_results = self.crypto_api.search_coins(symbol.upper(), limit=1)
                if search_results:
                    coin_ids.append(search_results[0]["id"])
                else:
                    return {
                        "success": False,
                        "error": f"Could not find cryptocurrency with symbol: {symbol}",
                        "message": f"Symbol '{symbol}' not found in our database"
                    }
            
            # Get detailed information for the found coins
            coins_data = self.crypto_api.get_coin_details(coin_ids)
            
            # Format the data
            formatted_coins = []
            for coin in coins_data:
                formatted_coins.append({
                    "symbol": coin["symbol"],
                    "name": coin["name"],
                    "rank": coin["rank"],
                    "price_usd": self.crypto_api.format_price(coin["price_usd"]),
                    "price_change_24h": f"{coin['price_change_24h']}%",
                    "price_change_1h": f"{coin['price_change_1h']}%",
                    "price_change_7d": f"{coin['price_change_7d']}%",
                    "market_cap": self.crypto_api.format_market_cap(coin["market_cap_usd"]),
                    "volume_24h": self.crypto_api.format_market_cap(coin["volume_24h"]),
                    "circulating_supply": f"{float(coin['circulating_supply']):,.0f}",
                    "total_supply": f"{float(coin['total_supply']):,.0f}" if coin['total_supply'] != "0" else "N/A",
                    "max_supply": f"{float(coin['max_supply']):,.0f}" if coin['max_supply'] != "0" else "N/A"
                })
            
            return {
                "success": True,
                "data": formatted_coins,
                "message": f"Retrieved details for {len(formatted_coins)} cryptocurrencies"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve cryptocurrency details"
            }
    
    def search_cryptocurrencies(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Search for cryptocurrencies by name or symbol.
        
        Args:
            query: Search query (can be partial name or symbol)
            limit: Maximum number of results to return
            
        Returns:
            Dict containing search results
        """
        try:
            # Parameter validation
            if not query or len(query.strip()) < 2:
                return {
                    "success": False,
                    "error": "Search query must be at least 2 characters long",
                    "message": "Please provide a longer search query"
                }
            
            if limit > 20:
                limit = 20
            if limit < 1:
                limit = 5
            
            search_results = self.crypto_api.search_coins(query.strip(), limit=limit)
            
            # Format results
            formatted_results = []
            for coin in search_results:
                formatted_results.append({
                    "symbol": coin["symbol"],
                    "name": coin["name"],
                    "rank": coin["rank"],
                    "price_usd": self.crypto_api.format_price(coin["price_usd"]),
                    "price_change_24h": f"{coin['price_change_24h']}%",
                    "market_cap": self.crypto_api.format_market_cap(coin["market_cap_usd"])
                })
            
            return {
                "success": True,
                "data": formatted_results,
                "message": f"Found {len(formatted_results)} cryptocurrencies matching '{query}'"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to search cryptocurrencies"
            }
    
    def get_cryptocurrency_markets(self, coin_symbol: str) -> Dict[str, Any]:
        """
        Get top 50 exchanges and markets for a specific cryptocurrency.
        
        Args:
            coin_symbol: Cryptocurrency symbol (e.g., "BTC", "ETH")
            
        Returns:
            Dict containing market information for the cryptocurrency
        """
        try:
            # Parameter validation and symbol lookup
            if not coin_symbol:
                return {
                    "success": False,
                    "error": "No cryptocurrency symbol provided",
                    "message": "Please provide a cryptocurrency symbol"
                }
            
            # Search for the coin to get its ID
            search_results = self.crypto_api.search_coins(coin_symbol.upper(), limit=1)
            if not search_results:
                return {
                    "success": False,
                    "error": f"Could not find cryptocurrency with symbol: {coin_symbol}",
                    "message": f"Symbol '{coin_symbol}' not found in our database"
                }
            
            coin_id = search_results[0]["id"]
            markets_data = self.crypto_api.get_coin_markets(coin_id)
            
            # Format the data
            formatted_markets = []
            for market in markets_data[:20]:  # Limit to top 20 for readability
                formatted_markets.append({
                    "exchange": market["exchange"],
                    "pair": f"{market['base']}/{market['quote']}",
                    "price": f"${market['price_usd']:,.2f}",
                    "volume_24h": self.crypto_api.format_market_cap(str(market["volume_usd"]))
                })
            
            return {
                "success": True,
                "data": {
                    "coin_symbol": coin_symbol,
                    "coin_name": search_results[0]["name"],
                    "markets": formatted_markets,
                    "total_markets": len(markets_data)
                },
                "message": f"Retrieved market data for {coin_symbol}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve cryptocurrency markets"
            }
    
    def get_social_statistics(self, coin_symbol: str) -> Dict[str, Any]:
        """
        Get social statistics (Reddit and Twitter) for a specific cryptocurrency.
        
        Args:
            coin_symbol: Cryptocurrency symbol (e.g., "BTC", "ETH")
            
        Returns:
            Dict containing social statistics for the cryptocurrency
        """
        try:
            # Parameter validation and symbol lookup
            if not coin_symbol:
                return {
                    "success": False,
                    "error": "No cryptocurrency symbol provided",
                    "message": "Please provide a cryptocurrency symbol"
                }
            
            # Search for the coin to get its ID
            search_results = self.crypto_api.search_coins(coin_symbol.upper(), limit=1)
            if not search_results:
                return {
                    "success": False,
                    "error": f"Could not find cryptocurrency with symbol: {coin_symbol}",
                    "message": f"Symbol '{coin_symbol}' not found in our database"
                }
            
            coin_id = search_results[0]["id"]
            social_data = self.crypto_api.get_social_stats(coin_id)
            
            return {
                "success": True,
                "data": {
                    "coin_symbol": coin_symbol,
                    "coin_name": search_results[0]["name"],
                    "reddit": {
                        "avg_active_users": f"{social_data['reddit']['avg_active_users']:,.0f}",
                        "subscribers": f"{social_data['reddit']['subscribers']:,.0f}"
                    },
                    "twitter": {
                        "followers_count": f"{social_data['twitter']['followers_count']:,.0f}",
                        "status_count": f"{social_data['twitter']['status_count']:,.0f}"
                    }
                },
                "message": f"Retrieved social statistics for {coin_symbol}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve social statistics"
            }
    
    def get_exchange_list(self, limit: int = 10) -> Dict[str, Any]:
        """
        Get list of top cryptocurrency exchanges by volume.
        
        Args:
            limit: Number of exchanges to retrieve
            
        Returns:
            Dict containing list of top exchanges
        """
        try:
            # Parameter validation
            if limit > 50:
                limit = 50
            if limit < 1:
                limit = 10
            
            exchanges_data = self.crypto_api.get_exchanges()
            
            # Sort by volume and take top exchanges
            sorted_exchanges = sorted(
                exchanges_data.values(),
                key=lambda x: x["volume_usd"],
                reverse=True
            )[:limit]
            
            # Format the data
            formatted_exchanges = []
            for exchange in sorted_exchanges:
                formatted_exchanges.append({
                    "name": exchange["name"],
                    "country": exchange["country"],
                    "volume_usd": self.crypto_api.format_market_cap(str(exchange["volume_usd"])),
                    "active_pairs": exchange["active_pairs"],
                    "url": exchange["url"]
                })
            
            return {
                "success": True,
                "data": formatted_exchanges,
                "message": f"Retrieved top {len(formatted_exchanges)} exchanges"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve exchange list"
            } 