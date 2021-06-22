import configparser
import psycopg2
from timeit import default_timer as timer
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Copies JSON log and JSON metadata on songs into our 2 staging tables.
    
    Parameters:
    cur - Cursor object that allows for executing SQL commands
    conn - Connection to database instance
    
    Returns:
    Log data into staging_events table
    Songs data into staging_songs table
    
    """
    print("Loading staging tables...")
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Transforms staged data into 5 dimensional tables(songplays, users, artists, songs, time).
    
    Parameters:
    cur - Cursor object that allows for executing SQL commands
    conn - Connection to database instance
    
    Returns:
    Inserts staged log data from staging_events table into dimensional tables
    Inserts staged song data from staging_songs table into 5 dimensionsal tables
    """
    print("Transforming staged log and song data into 5 tables...")
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Connects to Redshift cluster, loads 2 staging tables, gives the time duration for loading the staging tables, transforms the staged data into a set of dimensional tables, and finally closes the connection to the database. 
    
    Parameters:
    None
    
    Returns:
    Time it took to load the staging tables runs queries for loading the staging tables and transforming the staged data into 5 tables.
    
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CREDENTIALS'].values()))
    cur = conn.cursor()
    
    start = timer()
    load_staging_tables(cur, conn)
    end = timer()
    
    print("Loading the staging tables took {} seconds to run".format((end-start)))

    insert_tables(cur, conn)
    print("ETL complete")

    conn.close()


if __name__ == "__main__":
    main()