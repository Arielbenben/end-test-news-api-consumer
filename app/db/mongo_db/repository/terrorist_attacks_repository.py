from app.db.mongo_db.database import terrorist_attacks_collection



def insert_attack_to_mongo_db(attack: dict):
    terrorist_attacks_collection.insert_one(attack)
    print('inserted to mongo successfully')


