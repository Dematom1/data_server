CREATE TABLE successful_job_applications (
    application_id INT,
    event_time TIMESTAMP WITH TIME ZONE,
    user_id STRING,
    user_agent,
    ip_address,
    job_uuid STRING,
    job_title STRING,
    company_name STRING,
    processing_time as PROCTIME(),
    WATERMARK FOR event_time AS event_time - INTERVAL '15' SECOND
) with (
    'connector' = '{{connector}}',
    'boostrap_servers' = '{{bootstrap_servers}}',
    'topic' = '{{topic}}',
    'format' = '{{format}}'
)