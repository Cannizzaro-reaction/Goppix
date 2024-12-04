import os
from flask import request, send_from_directory, jsonify
from flask_restful import Resource

BASE_DOWNLOAD_FOLDER = "files"

def map_file(species):
    if species.lower() == 'e.coli':
        return 'Ecoli_interaction_overview.csv'
    elif species.lower() == 's.cerevisiae':
        return 'Scer_interaction_overview.csv'
    else:
        return {"error": "Wrong 'species' parameter"}, 400
    
class FileDownloadAPI(Resource):
    def get(self):
        try:
            species = request.args.get('species')
            filename = map_file(species)

            if not species or not filename:
                return {"error": "Missing 'species' parameter"}, 400

            file_path = os.path.join(BASE_DOWNLOAD_FOLDER, filename)

            if not os.path.isfile(file_path):
                return {"error": "Download file not found"}, 404

            return send_from_directory(BASE_DOWNLOAD_FOLDER, filename, as_attachment=True)
        except Exception as e:
            return {"error": str(e)}, 500