# Crypto AI Dashboard & Chatbot 🤖💰

A professional, real-time cryptocurrency dashboard and AI-powered chatbot built with Streamlit. Get instant access to cryptocurrency prices, market statistics, and engage with an AI assistant for crypto-related questions.

## Features

- 💬 AI-powered chatbot for cryptocurrency questions
- 📊 Real-time market overview dashboard
- 💎 Top cryptocurrencies tracking
- 📈 Live price updates and market statistics
- 🎨 Professional dark theme UI

## Technologies Used

- Python 3.11+
- Streamlit
- OpenAI (via OpenRouter)
- Pandas
- Plotly
- CoinLore API

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crypto-agent-chatbot.git
cd crypto-agent-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.streamlit/secrets.toml` file with your OpenRouter API key:
```toml
OPENROUTER_API_KEY = "your-api-key-here"
```

4. Run the app:
```bash
streamlit run main.py
```

## Deployment to Streamlit Cloud

1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/crypto-agent-chatbot.git
git push -u origin main
```

2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub

3. Click "New app" and select your repository

4. In the deployment settings:
   - Set Python version to 3.11
   - Add your OpenRouter API key in the secrets management section:
     ```toml
     OPENROUTER_API_KEY = "your-api-key-here"
     ```

5. Click "Deploy"

Your app will be live at `https://yourusername-crypto-agent-chatbot.streamlit.app`

## Environment Variables

The following secrets need to be set in `.streamlit/secrets.toml` or in Streamlit Cloud's secrets management:

- `OPENROUTER_API_KEY`: Your OpenRouter API key

## API Documentation

This project uses the following APIs:

- CoinLore API for cryptocurrency data
- OpenRouter API for AI chat functionality

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Ayesha Mughal

## Acknowledgments

- CoinLore for providing cryptocurrency data
- OpenRouter for AI capabilities
- Streamlit for the amazing framework
