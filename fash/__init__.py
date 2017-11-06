from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os, datetime
import fash.config as config
import fash.models

app = Flask(__name__)
app.config.from_object(__name__)

engine = create_engine('sqlite:///fash.db', echo=False)

import fash.controllers # registers controllers
