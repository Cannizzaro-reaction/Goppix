from . import db

class ScerPS(db.Model):
    __tablename__ = 'Scer_primary_structure'
    protein_id = db.Column(db.String(10), db.ForeignKey('species_protein.protein_id'), primary_key=True)
    seq = db.Column(db.String(5000), nullable=True)

    def to_dict(self):
        return {
            "protein_id": self.protein,
            "seq": self.seq,
        }

class ScerSS(db.Model):
    __tablename__ = 'Scer_secondary_structure'
    protein_id = db.Column(db.String(10), db.ForeignKey('species_protein.protein_id'), primary_key=True)
    ss = db.Column(db.String(2700), nullable=True)

    def to_dict(self):
        return {
            "protein_id": self.protein,
            "secondary_structure": self.ss,
        }

class ScerTS(db.Model):
    __tablename__ = 'Scer_tertiary_structure'
    protein_id = db.Column(db.String(10), db.ForeignKey('species_protein.protein_id'), primary_key=True)
    ts = db.Column(db.String(75), nullable=True)

    def to_dict(self):
        return {
            "protein_id": self.protein,
            "tertiary_structure": self.ts,
        }