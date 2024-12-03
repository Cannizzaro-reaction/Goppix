from flask import request
from flask_restful import Resource
from services.protein_basic_query import query_structure_go, ProteinNotFoundException, TableNotFoundException, query_by_sequence

class BasicInfoResource(Resource):
    def get(self):
        # Get query parameters
        search_type = request.args.get("search_type") # `protein_id` or `sequence`
        protein = request.args.get('protein')
        species = request.args.get('species')

        if not protein or not species:  # missing parameter
            return {"error": "Please provide both 'protein' and 'species' parameters."}, 400
        
        try:
            if search_type == "protein_id":
                response = query_structure_go(protein, species)
            elif search_type == "sequence":
                response = query_by_sequence(protein, species)
            else: # wrong `search_type` parameters
                return {"error": "Invalid 'search_type'. Must be 'protein_id' or 'sequence'."}, 400

            return {
                "protein_id": response["id"],
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
