from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from .api_call import SourceProcessor


class JobProcessingOperator(BaseOperator):
    @apply_defaults
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.source = source

    def execute(self, context):
        # Instantiate the SourceProcessor and perform data extraction and processing
        processor = SourceProcessor(self.source)
        data = processor.preprocess_data()

        return data