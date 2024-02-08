import sys
import json
import requests
from datetime import datetime

from airflow import DAG
from airflow.decorators import task, dag
from airflow.models import Variable

sys.path.append('/opt/bitnami/airflow/includes')
from job_boards.api_call import SourceProcessor


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'email' : ['laszlo@hey.com'],
}

@dag(default_args=default_args, schedule_interval="@daily", catchup=False)
def dynamic_job_api_calls():

    @task()
    def fetch_api_sources():
        api_url = "https://www.datafirstjobs.com/api/sources/"
        # api_url = "http://host.docker.internal:8000/api/sources/"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token c5b547b5718c4bd41f50c95d90c03b8bb926a6b6'
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        sources = response.json()
        
        return sources
    
    @task()
    def fetch_metadata():
        api_url = "https://www.datafirstjobs.com/api/regions/"
        # api_url = "http://host.docker.internal:8000/api/regions/"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token c5b547b5718c4bd41f50c95d90c03b8bb926a6b6'
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        metadata = response.json()
        print(f"Returning metadata: {metadata}, type({metadata}")
        
        return metadata
    
        

    @task(multiple_outputs=True)
    def pull_api_data(source):
        source_uuid = source['uuid']
        url = source['api_url']
        # For Dev purposes
        # url = "http://host.docker.internal:8000/api/"

        params = source.get('params', {})
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return {"data": data, "source": source}


    
    @task
    def transform_data(context, metadata):
        data = context['data']['results']
        source = context['source']
        parsing_instructions = context['source']['parsing_instructions']
        processor = SourceProcessor(data, metadata, source, parsing_instructions)
        processor.preprocess_data()
    
        lst = processor.job_data_list
        print(f"type:{type(processor.job_data_list)}")
        print(f"type:{type(lst)}")
        
        return processor.job_data_list
    


    @task
    def post_to_api(transformed_data):

        flattened_data = [item for sublist in transformed_data for item in sublist]

        # url = 'http://host.docker.internal:8000/api/add-jobs/'
        url = 'https://datafirstjobs.com/api/add-jobs/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization' : 'Token c5b547b5718c4bd41f50c95d90c03b8bb926a6b6'
        }

        print(f"type:{transformed_data}")

        try:
            response = requests.post(url, json=flattened_data, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to post batch data to API: {e}")

        return response.json()

    sources = fetch_api_sources()
    metadata = fetch_metadata()
    processed_data = pull_api_data.expand(source=sources)
    transformed_data = transform_data.partial(metadata=metadata).expand(context=processed_data)
    post_to_db = post_to_api(transformed_data)

dynamic_job_api_calls_dag = dynamic_job_api_calls()
        