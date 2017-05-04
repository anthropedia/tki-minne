from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from . import db
from .utils import generate_key


class User(db.Document):
    firstname = db.StringField()
    lastname = db.StringField()
    email = db.EmailField(unique=True)
    roles = db.ListField(db.StringField())
    creation_date = db.DateTimeField(default=datetime.datetime.utcnow)
    _password = db.StringField(max_length=255)

    def __init__(self, *args, **kwargs):
        db.Document.__init__(self, *args, **kwargs)
        if 'password' in kwargs:
            self.password = kwargs['password']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

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
    survey = db.StringField(max_length=20, required=True)
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


class Score(db.Document):
    user = db.ReferenceField(User, required=True)
    survey = db.StringField(required=True, max_length=20)
    answers = db.ListField(required=True)
    times = db.ListField()
    creation_date = db.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return ('score of {} on {}'.format(self.user, self.creation_date))
