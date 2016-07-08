.. image:: https://zeus.lab804.com.br/img/logo_zeus.svg
    :alt: Zeus logo
    :width: 300
    :height: 150
    :align: center

:Info: Scaffold flask.
:Repository: https://github.com/murilobsd/zeus
:Author: Murilo Ijanc (http://github.com/murilobsd)
:Site: `https://zeus.lab804.com.br <https://zeus.lab804.com.br>`_

.. image:: https://badge.fury.io/py/zeus-lab804.svg
   :target: https://badge.fury.io/py/zeus-lab804
   :alt: Pypi Package

.. image:: https://landscape.io/github/murilobsd/zeus/master/landscape.png
   :target: https://landscape.io/github/murilobsd/zeus/master
   :alt: Code Health

Sobre
=====
Zeus facilita a criação de projetos para `Flask` além de implementar outras
bibliotecas como `flask-cache <https://github.com/thadeusb/flask-cache>`_,
`flask-script <https://github.com/smurfix/flask-script>`_,
`flask-mongonegine <https://github.com/MongoEngine/flask-mongoengine>`_... possui
funcionalidades para criação de módulos e templates.

Instalação
==========
Nós recomendamos o uso do `virtualenv <https://virtualenv.pypa.io/>`_ e do
`pip <https://pip.pypa.io/>`_. Você pode instalar ``pip install -U zeus-lab804``.
é necessário ter `setuptools <http://peak.telecommunity.com/DevCenter/setuptools>`_
uma alternativa ``easy_install -U zeus-lab804``. Por fim, você pode realizar o
download do código em `GitHub <http://github.com/murilobsd/zeus>`_ e rodar ``python
setup.py install``.

Dependências
============
- mongo
- colorama==0.3.7
- colorlog==2.7.0
- Jinja2==2.8
- MarkupSafe==0.23
- pyfiglet==0.7.5
- termcolor==1.1.0

Exemplos
========
Alguns exemplos:

.. code-block:: shell

    # Criando Projeto
    $ zeus --project meuprojeto
    $ cd meuprojeto/
    $ pip install -r requirements-dev.txt
    $ python manage.py runserver
    # Abra seu navegador http://127.0.0.1:5000/

.. code-block:: shell

    # Gerando Modulo
    $ zeus --module pagamento meuprojeto # Caminho do meuprojeto
    # Gerando Template para Modulo
    $ zeus --template pagamento meuprojeto # Caminho do meuprojeto

Opções
======
Outras argumentos que podem ser utilizado na **criação do projeto**.

.. code-block:: shell

    $ zeus --help
     ________   _______  __    __       _______. __
    |       /  |   ____||  |  |  |     /       ||  |
    `---/  /   |  |__   |  |  |  |    |   (----`|  |
      /  /    |   __|  |  |  |  |     \   \     |  |
     /  /----.|  |____ |  `--'  | .----)   |    |__|
    /________||_______| \______/  |_______/     (__)


    usage: zeus [-h] [--project PROJECT] [--module MODULE MODULE]
               [--template TEMPLATE TEMPLATE] [--author AUTHOR] [--domain DOMAIN]
               [--debug DEBUG] [--version]

    optional arguments:
     -h, --help            show this help message and exit
     --project PROJECT, -p PROJECT
                           Creating project.
     --module MODULE MODULE, -m MODULE MODULE
                           Creating module.
     --template TEMPLATE TEMPLATE, -t TEMPLATE TEMPLATE
                           Creating template.
     --author AUTHOR, -a AUTHOR
                           Author of project (default: Lab804).
     --domain DOMAIN, -do DOMAIN
                           Domain, (default: lab804.com.br)
     --debug DEBUG, -d DEBUG
                           Debug mode.
     --version, -v         show program's version number and exit


Tests
=====
Preciso ter vergonha na cara é gerar testes.

Contribuir
============
Contribua de qualquer forma, veja se sua sugestão já não foi respondida nas
`issues <https://github.com/murilobsd/zeus/issues>`_, crie um logo para o
projeto, de sugestões para exemplos, crie templates, ajude criar a wiki...
