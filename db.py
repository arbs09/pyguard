import sqlite3
import re

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

def check_db():
    print("Checking database schema...")
    connection = get_db_connection()
    cursor = connection.cursor()
    with open('schema.sql', 'r') as file:
        schema = file.read()
    
    table_names = re.findall(r'CREATE TABLE (\w+)', schema)
    
    for table_name in table_names:
        cursor.execute(f'SELECT name FROM sqlite_master WHERE type="table" AND name="{table_name}"')
        if cursor.fetchone() is None:
            raise Exception(f"Table {table_name} does not exist in the database.")
    
    return "Database schema is correct."
