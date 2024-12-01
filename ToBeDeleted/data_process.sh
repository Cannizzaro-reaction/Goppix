# interaction data
tr ' ' ',' < SC_interaction_string.txt > SC_interaction_string.csv
sed 's/^[0-9]*\.\([A-Za-z0-9_]*\),[0-9]*\.\([A-Za-z0-9_]*\)/\1,\2/' SC_interaction_string.csv > SC_interaction_string_clear.csv
sed 's/,/;/g' SC_interaction_biogrid.txt > SC_interaction_biogrid_clear.txt
tr '\t' ',' < SC_interaction_biogrid_clear.txt > SC_interaction_biogrid.csv

awk -F, 'BEGIN {OFS=","} NR==1 {for (i=1; i<=NF; i++) colname[$i]=i}
         NR>1 {print $colname["Systematic Name Interactor A"],
                      $colname["Systematic Name Interactor B"],
                      $colname["Experimental System"],
                      $colname["Publication Source"],
                      $colname["Organism ID Interactor A"],
                      $colname["Organism ID Interactor B"]}' SC_interaction_biogrid.csv > SC_interaction.csv
awk -F, '$(NF-1) != "559292" || $NF != "559292" {count++} END {print count}' SC_interaction.csv #4258 # 53
awk -F, '$(NF-1) == "559292" && $NF == "559292"' SC_interaction.csv > SC_interaction_filtered.csv
wc -l < SC_interaction_filtered.csv #853470 # 2381

# get_score.sh
# Step 1: Create a dictionary of protein pairs and their scores from SC_interaction_string_clear.csv
awk -F, 'NR>1 {if ($1 < $2) key=$1","$2; else key=$2","$1; score[key]=$NF} END {for (k in score) print k, score[k]}' OFS=',' SC_interaction_string_clear.csv > score_dict.csv

# Step 2: Add scores to SC_interaction_filtered.csv; if no match, append "NA"
awk -F, 'NR==FNR {score[$1","$2]=$3; next} 
         NR>FNR {
             if (($1","$2) in score) {
                 print $0, score[$1","$2]
             }
             else if (($2","$1) in score) {
                 print $0, score[$2","$1]
             }
             else {
                 print $0, "NA"
             }
         }' OFS=',' score_dict.csv SC_interaction_filtered.csv > SC_interaction_filtered_with_scores.csv

awk -F, '$NF != "NA" {count++} END {print count}' SC_interaction_filtered_with_scores.csv # 476916 # 1436
awk -F, '$NF != "NA"' SC_interaction_filtered_with_scores.csv > SC_interaction_intersect.csv
wc -l < SC_interaction_intersect.csv # interaction information(in both database): 476916, 1436

# protein info
grep -c "^>" SC_pro_seq.fa # 6600 # 4140

awk -F, '{print $1; print $2}' SC_interaction_intersect.csv | sort | uniq > reference_ids.txt
awk -F, 'NR==FNR {ref[$1]; next} !($1 in ref)' reference_ids.txt SC_pro_seq.csv | wc -l 
# protein not in interaction table: 833, 3018

awk -F, '{print $1}' SC_pro_seq.csv | sort | uniq > reference_proteins.txt
awk -F, 'NR==FNR {ref[$1]; next} !($1 in ref) || !($2 in ref)' reference_proteins.txt SC_interaction_intersect.csv | wc -l 
# all proteins in interaction table is included in protein list






# go信息表和goi表比较
comm -23 <(awk -F, '{print $1; print $3}' goi.csv | sort | uniq) <(awk -F, '{print $1}' go_info.csv | sort | uniq)
# 基因go表和go信息表比较
comm -23 <(awk -F, '{print $2}' gene_go.csv | sort | uniq) <(awk -F, '{print $1}' go_info.csv | sort | uniq) > not_in_go_info.txt

