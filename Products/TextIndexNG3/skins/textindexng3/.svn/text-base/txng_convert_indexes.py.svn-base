##parameters=overwrite=0

###########################################################################
# TextIndexNG V 3                
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################

# Replace all text indexes with a TextIndexNG V3 instance

# set language as appropriate
LANGUAGES = ('en', )
#LANGUAGES = ('en', 'de')

encoding = context.portal_properties.site_properties.default_charset

metatypes =  ['ZCTextIndex', 'TextIndex', 'TextIndexNG2', 'TextIndexNG3']
needed = ('SearchableText', 'Title', 'Description')

catalog = context.portal_catalog
indexes = catalog.getIndexObjects()
all_ids = list()
source_names = dict()
for idx in indexes:
    if idx.meta_type in metatypes:
        all_ids.append(idx.getId())
        source_names[idx.getId()] = idx.getIndexSourceNames()
existing_ids = all_ids[:]

for id in needed:
    if not id in all_ids:
        all_ids.append(id)

for id in all_ids:

    if id in existing_ids:
        catalog.manage_delIndex(id)
    catalog.manage_addIndex(id, 'TextIndexNG3', extra={'languages': LANGUAGES,
                                                       'fields' : source_names[id],
                                                       'default_encoding' : encoding,
                                                       'splitter_casefolding' : True,
                                                       'dedicated_storages' : True,
                                                       'use_converters' : True,
                                                       'index_unknown_languages' : True,
                                                       'storage' : 'txng.storages.term_frequencies',
                                                       'ranking' : True,
                                                       })

catalog.manage_reindexIndex(all_ids, context.REQUEST)
context.REQUEST.RESPONSE.redirect('txng_maintenance?portal_status_message=All+TXNG+indexes+migrated+and+fixed')
