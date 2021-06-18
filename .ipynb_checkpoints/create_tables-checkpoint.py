import configparser
import psycopg2
import boto3
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops existing tables in the sparkify database for idempotency.
    
    Parameters:
    cur - Cursor object that allows for executing SQL commands
    conn - Connection to database instance
    
    Returns:
    Drops staging tables and dimension tables if they exist within the Redshift cluster.
    """
    print("Dropping tables")
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates our 2 staging tables and a set of 5 dimension tables.
    
    Parameters:
    cur - Cursor object that allows for executing SQL commands
    conn - Connection to database instance
    
    Returns:
    Creates staging tables for our log and song data and 5 dimension tables.
    """
    print("Creating tables")
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Connects to the Redshift cluster, drops any existing tables, and creates our staging and dimensional tables.
    
    Parameters:
    None
    
    Returns:
    Drops existing tables and creates tables for staging data and dimension tables.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CREDENTIALS'].values()))
    cur = conn.cursor()

    print("Running drop_tables and create_tables")
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()