# 得到string长度
awk -F',' '{if(NR>1) max=(length($2)>max)?length($1):max} END {print max}' go_info.csv # 10
awk -F',' '{if(NR>1) max=(length($2)>max)?length($2):max} END {print max}' go_info.csv # 189
awk -F',' '{if(NR>1) max=(length($2)>max)?length($3):max} END {print max}' go_info.csv # 18
awk -F',' '{if(NR>1) max=(length($2)>max)?length($4):max} END {print max}' go_info.csv # 200

awk -F',' '{if(NR>1) max=(length($2)>max)?length($2):max} END {print max}' goi.csv # 20

# 数据表查看
SELECT * FROM go_info LIMIT 10\G


# delete information about species in interaction table
awk -F, '{
    first = 1
    for (i=1; i<=NF; i++) {
        if (i != 5 && i != 6) {
            if (!first) printf ","
            printf "%s", $i
            first = 0
        }
    }
    printf "\n"
}' SC_interaction_intersect.csv > SC_interaction_clear.csv


# look for replication in interaction data
awk -F',' 'NR==1 {next} {pair=$1","$2; count[pair]++; records[pair]=records[pair] $0 "\n"} END {for (p in count) if (count[p] > 1) printf "%s", records[p]}' Ecoli_prot_interaction.csv
awk -F',' 'NR==1 {next} {pair=$1","$2; count[pair]++; records[pair]=records[pair] $0 "\n"} END {for (p in count) if (count[p] > 1) printf "%s", records[p]}' Scer_prot_interaction.csv

# split interaction table
# table1: protein_a, protein_b, score
# table2: protein_a, protein_b, pubmed_id, experiment_approach
awk -F',' '!seen[$1,$2,$5]++ {print $1 "," $2 "," $5}' Ecoli_prot_interaction.csv > Ecoli_interaction_score.csv
awk -F',' '!seen[$1,$2,$5]++ {print $1 "," $2 "," $5}' Scer_prot_interaction.csv > Scer_interaction_score.csv

awk -F',' '!seen[$1,$2,$3,$4]++ {print $1 "," $2 "," $3 "," $4}' Ecoli_prot_interaction.csv > Ecoli_validation.csv
awk -F',' '!seen[$1,$2,$3,$4]++ {print $1 "," $2 "," $3 "," $4}' Scer_prot_interaction.csv > Scer_validation.csv

# check replication
awk -F',' '{key=$1","$2; count[key]++} END {for (k in count) if (count[k]>1) print k, count[k]}' Scer_interaction_score.csv
awk -F',' '{key=$1","$2; count[key]++} END {for (k in count) if (count[k]>1) print k, count[k]}' Ecoli_interaction_score.csv
awk -F',' '{key=$1","$2","$3","$4; count[key]++} END {for (k in count) if (count[k]>1) print k, count[k]}' Scer_validation.csv
awk -F',' '{key=$1","$2","$3","$4; count[key]++} END {for (k in count) if (count[k]>1) print k, count[k]}' Ecoli_validation.csv

awk -F',' '{key=$1","$2","$3","$4; count[key]++} END {for (k in count) if (count[k]>1) print k, count[k]}' Scer_prot_interaction.csv
# 有4组数据重复，得分没影响


# get rid of replication like: prot_a, prot_b VS prot_b, prot_a
awk -F',' 'NR==1 {print; next} {key=($1<$2 ? $1","$2 : $2","$1)","$3","$4; if (!seen[key]++) print $0}' Scer_validation.csv > Scer_validation_deduplicated.csv
awk -F',' 'NR>1 {key=($1<$2 ? $1","$2 : $2","$1)","$3","$4; count[key]++} END {for (k in count) if (count[k]>1) print k, count[k]}' Scer_validation_no_rep.csv

awk -F',' 'NR==1 {print; next} {key=($1<$2 ? $1","$2 : $2","$1); if (!seen[key]++) print $0}' Ecoli_interaction_score.csv > Ecoli_score_deduplicated.csv
awk -F',' 'NR==1 {next} {key=($1<$2 ? $1","$2 : $2","$1); if (seen[key]++) print $0}' Ecoli_score_deduplicated.csv

