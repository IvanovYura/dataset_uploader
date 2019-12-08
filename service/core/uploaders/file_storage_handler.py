import os

from flask_restplus import abort
from werkzeug.exceptions import BadRequest

from config import config
from service.core.queries import (
    create_file_entry,
    delete_file_entry,
    create_dataset_entries,
)


class FileStorageHandler:
    def __init__(self):
        self.directory_path = config.STORAGE_DIRECTORY
        self.chunk_size = 1024  # 1MB

    def save_file(self, file_name: str, data) -> dict:
        """
        Saves the file to specified directory and returns its id

        It also creates entry in file table in DB

        Returns JSON serializable object
        """
        # I assume that directory does not exist from the beginning
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path)

        try:
            result = create_file_entry(file_name)
            with open(os.path.join(self.directory_path, f'{file_name}'), "wb") as fp:
                while True:
                    chunk = data.read(self.chunk_size)
                    if not chunk:
                        break

                    fp.write(chunk)

            # if file was added to the the storage and there is no Exception,
            # returns its id and name
            return result

        except ValueError:
            abort(409, f'File with name {file_name} already exists')

        # if there is any other problem send 400 error
        except Exception as e:
            raise BadRequest(f'Something went wrong: {str(e)}')

    def delete_file(self, file_id: int):
        """
        Deletes file from storage and from file table in DB

        Ideally both file and its id should be in the same place/storage
        """
        result = delete_file_entry(file_id)
        if not result:
            abort(404, 'File not found')

        file_name = result['name']
        file_path = os.path.join(self.directory_path, f'{file_name}')

        try:
            os.remove(file_path)
        # in case there is inconsistency between DB and storage
        except OSError:
            raise BadRequest(f'File {file_name} you are trying to delete does not exist in storage')

    def create_dataset(self, payload: dict) -> int:
        # get headers of al of them
        # if headers are the same -> proceed
        # if not -> 400

        # if OK -> create a new file and write there line by line from each file

        foo = config.PROJECT_DIR
        ids = payload['file_ids']

        for file_id in ids:
            file_name = get_file_name(file_id)
            # _csv_to_json(directory_path, file_name)

        result = create_dataset_entries(payload)

        return result['id']
