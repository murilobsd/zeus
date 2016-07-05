# -*- coding: utf-8 -*-
"""
    {{NAMEPROJECT}}.users.controllers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    {{NAME}} user controllers module

    :copyright: (c) {{YEAR}} by {{AUTHOR}}.
    :license: BSD, see LICENSE for more details.
"""
from flask import current_app, render_template, Blueprint
from flask_security import login_required

blueprint = Blueprint('users', __name__, url_prefix='/users')


@login_required
@blueprint.route('/profile')
def profile():
    """return user profle."""
    current_app.logger.debug(u'Get profile user.')
    return render_template('users/profile.html')
