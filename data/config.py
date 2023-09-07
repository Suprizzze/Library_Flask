from os import environ
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DATABASE_HOST = environ["DATABASE_HOST"]
DATABASE_PORT = environ["DATABASE_PORT"]
DATABASE_USER = environ["DATABASE_USER"]
DATABASE_PASS = environ["DATABASE_PASS"]
DATABASE_NAME = environ["DATABASE_NAME"]

CONNECTION_STRING = f"postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}/{DATABASE_NAME}"

