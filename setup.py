from setuptools import find_packages, setup

version = '1.7'

setup(name='pub.tools',
      version=version,
      description="Package of tools for formatting publication data and accessing data from Entrez tool",
      classifiers=[
          "Framework :: Plone :: 5.0",
          "Framework :: Plone :: 5.1",
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
          'lxml',
          'requests'
      ],
      )
