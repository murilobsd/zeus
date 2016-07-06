#!/usr/bin/env python
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
        self.name = name_project
        self.name_project = self._clean_name(name_project)
        self.author = author
        self.domain = self._adjust_domain(domain)

        # path of project
        self.projectfolder = os.path.join(self.cwd, self.name_project)

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
                                            self.name_project))
            logger.info("[ \u2714 ] Completed copy data to project folder.")
        except Exception as e:
            logger.error("[ \u2717 ] %s" % e)

    def random(self, size=32):
        """random values."""
        return codecs.encode(os.urandom(size), "hex").decode("utf-8")

    def rename_folder(self, src, dst):
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

        with open(dst, 'w+') as f:
            f.write(content)
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

        # path of project
        self.projectfolder = os.path.join(self.cwd, self.name_project)

        # Project exist.
        if not os.path.exists(self.projectfolder):
            logger.error("[ \u2717 ] Not exist name of project: %s" %
                         self.projectfolder)
            raise Exception("Not exist name of project.")

        self.modulesfolder = os.path.join(
            self.projectfolder, self.name_project)

    def ger_std_modules(self):
        """Generating default modules."""
        context = {
            "NAMEPROJECT": self.name_project,
            "YEAR": datetime.now().year,
            "AUTHOR": self.author,
            "NAME": self.name,
            "MODNAME": None
        }

        for m_folder in self.std_modules.keys():
            files = self.std_modules[m_folder]
            for f in files:
                templatefile = os.path.join(self.modulesfolder, m_folder,
                                            f)
                template = os.path.join(self._appfld, m_folder, f)
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
            logger.error("[ \u2717 ] Exists same name of module: %s" %
                         self.modulesfolder)
            raise DuplicateModuleException("Duplicated module name.")

        try:
            os.makedirs(mod_path)
        except:
            logger.error("[ \u2717 ] Error creating module folder: %s" %
                         self.modulesfolder)
            raise CreateFolderException("Error creating module folder.")

        context = {
            "NAMEPROJECT": self.name_project,
            "YEAR": datetime.now().year,
            "AUTHOR": self.author,
            "NAME": self.name,
            "MODNAME": custom_name
        }

        files = ["__init__.py", "controllers.py", "models.py", "forms.py"]
        for f in files:
            templatefile = os.path.join(mod_path, f)
            self.write(templatefile, f, context, templatefld=self._modulefld)

        # update __init__.py
        self.update_app(custom_name)

        logger.info("[ \u2714 ] Completed created module %s." % custom_name)

    def update_app(self, custom_name):
        """Update for put blueprints and modules in __init__.py."""
        template = None
        limit = 0
        with open(os.path.join(self.modulesfolder, "__init__.py")) as f:
            template = f.readlines()

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
        with open(os.path.join(self.modulesfolder, "__init__.py"), "w") as f:
            f.write("".join(template))


class Template(StructProject):
    """Represents Template. Template is an object that create templates modules.

    :class:`commands.Template` See :ref:`templates` for more information.
    """

    _modulefld = "_template"  # Folder template module.

    _files = ["create.jinja", "edit.jinja", "get.jinja", "list.jinja"]

    def __init__(self, name_project, author, domain):
        """Init function."""
        StructProject.__init__(self, name_project, author, domain)

        # path of project
        self.projectfolder = os.path.join(self.cwd, self.name_project)

        # Project exist.
        if not os.path.exists(self.projectfolder):
            logger.error("[ \u2717 ] Not exist name of project: %s" %
                         self.projectfolder)
            raise Exception("Not exist name of project.")

        self.templatesfolder = os.path.join(
            self.projectfolder, "templates")

    def ger_custom(self, name):
        """Generating custom template."""
        custom_name = self._clean_name(name)
        tpl_path = os.path.join(self.templatesfolder, name)
        if os.path.exists(tpl_path):
            logger.error("[ \u2717 ] Exists same name of template: %s" %
                         self.templatesfolder)
            raise DuplicateModuleException("Duplicated template name.")

        try:
            os.makedirs(tpl_path)
        except:
            logger.error("[ \u2717 ] Error creating template folder: %s" %
                         self.modulesfolder)
            raise CreateFolderException("Error creating template folder.")

        context = {
            "TITLE": name.capitalize(),
            "MODNAME": custom_name
        }

        # TODO: CHANGE THIS PLEASE
        for f in self._files:
            templatefile = os.path.join(tpl_path, f)
            # read
            with open(os.path.join(self.scriptdir, self._modulefld, f)) as f:
                content = f.read()

            content = content.replace("{{ TITLE }}", context["TITLE"])
            content = content.replace("{{MODNAME}}", context["MODNAME"])

            # write
            with open(templatefile, "w") as f:
                f.write(content)

        logger.info("[ \u2714 ] Completed created template %s." % custom_name)


