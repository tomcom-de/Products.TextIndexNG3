# -*- coding: iso-8859-15 -*-

################################################################
# (C) 2004-2011 
# ZOPYX Ltd.
# Charlottenstr. 37/1, D-72070 Tübingen, Germany
# info@zopyx.com, www.zopyx.com 
################################################################

import unittest
import pkg_resources

try:
    pkg_resources.get_distribution('Plone')
except pkg_resources.DistributionNotFound:
    _PLONE_INSTALLED = False
except pkg_resources.VersionConflict:
    raise Exception("Update this code!")
else:
    _PLONE_INSTALLED = True

if _PLONE_INSTALLED:
    from Products.PloneTestCase import PloneTestCase
    PloneTestCase.installProduct('Five')
    PloneTestCase.installProduct('CMFPlone')
    PloneTestCase.installProduct('TextIndexNG3')

    # setup a new Plohn site    
    PloneTestCase.setupPloneSite(products=('TextIndexNG3', ))
    PTC = PloneTestCase.PloneTestCase
    _PLONE_INSTALLED = True
else:
    PTC = object


class PloneTests(PTC):

    def afterSetUp(self):
        membership = self.portal.portal_membership
        membership.addMember('god', 'god', ('Manager',), ())

        self.login('god')
        self.portal.txng_convert_indexes()

    def testSetup(self):
        c = self.portal.portal_catalog
        indexes = c.Indexes
        self.assertEqual(indexes['SearchableText'].meta_type, 'TextIndexNG3')
        self.assertEqual(indexes['Title'].meta_type, 'TextIndexNG3')


def test_suite():
    s = unittest.TestSuite()
    if _PLONE_INSTALLED:
        s.addTest(unittest.makeSuite(PloneTests))
    else:
        print 'Products.TextIndexNG3: Skipped Plone setup tests.'
    return s
