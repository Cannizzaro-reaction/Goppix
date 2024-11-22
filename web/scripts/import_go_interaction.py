import csv, sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db, GoInteraction
from app import app

def import_go_interaction(filepath):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        with app.app_context():
            for row in reader:
                try:
                    go_interaction = GoInteraction(
                        go_id=row['go_id'],
                        relationship=row['relationship'],
                        target_go_id=row['target_go_id']
                    )
                    db.session.add(go_interaction)

                # if import more than one time
                except Exception as e:
                    db.session.rollback()
                    print(f"Skipping duplicate entry: {row['go_id']}, {row['relationship']}, {row['target_go_id']}")

            db.session.commit()
            print("GoInteraction data imported successfully!")

import_go_interaction(r'../data/go_interaction.csv')
