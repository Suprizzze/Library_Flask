from peewee import *
from data.db import db


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = AutoField(primary_key=True, null=False)
    login = CharField(max_length=20, unique=False, null=False)
    email = CharField(max_length=120, unique=False, null=False)
    psw = TextField(null=False)
    user_status = CharField(max_length=40, null=True, default='The best user')


db.create_tables([User])