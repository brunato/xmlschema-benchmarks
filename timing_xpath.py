#!/usr/bin/env python
#
# BDS 3-clause licence, copyright 2020, SISSA
# @Author: Davide Brunato
#
"""
Performance comparison of XPath selection on SAML2 XML data with elementpath,
xml.etree.ElementPath and lxml.
"""
import os
from timeit import timeit
from xml.etree import ElementTree
import lxml.etree as etree
from elementpath import select, XPath1Parser


PROJECT_DIR = os.path.dirname(__file__)

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


request_root = ElementTree.parse(REQUEST_XML_FILE).getroot()
response_root = ElementTree.parse(RESPONSE_XML_FILE).getroot()
metadata_root = ElementTree.parse(METADATA_XML_FILE).getroot()

request_lxml_root = etree.parse(REQUEST_XML_FILE).getroot()
response_lxml_root = etree.parse(RESPONSE_XML_FILE).getroot()
metadata_lxml_root = etree.parse(METADATA_XML_FILE).getroot()

value = 'http://www.w3.org/2001/04/xmlenc#rsa-oaep-mgf1p'
namespaces = {'md': 'urn:oasis:names:tc:SAML:2.0:metadata'}

path1 = "/md:EntitiesDescriptor/md:EntityDescriptor/md:SPSSODescriptor/" \
        "md:KeyDescriptor/md:EncryptionMethod[@Algorithm={!r}]".format(value)

XPath1Parser.build()

print("### Performance test of XPath selection over SAML2 XML data ###\n")


def elementpath_path_with_predicate():
    results = select(metadata_root, path1, namespaces, parser=XPath1Parser)
    assert len(results) == 1
    assert results[0] is metadata_root[1][1][1][9]
    assert results[0].get('Algorithm') == value


def element_tree_path_with_predicate():
    results = metadata_root.findall(path1[23:], namespaces=namespaces)
    assert len(results) == 1
    assert results[0] is metadata_root[1][1][1][9]
    assert results[0].get('Algorithm') == value


def lxml_etree_path_with_predicate():
    results = metadata_lxml_root.xpath(path1, namespaces=namespaces)
    assert len(results) == 1
    assert results[0] is metadata_lxml_root[5][2][1][9]
    assert results[0].get('Algorithm') == value


def elementpath_lxml_path_with_predicate():
    results = select(metadata_lxml_root, path1, namespaces, parser=XPath1Parser)
    assert len(results) == 1
    assert results[0] is metadata_lxml_root[5][2][1][9]
    assert results[0].get('Algorithm') == value


def elementpath_descendants():
    results = select(response_root, './/*', parser=XPath1Parser)
    assert len(results) == 46


def element_tree_descendants():
    results = response_root.findall('.//*')
    assert len(results) == 46


def lxml_etree_descendants():
    results = response_lxml_root.xpath('.//*')
    assert len(results) == 46


def elementpath_lxml_descendants():
    results = select(response_lxml_root, './/*', parser=XPath1Parser)
    assert len(results) == 46


NUMBER = 300

SETUP = 'from __main__ import ' \
        'elementpath_path_with_predicate, ' \
        'element_tree_path_with_predicate, ' \
        'lxml_etree_path_with_predicate, ' \
        'elementpath_lxml_path_with_predicate, ' \
        'elementpath_descendants, ' \
        'element_tree_descendants, ' \
        'lxml_etree_descendants, ' \
        'elementpath_lxml_descendants'


run_timeit("element_tree_path_with_predicate()", setup=SETUP, number=NUMBER)
t1 = run_timeit("lxml_etree_path_with_predicate()", setup=SETUP, number=NUMBER)
run_timeit("elementpath_path_with_predicate()", setup=SETUP, number=NUMBER, compare=t1)
run_timeit("elementpath_lxml_path_with_predicate()", setup=SETUP, number=NUMBER, compare=t1)

print()

run_timeit("element_tree_descendants()", setup=SETUP, number=NUMBER)
t2 = run_timeit("lxml_etree_descendants()", setup=SETUP, number=NUMBER)
run_timeit("elementpath_descendants()", setup=SETUP, number=NUMBER, compare=t2)
run_timeit("elementpath_lxml_descendants()", setup=SETUP, number=NUMBER, compare=t2)
