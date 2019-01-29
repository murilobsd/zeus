#!/usr/bin/env python3
"""Zeus ...."""

import os
import re
import sys
import uuid
import time
import jinja2
import codecs
import shutil
import logging
import colorlog
import argparse
from colorama import init
from termcolor import cprint
from datetime import datetime
from pyfiglet import figlet_format
init(autoreset=True, strip=not sys.stdout.isatty())


# logging
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(name)s] \u2192 %(message)s',
    datefmt="%d/%m/%Y"))
logger = colorlog.getLogger("ZEUS")
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class CreateFolderException(Exception):
    """Create Folder Module."""

    pass


class DuplicateModuleException(Exception):
    """Duplicate Module Name."""

    pass


class DuplicateException(Exception):
    """Duplicate Project Name."""

    pass


class RenameFolder(Exception):
    """Exception Rename Folder."""

    pass


class StructProject:
    """Resposible to struct project.

    :class:`commands.StructProject` See :ref:`projects` for more information.
    """

    _templatesfld = "templates"  # Template folder.
    _appfld = "app"  # Template app folder
    cwd = os.getcwd()

    # Where i who?
    scriptdir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, name_project, author, domain):
        """Init function."""
        self.name_project = self._clean_name(name_project)
        self.name = os.path.basename(self.name_project)
        self.author = author
        self.domain = self._adjust_domain(domain)

        # path of project
        self.projectfolder = os.path.abspath(name_project)

    def _clean_name(self, name):
        """Clean name of project."""
        logger.debug("Clean name of project.")
        return re.sub(r"[\s\.]", "", name.lower())

    def _adjust_domain(self, domain):
        """Adjust domain."""
        logger.debug("Adjusting domain.")
        # TODO: Checking if domain is correctly.
        return domain.lower()

    def copy_struct(self):
        """Copy folders to project folder path."""
        logger.debug("Copy struct of folders with new project.")

        try:
            shutil.copytree(os.path.join(self.scriptdir, self._templatesfld),
                            self.projectfolder)
            self.rename_folder(os.path.join(self.projectfolder,
                                            self._appfld),
                               os.path.join(self.projectfolder,
                                            self.name))
            logger.info("[ \u2714 ] Completed copy data to project folder.")
        except Exception:
            logger.error("[ \u2717 ] Error coping project folder.")

    @staticmethod
    def random(size=32):
        """random values."""
        return codecs.encode(os.urandom(size), "hex").decode("utf-8")

    @staticmethod
    def rename_folder(src, dst):
        """Rename folder."""
        try:
            os.rename(src, dst)
            return True
        except:
            raise RenameFolder("Error rename folder: %s" % src)

    def write(self, dst, templatef, context, templatefld=None):
        """write contents."""
        if templatefld is None:
            templatefld = self._templatesfld

        # jinja env
        template_loader = jinja2.FileSystemLoader(
            searchpath=os.path.join(self.scriptdir, templatefld))
        template_env = jinja2.Environment(loader=template_loader)

        template = template_env.get_template(templatef)
        content = template.render(context)

        with open(dst, 'w+') as destiny:
            destiny.write(content)
        return True


