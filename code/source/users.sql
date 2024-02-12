CREATE TABLE users (
    id INT,
    first_name STRING,
    last_name STRING,
    email STRING
) with (
    'connector' = '{{connector}}',
    'url' = '{{url}}',
    'table-name' = '{{table_name}}',
    'username' = '{{username}}',
    'password' = '{{password}}',
    'driver' = '{{driver}}'
)

