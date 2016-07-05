#!/usr/bin/env python
# coding=utf-8

from flask_script import Manager
from flask_script.commands import Server, Shell, ShowUrls, Clean
from flask_security.script import CreateUserCommand, AddRoleCommand,\
    RemoveRoleCommand, ActivateUserCommand, DeactivateUserCommand, \
    CreateRoleCommand
from flask_assets import ManageAssets


from {{NAMEPROJECT}} import create_app

app = create_app()

manager = Manager(app)
manager.add_command("urls", ShowUrls())
manager.add_command("shell", Shell(use_ipython=True))
manager.add_command("runserver", Server(use_reloader=True))
manager.add_command("clean", Clean())
manager.add_command("create_user", CreateUserCommand())
manager.add_command("add_role", AddRoleCommand())
manager.add_command("remove_role", RemoveRoleCommand())
manager.add_command("deactivate_user", DeactivateUserCommand())
manager.add_command("activate_user", ActivateUserCommand())
manager.add_command("create_role", CreateRoleCommand())
manager.add_command("assets", ManageAssets())

if __name__ == "__main__":
    manager.run()
