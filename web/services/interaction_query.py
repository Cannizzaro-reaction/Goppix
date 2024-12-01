import sys
import os
from graphviz import Graph

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db, SpeciesProtein, EcoliInteractionScore, ScerInteractionScore, EcoliValidation, ScerValidation
from sqlalchemy.orm.exc import NoResultFound

class ProteinNotFoundException(Exception):
    # Raised when the protein is not found in the species-protein table
    pass

class TableNotFoundException(Exception):
    # Raised when the interaction table for the given species is not found (wrong species name)
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

def get_interaction_table(species):
    # Map species to corresponding table models
    species_table_map = {
        "E.coli": EcoliInteractionScore,
        "S.cerevisiae": ScerInteractionScore,
    }

    table_model = species_table_map.get(species)
    if not table_model:
        raise TableNotFoundException(f"No interaction table found for species '{species}'.")
    return table_model

def get_validation_table(species):
    # Map species to corresponding validation table models
    species_table_map = {
        "E.coli": EcoliValidation,
        "S.cerevisiae": ScerValidation,
    }

    table_model = species_table_map.get(species)
    if not table_model:
        raise TableNotFoundException(f"No validation table found for species '{species}'.")
    return table_model

def validate_protein_species(protein, species):
    # Validate that a given protein belongs to the specified species.
    normalized_protein = normalize_protein_id(protein, species)
    protein_record = SpeciesProtein.query.filter_by(protein_id=normalized_protein, species=species).first()
    if not protein_record:
        raise ProteinNotFoundException(f"Protein '{protein}' not found in species '{species}'.")

def query_interactions(protein, species, min_score=0):
    # Normalize and validate the protein ID
    protein = normalize_protein_id(protein, species)
    validate_protein_species(protein, species)

    # Dynamically get tables
    InteractionTable = get_interaction_table(species)
    ValidationTable = get_validation_table(species)

    # Fetch direct interactions involving the query protein
    direct_interactions = InteractionTable.query.filter(
        ((InteractionTable.protein_a == protein) | (InteractionTable.protein_b == protein)) &
        (InteractionTable.interaction_score >= min_score)
    ).all()

    if not direct_interactions:
        return {
            "protein": protein,
            "species": species,
            "message": f"No interactions found for protein '{protein}' in species '{species}'.",
            "interactions": [],
            "interaction_data": [],
            "graph_svg": None
        }

    # Collect directly connected proteins
    directly_connected_proteins = set(
        interaction.protein_b if interaction.protein_a == protein else interaction.protein_a
        for interaction in direct_interactions
    )

    # Fetch secondary interactions for visualization
    secondary_interactions = InteractionTable.query.filter(
        (InteractionTable.protein_a.in_(directly_connected_proteins)) &
        (InteractionTable.protein_b.in_(directly_connected_proteins)) &
        (InteractionTable.interaction_score >= min_score)
    ).all()

    # Prepare results for API response (direct interactions only)
    results = []
    for interaction in direct_interactions:
        other_protein = (
            interaction.protein_b if interaction.protein_a == protein else interaction.protein_a
        )
        validations = ValidationTable.query.filter(
            ((ValidationTable.protein_a == protein) & (ValidationTable.protein_b == other_protein)) |
            ((ValidationTable.protein_a == other_protein) & (ValidationTable.protein_b == protein))
        ).all()

        validation_data = [
            {
                "experiment_approach": validation.experiment_approach,
                "pubmed_id": validation.pubmed_id,
            }
            for validation in validations
        ]

        results.append({
            "protein_a": protein,
            "protein_b": other_protein,
            "interaction_score": interaction.interaction_score,
            "validations": validation_data,
        })

    # Prepare data for visualization (direct + secondary interactions)
    interaction_data = []
    for interaction in direct_interactions + secondary_interactions:
        interaction_data.append({
            "protein_a": interaction.protein_a,
            "protein_b": interaction.protein_b,
            "interaction_score": interaction.interaction_score,
        })

    # Generate interaction graph SVG
    graph_svg = generate_interaction_graph(interaction_data)

    # Return the filtered results
    return {
        "protein": protein,
        "species": species,
        "interactions": results,  # only direct interactions
        "interaction_data": interaction_data,  # includes both direct and secondary interactions
        "graph_svg": graph_svg  # include the generated SVG graph
    }

def generate_interaction_graph(interaction_data):
    dot = Graph(comment="Protein-Protein Interaction Network", format="svg", engine="neato")
    dot.attr(rankdir="LR", overlap="false", nodesep="0.8")

    node_color = '#ceaa90'
    edge_color = '#c3bbb080'
    edge_style = 'dashed'

    for interaction in interaction_data:
        protein_a = interaction["protein_a"]
        protein_b = interaction["protein_b"]
        score = interaction["interaction_score"]

        dot.node(protein_a, protein_a, shape="ellipse", style='filled', fillcolor=node_color)
        dot.node(protein_b, protein_b, shape="ellipse", style='filled', fillcolor=node_color)

        edge_width = max(1, score / 150)  # Normalize edge width
        dot.edge(protein_a, protein_b, style=edge_style, color=edge_color, penwidth=str(edge_width))

    return dot.pipe().decode("utf-8")
