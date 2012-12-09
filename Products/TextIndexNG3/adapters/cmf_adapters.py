###########################################################################
# TextIndexNG V 3
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################

"""
A collection of adapter to provide better indexing support for
CMF derived types.

$Id: cmf_adapters.py 2305 2011-03-18 21:53:07Z patrick_gerken $
"""

from zope.component import adapts
from zope.interface import implements

from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.interfaces import IDocument
from Products.CMFDefault.interfaces import IFile

from zopyx.txng3.core.interfaces import IIndexableContent
from zopyx.txng3.core.content import IndexContentCollector as ICC
from zopyx.txng3.core.logger import LOG
from zopyx.txng3.core.config import DEFAULT_LANGUAGE


class CMFContentAdapter:

    """An adapter for CMF content.
    """

    adapts(IContentish)
    implements(IIndexableContent)

    def __init__(self, context):
        self.context = context
        self.encoding = self._getSiteEncoding()
        try:
            self.language = context.Language()
        except AttributeError:
            self.language = DEFAULT_LANGUAGE

    def _getSiteEncoding(self):
        plone_utils = getToolByName(self.context, 'plone_utils', None)
        if plone_utils is not None:
            return plone_utils.getSiteEncoding()

        ptool = getToolByName(self.context, 'portal_properties', None)
        if ptool is not None:
            return ptool.getProperty('default_charset', 'utf-8')

        return 'utf-8'

    def _c(self, text):
        if isinstance(text, unicode):
            return text
        try:
            return unicode(text, self.encoding)
        except UnicodeDecodeError:
            LOG.warn('Content from %s could not be converted to unicode using the site encoding %s' %
                    (self.context.absolute_url(1), self.encoding))
            raise

    def indexableContent(self, fields):
        icc = ICC()
        if 'getId' in fields:
            self.addIdField(icc)
        if 'Title' in fields:
            self.addTitleField(icc)
        if 'Description' in fields:
            self.addDescriptionField(icc)
        if 'SearchableText' in fields:
            self.addSearchableTextField(icc)
        return icc

    def addIdField(self, icc):
        try:
            id = self._c(self.context.getId())
        except TypeError:
            id = self._c(self.context.getId)
        icc.addContent('getId', id, self.language)

    def addTitleField(self, icc):
        try:
            title = self._c(self.context.Title())
        except TypeError:
            title = self._c(self.context.Title)
        icc.addContent('Title', title, self.language)

    def addDescriptionField(self, icc):
        try:
            description = self._c(self.context.Description())
        except TypeError:
            description = self._c(self.context.Description)
        icc.addContent('Description', description, self.language)

    def addSearchableTextField(self, icc):
        try:
            text = self._c(self.context.SearchableText())
        except TypeError:
            text = self._c(self.context.SearchableText)
        icc.addContent('SearchableText', text, self.language)


class CMFDocumentAdapter(CMFContentAdapter):

    """An adapter for CMFDefault documents.
    """

    adapts(IDocument)

    def addSearchableTextField(self, icc):
        title = self._c(self.context.Title())
        icc.addContent('SearchableText', title, self.language)

        description = self._c(self.context.Description())
        icc.addContent('SearchableText', description, self.language)

        body = self._c(self.context.EditableBody())
        if body:
            mt = self.context.Format()
            if mt == 'text/plain':
                icc.addContent('SearchableText', body, self.language)
            else:
                icc.addBinary('SearchableText', body, mt, None, self.language)


class CMFFileAdapter(CMFContentAdapter):

    """An adapter for CMFDefault files.
    """

    adapts(IFile)

    def addSearchableTextField(self, icc):
        title = self._c(self.context.Title())
        icc.addContent('SearchableText', title, self.language)

        description = self._c(self.context.Description())
        icc.addContent('SearchableText', description, self.language)

        body = str(self.context)
        if body:
            mt = self.context.Format()
            if mt == 'text/plain':
                icc.addContent('SearchableText', self._c(body), self.language)
            else:
                icc.addBinary('SearchableText', body, mt, None, self.language)
