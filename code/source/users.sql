CREATE TABLE users {
    id INT,
    first_name STRING,
    last_name STRING,
    email STRING
} with (
    'connector' = '{{connector}}',
    'boostrap_servers' = '{{bootstap_servers}}',
    'topic' = '{{topic}}',
    'format' = '{{format}}',
)

