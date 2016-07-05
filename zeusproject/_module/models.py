# -*- coding: utf-8 -*-
"""
    {{NAMEPROJECT}}.{{MODNAME}}.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    {{NAME}} {{MODNAME}} models module

    :copyright: (c) {{YEAR}} by {{AUTHOR}}.
    :license: BSD, see LICENSE for more details.
"""
from wtforms import validators

from {{NAMEPROJECT}}.extensions import db


class {{MODNAME | capitalize}}(db.Document):
    """The :class:`{{MODNAME | capitalize}}` class represent the
    {{MODNAME | capitalize}} model.

    param str nome: example of field, description here.
    """
    nome = db.StringField(max_length=150, required=True, validators=[
                          validators.InputRequired(message=u'O nome é obrigatório.'), ])

    def __unicode__(self):
        """Return the ObjectID representation of a pagamento."""
        return "{}".format(self.pk)
