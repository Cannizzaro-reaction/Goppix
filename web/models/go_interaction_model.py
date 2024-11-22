from . import db
from sqlalchemy.schema import UniqueConstraint

class GoInteraction(db.Model):
    __tablename__ = 'go_interaction'
    index = db.Column(db.Integer, primary_key=True)
    go_id = db.Column(db.String(15), db.ForeignKey('go_info.id'), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    target_go_id = db.Column(db.String(15), db.ForeignKey('go_info.id'), nullable=False)

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
