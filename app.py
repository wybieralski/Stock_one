import pandas as pd
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

def load_btc_data():
    # Wczytaj dane z pliku CSV
    df = pd.read_csv('data/btc_prices.csv', parse_dates=['timestamp'], index_col='timestamp')
    return df

@app.route('/')
def index():
    try:
        # Wczytaj dane z pliku CSV
        df = load_btc_data()

        # Przygotowanie danych do przekazania do szablonu
        labels = df.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
        values = df['price'].tolist()

        return render_template('index.html', labels=labels, values=values)
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
