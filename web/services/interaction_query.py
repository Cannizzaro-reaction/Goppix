import sys
import os
from graphviz import Graph

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db, SpeciesProtein, EcoliInteractionScore, ScerInteractionScore, EcoliValidation, ScerValidation
from sqlalchemy.orm.exc import NoResultFound

class ProteinNotFoundException(Exception):
    # raised when the protein is not found in the species-protein table
    pass

class TableNotFoundException(Exception):
    # raised when the interaction table for the given species is not found (wrong species name)
    pass


def get_interaction_table(species):
    # Map species to corresponding table models
    species_table_map = {
        "E.coli": EcoliInteractionScore,
        "S.cerevisiae": ScerInteractionScore,
    }

    table_model = species_table_map.get(species)
    if not table_model:
        raise TableNotFoundException(f"No interaction table found for species '{species}'.")

    # dynamically return interaction table model
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

    # dynamically return validation table model
    return table_model


def validate_protein_species(protein, species):
    # validate that a given protein belongs to the specified species.
    protein_record = SpeciesProtein.query.filter_by(protein_id=protein, species=species).first()
    if not protein_record:
        raise ProteinNotFoundException(f"Protein '{protein}' not found in species '{species}'.")


def query_interactions(protein, species, min_score=0):
    # validate the protein-species mapping
    validate_protein_species(protein, species)

    # dynamically get tables
    InteractionTable = get_interaction_table(species)
    ValidationTable = get_validation_table(species)

    interactions = InteractionTable.query.filter(
        ((InteractionTable.protein_a == protein) | (InteractionTable.protein_b == protein)) &
        (InteractionTable.interaction_score >= min_score)
    ).all()

    if not interactions:
        return {
            "protein": protein,
            "species": species,
            "message": f"No interactions found for protein '{protein}' in species '{species}'.",
            "interactions": [],
            "interaction_data": []
        }

    # collect directly interacting proteins
    directly_connected_proteins = set(
        interaction.protein_b if interaction.protein_a == protein else interaction.protein_a
        for interaction in interactions
    )

    # get interactions between directly connected proteins
    secondary_interactions = InteractionTable.query.filter(
        (InteractionTable.protein_a.in_(directly_connected_proteins)) &
        (InteractionTable.protein_b.in_(directly_connected_proteins)) &
        (InteractionTable.interaction_score >= min_score)
    ).all()

    results = []
    interaction_data = []  # Data for visualization

    for interaction in interactions:
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

        interaction_data.append({
            "protein_a": protein,
            "protein_b": other_protein,
            "interaction_score": interaction.interaction_score,
        })

    # add secondary interactions
    for interaction in secondary_interactions:
        validations = ValidationTable.query.filter(
            ((ValidationTable.protein_a == interaction.protein_a) & (ValidationTable.protein_b == interaction.protein_b)) |
            ((ValidationTable.protein_a == interaction.protein_b) & (ValidationTable.protein_b == interaction.protein_a))
        ).all()

        validation_data = [
            {
                "experiment_approach": validation.experiment_approach,
                "pubmed_id": validation.pubmed_id,
            }
            for validation in validations
        ]

        results.append({
            "protein_a": interaction.protein_a,
            "protein_b": interaction.protein_b,
            "interaction_score": interaction.interaction_score,
            "validations": validation_data,
        })

        interaction_data.append({
            "protein_a": interaction.protein_a,
            "protein_b": interaction.protein_b,
            "interaction_score": interaction.interaction_score,
        })

    return {
        "protein": protein,
        "species": species,
        "interactions": results,
        "interaction_data": interaction_data
    }

def generate_interaction_graph(interaction_data):
    dot = Graph(comment="Protein-Protein Interaction Network", format="svg", engine="neato")
    dot.attr(rankdir="LR", overlap="false", nodesep="0.8")

    for interaction in interaction_data:
        protein_a = interaction["protein_a"]
        protein_b = interaction["protein_b"]
        score = interaction["interaction_score"]

        dot.node(protein_a, protein_a, shape="ellipse", style='filled', fillcolor='#ceaa90')
        dot.node(protein_b, protein_b, shape="ellipse", style='filled', fillcolor='#e7c5a9')

        edge_width = max(1, score / 150) # normalize
        dot.edge(protein_a, protein_b, style='dashed', color='#c3bbb080', penwidth=str(edge_width))

    return dot.pipe().decode("utf-8")