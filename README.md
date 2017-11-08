# FASH
FASH is a scavenger hunt tracker for MIT ATS's Fall Asyncrhonous Scavenger Hunt (FASH).

## Getting Started
Install all the requirements:
```
pip install -r requirements.txt
```
Configure `config.py` and `constants.py` (see configuration for details).

Start the server:
```
python runapp.py
```

## Configuration
Both `config.py` and `constants.py` live in the `/fash` folder.
`config.py` includes information used to set admins and OIDC. Below is an example:
```
CLIENT_ID = ""
CLIENT_SECRET = ""
CLIENT_CONFIG_URL = ""

REGISTRATION_AT = ""

ADMINS = set([
    'jynnie@mit.edu',
    ])
```

`constants.py` includes information regarding the domain and port. Below is an example:
```
PORT = 80

DEBUG = True

DOMAIN = 'http://localhost'

SECRET = 'wellicanttellunowcani'
```

## Notes
Thanks to [Shreyas](http://github.com/revalo) for help in setting up structure and setting up OIDC.
