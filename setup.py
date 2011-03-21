from setuptools import setup

setup(
    name="pytest_filetests",
    version='0.1',
    packages=['pytest_filetests'],
    description='Simple plugin for py.test for reading tests from yaml files',
    author='Ermolin Ilya',
    author_email='ermolinis+pytest@gmail.com',
    url='http://github.com/cgi/pytest_filetests',
    # the following makes a plugin available to py.test
    entry_points={
        'pytest11': [
            'filetests = pytest_filetests.filetests',
        ]
    }
)
