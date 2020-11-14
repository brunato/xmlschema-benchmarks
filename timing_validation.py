#!/usr/bin/env python3
#
# BDS 3-clause licence, copyright 2020, SISSA
# @Author: Davide Brunato
#
"""
Performance comparison of SAML2 XML data validation with xmlschema and lxml.
"""
import os
from timeit import timeit
import lxml.etree as etree
import xmlschema


PROJECT_DIR = os.path.dirname(__file__)

SAML2_XSD_FILE = os.path.join(PROJECT_DIR, 'schemas/saml-schema-protocol-2.0.xsd')
SAML2_METADATA_XSD_FILE = os.path.join(PROJECT_DIR, 'schemas/saml-schema-metadata-2.0.xsd')

REQUEST_XML_FILE = os.path.join(PROJECT_DIR, 'data/authn_request.xml')
RESPONSE_XML_FILE = os.path.join(PROJECT_DIR, 'data/simple_saml_php.xml')
METADATA_XML_FILE = os.path.join(PROJECT_DIR, 'data/testshib-providers.xml')


def run_timeit(stmt='pass', setup='pass', number=10):
    print("{}: {}s".format(stmt, timeit(stmt, setup=setup, number=number)))


saml2_schema = xmlschema.XMLSchema10(SAML2_XSD_FILE)
saml2_metadata_schema = xmlschema.XMLSchema10(SAML2_METADATA_XSD_FILE)

saml2_lxml_schema = etree.XMLSchema(etree.parse(SAML2_XSD_FILE).getroot())
saml2_metadata_lxml_schema = etree.XMLSchema(etree.parse(SAML2_METADATA_XSD_FILE).getroot())


print("### Performance test SAML2 XML data validation ###\n")


def xmlschema_validate_request():
    saml2_schema.validate(REQUEST_XML_FILE)


def xmlschema_validate_response():
    # data/simple_saml_php.xml has 2 invalid base64 values:
    #   'LHNK1FJfcOIUuWVKJmGABQ+W98+pQ=='
    #   'LqkW39SOYbttYxlGhIBw=='
    # these 2 errors are confirmed by Xerces but lxml doesn't detect them.
    assert len(list(saml2_schema.iter_errors(RESPONSE_XML_FILE))) == 2


def xmlschema_validate_metadata():
    saml2_metadata_schema.validate(METADATA_XML_FILE)


def lxml_validate_request():
    xt = etree.parse(REQUEST_XML_FILE)
    saml2_lxml_schema.validate(xt.getroot())


def lxml_validate_response():
    xt = etree.parse(RESPONSE_XML_FILE)
    saml2_lxml_schema.validate(xt.getroot())


def lxml_validate_metadata():
    xt = etree.parse(METADATA_XML_FILE)
    saml2_lxml_schema.validate(xt.getroot())


NUMBER = 10

SETUP = 'from __main__ import ' \
        'xmlschema_validate_request, ' \
        'xmlschema_validate_response, ' \
        'xmlschema_validate_metadata, ' \
        'lxml_validate_request, ' \
        'lxml_validate_response, ' \
        'lxml_validate_metadata'


run_timeit("lxml_validate_request()", setup=SETUP, number=NUMBER)
run_timeit("lxml_validate_response()", setup=SETUP, number=NUMBER)
run_timeit("lxml_validate_metadata()", setup=SETUP, number=NUMBER)

print()

run_timeit("xmlschema_validate_request()", setup=SETUP, number=NUMBER)
run_timeit("xmlschema_validate_response()", setup=SETUP, number=NUMBER)
run_timeit("xmlschema_validate_metadata()", setup=SETUP, number=NUMBER)
