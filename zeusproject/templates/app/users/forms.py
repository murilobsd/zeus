# -*- coding: utf-8 -*-
"""
    {{NAMEPROJECT}}.users.forms
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    {{NAME}} user forms module

    :copyright: (c) {{YEAR}} by {{AUTHOR}}.
    :license: BSD, see LICENSE for more details.
"""

from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, \
    ValidationError
from flask_security.forms import ConfirmRegisterForm, LoginForm


class CustomLoginForm(LoginForm):
    """Custom LoginForm"""
    email = StringField("Email")
    password = PasswordField("Senha")
    remember = BooleanField("Lembre-se de mim")


class ExtendedRegisterForm(ConfirmRegisterForm):
    """Custom Register Form."""
    fullname = StringField("Nome Completo", [DataRequired(message='Esse campo é obrigatório.')])
    email = StringField("Email")
    password = PasswordField("Senha")
    submit = SubmitField("Registrar")
