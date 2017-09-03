
import os
import logging as logging

import flask
from flask import Flask, request
from flask_restful import Api


logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config['DEBUG'] = True


# create api
_api = Api(app)

# api endpoints

# Function Request
from .api.function_request import FunctionRequestApi
_api.add_resource(FunctionRequestApi, '/api/function_request', methods=['POST'], endpoint='function_request')

# Module exploration
from .api.exploration import ExplorationApi
_api.add_resource(ExplorationApi, '/api/exploration', methods=['GET'], endpoint='exploration')

logging.info('InitApp')
