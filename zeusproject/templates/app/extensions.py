# -*- coding: utf-8 -*-
"""
    {{NAMEPROJECT}}.extensions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    {{NAME}} extensions module

    :copyright: (c) {{YEAR}} by {{AUTHOR}}.
    :license: BSD, see LICENSE for more details.
"""
from flask_mongoengine import MongoEngine
from flask_mail import Mail
from flask_assets import Environment
from flask_cache import Cache
from flask_bootstrap import Bootstrap

mail = Mail()
db = MongoEngine()
assets = Environment()
cache = Cache()
bootstrap = Bootstrap()
