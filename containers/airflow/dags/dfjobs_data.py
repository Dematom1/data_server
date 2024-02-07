import sys
import requests
from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable

sys.path.append('/opt/bitnami/airflow/includes')
from job_boards.api_call import SourceProcessor


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
        api_url = "https://www.datafirstjobs.com/api/sources/"

        headers = {
            'Content-Type': 'application/json',
            'Authorization' : 'Token c5b547b5718c4bd41f50c95d90c03b8bb926a6b6'
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
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to pull data from api: {e}")
        
        data = response.json()
        return data

    
    @task()
    def transform_data(data):
        processor = SourceProcessor(data)
        processor.preprocess_data(data['parsing_instructions'])

        return processor
    


    @task()
    def post_to_api(processor):
        url = 'https://datafirstjobs.com/api/create-jobs'
        headers = {
            'Content-Type': 'application/json',
            'Authorization' : 'Token c5b547b5718c4bd41f50c95d90c03b8bb926a6b6'
        }
        body = processor.job_data_list
        try:
            response = requests.post(url, json=body, headers=headers, timeout=10)  
            response.raise_for_status() 
        except requests.RequestException as e:
            raise Exception(f"Failed to post data to API: {e}")

        return True
    
    @task()
    def process_sources(sources):
        for source in sources:
            data = pull_api_data(source)
            processor = transform_data(data)
            # post_to_api(processor)
        
    sources = fetch_api_sources()
    process_sources(sources)
        