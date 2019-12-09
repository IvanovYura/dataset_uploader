import os

from flask_restplus import abort
from werkzeug.exceptions import BadRequest

from config import config
from service.core.queries import (
    create_file_entry,
    delete_file_entry,
    create_dataset_entries,
    get_files,
)


class FileStorageHandler:
    def __init__(self):
        self.storage_directory = config.STORAGE_DIRECTORY
        self.chunk_size = 1024  # 1MB

    def save_file(self, file_name: str, data) -> dict:
        """
        Saves the file to specified directory and returns its id

        It also creates entry in file table in DB

        Returns JSON serializable object
        """
        # I assume that directory does not exist from the beginning
        if not os.path.exists(self.storage_directory):
            os.makedirs(self.storage_directory)

        try:
            # reads the first line
            first_line = data.readline()
            # we pray encoding is utf-8
            headers = first_line.decode('utf-8').rstrip().split(',')

            result = create_file_entry(file_name, headers)
            with open(os.path.join(self.storage_directory, file_name), 'wb') as fp:
                fp.write(first_line)

                while True:
                    chunk = data.read(self.chunk_size)
                    if not chunk:
                        break

                    fp.write(chunk)

            # if file was added to the the storage and there is no Exception,
            # returns its id and name
            return result

        # TODO: should be a custom exception with its own code to respond
        except ValueError as e:
            abort(409, str(e))

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
        file_path = os.path.join(self.storage_directory, file_name)

        try:
            os.remove(file_path)
        # in case there is inconsistency between DB and storage
        except OSError:
            raise BadRequest(f'File {file_name} you are trying to delete does not exist in storage')

    def create_dataset(self, payload: dict) -> int:
        ids = payload['file_ids']
        files = get_files(ids)

        if not files:
            raise BadRequest(f'There are no CSV files for specified ids: {ids}')

        headers = self._get_headers_or_400(files)

        try:
            result = create_dataset_entries(ids)

            # if it is possible to create dataset with provided files,
            # create the target directory first
            target_path = os.path.join(self.storage_directory, 'concatenated')

            if not os.path.exists(target_path):
                os.makedirs(target_path)

            with open(os.path.join(target_path, result['name']), 'a') as fp:
                # write headers to concatenated dataset first
                fp.write(f"{','.join(headers)}\n")

                for file in files:
                    file_path = os.path.join(self.storage_directory, file['name'])
                    with open(file_path, 'r') as cfp:  # current file placeholder
                        # skip header of each file
                        next(cfp)

                        while True:
                            chunk = cfp.read(self.chunk_size)
                            if not chunk:
                                break

                            fp.write(chunk)

                    # terminate the last line of file by default terminator
                    fp.write('\n')

            return result['id']

        except ValueError as e:
            abort(409, str(e))

    @staticmethod
    def _get_headers_or_400(files: dict):
        """
        Returns headers for files (one or more) if they are the same (if more than one)

        Otherwise raise 400 error
        """
        headers = files[0]['headers']

        for i in range(1, len(files)):
            current_headers = files[i]['headers']

            if headers != current_headers:
                raise BadRequest('There are not all CSV files have the same headers')

            headers = current_headers

        return headers
