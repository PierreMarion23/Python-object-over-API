
import os
import logging as logging

import flask
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS

from . import config


logging.getLogger().setLevel(logging.DEBUG)


app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
app.config['TOKEN_KEY'] = config.TOKEN_KEY


# create api
_api = Api(app)

# api endpoints

# Function Request
from .api.function_request import FunctionRequestApi
_api.add_resource(FunctionRequestApi, '/api/function_request', methods=['POST'], endpoint='function_request')

# Module exploration
from .api.exploration import ExplorationApi
_api.add_resource(ExplorationApi, '/api/exploration', methods=['GET'], endpoint='exploration')

@app.after_request
def after_request(response):
    if 'Origin' not in request.headers:
        return response

    approved_origins = ['http://localhost:8888',
                        'http://localhost:8889',
                        ]
    if request.headers['Origin'] in approved_origins:
        response.headers.add('Access-Control-Allow-Origin', request.headers['Origin'])
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        # response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response


logging.info('InitApp')
