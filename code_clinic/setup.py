
from setuptools import setup, find_packages
from codeclinic.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='codeclinic',
    version=VERSION,
    description='WeThinkCode_ - Team_17 - Code_Clinic',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Team_17',
    author_email='tcajee@student.wethinkcode.co.za',
    url=' https://github.com/tcajee/code_clinic.git',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'codeclinic': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        codeclinic = codeclinic.main:main
    """,
)
