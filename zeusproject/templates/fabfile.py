#!/usr/bin/env python
"""Fabric."""

from getpass import getpass
from fabric.api import cd, env, lcd, put, prompt, local, sudo, task, prefix
from fabric.colors import green, red
from fabric.contrib.files import exists, append

local_app_dir = "./"
local_config_dir = "./config"

remote_app_dir = "/home/www"
remote_flask_dir = remote_app_dir + "/{{NAMEPROJECT}}"
remote_nginx_dir = "/etc/nginx/sites-enabled"
remote_supervisor_dir = "/etc/supervisor/conf.d"
remote_systemd_dir = "/etc/systemd/system/"

env.hosts = ["add_ip_or_domain"]
env.user = "root"

DB_APT = "http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse"


PACKAGES = [
    "python3",
    "python3-pip",
    "python3-virtualenv",
    "virtualenv",
    "nginx",
    "git",
    "supervisor"
]


def install_dep():
    """Install dependencies."""
    sudo("apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927")
    sudo("echo 'deb " + DB_APT + "' > /etc/apt/sources.list.d/mongodb-org-3.2.list")
    sudo("apt-get update")
    sudo("apt-get install -y " + " ".join(PACKAGES))


def install_db():
    """Install DB."""
    sudo("apt-get install -y --allow-unauthenticated mongodb-org")
    with lcd(local_config_dir):
        with cd(remote_systemd_dir):
            put("./mongodb.service", "./", use_sudo=True)

    sudo("systemctl enable mongodb")
    sudo("systemctl start mongodb")
    print(green("Starting MongoDB."))


def install_requirements():
    """Install requirements."""

    if exists(remote_app_dir) is False:
        sudo("mkdir " + remote_app_dir)
    if exists(remote_flask_dir) is False:
        sudo("mkdir " + remote_flask_dir)
    with lcd(local_app_dir):
        with cd(remote_app_dir):
            with cd(remote_flask_dir):
                put("*", "./", use_sudo=True)
            if exists(remote_app_dir + "/env-{{NAMEPROJECT}}") is False:
                sudo("virtualenv env-{{NAMEPROJECT}} -p python3")
            sudo(
                "source env-{{NAMEPROJECT}}/bin/activate && pip install -r {{NAMEPROJECT}}/requirements.txt")


def create_role():
    """Create Remote Role."""
    name_role = prompt("Unique name? ")
    with cd(remote_app_dir):
        sudo(
            "source env-{{NAMEPROJECT}}/bin/activate && python {{NAMEPROJECT}}/manage.py create_role -n {}".format(name_role))


def create_user():
    """Create Remote User."""
    email = prompt("Email ")
    passw = getpass("Password: ")
    active = prompt("Activate (y/n): ")
    if len(passw) < 6:
        print(red("Password length greather than 6 catacters."))
        return
    if active != "y" or active != "n":
        active = "y"
    with cd(remote_app_dir):
        sudo("source env-{{NAMEPROJECT}}/bin/activate && python {{NAMEPROJECT}}/manage.py create_user -n {} -p {} -a {}".format(email,
                                                                                                                                passw,
                                                                                                                                active
                                                                                                                                ))
        print(green("Creted User."))


def configure_nginx():
    """Configure Nginx."""
    sudo("systemctl start nginx")
    if exists("/etc/nginx/sites-enabled/default"):
        sudo("rm /etc/nginx/sites-enabled/default")
    if exists("/etc/nginx/sites-enabled/{{NAMEPROJECT}}") is False:
        sudo("touch /etc/nginx/sites-available/{{NAMEPROJECT}}")
        sudo("ln -s /etc/nginx/sites-available/{{NAMEPROJECT}}" +
             " /etc/nginx/sites-enabled/{{NAMEPROJECT}}")
    with lcd(local_config_dir):
        with cd(remote_nginx_dir):
            put("./project_nginx.conf", "./{{NAMEPROJECT}}", use_sudo=True)
    sudo("systemctl restart nginx")


def configure_supervisor():
    """Configure Supervisor."""
    sudo("systemctl enable supervisor")
    sudo("systemctl start supervisor")
    if exists("/etc/supervisor/conf.d/{{NAMEPROJECT}}.conf") is False:
        with lcd(local_config_dir):
            with cd(remote_supervisor_dir):
                put("./project_supervisor.conf", "./{{NAMEPROJECT}}.conf",
                    use_sudo=True)
                sudo("supervisorctl reread")
                sudo("supervisorctl update")


def run_app():
    """Run the app."""
    with cd(remote_flask_dir):
        sudo("supervisorctl start {{NAMEPROJECT}}")


def deploy():
    """Deploy."""
    with lcd(local_app_dir):
        with cd(remote_app_dir):
            with cd(remote_flask_dir):
                put("*", "./", use_sudo=True)
            if exists(remote_app_dir + "/env-{{NAMEPROJECT}}") is False:
                sudo("virtualenv env-{{NAMEPROJECT}} -p python3")
            sudo(
                "source env-{{NAMEPROJECT}}/bin/activate && pip install -r {{NAMEPROJECT}}/requirements.txt")

    sudo("supervisorctl restart {{NAMEPROJECT}}")


def status():
    """Statu app."""
    sudo("supervisorctl status {{NAMEPROJECT}}")


def create():
    """Create app."""
    install_dep()
    install_db()
    install_requirements()
    configure_nginx()
    configure_supervisor()
