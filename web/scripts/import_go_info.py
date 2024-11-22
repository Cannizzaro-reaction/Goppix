import csv, sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db, GoInfo
from app import app

def import_go_info(filepath):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        with app.app_context():
            for row in reader:
                # check if `id` has already existed
                existing_record = GoInfo.query.filter_by(id=row['id']).first()
                if existing_record:
                    print(f"Skipping duplicate entry: {row['id']}")
                    continue
                go_info = GoInfo(
                    id=row['id'],
                    name=row['name'],
                    category=row['category'],
                    description=row['description']
                )
                db.session.add(go_info)
            db.session.commit()
            print("GoInfo data imported successfully!")

import_go_info(r'../data/go_info.csv')
