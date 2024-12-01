from . import db

class EcoliPS(db.Model):
    __tablename__ = 'Ecoli_primary_structure'
    protein_id = db.Column(db.String(10), db.ForeignKey('species_protein.protein_id'), primary_key=True)
    seq = db.Column(db.String(2400), nullable=True)

    def to_dict(self):
        return {
            "protein_id": self.protein,
            "seq": self.seq,
        }

class EcoliSS(db.Model):
    __tablename__ = 'Ecoli_secondary_structure'
    protein_id = db.Column(db.String(10), db.ForeignKey('species_protein.protein_id'), primary_key=True)
    ss = db.Column(db.String(2400), nullable=True)

    def to_dict(self):
        return {
            "protein_id": self.protein,
            "secondary_structure": self.ss,
        }

class EcoliTS(db.Model):
    __tablename__ = 'Ecoli_tertiary_structure'
    protein_id = db.Column(db.String(10), db.ForeignKey('species_protein.protein_id'), primary_key=True)
    ts = db.Column(db.String(65), nullable=True)

    def to_dict(self):
        return {
            "protein_id": self.protein,
            "tertiary_structure": self.ts,
        }