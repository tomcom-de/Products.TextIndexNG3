###########################################################################
# TextIndexNG V 3
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################

"""
TextIndexNG3 test layer

$Id: txngtest.py 2342 2011-06-01 08:27:35Z yvoschu $
"""

from Testing.ZopeTestCase.layer import ZopeLite
from zope.testing.cleanup import cleanUp
from Zope2.App import zcml


class TextIndexNG3ZCMLLayer(ZopeLite):

    @classmethod
    def setUp(cls):
        import Products.Five
        import Products.TextIndexNG3

        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('configure.zcml', Products.Five)
        try:
            import Products.GenericSetup
            zcml.load_config('meta.zcml', Products.GenericSetup)
        except ImportError:
            pass
        zcml.load_config('configure.zcml', Products.TextIndexNG3)

    @classmethod
    def tearDown(cls):
        cleanUp()
