###########################################################################
# TextIndexNG V 3                
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################

from StringIO import StringIO

import transaction
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.TextIndexNG3 import textindexng_globals

key = 'textindexng3'

configlets = \
( { 'id'         : 'TextIndexNG3'
  , 'name'       : 'TextIndexNG3'
  , 'action'     : 'string:${portal_url}/txng_maintenance'
  , 'category'   : 'Products'
  , 'appId'      : 'TextIndexNG3'
  , 'permission' : ManagePortal
  , 'imageUrl'   : 'index.gif'
  }
,
)

def install(self):
    out = StringIO()

    skins_tool = getToolByName(self, 'portal_skins')

    # Setup the skins
    if key  not in skins_tool.objectIds():
        addDirectoryViews(skins_tool, 'skins',  textindexng_globals)
        out.write("Added %s skin directory view to portal_skins\n" % key)

    # Now we need to go through the skin configurations and insert
    # 'textindexng' into the configurations.  Preferably, this should be
    # right before where 'content' is placed.  Otherwise, we append
    # it to the end.
    skins = skins_tool.getSkinSelections()

    for skin in skins:
        path = skins_tool.getSkinPath(skin)
        path = [p.strip() for p in  path.split(',')]

        if key not in path:
            try: path.insert(0, key)
            except ValueError:
                path.append(key)

            path = ', '.join(path)
            # addSkinSelection will replace exissting skins as well.
            skins_tool.addSkinSelection(skin, path)
            out.write("Added '%s' to %s skin\n" % (key, skin))
        else:
            out.write("Skipping %s skin, '%s' is already set up\n" % (
                key, skin))


    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            print >>out, 'Adding configlet %s\n' % conf['id']
            configTool.registerConfiglet(**conf)

    print >> out, "Successfully installed"  
    return out.getvalue()


def uninstall(self, reinstall=False):
    out = StringIO()

    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            print >>out, 'Removing configlet %s\n' % conf['id']
            configTool.unregisterConfiglet(conf['id'])

    skins_tool = getToolByName(self, 'portal_skins')

    # Now we need to go through the skin configurations and insert
    # 'textindexng3' into the configurations.  Preferably, this should be
    # right before where 'content' is placed.  Otherwise, we append
    # it to the end.
    skins = skins_tool.getSkinSelections()

    for skin in skins:
        path = skins_tool.getSkinPath(skin)
        path = [p.strip() for p in  path.split(',')]

        if key in path:
            path.remove(key)

            path = ', '.join(path)
            # addSkinSelection will replace exissting skins as well.
            skins_tool.addSkinSelection(skin, path)
            out.write("Removed '%s' from %s skin\n" % (key, skin))
        else:
            out.write("Skipping %s skin, '%s' is removed set up\n" % (
                key, skin))

    if not reinstall:
        # uninstall TXGN3 indexes and re-create the original TextIndexes

        catalog = getToolByName(self, 'portal_catalog')
        indexes = catalog.getIndexObjects()
        indexes = [idx.getId() for idx in indexes
                    if idx.meta_type in ('TextIndexNG3',)]

        class _extra:
            lexicon_id="plone_lexicon"
            index_type="Okapi BM25 Rank"
        extra=_extra()

        for idx in indexes:
            catalog.manage_delIndex(idx)
            catalog.addIndex(idx, "ZCTextIndex", extra=extra)
            index=catalog._catalog.getIndex(idx)
            index.indexed_attrs=[idx]

        catalog.manage_reindexIndex(indexes, self.REQUEST)

    return out.getvalue()
