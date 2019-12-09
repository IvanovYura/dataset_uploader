from yoyo import step

"""
Init DB for Skeleton project
"""

SQL_INIT_DB = '''
    CREATE TABLE IF NOT EXISTS file (
        id SERIAL,
        name TEXT NOT NULL,
        created_on timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,  
        
        headers TEXT[] NOT NULL,  
            
        PRIMARY KEY(id)
    );
    
    CREATE UNIQUE INDEX IF NOT EXISTS uniq_file_name ON file(name);
'''

steps = [
    step(SQL_INIT_DB),
]
