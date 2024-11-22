from flask_restful import Resource
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.go_query import go_term_details, InvalidGOIDException, GOIDNotFoundException, normalize_go

class GOQuery(Resource):
    def get(self, go_id):
        try:
            normalized_go_id = normalize_go(go_id)
            result = go_term_details(normalized_go_id)
            return result, 200
        except InvalidGOIDException as e:
            return {
                'error': 'Invalid GO term format',
                'provided_id': go_id
            }, 400 # wrong format of go term
        
        except GOIDNotFoundException as e:
            return {
                'error': 'GO term not found',
                'go_id': go_id
            }, 404 # inexistent go term