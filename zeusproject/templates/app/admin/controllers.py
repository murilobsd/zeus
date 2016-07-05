# -*- coding: utf-8 -*-
"""
    {{NAMEPROJECT}}.admin.controllers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    {{NAME}} admin controllers module

    :copyright: (c) {{YEAR}} by {{AUTHOR}}.
    :license: BSD, see LICENSE for more details.
"""
from flask import current_app, render_template, Blueprint
from flask.ext.security import roles_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@roles_required('admin')
@blueprint.route('/users')
def get_users():
    """return users in admin."""
    current_app.logger.debug(u'Get all users in admin.')
    return render_template('admin/users/list.html')
