import streamlit as st
import pandas as pd
from streamlit_chat import message
from utils import api, helpers, chatbot
import asyncio

# --- Page Config ---
st.set_page_config(
    page_title="Crypto AI Dashboard",
    layout="wide",
    page_icon="💰",
    initial_sidebar_state="expanded"
)

# --- Load CSS and Footer ---
helpers.load_css("styles/style.css")
st.markdown(helpers.get_footer(), unsafe_allow_html=True)

# --- Data Caching ---
@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    """Loads and caches data from the CoinLore API."""
    try:
        global_stats = api.get_global_stats()
        top_100_data = api.get_top_coins(100)
        df = pd.DataFrame(top_100_data.get('data', []))
        if not df.empty:
            numeric_columns = [
                'price_usd', 'percent_change_24h', 'percent_change_1h',
                'percent_change_7d', 'market_cap_usd', 'volume24'
            ]
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
        
        info = top_100_data.get('info', {})
        return global_stats, df, info
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, pd.DataFrame(), {}

# Load data at startup
global_stats, df_coins, api_info = load_data()

# --- Sidebar ---
with st.sidebar:
    st.title("🤖 Crypto AI")
    if global_stats:
        stats = global_stats[0]
        st.subheader("📊 Global Market Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Market Cap", f"${float(stats['total_mcap']):,.0f}B")
            st.metric("BTC Dom.", f"{stats['btc_d']}%")
        with col2:
            st.metric("24h Vol.", f"${float(stats['total_volume']):,.0f}B")
            st.metric("Active Markets", f"{stats['active_markets']:,}")

    if not df_coins.empty:
        st.subheader("💎 Top 5 Coins")
        for _, coin in df_coins.head().iterrows():
            price = float(coin['price_usd'])
            change = float(coin['percent_change_24h'])
            delta_color = "green" if change > 0 else "red"
            st.markdown(f"""
            <div class="coin-card">
                <span class="coin-symbol">{coin['symbol']}</span>
                <span class="coin-price">${price:,.2f}</span>
                <span class="coin-change" style="color: {delta_color}">{change:+.2f}%</span>
            </div>
            """, unsafe_allow_html=True)

    st.subheader("❓ Example Questions")
    example_questions = [
        "What's the current Bitcoin price?",
        "Show me the top 10 cryptocurrencies",
        "What are the global market statistics?",
        "Tell me about Ethereum"
    ]
    for q in example_questions:
        if st.button(q, key=f"btn_{q}"):
            if "messages" not in st.session_state:
                st.session_state.messages = []
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()

# --- Main Content ---
tab1, tab2 = st.tabs(["💰 Dashboard", "💬 AI Chat"])

with tab1:
    st.header("Market Overview")
    if global_stats and not df_coins.empty:
        # Data Table with improved styling
        st.markdown("### 📈 Top 20 Cryptocurrencies")
        df_display = df_coins.head(20).copy()
        
        # Format the columns
        df_display['price_usd'] = df_display['price_usd'].apply(lambda x: f"${float(x):,.2f}")
        df_display['market_cap_usd'] = df_display['market_cap_usd'].apply(lambda x: f"${float(x):,.0f}")
        df_display['percent_change_24h'] = df_display['percent_change_24h'].apply(lambda x: f"{float(x):+.2f}%")
        df_display['volume24'] = df_display['volume24'].apply(lambda x: f"${float(x):,.0f}")
        
        # Rename columns for display
        df_display = df_display.rename(columns={
            'rank': 'Rank',
            'symbol': 'Symbol',
            'name': 'Name',
            'price_usd': 'Price',
            'percent_change_24h': '24h Change',
            'market_cap_usd': 'Market Cap',
            'volume24': '24h Volume'
        })
        
        st.dataframe(
            df_display[['Rank', 'Symbol', 'Name', 'Price', '24h Change', 'Market Cap', '24h Volume']],
            hide_index=True,
            use_container_width=True
        )

with tab2:
    st.header("AI Crypto Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your crypto AI assistant. How can I help you today?"}
        ]

    # Chat container
    chat_container = st.container()
    
    # Input container at the bottom
    input_container = st.container()
    
    # Display chat messages
    with chat_container:
        for i, msg in enumerate(st.session_state.messages):
            message(
                msg["content"],
                is_user=msg["role"] == "user",
                key=f"msg_{i}_{msg['role']}",
                avatar_style="adventurer" if msg["role"] == "user" else "bottts",
                seed=123 if msg["role"] == "user" else 42
            )
    
    # Chat input at the bottom
    with input_container:
        if prompt := st.chat_input("Ask me anything about crypto...", key="chat_input"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Thinking..."):
                response_message = chatbot.run_conversation(st.session_state.messages)
                st.session_state.messages.append(response_message)
                st.rerun()
