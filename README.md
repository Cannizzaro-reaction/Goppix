# Protein-Protein Interaction Network and Functional Annotation Database

写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出写不出啊啊啊啊啊啊啊啊



## :microscope: ​Introduction

pass



## :wrench: Installation

pass



## :computer: ​Back-end

### Database Design :card_file_box: 

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



### API Design​ :mag_right:

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

  | Field        | Type     | Description                                             |
  | ------------ | -------- | ------------------------------------------------------- |
  | `basic_info` | `object` | Contains detailed information about the queried GO term |
  | \|-- `id`    | `string` |                                                         |
  |              | `string` |                                                         |
  |              | `string` |                                                         |
  |              |          |                                                         |
  |              |          |                                                         |
  |              |          |                                                         |
  |              |          |                                                         |
  |              |          |                                                         |
  |              |          |                                                         |
  |              |          |                                                         |
  |              |          |                                                         |
  |              |          |                                                         |

  



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

    

