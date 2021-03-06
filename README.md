# Hatchways Backend Assessment

## Flask REST API

### Run API with Flask's Server

To utilize Flask's server run the following commands in Bash/Zsh

#### Create and activate a Python virtual environment

```console
python3 -m venv venv
source venv/bin/activate
```

#### Install development requirements

```console
pip install -r requirements.txt
```

#### Alternatively, install minimal requirements

```console
pip install -e .
```

#### Run Flask server

```console
export FLASK_APP=blog_api
flask run
```

#### Run tests

```console
pytest
```

#### Get test coverage report as HTML

```console
coverage run -m pytest
coverage html
```

#### Get a Python Wheel built for distribution

```console
python setup.py bdist_wheel
```

### Package Layout

I am following [Flask](https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/)'s documentation about package layout.
