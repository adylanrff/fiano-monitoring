import config
from rq import Retry

from datetime import datetime

from flask import Flask, request
from flask_peewee.db import Database

DATABASE = {
    'engine': 'peewee.PostgresqlDatabase',
    'name': 'fiano',
    'user': config.POSTGRES_USER,  # Will be passed directly to psycopg2.
    'password': config.POSTGRES_PASSWORD,  # Ditto.
    'host': config.POSTGRES_HOST,  # Ditto.
}
DEBUG = True
SECRET_KEY = 'ssshhhh'

app = Flask(__name__)
app.config.from_object(__name__)

db = Database(app)
