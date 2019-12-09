from yoyo import step

"""
Create dataset table
"""

SQL_INIT_DB = '''
    CREATE TABLE IF NOT EXISTS dataset (
        id SERIAL,
        name TEXT NOT NULL, 
        created_on timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
        
        file_ids INT[] NOT NULL,
          
        PRIMARY KEY(id)
    );
    
    CREATE UNIQUE INDEX IF NOT EXISTS uniq_dataset_name ON dataset(name);
'''

steps = [
    step(SQL_INIT_DB),
]
