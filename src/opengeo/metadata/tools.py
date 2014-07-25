import json
import os

_elements = {}
_schemes = {}

OBLIGATION_OPTIONAL = "optional"
OBLIGATION_CONDITIONAL = "conditional"
OBLIGATION_MANDATORY = "mandatory"

def elementObligation(name):
    name = name.split(":")[-1]
    elem = elements().get(name)
    if elem is None:
        return "optional"
    else:
        return elem.get("obligation", "optional")

def elementType(name):
    name = name.split(":")[-1]
    elem = elements().get(name)
    if elem is None:
        return "string"
    else:
        return elem.get("type", "string")

def elementLabel(name):
    name = name.split(":")[-1]
    elem = elements().get(name)
    if elem is None:
        return name
    else:
        return elem.get("label", name)

def elements():
    global _elements
    if not _elements:
        filename = os.path.join(os.path.dirname(__file__), "elements.json")
        with open(filename) as f:
            _elements = json.load(f)
    return _elements

def codelist(scheme):
    scheme = scheme.split(":")[-1]
    global _schemes
    if not _schemes is None:
        filename = os.path.join(os.path.dirname(__file__), "codelists.json")
        with open(filename) as f:
            _schemes = json.load(f)
    return _schemes.get(scheme, None)