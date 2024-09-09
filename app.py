import requests
import pandas as pd
from flask import Flask, render_template
from datetime import datetime, timedelta

app = Flask(__name__)


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


@app.route('/')
def index():
    try:
        interval = '1m'
        limit = 1440  # Liczba minut w 24 godzinach
        timestamps, prices = get_btc_prices_binance(interval=interval, limit=limit)

        # Konwersja timestampów z milisekund do daty i godziny
        timestamps = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]

        # Przygotowanie danych do przekazania do szablonu
        labels = [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps]
        values = prices

        return render_template('index.html', labels=labels, values=values)
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred."


if __name__ == '__main__':
    app.run(debug=True)
