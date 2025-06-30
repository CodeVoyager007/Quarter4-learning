import plotly.graph_objects as go
import pandas as pd

# Color palette from user request
COLORS = {
    "background": "#0D0D0D",
    "text": "#F8F8F2",
    "primary": "#6C3FB6",
    "secondary": "#B3001B",
    "highlight": "#005F73",
    "gold": "#D4AF37"
}

def create_price_change_bar_chart(df):
    """Creates an interactive bar chart of 24h price changes."""
    df_sorted = df.sort_values(by="percent_change_24h", ascending=False)
    
    colors = [COLORS['highlight'] if x > 0 else COLORS['secondary'] for x in df_sorted['percent_change_24h']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_sorted['symbol'],
        y=df_sorted['percent_change_24h'],
        marker_color=colors,
        text=df_sorted['percent_change_24h'].apply(lambda x: f"{x:.2f}%"),
        textposition='auto'
    ))

    fig.update_layout(
        title="Top 10 Cryptocurrencies - 24h Price Change",
        xaxis_title="Cryptocurrency",
        yaxis_title="Price Change (%)",
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font_color=COLORS['text'],
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        hovermode='x unified'
    )
    return fig

def create_market_cap_pie_chart(df):
    """Creates an interactive pie chart of market cap distribution."""
    fig = go.Figure(data=[go.Pie(
        labels=df['name'],
        values=df['market_cap_usd'],
        hole=.3,
        pull=[0.1 if i == 0 else 0 for i in range(len(df))],
        marker_colors=[COLORS['primary'], COLORS['highlight'], COLORS['gold'], COLORS['secondary']] * (len(df) // 4 + 1)
    )])

    fig.update_traces(
        textinfo='percent+label',
        insidetextorientation='radial'
    )

    fig.update_layout(
        title_text="Top 10 Market Cap Distribution",
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font_color=COLORS['text'],
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    return fig 