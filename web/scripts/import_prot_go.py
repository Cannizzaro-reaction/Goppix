import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db, EcoliProtGO, ScerProtGO
from app import app

def import_prot_info(filepath, model):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)

        # Validate required columns
        required_columns = {"protein_id", "go_term"}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"CSV file must contain the following columns: {required_columns}")

        with app.app_context():
            rows_to_insert = []
            for row in reader:
                protein_id = row["protein_id"].strip()
                go = row["go_term"].strip()

                rows_to_insert.append(model(protein_id=protein_id, go=go))

            try:
                db.session.bulk_save_objects(rows_to_insert)
                db.session.commit()
                print("CSV data imported successfully.")
            except Exception as e:
                db.session.rollback()
                print(f"Error occurred during import: {e}")

import_prot_info(r'../data/Ecoli_protein_go.csv', EcoliProtGO)
import_prot_info(r'../data/Scer_protein_go.csv', ScerProtGO)