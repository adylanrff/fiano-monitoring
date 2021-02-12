import config
from peewee import PostgresqlDatabase, Model

db = PostgresqlDatabase(
    config.POSTGRES_DB,
    user=config.POSTGRES_USER,  # Will be passed directly to psycopg2.
    password=config.POSTGRES_PASSWORD,  # Ditto.
    host=config.POSTGRES_HOST,  # Ditto.
)

class BaseModel(Model):
    class Meta:
        database = db

