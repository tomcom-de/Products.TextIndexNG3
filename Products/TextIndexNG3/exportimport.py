###########################################################################
# TextIndexNG V 3
# The next generation TextIndex for Zope
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
###########################################################################

"""
export / import support

$Id: exportimport.py 1833 2007-03-19 11:07:57Z yvoschu $
"""

from zope.component import adapts

from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import NodeAdapterBase

from Products.TextIndexNG3.interfaces import ITextIndexNG3


class TextIndexNG3NodeAdapter(NodeAdapterBase):

    """Node im- and exporter for TextIndexNG3.
    """

    adapts(ITextIndexNG3, ISetupEnviron)

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('index')

        settings = self.context.index.getSettings()
        items = settings.items()
        items.sort()
        for key, value in items:
            if key == 'splitter_max_length':
                continue
            if isinstance(value, (tuple, list)):
                for item in value:
                    child = self._doc.createElement(key[:-1])
                    child.setAttribute('value', unicode(item))
                    node.appendChild(child)
            else:
                child = self._doc.createElement(key)
                child.setAttribute('value', unicode(value))
                node.appendChild(child)

        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        node_infos = [ {'name': child.nodeName,
                        'value': child.getAttribute('value').encode('utf-8')}
                       for child in node.childNodes
                       if child.nodeType == child.ELEMENT_NODE ]

        settings = self.context.index.getSettings()
        new_settings = {}
        for key, value in settings.items():
            if key == 'splitter_max_length':
                continue
            if isinstance(value, (tuple, list)):
                name = key[:-1]
            else:
                name = key
            new_value = [ info['value']
                          for info in node_infos if info['name'] == name ]
            if not new_value:
                continue
            if new_value == ['None']:
                new_value = None
            elif isinstance(value, bool):
                new_value = self._convertToBoolean(new_value[0])
            elif isinstance(value, basestring) or value is None:
                new_value = new_value[0]
            elif isinstance(value, int):
                new_value = int(new_value[0])
            elif isinstance(value, tuple):
                new_value = tuple(new_value)
            if new_value != value:
                new_settings[key] = new_value
        if new_settings:
            settings.update(new_settings)
            self.context.index.__init__(**settings)

    node = property(_exportNode, _importNode)
