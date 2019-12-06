from flask import request, current_app
from flask_restplus import Namespace, Resource
from werkzeug.datastructures import FileStorage

from service.apis.utils import register_models
from service.core.models import file_create_response_model, dataset_request_model
from service.core.uploaders.file_storage_handler import FileStorageHandler

namespace = Namespace(
    name='Skeleton',
    description='Namespace for CRUD',
    path='/',
)

# register namespace models
register_models(namespace, [
    file_create_response_model,
    dataset_request_model,
])

parser = namespace.parser()

parser.add_argument('csv_file',
                    type=FileStorage,
                    location='files',
                    required=True,
                    help='File to upload',
                    )

uploader = FileStorageHandler()


@namespace.route('/file')
class FilesApi(Resource):
    @namespace.response(201, 'Created')
    # unique violation
    @namespace.response(409, 'File already exists')
    @namespace.expect(parser, validate=True)
    @namespace.marshal_with(file_create_response_model)
    def post(self):
        args = parser.parse_args()
        file = args['csv_file']
        data_stream = request.data

        result = uploader.save_file(file.filename, data_stream)

        return result, 201


@namespace.route('/file/<int:file_id>')
@namespace.doc(
    params={
        'resource_id': 'Resource ID',
    }
)
class FileApi(Resource):
    @namespace.response(204, 'No Content')
    @namespace.response(404, 'File Not Found')
    def delete(self, file_id: int):
        """
        Deletes file

        If file to delete not found, returns 404
        """
        uploader.delete_file(file_id)

        return None, 204


@namespace.route('/dataset')
class DatasetApi(Resource):
    @namespace.response(201, 'Created')
    # unique violation
    @namespace.response(409, 'Dataset already exists')
    @namespace.expect(dataset_request_model, validate=True)
    def post(self):
        payload = namespace.payload

        result = uploader.create_dataset(payload)

        return result, 201
