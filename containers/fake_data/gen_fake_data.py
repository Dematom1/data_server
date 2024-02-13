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

def gen_click_event(user_id: str, job_uuid: str = None) -> dict:
        user_agent: str = fake.user_agent()
        event_time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        event_type: str = fake.job_event_type()
        template_name: str  = fake.job_template_name()
        element: str = fake.job_element()
        job_uuid: str = job_uuid or str(uuid4())
        ip_address: str = fake.ipv4()
        
        click_event = {
            'user_agent': user_agent,
            'event_time': event_time,
            'job_uuid': job_uuid,
            'event_type': event_type,
            'template_name': template_name,
            'tag': element,
            'job_uuid': job_uuid,
            'user_id': user_id,
            'ip_address': ip_address
        }
        return click_event

def gen_successful_job_application(event: dict) -> dict:
    event_time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    job_title: str = fake.job_description()
    company_name: str = fake.company()
    application_id: str = str(uuid4())
    
    attr_job_applications = {
        'application_id': application_id,
        'event_time': event_time,
        'user_id': event['user_id'],
        'user_agent': event['user_agent'],
        'ip_address': event['ip_address'],
        'job_uuid': event['job_uuid'],
        'job_title': job_title,
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
        print(event)
        push_to_kafka(event, 'clicks')

        # 60% chance to proceed to application after click
        if random.randint(0, 100) < 60:
            # Create a click event for click on apply now
            apply_event = gen_click_event(user_id, event['job_uuid'])
            print(apply_event)
            push_to_kafka(apply_event, 'clicks')

            # 40% chance that the user completes the application on the company's job page
            if random.randint(0, 100) < 40:
                # Create corresponding successful job application
                success_event = gen_successful_job_application(apply_event)
                print(success_event)
                push_to_kafka(success_event, 'applications')


if __name__ == "__main__":
    gen_fake_user(500)
    gen_user_click_data(2000)