from flask import request
from flask_restful import Resource
from services.protein_basic_query import query_structure_go, ProteinNotFoundException, TableNotFoundException

class BasicInfoResource(Resource):
    def get(self):
        # Get query parameters
        protein_id = request.args.get('protein')
        species = request.args.get('species')

        if not protein_id or not species:  # missing parameter
            return {"error": "Please provide both 'protein' and 'species' parameters."}, 400

        try:
            response = query_structure_go(protein_id, species)

            return {
                "protein_id": protein_id,
                "species": species,
                "primary_structure": response["primary"],
                "secondary_structure": response["secondary"],
                "tertiary_structure": response["tertiary"],
                "go_terms": response["go"]
            }, 200

        except ProteinNotFoundException as e:
            return {"error": str(e)}, 404  # protein not found

        except TableNotFoundException as e:
            return {"error": str(e)}, 400  # invalid species

        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500
