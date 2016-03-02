from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='pub.tools',
      version=version,
      description="Package of tools for formatting publication data and accessing data from Entrez tool",
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='',
      author='Eric Wohnlich',
      author_email='wohnlice@imsweb.com',
      url='http://git.imsweb.com/wohnlice/pub.tools',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['pub'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'biopython',
          'unidecode',
      ],
      )
