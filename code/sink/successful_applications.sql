CREATE TABLE attributed_successful_applications (
    job_application_id int,
    username STRING,
    event_id STRING,
    ip_address STRING,
    job_uuid STRING,
    job_title STRING,
    company_name STRING,
    applied_at TIMESTAMP WITH TIME ZONE
    click_time TIMESTAMP WITH TIME ZONE
) with (
    'connector' = '{{connector}}',
    'url' = '{{url}}',
    'table-name' : 'job_board.successful_applications',
    'username': '{{username}}',
    'password': '{{password}}',
    'driver': '{{driver}}'
)