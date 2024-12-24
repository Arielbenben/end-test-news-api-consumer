import json
import os
from dotenv import load_dotenv
from kafka import KafkaConsumer


load_dotenv(verbose=True)


bootstrap_servers = os.environ["BOOTSTRAP_SERVERS"]
news_api_topic = os.environ["NEWS_API_TOPIC"]


def consume(topic_name:str, func = lambda x: x):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
        value_deserializer= lambda value: json.loads(value.decode('utf-8')),
        auto_offset_reset='latest'
    )

    for message in consumer:
        func(message.value)
        print(f"Recieved: {message.key}: {message.value}")


