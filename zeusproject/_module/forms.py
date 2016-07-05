# -*- coding: utf-8 -*-
"""
    {{NAMEPROJECT}}.{{MODNAME}}.forms
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    {{NAME}} {{MODNAME}} forms module

    :copyright: (c) {{YEAR}} by {{AUTHOR}}.
    :license: BSD, see LICENSE for more details.
"""

from flask.ext.mongoengine.wtf import model_form
from flask.ext.wtf import Form
from wtforms import SubmitField

{# Get Model #}
from {{NAMEPROJECT}}.{{MODNAME}}.models import {{MODNAME | capitalize}}

class SubForm(Form):
    submit = SubmitField("Adicionar")

{{MODNAME }}Form = model_form({{MODNAME | capitalize}}, base_class=SubForm, exclude=[])
