SET TIME ZONE 'America/Edmonton';
CREATE SCHEMA job_board;


SET search_path TO job_board;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    user_agent VARCHAR(255) NOT NULL,
    event_time TIMESTAMP WITH TIME ZONE NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    template_name VARCHAR(255) NOT NULL,
    tag VARCHAR(255) NOT NULL,
    user_id VARCHAR NOT NULL,
    ip_address VARCHAR(255) NOT NULL
);


CREATE TABLE attributed_successful_applications (
    application_id VARCHAR PRIMARY KEY,
    username VARCHAR NOT NULL,
    event_id VARCHAR,
    user_agent VARCHAR,
    ip_address VARCHAR,
    job_uuid VARCHAR(255),
    job_title VARCHAR(255),
    company_name VARCHAR(255),
    applied_at TIMESTAMP WITH TIME ZONE,
    click_time TIMESTAMP WITH TIME ZONE
);

    
    
    