INSERT INTO attributed_successful_applications
WITH (
    SELECT
    , ap.job_application_id
    , u.email as username
    , ev.id as event_id
    , ap.user_agent
    , ap.ip_address
    , ap.job_uuid
    , ap.job_title
    , ap.company_name
    , ap.event_time as applied_at
    , ev.event_time as click_time
    ROW_NUMBER() OVER (
        PARTITION BY u.email
        , ev.element
        ORDER BY 
            ev.event_time
    ) as rn

    FROM applications ap
    JOIN users FOR SYSTEM_TIME AS OF ap.processing_time AS u on ap.user_id = u.user_id
    LEFT JOIN events as ev on ap.user_id = ev.user_id
    AND ap.job_uuid = ev.job_uuid
    AND ap.event_time BETWEEN ev.event_time
    AND ev.event_time + INTERVAL '1' HOUR
) as CTE


SELECT job_application_id
    , username
    , event_id,
    , user_agent
    , ip_address
    , job_uuid
    , job_title,
    , company_name,
    , applied_at
    , click_time
FROM 
    CTE
WHERE RN = 1;
    