from yoyo import step

"""
Create dataset table
"""

SQL_INIT_DB = '''
    CREATE TABLE IF NOT EXISTS dataset (
        id SERIAL,
        dataset 

        PRIMARY KEY(id)
    );
'''

steps = [
    step(SQL_INIT_DB),
]
