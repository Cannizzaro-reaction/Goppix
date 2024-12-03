from flask import request
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound
from models import db, EcoliPS, EcoliSS, EcoliTS, ScerPS, ScerSS, ScerTS, EcoliProtGO, ScerProtGO, SpeciesProtein, GoBasic

class TableNotFoundException(Exception):
    # Raised when the interaction table for the given species is not found (wrong species name)
    pass

class ProteinNotFoundException(Exception):
    # Raised when the protein is not found in the species-protein table
    pass


def normalize_protein_id(protein_id, species):
    """
    Normalize the protein ID based on species.
    E. coli: all lowercase
    S. cerevisiae: all uppercase
    """
    if species.lower() == "e.coli":
        return protein_id.strip().lower()
    elif species.lower() == "s.cerevisiae":
        return protein_id.strip().upper()
    else:
        raise TableNotFoundException(f"Species '{species}' not supported.")

def validate_protein_species(protein, species):
    # Validate that a given protein belongs to the specified species.
    normalized_protein = normalize_protein_id(protein, species)
    protein_record = SpeciesProtein.query.filter_by(protein_id=normalized_protein, species=species).first()
    if not protein_record:
        raise ProteinNotFoundException(f"Protein '{protein}' not found in species '{species}'.")
    
def get_info_tables(species):
    # mapping tables to different species
    species_table_map = {
        "E.coli": {
            "primary": EcoliPS,
            "secondary": EcoliSS,
            "tertiary": EcoliTS,
            "go": EcoliProtGO,
        },
        "S.cerevisiae": {
            "primary": ScerPS,
            "secondary": ScerSS,
            "tertiary": ScerTS,
            "go": ScerProtGO,
        }
    }
    
    if species not in species_table_map:
        raise TableNotFoundException(f"Species '{species}' not supported.")
    
    return species_table_map[species]

def query_by_sequence(sequence, species):
    """
    Get protein information by sequence searching.
    The sequence will be used to get protein_id and merge into id searching.
    """
    # map species to the corresponding primary structure table
    species_table_map = {
        "E.coli": EcoliPS,
        "S.cerevisiae": ScerPS,
    }

    if species not in species_table_map:
        raise TableNotFoundException(f"Species '{species}' not supported.")
    
    primary_structure_table = species_table_map[species]
    record = primary_structure_table.query.filter_by(seq=sequence.strip()).first()
    
    if not record:
        raise ProteinNotFoundException(f"No protein found for the given sequence in '{species}'.")

    protein_id = record.protein_id
    return query_structure_go(protein_id, species)

def query_structure_go(protein_id, species):
    # Get the appropriate table classes for the species
    info_tables = get_info_tables(species)
    protein_id = normalize_protein_id(protein_id, species)
    validate_protein_species(protein_id, species)
    
    results = {
        "id": protein_id,
        "primary": "unknown",
        "secondary": "unknown",
        "tertiary": "unknown",
        "go": []
    }
    
    for info_type, table_class in info_tables.items():
        record = table_class.query.filter_by(protein_id=protein_id).first()

        if record:
            if info_type == "go":
                go_terms = table_class.query.filter_by(protein_id=protein_id).all()
                go_info_list = []
                for go_term in go_terms:
                    go_detail = GoBasic.query.filter_by(id=go_term.go).first()
                    if go_detail:
                        go_info = go_detail.to_dict()
                        go_info_list.append(go_info)
                    else:
                        go_info_list.append({"id": go_term.go, "name": "unknown", "category": "unknown"})
                results["go"] = go_info_list
            else:
                value = getattr(record, "seq", None) or getattr(record, "ss", None) or getattr(record, "ts", None)
                results[info_type] = value if value else "unknown"

    return results