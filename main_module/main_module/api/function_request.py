import flask
import pickle
import os
import json
from flask import request
from flask_restful import Resource

from importlib import import_module


class FunctionRequestApi(Resource):
    '''
    Execute a local function with args passed through the API.

    Three cases are dealt with:
        - the user wants to execute a function ;
        - the user wants to create an object from a class (execute the __init__ method). In this case, the object is created
        locally, and then its __dict__ and its methods' signatures are returned through the API
        - the user wants to execute a class method. In this case, an instance of the class is created locally.
        The attributes of this object are populated thanks to the remote object's __dict__, which is passed through the API.
        Then the method is executed ; if any result is returned by the method, it is also returned through the API. The method
        may also modify the object in-place, thus the object's __dict__ is also returned through the API.
    Thus the API only works if it's able to pickle the object's __dict__. Therefore if any attribute from the object is unpicklable,
    it cannot be passed through the API and must be manually modified or removed before pickling.
    '''

    def post(self):
        request_json = pickle.loads(request.data)
        module_name = request_json['module']
        function_name = request_json['function']
        method_name = request_json['method'] if 'method' in request_json else None
        function_args = request_json['args']

        print(module_name)
        print(function_name)
        if method_name:
            print(method_name)
        print(function_args)

        current_path = os.path.dirname(os.path.abspath(__file__))
        json_path = current_path.replace('api', 'structure.json')
        with open(json_path) as json_data:
            structure_json = json.load(json_data)

        if not method_name:     # a function is called, not a class method called from an instance
            module = import_module(module_name)
            function = getattr(module, function_name)
            function_result = function(**function_args)

            if (__name__.split('.')[0] in str(type(function_result))):   # the function was actually an __init__ of a class
                
                dic = function_result.__dict__
                upper_module, lower_module = module_name.split('.')[1:]
                methods = structure_json[upper_module][lower_module][function_name]
                result = {'_dic':dic, 'methods':methods}    # we return the necessary information to construct the corresponding object
                status_code = 201
            else:
                result = function_result
                status_code = 200

        else:   # a class method has been called from within a class instance
            module = import_module(module_name)
            Class = getattr(module, function_name)
            instance = Class.__new__(Class)
            instance.__dict__ = function_args.pop('_dic')

            if hasattr(instance, method_name):
                print('executing ' + method_name)
                try:
                    method_result = getattr(instance, method_name)(**function_args)
                except Exception as e:
                    print(traceback.format_exc())
                    return {'error': e.args[0]}, 521
                
                # upper_module, lower_module = module_name.split('.')[1:]
                # methods = structure_json[upper_module][lower_module][function_name]
                result = {'method_result':method_result, '_dic':instance.__dict__}
                # we return the necessary information to construct the corresponding object, and the method result, if any.
                status_code = 202
            else:
                return {'msg': 'Not a correct method name'}, 400

        payload2 = pickle.dumps(result, pickle.HIGHEST_PROTOCOL)
        response = flask.make_response(payload2)
        response.headers['content-type'] = 'application/octet-stream'
        response.status_code = status_code
        return response