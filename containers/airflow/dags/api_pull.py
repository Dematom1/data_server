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

jobdata_schema = {
  "role": "title",
  "slug": "ext_id",
  "company": {
    "name": "company['name']",
    "url": "company['website_url']",
    "location": "location"
  },
  "location": {
    "city": "cities[0]['asciiname']",
    "country": "countries[0]['code']",
    "region": "regions[0]['name']"
  },
  "content":"description",
  "is_remote": "has_remote",
  "apply_url": "application_url",
  "external_id": "id"
}

@dag(default_args=default_args, schedule_interval="@daily", catchup=False)
def job_data_api_call():

    @task()
    def fetch_metadata():
        # api_url = "https://www.datafirstjobs.com/api/regions/"
        api_url = "http://host.docker.internal:8000/api/regions/"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token c5b547b5718c4bd41f50c95d90c03b8bb926a6b6'
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        metadata = response.json()
        
        return metadata
    
        

    @task
    def pull_api_data(job_tags):

        file_path = '/opt/bitnami/airflow/includes/job_boards/fake_data.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        print(data)
        print(type(data))

        # # return tags
        # api_url = "https://jobdataapi.com/api/jobs"
        # # api_url = "http://host.docker.internal:8000/api/sources/"

        # title_param = "|".join(job_tags)
        # params = {
        #     "country_code": "US|CA",
        #     "type_id":"1|4|6",
        #     "title": title_param,
        #     # 'page_size': '2000'
        # }

        # # headers = {
        # #     'Authorization': 'Api-Key API_KEY'
        # # }

        # response = requests.get(api_url, params=params)
        # response.raise_for_status()
        # jobs = response.json()
        
    
        return data

    
    @task
    def transform_data(jobs, metadata):
        job_tags = metadata
        tags = [tag['name'] for tag in job_tags['tags'] if tag['category'] == 1]
        content_tags = [tag['name'] for tag in job_tags['tags'] if tag['category'] in (2,5,6)]
        data = jobs['results']
        processor = SourceProcessor(data, metadata, jobdata_schema, content_tags)
        processor.preprocess_data()
    
        
        return processor.job_data_list
    


    @task
    def post_to_api(transformed_data):

        flattened_data = [item for sublist in transformed_data for item in sublist]

        url = 'http://host.docker.internal:8000/api/add-jobs/'
        # url = 'https://datafirstjobs.com/api/add-jobs/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization' : 'Token c5b547b5718c4bd41f50c95d90c03b8bb926a6b6'
        }

        try:
            response = requests.post(url, json=flattened_data, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Failed to post batch data to API: {e}")

        return response.json()

    metadata = fetch_metadata()
    jobs = pull_api_data(job_tags=metadata)
    transformed_data = transform_data(jobs, metadata)
    # post_to_db = post_to_api(transformed_data)

dynamic_job_api_calls_dag = job_data_api_call()
        