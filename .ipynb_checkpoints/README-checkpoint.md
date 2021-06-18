# Project 3 - Building an ETL pipeline
The goal for this project is to build an ETL pipeline that extracts JSON logs and metadata from S3 buckets, stages them in Redshift, and transforms the staged data into a set of dimensional tables that can be queried for insights on users
---

## Project Files
### dwh.cfg
    - Provides credentials, S3 bucket location, and defines cluster nodes

### sql_queries.py
SQL queries for:
    - Dropping staging and dimension tables
    - Creating staging and dimension tables
    - Copying log and song data from S3 bucket into 2 staging tables
    - Inserts stage table data into dimension tables

### create_tables.py
    - Idempotent script which connects to Redshift cluster, deletes staging and dimension tables if they exist and then creates the staging tables and dimension tables
    
### etl.py
    - Loads 2 staging tables for log data and song data and transforms the staged data into 5 dimension tables: songplays, users, songs, artists, and time
    
### redshift_cluster_setup.ipynb
    - Creates Redshift cluster and creates a connection for querying
    
---
## How To Run Project
1. Run the cells in `redshift_cluster_setup.ipynb` to create the Redshift cluster and connect to it
2. Run `create_tables.py` to create staging and dimension tables
3. Run `etl.py` to load the staging tables and transform the data into the 5 dimension tables
4. Test data quality

---
## 1. Run create_tables.py
Run `python3 create_tables.py` in terminal


## Redshift Configuration and Setup
---
### Config File
The config file is `dwh.cfg` which stores credentials, cluster information, data location, and AWS access ids.

### Redshift Setup
Run the cells in `redshift_cluster_setup.ipynb` to:
1. Create IAM Role
2. Create a Redshift cluster of 4 dc2.large nodes
3. Connect to the cluster

<em>Remember to run the clean up cells at the bottom of the notebook to avoid a massive bill :)</em>
---
## Data Quality Check
Great Expectations(GE) is a Python library that allows for testing data, detecting data quality issues, and document ingested data.
GE takes assertions on the data (Expectations) that can are then used to validate data in a pass or fail test.

### Install Great Expectations and Initialize a Data Context
* Run the following in the command line to install
`pip install great_expectations`

* Run the following command to create a Data Context (select yes when asked to create a new directory)
`great_expectations init`

### Configure Redshift Datasource
The following steps can all be found here: https://docs.greatexpectations.io/en/latest/guides/how_to_guides/configuring_datasources/how_to_configure_a_redshift_datasource.html

1. Install the following modules to use a Redshift datasource:
`pip install sqlalchemy`
`pip install psycopg2`
or
`pip install psycopg2-binary` #for macOS
2. Run datasource new: `great_expectations datasource new`
3. Choose "Relational database (SQL)"
4. Choose Redshift
5. Give the Datasource a name
6. Provide Redshift credentials 
7. Save configuration after connection to database is established

---
## 