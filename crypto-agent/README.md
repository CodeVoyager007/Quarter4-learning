# �� Crypto Agent AI

A sophisticated AI-powered cryptocurrency chatbot with a dark, professional theme that uses real-time data from the CoinLore API and OpenAI's GPT-4o-mini via OpenRouter.

## ✨ Features

- **🤖 AI Chatbot**: Intelligent cryptocurrency assistant powered by OpenAI GPT-4o-mini
- **📊 Real-time Data**: Live cryptocurrency data from CoinLore API
- **🎯 Function Tools**: OpenAI function tools demonstrating parameter handling
- **📈 Market Overview**: Interactive charts and market statistics
- **💬 Chat Interface**: Beautiful Streamlit UI with chat functionality
- **🌙 Dark Professional Theme**: Custom dark theme with royal purple and crimson accents
- **📱 Responsive Design**: Modern, mobile-friendly interface

## 🎨 Theme & Design

**Color Palette:**
- **Main Background:** Charcoal Black `#0D0D0D`
- **Primary Accent:** Royal Purple `#6C3FB6`
- **Secondary Accent:** Crimson Red `#B3001B`
- **Highlight/Glow:** Midnight Teal `#005F73`
- **Text:** Ivory White `#F8F8F2`
- **VIP/Balance:** Dusty Gold `#D4AF37`

**Typography:** Modern sans-serif fonts (Inter, Segoe UI, system-ui)

## 🛠️ Technology Stack

- **Backend:** Python 3.11+
- **AI:** OpenAI GPT-4o-mini via OpenRouter
- **API:** CoinLore Cryptocurrency Data API
- **UI:** Streamlit with custom dark theme
- **Charts:** Plotly with custom styling
- **Package Manager:** uv or pip

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd crypto-agent
```

### 2. Install Dependencies

**Option A: Using uv (Recommended)**
```bash
uv sync
```

**Option B: Using pip**
```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Get your OpenRouter API key from: https://openrouter.ai/

### 4. Run the Application

```bash
streamlit run main.py
```

The app will be available at: http://localhost:8501

## 📋 Project Structure

```
crypto-agent/
├── main.py              # Streamlit UI application with dark theme
├── crypto_agent.py      # Main AI agent with OpenAI function tools
├── crypto_tools.py      # Function tools demonstrating parameter handling
├── crypto_api.py        # CoinLore API client
├── pyproject.toml       # Project dependencies (uv)
├── requirements.txt     # Project dependencies (pip)
├── README.md           # This file
└── .env                # Environment variables (create this)
```

## 🎯 OpenAI Function Tools

This project demonstrates how parameters are handled in functions underneath the function_tool decorator:

### Function Examples:

1. **No Parameters:**
   ```python
   def get_global_market_stats(self) -> Dict[str, Any]:
   ```

2. **Integer with Defaults:**
   ```python
   def get_top_cryptocurrencies(self, limit: int = 10, start: int = 0) -> Dict[str, Any]:
   ```

3. **Array Parameters:**
   ```python
   def get_cryptocurrency_details(self, coin_symbols: List[str]) -> Dict[str, Any]:
   ```

4. **String with Validation:**
   ```python
   def search_cryptocurrencies(self, query: str, limit: int = 5) -> Dict[str, Any]:
   ```

### Parameter Handling Features:

- **Validation:** Parameters are validated with min/max values
- **Defaults:** Optional parameters have sensible defaults
- **Type Safety:** All parameters are properly typed
- **Constraints:** Parameters have constraints (e.g., minLength, maximum)

## 💬 Example Questions

The chatbot can answer questions like:

- "What's the current Bitcoin price?"
- "Show me the top 10 cryptocurrencies"
- "What are the global market statistics?"
- "Tell me about Ethereum"
- "Which exchanges trade Bitcoin?"
- "What are the social stats for Bitcoin?"
- "Search for coins with 'coin' in the name"

## 🎨 UI Features

### Chat Tab
- Real-time conversation with AI
- Example questions for quick start
- Message history
- Clear chat functionality
- Dark theme with purple/crimson accents

### Market Overview Tab
- Interactive price change charts with custom colors
- Market cap distribution pie chart
- Detailed cryptocurrency table
- Real-time metrics with gold accents
- Professional dark theme

### Sidebar
- Quick market statistics
- Top 5 cryptocurrencies
- Example questions buttons
- Consistent dark theme

## 🔧 API Endpoints Used

The application uses the following CoinLore API endpoints:

- `/global/` - Global market statistics
- `/tickers/` - Top cryptocurrencies
- `/ticker/?id={ids}` - Specific coin details
- `/coin/markets/?id={id}` - Coin market data
- `/exchanges/` - Exchange information
- `/coin/social_stats/?id={id}` - Social statistics

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Yes |

## 📊 Dependencies

### Core Dependencies:
- `openai>=1.0.0` - OpenAI SDK for function tools
- `streamlit>=1.46.0` - Web UI framework
- `pandas>=2.0.0` - Data manipulation
- `plotly>=5.0.0` - Interactive charts
- `streamlit-chat>=0.1.1` - Chat UI components
- `requests>=2.32.4` - HTTP requests
- `python-dotenv>=1.1.1` - Environment management

## 🎨 Custom Theme Features

- **Dark Background:** Charcoal black for reduced eye strain
- **Professional Colors:** Royal purple and crimson red accents
- **Modern Typography:** Clean, readable fonts
- **Interactive Elements:** Hover effects and smooth transitions
- **Chart Styling:** Custom colors for all data visualizations
- **No Gray/Neon:** Pure professional aesthetic

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [CoinLore](https://www.coinlore.com/) for providing the cryptocurrency data API
- [OpenRouter](https://openrouter.ai/) for AI model access
- [OpenAI](https://openai.com/) for the GPT models
- [Streamlit](https://streamlit.io/) for the web framework

---

**Made with ♥ by Ayesha Mughal**

**Happy Trading! 🚀📈**
