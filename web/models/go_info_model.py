from . import db

class GoInfo(db.Model):
    __tablename__ = 'go_info'
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
        }