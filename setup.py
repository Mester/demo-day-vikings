from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['tests/']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import sys, pytest
        errcode = pytest.main(self.pytest_args)
        sys.exit(errcode)


with open('README.md') as f:
    readme = f.read()


with open('LICENSE') as f:
    license = f.read()


setup(
    name='music_app',
    version='0.0.1',
    description='Generate a list of 10 trending songs from r/listentothis',
    long_description=readme,
    authors='Ben Dauer, Adrian Hintermaier, Jason Meeks, Tyler Phillips, Anubhav Yadav',
    url='https://github.com/Mester/demo-day-vikings',
    license=license,
    packages=['music_app'],
    install_requires=[
        'Flask>=0.11.1'
    ],
     tests_require=[
        'pytest==2.9.2',
        'pytest-cov==2.2.1',
        'coverage==4.0.3',
        'tox==2.3.1'
    ],
    cmdclass={'test': PyTest},
)

