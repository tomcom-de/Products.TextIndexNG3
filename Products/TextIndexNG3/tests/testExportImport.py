###########################################################################
# TextIndexNG V 3
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################

"""
export / import support unit tests

$Id: testExportImport.py 2324 2011-05-31 12:03:55Z yvoschu $
"""

import unittest
import sys
import txngtest

try:
    from Products.GenericSetup.testing import NodeAdapterTestCase
    _GS_INSTALLED = True
except ImportError:
    class NodeAdapterTestCase: pass
    _GS_INSTALLED = False

_TXNG3_XML = """\
<index name="foo_txng3" meta_type="TextIndexNG3">
 <autoexpand value="off"/>
 <autoexpand_limit value="4"/>
 <dedicated_storage value="True"/>
 <default_encoding value="iso-8859-15"/>
 <field value="foo_txng3"/>
 <index_unknown_languages value="True"/>
 <language value="en"/>
 <lexicon value="txng.lexicons.default"/>
 <query_parser value="txng.parsers.en"/>
 <ranking value="False"/>
 <ranking_method value="txng.ranking.cosine"/>
 <splitter value="txng.splitters.simple"/>
 <splitter_additional_chars value="_-"/>
 <splitter_casefolding value="True"/>
 <storage value="txng.storages.default"/>
 <use_normalizer value="False"/>
 <use_stemmer value="False"/>
 <use_stopwords value="False"/>
</index>
"""


class TextIndexNG3NodeAdapterTests(NodeAdapterTestCase, unittest.TestCase):

    layer = txngtest.TextIndexNG3ZCMLLayer

    def _getTargetClass(self):
        from Products.TextIndexNG3.exportimport import TextIndexNG3NodeAdapter

        return TextIndexNG3NodeAdapter

    def _populate(self, obj):
        obj.index.__init__(fields=('foo_txng3',))

    def setUp(self):
        from Products.TextIndexNG3.TextIndexNG3 import TextIndexNG3

        self._obj = TextIndexNG3('foo_txng3', None, None)
        self._XML = _TXNG3_XML


def test_suite():
    s = unittest.TestSuite()
    if _GS_INSTALLED:
        s.addTest(unittest.makeSuite(TextIndexNG3NodeAdapterTests))
    else:
        print 'Products.TextIndexNG3: Skipped GenericSetup export/import tests.'
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
