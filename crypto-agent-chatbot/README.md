# Crypto AI Dashboard & Chatbot 🤖💰

A professional, real-time cryptocurrency dashboard and AI-powered chatbot that provides instant access to crypto market data, prices, and insights.

## Features ✨

- 💬 AI-powered chatbot for natural language crypto queries
- 📊 Real-time market overview dashboard
- 💎 Top 20 cryptocurrencies with detailed metrics
- 📈 Live price updates and market statistics
- 🎨 Dark mode professional UI

## Demo 🚀

[Live Demo](https://crypto-ai-dashboard.streamlit.app) _(Add your Streamlit Cloud URL after deployment)_

## Setup 🛠️

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crypto-agent-chatbot.git
cd crypto-agent-chatbot
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.streamlit/secrets.toml` with your OpenRouter API key:
```toml
OPENROUTER_API_KEY = "your-api-key-here"
```

5. Run the app:
```bash
streamlit run main.py
```

## Deployment Guide 🌐

1. Create a GitHub repository and push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/crypto-agent-chatbot.git
git push -u origin main
```

2. Deploy to Streamlit Cloud:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository and branch
   - Set the main file path as `main.py`
   - Add your OpenRouter API key in the Streamlit Cloud secrets management

## Environment Variables 🔑

Required secrets in `.streamlit/secrets.toml`:
```toml
OPENROUTER_API_KEY = "your-api-key-here"
```

## Technologies Used 🔧

- Python 3.11+
- Streamlit
- OpenAI via OpenRouter
- CoinLore API
- Pandas
- Plotly

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- CoinLore for providing cryptocurrency data
- OpenRouter for AI capabilities
- Streamlit for the amazing web framework
