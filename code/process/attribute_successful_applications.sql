INSERT INTO 
    attributed_successful_applications
SELECT application_id
    , username
    , event_id
    , user_agent
    , ip_address
    , job_uuid
    , job_title
    , company_name
    , applied_at
    , click_time
FROM 
    (
        SELECT ap.application_id
        , u.email as username
        , cl.id as event_id
        , ap.user_agent
        , ap.ip_address
        , ap.job_uuid
        , ap.job_title
        , ap.company_name
        , ap.event_time as applied_at
        , cl.event_time as click_time
        , ROW_NUMBER() OVER (
            PARTITION BY u.email
            , cl.tag
            ORDER BY 
                cl.event_time
        ) as rn
        FROM 
            applications ap
            JOIN users FOR SYSTEM_TIME AS OF ap.processing_time AS u on ap.user_id = u.id
            LEFT JOIN clicks as cl on ap.user_id = cl.user_id
            AND ap.job_uuid = cl.job_uuid
            AND ap.event_time BETWEEN cl.event_time
            AND cl.event_time + INTERVAL '1' HOUR
) 
WHERE 
    rn = 1;
