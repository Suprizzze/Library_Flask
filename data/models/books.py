from peewee import *
from data.db import db

class BaseModel(Model):
    class Meta:
        database = db

class Books(BaseModel):
    id = AutoField(primary_key=True, null=False)
    title = CharField(null=False)
    authors = CharField(null=False)
    year = IntegerField(null=False)
    ISBN = CharField(null=False)
    genre = CharField(null=False)
    url = TextField(null=False)
    image = TextField(null=True)
    about = TextField(null=True)


class BooksCopy(BaseModel):
    id = AutoField(primary_key=True, null=False)
    book = ForeignKeyField(Books, backref='copies')
    state = IntegerField(null=False)
    status = TextField(null=True, default="Free")

    def reserve(self):
        if self.status == "Free":
            self.status = "Busy"
            self.save()
            return True
        else:
            return False

    def reserve_back(self):
        if self.status == "Busy":
            self.status = "Free"
            self.save()
            return True
        else:
            return False


db.create_tables([Books, BooksCopy])
