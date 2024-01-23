CREATE TABLE attributed_successful_applications (
    job_application_id INT,
    event_time TIMESTAMP WITH TIME ZONE,
    user_id STRING,
    job_uuid STRING,
    job_desc STRING,
    company_name STRING,
    processing_time as PROCTIME(),
    WATERMARK FOR event_time AS event_time - INTERVAL '15' SECOND
) with (
    'connector' = '{{connector}}',
    'boostrap_servers' = '{{bootstrap_servers}}',
    'topic' = '{{topic}}',
    'format' = '{{format}}'
)