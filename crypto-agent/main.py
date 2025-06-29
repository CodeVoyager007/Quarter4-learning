import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
from crypto_agent import CryptoAgent
from streamlit_chat import message
import os
from dotenv import load_dotenv

# Page configuration
st.set_page_config(
    page_title="Crypto Agent AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    html, body, [class*="css"]  {
        background-color: #0D0D0D !important;
        color: #F8F8F2 !important;
        font-family: 'Inter', 'Segoe UI', 'system-ui', sans-serif !important;
    }
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #6C3FB6 0%, #B3001B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #6C3FB6 0%, #005F73 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #F8F8F2;
        text-align: center;
    }
    .chat-container {
        background-color: #16161a;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #F8F8F2;
    }
    .stButton > button {
        background: linear-gradient(90deg, #6C3FB6 0%, #B3001B 100%);
        color: #F8F8F2;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        font-family: 'Inter', 'Segoe UI', 'system-ui', sans-serif !important;
        box-shadow: 0 2px 8px #005F7333;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #B3001B 0%, #6C3FB6 100%);
        color: #F8F8F2;
    }
    .stTextInput > div > input, .stTextArea textarea {
        background: #16161a !important;
        color: #F8F8F2 !important;
        border: 1.5px solid #6C3FB6 !important;
        border-radius: 8px !important;
        font-family: 'Inter', 'Segoe UI', 'system-ui', sans-serif !important;
    }
    .stTextInput > div > input:focus, .stTextArea textarea:focus {
        border: 1.5px solid #005F73 !important;
        outline: none !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: #0D0D0D !important;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #F8F8F2 !important;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.5rem 2rem;
        border-radius: 8px 8px 0 0;
        background: #16161a !important;
        margin-right: 2px;
    }
    .stTabs [aria-selected="true"] {
        background: #6C3FB6 !important;
        color: #F8F8F2 !important;
    }
    .stMetric {
        color: #D4AF37 !important;
    }
    .stAlert, .stError, .stWarning {
        background: #B3001B !important;
        color: #F8F8F2 !important;
        border-radius: 8px;
    }
    .stMarkdown, .stDataFrame, .stTable {
        color: #F8F8F2 !important;
        background: #16161a !important;
    }
    .stDataFrame thead tr th {
        color: #D4AF37 !important;
    }
    .stDataFrame tbody tr td {
        color: #F8F8F2 !important;
    }
    .stSpinner {
        color: #6C3FB6 !important;
    }
    .stDivider {
        border-top: 1.5px solid #005F73 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'agent' not in st.session_state:
    try:
        load_dotenv()
        
        api_key = None
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not api_key or api_key == "your_openrouter_api_key_here":
            try:
                api_key = st.secrets["OPENROUTER_API_KEY"]
            except Exception as e:
                try:
                    api_key = st.secrets.get("OPENROUTER_API_KEY")
                except:
                    pass
        
        if not api_key:
            st.error("❌ OpenRouter API key not configured!")
            st.info("💡 Please add your OPENROUTER_API_KEY to Streamlit Cloud secrets")
            st.stop()
        
        if api_key == "your_openrouter_api_key_here":
            st.error("❌ Please replace the placeholder API key with your actual OpenRouter API key!")
            st.stop()
        
        try:
            from openai import OpenAI
            test_client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                default_headers={
                    "HTTP-Referer": "https://crypto-agent.streamlit.app",
                    "X-Title": "Crypto Agent AI"
                }
            )
            test_response = test_client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
        except Exception as api_error:
            st.error(f"❌ API key test failed: {str(api_error)}")
            try:
                import requests
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://crypto-agent.streamlit.app",
                    "X-Title": "Crypto Agent AI",
                    "Content-Type": "application/json"
                }
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": "openai/gpt-4o-mini",
                        "messages": [{"role": "user", "content": "Hello"}],
                        "max_tokens": 5
                    },
                    timeout=10
                )
                if response.status_code != 200:
                    st.error(f"❌ API authentication failed: {response.status_code} - {response.text}")
                    st.stop()
            except Exception as direct_error:
                st.error(f"❌ API authentication failed: {str(direct_error)}")
                st.stop()
            
        st.session_state.agent = CryptoAgent()
    except Exception as e:
        st.error(f"❌ Error initializing Crypto Agent: {str(e)}")
        st.stop()

