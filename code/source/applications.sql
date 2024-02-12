CREATE TABLE applications (
    application_id INT,
    event_time TIMESTAMP(3),
    user_id INT,
    user_agent STRING,
    ip_address STRING,
    job_uuid STRING,
    job_title STRING,
    company_name STRING,
    processing_time as PROCTIME(),
    WATERMARK FOR event_time AS event_time - INTERVAL '15' SECOND
) with (
    'connector' = '{{connector}}',
    'properties.bootstrap.servers' = '{{bootstrap_servers}}',
    'properties.group.id' = '{{ consumer_group_id }}',
    'scan.startup.mode' = '{{ scan_stratup_mode }}',
    'topic' = '{{topic}}',
    'format' = '{{format}}'
)