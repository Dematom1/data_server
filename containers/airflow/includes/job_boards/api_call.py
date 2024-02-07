from jsonpath_ng import parse
import re

from airflow.models import Variable




class SourceProcessor:
    def __init__(self, data, **kwargs):
        self.data = data | []
        self.job_data_list = []
        self.tags = Variable.get('tags')
        self.tag_values = Variable.get('tag_values',[])
        self.regions = Variable.get('regions', [])
        self.countries = Variable.get('countries', [])
        self.states = Variable.get('states', [])
        # Other attributes...
    
    def extract_data(self, item, path):
        jsonpath_expr = parse(path)
        return [match.value for match in jsonpath_expr.find(item)]
    
    def preprocess_data(self, data):
        for item in data:
            self.job_data_list.append(self.process_single_item(item))

    def process_single_item(self, item):
        job = {}
        for key, value in self.parsing_instructions.items():
            job[key] = self.extract_and_assign(value, item, key)
        self.extract_tags(job)
        return job
    
    def extract_and_assign(self, value, item, key):
        if isinstance(value, str):
            result = self.extract_data(item, value)
            # Check if result is a list and has more than one item
            if isinstance(result, list) and len(result) > 1:
                return result
            else:
                return result[0] if result else None
        elif isinstance(value, dict):
            nested_result = {}
            for nested_key, nested_value in value.items():
                nested_data = self.extract_data(item, nested_value)
                # Check if nested_data is a list and has more than one item
                if isinstance(nested_data, list) and len(nested_data) > 1:
                    nested_result[nested_key] = nested_data
                else:
                    nested_result[nested_key] = nested_data[0] if nested_data else None
            return nested_result

    def extract_tags(self, job):
        content = job.get('content', '').lower()
        content = re.sub(r'\W+', ' ', content)  # Replace non-word chars with space
        job['additional_tags'] = self.find_matching_tags(content)

    
    def find_matching_tags(self, job_content):
        matched_tags = set()
        job_content_lower = job_content.lower()  # Convert job content to lowercase
        for tag in self.tag_values:
            if re.search(r'\b{}\b'.format(re.escape(tag)), job_content_lower):
                matched_tags.add(tag)
        return list(matched_tags)


    # @transaction.atomic
    # def save_to_database(self):
    #     jobs = []
    #     existing_ids = set(Job.objects.filter(
    #                 source=self.source,
    #                 external_id__in=[data['external_id'] for data in self.job_data_list]
    #                 ).values_list('external_id', flat=True))
    #     for job_data in self.job_data_list:
    #         if job_data['external_id'] not in existing_ids:
    #             job = Job(
    #                 role = job_data['role'],
    #                 content = job_data['content'],
    #                 source = self.source,
    #                 restriction = job_data.get('restriction', None),
    #                 slug = job_data['slug'],
    #                 type='api',
    #                 apply_url = str(job_data['apply_url']),
    #                 city = job_data.get('location', None).get('city', None),
    #             )
    #             jobs.append(job)
    #     created_jobs = Job.objects.bulk_create(jobs)
    #     scraped_jobs = []

    #     for job, job_data in zip(created_jobs, self.job_data_list):

    #         scraped_job = ScrapedJob(
    #             job=job,
    #             source=self.source,
    #             company_name=job_data.get('company',{}).get('name', None),
    #             external_id=job_data.get('external_id')
    #         )
    #         scraped_jobs.append(scraped_job)
            
    #         job_tags_values = [tag_name.lower() for tag_name in job_data.get('job_tag', {}).get('name', [])]
    #         job_tags_values += [job_tag.lower() for job_tag in job_data.get('additional_tags')]
    #         job_tags_values = list(set(job_tags_values))

    #         query = Q(name__iexact=job_tags_values[0])
    #         for value in job_tags_values[1:]:
    #             query |= Q(name__iexact=value)

    #         tag_instances = self.tags.filter(query)
            
    #         job_region_name = job_data.get('location', {}).get('region', None)
    #         job_country_name = job_data.get('location', {}).get('country', None)
    #         job_state_name = job_data.get('location', {}).get('state', None)

    #         region_instance = self.regions.get(name=job_region_name)
    #         if job_state_name in US_STATES:
    #             state_instance = self.states.get(state=job_state_name)
    #         state_instance = self.states.get(ca_province=job_state_name)
    #         country_instance = self.countries.get(name=job_country_name)

    #         job.region = region_instance
    #         job.country = country_instance
    #         job.state = state_instance
    #         job.activate_date = datetime.datetime.now()

    #         non_existing_tags = list(set(job_tags_values) - set(tag_instances))
    #         scraped_job.additional_tags = non_existing_tags
    #         job.job_tag.set(tag_instances)

    #     Job.objects.bulk_update(created_jobs, ['additional_tags', 'activate_date','region','state','country'])
    #     ScrapedJob.objects.bulk_create(scraped_jobs)
