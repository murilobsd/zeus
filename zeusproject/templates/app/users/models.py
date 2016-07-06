# -*- coding: utf-8 -*-
"""
    {{NAMEPROJECT}}.users.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    {{NAME}} user models module

    :copyright: (c) {{YEAR}} by {{AUTHOR}}.
    :license: BSD, see LICENSE for more details.
"""
from flask import current_app

from flask_security import UserMixin, RoleMixin


from mongoengine import *
from mongoengine import signals
from mongoengine import fields

from {{NAMEPROJECT}}.extensions import db


class Role(db.Document, RoleMixin):
    """Roles."""
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class Address(db.EmbeddedDocument):
    """ endereco usuario """
    tipo = db.StringField()
    endereco = db.StringField()
    cidade = db.StringField()
    estado = db.StringField()
    bairro = db.StringField()
    complemento = db.StringField()
    cep = db.StringField()
    numero = db.StringField()


class User(db.Document, UserMixin):
    """User."""
    email = db.StringField(max_length=255)
    fullname = db.StringField()
    username = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=False)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    current_login_at = db.DateTimeField()
    current_login_ip = db.StringField()
    last_login_at = db.DateTimeField()
    last_login_ip = db.StringField()
    login_count = db.IntField()
    avatar = db.StringField()
    endereco = db.EmbeddedDocumentField(Address)

    @property
    def id(self):
        """Return id."""
        return self.pk

    @classmethod
    def by_email(cls, email):
        """Find user by email."""
        return cls.objects(email=email).first()

    @property
    def gravatar(self):
        """Get gravatar."""
        email = self.email.strip()
        if isinstance(email, unicode):
            email = email.encode("utf-8")
        import hashlib
        encoded = hashlib.md5(email).hexdigest()
        return "https://secure.gravatar.com/avatar/%s.png" % encoded

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """Save user and put role user."""
        if len(document.roles) == 0:
            role = Role.objects.get(name='user')
            document.roles = [role]

    def __unicode__(self):
        """return object with email."""
        return "{}".format(self.email)


signals.pre_save.connect(User.pre_save, sender=User)
