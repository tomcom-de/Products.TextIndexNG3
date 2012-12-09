###########################################################################
# TextIndexNG V 3                
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################

try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass #BBB: for Zope < 2.11.3

from Products.Five import BrowserView


class IndexView(BrowserView):

    def test_index(self, query, parser, encoding='iso-8859-15'):
        """ perform a query and return the search result as list of
            object paths
        """
        if not isinstance(query, unicode):
            pattern = unicode(pattern, encoding)
        rs = self.context.index.search(query, parser=parser)
        return [self.context.getpath(docid) for docid in rs.getDocids()]

    def words_vocabulary(self, pattern, language='en'):
        """ return all words from the lexicon that match a particualar
            pattern for a given language.
        """
        if not isinstance(pattern, unicode):
            pattern = unicode(pattern, 'utf-8') # ZMI encoding
        words = self.context.index.getLexicon().getWordsForPattern(pattern, language)
        words.sort()
        return words

    def get_vocabulary_stats(self):
        """ return per-language length of the vocabulary """
        lexicon = self.context.index.getLexicon()
        d = dict()
        for lang in lexicon.getLanguages():
            d[lang] = len(lexicon.getWordsForLanguage(lang))
        return d

    def _getUtilitiesFor(self, iface):
        """ return everything registered for an interface """

        try:
            from zope.app import zapi
            return zapi.getUtilitiesFor(iface)
        except ImportError:
            from zope.component import getUtilitiesFor
            return getUtilitiesFor(iface)

    def get_converters(self):
        """ return all available converters """
        from zopyx.txng3.core.interfaces import IConverter
        return self._getUtilitiesFor(IConverter)

    def get_storages(self):
        """ return all available storages """
        from zopyx.txng3.core.interfaces import IStorage
        return self._getUtilitiesFor(IStorage)

    def get_lexicons(self):
        """ return all available lexicons """
        from zopyx.txng3.core.interfaces import ILexicon
        return self._getUtilitiesFor(ILexicon)

    def get_thesauruses(self):
        """ return all available thesaurus"""
        from zopyx.txng3.core.interfaces import IThesaurus
        return self._getUtilitiesFor(IThesaurus)

    def get_thesaurus(self):
        """ return the content for a particular thesurus """
        from zopyx.txng3.core.interfaces import IThesaurus
        try:
            from zope.app import zapi
            return zapi.getUtility(IThesaurus, self.request['id'])
        except ImportError:
            from zope.component import getUtility
            return getUtility(IThesaurus, self.request['id'])

    def get_splitters(self):
        """ return all available lexicons """
        from zopyx.txng3.core.interfaces import ISplitter
        return self._getUtilitiesFor(ISplitter)

    def get_parsers(self):
        """ return all available lexicons """
        from zopyx.txng3.core.interfaces import IParser
        return self._getUtilitiesFor(IParser)

    def documents_for_word(self):
        """ return all document paths for a given word """
        word = self.request['word']
        language = self.request.get('language', self.context.index.languages[0])
        if not isinstance(word, unicode):
            word = unicode(word, 'utf-8') # ZMI encoding
        wid = self.context.index.getLexicon().getWordId(word,language)
        docids = self.context.index.getStorage(self.context.index.fields[0]).getDocumentsForWordId(wid)
        return [self.context.getpath(docid) for docid in docids]

    def get_adapters(self):
        """ return all registered adapters"""

        from zopyx.txng3.core.interfaces import IIndexableContent
        from zope.component.globalregistry import getGlobalSiteManager as getSiteManager

        registrations = getSiteManager().registeredAdapters()

        for reg in registrations:
            if reg.provided == IIndexableContent:
                yield (reg.required, reg.factory)

InitializeClass(IndexView)
