# -*- coding: iso-8859-15 -*-

###########################################################################
# TextIndexNG V 3
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################

"""
adapter unit tests

$Id: testAdapters.py 2311 2011-04-20 10:01:11Z yvoschu $
"""

import unittest
import pkg_resources
import os
import sys
import txngtest
from Testing import ZopeTestCase

ZopeTestCase.installProduct('ZCatalog', 1)
ZopeTestCase.installProduct('TextIndexNG3', 1)

from zopyx.txng3.core import tests

try:
    pkg_resources.get_distribution('Products.CMFDefault')
except pkg_resources.DistributionNotFound:
    _CMF_INSTALLED = False
else:
    _CMF_INSTALLED = True

try:
    pkg_resources.get_distribution('plone.indexer')
except pkg_resources.DistributionNotFound:
    _PLONE_INDEXER_INSTALLED = False
else:
    _PLONE_INDEXER_INSTALLED = True

_DATA_DIR = os.path.join(os.path.dirname(tests.__file__), 'data')


class CMFDocumentAdapterTests(unittest.TestCase):

    layer = txngtest.TextIndexNG3ZCMLLayer

    def _getTargetClass(self):
        from Products.TextIndexNG3.adapters.cmf_adapters import CMFDocumentAdapter

        return CMFDocumentAdapter

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_indexableContent_plain(self):
        from Products.CMFCore.CatalogTool import IndexableObjectWrapper
        from Products.CMFDefault.Document import Document

        d = Document('foo', title='Foo', text_format='plain',
                     text='foo content')
        d.setLanguage('en')
        try:
            w = IndexableObjectWrapper(ob=d, catalog=None)
        except TypeError:
            w = IndexableObjectWrapper({}, d) # BBB: for CMF < 2.2
        a = self._makeOne(w)

        icc = a.indexableContent(['Title', 'Description'])
        self.assertEqual(icc.getFields(), ['Description', 'Title'])
        self.assertEqual(icc.getFieldData('Title')[0],
                         {'content': u'Foo', 'language': 'en'})
        self.assertEqual(icc.getFieldData('Description')[0],
                         {'content': u'', 'language': 'en'})

        icc = a.indexableContent(['SearchableText'])
        self.assertEqual(icc.getFields(), ['SearchableText'])
        self.assertEqual(icc.getFieldData('SearchableText')[0],
                         {'content': u'Foo', 'language': 'en'})
        self.assertEqual(icc.getFieldData('SearchableText')[1],
                         {'content': u'', 'language': 'en'})
        self.assertEqual(icc.getFieldData('SearchableText')[2],
                         {'content': u'foo content', 'language': 'en'})

    def test_indexableContent_html(self):
        from Products.CMFCore.CatalogTool import IndexableObjectWrapper
        from Products.CMFDefault.Document import Document

        d = Document('foo', title='Foo', text_format='html',
                     text='foo content')
        d.setLanguage('en')
        try:
            w = IndexableObjectWrapper(ob=d, catalog=None)
        except TypeError:
            w = IndexableObjectWrapper({}, d) # BBB: for CMF < 2.2
        a = self._makeOne(w)

        icc = a.indexableContent(['Title', 'Description'])
        self.assertEqual(icc.getFields(), ['Description', 'Title'])
        self.assertEqual(icc.getFieldData('Title')[0],
                         {'content': u'Foo', 'language': 'en'})
        self.assertEqual(icc.getFieldData('Description')[0],
                         {'content': u'', 'language': 'en'})

        icc = a.indexableContent(['SearchableText'])
        self.assertEqual(icc.getFields(), ['SearchableText'])
        self.assertEqual(icc.getFieldData('SearchableText')[0],
                         {'content': u'Foo', 'language': 'en'})
        self.assertEqual(icc.getFieldData('SearchableText')[1],
                         {'content': u'', 'language': 'en'})
        self.assertEqual(icc.getFieldData('SearchableText')[2],
                         {'content': u'foo content', 'language': 'en'})


