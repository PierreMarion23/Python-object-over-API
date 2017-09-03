# Object over API for Python

## Overview

This is a small project to pass objects over APIs in Python.   
The context is an architecture that requires a client-server setup, with both the client and the server being Python scripts.

The API is a RestFul API based on Python Flask.

IMPORTANT: Both server and client (notebook here) must share the **exact same environment**. Why ? Because the objects are pickled / un-pickled on both sides of the API. This operation may fail if the Python and/or libraries versions are not the same.

## Install and run

### 1 - Create environment

On Windows:

```bat
REM create conda env
conda env create -f conda_env.yaml

REM create env
conda create -n object-over-api python=3

REM activate env
activate object-over-api

REM instal packages with conda
conda install -y flask

REM instal packages with pip
pip install flask-restful

REM export env to file - for easier subsequent creation
conda env export > conda_env.yml

REM to create env from file - if necessary
REM conda env create -f conda_env.yml

REM deactivate env
deactivate
```

On Linux / macOS:

```bash
# create conda env
conda env create -f conda_env.yaml

# create env
conda create -n object-over-api python=3

# activate env
source activate object-over-api

# instal packages with conda
conda install -y flask

# instal packages with pip
pip install flask-restful

# export env to file - for easier subsequent creation
conda env export > conda_env.yml

# to create env from file - if necessary
# conda env create -f conda_env.yml

# deactivate env
source deactivate
```

### 2 - Make environment available to Jupyter

From outside the environment created above:

```bash
python -m ipykernel install --user --name object-over-api --display-name "Python object-over-api"
```

### 3 - Run

Launch the server.

On Windows:

```bat
REM activate env
activate activate object-over-api

REM run server
python main_module/run.py
```

On Linux / macOS:

```bash
# activate env
source activate activate object-over-api

# run server
python main_module/run.py
```

Launch [Jupyter](http://jupyter.org/):
```bash
jupyter notebook
```

Run the [demo notebook](http://nbviewer.jupyter.org/github/PierreMarion23/Python-object-over-API/blob/master/demo_Python-object-over-API.ipynb).  
There should be enough comments and prints to understand what is going on.  
Read the server logs too. It is verbose.
