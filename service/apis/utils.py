from typing import List

from flask_restplus import Model, Namespace


def register_models(namespace: Namespace, models: List[Model]):
    """
    Registers models for a given namespace
    """
    for model in models:
        namespace.models[model.name] = model
