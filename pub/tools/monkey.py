import os
import xml.etree.ElementTree as ET

from Bio.Entrez.Parser import DataHandler, ListElement, DictionaryElement, StructureElement, ValidationError, \
    StringElement
from Bio._py3k import urlopen as _urlopen


def patch_startElementHandler(self, name, attrs):
    # preprocessing the xml schema
    if self.is_schema:
        if len(attrs) == 1:
            schema = list(attrs.values())[0]
            handle = self.open_xsd_file(os.path.basename(schema))
            # if there is no local xsd file grab the url and parse the file
            if not handle:
                handle = _urlopen(schema)
                text = handle.read()
                self.save_xsd_file(os.path.basename(schema), text)
                handle.close()
                self.parse_xsd(ET.fromstring(text))
            else:
                self.parse_xsd(ET.fromstring(handle.read()))
                handle.close()
    if name not in ["i", "u", "b", "sup", "sub"]:
        self.content = ""
    if name in self.lists:
        object = ListElement()
    elif name in self.dictionaries:
        object = DictionaryElement()
    elif name in self.structures:
        object = StructureElement(self.structures[name])
    elif name in self.items:  # Only appears in ESummary
        name = str(attrs["Name"])  # convert from Unicode
        del attrs["Name"]
        itemtype = str(attrs["Type"])  # convert from Unicode
        del attrs["Type"]
        if itemtype == "Structure":
            object = DictionaryElement()
        elif name in ("ArticleIds", "History"):
            object = StructureElement(["pubmed", "medline"])
        elif itemtype == "List":
            object = ListElement()
        else:
            object = StringElement()
        object.itemname = name
        object.itemtype = itemtype
    elif name in self.strings + self.errors + self.integers:
        self.attributes = attrs
        return
    else:
        # Element not found in DTD
        if self.validating:
            raise ValidationError(name)
        else:
            # this will not be stored in the record
            object = ""
    if object != "":
        object.tag = name
        if attrs:
            object.attributes = dict(attrs)
        if len(self.stack) != 0:
            current = self.stack[-1]
            try:
                current.append(object)
            except AttributeError:
                current[name] = object
    self.stack.append(object)


DataHandler.startElementHandler = patch_startElementHandler
