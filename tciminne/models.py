import datetime

from werkzeug.security import gen_salt

from core import db


class Client(db.Document):
    reference = db.StringField(unique=True)

    def __str__(self):
        return self.reference


class Token(db.Document):
    client = db.ReferenceField(Client)
    key = db.StringField(min_length=8, max_length=8, unique=True,
                         required=True)
    creation_date = db.DateTimeField(default=datetime.datetime.utcnow)
    provider = db.StringField()
    usage_date = db.DateTimeField()

    def __str__(self):
        return self.key

    def void(self):
        self.usage_date = datetime.datetime.utcnow()
        self.save()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = gen_salt(8)
        return super().save(*args, **kwargs)


class Score(db.Document):
    answers = db.ListField()
    times = db.ListField()
    token = db.ReferenceField(Token)
