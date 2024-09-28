import subprocess
import pandas as pd
from flask import Flask, render_template
from datetime import datetime
import threading

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

# Funkcja do uruchomienia Airflow
def run_airflow():
    try:
        # Uruchomienie webservera
        subprocess.Popen(["airflow", "webserver", "--port", "8080"])
        # Uruchomienie schedulera
        subprocess.Popen(["airflow", "scheduler"])
    except Exception as e:
        print(f"Error running Airflow: {e}")

if __name__ == '__main__':
    # Uruchomienie Airflow w osobnym wątku
    airflow_thread = threading.Thread(target=run_airflow)
    airflow_thread.start()

    # Uruchomienie aplikacji Flask
    app.run(host='0.0.0.0', port=5001)
