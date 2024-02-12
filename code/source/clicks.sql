CREATE TABLE clicks (
    id INT,
    user_agent STRING,
    event_time TIMESTAMP(3),
    event_type STRING,
    template_name STRING,
    tag STRING,
    job_uuid STRING,
    user_id INT,
    ip_address STRING,
    processing_time AS PROCTIME(),
    WATERMARK FOR event_time AS event_time - INTERVAL '15' SECOND
) with (
    'connector' = '{{ connector }}',
    'properties.bootstrap.servers' = '{{bootstrap_servers}}',
    'properties.group.id' = '{{ consumer_group_id }}',
    'scan.startup.mode' = '{{ scan_stratup_mode }}',
    'topic' = '{{topic}}',
    'format' = '{{format}}'
);