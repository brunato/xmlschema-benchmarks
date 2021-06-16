#!/usr/bin/env python
#
# BDS 3-clause licence, copyright 2020, SISSA
# @Author: Davide Brunato
#
"""
Performance comparison of SAML2 XML data decoding with xmlschema and lxml validation.
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


def run_timeit(stmt='pass', setup='pass', number=10, compare=None):
    seconds = timeit(stmt, setup=setup, number=number)
    if compare is None:
        print("{}: {}s".format(stmt, seconds))
    else:
        print("{}: {}s ({:g}x)".format(stmt, seconds, seconds / compare))
    return seconds


saml2_schema = xmlschema.XMLSchema10(SAML2_XSD_FILE)
saml2_metadata_schema = xmlschema.XMLSchema10(SAML2_METADATA_XSD_FILE)

saml2_lxml_schema = etree.XMLSchema(etree.parse(SAML2_XSD_FILE).getroot())
saml2_metadata_lxml_schema = etree.XMLSchema(etree.parse(SAML2_METADATA_XSD_FILE).getroot())


print("### Performance test SAML2 XML data decoding ###\n")


def xmlschema_decode_request():
    saml2_schema.validate(REQUEST_XML_FILE)


def xmlschema_decode_response():
    # data/simple_saml_php.xml has 2 invalid base64 values:
    #   'LHNK1FJfcOIUuWVKJmGABQ+W98+pQ=='
    #   'LqkW39SOYbttYxlGhIBw=='
    # these 2 errors are confirmed by Xerces but lxml doesn't detect them.
    _, errors = saml2_schema.decode(RESPONSE_XML_FILE, validation='lax')
    assert len(errors) == 2


def xmlschema_decode_metadata():
    saml2_metadata_schema.decode(METADATA_XML_FILE)


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
        'xmlschema_decode_request, ' \
        'xmlschema_decode_response, ' \
        'xmlschema_decode_metadata, ' \
        'lxml_validate_request, ' \
        'lxml_validate_response, ' \
        'lxml_validate_metadata'

t1 = [run_timeit("lxml_validate_request()", setup=SETUP, number=NUMBER),
      run_timeit("lxml_validate_response()", setup=SETUP, number=NUMBER),
      run_timeit("lxml_validate_metadata()", setup=SETUP, number=NUMBER)]

print()

t2 = [run_timeit("xmlschema_decode_request()", setup=SETUP, number=NUMBER, compare=t1[0]),
      run_timeit("xmlschema_decode_response()", setup=SETUP, number=NUMBER, compare=t1[1]),
      run_timeit("xmlschema_decode_metadata()", setup=SETUP, number=NUMBER, compare=t1[2])]

print()

print('lxml is about {:g} times faster than xmlschema (only-validation for lxml)'.format(sum(t2) / sum(t1)))
