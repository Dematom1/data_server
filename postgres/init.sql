SET TIME ZONE 'America/Edmonton'
CREATE SCHEMA job_board;


SET 
    search_path TO job_board;

CREATE TABLE users (
    id int SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE events (
    id int SERIAL PRIMARY KEY,
    user_agent VARCHAR(255) NOT NULL,
    event_time TIMESTAMP WITH TIME ZONE NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    template_name VARCHAR(255) NOT NULL,
    element VARCHAR(255) NOT NULL,
    user_id VARCHAR NOT NULL,
    ip_address VARCHAR(255) NOT NULL,
);


CREATE TABLE successful_applications (
    job_application_id int SERIAL PRIMARY KEY,
    event_time TIMESTAMP WITH TIME ZONE NOT NULL,
    user_id VARCHAR NOT NULL,
    job_uuid VARCHAR(255),
    job_desc VARCHAR(255),
    company_name VARCHAR(255)
);

    
    
    