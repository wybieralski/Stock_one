import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 9),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}
def fetch_and_save_btc_data(**kwargs):
    print("NO_Proxy zastosowane")
    # Ustaw zmienną środowiskową, aby pominąć proxy
    os.environ['NO_PROXY'] = '*'
    print("DAG STARTED")
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': 'BTCUSDT',
        'interval': '1m',
        'limit': 500
    }
    print("Parametry ustawione")

    response = requests.get(url, params=params)
    print("response = requests.get(url, params=params) | WYKONANE")
    response.raise_for_status()
    print("response.raise_for_status() | WYKONANE")
    data = response.json()
    print("data = response.json() | WYKONANE")
    print(data)
    print("    print(data) | WYKONANE")

    timestamps = [int(entry[0]) for entry in data]
    prices = [float(entry[4]) for entry in data]
    df = pd.DataFrame({'timestamp': timestamps, 'price': prices})
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    print(f"Data fetched")
    # Zapisz dane do pliku CSV
    df.to_csv('/Users/lukaszw/PycharmProjects/Stock_one/Stock_one/data/btc_prices.csv')
    print(f"Data saved to /Users/lukaszw/PycharmProjects/Stock_one/Stock_one/data/btc_prices.csv")


dag = DAG(
    'update_btc_data',
    default_args=default_args,
    description='DAG do aktualizacji danych BTC co minutę',
    schedule_interval='* * * * *',  # Co minutę
    catchup=False,
)

update_task = PythonOperator(
    task_id='fetch_and_save_btc_data',
    python_callable=fetch_and_save_btc_data,
    dag=dag,
)
