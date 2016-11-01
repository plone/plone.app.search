from setuptools import setup, find_packages
import os

version = '1.1.9.dev0'

tests_require = ['collective.testcaselayer',
                 'plone.app.testing',
                 'selenium>=2.0a5']

setup(
    name='plone.app.search',
    version=version,
    description="Search user interface for Plone CMS.",
    long_description=open("README.rst").read() + "\n" +
                     open(os.path.join("CHANGES.rst")).read(),
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='Denys Mishunov',
    author_email='denys.mishunov@gmail.com',
    url='http://github.com/plone/plone.app.search',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.app.contentlisting',
        # -*- Extra requirements: -*-
    ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
    entry_points = '''
        [z3c.autoinclude.plugin]
        target = plone
    ''',
    )
