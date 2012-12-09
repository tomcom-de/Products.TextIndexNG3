###########################################################################
# TextIndexNG V 3
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################

"""
TextIndexNG3 unit tests

$Id: testTextIndexNG3.py 2347 2011-06-01 10:06:42Z yvoschu $
"""

import sys, os, unittest
import txngtest
from Testing import ZopeTestCase
ZopeTestCase.installProduct('ZCatalog', 1)
ZopeTestCase.installProduct('TextIndexNG3', 1)

from OFS.DTMLDocument import addDTMLDocument
from Products.ZCatalog.ZCatalog import ZCatalog
from zope.interface.verify import verifyClass

from Products.TextIndexNG3.TextIndexNG3 import TextIndexNG3
from zopyx.txng3.core.config import *
from zopyx.txng3.core.resultset import ResultSet


class TextIndexNG3Tests(ZopeTestCase.ZopeTestCase):

    layer = txngtest.TextIndexNG3ZCMLLayer

    def afterSetUp(self):
        self.folder._setObject('catalog', ZCatalog('catalog'))

    def testInterfaceMock(self):
        from Products.PluginIndexes.interfaces import IPluggableIndex
        verifyClass(IPluggableIndex, TextIndexNG3)

    def testSimpleSetup(self):
        extra = {'lexicon' : DEFAULT_LEXICON,
                 'storage' : DEFAULT_STORAGE,
                 'splitter' : DEFAULT_SPLITTER}
        self.folder.catalog.manage_addIndex('PrincipiaSearchSource', 'TextIndexNG3', extra)

    def testStemmer(self):
        extra = {'use_stemmer' : True}
        self.folder.catalog.manage_addIndex('PrincipiaSearchSource', 'TextIndexNG3', extra)
        idx = self.folder.catalog.Indexes['PrincipiaSearchSource']
        self.assertEqual(idx.index.use_stemmer, True)

        extra = {'use_stemmer' : False}
        self.folder.catalog.manage_addIndex('PrincipiaSearchSource1', 'TextIndexNG3', extra)
        idx = self.folder.catalog.Indexes['PrincipiaSearchSource1']
        self.assertEqual(idx.index.use_stemmer, False)

    def testIndexing(self):
        extra = {'lexicon' : DEFAULT_LEXICON,
                 'storage' : DEFAULT_STORAGE,
                 'splitter' : DEFAULT_SPLITTER}
        self.folder.catalog.manage_addIndex('PrincipiaSearchSource', 'TextIndexNG3', extra)

        from zopyx.txng3.core import tests
        datadir = os.path.join(os.path.dirname(tests.__file__), 'data', 'texts')
        for f in os.listdir(datadir):
            fname = os.path.join(datadir, f)
            if not os.path.isfile(fname): continue
            fp = open(fname)
            addDTMLDocument(self.folder, id=f, title=f, file=fp)
            fp.close()

        for obj in [o for o in self.folder.objectValues('DTML Document') if o.getId().endswith('txt')]:
            self.folder.catalog.catalog_object(obj, obj.absolute_url(1))
        self.assertEqual(len(self.folder.catalog), 199)

    def test_apply_index(self):
        self.folder.catalog.manage_addIndex('foo', 'TextIndexNG3')
        idx = self.folder.catalog.Indexes['foo']
        def dummysearch(query, **kw):
            return ResultSet((query, kw), None)
        idx.index.search = dummysearch

        request = {}
        self.assertEqual(idx._apply_index(request), None)

        request = {'foo': 'Foo'}
        self.assertEqual(idx._apply_index(request)[0][0], u'Foo')
        self.assertEqual(idx._apply_index(request)[0][1], {})

        request = {'foo': {'query': 'Foo'}}
        self.assertEqual(idx._apply_index(request)[0][0], u'Foo')
        self.assertEqual(idx._apply_index(request)[0][1], {})

        request = {'foo': {'query': 'Foo', 'parser': 'foo_parser'}}
        self.assertEqual(idx._apply_index(request)[0][0], u'Foo')
        self.assertEqual(idx._apply_index(request)[0][1],
                         {'parser': 'foo_parser'})

        request = {'foo': {'query': 'Foo', 'ranking': False}}
        self.assertEqual(idx._apply_index(request)[0][0], u'Foo')
        self.assertEqual(idx._apply_index(request)[0][1],
                         {'ranking': False})


def test_suite():
    s = unittest.TestSuite()
    s.addTest(unittest.makeSuite(TextIndexNG3Tests))
    return s

def main():
    unittest.TextTestRunner().run(test_suite())

def debug():
    test_suite().debug()

def pdebug():
    import pdb
    pdb.run('debug()')

if __name__=='__main__':
    if len(sys.argv) > 1:
        globals()[sys.argv[1]]()
    else:
        main()
