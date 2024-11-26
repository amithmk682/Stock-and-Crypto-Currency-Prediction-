import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Custom CSS to style the app similar to TradingView
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    body {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Roboto', sans-serif;
    }
    .main {
        background-color: #0d1117;
        color: #c9d1d9;
        padding: 20px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #58a6ff;
        text-align: center;
    }
    .stTextInput label {
        font-size: 1.2em;
        color: #c9d1d9;
    }
    .stButton button {
        background-color: #238636;
        color: white;
        border-radius: 5px;
        font-size: 1.2em;
        width: 100%;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #2ea043;
        color: white;
    }
    .stMarkdown p {
        color: #c9d1d9;
        text-align: center;
    }
    .stDataFrame {
        background-color: #161b22;
        color: #c9d1d9;
    }
    .stPlotlyChart {
        background-color: #161b22;
        color: #c9d1d9;
    }
    .title-wrapper {
        background-color: #0d1117;
        text-align: center;
        padding: 20px;
    }
    .title-wrapper h1 {
        color: #58a6ff;
    }
    .input-wrapper {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .input-wrapper input {
        width: 300px;
        padding: 10px;
        font-size: 1.2em;
        border-radius: 5px;
        border: 1px solid #30363d;
        margin-right: 10px;
        background-color: #161b22;
        color: #c9d1d9;
    }
    .input-wrapper button {
        background-color: #238636;
        color: white;
        border-radius: 5px;
        font-size: 1.2em;
        padding: 10px 20px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .input-wrapper button:hover {
        background-color: #2ea043;
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
        padding: 20px;
        background-color: #21262d;
        border-radius: 10px;
        margin: 20px 0;
    }
    .stat {
        flex: 1;
        text-align: center;
        color: #c9d1d9;
        padding: 10px;
        min-width: 200px;
    }
    .stat h3 {
        color: #58a6ff;
        margin-bottom: 10px;
    }
    .stat p {
        font-size: 1.5em;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title-wrapper'><h1>Stock Trend Analysis</h1></div>", unsafe_allow_html=True)

# User input for stock ticker and time frame
user_input = st.text_input('Enter Stock Ticker (e.g., AAPL)', 'AAPL')
time_frames = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max']
selected_time_frame = st.selectbox('Select Time Frame', time_frames, index=8)

# Calculate start and end dates based on the selected time frame
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
    start_date = '2010-01-01'  # Default to fetching all available data

# Fetch stock data
ticker = yf.Ticker(user_input)
df = ticker.history(start=start_date, end=end_date, auto_adjust=True)

# Display the first few rows of the data
st.markdown("<div class='data-section'><h2>Historical Data</h2>", unsafe_allow_html=True)
st.dataframe(df.head())

# Calculate key statistics
max_close = df['Close'].max()
min_close = df['Close'].min()
mean_close = df['Close'].mean()
median_close = df['Close'].median()
percentile_25 = df['Close'].quantile(0.25)
percentile_75 = df['Close'].quantile(0.75)
std_close = df['Close'].std()
pct_change = df['Close'].pct_change().mean() * 100

# Display key statistics
st.markdown("<div class='stats-box'>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Highest Closing Price</h3><p>₹{max_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Lowest Closing Price</h3><p>₹{min_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Average Closing Price</h3><p>₹{mean_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Median Closing Price</h3><p>₹{median_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>25th Percentile</h3><p>₹{percentile_25:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>75th Percentile</h3><p>₹{percentile_75:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Standard Deviation</h3><p>₹{std_close:.2f}</p></div>", unsafe_allow_html=True)
st.markdown(f"<div class='stat'><h3>Average Percentage Change</h3><p>{pct_change:.2f}%</p></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Plotting the closing price using Plotly
st.markdown("<div class='plot-section'><h2>Closing Price vs Time Chart</h2>", unsafe_allow_html=True)
fig = go.Figure()

fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close', line=dict(color='cyan')))
fig.update_layout(
    title='Closing Price vs Time',
    xaxis_title='Time',
    yaxis_title='Closing Price (₹)',
    template='plotly_dark',
    paper_bgcolor='#161b22',
    plot_bgcolor='#161b22',
    font=dict(color='#c9d1d9')
)
st.plotly_chart(fig)

# Plotting the volume
st.markdown("<div class='plot-section'><h2>Volume vs Time Chart</h2>",
unsafe_allow_html=True)
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

# Plotting the moving averages
st.markdown("<div class='plot-section'><h2>Moving Averages vs Time Chart</h2>", unsafe_allow_html=True)
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