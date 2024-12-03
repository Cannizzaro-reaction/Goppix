import csv, sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db, GoBasic, GoDetail
from app import app

def import_go_basic(filepath):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        with app.app_context():
            for row in reader:
                # check if `id` has already existed
                existing_record = GoBasic.query.filter_by(id=row['id']).first()
                if existing_record:
                    print(f"Skipping duplicate entry: {row['id']}")
                    continue
                go_info = GoBasic(
                    id=row['id'],
                    name=row['name'],
                    category=row['category']
                )
                db.session.add(go_info)
            db.session.commit()
            print("GoInfo data imported successfully!")

def import_go_detail(filepath):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        with app.app_context():
            for row in reader:
                # check if `id` has already existed
                existing_record = GoDetail.query.filter_by(id=row['id']).first()
                if existing_record:
                    print(f"Skipping duplicate entry: {row['id']}")
                    continue
                go_info = GoDetail(
                    id=row['id'],
                    description=row['description']
                )
                db.session.add(go_info)
            db.session.commit()
            print("GoInfo data imported successfully!")

import_go_basic(r'../data/go_basic.csv')
import_go_detail(r'../data/go_detail.csv')