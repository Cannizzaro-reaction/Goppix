import os

def extract_sequence_from_cif(data):
    sequence = ""
    in_sequence = False

    for line in data.splitlines():
        if line.startswith("_entity_poly.pdbx_seq_one_letter_code_can"):
            parts = line.split()
            if len(parts) > 1:
                # 单行格式，标签和序列在同一行
                sequence = parts[1]
                return sequence, len(sequence)
            else:
                # 多行格式，标记开始读取序列
                in_sequence = True
                continue

        if in_sequence:
            if line.strip() == ";":
                if sequence:
                    in_sequence = False
                    break
                continue
            else:
                sequence += line.strip()

    sequence = sequence[1:]
    return sequence, len(sequence)

def parse_secondary_structure_from_text(data, sequence_length):
    regions = []

    for line in data.splitlines():
        if not line.strip().endswith("? ?"):
            continue

        parts = line.split()
        if len(parts) < 8:
            continue

        start_res = int(parts[2])
        end_res = int(parts[9])

        sec_structure = parts[6]
        symbol = "C"
        if "HELX" in sec_structure:
            symbol = "H"
        elif "TURN" in sec_structure:
            symbol = "T"
        elif "BEND" in sec_structure:
            symbol = "B"

        regions.append((start_res, end_res, symbol))

    structure_seq = ["C"] * sequence_length
    for start_res, end_res, symbol in regions:
        for i in range(start_res - 1, end_res):
            if i < sequence_length:
                structure_seq[i] = symbol

    return "".join(structure_seq)

def extract_secondary_structure_from_cif(cif_file):
    with open(cif_file, 'r') as file:
        data = file.read()

    sequence, sequence_length = extract_sequence_from_cif(data)
    sec_structure = parse_secondary_structure_from_text(data, sequence_length)
    return sequence, sequence_length, sec_structure

def secondary_structure(cif_file):
    if not os.path.isfile(cif_file):
        print("File does not exist. Please check the file path.")
        return

    sequence, sequence_length, sec_structure = extract_secondary_structure_from_cif(cif_file)
    if sec_structure:
        pass
        # print(f"Secondary Structure for {cif_file}: {sec_structure}")
    else:
        print("No secondary structure information extracted.")
    
    return sequence, sequence_length, sec_structure

if __name__ == "__main__":
    cif_file_path = "AF-P38967-F1-model_v4.cif"
    secondary_structure(cif_file_path)
