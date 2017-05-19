from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from . import db
from .utils import generate_key


class Client(db.Document):
    reference = db.StringField(max_length=50)
    firstname = db.StringField(max_length=50)
    middlename = db.StringField(max_length=50)
    lastname = db.StringField(max_length=50, required=True)
    email = db.EmailField(unique=True)
    culture = db.StringField(max_length=2)
    note = db.StringField()

    def __str__(self):
        if self.firstname and self.lastname:
            return '{} {}'.format(self.firstname, self.lastname)
        return self.lastname


class ProfessionalProfile(db.EmbeddedDocument):
    clients = db.ListField(db.ReferenceField(Client))


class User(db.Document):
    firstname = db.StringField()
    lastname = db.StringField()
    email = db.EmailField(unique=True)
    roles = db.ListField(db.StringField())
    creation_date = db.DateTimeField(default=datetime.datetime.utcnow)
    _password = db.StringField(max_length=255)
    professional_profile = db.EmbeddedDocumentField(ProfessionalProfile)

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


class BaseToken:
    key = db.StringField(min_length=32, max_length=32, unique=True,
                         required=True)
    survey = db.StringField(max_length=20, required=True)
    creation_date = db.DateTimeField(default=datetime.datetime.utcnow)
    usage_date = db.DateTimeField()

    def __str__(self):
        return str(self.key)

    @property
    def is_valid(self):
        return self.usage_date is None

    def get_user_field(self):
        return self.user

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
            self.key = generate_key('{}{}'.format(
                                    self.get_user_field().id,
                                    self.creation_date.timestamp()))
        return super(BaseToken, self).save(*args, **kwargs)


class SurveyToken(BaseToken, db.Document):
    client = db.ReferenceField(Client, required=True)
    provider = db.ReferenceField(User, required=True)

    def get_user_field(self):
        return self.client


class ResearchToken(BaseToken, db.Document):
    user = db.ReferenceField(User, required=True)
    name = db.StringField(max_length=100)
    comment = db.StringField()


class Score(db.Document):
    user = db.ReferenceField(User, required=True)
    survey = db.StringField(required=True, max_length=20)
    answers = db.ListField(required=True)
    times = db.ListField()
    creation_date = db.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return ('score of {} on {}'.format(self.user, self.creation_date))
