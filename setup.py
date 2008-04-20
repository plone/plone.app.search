from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='plone.app.search',
      version=version,
      description="Search functionality for Plone 3",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='http://svn.plone.org/svn/plone/plone.app.search',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'archetypes.schemaextender',
          'plone.browserlayer',
          'plone.memoize',
          'plone.i18n',
#         'zope.component',
#         'Products.CMFCore'.
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
