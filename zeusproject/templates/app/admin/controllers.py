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

@blueprint.route('/users')
@roles_required('admin')
def get_users():
    """return users in admin."""
    current_app.logger.debug(u'Get all users in admin.')
    return render_template('admin/users/list.html')

@blueprint.route('/')
@roles_required('admin')
def admin_page():
    """return admin page."""
    current_app.logger.debug(u'Get all users in admin.')
    return render_template('admin/index.html')
