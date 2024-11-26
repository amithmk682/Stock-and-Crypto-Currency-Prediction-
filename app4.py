import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

# Set a fixed conversion rate for USD to INR (you can update this as needed)
usd_to_inr = 82.50  # Example conversion rate (check actual rate if you want live rates)

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Roboto', sans-serif;
    }
    .title-wrapper {
        text-align: center;
        padding: 20px;
    }
    .title-wrapper h1 {
        color: #58a6ff;
    }
    .input-wrapper {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .data-section, .stats-section, .plot-section {
        padding: 20px;
        background-color: #161b22;
        margin: 20px 0;
        border-radius: 10px;
    }
    .stats-box {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
    }
    .stat {
        text-align: center;
        color: #c9d1d9;
        padding: 20px;
        flex: 1;
    }
    .stat h3 {
        color: #58a6ff;
    }
    .plot-section {
        background-color: #161b22;
        padding: 20px;
        margin: 20px 0;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for selecting asset type (Stock or Crypto)
st.sidebar.title("Select Asset Type")
asset_type = st.sidebar.radio("Choose Asset Type", ["Stock", "Crypto"])

# Sidebar for input
if asset_type == "Crypto":
    default_ticker = 'BTC-USD'
else:
    default_ticker = 'AAPL'

user_input = st.sidebar.text_input('Enter Ticker', default_ticker)
time_frames = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max']
selected_time_frame = st.sidebar.selectbox('Select Time Frame', time_frames, index=8)

# Calculate start and end dates for the selected time frame
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

# Fetch data using yfinance
ticker = yf.Ticker(user_input)
df = ticker.history(start=start_date, end=end_date, auto_adjust=True)

# Convert stock prices from USD to INR if asset type is "Stock"
if asset_type == "Stock":
    df['Close'] = df['Close'] * usd_to_inr
    df['Open'] = df['Open'] * usd_to_inr
    df['High'] = df['High'] * usd_to_inr
    df['Low'] = df['Low'] * usd_to_inr

# Title for the application
st.markdown(f"<div class='title-wrapper'><h1>Trend Analysis for {asset_type}</h1></div>", unsafe_allow_html=True)

# Display Historical Data Section
st.markdown("<div class='data-section'><h2>Historical Data</h2></div>", unsafe_allow_html=True)
st.dataframe(df.head())

# Calculate and display key statistics
max_close = df['Close'].max()
min_close = df['Close'].min()
mean_close = df['Close'].mean()
median_close = df['Close'].median()
percentile_25 = df['Close'].quantile(0.25)
percentile_75 = df['Close'].quantile(0.75)
std_close = df['Close'].std()
pct_change = df['Close'].pct_change().mean() * 100

# Display Key Stats Section
st.markdown("<div class='stats-box'>", unsafe_allow_html=True)
currency = '₹' if asset_type == "Stock" else '$'
st.markdown(f"<div class='stat'><h3>Highest Closing Price</h3><p>{currency}{max_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Lowest Closing Price</h3><p>{currency}{min_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Average Closing Price</h3><p>{currency}{mean_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Median Closing Price</h3><p>{currency}{median_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>25th Percentile</h3><p>{currency}{percentile_25:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>75th Percentile</h3><p>{currency}{percentile_75:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Standard Deviation</h3><p>{currency}{std_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Average Percentage Change</h3><p>{pct_change:.2f}%</p></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Plot the Closing Price over Time
st.markdown("<div class='plot-section'><h2>Closing Price vs Time Chart</h2></div>", unsafe_allow_html=True)
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close', line=dict(color='cyan')))
fig.update_layout(
    title=f'{user_input} Closing Price vs Time',
    xaxis_title='Time',
    yaxis_title=f'Closing Price ({currency})',
    template='plotly_dark',
    paper_bgcolor='#161b22',
    plot_bgcolor='#161b22',
    font=dict(color='#c9d1d9')
)
st.plotly_chart(fig)

# Plot the Volume over Time
st.markdown("<div class='plot-section'><h2>Volume vs Time Chart</h2></div>", unsafe_allow_html=True)
fig_vol = go.Figure()
fig_vol.add_trace(go.Scatter(x=df.index, y=df['Volume'], mode='lines', name='Volume', line=dict(color='orange')))
fig_vol.update_layout(
    title=f'{user_input} Volume vs Time',
    xaxis_title='Time',
    yaxis_title='Volume',
    template='plotly_dark',
    paper_bgcolor='#161b22',
    plot_bgcolor='#161b22',
    font=dict(color='#c9d1d9')
)
st.plotly_chart(fig_vol)

# Plot the Moving Averages (50 and 200)
st.markdown("<div class='plot-section'><h2>Moving Averages vs Time Chart</h2></div>", unsafe_allow_html=True)
df['MA50'] = df['Close'].rolling(window=50).mean()
df['MA200'] = df['Close'].rolling(window=200).mean()
fig_ma = go.Figure()
fig_ma.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close', line=dict(color='cyan')))
fig_ma.add_trace(go.Scatter(x=df.index, y=df['MA50'], mode='lines', name='50-Day MA', line=dict(color='magenta')))
fig_ma.add_trace(go.Scatter(x=df.index, y=df['MA200'], mode='lines', name='200-Day MA', line=dict(color='yellow')))
fig_ma.update_layout(
    title=f'{user_input} Moving Averages vs Time',
    xaxis_title='Time',
    yaxis_title=f'Price ({currency})',
    template='plotly_dark',
    paper_bgcolor='#161b22',
    plot_bgcolor='#161b22',
    font=dict(color='#c9d1d9')
)
st.plotly_chart(fig_ma)
