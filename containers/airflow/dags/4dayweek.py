from datetime import datetime

from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'email' : ['laszlo@hey.com'],
    'scehdule_interval': '@daily'
}

def fetch_data():
    ''''
    Fetchs data from Data First Jobs
    '''
    pass

def query_external_api_and_transform(**kwargs):
    # Fetch required data (from XComs or intermediate storage)
    # Make request to external API
    # Transform data
    # Return transformed data
    pass

def post_data_to_api(**kwargs):
    # Fetch transformed data (from XComs or intermediate storage)
    # Make POST request to your API
    pass

with DAG(dag_id='4dayweek_api_pull', default_args=default_args, start_date=datetime(2024, 1, 31), schedule="0 0 * *") as dag:
    pass