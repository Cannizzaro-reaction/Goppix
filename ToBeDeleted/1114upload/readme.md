现有数据：

`SC_pro_seq.csv` ：

第一列 gene name，第二列蛋白序列（STRING database 上直接下的序列，6600 条全）



`gene_sequence_structure.csv`：

第一列 gene name，第二列蛋白序列（从 alphafold 数据库的 `.cif` 文件里提的），第三列二级结构（从 alphafold 数据库的 `.cif` 文件里提的）

> YBL088C, YBL108C-A, YBR140C, YCL022C, YDR150W, YDR457W, YEL077W-A, YHR099W, YKR054C, YLL040C, YLL066C, YLL067C, YLR087C, YLR106C, YMR231W, YOL081W, YOR312C
>
> 以上 17 个在 alphafold 数据库里找不到，目前的序列是拿 `SC_pro_seq.csv` 里的序列填的，二级结构写的是 NA



`SC_pro_seq_url.csv`：

第一列 gene name，第二列下载三级结构文件的 url；

其中能得到 pdb 编号且 url 可访问的，写的是 pdb 的url，否则用 alphafold 数据库的 url，都找不到是 NA

> YBL108C-A, YBR140C, YCL022C, YDR150W, YDR457W, YEL077W-A, YLL040C, YLL066C, YLL067C, YLR087C, YMR231W, YOL081W, YOR312C
>
> 以上 13 个两边都找不到
>
> `SC_alias.txt` 是把 gene name 对应到 pdb 编号和 uniprot 编号（alphafold 数据库需要 uniprot 编号）的参考文件



`SC_interaction_intersect.csv`：

互作数据（取 biogrid 和 STRING 的交集）；

第一二列 gene name，第三列互作发现的实验方法，第四列报道文献的 pubmed id，第五六列物种，第七列互作得分；

除了第七列来自 STRING 外其余都是 Biogrid 的信息



其他：

`structure_url.py`：通过 gene name 得到三级结构下载地址

`get_seq_ss.py`（包括 `ss_prediction.py`）：通过 gene name 得到 alphafold 预测结构，提取二级结构和序列

> 慢，可中途中断后继续