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
