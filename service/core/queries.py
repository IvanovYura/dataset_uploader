from psycopg2.errors import UniqueViolation

from service.core.database import conn, get_dict_cursor

SQL_GET_FILE = '''
    SELECT name
    FROM file
    WHERE
    id = %(file_id)s;
'''

SQL_CREATE_FILE = '''
    INSERT INTO file (
        name
    )
    VALUES (
        %(name)s    
    )
    RETURNING id, name;
'''

SQL_DELETE_FILE = '''
    DELETE FROM file
    WHERE
        id = %(file_id)s
    RETURNING name;
'''

SQL_CREATE_DATSASET_ENTRY = '''
    INSERT INTO dataset (
        dataset
    )
    VALUES
    (
        %(dataset)s
    )
    RETURNING id;
'''


def create_file_entry(file_name: str) -> dict:
    """
    Creates entry in file table

    Raise value error if resource with this name already exists
    """
    with get_dict_cursor(conn) as cursor:
        try:
            cursor.execute(SQL_CREATE_FILE, {'name': file_name})

        except UniqueViolation:
            raise ValueError(f'File with the name={file_name} already exists.')

        conn.commit()
        return cursor.fetchone()


def delete_file_entry(file_id: int):
    """
    Deletes file by its id
    """
    with get_dict_cursor(conn) as cursor:
        cursor.execute(
            SQL_DELETE_FILE,
            {
                'file_id': file_id,
            })

        # if it is successful then commit
        if cursor.rowcount:
            conn.commit()
            return cursor.fetchone()

        # nothing to return, because nothing to delete
        return None


def create_dataset_entries(dataset: dict):
    with get_dict_cursor(conn) as cursor:
        cursor.execute(
            SQL_CREATE_DATSASET_ENTRY,
            {
                'dataset': dataset,
            })
        conn.commit()
        return cursor.fetchone()


def get_file_name(file_id: int):
    with get_dict_cursor(conn) as cursor:
        cursor.execute(
            SQL_GET_FILE,
            {
                'file_id': file_id,
            })
        return cursor.fetchone()
