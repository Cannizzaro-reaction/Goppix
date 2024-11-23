from flask import request
from flask_restful import Resource
from services.interaction_query import query_interactions, ProteinNotFoundException, TableNotFoundException
from services.interaction_query import generate_interaction_graph
from flask import Response

class InteractionResource(Resource):
    def get(self):
        # get parameters
        protein = request.args.get('protein')
        species = request.args.get('species')
        min_score = request.args.get('min_score', default=0, type=float)

        if not protein or not species: # missing parameter
            return {"error": "Please provide both 'protein' and 'species' parameters."}, 400

        try:
            response = query_interactions(protein, species, min_score)
            interaction_data = response.get("interaction_data")

            if not interaction_data:
                return response, 200

            # Generate interaction graph
            graph_svg = generate_interaction_graph(interaction_data)

            combined_response = {
                "protein": response["protein"],
                "species": response["species"],
                "interactions": response["interactions"],
                "graph_svg": graph_svg
            }

            return combined_response
            # return Response(graph_svg, mimetype="image/svg+xml")

        except ProteinNotFoundException as e:
            return {"error": str(e)}, 404 # wrong protein id

        except TableNotFoundException as e:
            return {"error": str(e)}, 400 # wrong speices name

        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500 # other error
