from . import db
from sqlalchemy.schema import UniqueConstraint

class GoInteraction(db.Model):
    __tablename__ = 'go_interaction'
    index = db.Column(db.Integer, primary_key=True)
    go_id = db.Column(db.String(15), db.ForeignKey('go_basic.id'), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    target_go_id = db.Column(db.String(15), db.ForeignKey('go_basic.id'), nullable=False)

    def to_dict(self):
        return {
            "index": self.index,
            "go_id": self.go_id,
            "relationship": self.relationship,
            "target_go_id": self.target_go_id,
        }
    
    # add unique constraint
    __table_args__ = (
        UniqueConstraint('go_id', 'relationship', 'target_go_id', name='uix_go_relationship_target'),
    )

class GoBasic(db.Model):
    __tablename__ = 'go_basic'
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
        }

class GoDetail(db.Model):
    __tablename__ = 'go_detail'
    id = db.Column(db.String(15), primary_key=True)
    description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
        }

class EcoliProtGO(db.Model):
    __tablename__ = 'Ecoli_protein_go'
    protein_id = db.Column(db.String(10), db.ForeignKey('species_protein.protein_id'), primary_key=True)
    go = db.Column(db.String(15), db.ForeignKey('go_basic.id'), primary_key=True)

    def to_dict(self):
        return {
            "protein_id": self.protein_id,
            "go": self.go
        }
    
class ScerProtGO(db.Model):
    __tablename__ = 'Scer_protein_go'
    protein_id = db.Column(db.String(10), db.ForeignKey('species_protein.protein_id'), primary_key=True)
    go = db.Column(db.String(15), db.ForeignKey('go_basic.id'), primary_key=True)

    def to_dict(self):
        return {
            "protein_id": self.protein_id,
            "go": self.go
        }