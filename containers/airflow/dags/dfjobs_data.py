import datetime
import requests

from airflow import DAG, task
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator

from job_boards.api_call import SourceProcessor


source_config = Variable.get('sources', deserialize_json=True)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'email' : ['laszlo@hey.com'],
    'scehdule_interval': '@daily'
}

with DAG(
    dag_id="pull_api_sources", default_args=default_args) as dag:

    @task()
    def fetch_api_sources():
        api_url = "https://datafirstjobs/api/sources"

        headers = {
            'Content-Type': 'application/json',
            'Authorization' : ''
            # Include 'Authorization': 'Bearer YOUR_ACCESS_TOKEN' if needed
        }

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to pull from from dfjobs: {e}")

        sources = response.json()
        return sources


    @task()
    def pull_api_data(source):
        url = source.api_url
        params = source.params
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to pull data from api: {e}")

        desired_roles = ['data', 'analytics', 'analyst']
        
        data = response.json()
        return source, data

    
    @task()
    def transform_data(source, data):
        processor = SourceProcessor(source)
        processor.preprocess_data(data)

        return processor
    


    @task()
    def post_to_api(processor):
        url = 'https://datafirstjobs.com/api/create-jobs'
        headers = {
            'Content-Type': 'application/json',
            # Include 'Authorization': 'Bearer YOUR_ACCESS_TOKEN' if needed
        }
        body = processor.job_data_list
        try:
            response = requests.post(url, json=body, headers=headers, timeout=10)  
            response.raise_for_status() 
        except requests.RequestException as e:
            raise Exception(f"Failed to post data to API: {e}")

        return True
    
    sources = fetch_api_sources()

    for source in sources:
        source, data = pull_api_data(sources)
        processor = transform_data(source, data)
        post_to_api(processor)
        
        

    dag_instance = dag()