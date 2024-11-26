import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Custom CSS for the app styling (keeps the TradingView-like appearance)
st.markdown("""
    <style>
    /* Styling similar to the stock market app */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    body { background-color: #0d1117; color: #c9d1d9; font-family: 'Roboto', sans-serif; }
    .main { background-color: #0d1117; color: #c9d1d9; padding: 20px; }
    h1, h2, h3, h4, h5, h6 { color: #58a6ff; text-align: center; }
    /* Additional custom styling remains unchanged */
    </style>
""", unsafe_allow_html=True)

# Title for the cryptocurrency prediction
st.markdown("<div class='title-wrapper'><h1>Cryptocurrency Trend Analysis</h1></div>", unsafe_allow_html=True)

# User input for selecting cryptocurrency ticker and time frame
user_input = st.text_input('Enter Crypto Ticker (e.g., BTC-USD)', 'BTC-USD')
time_frames = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max']
selected_time_frame = st.selectbox('Select Time Frame', time_frames, index=8)

# Calculate start and end dates for crypto data
end_date = datetime.today().strftime('%Y-%m-%d')
if selected_time_frame == '1d':
    start_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
elif selected_time_frame == '5d':
    start_date = (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')
elif selected_time_frame == '1mo':
    start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
elif selected_time_frame == '3mo':
    start_date = (datetime.today() - timedelta(days=3*30)).strftime('%Y-%m-%d')
elif selected_time_frame == '6mo':
    start_date = (datetime.today() - timedelta(days=6*30)).strftime('%Y-%m-%d')
elif selected_time_frame == '1y':
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
elif selected_time_frame == '2y':
    start_date = (datetime.today() - timedelta(days=2*365)).strftime('%Y-%m-%d')
elif selected_time_frame == '5y':
    start_date = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')
else:
    start_date = '2010-01-01'  # Default for max time frame

# Fetch cryptocurrency data using yfinance
ticker = yf.Ticker(user_input)
df = ticker.history(start=start_date, end=end_date, auto_adjust=True)

# Display historical data for the selected cryptocurrency
st.markdown("<div class='data-section'><h2>Historical Crypto Data</h2></div>", unsafe_allow_html=True)
st.dataframe(df.head())

# Calculate key statistics for the cryptocurrency
max_close = df['Close'].max()
min_close = df['Close'].min()
mean_close = df['Close'].mean()
median_close = df['Close'].median()
percentile_25 = df['Close'].quantile(0.25)
percentile_75 = df['Close'].quantile(0.75)
std_close = df['Close'].std()
pct_change = df['Close'].pct_change().mean() * 100

# Display key stats in the same style as the stock code
st.markdown("<div class='stats-box'>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Highest Closing Price</h3><p>${max_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Lowest Closing Price</h3><p>${min_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Average Closing Price</h3><p>${mean_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Median Closing Price</h3><p>${median_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>25th Percentile</h3><p>${percentile_25:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>75th Percentile</h3><p>${percentile_75:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Standard Deviation</h3><p>${std_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Average Percentage Change</h3><p>{pct_change:.2f}%</p></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Plot the closing price for the cryptocurrency
st.markdown("<div class='plot-section'><h2>Crypto Closing Price vs Time</h2></div>", unsafe_allow_html=True)
fig = go.Figure()

fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close', line=dict(color='cyan')))
fig.update_layout(
    title='Closing Price vs Time',
    xaxis_title='Time',
    yaxis_title='Closing Price ($)',
    template='plotly_dark',
    paper_bgcolor='#161b22',
    plot_bgcolor='#161b22',
    font=dict(color='#c9d1d9')
)
st.plotly_chart(fig)

# Plot the volume for cryptocurrency
st.markdown("<div class='plot-section'><h2>Crypto Volume vs Time</h2>", unsafe_allow_html=True)
fig_vol = go.Figure()

fig_vol.add_trace(go.Scatter(x=df.index, y=df['Volume'], mode='lines', name='Volume', line=dict(color='orange')))
fig_vol.update_layout(
    title='Volume vs Time',
    xaxis_title='Time',
    yaxis_title='Volume',
    template='plotly_dark',
    paper_bgcolor='#161b22',
    plot_bgcolor='#161b22',
    font=dict(color='#c9d1d9')
)
st.plotly_chart(fig_vol)

# Plotting the moving averages for cryptocurrency
st.markdown("<div class='plot-section'><h2>Crypto Moving Averages vs Time</h2></div>", unsafe_allow_html=True)
df['MA50'] = df['Close'].rolling(window=50).mean()
df['MA200'] = df['Close'].rolling(window=200).mean()

fig_ma = go.Figure()

fig_ma.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close', line=dict(color='cyan')))
fig_ma.add_trace(go.Scatter(x=df.index, y=df['MA50'], mode='lines', name='50-Day MA', line=dict(color='magenta')))
fig_ma.add_trace(go.Scatter(x=df.index, y=df['MA200'], mode='lines', name='200-Day MA', line=dict(color='yellow')))
fig_ma.update_layout(
    title='Moving Averages vs Time',
    xaxis_title='Time',
    yaxis_title='Price',
    template='plotly_dark',
    paper_bgcolor='#161b22',
    plot_bgcolor='#161b22',
    font=dict(color='#c9d1d9')
)
st.plotly_chart(fig_ma)

st.markdown("</div>", unsafe_allow_html=True)
