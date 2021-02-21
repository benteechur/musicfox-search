# musicfox-search

## NOTE: instructions assume use of bash emulator on Windows.
### For additional environments, see:
[Python](https://docs.python.org/3/tutorial/venv.html)

[Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/)


### Create virtual environment:
```
$ python -m venv .venv
$ source .venv/Scripts/activate
```

### Install packages:

```
$ pip install -r requirements.txt
```

### Run application:

```
$ export FLASK_APP=api.py
$ flask run
```

### Endpoint:

```
localhost:5000/search
```

### Additional Explanation:

#### [Trigrams](https://github.com/benteechur/musicfox-search/blob/main/trigrams.ipynb)
