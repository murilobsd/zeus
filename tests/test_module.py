"""
    zeusproject.testsuite.tests
    ~~~~~~~~~~~~~~~~~~~~~~
    Who tests the tests?
    :copyright: (c) 2016 by the Lab804 Team.
    :license: BSD, see LICENSE for more details.
"""
import os
import pytest

from zeusproject import commands


@pytest.mark.test_module
class TestModule():
    """Testing Module."""

    project_f = os.path.join(os.getcwd(), "../tests/ex")
    module = commands.Module(name_project=project_f,
                             author="Testuser",
                             domain="lab804.com.br")

    def test_instance(self):
        """Testing is instance of module."""
        assert True == isinstance(self.module, commands.Module)

    def test_path_not_exist(self):
        """Path project not exist."""
        with pytest.raises(Exception):
            commands.Module(name_project="path_not_exist",
                            author="Testuser",
                            domain="lab804.com.br")
