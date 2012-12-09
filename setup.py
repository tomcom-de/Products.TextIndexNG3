##########################################################################
# TextIndexNG3
# (C) 2007, ZOPYX Ltd & Co. KG, Tuebingen, Germany
##########################################################################

import os
from setuptools import setup, find_packages


CLASSIFIERS = [
    'Programming Language :: Python',
]

version_file = os.path.join('Products', 'TextIndexNG3', 'version.txt')
version = open(version_file).read().strip()

readme_file= os.path.join('Products', 'TextIndexNG3', 'doc', 'README.txt')
desc = open(readme_file).read().strip()
changes_file = os.path.join('Products', 'TextIndexNG3', 'CHANGES.txt')
changes= open(changes_file).read().strip()

long_description = desc  + '\n\nCHANGES\n===========\n\n' + changes

test_optionals_requirements = (
    'zope.testing'
  , 'plone.indexer'
  , 'Products.CMFDefault'
  , 'Plone'
  , 'Pillow'
)


setup(name='Products.TextIndexNG3',
      version=version,
      license='ZPL (see LICENSE.txt)',
      author='Andreas Jung',
      author_email='info@zopyx.com',
      maintainer='Andreas Jung',
      maintainer_email='info@zopyx.com',
      classifiers=CLASSIFIERS,
      keywords='Zope2 Zope3 fulltext indexing ',
      url='http://pypi.zopyx.com/pypi/Products.TextIndexNG3',
      description='Pluggable fulltext indexing solution for Zope 2 and Zope 3',
      long_description=long_description,
      packages=['Products', 'Products.TextIndexNG3'],
      include_package_data = True,
      zip_safe=False,
      install_requires=('setuptools',
                        'Zope2 >= 2.12.18',
                        'zopyx.txng3.core',
                        'zopyx.txng3.ext',
                        ),
      tests_require=('zope.testing', ),
      extras_require={'zope2.12' : []
                     ,'test' : ('zope.testing', )
                     ,'test_optionals' : test_optionals_requirements
                     },
      namespace_packages=['Products'],
      )
