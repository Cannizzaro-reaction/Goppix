from . import db

class ScerInteractionScore(db.Model):
    __tablename__ = 'Scer_interaction_score'
    protein_a = db.Column(db.String(10), db.ForeignKey('species_protein.protein_id'), primary_key=True)
    protein_b = db.Column(db.String(10), db.ForeignKey('species_protein.protein_id'), primary_key=True)
    interaction_score = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "protein_a": self.protein_a,
            "protein_b": self.protein_b,
            "interaction_score": self.interaction_score,
        }