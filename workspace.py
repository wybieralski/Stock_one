import requests
import pandas as pd


def fetch_and_save_btc_data(**kwargs):
    print(f"DAG STARTED")
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': 'BTCUSDT',
        'interval': '1m',
        'limit': 500
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        timestamps = [int(entry[0]) for entry in data]
        prices = [float(entry[4]) for entry in data]
        df = pd.DataFrame({'timestamp': timestamps, 'price': prices})
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        print(f"Data fetched")
        # Zapisz dane do pliku CSV
        df.to_csv('data/btc_prices.csv')
        print(f"Data saved to /Users/lukaszw/PycharmProjects/Stock_one/Stock_one/data/btc_prices.csv")
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania danych: {e}")

fetch_and_save_btc_data()