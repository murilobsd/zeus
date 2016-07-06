# -*- coding: utf-8 -*-
"""
    {{NAMEPROJECT}}
    ~~~~~~~~~~~~~~

    {{NAME}} descrição do seu projeto.

    :copyright: (c) {{YEAR}} by {{AUTHOR}}.
    :license: BSD, see LICENSE for more details.
"""
import os
import sys
import logging
from flask import Flask
from flask_security import Security, MongoEngineUserDatastore


from {{NAMEPROJECT}} import extensions
from {{NAMEPROJECT}}.users.models import User, Role
from {{NAMEPROJECT}}.users.forms import CustomLoginForm, ExtendedRegisterForm
from {{NAMEPROJECT}} import {% if MODULES -%} {% for module in MODULES -%}{% if loop.last -%}{{module}}{%else-%}{{module}}, {%endif-%} {% endfor %}{% endif %}

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

APP_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app():
    """Flask app factory."""

    app = Flask(__name__,
                template_folder=os.path.join(APP_DIR, "..", 'templates'),
                static_folder=os.path.join(APP_DIR, "..", 'static'))

    # Config App
    app.config.from_object("{{NAMEPROJECT}}.config.app_config")
    app.logger.info("Config enviroment: %s" % app.config["ENVIROMENT"])

    # Format logging
    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format='%(asctime)s %(levelname)s: %(message)s '
               '[in %(pathname)s:%(lineno)d]',
        datefmt='%d%m%Y-%H:%M%p',
    )

    email_errors(app)
    register_extensions(app)
    register_blueprints(app)

    return app


def email_errors(app):
    """ Sendo erros of email."""
    if not app.debug and not app.testing:
        import logging.handlers
        mail_handler = logging.handlers.SMTPHandler(
            'localhost',
            os.getenv('USER'),
            app.config['SYS_ADMINS'],
            '{0} error'.format(app.config['SITE_NAME']),
        )
        mail_handler.setFormatter(logging.Formatter('''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s
            Message:
            %(message)s
        '''.strip()))

        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        app.logger.info("Emailing on error is ENABLED")
    else:
        app.logger.info("Emailing on error is DISABLED")


def register_extensions(app):
    """Call the method 'init_app' to register the extensions in the flask.Flask
    object passed as parameter.

    :app: flask.Flask object
    :returns: None

    """
    # DB
    app.db = extensions.db
    app.db.init_app(app)
    # Email
    extensions.mail.init_app(app)
    # Securirty
    app.user_datastore = MongoEngineUserDatastore(app.db, User, Role)
    app.security = Security(app, app.user_datastore,
                            register_form=ExtendedRegisterForm,
                            login_form=CustomLoginForm)
    # Assets
    extensions.assets.init_app(app)
    assets_out = os.path.join(APP_DIR, "..", "static", "gen")

    if not os.path.exists(assets_out):
        app.logger.info("Create static folder of minify files.")
        os.mkdir(assets_out)

    # Fist time, create basic roles.
    if Role.objects.count() == 0:
        Role.objects.create(name="admin", description="admin roles")
        Role.objects.create(name="user", description="user roles")

    # Cache
    extensions.cache.init_app(app)

    # BootStrap
    extensions.bootstrap.init_app(app)


def register_blueprints(app):
    """Register all blueprints.

    :app: flask.Flask object
    :returns: None

    """
    {% if MODULES -%}
    {% for module in MODULES -%}
    app.register_blueprint({{module}}.controllers.blueprint)
    {% endfor -%}
    {% endif -%}
