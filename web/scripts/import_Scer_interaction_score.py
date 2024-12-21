import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db, ScerInteractionScore
from app import app

def import_interaction_scores(filepath):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        with app.app_context():
            for row in reader:
                existing_record = ScerInteractionScore.query.filter_by(
                    protein_a=row['protein_a'], 
                    protein_b=row['protein_b']
                ).first()
                if existing_record:
                    print(f"Skipping duplicate entry: {row['protein_a']} - {row['protein_b']}")
                    continue

                interaction_score = ScerInteractionScore(
                    protein_a=row['protein_a'],
                    protein_b=row['protein_b'],
                    interaction_score=int(row['interaction_score'])
                )
                db.session.add(interaction_score)

            db.session.commit()
            print("Interaction scores imported successfully!")

def run():
    import_interaction_scores(r'../data/Scer_interaction_score.csv')