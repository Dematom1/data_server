CREATE TABLE attributed_successful_applications (
    application_id STRING,
    username STRING,
    event_id INT,
    user_agent STRING,
    ip_address STRING,
    job_uuid STRING,
    job_title STRING,
    company_name STRING,
    applied_at TIMESTAMP(3),
    click_time TIMESTAMP,
    PRIMARY KEY(application_id) NOT ENFORCED
) with (
    'connector' = '{{connector}}',
    'url' = '{{url}}',
    'table-name' = 'job_board.attributed_successful_applications',
    'username'= '{{username}}',
    'password'= '{{password}}',
    'driver'= '{{driver}}'
)