class Module(StructProject):
    """Module."""

    _modulefld = "_module"  # Folder template module.

    std_modules = {
        "users": ["__init__.py", "controllers.py", "models.py", "forms.py"],
        "admin": ["__init__.py", "controllers.py", "models.py", "forms.py"],
        "public": ["__init__.py", "controllers.py", "models.py", "forms.py"]
    }

    def __init__(self, name_project, author, domain):
        """Init function."""
        StructProject.__init__(self, name_project, author, domain)

        # Path of Project exist.
        if not os.path.exists(self.projectfolder):
            logger.error("[ \u2717 ] Not exist name of project.")
            raise Exception("Not exist name of project.")

        self.modulesfolder = os.path.join(
            self.projectfolder, self.name)

    def ger_std_modules(self):
        """Generating default modules."""
        context = {
            "NAMEPROJECT": self.name,
            "YEAR": datetime.now().year,
            "AUTHOR": self.author,
            "NAME": self.name,
            "MODNAME": None
        }

        for m_folder in self.std_modules.keys():
            modfiles = self.std_modules[m_folder]
            for mfile in modfiles:
                templatefile = os.path.join(self.modulesfolder, m_folder,
                                            mfile)
                template = os.path.join(self._appfld, m_folder, mfile)
                # update context key modname
                context.update({"MODNAME": m_folder})
                self.write(templatefile, template, context)

        logger.info("[ \u2714 ] Creating Default Modules.")

    def _get_modules(self):
        """return modules folder."""
        modules_folder = [folder for folder in
                          os.listdir(self.modulesfolder)
                          if os.path.isdir(os.path.join(self.modulesfolder,
                                                        folder))]

        return modules_folder

    def ger_custom(self, name):
        """Generating custom modules."""
        custom_name = self._clean_name(name)
        mod_path = os.path.join(self.modulesfolder, name)
        if os.path.exists(mod_path):
            logger.error("[ \u2717 ] Exists same name of module.")
            raise DuplicateModuleException("Duplicated module name.")

        try:
            os.makedirs(mod_path)
        except:
            logger.error("[ \u2717 ] Error creating module folder.")
            raise CreateFolderException("Error creating module folder.")

        context = {
            "NAMEPROJECT": self.name,
            "YEAR": datetime.now().year,
            "AUTHOR": self.author,
            "NAME": self.name,
            "MODNAME": custom_name
        }

        templatesfile = ["__init__.py",
                         "controllers.py", "models.py", "forms.py"]
        for template in templatesfile:
            templatefile = os.path.join(mod_path, template)
            self.write(templatefile, template, context,
                       templatefld=self._modulefld)

        # update __init__.py
        self.update_app(custom_name)

        logger.info("[ \u2714 ] Completed created module.")

    def update_app(self, custom_name):
        """Update for put blueprints and modules in __init__.py."""
        template = None
        limit = 0

        with open(os.path.join(self.modulesfolder, "__init__.py")) as destiny:
            template = destiny.readlines()

        if not template:
            raise Exception("Not exist file __int__.py file")

        for num, line in enumerate(template):
            str_find = ("from "
                        + self.name_project + " import users, admin, public")
            if line.startswith(str_find):
                list_line = line.split(",")
                list_line[-1] = list_line[-1].replace("\n", "")
                list_line.append(" " + custom_name + "\n")
                line = ",".join(list_line)
                template[num] = line
            elif line.startswith("    app.register_blueprint("):
                limit = num
            else:
                pass

        if limit != 0:
            # Template blueprint
            tpl_bp = "    app.register_blueprint({}.controllers.blueprint)\n"
            template.insert(limit + 1, tpl_bp.format(custom_name))

        # save update datas
        filename = os.path.join(self.modulesfolder, "__init__.py")
        with open(filename, "w") as destiny:
            destiny.write("".join(template))


class Template(StructProject):
    """Represents Template. Template is an object that create templates modules.

    :class:`commands.Template` See :ref:`templates` for more information.
    """

    _modulefld = "_template"  # Folder template module.

    _files = ["create.jinja", "edit.jinja", "get.jinja", "list.jinja"]

    def __init__(self, name_project, author, domain):
        """Init function."""
        StructProject.__init__(self, name_project, author, domain)

        # Project exist.
        if not os.path.exists(self.projectfolder):
            logger.error("[ \u2717 ] Not exist name of project.")
            raise Exception("Not exist name of project.")

        self.templatesfolder = os.path.join(
            self.projectfolder, "templates")

    def ger_custom(self, name):
        """Generating custom template."""
        custom_name = self._clean_name(name)
        tpl_path = os.path.join(self.templatesfolder, name)
        if os.path.exists(tpl_path):
            logger.error("[ \u2717 ] Exists same name of template.")
            raise DuplicateModuleException("Duplicated template name.")

        try:
            os.makedirs(tpl_path)
        except:
            logger.error("[ \u2717 ] Error creating template folder.")
            raise CreateFolderException("Error creating template folder.")

        context = {
            "TITLE": name.capitalize(),
            "MODNAME": custom_name
        }

        # TODO: CHANGE THIS PLEASE
        for fname in self._files:
            templatefile = os.path.join(tpl_path, fname)
            # read
            filename = os.path.join(self.scriptdir, self._modulefld, fname)
            with open(filename) as destiny:
                content = destiny.read()

            content = content.replace("{{ TITLE }}", context["TITLE"])
            content = content.replace("{{MODNAME}}", context["MODNAME"])

            # write
            with open(templatefile, "w") as destiny:
                destiny.write(content)

        logger.info("[ \u2714 ] Completed created template.")


