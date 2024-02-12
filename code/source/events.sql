CREATE TABLE clicks (
    id INT,
    user_agent STRING,
    event_time TIMESTAMP WITH TIME ZONE,
    event_type STRING,
    template_name STRING,
    element STRING,
    job_ib STRING,
    user_id STRING,
    ip_address STRING,
    processing_time AS PROCTIME(),
    WATERMARK FOR event_time AS event_time - INTERVAL '15' SECOND
) with (
    'connector' = '{{ connector }}',
    'boostrap_servers' = '{{bootstrap_servers}}',
    'topic' = '{{topic}}',
    'format' = '{{format}}'
);