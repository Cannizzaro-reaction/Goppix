import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db, SpeciesProtein
from app import app

def import_species_protein(filepath):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        with app.app_context():
            for row in reader:
                existing_record = SpeciesProtein.query.filter_by(protein_id=row['protein_id']).first()
                if existing_record:
                    print(f"Skipping duplicate entry: {row['protein_id']} ({row['species']})")
                    continue

                species_protein = SpeciesProtein(
                    protein_id=row['protein_id'],
                    species=row['species']
                )
                db.session.add(species_protein)
            db.session.commit()
            print("Species-Protein data imported successfully!")

def run():
    csv_file_path = r'../data/species_protein.csv'
    import_species_protein(csv_file_path)
