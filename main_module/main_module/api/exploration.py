import os
import json
import flask
from flask import request
from flask_restful import Resource
import inspect
from importlib import import_module
from glob import glob


def construct_dic_file(file):
    '''Return a dict describing the structure of the file - both functions and classes.'''

    lis_class = {}      # list of the classes contained in the file
    lis_function = {}   # list of the functions contained in the file
    for (name, member) in inspect.getmembers(file):
        if inspect.isclass(member):
            lis_class[name] = member
        if inspect.isfunction(member):
            lis_function[name] = member

    dic_file = {}
    
    for class_name, Class in lis_class.items():
        dic_class = {}
        for name, member in inspect.getmembers(Class):
            if inspect.isfunction(member):
                sig = inspect.signature(member)
                list_of_args = str(sig)[1:-1].replace(' ', '').split(',')
                list_of_args.remove('self')
                dic_class[name] = list_of_args
        dic_file[class_name] = dic_class

    for function_name, function in lis_function.items():
        sig = inspect.signature(function)
        list_of_args = str(sig)[1:-1].replace(' ', '').split(',')
        dic_file[function_name] = list_of_args

    return dic_file



def construct_dic_outer_module():
    '''Return a dict describing the structure of the whole module.'''

    paths = glob('*/*/*.py')
    dic_outer_module = {}
    for path in paths:
        if os.sep + 'api' + os.sep not in path:   # we don't want to include the api module in the structure
            file_path = path.replace(os.sep, '.')
            _, inner_module, file_name, _ = file_path.split('.')
            if inner_module not in dic_outer_module:
                dic_outer_module[inner_module] = {}
            dic_inner_module = dic_outer_module[inner_module]
            file = import_module(file_path[:-3])
            dic_file = construct_dic_file(file)
            if len(dic_file) > 0:   # if the file is not empty
                dic_inner_module[file_name] = dic_file
    return dic_outer_module


class ExplorationApi(Resource):
    '''
    Return a JSON containing the structure of the submodules.

    If the JSON is not available, it is built.
    If you update manually the JSON, you have to respect the following rules:
        - no space before and after the = sign
        - if **kwargs is present, must be the last element of its list
    '''

    def get(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        json_path = current_path.replace('api', 'structure.json')

        if os.path.exists(json_path):
            with open(json_path) as json_data:
                d = json.load(json_data)
            return d, 200
        
        else:
            # we construct the json.
            d = construct_dic_outer_module()
            s = json.dumps(d, indent=2)
            with open(json_path, 'w') as f:
                f.write(s)
            return d, 200