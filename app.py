import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Set layout configurations matching professional monitoring rigs
st.set_page_config(page_title="AI Candlestick Engine", page_icon="📊", layout="wide")

st.title("📊 Real-Time Candlestick Analysis Engine")
st.write("Streams accurate market ticks, drops hierarchical structural bugs, and generates pure algorithmic signals.")

# ==========================================
# 1. LIVE CONTROL SIDEBAR PANEL
# ==========================================
st.sidebar.header("🎛️ Control Terminal")

market_type = st.sidebar.selectbox("Select Asset Class", ["Forex", "Crypto", "Stocks"])

# Configuration validation structures
if market_type == "Forex":
    ticker = st.sidebar.text_input("Asset Ticker (e.g., EURUSD=X, GBPUSD=X)", value="EURUSD=X")
elif market_type == "Crypto":
    ticker = st.sidebar.text_input("Asset Ticker (e.g., BTC-USD, ETH-USD)", value="BTC-USD")
else:
    ticker = st.sidebar.text_input("Asset Ticker (e.g., AAPL, NVDA)", value="AAPL")

# Precision Timeframe Management Dropdown
timeframe = st.sidebar.selectbox(
    "Chart Frame Interval",
    options=["1m", "2m", "5m", "15m", "30m", "60m"],
    index=0  # Primary real-world 1-minute candlestick tracking
)

refresh_rate = st.sidebar.slider("Stream Auto-Refresh Loop (Seconds)", min_value=2, max_value=30, value=5)

# Safety window lookback bounds
period_window = "1d"
if timeframe in ["60m"]:
    period_window = "5d"

# ==========================================
# 2. DATA FEEDS & ENGINE CORRECTIONS
# ==========================================
@st.fragment(run_every=refresh_rate)
def live_trading_dashboard():
    current_time_str = datetime.now().strftime("%H:%M:%S")
    st.write(f"🔄 **Live Engine Status:** Connected | Current Frame Updated at `{current_time_str}` (Streaming every {refresh_rate}s)")
    
    try:
        # Fetching raw data arrays
        df = yf.download(tickers=ticker, period=period_window, interval=timeframe, progress=False)
        
        if not df.empty:
            # 💡 MANDATORY FIX: If yfinance passes back MultiIndex layers, flatten columns instantly!
            if isinstance(df.columns, pd.MultiIndex):
                # Pull out the first element tier ('Open', 'High', etc.) explicitly to remove column level duplication
                df.columns = [col[0] for col in df.columns]
            
            # Drop empty buffer entries
            df = df.dropna()
            
            # Target clean index rows sequentially
            latest_candle = df.iloc[-1]
            previous_candle = df.iloc[-2] if len(df) > 1 else latest_candle
            
            # Cast raw items into single precision floating metrics with absolute structural safety
            live_close = float(latest_candle['Close'])
            live_open = float(latest_candle['Open'])
            live_high = float(latest_candle['High'])
            live_low = float(latest_candle['Low'])
            
            prev_close = float(previous_candle['Close'])
            price_delta = live_close - prev_close
            
            # Display Dashboard Grid
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label=f"🔴 LIVE PRICE ({ticker})", value=f"{live_close:.5f}", delta=f"{price_delta:.5f}")
            col2.metric(label="📊 OPEN", value=f"{live_open:.5f}")
            col3.metric(label="📈 HIGH", value=f"{live_high:.5f}")
            col4.metric(label="📉 LOW", value=f"{live_low:.5f}")
            
            # ==========================================
            # 3. ALGORITHMIC MATHEMATICAL SIGNALS
            # ==========================================
            st.markdown("---")
            st.subheader("🤖 Algorithmic Momentum Decision Matrix")
            
            # Append moving pattern mathematical layer
            df['SMA_5'] = df['Close'].rolling(window=5).mean()
            current_sma = float(df['SMA_5'].iloc[-1]) if not pd.isna(df['SMA_5'].iloc[-1]) else live_close
            
            is_bullish = live_close > live_open
            is_above_trend = live_close > current_sma
            
            if is_bullish and is_above_trend:
                st.success(f"🟢 **SIGNAL: CALL / BUY (STRONG TREND MOMENTUM)**\n\nPrice action closed green and broke clear above the structural Moving Trend Line (`{timeframe}` scale). Velocity is highly favorable.")
            elif not is_bullish and not is_above_trend:
                st.error(f"🔴 **SIGNAL: PUT / SELL (STRONG BEARISH DIRECTION)**\n\nPrice action distribution dropped below structural open boundaries and fell beneath the `{timeframe}` Moving Average floor. Selling weight is dominating.")
            else:
                st.warning(f"🟡 **SIGNAL: NEUTRAL / STANDBY (MARKET CONSOLIDATION)**\n\nIndecisive indicators are triggering inside the active trend channels. Price action is ranging sideways. Standby for true breakout signatures.")
                
            # ==========================================
            # 4. LIVING CANDLESTICK CHART PLOT
            # ==========================================
            st.markdown("---")
            st.subheader(f"🕯️ Live Exchange Candle Stream ({timeframe} View)")
            
            # Subset layout arrays cleanly for view optimization
            chart_slice = df.tail(35)
            
            # Construct active plotly green/red candle matrices
            fig = go.Figure(data=[go.Candlestick(
                x=chart_slice.index,
                open=chart_slice['Open'],
                high=chart_slice['High'],
                low=chart_slice['Low'],
                close=chart_slice['Close'],
                increasing_line_color='#00ffcc', # Bright electric green candles
                decreasing_line_color='#ff3366', # Bright electric red candles
                name=ticker
            )])
            
            # Format UI layouts cleanly
            fig.update_layout(
                margin=dict(l=20, r=20, t=10, b=10),
                template="plotly_dark",
                xaxis_rangeslider_visible=False, # Removes the clunky bottom navigation bar
                yaxis_title="Asset Exchange Price",
                xaxis_title="Time / Data Window Chronology"
            )
            
            # Direct rendering call into the web interface
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("👁️ View Live Raw Feed Spreadsheet Ledger"):
                st.dataframe(df.tail(10), use_container_width=True)
                
        else:
            st.warning("⚠️ Connected to API successfully but waiting for data stream response arrays.")
            
    except Exception as error:
        st.error(f"Streaming data channel error: {error}")

# Direct runner execution command
live_trading_dashboard()
