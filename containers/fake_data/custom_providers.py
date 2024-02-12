from collections import OrderedDict

from faker import Faker
from faker.providers import BaseProvider

fake = Faker()

class JobEventProvider(BaseProvider):
    __provider__ = "job_event_type"
    __provider__ = "job_template_name"
    __provider__ = "job_element"
    __provider__ = "job_description"
    event_types = ["click", "reload"]
    template_name = ['/','job_search','job_detail']
    elements = ['div.jobCard','div.tag', 'a.footer_link']
    job_desc = ['Data Analyst', 'Data Engineer', 'Data Architect', 'Analytics Engineer']
    
    def job_event_type(self) -> str:
        return self.random_element(
            elements=OrderedDict([
                (self.event_types[0], 0.80),
                (self.event_types[1], 0.20),
            ])
        )
    
    def job_template_name(self) -> str:
        return self.random_element(
            elements=OrderedDict([
                (self.template_name[0], 0.55),
                (self.template_name[1], 0.3),
                (self.template_name[2], 0.15)
            ]), 
        )
    
    def job_element(self) -> str:
        return self.random_element(
            elements=OrderedDict([
                (self.elements[0], 0.55),
                (self.elements[1], 0.40),
                (self.elements[2], 0.05),
            ])
        )
    
    def job_description(self)-> str:
        return self.random_element(
            elements=OrderedDict([
                (self.job_desc[0], 0.50),
                (self.job_desc[1], 0.25),
                (self.job_desc[2], 0.05),
                (self.job_desc[3], 0.10),
            ])
        )


fake.add_provider(JobEventProvider)


