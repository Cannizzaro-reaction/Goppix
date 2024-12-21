# Protein-Protein Interaction Network and Functional Annotation Database



## Introduction

**GOPPIX Database** is a comprehensive resource designed to facilitate the exploration and analysis of protein interactions and functional annotations. This database integrates data from multiple reliable sources, such as BioGRID, STRING, PDB, AlphaFold, SWISS-MODEL, MyGene.info, and the Gene Ontology database. The dataset encompasses detailed information about protein interactions, experimental validation, protein structures (primary, secondary, and tertiary), and functional annotations using Gene Ontology (GO) terms.

With 16 meticulously designed tables conforming to the BCNF standard, the database supports a range of queries. Users can retrieve detailed protein information (such as sequences, structures, and GO annotations), explore GO term descriptions and interactions, analyze protein-protein interaction scores, and even download comprehensive datasets for specific species. Supported organisms include *Escherichia coli* and *Saccharomyces cerevisiae*.

The database also features a suite of APIs for retrieving and visualizing interaction networks, enabling researchers to perform targeted queries and gain insights into protein functionality and interaction mechanisms. This resource is an essential tool for researchers in the fields of bioinformatics, molecular biology, and systems biology, offering robust data and functionality to support advanced analysis.

GOPPIX is a name given by ChatGPT. GO represents the Gene Ontology annotations included in our database, while PPI highlights our database's focus on protein-protein interaction data within organisms. "X" signifies the unknown, which users can explore through our database to gain deeper insights into protein functional networks and uncover the unknown.



## Installation

* Create environment:

  Go to the directory of environment file:

  ```bash
  cd environment
  ```

  Create environment using Anaconda:

  ```bash
  conda env create -f environment_backend1.yml
  ```

  Activate the environment:

  ```bash
  conda activate goppix
  ```

* Database setup:

  Go to *web* directory. Edit the `.env` file to include your database credentials.

  Create the database:

  ```bash
  mysql -u <DB_USER> -p -e "CREATE DATABASE goppix;"
  ```

  Import data:

  ```
  python setup.py
  ```

  After setup, test in your MySQL, and your database will look something like this:

  ```mysql
  mysql> USE goppix;
  Reading table information for completion of table and column names
  You can turn off this feature to get a quicker startup with -A
  
  Database changed
  mysql> SHOW TABLES;
  +---------------------------+
  | Tables_in_goppix          |
  +---------------------------+
  | Ecoli_interaction_score   |
  | Ecoli_primary_structure   |
  | Ecoli_protein_go          |
  | Ecoli_secondary_structure |
  | Ecoli_tertiary_structure  |
  | Ecoli_validation          |
  | Scer_interaction_score    |
  | Scer_primary_structure    |
  | Scer_protein_go           |
  | Scer_secondary_structure  |
  | Scer_tertiary_structure   |
  | Scer_validation           |
  | go_basic                  |
  | go_detail                 |
  | go_interaction            |
  | species_protein           |
  +---------------------------+
  16 rows in set (0.01 sec)
  ```

  An alternative way to import data is by running all the `run` functions in the `scripts` directory. Before that, remember to run `app.py` to create all tables.

* After that, you can start this application with:

  ```bash
  python app.py
  ```



## Back-end

### Data Source :bulb:

