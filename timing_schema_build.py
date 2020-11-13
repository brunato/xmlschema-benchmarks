#!/usr/bin/env python3
#
# BDS 3-clause licence, copyright 2020, SISSA
# @Author: Davide Brunato
#
"""
Performance comparison of SAML2 schema building with xmlschema and lxml.

Also pickle is used for considering performance improving for xmlschema.
Lxml's schema cannot be pickled.
"""
import os
from timeit import timeit
import lxml.etree as etree
import xmlschema
import pickle

PROJECT_DIR = os.path.dirname(__file__)

SAML2_XSD_FILE = os.path.join(PROJECT_DIR, 'schemas', 'saml-schema-protocol-2.0.xsd')
SAML2_METADATA_XSD_FILE = os.path.join(PROJECT_DIR, 'schemas', 'saml-schema-metadata-2.0.xsd')


def run_timeit(stmt='pass', setup='pass', number=10):
    print("{}: {}s".format(stmt, timeit(stmt, setup=setup, number=number)))


print("### Performance test XML Schema build of SAML2 schemas ###\n")


def xmlschema_build_saml2_schema_and_meta_schema():
    xs = xmlschema.XMLSchema10(SAML2_XSD_FILE)
    return xs


def xmlschema_build_saml2_schema():
    xs = xmlschema.XMLSchema10(SAML2_XSD_FILE)
    return xs


def xmlschema_build_saml2_metadata_schema():
    xs = xmlschema.XMLSchema10(SAML2_METADATA_XSD_FILE)
    return xs


def xmlschema_loads_saml2_schema():
    xs = pickle.loads(saml2_schema)
    return xs


def xmlschema_loads_saml2_metadata_schema():
    xs = pickle.loads(saml2_metadata_schema)
    return xs


def lxml_build_saml2_schema():
    xt = etree.parse(SAML2_XSD_FILE)
    xs = etree.XMLSchema(xt.getroot())
    return xs


def lxml_build_saml2_metadata_schema():
    xt = etree.parse(SAML2_METADATA_XSD_FILE)
    xs = etree.XMLSchema(xt.getroot())
    return xs


NUMBER = 10

SETUP = 'from __main__ import ' \
        'xmlschema_build_saml2_schema_and_meta_schema, ' \
        'xmlschema_build_saml2_schema, xmlschema_build_saml2_metadata_schema, ' \
        'xmlschema_loads_saml2_schema, xmlschema_loads_saml2_metadata_schema, ' \
        'lxml_build_saml2_schema, lxml_build_saml2_metadata_schema'

run_timeit("lxml_build_saml2_schema()", setup=SETUP, number=NUMBER)
run_timeit("lxml_build_saml2_metadata_schema()", setup=SETUP, number=NUMBER)

print()

run_timeit("xmlschema_build_saml2_schema_and_meta_schema()", setup=SETUP, number=NUMBER)

saml2_schema = pickle.dumps(xmlschema.XMLSchema10(SAML2_XSD_FILE))
saml2_metadata_schema = pickle.dumps(xmlschema.XMLSchema10(SAML2_METADATA_XSD_FILE))

run_timeit("xmlschema_build_saml2_schema()", setup=SETUP, number=NUMBER)
run_timeit("xmlschema_build_saml2_metadata_schema()", setup=SETUP, number=NUMBER)
run_timeit("xmlschema_loads_saml2_schema()", setup=SETUP, number=NUMBER)
run_timeit("xmlschema_loads_saml2_metadata_schema()", setup=SETUP, number=NUMBER)