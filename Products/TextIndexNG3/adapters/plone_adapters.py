###########################################################################
# TextIndexNG V 3
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################

"""
A collection of adapter to provide out-of-the-box indexing support
for Plone content-types.

$Id: plone_adapters.py 2166 2009-04-22 19:53:38Z yvoschu $
"""

from zope.component import adapts

from Products.ATContentTypes.interface.file import IATFile

from cmf_adapters import CMFContentAdapter


class ATFileAdapter(CMFContentAdapter):

    """An adapter for ATCT files.
    """

    adapts(IATFile)

    def addSearchableTextField(self, icc):
        text = self._c(self.context.SearchableText())
        icc.addContent('SearchableText', text, self.language)

        f = self.context.getFile()
        if not f:
            return

        body = str(f)
        if body:
            mt = f.getContentType()
            if mt == 'text/plain':
                icc.addContent('SearchableText', self._c(body), self.language)
            else:
                icc.addBinary('SearchableText', body, mt, None, self.language)
