from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# import models
from .go_model import GoInteraction, GoInfo, EcoliProtGO, ScerProtGO
from .Ecoli_interaction_score_model import EcoliInteractionScore
from .Scer_interaction_score_model import ScerInteractionScore
from .Ecoli_validation_model import EcoliValidation
from .Scer_validation_model import ScerValidation
from .species_protein_model import SpeciesProtein
from .Ecoli_protein_model import EcoliPS, EcoliSS, EcoliTS
from .Scer_protein_model import ScerPS, ScerSS, ScerTS