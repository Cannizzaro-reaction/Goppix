import csv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db, EcoliPS, EcoliSS, EcoliTS, ScerPS, ScerSS, ScerTS
from app import app

def import_prot_info(filepath, model, row_name, att_name, length):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        with app.app_context():
            for row in reader:
                existing_record = model.query.filter_by(protein_id=row['protein_id']).first()
                if existing_record:
                    print(f"Skipping duplicate entry: {row['protein_id']}")
                    continue
                
                # deal with null value
                value = row[row_name]
                if value.strip().upper() == "NA":
                    value = None

                prot_info = model(protein_id=row['protein_id'])
                setattr(prot_info, att_name, value[:length] if value else None)

                db.session.add(prot_info)

            db.session.commit()
            print("Successful import")


def run():
    import_prot_info(r'../data/Ecoli_ps.csv', EcoliPS, 'seq', 'seq', 2400)
    import_prot_info(r'../data/Ecoli_ss.csv', EcoliSS, 'secondary_structure', 'ss', 2400)
    import_prot_info(r'../data/Ecoli_ts.csv', EcoliTS, 'tertiary_structure', 'ts', 65)
    import_prot_info(r'../data/Scer_ps.csv', ScerPS, 'seq', 'seq', 5000)
    import_prot_info(r'../data/Scer_ss.csv', ScerSS, 'secondary_structure', 'ss', 2700)
    import_prot_info(r'../data/Scer_ts.csv', ScerTS, 'tertiary_structure', 'ts', 75)
