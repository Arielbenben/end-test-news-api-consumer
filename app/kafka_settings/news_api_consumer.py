import os
from dotenv import load_dotenv
from app.kafka_settings.consumer import consume
from app.service.mongo_service import prepare_article_and_insert_to_db


load_dotenv(verbose=True)


news_api_topic = os.getenv('NEWS_API_TOPIC')


def consume_news():
    consume(news_api_topic, prepare_article_and_insert_to_db)