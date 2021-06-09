#!/usr/bin/env python3
#
# BDS 3-clause licence, copyright 2020, SISSA
# @Author: Davide Brunato
#
"""
Performance comparison of SAML2 XSD and XML resource load.
"""
import os
from timeit import timeit


PROJECT_DIR = os.path.dirname(__file__)

SAML2_XSD_FILE = os.path.join(PROJECT_DIR, 'schemas/saml-schema-protocol-2.0.xsd')
SAML2_METADATA_XSD_FILE = os.path.join(PROJECT_DIR, 'schemas/saml-schema-metadata-2.0.xsd')

REQUEST_XML_FILE = os.path.join(PROJECT_DIR, 'data/authn_request.xml')
RESPONSE_XML_FILE = os.path.join(PROJECT_DIR, 'data/simple_saml_php.xml')
METADATA_XML_FILE = os.path.join(PROJECT_DIR, 'data/testshib-providers.xml')


def run_timeit(stmt='pass', setup='pass', number=10, compare=None):
    seconds = timeit(stmt, setup=setup, number=number)
    if compare is None:
        print("{}: {}s".format(stmt, seconds))
    else:
        print("{}: {}s ({:g}x)".format(stmt, seconds, seconds / compare))
    return seconds


print("### Performance test SAML2 XSD and XML data loading ###\n")


NUMBER = 1000

SETUP = 'import ' \
        'xml.etree.ElementTree as ElementTree, ' \
        'lxml.etree as etree, ' \
        'xmlschema\n' \
        'from __main__ import ' \
        'SAML2_XSD_FILE, ' \
        'SAML2_METADATA_XSD_FILE, ' \
        'REQUEST_XML_FILE, ' \
        'RESPONSE_XML_FILE, ' \
        'METADATA_XML_FILE'

run_timeit("xmlschema.XMLResource(SAML2_XSD_FILE)", setup=SETUP, number=NUMBER)
run_timeit("ElementTree.parse(SAML2_XSD_FILE)", setup=SETUP, number=NUMBER)
run_timeit("etree.parse(SAML2_XSD_FILE)", setup=SETUP, number=NUMBER)

print()

run_timeit("xmlschema.XMLResource(SAML2_METADATA_XSD_FILE)", setup=SETUP, number=NUMBER)
run_timeit("ElementTree.parse(SAML2_METADATA_XSD_FILE)", setup=SETUP, number=NUMBER)
run_timeit("etree.parse(SAML2_METADATA_XSD_FILE)", setup=SETUP, number=NUMBER)

print()

run_timeit("xmlschema.XMLResource(REQUEST_XML_FILE)", setup=SETUP, number=NUMBER)
run_timeit("ElementTree.parse(REQUEST_XML_FILE)", setup=SETUP, number=NUMBER)
run_timeit("etree.parse(REQUEST_XML_FILE)", setup=SETUP, number=NUMBER)

print()

run_timeit("xmlschema.XMLResource(RESPONSE_XML_FILE)", setup=SETUP, number=NUMBER)
run_timeit("ElementTree.parse(RESPONSE_XML_FILE)", setup=SETUP, number=NUMBER)
run_timeit("etree.parse(RESPONSE_XML_FILE)", setup=SETUP, number=NUMBER)

print()

run_timeit("xmlschema.XMLResource(METADATA_XML_FILE)", setup=SETUP, number=NUMBER)
run_timeit("ElementTree.parse(METADATA_XML_FILE)", setup=SETUP, number=NUMBER)
run_timeit("etree.parse(METADATA_XML_FILE)", setup=SETUP, number=NUMBER)

print()
