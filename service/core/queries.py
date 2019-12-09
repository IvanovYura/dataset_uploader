from typing import List

from psycopg2.errors import UniqueViolation

from service.core.database import conn, get_dict_cursor

SQL_GET_FILES = '''
    SELECT name, headers
    FROM file
    WHERE id IN %(file_ids)s;
'''

SQL_CREATE_FILE = '''
    INSERT INTO file (
        name,
        headers
    )
    VALUES (
        %(name)s,
        %(headers)s  
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
        name,
        file_ids
    )
    VALUES
    (
        %(name)s,
        %(file_ids)s
    )
    RETURNING id, name;
'''


def create_file_entry(file_name: str, headers: list) -> dict:
    """
    Creates entry in file table

    Raise value error if resource with this name already exists
    """
    with get_dict_cursor(conn) as cursor:
        try:
            cursor.execute(SQL_CREATE_FILE, {'name': file_name, 'headers': headers})

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


def create_dataset_entries(file_ids: List[int]):
    with get_dict_cursor(conn) as cursor:
        dataset_name = _generate_dataset_name(file_ids)
        try:
            cursor.execute(
                SQL_CREATE_DATSASET_ENTRY,
                {
                    'name': dataset_name,
                    'file_ids': file_ids,
                })
        except UniqueViolation:
            raise ValueError(f'Dataset with the name={dataset_name} already exists.')

        conn.commit()
        return cursor.fetchone()


def _generate_dataset_name(file_ids: List[int]):
    # if ids = [1, 2, 3], dataset name will be files_1_2_3
    ids = '_'.join(map(str, file_ids))
    return f'files_{ids}'


def get_files(file_ids: List[int]):
    with get_dict_cursor(conn) as cursor:
        cursor.execute(
            SQL_GET_FILES,
            {
                'file_ids': tuple(file_ids),
            })
        return cursor.fetchall()
