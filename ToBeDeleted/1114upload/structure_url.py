import requests
import pandas as pd
from Bio.PDB import PDBParser, DSSP
import os
from Bio import SeqIO
from Bio.PDB import MMCIFParser, PDBIO

def get_id_dict(filepath):
    pdb_sources = {"Ensembl_PDB", "UniProt_DR_PDB"}
    uniprot_sources = {"Ensembl_UniProt", "UniProt_AC"}

    mapping = {}

    with open(filepath, 'r') as file:
        next(file)
        for line in file:
            parts = line.strip().split('\t')
            gene_id = parts[0].replace('4932.', '')

            if gene_id not in mapping:
                mapping[gene_id] = {"pdb_ids": set(), "uniprot_ids": set()}

            if parts[-1] in pdb_sources:
                mapping[gene_id]["pdb_ids"].add(parts[1])
            elif parts[-1] in uniprot_sources:
                mapping[gene_id]["uniprot_ids"].add(parts[1])

    mapping = {gene_id: {"pdb_ids": list(ids["pdb_ids"]), "uniprot_ids": list(ids["uniprot_ids"])}
               for gene_id, ids in mapping.items()}
    return mapping

def check_pdb(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.head(url)
    return url if response.status_code == 200 else None

def check_alphafold(uniprot_id):
    url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
    response = requests.head(url)
    return url if response.status_code == 200 else None

def find_structure_url(gene_data):
    for pdb_id in gene_data.get("pdb_ids", []):
        pdb_url = check_pdb(pdb_id)
        if pdb_url:
            return pdb_url

    for uniprot_id in gene_data.get("uniprot_ids", []):
        alphafold_url = check_alphafold(uniprot_id)
        if alphafold_url:
            return alphafold_url
        
    return "NA"

def add_url(df, mapping, output_file="SC_pro_seq_url.csv"):
    try:
        processed_df = pd.read_csv(output_file, header=None)
        processed_genes = set(processed_df.iloc[:, 0].values)
    except FileNotFoundError:
        processed_genes = set()
    
    with open(output_file, "a") as file:
        count = 0
        for gene_id in df.iloc[:, 0]:
            if gene_id in processed_genes:
                continue

            gene_data = mapping.get(gene_id, {"pdb_ids": [], "uniprot_ids": []})
            url = find_structure_url(gene_data)

            file.write(f"{gene_id},{url}\n")
            file.flush()
            
            count += 1
            if count % 100 == 0:
                print(f"{count} URLs have been processed.")

    print('Dataframe with urls has been saved incrementally!')
