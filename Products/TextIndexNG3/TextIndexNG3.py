###########################################################################
# TextIndexNG V 3
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################

"""
TextIndexNG3

$Id: TextIndexNG3.py 2274 2010-10-30 09:18:47Z ajung $
"""

from zope.interface import implements

try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass #BBB: for Zope < 2.11.3
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PluginIndexes.interfaces import IPluggableIndex
from Products.PluginIndexes.common.util import parseIndexRequest
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from zopyx.txng3.core.index import Index
from zopyx.txng3.core.config import *
from zopyx.txng3.core.storage import StorageException
from Products.TextIndexNG3.interfaces.textindexng import ITextIndexNG3

marker = object

def get(o, k, default=None):
    """ return a value for a given key of a dict/record 'o' """
    if isinstance(o, dict):
        return o.get(k, default)
    else:
        return getattr(o, k, default)


class TextIndexNG3(SimpleItem, PropertyManager):

    implements(ITextIndexNG3, IPluggableIndex)

    meta_type = 'TextIndexNG3'
    default_encoding = 'iso-8859-15'    # I think we don't need this anymore
    management_page_charset = 'utf-8'   # needed for several ZMI methods
    manage_options = ( {'label' : 'Index', 'action': 'manage_workspace'},
                       {'label' : 'Vocabulary', 'action' : 'vocabularyform'},
                       {'label' : 'Test', 'action' : 'queryform'},
                       {'label' : 'Converters', 'action' : 'converters'},
                       {'label' : 'Thesaurus', 'action' : 'thesaurus'},
                       {'label' : 'Adapters', 'action' : 'adapters'},
                     ) +\
                     SimpleItem.manage_options + \
                     PropertyManager.manage_options    

    query_options = ('query', 'encoding', 'parser', 'language', 'field',
                     'autoexpand', 'similarity_ratio',
                     'ranking', 'ranking_maxhits', 'thesaurus',
                     'search_all_fields')

    def __init__(self, id, extra, caller):
        self.id = id
        self.title = id

        # fields
        fields = [id] # default
        if get(extra, 'fields', []):
            fields = get(extra, 'fields')

        self.index = Index(fields=fields,
                           lexicon=get(extra, 'lexicon', DEFAULT_LEXICON),
                           storage=get(extra, 'storage', DEFAULT_STORAGE),
                           splitter=get(extra, 'splitter', DEFAULT_SPLITTER),
                           autoexpand=get(extra, 'autoexpand', 'off'),
                           autoexpand_limit=get(extra, 'autoexpand_limit', 4),
                           query_parser=get(extra, 'query_parser', 'txng.parsers.en'),
                           use_stemmer=get(extra, 'use_stemmer', False),
                           languages=get(extra, 'languages', ('en',)),
                           use_stopwords=bool(get(extra, 'use_stopwords')),
                           default_encoding=get(extra, 'default_encoding', DEFAULT_ENCODING),
                           use_normalizer=bool(get(extra, 'use_normalizer')),
                           dedicated_storage=bool(get(extra, 'dedicated_storage')),
                           splitter_casefolding=bool(get(extra, 'splitter_casefolding', True)),
                           splitter_additional_chars=get(extra, 'splitter_additional_chars', DEFAULT_ADDITIONAL_CHARS),
                           index_unknown_languages=bool(get(extra, 'index_unknown_languages', True)),
                           ranking=bool(get(extra, 'ranking')),
                           ranking_method=(get(extra, 'ranking_method', DEFAULT_RANKING)),
                           )

    def clear(self):
        """ clear the index """
        self.index.clear()

    def index_object(self, docid, obj, threshold=None):
        result = self.index.index_object(obj, docid)
        return int(result)

    def unindex_object(self, docid):
        self.index.unindex_object(docid)
        return 1

    def getIndexSourceNames(self):
        """ return indexed fields """
        return self.index.fields

    def indexSize(self):
        return len(self.index.getLexicon())

    def getEntryForObject(self, docid, default=None):
        """Get all information contained for 'docid'.

        Returns a string representing a mapping field -> list of indexed words
        for dedicated storages or a list of indexed words for shared storage.
        """
        getWord = self.index.getLexicon().getWord
        d = {}
        for field in self.index.fields:
            try:
                wids = self.index.getStorage(field).getWordIdsForDocId(docid)
            except StorageException:
                wids = ()
            words = [getWord(wid) for wid in wids]
            d[field] = words
        if not self.index.dedicated_storage:
            return repr(d[self.index.fields[0]])
        return repr(d)

    def _apply_index(self, request, cid=''):

        # parse the query options
        record = parseIndexRequest(request, self.getId(), self.query_options)
        if record.keys is None: 
            return None

        # prepare query (must be unicode string)
        query = record.keys[0]
        if not isinstance(query, unicode):
            query = unicode(query, record.get('encoding', self.index.default_encoding), 'ignore')
        if not query:
            return None

        # options
        options = {}
        for k in ('parser', 'language', 'field', 'autoexpand',
                  'similarity_ratio', 'thesaurus', 'ranking',
                  'ranking_maxhits', 'search_all_fields'):
            v = getattr(record, k, marker)
            if v is not marker:
                options[k] = v

        result = self.index.search(query, **options)                                               
        ranked_resultset = result.getRankedResults()
        if ranked_resultset:
            return ranked_resultset, self.id
        else:
            return result.getDocids(), self.id

    def __len__(self):
        return len(self.index)
    numObjects = __len__

    def manage_workspace(self, REQUEST):
        """ redirect to manage since we can not override manage_workspace
            through a Five browser view
        """
        from zope.component import getMultiAdapter
        view = getMultiAdapter((self, REQUEST), name='manageform')
        return view() 


InitializeClass(TextIndexNG3)


manage_addTextIndexNG3Form = PageTemplateFile( "pt/add.pt", globals(), __name__ = 'manage_addTextIndexNG3Form')

def manage_addTextIndexNG3(self, id, extra=None, REQUEST=None, RESPONSE=None, URL3=None):
    """ Hook for the ZCatalog UI """

    return self.manage_addIndex(id, 'TextIndexNG3', extra=extra, 
                REQUEST=REQUEST, RESPONSE=RESPONSE, URL1=URL3)
