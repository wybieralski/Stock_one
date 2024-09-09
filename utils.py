import requests
import pandas as pd
import matplotlib.pyplot as plt

def fetch_stock_data(api_key, symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['Time Series (Daily)']).T
    df.index = pd.to_datetime(df.index)
    df = df[['4. close']].rename(columns={'4. close': 'Price'})
    df.sort_index(inplace=True)
    return df

def create_plot(df, filename='static/plot.png'):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['Price'])
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Prices Over Time')
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
