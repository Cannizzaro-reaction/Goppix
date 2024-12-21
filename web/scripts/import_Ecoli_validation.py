import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db, EcoliValidation
from app import app

def import_ecoli_validation(filepath):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        with app.app_context():
            for row in reader:
                existing_record = EcoliValidation.query.filter_by(
                    protein_a=row['protein_a'],
                    protein_b=row['protein_b'],
                    experiment_approach=row['experiment_approach'],
                    pubmed_id=row['pubmed_id']
                ).first()
                if existing_record:
                    print(f"Skipping duplicate entry: {row['protein_a']}, {row['protein_b']}, {row['experiment_approach']}, {row['pubmed_id']}")
                    continue

                validation_record = EcoliValidation(
                    protein_a=row['protein_a'],
                    protein_b=row['protein_b'],
                    experiment_approach=row['experiment_approach'],
                    pubmed_id=row['pubmed_id']
                )
                db.session.add(validation_record)
            db.session.commit()
            print("EcoliValidation data imported successfully!")

def run():
    import_ecoli_validation(r'../data/Ecoli_validation.csv')
