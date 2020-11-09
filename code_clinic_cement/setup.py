
from setuptools import setup, find_packages
from codeclinic.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='codeclinic',
    version=VERSION,
    description='WeThinkCode_ Cohort 2020 - Team_17 - C',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Team_17',
    author_email='john.doe@example.com',
    url='https://github.com/tcajee/code_clinic',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'codeclinic': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        codeclinic = codeclinic.main:main
    """,
)
