from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np


PERIODS = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
INTERVALS = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]


def technical_analysis_page(stock_symbol, llm):
    # interval = st.selectbox("Tick Interval", INTERVALS)
    # period = st.selectbox("Tick Period", PERIODS)
    # data = get_data(stock_symbol, period=period, interval=interval)
    daily = get_data(stock_symbol, period="2y", interval="1d")
    daily = get_technical_indicators(daily)

    weekly = get_data(stock_symbol, period="10y", interval="1wk")
    weekly = get_technical_indicators(weekly)
    print("This isworking")
    fig = combined_fig(daily)
    st.plotly_chart(fig)
    prompt = get_prompt(stock_symbol, daily=daily, weekly=weekly)
    response = llm.invoke([
        ("human"), prompt
    ])
    st.markdown(response.content)



def get_data(stock_symbol: str, period: str, interval: str):
    data = yf.download(stock_symbol, period=period, interval=interval)
    return data


def get_technical_indicators(data: pd.DataFrame):
    """
    Perform a comprehensive technical analysis on the given stock symbol.
    
    Args:
        stock_symbol (str): The stock symbol to analyze.
        period (str): The time period for analysis. Default is "1y" (1 year).
    
    Returns:
        dict: A dictionary with the detailed technical analysis results.
    """
    
    # Basic Moving Averages
    for ma in [20, 50, 100, 200]:
        data[f'{ma}_MA'] = data['Close'].rolling(window=ma).mean()
    
    # Exponential Moving Averages
    for ema in [12, 26, 50, 200]:
        data[f'{ema}_EMA'] = data['Close'].ewm(span=ema, adjust=False).mean()
    
    # MACD
    data['MACD'] = data['12_EMA'] - data['26_EMA']
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    data['MACD_Histogram'] = data['MACD'] - data['Signal_Line']
    
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    data['20_MA'] = data['Close'].rolling(window=20).mean()
    data['20_SD'] = data['Close'].rolling(window=20).std()
    data['Upper_BB'] = data['20_MA'] + (data['20_SD'] * 2)
    data['Lower_BB'] = data['20_MA'] - (data['20_SD'] * 2)
    
    # Stochastic Oscillator
    low_14 = data['Low'].rolling(window=14).min()
    high_14 = data['High'].rolling(window=14).max()
    data['%K'] = (data['Close'] - low_14) / (high_14 - low_14) * 100
    data['%D'] = data['%K'].rolling(window=3).mean()
    
    # Average True Range (ATR)
    data['TR'] = np.maximum(data['High'] - data['Low'], 
                            np.maximum(abs(data['High'] - data['Close'].shift()), 
                                       abs(data['Low'] - data['Close'].shift())))
    data['ATR'] = data['TR'].rolling(window=14).mean()
    
    # On-Balance Volume (OBV)
    # data['OBV'] = (np.sign(data['Close'].diff()) * data['Volume']).cumsum()
    
    # Calculate support and resistance levels
    # data['Support'] = data['Low'].rolling(window=20).min()
    # data['Resistance'] = data['High'].rolling(window=20).max()
    
    # Identify potential breakouts
    # data['Potential_Breakout'] = np.where((data['Close'] > data['Resistance'].shift(1)), 'Bullish Breakout',
    #                              np.where((data['Close'] < data['Support'].shift(1)), 'Bearish Breakdown', 'No Breakout'))
    
    # Trend Identification
    # data['Trend'] = np.where((data['Close'] > data['200_MA']) & (data['50_MA'] > data['200_MA']), 'Bullish',
    #                 np.where((data['Close'] < data['200_MA']) & (data['50_MA'] < data['200_MA']), 'Bearish', 'Neutral'))
    
    # Volume Analysis
    data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
    # data['Volume_Trend'] = np.where(data['Volume'] > data['Volume_MA'], 'Above Average', 'Below Average')
    # data.to_csv("stock.csv")
    data = data.dropna(how='any')
    return data


def plot_indicators():
    pass

# if __name__ == "__main__":
#     print(yf_tech_analysis("SMCI"))


def combined_fig(data):

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.02,
        subplot_titles=("OHLC with Moving Averages", "Volume")
    )

    fig.add_trace(
        go.Ohlc(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            increasing=dict(line=dict(color='green')),
            decreasing=dict(line=dict(color='red')),
            name="OHLC"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['50_MA'],
            mode='lines',
            name='50-Day MA',
            line=dict(color='orange', width=1.5, dash='dot')
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data['200_MA'],
            mode='lines',
            name='200-Day MA',
            line=dict(color='purple', width=1.5, dash='dot')
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['Volume'],
            marker_color='blue',
            name='Volume'
        ),
        row=1, col=1
    )

    fig.update_layout(
        title="OHLC, Moving Averages, and Volume",
        template="plotly_dark",  # Optional: Use 'plotly' for a light theme
        xaxis=dict(title="Date"),
        yaxis=dict(title="Price"),            # Primary y-axis for price data
        yaxis2=dict(title="Volume",           # Secondary y-axis for volume
                    overlaying="y", 
                    side="right"),
    )

    fig.update(layout_xaxis_rangeslider_visible=False)


    return fig


def get_prompt(stock_name: str, daily: pd.DataFrame, weekly: pd.DataFrame):
    risk = "aggressive"

    daily_data_prompt = ""
    for ts, row in daily.tail(50).iterrows():
        daily_data_prompt += f'{str(ts).split(" ")[0]} - Open: {row["Open"]}, High: {row["High"]}, Low: {row["Low"]}, Close: {row["Close"]}, Volume: {row["Volume"]}, 20-day Average: {row["20_MA"]}, 50-day Average: {row["50_MA"]}, MACD Histogram: {row["MACD_Histogram"]}'
        daily_data_prompt += "\n"

    weekly_data_prompt = ""
    for ts, row in weekly.tail(50).iterrows():
        weekly_data_prompt += f'{str(ts).split(" ")[0]} - Open: {row["Open"]}, High: {row["High"]}, Low: {row["Low"]}, Close: {row["Close"]}, Volume: {row["Volume"]}, 20-day Average: {row["20_MA"]}, 50-day Average: {row["50_MA"]}, MACD Histogram: {row["MACD_Histogram"]}'
        weekly_data_prompt += "\n"

    prompt = f"""
    I am going to give you technical indicators about a stock. This will include the last 50 ticks on a
    daily and weekly timeframe. I want you to analyze those indicators and determine if this is a good time 
    to buy for a {risk} investor. 

    Please justify your responses, and keep it to no more than fifty words. Keep in mind both short term and long term trends, resistance levels and trend
    reversal signals. 

    Stock Name: {stock_name}

    Last 50 Ticks Daily:
    {daily_data_prompt}

    Last 50 Ticks Weekly:
    {weekly_data_prompt}


    """
    return prompt


if __name__ == "__main__":
    technical_analysis_page("AAPL")