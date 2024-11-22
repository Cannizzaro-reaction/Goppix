from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# import models
from .go_info_model import GoInfo
from .go_interaction_model import GoInteraction