import datetime

from werkzeug.security import gen_salt

from . import db


class Client(db.Document):
    name = db.StringField(required=True)
    reference = db.StringField()
    language = db.StringField(default='en', max_length=2)
    comment = db.StringField()
    creation_date = db.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return self.name

    meta = {'ordering': ['-creation_date', 'name']}


class Token(db.Document):
    client = db.ReferenceField(Client, reverse_delete_rule=db.CASCADE)
    key = db.StringField(min_length=8, max_length=8, unique=True,
                         required=True)
    provider = db.StringField(required=True)
    creation_date = db.DateTimeField(default=datetime.datetime.utcnow)
    usage_date = db.DateTimeField()

    def __str__(self):
        return self.key

    meta = {'ordering': ['-creation_date']}

    def void(self):
        self.usage_date = datetime.datetime.utcnow()
        self.save()

    def is_valid(self):
        return self.usage_date is None

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = gen_salt(8)
        return super().save(*args, **kwargs)


class Score(db.Document):
    token = db.ReferenceField(Token, reverse_delete_rule=db.NULLIFY)
    client = db.ReferenceField(Client, reverse_delete_rule=db.NULLIFY)
    answers = db.ListField(required=True)
    times = db.ListField()
    creation_date = db.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return f'{self.client} on {self.creation_date}'

    meta = {'ordering': ['-creation_date']}


def drop_all():
    Score.drop_collection()
    Client.drop_collection()
    Token.drop_collection()
