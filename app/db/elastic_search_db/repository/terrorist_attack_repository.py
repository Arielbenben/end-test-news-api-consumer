from app.db.elastic_search_db.database import current_terrorist_attacks_index, elastic_client



def insert_attack_to_elastic_db(terrorist_attack: dict):
    try:
        response = elastic_client.index(index=current_terrorist_attacks_index, body=terrorist_attack)
        if response['result'] == 'created':
            print('inserted to elastic successfully')
            return {'Success': f"Review inserted with ID: {response['_id']}"}
        else:
            return {'Error': f"Failed to insert review: {response}"}
    except Exception as e:
        return {'Error': f'Exception occurred: {str(e)}'}