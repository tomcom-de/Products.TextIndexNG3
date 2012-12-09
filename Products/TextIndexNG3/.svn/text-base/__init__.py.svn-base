###########################################################################
# TextIndexNG V 3                
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################


import os, sys

try:
    import zopyx
except ImportError:
    raise ImportError('The zopyx package could not be imported. Please check the installation of the TextIndexNG extension modules!')

package_home = os.path.dirname(__file__)

# add base package to sys.path
src_dir = os.path.abspath(os.path.join(package_home, 'src'))
if not src_dir in sys.path:
    sys.path.append(src_dir)


import TextIndexNG3

def initialize(context):
    context.registerClass(
        TextIndexNG3.TextIndexNG3,
        permission='Add Pluggable Index',
        icon='pt/index.gif',
        visibility=None,
        constructors=(TextIndexNG3.manage_addTextIndexNG3Form,
                      TextIndexNG3.manage_addTextIndexNG3),
    )


def get_storages(self):
    """ return all available storages """
    from zope.component import getUtilitiesFor
    from zopyx.txng3.core.interfaces import IStorage, IStorageWithTermFrequency
    return [x[0] for x in getUtilitiesFor(IStorage)]

def get_lexicons(self):
    """ return all available lexicons"""
    from zope.component import getUtilitiesFor
    from zopyx.txng3.core.interfaces import ILexicon
    return [x[0] for x in getUtilitiesFor(ILexicon)]

def get_splitters(self):
    """ return all available splitters"""
    from zope.component import getUtilitiesFor
    from zopyx.txng3.core.interfaces import ISplitter
    return [x[0] for x in getUtilitiesFor(ISplitter)]

def get_parsers(self):
    """ return all available parsers"""
    from zope.component import getUtilitiesFor
    from zopyx.txng3.core.interfaces import IParser
    return [x[0] for x in getUtilitiesFor(IParser)]

def get_ranking_methods(self):
    """ return all available parsers"""
    from zope.component import getUtilitiesFor
    from zopyx.txng3.core.interfaces import IRanking
    return [x[0] for x in getUtilitiesFor(IRanking)]

# some monkey patching (necessary since we have no context object
# during the factory phase where we could use browser views)

from Products.ZCatalog.ZCatalog import ZCatalog
ZCatalog.get_storages = get_storages
ZCatalog.get_lexicons = get_lexicons
ZCatalog.get_splitters = get_splitters
ZCatalog.get_parsers = get_parsers
ZCatalog.get_ranking_methods = get_ranking_methods

# Plone
textindexng_globals = globals()

try:
    from Products.CMFCore.DirectoryView import registerDirectory
    registerDirectory('skins', textindexng_globals)
except ImportError:
    pass
