# -*- coding: utf-8 -*-
"""
    {{NAMEPROJECT}}.public.controllers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    {{NAME}} public controllers module

    :copyright: (c) {{YEAR}} by {{AUTHOR}}.
    :license: BSD, see LICENSE for more details.
"""
from flask import render_template, Blueprint

blueprint = Blueprint('public', __name__)


@blueprint.route('/')
def home():
    """return user profle."""
    return render_template('public/index.html')
