import json
import random
from uuid import uuid4
from datetime import datetime

import psycopg
from confluent_kafka import Producer



from custom_providers import fake


def gen_fake_user(n_users:int ) -> None:

    users_data = [
        (fake.first_name(), fake.last_name(), fake.free_email())
        for _ in range(n_users)
    ]
    with psycopg.connect(dbname="postgres", user="postgres", password="postgres", host="postgres") as conn:
        with conn.cursor() as curr:
            insert_query = """INSERT INTO job_board.users (first_name, last_name, email) VALUES (%s, %s, %s)"""
            curr.executemany(insert_query, users_data)
            conn.commit
    curr.close()
    conn.close()

    return 

def gen_click_event(user_id: str, job_uuid:str = None) -> dict:
        user_agent: str = fake.user_agent()
        event_time: datetime = datetime.utcnow().isoformat()
        event_type: str = 'click' if job_uuid else fake.job_event_type()
        template_name: str  = 'job_detail' if job_uuid else fake.job_template_name()
        element: str = 'apply' if job_uuid else fake.job_element()
        job_uuid: str = job_uuid or str(uuid4())
        ip_address: str = fake.ipv4()
        
        click_event = {
            'user_agent': user_agent,
            'event_time': event_time,
            'job_uuid': job_uuid,
            'event_type': event_type,
            'template_name': template_name,
            'element': element,
            'user_id': user_id,
            'ip_address': ip_address
        }
        return click_event

def gen_successful_job_applications(user_id: str, job_uuid:str) -> dict:
    event_type: datetime = datetime.utcnow().isoformat()
    job_uuid = job_uuid or str(uuid4())
    job_desc: str = fake.job_description()
    company_name: str = fake.company()
    
    attr_job_applications = {
        'event_type': event_type,
        'user_id': user_id,
        'job_uuid': job_uuid,
        'job_desc': job_desc,
        'company_name': company_name
    }
    
    return attr_job_applications

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def push_to_kafka(event, topic:str ) -> None:
    producer = Producer({'bootstrap.servers':'kafka:9092'})
    producer.produce(topic, json.dumps(event).encode('utf-8'), callback=delivery_report)
    producer.flush()

def gen_user_click_data(num_records: int) -> None:
    # import pdb; pdb.set_trace()
    for _ in range(num_records):
        user_id = random.randint(1, 500)
        
        # Generate and push a click event
        event = gen_click_event(user_id)
        push_to_kafka(event, 'clicks')

        # 60% chance to proceed to application after click
        if random.randint(0, 100) < 60:
            # Create a click event for click on apply now
            apply_event = gen_click_event(user_id, event['job_uuid'])
            push_to_kafka(apply_event, 'clicks')

            # 40% chance that the user completes the application on the company's job page
            if random.randint(0, 100) < 40:
                # Create corresponding successful job application
                success_event = gen_successful_job_applications(apply_event['user_id'], apply_event['job_uuid'])
                push_to_kafka(success_event, 'applications')


if __name__ == "__main__":
    gen_fake_user(500)
    gen_user_click_data(2000)