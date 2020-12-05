# Using a Global Corporations Knowledge Graph to Predict Mergers and Acquisitions

## Project Description
Currently developing a Knowledge GraphDB with ~50k global corporations. Data extracted using SPARQL to query WikiData, WikiMedia’s massive Semantic Triplestore (~91m triples). Example Schema: (Company)--[size, location, industry]--(Company). Goal is to predict Mergers and Acquisitions using link prediction ML algorithms from metadata and graph embeddings (Node2Vec). Example prediction: (Company)--[ACQUIRED]--(Company)

## Project Status
- [x] Write Wikidata Sparql Queries for global corporations and corp-to-corp acquisition relationships
- [x] Build/Run extraction and cleaning of data using Wikidata API
- [x] Build/Run ETL process to prepare CSVs for Neo4j GraphDB Node and Edge Ingestion
- [x] Run actual ingestion with pre-processed data
- [-] Inspect and verify ingestion
- [ ] Peform Graph analytics exploratory data analysis (still important for ML even in Graph!)
- [ ] Test Graph Database embedding models and research more graph native link prediction algos
- [ ] Formalize ML approach and record performance
- [ ] Clean repo and publish project

## Project Tools
- Python
  - sparql_config
  - Pandas
  - JSON
  - MultiThreading
  - NetworkX
  - TensorFlow
  - Sklearn
  - Plotly
- Neo4j
  - Cypher
- Docker base images
  - Neo4j
- Sparql
- Wikidata

## Publication
- [Not Published yet](keenanvenuti.com/projects)

## Installation and Running (not ready yet)
```sh
git clone git.repo.com
```
```sh
python installation
```