🧩[BioGRID](https://thebiogrid.org/)

BioGRID is one of the main source of interaction data in our project. Besides, the interaction validation data, including the PubMed IDs of the articles verifying the interactions and the experimental methods, is provided by BioGRID.

🧩 [STRING](https://string-db.org/)

The STRING database also provides a large amount of interaction data. Unlike BioGRID, it primarily provides interaction scores based on experiments and predictions, which indicate the reliability of a given interaction. The final interactions shown in our database are an intersection of the two databases mentioned above. Additionally, we use protein sequences from the STRING database when structure files are unavailable for certain proteins. Furthermore, we retrieve protein aliases and corresponding tertiary structure names from the STRING database to facilitate cross-database searches and conversions.

🧩 [PDB](https://www.rcsb.org/)

We obtain the download URLs for protein tertiary structure files from the PDB database. The tertiary structure from PDB database is obtained from experiment, including X-ray Crystallography, NMR Spectroscopy, Cryo-EM, etc. So when we are collecting tertiary structure data for each protein, data from PDB database is given the top priority.

🧩 [AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/)

The AlphaFold database provides over 200 million protein structure predictions generated by AlphaFold model. When experimental structures cannot be retrieved from the PDB database, we prioritize searching the AlphaFold database to obtain the download URL for predicted structures. Additionally, we extract sequences and secondary structures from the `.cif` files provided by the AlphaFold database to ensure correspondence between the secondary structures and sequences.

🧩 [SWISS-MODEL](https://swissmodel.expasy.org/)

SWISS-MODEL is a fully automated protein structure homology-modelling server. When valid tertiary structures cannot be obtained from the previous two databases, we manually supplement them using SWISS-MODEL.

🧩 [MyGene.info](https://mygene.info/)

MyGene.info can be used to quickly retrieve functional annotations for each gene, specifically GO terms.

🧩 [Gene Oncology](https://geneontology.org/)

The Gene Ontology database provides detailed information about GO terms. In this project, we obtained the GO term information files from the Gene Ontology database and extracted the interaction relationships between different GO terms.



### Database Design :card_file_box: 

This database contains a total of 16 tables, and its design adheres to the BCNF (Boyce-Codd Normal Form) standard.

:pushpin: ​`species_protein` table

This table records the name of protein and the corresponding species, including *E. coli* and *S. cerevisiae*.

| Column Name | Data Type  | Constraints | Description                                                |
| ----------- | ---------- | ----------- | ---------------------------------------------------------- |
| protein_id  | String(10) | Primary Key | The name (ID) of the protein                               |
| species     | String(20) | NOT NULL    | The name of the species from which this protein originates |



:pushpin: `go_basic` table

This table records the basic information of each GO term, including its name and category.

| Column Name | Data Type   | Constraints           | Description                                                  |
| ----------- | ----------- | --------------------- | ------------------------------------------------------------ |
| id          | String(15)  | Primary Key, NOT NULL | The ID of each GO term, serving as a unique identifier       |
| name        | String(200) | NOT NULL              | The name of the GO term                                      |
| category    | String(20)  | NOT NULL              | The category of the GO term, including biological process, molecular function and cellular component |



:pushpin: `go_detail` table

This table provides detailed information about each GO term.

| Column Name | Data Type  | Constraints           | Description                                            |
| ----------- | ---------- | --------------------- | ------------------------------------------------------ |
| id          | String(15) | Primary Key, NOT NULL | The ID of each GO term, serving as a unique identifier |
| description | Text       | NOT NULL              | A detailed description of the GO term                  |



:pushpin: `go_interaction` table

This table records a directed relationship between two GO terms in each row. One GO term may have different relationships with different other terms.

| Column Name  | Data Type  | Constraints                           | Description                                                  |
| ------------ | ---------- | ------------------------------------- | ------------------------------------------------------------ |
| index        | Integer    | Primary Key, NOT NULL                 | A unique identifier for each record in the table             |
| go_id        | String(15) | Foreign Key (`go_basic.id`), NOT NULL | The source GO term in this relationship, which is a foreign key from the `id` field in `go_basic` |
| relationship | String(50) | NOT NULL                              | The type of relationship between the two GO terms, including `is_a`, `part_of`, `positively_regulates`, `negatively_regulates` and `regulates` |
| target_go_id | String(15) | Foreign Key (`go_basic.id`), NOT NULL | The target GO term in this relationship, which is a foreign key from the `id` field in `go_basic` |



:pushpin: `Ecoli_interaction_score` table & `Scer_interaction_score` table

These two tables document key protein-protein interactions in *E. coli* and *S. cerevisiae*. The first two columns represent the two proteins involved in the interaction, while the third column provides the interaction score. This score is calculated by integrating probabilities from various evidence channels and adjusting for the likelihood of randomly observing an interaction.

| Column Name       | Data Type  | Constraints                                                  | Description                                                  |
| ----------------- | ---------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| protein_a         | String(10) | Primary Key, Foreign Key (`species_protein.protein_id`), NOT NULL | One of the protein in the interaction, which is a foreign key from the `protein_id` field in `species_protein` |
| protein_b         | String(10) | Primary Key, Foreign Key (`species_protein.protein_id`), NOT NULL | One of the protein in the interaction, which is a foreign key from the `protein_id` field in `species_protein` |
| interaction_score | Integer    | NOT NULL                                                     | The interaction score given by combining the probabilities from the different evidence channels |



:pushpin: `Ecoli_validation` table & `Scer_validation` table

These two tables record the experimental validation information of protein-protein interactions in *E. coli* and *S. cerevisiae*. The validation information includes the type of experiment and the PubMed ID of the paper that reports the interaction. An interaction may have been validated by more than one type of experiment or reported in more than one paper.

| Column Name         | Data Type  | Constraints                                                  | Description                                                  |
| ------------------- | ---------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| protein_a           | String(10) | Primary Key, Foreign Key (`species_protein.protein_id`), NOT NULL | One of the protein in the interaction, which is a foreign key from the `protein_id` field in `species_protein` |
| protein_b           | String(10) | Primary Key, Foreign Key (`species_protein.protein_id`), NOT NULL | One of the protein in the interaction, which is a foreign key from the `protein_id` field in `species_protein` |
| experiment_approach | String(30) | Primary Key, NOT NULL                                        | The type of experiment that has validated this interaction   |
| pubmed_id           | String(20) | Primary Key, NOT NULL                                        | The paper that reports this interaction                      |



:pushpin: `Ecoli_protein_go` & `Scer_protein_go` table

These two tables provide information about the functional annotation (which is GO term in our database) of each protein in *E. coli* and *S. cerevisiae*. One `protein_id` may have more than one record if it has several GO terms.

| Column Name | Data Type  | Constraints                                                  | Description                                         |
| ----------- | ---------- | ------------------------------------------------------------ | --------------------------------------------------- |
| protein_id  | String(10) | Primary Key, Foreign Key (`species_protein.protein_id`), NOT NULL | ID of the protein (FK)                              |
| go          | String(15) | Primary Key, Foreign Key (`go_basic.id`), NOT NULL           | The functional annotation (GO term) of this protein |



:pushpin: `Ecoli_primary_structure` & `Scer_primary_structure` table

These two tables provide primary structure (sequence) for each corresponding protein. The sequence is obtained from the Alpha Fold database to ensure alignment with the secondary structure. The missing information is supplemented using sequences from the STRING database.

| Column Name | Data Type                                 | Constraints                                                  | Description             |
| ----------- | ----------------------------------------- | ------------------------------------------------------------ | ----------------------- |
| protein_id  | String(10)                                | Primary Key, Foreign Key (`species_protein.protein_id`), NOT NULL | ID of the protein (FK)  |
| seq         | Ecoli: String(2400) \| Scer: String(5000) | /                                                            | Sequence of the protein |



:pushpin: `Ecoli_secondary_structure` & `Scer_secondary_structure` table

These two tables provide secondary structure for each corresponding protein. The secondary structure is given in string format and presented as "C", "H", T", or "B", in which "H" represents helix, "T" represents turn, "B" represents bend, and "C" represents the other remaining secondary structure, which mainly contains beta sheet.

The secondary structure sequence corresponds one-to-one with the primary structure sequence. The information is taken from the predicted tertiary structure files in `.cif` format by a package developed by ourselves. The tertiary structures are got from Alpha Fold database. There are some missing values, which we can't get tertiary structure files or extract secondary structure successfully.

| Column Name | Data Type                                 | Constraints                                                  | Description                        |
| ----------- | ----------------------------------------- | ------------------------------------------------------------ | ---------------------------------- |
| protein_id  | String(10)                                | Primary Key, Foreign Key (`species_protein.protein_id`), NOT NULL | ID of the protein (FK)             |
| ss          | Ecoli: String(2400) \| Scer: String(2700) | /                                                            | Secondary structure of the protein |



:pushpin: `Ecoli_tertiary_structure` & `Scer_tertiary_structure` table

These two tables provide download URL for tertiary structure of each corresponding protein. Proteins are first searched in the PDB database for tertiary structures. If no structure is found, the predicted structure is retrieved from the Alpha Fold database. The remaining proteins are supplemented using the SWISS-MODEL database. There are some missing values, which tertiary structure can't be obtained from the three databases above.

| Column Name | Data Type                             | Constraints                                                  | Description                       |
| ----------- | ------------------------------------- | ------------------------------------------------------------ | --------------------------------- |
| protein_id  | String(10)                            | Primary Key, Foreign Key (`species_protein.protein_id`), NOT NULL | ID of the protein (FK)            |
| ts          | Ecoli: String(65) \| Scer: String(75) | /                                                            | Tertiary Structure of the protein |



### Query API Design​ :mag_right:

#### :old_key: Retrieve Basic Protein Information

This API allows users to retrieve information about proteins based on their ID or sequence. The response includes primary, secondary, tertiary structures, and functional annotations.

* Endpoint: `GET /basic-info-search`

* Request Parameters:

  | Parameter     | Data Type | Required | Description                                                  |
  | ------------- | --------- | -------- | ------------------------------------------------------------ |
  | `search_type` | `string`  | Yes      | The type of search, choosing from `protein_id` or `sequence` |
  | `protein`     | `string`  | Yes      | The protein ID or sequence to query                          |
  | `species`     | `string`  | Yes      | The species of the protein (`E.coli` and `S.cerevisiae` supported) |

* Example Request URL:

  ```
  http://127.0.0.1:5000/go-search/GO:0000122
  ```

* Response Structure:

  | Field                 | Type     | Description                                                  |
  | --------------------- | -------- | ------------------------------------------------------------ |
  | `protein_id`          | `string` | The ID of the protein                                        |
  | `species`             | `string` | The species of the protein                                   |
  | `primary_structure`   | `string` | The primary structure (sequence) of the protein              |
  | `secondary_structure` | `string` | The secondary structure of the protein                       |
  | `tertiary_structure`  | `string` | The URL to download the tertiary structure of the protein    |
  | `go_terms`            | `array`  | A list of Gene Ontology (GO) terms associated with the protein |
  | \|-- `id`             | `string` | The GO term ID                                               |
  | \|-- `name`           | `string` | The name of the GO term                                      |
  | \|-- `category`       | `string` | The category of the GO term                                  |

* Error Code

  | HTTP Status Code | Description                                                  |
  | ---------------- | ------------------------------------------------------------ |
  | `404`            | One or more required parameters are missing, or there is something wrong in the format of the parameters |
  | `400`            | The queried protein does not exist in the database           |
  | `500`            | Unexpected Error                                             |

* Notes:

  * Case Insensitivity: The letters in protein IDs of E.coli will be automatically normalized to lowercase, while the letters in protein IDs of S.cerevisiae will be automatically normalized to uppercase.

    

#### :old_key: Retrieve GO term description and GO interaction

This API allows users to query specific GO terms and returns information including detailed GO term data and interaction data. In the detailed information section, users can obtain the name, category, and a detailed explanation of the GO term. In the interaction data section, users can retrieve GO terms that are related to the queried GO term, along with the type of relationship between them.

* Endpoint: `GET /go-search/<string:go_id>`

* Request Parameters:

  | Parameter | Data Type | Required | Description          |
  | --------- | --------- | -------- | -------------------- |
  | `go_id`   | `string`  | Yes      | The GO term to query |

* Example Request URL:

  ```
  http://127.0.0.1:5000/go-search/GO:0000122
  ```

* Response Structure:

  | Field                   | Type     | Description                                                  |
  | ----------------------- | -------- | ------------------------------------------------------------ |
  | `basic_info`            | `object` | Contains detailed information about the queried GO term      |
  | \|-- `id`               | `string` | The ID of the GO term                                        |
  | \|-- `name`             | `string` | The name of the GO term                                      |
  | \|-- `category`         | `string` | The category of the GO term, including `biological_process`, `molecular_function`, and `cellular_component` |
  | \|-- `description`      | `string` | A detailed explanation of the GO term                        |
  | `outgoing_interactions` | `array`  | A list of interactions where the queried GO term relates to other GO terms |
  | \|-- `go_term`          | `string` | The queried GO term ID                                       |
  | \|-- `to_go_term`       | `string` | The target GO term ID that the queried term relates to       |
  | \|-- `interaction_type` | `string` | The type of relationship                                     |
  | `incoming_interactions` | `array`  | A list of interactions where other GO terms relate to the queried GO term |
  | \|-- `go_term`          | `string` | The queried GO term ID                                       |
  | \|-- `from_go_term`     | `string` | The source GO term ID that points to the queried term        |
  | \|-- `interaction_type` | `string` | The type of relationship                                     |

* Error Code

  | HTTP Status Code | Description                                                |
  | ---------------- | ---------------------------------------------------------- |
  | `400`            | The provided GO term ID does not follow the correct format |
  | `404`            | The queried GO term does not exist in the database         |
  | `500`            | Unexpected Error                                           |

* Notes:

  * The GO term can be accepted regardless of case sensitivity or the absence of a colon. The `normalize_go` function ensures that the input is standardized to the format `GO:XXXXXXX`.



#### :old_key: Retrieve protein interaction information and visualization

This API allows users to query interactions for a given protein in a specific species, returning interaction details and an interaction network visualization graph. The interaction details include two interacting proteins, their interaction score, the publications reporting the interaction, and the experimental methods used to discover the interaction.

* Endpoint: `GET /interaction-search`

* Request Parameters:

  | Parameter   | Data Type | Required | Description                                                  |
  | ----------- | --------- | -------- | ------------------------------------------------------------ |
  | `protein`   | `string`  | Yes      | The ID of the protein to query                               |
  | `species`   | `string`  | Yes      | The species name of the queried protein (`E.coli` and `S.cerevisiae` supported) |
  | `min_score` | `float`   | No       | The minimum interaction score threshold (default: `0`)       |

* Example Request URL:

  ```
  http://127.0.0.1:5000/interaction-search?protein=B3317&species=E.coli&min_score=800
  ```

* Response Structure:

  | Field                         | Type     | Description                                                  |
  | ----------------------------- | -------- | ------------------------------------------------------------ |
  | `protein`                     | `string` | The queried protein ID                                       |
  | `species`                     | `string` | The species name of the queried protein                      |
  | `interactions`                | `array`  | List of interaction details                                  |
  | \|-- `protein_a`              | `string` | Protein_a in the interaction found                           |
  | \|-- `protein_b`              | `string` | Protein_b in the interaction found                           |
  | \|-- `interaction_score`      | `float`  | The score of this interaction. The higher, the more reliable |
  | \|-- `validations`            | `array`  | The experimental validations for this interaction            |
  | \| \|-- `experiment_approach` | `string` | The experimental method used for validation                  |
  | \| \|-- `pubmed_id`           | `string` | The PubMed ID of the paper validated this interaction        |
  | `graph_svg`                   | `string` | The interaction network graph in SVG format                  |

* Error Codes

  | HTTP Status Code | Description                                           |
  | ---------------- | ----------------------------------------------------- |
  | `400`            | Invalid species name                                  |
  | `404`            | Invalid protein name or protein not found in database |
  | `500`            | Unexpected error                                      |

* Notes:

  * Case Insensitivity: The letters in protein IDs of E.coli will be automatically normalized to lowercase, while the letters in protein IDs of S.cerevisiae will be automatically normalized to uppercase.

  * Interaction Graph: The `graph_svg` field contains an SVG string representing the interaction network. The graph includes proteins that interact with the query protein, as well as interactions between these proteins. The thickness of the edges represents the interaction score, with thicker edges indicating higher scores. An example is given below:

     <img src="./accessory/ppi_net_example.png" alt="ppi_graph_example" width="50%"> ​

    



### Download API Design :envelope_with_arrow:

Through this API, users can download all interaction data for a specific species (including interacting proteins, scores, literature references, and validation experiments), as well as the GO annotations of the proteins involved in the interactions.

* Endpoint: `GET/download`

* Request Parameters:

  | Parameter | Data Type | Required | Description                                                  |
  | --------- | --------- | -------- | ------------------------------------------------------------ |
  | `species` | `string`  | Yes      | The name of the species. Accepted values are E`.coli` and `S.cerevisiae`. |

* Example Request URL:

  ```
  http://127.0.0.1:5000/download?species=S.cerevisiae
  ```

* Download files:

  Data is given in `.csv` format, including the following columns:

  | protein_a                     | protein_b                     | interaction_score               | experiment_approach                                       | pubmed_id                            | GO_a                       | GO_b                       |
  | ----------------------------- | ----------------------------- | ------------------------------- | --------------------------------------------------------- | ------------------------------------ | -------------------------- | -------------------------- |
  | protein ID in the interaction | protein ID in the interaction | reliability of this interaction | the experiment approach used to validate this interaction | the paper validated this interaction | GO annotation of protein A | GO annotation of protein B |

* Error code:

  | HTTP Status Code | Description                                                  |
  | ---------------- | ------------------------------------------------------------ |
  | `400`            | The `species` parameter is missing or provided in wrong format |
  | `404`            | The requested file does not exist in the server              |
  | `500`            | Unexpected error                                             |

  