FROM python:latest

RUN pip install \
    psycopg[binary] \
    Faker==22.5.0 \ 
    confluent-kafka

COPY . /opt/fake_data/

WORKDIR /opt/fake_data

RUN pip install --no-cache-dir -r requirements.txt

CMD ["tail" "-F" "anything"]