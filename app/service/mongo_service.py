from datetime import datetime
from app.api.groq_api import classify_and_extract_news
from app.api.location_api import get_lot_and_lan_for_location
from app.db.elastic_search_db.repository.terrorist_attack_repository import insert_attack_to_elastic_db
from app.db.mongo_db.repository.terrorist_attacks_repository import insert_attack_to_mongo_db



def validate_location(location: dict):
    if location['city']:
        return location['city']
    elif location['country']:
        return location['country']
    return None


def prepare_terrorist_group():
    return {
        'name': None,
        'perps': None
    }

def prepare_date(article):
    date_time = article.get('dateTime')
    if date_time:
        date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ")
        return {
            'day': date_time.day,
            'month': date_time.month,
            'year': date_time.year,
            'full_date': date_time
        }
    return {'day': None, 'month': None, 'year': None, 'full_date': None}


def prepare_attack(article):
    return {
        'summary': article.get('body'),
        'attack_type': None,
        'target': None,
        'weapon': None,
        'target_type': None,
        'target_sub_type': None
    }

def prepare_location(extract_location, coordinates):
    return {
        'country': extract_location.get('country'),
        'city': extract_location.get('city'),
        'region': extract_location.get('region'),
        'latitude': coordinates.get('lat'),
        'longitude': coordinates.get('lng'),
        'province': None,
        'exact_location': None
    }

def prepare_casualties():
    return {
        'killed': None,
        'wound': None,
        'deadly_grade': None
    }

def prepare_attack_to_dict(article: dict, extract_location: dict, coordinates: dict):
    return {
        'terrorist_group': prepare_terrorist_group(),
        'date': prepare_date(article),
        'attack': prepare_attack(article),
        'location': prepare_location(extract_location, coordinates),
        'casualties': prepare_casualties()
    }


def prepare_article_and_insert_to_db(article: dict):
    extract_location = classify_and_extract_news(article)
    print(extract_location)
    print()
    if not isinstance(extract_location, dict):
        return
    if extract_location['category'] == 'General news':
        return
    correct_location = validate_location(extract_location)
    if not correct_location:
        return
    coordinates = get_lot_and_lan_for_location(correct_location)

    attack_dict = prepare_attack_to_dict(article, extract_location, coordinates)

    insert_attack_to_elastic_db(attack_dict)
    insert_attack_to_mongo_db(attack_dict)

    return















