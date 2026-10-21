import streamlit as st
import yfinance as yf
import pandas as pd

# Set webpage browser title and icon
st.set_page_config(page_title="Market Bot", page_icon="📈", layout="wide")

st.title("📈 Real-Time Market Analysis Bot")
st.write("This bot pulls live data from global markets and generates trade analysis signals.")

# 1. Sidebar Configurations
st.sidebar.header("Bot Configurations")
market_type = st.sidebar.selectbox("Select Asset Class", ["Forex", "Crypto", "Stocks"])

# Dynamic Ticker Selection based on Asset Class
if market_type == "Forex":
    ticker = st.sidebar.text_input("Enter Forex Ticker (e.g., EURUSD=X, GBPUSD=X)", value="EURUSD=X")
elif market_type == "Crypto":
    ticker = Bell = st.sidebar.text_input("Enter Crypto Ticker (e.g., BTC-USD, ETH-USD)", value="BTC-USD")
else:
    ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, NVDA, TSLA)", value="AAPL")

interval = st.sidebar.selectbox("Chart Interval", ["1m", "5m", "15m", "30m", "1h"])

# 2. Fetch Live Market Data
st.subheader(f"Analyzing Live Feed: {ticker}")

try:
    # Pull data for the last 1 day with chosen interval
    data = yf.download(tickers=ticker, period="1d", interval=interval)
    
    if not data.empty:
        # Extract latest metrics cleanly
        latest_row = data.iloc[-1]
        open_p = float(latest_row['Open'].iloc[0] if isinstance(latest_row['Open'], pd.Series) else latest_row['Open'])
        close_p = float(latest_row['Close'].iloc[0] if isinstance(latest_row['Close'], pd.Series) else latest_row['Close'])
        high_p = float(latest_row['High'].iloc[0] if isinstance(latest_row['High'], pd.Series) else latest_row['High'])
        low_p = float(latest_row['Low'].iloc[0] if isinstance(latest_row['Low'], pd.Series) else latest_row['Low'])
        
        # Display Key Metrics Dashboard
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Current Live Price", value=f"{close_p:.4f}")
        col2.metric(label="Session High", value=f"{high_p:.4f}")
        col3.metric(label="Session Low", value=f"{low_p:.4f}")
        
        # 3. Dynamic Technical Analysis Logic
        st.markdown("---")
        st.subheader("🤖 Automated Algorithmic Signal")
        
        # Super simple momentum logic (Close vs Open)
        if close_p > open_p:
            st.success(f"🟢 **SIGNAL: CALL / BUY** | Market is experiencing upward momentum on the {interval} timeframe.")
        else:
            st.error(f"🔴 **SIGNAL: PUT / SELL** | Market is experiencing downward pressure on the {interval} timeframe.")
            
        # 4. Render Live Interactive Chart Layout
        st.markdown("---")
        st.subheader("Market Visual Trend Line")
        st.line_chart(data['Close'])
        
    else:
        st.warning("⚠️ No data returned. Please make sure your ticker symbol is typed correctly.")

except Exception as e:
    st.error(f"An error occurred while analyzing the market: {e}")
