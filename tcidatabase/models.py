import datetime

from . import db
from .utils import generate_key


class User(db.Document):
    firstname = db.StringField()
    lastname = db.StringField()
    email = db.EmailField()
    roles = db.ListField(db.StringField())
    creation_date = db.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        if self.firstname and self.lastname:
            return '{} {}'.format(self.firstname, self.lastname)
        elif self.email:
            return self.email
        return 'user {}'.format(self.id)


class Token(db.Document):
    user = db.ReferenceField(User, required=True)
    key = db.StringField(min_length=32, max_length=32, unique=True,
                         required=True)
    name = db.StringField(max_length=100)
    comment = db.StringField()
    creation_date = db.DateTimeField(default=datetime.datetime.utcnow)
    usage_date = db.DateTimeField()

    def __str__(self):
        return str(self.key)

    @property
    def is_valid(self):
        return self.usage_date is None

    @property
    def is_dummy(self):
        return not bool(self.key)

    def void(self):
        self.usage_date = datetime.datetime.utcnow()
        self.save()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.utcnow()
        if not self.key:
            self.key = generate_key('{}{}'.format(self.user.id,
                                    self.creation_date.timestamp()))
        return super(Token, self).save(*args, **kwargs)
