from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from dotenv import load_dotenv
from models import db
import os

from services.go_query import go_term_details

from resources.go_resource import GOQuery
from resources.interaction_resource import InteractionResource
from resources.basic_info_resource import BasicInfoResource
from resources.download_resource import FileDownloadAPI

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db.init_app(app)
with app.app_context():
    db.create_all()

# initialize API
api = Api(app)

# register resources to API
api.add_resource(GOQuery, '/go-search/<string:go_id>')
api.add_resource(InteractionResource, '/interaction-search')
api.add_resource(BasicInfoResource, '/basic-info-search')
api.add_resource(FileDownloadAPI, '/download')

if __name__ == '__main__':
    app.run(debug=True)