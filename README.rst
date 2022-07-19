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
* *timing_decoding.py* : performance on decoding SAML2 XML data
* *timing_xpath.py* : performance of XPath selection on SAML2 XML data
* *timing_resource.py*: performance on loading SAML2 schema and XML sources

Results
=======

Performance comparison:

* Schemas build is ~75 times faster with lxml, only ~4 times with loading
  of serialized schemas with pickle;
* Validation is ~42 times faster with lxml, but lxml validates an XML file
  that has 2 invalid base64 values;
* XPath selection is ~19 times faster with lxml (*)

Even lxml is more faster with these types of schemas, xmlschema covers full XSD 1.0
and XSD 1.1 and has other protection features over malicious constructed XSD/XML
sources (eg. MAX_XML_DEPTH/MAX_MODEL_DEPTH).
For XPath lxml has only selectors for XPath 1.0.

(*) The difference against the XPath selectors of the standard library is
higher but ElementTree doesn't have a full XPath processor.

Benchmarks comparison matrix
============================

+--------------------+------------------------+----------------------+-----------------+
| lxml VS xmlschema  | timing_schema_build.py | timing_validation.py | timing_xpath.py |
+====================+========================+======================+=================+
| xmlschema==1.4.1,  | ~78                    | ~57x                 | ~20x            |
| elementpath==2.0.5 |                        |                      |                 |
+--------------------+------------------------+----------------------+-----------------+
| xmlschema==1.5.3,  | ~75                    | ~42x                 | ~24x            |
| elementpath==2.1.4 |                        |                      |                 |
+--------------------+------------------------+----------------------+-----------------+
| xmlschema==1.6.4,  | ~75                    | ~42x                 | ~23x            |
| elementpath==2.2.3 |                        |                      |                 |
+--------------------+------------------------+----------------------+-----------------+
| xmlschema==1.7.1,  | ~75                    | ~42x                 | ~19x            |
| elementpath==2.3.0 |                        |                      |                 |
+--------------------+------------------------+----------------------+-----------------+
| xmlschema==1.11.3, | ~67x (Python 3.10.5),  | ~47x,                | ~25x,           |
| elementpath==2.5.3 | ~63x (Python 3.11.0b4) | ~43x                 | ~26x            |
+--------------------+------------------------+----------------------+-----------------+
| xmlschema==2.0.0,  | ~66x (Python 3.10.5),  | ~46x,                | ~25x,           |
| elementpath==3.0.0 | ~63x (Python 3.11.0b4) | ~43x                 | ~19x            |
+--------------------+------------------------+----------------------+-----------------+

License
=======

This software is distributed under the terms of the BSD 3-Clause License.
See the file 'LICENSE' in the root directory of the present distribution,
or https://opensource.org/licenses/BSD-3-Clause.
