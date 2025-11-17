import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import pandas_datareader as pdr
from statsmodels.tsa.stattools import coint

load_dotenv()
TIINGO_API_KEY = os.getenv("TIINGO_APIKEY")

def check_cointegration(ticker_a, ticker_b, start_date='2015-01-01', api_key=None):
    """
    Fetches data for two tickers and checks for cointegration.
    """
    if not api_key:
        print("API key is missing.")
        return

    print(f"\n--- Testing Pair: {ticker_a} vs {ticker_b} ---")
    try:
        # Fetch data
        df_a = pdr.get_data_tiingo(ticker_a, start=start_date, api_key=api_key)
        df_b = pdr.get_data_tiingo(ticker_b, start=start_date, api_key=api_key)

        # Fix indexes
        df_a.index = df_a.index.get_level_values('date')
        df_b.index = df_b.index.get_level_values('date')
        
        df_a.to_csv(f"{ticker_a}.csv")
        df_b.to_csv(f"{ticker_b}.csv")
        data = pd.DataFrame({
            ticker_a: df_a['adjClose'],
            ticker_b: df_b['adjClose']
        }).dropna()

        if len(data) < 252:
            print(f"Not enough overlapping data to test.")
            return

        print(f"Using {len(data)} overlapping data points.")
        stock_a = data[ticker_a]
        stock_b = data[ticker_b]
        score, p_value, _ = coint(stock_a, stock_b)

        print(f"Cointegration Test P-Value: {p_value:.4f}")

        if p_value < 0.05:
            print("Result: The pair IS cointegrated (p < 0.05).")
        else:
            print("Result: The pair is NOT cointegrated.")

    except Exception as e:
        print(f"An error occurred: {e}")

# --- Run the Tests ---

# 1
check_cointegration('GOOGL', 'GOOG', api_key=TIINGO_API_KEY)

# # 2. The "ETF" Pair
# check_cointegration('SPY', 'VOO', api_key=TIINGO_API_KEY)

# # 3. energy pairs
# check_cointegration('XOM', 'CVX', api_key=TIINGO_API_KEY)

# # 4.
# check_cointegration('T', 'VZ', api_key=TIINGO_API_KEY)

# # 5.
# check_cointegration('AAPL', 'MSFT', api_key=TIINGO_API_KEY)