class PloneIndexerAdapterTests(unittest.TestCase):

    layer = txngtest.TextIndexNG3ZCMLLayer

    def testCorrectAdapter(self):
        from zope.component import provideAdapter

        from Products.CMFCore.PortalContent import PortalContent
        from plone.indexer.interfaces import IIndexer as PIIIndexer
        from plone.indexer.wrapper import IndexableObjectWrapper \
            as PIIndexableObjectWrapper

        from zopyx.txng3.core.interfaces import IIndexableContent

        d = PortalContent()
        piwrapper = PIIndexableObjectWrapper(d, None)
        txngwrapper = IIndexableContent(piwrapper)
        def SearchableText():
            return ""
        provideAdapter(lambda a,b:SearchableText, (None, None), \
            PIIIndexer, name='SearchableText')
        # This can throw an exception if the adapter is not prepared for
        # the "transparent" Plone Indexer wrapper
        txngwrapper.indexableContent('SearchableText')


class CMFFileAdapterTests(unittest.TestCase):

    layer = txngtest.TextIndexNG3ZCMLLayer

    def _getTargetClass(self):
        from Products.TextIndexNG3.adapters.cmf_adapters import CMFFileAdapter

        return CMFFileAdapter

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_indexableContent_plain(self):
        from Products.CMFCore.CatalogTool import IndexableObjectWrapper
        from Products.CMFDefault.File import File

        d = File('foo', title='Foo', file='foo content',
                 content_type='text/plain')
        d.setLanguage('en')
        try:
            w = IndexableObjectWrapper(ob=d, catalog=None)
        except TypeError:
            w = IndexableObjectWrapper({}, d) # BBB: for CMF < 2.2
        a = self._makeOne(w)

        icc = a.indexableContent(['Title', 'Description'])
        self.assertEqual(icc.getFields(), ['Description', 'Title'])
        self.assertEqual(icc.getFieldData('Title')[0],
                         {'content': u'Foo', 'language': 'en'})
        self.assertEqual(icc.getFieldData('Description')[0],
                         {'content': u'', 'language': 'en'})

        icc = a.indexableContent(['SearchableText'])
        self.assertEqual(icc.getFields(), ['SearchableText'])
        self.assertEqual(icc.getFieldData('SearchableText')[0],
                         {'content': u'Foo', 'language': 'en'})
        self.assertEqual(icc.getFieldData('SearchableText')[1],
                         {'content': u'', 'language': 'en'})
        self.assertEqual(icc.getFieldData('SearchableText')[2],
                         {'content': u'foo content', 'language': 'en'})

    def test_indexableContent_pdf(self):
        from Products.CMFCore.CatalogTool import IndexableObjectWrapper
        from Products.CMFDefault.File import File

        pdf_path = os.path.join(_DATA_DIR, 'test.pdf')
        d = File('foo', title='Foo', file=file(pdf_path, 'rb'),
                 content_type='application/pdf')
        d.setLanguage('de')
        try:
            w = IndexableObjectWrapper(ob=d, catalog=None)
        except TypeError:
            w = IndexableObjectWrapper({}, d) # BBB: for CMF < 2.2
        a = self._makeOne(w)

        icc = a.indexableContent(['Title', 'Description'])
        self.assertEqual(icc.getFields(), ['Description', 'Title'])
        self.assertEqual(icc.getFieldData('Title')[0],
                         {'content': u'Foo', 'language': 'de'})
        self.assertEqual(icc.getFieldData('Description')[0],
                         {'content': u'', 'language': 'de'})

        icc = a.indexableContent(['SearchableText'])
        self.assertEqual(icc.getFields(), ['SearchableText'])
        self.assertEqual(icc.getFieldData('SearchableText')[0],
                         {'content': u'Foo', 'language': 'de'})
        self.assertEqual(icc.getFieldData('SearchableText')[1],
                         {'content': u'', 'language': 'de'})
        body = icc.getFieldData('SearchableText')[2]
        self.assertEqual(body['content'].strip(), u'Viel Vögel sprangen artig '
                         u'in den Tüpel und über Feld und Wüste')
        self.assertEqual(body['language'], 'de')


def test_suite():
    s = unittest.TestSuite()
    if _CMF_INSTALLED:
        s.addTest(unittest.makeSuite(CMFDocumentAdapterTests))
        s.addTest(unittest.makeSuite(CMFFileAdapterTests))
    else:
        print 'Products.TextIndexNG3: Skipped CMF adapter tests.'
    if _PLONE_INDEXER_INSTALLED:
        s.addTest(unittest.makeSuite(PloneIndexerAdapterTests))
    else:
        print 'Products.TextIndexNG3: Skipped Plone Indexer adapter tests.'
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
