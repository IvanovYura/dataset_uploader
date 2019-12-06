from flask_restplus import Model
from flask_restplus.fields import Integer, String, List

file = {
    'name': String(required=True),
}

# MODELS

file_create_response_model = Model(
    'File Create Response Model',
    {
        'id': Integer(required=True),
        **file,
    },
)

dataset_request_model = Model(
    'Dataset Request Model', {
        'file_ids': List(Integer, required=True),
    }
)
