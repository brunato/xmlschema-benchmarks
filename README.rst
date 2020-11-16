********************
xmlschema-benchmarks
********************

A repository with a set of test scripts for comparing
`xmlschema <https://github.com/sissaschool/xmlschema>`_ performance
against to `lxml <https://github.com/lxml/lxml>`_'s *XMLSchema* validator.
XPath selection comparison is operated between
`elementpath <https://github.com/sissaschool/elementpath>`_,
Python's standard library XPath selectors and lxml.

The XSD/XML files used for comparison are from
`OneLogin's SAML Python Toolkit repository <https://github.com/onelogin/python3-saml>`_.

Available performance tests:

* *timing_schema_build.py* : performance on building of the SAML2 schemas
* *timing_validation.py* : performance on validation of SAML2 XML data
* *timing_xpath.py* : performance of XPath selection on SAML2 XML data


Results
=======

Performance comparison:

* Schemas build is ~70-80 times faster with lxml, only ~5 times with loading
  of serialized schemas with pickle;
* Validation is ~63-77 times faster with lxml, but lxml validates an XML file
  that has 2 invalid base64 values;
* XPath selection is ~20-30 times faster with lxml and is ~60-85 times faster
  with ElementTree

Even lxml is more faster with these types of schemas, xmlschema covers full XSD 1.0
and XSD 1.1 and has other protection features over malicious constructed XSD/XML
sources (eg. MAX_XML_DEPTH/MAX_MODEL_DEPTH).

For XPath the difference against lxml is reduced, and lxml has only selectors for
XPath 1.0. The difference against the XPath selectors of the standard library is
higher but ElementTree doesn't have a full XPath processor.

Future improvements could be tentatives of using type-hints and optional
Cythonized modules.


License
=======

This software is distributed under the terms of the BSD 3-Clause License.
See the file 'LICENSE' in the root directory of the present distribution,
or https://opensource.org/licenses/BSD-3-Clause.
