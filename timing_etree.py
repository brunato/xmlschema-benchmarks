#!/usr/bin/env python3
#
# BDS 3-clause licence, copyright 2021, SISSA
# @Author: Davide Brunato
#
"""
Performance comparison of ElementTree iterations.
"""
from timeit import timeit
import lxml.etree as etree
from xmlschema.etree import ElementTree, PyElementTree


def run_timeit(stmt='pass', setup='pass', number=10, compare=None):
    seconds = timeit(stmt, setup=setup, number=number)
    if compare is None:
        print("{}: {}s".format(stmt, seconds))
    else:
        print("{}: {}s ({:g}x)".format(stmt, seconds, seconds / compare))
    return seconds


XML_DATA = '<a>' * 250 + '</a>' * 250
root = ElementTree.XML(XML_DATA)
py_root = PyElementTree.XML(XML_DATA)
lxml_root = etree.XML(XML_DATA)


def etree_iter(elem):
    iterators = []
    yield elem
    children = iter(elem)

    while True:
        try:
            e = next(children)
        except StopIteration:
            try:
                children = iterators.pop()
            except IndexError:
                return
        else:
            yield e
            if not len(e):
                continue
            iterators.append(children)
            children = iter(e)


def element_tree_iter():
    for _ in root.iter():
        pass


def py_element_tree_iter():
    for _ in py_root.iter():
        pass


def py_element_tree_iter2():
    for _ in etree_iter(py_root):
        pass


def lxml_etree_iter():
    for _ in lxml_root.iter():
        pass


NUMBER = 1000
SETUP = 'from __main__ import XML_DATA, etree, ElementTree, PyElementTree'

print()
t1 = run_timeit("ElementTree.XML(XML_DATA)", setup=SETUP, number=NUMBER)
run_timeit("PyElementTree.XML(XML_DATA)", setup=SETUP, number=NUMBER, compare=t1)
run_timeit("etree.XML(XML_DATA)", setup=SETUP, number=NUMBER, compare=t1)


SETUP = 'from __main__ import element_tree_iter, py_element_tree_iter, ' \
        'py_element_tree_iter2, lxml_etree_iter'

print()
t1 = run_timeit("element_tree_iter()", setup=SETUP, number=NUMBER)
run_timeit("py_element_tree_iter()", setup=SETUP, number=NUMBER, compare=t1)
run_timeit("py_element_tree_iter2()", setup=SETUP, number=NUMBER, compare=t1)
run_timeit("lxml_etree_iter()", setup=SETUP, number=NUMBER, compare=t1)
