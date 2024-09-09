import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def get_btc_prices_binance(interval='1m', limit=1440):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': 'BTCUSDT',
        'interval': interval,
        'limit': limit
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        timestamp_list = []
        prices_list = []

        for entry in data:
            timestamp_list.append(int(entry[0]))
            prices_list.append(float(entry[4]))

        return timestamp_list, prices_list

    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania danych: {e}")
        return [], []


def plot_btc_prices_last_24_hours():
    interval = '1m'
    limit = 1440  # Liczba minut w 24 godzinach
    timestamps, prices = get_btc_prices_binance(interval=interval, limit=limit)

    if timestamps and prices:
        # Konwersja danych do DataFrame
        df = pd.DataFrame({'timestamp': timestamps, 'price': prices})
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        # Tworzenie wykresu
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['price'], label='Cena BTC', color='blue')
        plt.title('Cena Bitcoina (BTC) w ciągu ostatnich 24 godzin')
        plt.xlabel('Czas')
        plt.ylabel('Cena (USD)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()  # Automatyczne dopasowanie wykresu
        plt.show()


if __name__ == '__main__':
    plot_btc_prices_last_24_hours()
