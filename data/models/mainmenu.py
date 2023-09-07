from peewee import *
from data.db import db


class BaseModel(Model):
    class Meta:
        database = db


class Mainmenu(BaseModel):
    id = IntegerField(primary_key=True, null=False)
    title = CharField(null=False)
    url = CharField(null=False)


class Mainmenu_admin(BaseModel):
    id = IntegerField(primary_key=True, null=False)
    title = CharField(null=False)
    url = CharField(null=False)


class Mainmenu_admin_lower(BaseModel):
    id = IntegerField(primary_key=True, null=False)
    title = CharField(null=False)
    url = CharField(null=False)


if __name__ == "__main__":
    db.create_tables([Mainmenu, Mainmenu_admin, Mainmenu_admin_lower])