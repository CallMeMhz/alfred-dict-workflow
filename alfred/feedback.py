# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import json
from xml.etree import ElementTree
import xml.sax.saxutils as saxutils
import copy
from six import string_types


class Item(object):
    def __init__(self, **kwargs):
        self.content = {
            'title': kwargs.get('title', ''),
            'subtitle': kwargs.get('subtitle', ''),
            'icon': kwargs.get('icon') if kwargs.get('icon') else 'icon.png'
        }

        it = kwargs.get('icontype', '').lower()
        self.icon_type = it if it in ['fileicon', 'filetype'] else None

        valid = kwargs.get('valid', None)
        if isinstance(valid, string_types) and valid.lower() == 'no':
            valid = 'no'
        elif isinstance(valid, bool) and not valid:
            valid = 'no'
        else:
            valid = None

        self.attrb = {
            'uid': kwargs.get('uid', None),
            'arg': kwargs.get('arg', None),
            'valid': valid,
            'autocomplete': kwargs.get('autocomplete', None),
            'type': kwargs.get('type', None)
        }

        self.content = dict((k, v) for k, v in self.content.items() if v is not None)
        self.attrb = dict((k, v) for k, v in self.attrb.items() if v is not None)

    def copy(self):
        return copy.copy(self)

    def get_xml_element(self):
        item = ElementTree.Element('item', self.attrb)
        for k, v in self.content.items():
            attrb = {}
            if k == 'icon' and self.icon_type:
                attrb['type'] = self.icon_type
            sub = ElementTree.SubElement(item, k, attrb)
            sub.text = v
        return item

    def get_dict(self):
        return {**self.attrb, **self.content}


class Feedback(object):
    def __init__(self):
        self.items = []

    def __repr__(self):
        return self.get()

    def add_item(self, **kwargs):
        item = kwargs.pop('item', None)
        item = item if isinstance(item, Item) else Item(**kwargs)
        self.items.append(item)

    def clean(self):
        self.items = []

    def is_empty(self):
        return not bool(self.items)

    def get(self, unescape=False):
        data = {'variables': {}, 'items': [item.get_dict() for item in self.items]}
        return json.dumps(data, ensure_ascii=False)

    def output(self):
        print(self.get())