class Project(StructProject):
    """Represents Project. Project is an object that create a struct.

    :class:`commands.Project` See :ref:`projects` for more information.
    """

    def __init__(self, name_project, author, domain):
        """Init function."""
        StructProject.__init__(self, name_project, author, domain)

        # path of project
        self.projectfolder = os.path.join(self.cwd, self.name_project)

        # Project exist.
        if os.path.exists(self.projectfolder):
            logger.error("[ \u2717 ] Exists same name of project: %s" %
                         self.projectfolder)
            raise DuplicateException("Duplicated project name.")

        # Copy all data
        self.copy_struct()

        self.module = Module(self.name_project, self.author, self.domain)

        self.context = {
            "SECRETKEY": self.random(),
            "NAME": self.name,
            "DOMAIN": self.domain,
            "SALT": uuid.uuid4().hex,
            "NAMEPROJECT": self.name_project,
            "AUTHOR": self.author,
            "YEAR": datetime.now().year,
            "MODULES": ["users", "admin", "public"]
        }

    def _extensions(self):
        """Plugin flask."""
        templatefile = os.path.join(self.projectfolder, self.name_project,
                                    "extensions.py")

        self.write(templatefile, os.path.join(self._appfld, "extensions.py"),
                   self.context)
        logger.info("[ \u2714 ] Creating Extensions file.")

        return True

    def _config(self):
        """Config files."""
        templatefile = os.path.join(self.projectfolder, self.name_project,
                                    "config.py")

        self.write(templatefile, os.path.join(self._appfld, "config.py"),
                   self.context)
        logger.info("[ \u2714 ] Creating config file.")

        return True

    def _app(self):
        """Generate App file."""
        dst = os.path.join(self.projectfolder, self.name_project,
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
        templatefile = os.path.join(self.projectfolder, "README.md")

        self.write(templatefile, "README.md", self.context)

        logger.info("[ \u2714 ] Creating README.")

    def ger_template(self, name=None):
        """Generate templates."""
        self.template.construct()

    def ger_modules(self, name=None):
        """Generate modules."""
        self.modules.construct()

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
        # Std. Modules
        self.module.ger_std_modules()
        end = time.time() - start
        cprint("=" * 55, "green", attrs=["bold"])
        logger.info("[ \u0231 ] Finishing: %f sec." % end)


def get_arguments():
    """Get Arguments command line."""
    parser = argparse.ArgumentParser(
        description=cprint(figlet_format("ZeUs!", font="starwars"),
                           "green", attrs=["bold"]))
    parser.add_argument("--createproject", "-cp", help="Creating project.",
                        type=bool, default=False)
    parser.add_argument("--createmodule", "-cm", help="Creating module.",
                        type=str, default="")
    parser.add_argument("--createtemplate", "-ct", help="Creating template.",
                        type=str, default=False)
    parser.add_argument("name", help="Name of project.")
    parser.add_argument("--author", "-a",
                        help="Name of author, default: Lab804.",
                        type=str, default="Lab804")
    parser.add_argument("--domain", "-do",
                        help="Domain, default: projectname.lab804.com.br",
                        type=str, default="lab804.com.br")
    parser.add_argument("--debug", "-d", help="Debug mode.",
                        type=bool, default=False)
    args = parser.parse_args()
    return args
