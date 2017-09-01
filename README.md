# Object over API for Python

This repo is a small project to pass objects over APIs in Python. The context is an architecture that requires a client-server setup, with both the client and the server being Python scripts.

The API is a RestFul API based on Python Flask.

## Install and run

```bat
REM to create conda env:
conda env create -f conda_env.yaml

cd main_module
activate object-over-api
python run.py
```

Then you can run the notebook. To be on the safe side, it's advised to run the notebook from the same environment as the server. Why ? Because the objects are pickled / unpickled on both sides of the API. This operation may fail if the versions of Python libraries are not the same on both sides.

To add your newly created env to Jupyter env list:

```bat
activate object-over-api
pip install ipykernel
python -m ipykernel install --user --name object-over-api --display-name "Python object-over-api"
```