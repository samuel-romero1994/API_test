from flask_restx import Api
from .resources import api as items_namespace

def initialize_routes(api: Api):
    api.add_namespace(items_namespace, path='/items')