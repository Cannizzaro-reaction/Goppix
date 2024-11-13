import requests
import pandas as pd
import os

from ss_prediction import secondary_structure
from structure_url import get_id_dict

def check_alphafold_cif(uniprot_id):
    url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.cif"
    response = requests.head(url)
    return url if response.status_code == 200 else None

def get_uniprot_and_download_cif(gene_data, output_dir="cif_files"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for uniprot_id in gene_data.get("uniprot_ids", []):
        cif_url = check_alphafold_cif(uniprot_id)
        if cif_url:
            cif_path = os.path.join(output_dir, f"{uniprot_id}.cif")
            if not os.path.exists(cif_path):
                response = requests.get(cif_url)
                with open(cif_path, "wb") as file:
                    file.write(response.content)
            return cif_path
    return None

def find_structure_and_extract(gene_id, gene_data, output_dir="cif_files"):
    cif_file = get_uniprot_and_download_cif(gene_data, output_dir)
    if cif_file:
        sequence, sequence_length, sec_structure = secondary_structure(cif_file)

        os.remove(cif_file)
        
        return sequence, sec_structure
    return "NA", "NA"

def add_sequence_and_structure(df, mapping, output_file="gene_sequence_structure.csv"):
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
            sequence, sec_structure = find_structure_and_extract(gene_id, gene_data)

            file.write(f"{gene_id},{sequence},{sec_structure}\n")
            file.flush()
                
            count += 1
            if count % 100 == 0:
                print(f"{count} entries have been processed.")

    print('Gene sequence and structure data have been saved incrementally!')

if __name__ == "__main__":
    gene_list_df = pd.read_csv("SC_pro_seq.csv")
    gene_mapping = get_id_dict("SC_alias.txt")

    add_sequence_and_structure(gene_list_df, gene_mapping)
