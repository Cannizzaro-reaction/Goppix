from . import db

class ScerValidation(db.Model):
    __tablename__ = 'Scer_validation'

    protein_a = db.Column(db.String(10), db.ForeignKey('species_protein.protein_id'), primary_key=True)
    protein_b = db.Column(db.String(10), db.ForeignKey('species_protein.protein_id'), primary_key=True)
    experiment_approach = db.Column(db.String(30), primary_key=True)
    pubmed_id = db.Column(db.String(20), primary_key=True)

    def to_dict(self):
        return {
            "protein_a": self.protein_a,
            "protein_b": self.protein_b,
            "experiment_approach": self.experiment_approach,
            "pubmed_id": self.pubmed_id,
        }
    