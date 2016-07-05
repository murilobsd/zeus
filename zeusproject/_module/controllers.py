# -*- coding: utf-8 -*-
"""
    {{NAMEPROJECT}}.{{MODNAME}}.controllers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    {{NAME}} {{MODNAME}} controllers module

    :copyright: (c) {{YEAR}} by {{AUTHOR}}.
    :license: BSD, see LICENSE for more details.
"""
from flask import current_app, render_template, Blueprint, redirect, \
    url_for, flash, current_app, request
from flask.ext.security import login_required

{# Get Model #}
from {{NAMEPROJECT}}.{{MODNAME}}.models import {{MODNAME | capitalize}}
{# Get Form #}
from {{NAMEPROJECT}}.{{MODNAME}}.forms import {{MODNAME}}Form

blueprint = Blueprint('{{MODNAME}}', __name__, url_prefix='/{{MODNAME}}')


@login_required
@blueprint.route('/')
def get_all(page=1):
    """Return all {{MODNAME}}.

    :param int page: Number of pagination.

    """
    _all = {{MODNAME | capitalize}}.objects.all()
    current_app.logger.debug(u'Get all {{MODNAME}}.')
    return render_template('{{MODNAME}}/list.jinja', _all=_all)


@login_required
@blueprint.route('/create', methods=["GET", "POST"])
def create():
    """Create instance of {{MODNAME}}."""
    form = {{MODNAME}}Form(request.form)
    if request.method == 'POST' and form.validate():
        instance = {{MODNAME | capitalize}}()
        form.populate_obj(instance)
        instance.save()
        flash("Criado com sucesso.", "success")
        current_app.logger.debug(u"Create {{MODNAME}}.")
        return redirect(url_for("{{MODNAME}}.get_all"))
    return render_template('{{MODNAME}}/create.jinja', form=form)


@login_required
@blueprint.route('/<pk>')
def get(pk):
    """Get {{MODNAME}}.

    :param ObjectID pk: pk is ObjectID of instance.

    """
    current_app.logger.debug(u'Get {{MODNAME}} - %s' % str(pk))
    instance = {{MODNAME | capitalize}}.objects.get_or_404(_id=pk)
    return render_template('{{MODNAME}}/get.jinja', instance=instance)


@login_required
@blueprint.route('/<pk>/edit', methods=["GET", "POST"])
def edit(pk):
    """Edit {{MODNAME}}.

    :param ObjectID pk: pk is objectid of instance.

    """
    current_app.logger.debug(u'Edit {{MODNAME}} - %s' % str(pk))

    instance = {{MODNAME | capitalize}}.objects.get_or_404(_id=pk)
    form = {{MODNAME}}Form(request.form, obj=instance)

    if request.method == 'POST' and form.validate():
        form.populate_obj(instance)
        instance.save()
        flash("Alteração salva.", "info")
        return redirect(url_for("{{MODNAME}}.get_all"))
    return render_template('{{MODNAME}}/edit.jinja', form=form)


@login_required
@blueprint.route('/<pk>/remove')
def remove(pk):
    """Remove instance of {{MODNAME}}.

    :param ObjectID pk: pk is objectid of instance.

    """
    instance = {{MODNAME | capitalize}}.objects.get_or_404(_id=pk)
    instance.remove()
    current_app.logger.debug(u'Removed {{MODNAME}} - %s' % str(pk))
    flash("Removido com sucesso.", "danger")
    return redirect(url_for("{{MODNAME}}.get_all"))