awk -F',' 'NR==1 {print; next} {key=($1<$2 ? $1","$2 : $2","$1); if (!seen[key]++) print $0}' Scer_interaction_score.csv > Scer_score_deduplicated.csv
awk -F',' 'NR==1 {next} {key=($1<$2 ? $1","$2 : $2","$1); if (seen[key]++) print $0}' Scer_score_deduplicated.csv


# merge protein information table
awk -F, 'FNR==NR {data1[$1] = $2 "," $3; next} 
         {
            if ($1 in data1) {
                print $1 "," $2 "," data1[$1]
            } else {
                print $1 "," $2 ",NA,NA"
            }
         }' K12_PdbSeq_SecondaryStructure.csv K12_pro_seq_url.csv > K12_prot_info1.csv

# add sequence to the remaining protein
awk -F, 'BEGIN {OFS = ","}
         FNR==NR {data[$1] = $2; next}
         {
            if ($2 == "NA" && $1 in data) {
                $2 = data[$1]
            }
            print $0
         }' K12_pro_seq.csv K12_gene_sequence_structure1.csv > K12_gene_sequence_structure.csv

# split protein information data to satisfy 3NF
awk -F, 'NR==1 {print $1","$2","$3 > "Ecoli_seq_pdb.csv"}
         NR>1 {print $1","$2","$3 >> "Ecoli_seq_pdb.csv"}' K12_prot_info.csv

awk -F, 'NR==1 {print $1","$4 > "Ecoli_ss.csv"}
         NR>1 {print $1","$4 >> "Ecoli_ss.csv"}' K12_prot_info.csv

# count length in each column
# url for pdb file
awk -F',' '{if(NR>1) max=(length($2)>max)?length($2):max} END {print max}' Scer_seq_pdb.csv # 69
awk -F',' '{if(NR>1) max=(length($2)>max)?length($2):max} END {print max}' Ecoli_seq_pdb.csv # 59

# protein sequence
awk -F',' '{if(NR>1) max=(length($3)>max)?length($3):max} END {print max}' Scer_seq_pdb.csv # 20300
awk -F',' '{if(NR>1) max=(length($3)>max)?length($3):max} END {print max}' Ecoli_seq_pdb.csv # 26368

# secondary structure
awk -F',' '{if(NR>1) max=(length($2)>max)?length($2):max} END {print max}' Scer_ss.csv # 20300
awk -F',' '{if(NR>1) max=(length($2)>max)?length($2):max} END {print max}' Ecoli_ss.csv # 26368

# split protein information(12.1)
awk -F, '{print $1 "," $2 > "Scer_ps.csv"; print $1 "," $3 > "Scer_ss.csv"}' gene_sequence_structure.csv

awk -F, '{
    if (NR > 1) {
        len = length($2)
        if (len > max) max = len
    }
}
END {
    print "最大长度:", max
}' Scer_ts.csv
# 2358, 2358, 59
# 4910, 2620, 69

## pro_ver of checking
awk -F, '{
    if (NR > 1) {
        len = length($2)
        if (len > max) {
            max = len
            max_line = $0
            max_line_num = NR
        }
    }
}
END {
    print "最大长度:", max
    print "对应行:", max_line
    print "行号:", max_line_num
}' Scer_ps.csv

# check if the length of primary structure and secondary structure are the same
awk -F, 'length($3) != length($2) {count++} END {print count}' gene_sequence_structure.csv

# get rid of duplicated rows in go information
awk -F, 'NR == 1 || !seen[$1","$2]++' K12_gene_go.csv > Ecoli_protein_go.csv
awk -F, '!seen[$1]++ { count++ } END { print "Unique values in the first column:", count }' Ecoli_protein_go.csv
# Scer: 5802, Ecoli: 3725