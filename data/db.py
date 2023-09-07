from peewee import *
from data.config import CONNECTION_STRING

db = PostgresqlDatabase(CONNECTION_STRING)
db.connect()

