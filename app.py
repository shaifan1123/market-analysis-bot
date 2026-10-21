import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Set page structure and wide viewport layout
st.set_page_config(page_title="Live AI Market Engine", page_icon="⚡", layout="wide")

st.title("⚡ Live Real-Time Market Analysis Suite")
st.write("This application automatically streams live data feed tickers, handles structural timeframes, and calculates signals.")

# ==========================================
# 1. TIME AND PAIR SIDEBAR CONTROL PANEL
# ==========================================
st.sidebar.header("🎛️ Control Panel")

market_type = st.sidebar.selectbox("Select Asset Class", ["Forex", "Crypto", "Stocks"])

# Core Ticker Input Config
if market_type == "Forex":
    ticker = st.sidebar.text_input("Asset Ticker (e.g., EURUSD=X, GBPUSD=X)", value="EURUSD=X")
elif market_type == "Crypto":
    ticker = st.sidebar.text_input("Asset Ticker (e.g., BTC-USD, ETH-USD)", value="BTC-USD")
else:
    ticker = st.sidebar.text_input("Asset Ticker (e.g., AAPL, NVDA)", value="AAPL")

# Precise Timeframe Selector Management
timeframe = st.sidebar.selectbox(
    "Select Chart Timeframe Interval",
    options=["1m", "2m", "5m", "15m", "30m", "60m"],
    index=0  # Default to 1-minute chart execution
)

# Automated Real-time Auto-Refresh Cycle Input
refresh_rate = st.sidebar.slider("Live Price Stream Refresh (Seconds)", min_value=2, max_value=30, value=5)

# Calculate historic padding required dynamically for yfinance limitations
period_window = "1d"
if timeframe in ["60m"]:
    period_window = "5d"

# ==========================================
# 2. HIGH-SPEED REAL-TIME DATA STREAM
# ==========================================

# Using fragment to handle isolated high-speed refresh loops cleanly
@st.fragment(run_every=refresh_rate)
def live_trading_dashboard():
    # Show active tracking state indicator
    current_time_str = datetime.now().strftime("%H:%M:%S")
    st.write(f"🔄 **Live Data Stream Active:** Auto-updated at `{current_time_str}` (Refreshing every {refresh_rate}s)")
    
    try:
        # Download market dataframe with selected timeframe constraints
        df = yf.download(tickers=ticker, period=period_window, interval=timeframe, progress=False)
        
        if not df.empty:
            # Drop empty columns and sort chronology
            df = df.dropna()
            
            # Extract clean float variables directly from the last rows safely
            live_close = float(df['Close'].iloc[-1])
            live_open = float(df['Open'].iloc[-1])
            live_high = float(df['High'].iloc[-1])
            live_low = float(df['Low'].iloc[-1])
            
            # Get previous candle close price to find delta direction
            prev_close = float(df['Close'].iloc[-2]) if len(df) > 1 else live_close
            price_delta = live_close - prev_close
            
            # Display Real-Time Price Cards
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label=f"🔴 LIVE PRICE ({ticker})", value=f"{live_close:.5f}", delta=f"{price_delta:.5f}")
            col2.metric(label="📊 OPEN", value=f"{live_open:.5f}")
            col3.metric(label="📈 HIGH", value=f"{live_high:.5f}")
            col4.metric(label="📉 LOW", value=f"{live_low:.5f}")
            
            # ==========================================
            # 3. REAL-TIME TECHNICAL SIGNAL GENERATOR
            # ==========================================
            st.markdown("---")
            st.subheader("🤖 Algorithmic Order Signal Engine")
            
            # Multi-layered momentum validation logic (Close vs Open + Simple Moving Average direction)
            df['SMA_5'] = df['Close'].rolling(window=5).mean()
            current_sma = float(df['SMA_5'].iloc[-1]) if not pd.isna(df['SMA_5'].iloc[-1]) else live_close
            
            is_bullish_candle = live_close > live_open
            is_above_trend = live_close > current_sma
            
            # Order routing evaluation criteria
            if is_bullish_candle and is_above_trend:
                st.success(f"🟢 **SIGNAL: CALL / BUY (HIGH CONFIDENCE)**\n\nMarket trend structures match upward velocity on the `{timeframe}` timeframe. Price action is breaking above moving patterns.")
            elif not is_bullish_candle and not is_above_trend:
                st.error(f"🔴 **SIGNAL: PUT / SELL (HIGH CONFIDENCE)**\n\nMarket trend structures confirm downward distribution on the `{timeframe}` timeframe. Bearish pressure is dominating the current candle.")
            else:
                st.warning(f"🟡 **SIGNAL: NEUTRAL / STANDBY**\n\nConflicting momentum markers on the `{timeframe}` charts. Market is consolidating. Wait for structural breakout.")
            
            # ==========================================
            # 4. STRUCTURAL CHART REPRESENTATION
            # ==========================================
            st.markdown("---")
            st.subheader(f"📊 Real Market Trend Line Chart ({timeframe})")
            
            # Format dataframe specifically for native Streamlit charting (last 30 intervals)
            chart_data = df.tail(30).copy()
            
            # Render a high-performance chart that turns green for up trends and red for down trends
            st.area_chart(chart_data['Close'], color="#00ffcc" if live_close > live_open else "#ff3366")
            
            # Provide clean tabular overview data spreadsheet below
            with st.expander("👁️ View Live Raw Feed Spreadsheet Ledger"):
                st.dataframe(df.tail(10), use_container_width=True)
                
        else:
            st.warning("⚠️ Waiting for active exchange response data. Verify ticker is properly structured.")
            
    except Exception as error:
        st.error(f"Streaming data channel error: {error}")

# Run streaming architecture execution line
live_trading_dashboard()
