from . import db

class SpeciesProtein(db.Model):
    __tablename__ = 'species_protein'

    protein_id = db.Column(db.String(10), primary_key=True)
    species = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "protein_id": self.protein_id,
            "species": self.species
        }