class Project(StructProject):
    """Represents Project. Project is an object that create a struct.

    :class:`commands.Project` See :ref:`projects` for more information.
    """

    def __init__(self, name_project, author, domain):
        """Init function."""
        StructProject.__init__(self, name_project, author, domain)

        # Project exist.
        if os.path.exists(self.projectfolder):
            logger.error("[ \u2717 ] Exists same name of project.")
            raise DuplicateException("Duplicated project name.")

        # Copy all data
        self.copy_struct()

        self.module = Module(name_project, author, domain)

        self.context = {
            "SECRETKEY": StructProject.random(),
            "NAME": self.name,
            "DOMAIN": self.domain,
            "SALT": uuid.uuid4().hex,
            "NAMEPROJECT": self.name,
            "AUTHOR": self.author,
            "YEAR": datetime.now().year,
            "MODULES": ["users", "admin", "public"]
        }

    def _extensions(self):
        """Plugin flask."""
        templatefile = os.path.join(self.projectfolder, self.name,
                                    "extensions.py")

        self.write(templatefile, os.path.join(self._appfld, "extensions.py"),
                   self.context)
        logger.info("[ \u2714 ] Creating Extensions file.")

        return True

    def _config(self):
        """Config files."""
        templatefile = os.path.join(self.projectfolder, self.name,
                                    "config.py")

        self.write(templatefile, os.path.join(self._appfld, "config.py"),
                   self.context)
        logger.info("[ \u2714 ] Creating config file.")

        return True

    def _app(self):
        """Generate App file."""
        dst = os.path.join(self.projectfolder, self.name,
                           "__init__.py")

        self.write(dst, os.path.join(self._appfld, "__init__.py"),
                   self.context)
        logger.info("[ \u2714 ] Creating app file.")

    def _manage(self):
        """Generate manage file."""
        templatefile = os.path.join(self.projectfolder, "manage.py")

        self.write(templatefile, "manage.py", self.context)
        logger.info("[ \u2714 ] Creating manage file.")

    def _license(self):
        """Generate License."""
        templatefile = os.path.join(self.projectfolder, "LICENSE")

        self.write(templatefile, "LICENSE", self.context)

        logger.info("[ \u2714 ] Creating LICENSE BSD ;-)")

    def _readme(self):
        """Generate Readme."""
        templatefile = os.path.join(self.projectfolder, "README.rst")

        self.write(templatefile, "README.rst", self.context)

        logger.info("[ \u2714 ] Creating README.")

    def _fabfile(self):
        """Generate Fabfile."""
        templatefile = os.path.join(self.projectfolder, "fabfile.py")

        self.write(templatefile, "fabfile.py", self.context)

    def _uwsgi(self):
        """Generate Uwsgi."""
        templatefile = os.path.join(self.projectfolder, "uwsgi.ini")

        self.write(templatefile, "uwsgi.ini", self.context)

    def _uwsgi_log_folder(self):
        uwsgi_log_folder = os.path.join(self.projectfolder, 'log')
        
        # if folder exists, do nothing
        if os.path.exists(uwsgi_log_folder):
            return
        
        try:
            os.mkdir(uwsgi_log_folder)
        except:
            logger.error("[ \u2717 ] Error creating uwsgi log folder.")
            raise CreateFolderException("Error creating uwsgi log folder.")

    def _config_files(self):
        """Nginx Supervisor conf files."""
        files = ["project_nginx.conf", "project_supervisor.conf"]
        folder = os.path.join(self.projectfolder, "config")

        for conffile in files:
            templatefile = os.path.join(folder, conffile)

            self.write(templatefile, os.path.join("config", conffile),
                       self.context)

    def generate(self):
        """Generate Project."""
        logger.debug("Starting generating project...")
        start = time.time()
        # Config
        self._config()
        # Extensions
        self._extensions()
        # App
        self._app()
        # Manage
        self._manage()
        # License
        self._license()
        # Readme
        self._readme()
        # Fabfile
        self._fabfile()
        # Uwsgi
        self._uwsgi()
        # Uwsgi
        self._uwsgi_log_folder()
        # Conf files Nginx Supervidor
        self._config_files()
        # Std. Modules
        self.module.ger_std_modules()
        end = time.time() - start
        cprint("=" * 55, "green", attrs=["bold"])
        logger.info("[ \u0231 ] Finishing: %f sec." % end)


def get_arguments():
    """Get Arguments command line."""
    parser = argparse.ArgumentParser(
        description=cprint(figlet_format("ZeUs!", font="starwars"),
                           "green", attrs=["bold"]),
        prog="zeus")
    parser.add_argument("--project", "-p", help="Creating project.",
                        type=str, default="")
    parser.add_argument("--module", "-m", help="Creating module.",
                        nargs=2)
    parser.add_argument("--template", "-t", help="Creating template.",
                        nargs=2)
    parser.add_argument("--author", "-a",
                        help="Author of project (default: %(default)s).",
                        type=str, default="Lab804")
    parser.add_argument("--domain", "-do",
                        help="Domain, (default: %(default)s)",
                        type=str, default="lab804.com.br")
    parser.add_argument("--debug", "-d", help="Debug mode.",
                        type=bool, default=False),
    parser.add_argument("--version", "-v", action="version",
                        version="%(prog)s 0.1.2")
    args = parser.parse_args()
    return args