# Header
st.markdown('<h1 class="main-header">🚀 Crypto Agent AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #F8F8F2;">Your AI-powered cryptocurrency assistant with real-time data</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Quick Stats")
    
    # Get quick stats
    stats = st.session_state.agent.get_quick_stats()
    
    if stats:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Market Cap", stats.get("total_market_cap", "N/A"))
            st.metric("Bitcoin Dominance", stats.get("bitcoin_dominance", "N/A"))
        with col2:
            st.metric("24h Volume", stats.get("total_volume_24h", "N/A"))
            st.metric("Active Markets", stats.get("active_markets", "N/A"))
    
    st.divider()
    
    st.header("🔥 Top Coins")
    top_coins = st.session_state.agent.get_top_coins_summary(limit=5)
    
    if top_coins:
        for coin in top_coins:
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write(f"**{coin['symbol']}**")
                with col2:
                    st.write(f"${coin['price_usd']}")
                    change_color = "green" if float(coin['price_change_24h'].replace('%', '')) >= 0 else "#B3001B"
                    st.markdown(f"<span style='color: {change_color};'>{coin['price_change_24h']}</span>", unsafe_allow_html=True)
                st.divider()
    
    st.divider()
    
    st.header("💡 Example Questions")
    example_questions = [
        "What's the current Bitcoin price?",
        "Show me the top 10 cryptocurrencies",
        "What are the global market statistics?",
        "Tell me about Ethereum",
        "Which exchanges trade Bitcoin?",
        "What are the social stats for Bitcoin?",
        "Search for coins with 'coin' in the name"
    ]
    
    for question in example_questions:
        if st.button(question, key=f"example_{question}"):
            st.session_state.user_input = question

# Main content area
tab1, tab2 = st.tabs(["💬 Chat", "📈 Market Overview"])

with tab1:
    st.header("Chat with Crypto Agent AI")
    
    # Add clear conversation button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.rerun()
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages (only user and assistant)
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                message(msg["content"], is_user=True, key=f"user_{i}")
            elif msg["role"] == "assistant":
                message(msg["content"], is_user=False, key=f"assistant_{i}")
    
    # Chat input
    st.divider()
    
    # Initialize user input in session state
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    
    # Chat input form
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Ask me anything about cryptocurrencies:",
            value=st.session_state.user_input,
            height=100,
            placeholder="e.g., What's the current Bitcoin price? Show me top 10 cryptocurrencies..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button("🚀 Send", use_container_width=True)
        
        # Clear the session state input after using it
        if 'user_input' in st.session_state:
            del st.session_state.user_input
    
    # Process user input
    if submit_button and user_input.strip():
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show typing indicator
        with st.spinner("🤖 Crypto Agent is thinking..."):
            # Get AI response - pass only user and assistant messages
            conversation_history = [msg for msg in st.session_state.messages[:-1] if msg["role"] in ["user", "assistant"]]
            response = st.session_state.agent.chat(user_input, conversation_history)
            
            # Add assistant response to chat
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update the chat display
        st.rerun()

with tab2:
    st.header("📈 Market Overview")
    
    # Get top cryptocurrencies
    with st.spinner("Loading market data..."):
        result = st.session_state.agent.crypto_tools.get_top_cryptocurrencies(limit=20)
    
    if result["success"]:
        coins_data = result["data"]["coins"]
        
        # Create DataFrame for better display
        df = pd.DataFrame(coins_data)
        
        # Convert price change to numeric for sorting
        df['price_change_numeric'] = df['price_change_24h'].str.replace('%', '').astype(float)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Coins", f"{result['data']['total_coins']:,}")
        with col2:
            st.metric("Data Timestamp", datetime.fromtimestamp(result['data']['timestamp']).strftime('%H:%M:%S'))
        with col3:
            avg_change = df['price_change_numeric'].mean()
            st.metric("Avg 24h Change", f"{avg_change:.2f}%")
        with col4:
            top_gainer = df.loc[df['price_change_numeric'].idxmax()]
            st.metric("Top Gainer", f"{top_gainer['symbol']} ({top_gainer['price_change_24h']})")
        
        # Price change chart
        st.subheader("24h Price Changes")
        fig = px.bar(
            df.head(10),
            x='symbol',
            y='price_change_numeric',
            color='price_change_numeric',
            color_continuous_scale=["#B3001B", "#6C3FB6"],
            title="Top 10 Cryptocurrencies - 24h Price Change (%)"
        )
        fig.update_layout(
            xaxis_title="Cryptocurrency",
            yaxis_title="24h Change (%)",
            plot_bgcolor="#0D0D0D",
            paper_bgcolor="#0D0D0D",
            font_color="#F8F8F2",
            title_font_color="#D4AF37",
            xaxis=dict(color="#F8F8F2"),
            yaxis=dict(color="#F8F8F2")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Market cap chart
        st.subheader("Market Capitalization")
        # Convert market cap to numeric for charting
        df['market_cap_numeric'] = df['market_cap'].str.replace('$', '').str.replace(',', '').str.replace('B', '000000000').str.replace('M', '000000').str.replace('T', '000000000000').astype(float)
        
        fig2 = px.pie(
            df.head(10),
            values='market_cap_numeric',
            names='symbol',
            title="Market Cap Distribution (Top 10)",
            color_discrete_sequence=["#6C3FB6", "#B3001B", "#005F73", "#D4AF37", "#F8F8F2"]
        )
        fig2.update_layout(
            plot_bgcolor="#0D0D0D",
            paper_bgcolor="#0D0D0D",
            font_color="#F8F8F2",
            title_font_color="#D4AF37"
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Detailed table
        st.subheader("Detailed Market Data")
        display_df = df[['rank', 'symbol', 'name', 'price_usd', 'price_change_24h', 'market_cap', 'volume_24h']].copy()
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #F8F8F2; padding: 1rem; font-family: 'Inter', 'Segoe UI', 'system-ui', sans-serif;">
    <p>🚀 Powered by CoinLore API & OpenAI GPT-4o-mini via OpenRouter</p>
    <p>Made with <span style="color: #800000;">♥</span> by Ayesha Mughal</p>
</div>
""", unsafe_allow_html=True)
