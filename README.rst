********************
xmlschema-benchmarks
********************

A repository with a set of test scripts for comparing
`xmlschema <https://github.com/brunato/xmlschema>`_ performance
against to `lxml <https://github.com/lxml/lxml>`_'s *XMLSchema* validator.
The XSD/XML files used for comparison are from
`OneLogin's SAML Python Toolkit repository <https://github.com/onelogin/python3-saml>`_.

Available performance tests:

* *timing_schema_build.py* : performance on building of the SAML2 schemas
* *timing_validation.py* : performance on validation of SAML2 XML data

Results
=======

Performance comparison:

* Schemas build is ~70-80 times faster with lxml, only ~5 times with loading
  of serialized schemas with pickle;
* Validation is ~50 times faster with lxml

Even lxml is more faster with these types of schemas, xmlschema cover full XSD 1.0
and XSD 1.1 and has other protection features over malicious constructed XSD/XML
sources (eg. MAX_XML_DEPTH/MAX_MODEL_DEPTH).

Future improvements could be tentatives of using type-hints and optional
Cythonized modules.


License
=======

This software is distributed under the terms of the BSD 3-Clause License.
See the file 'LICENSE' in the root directory of the present distribution,
or https://opensource.org/licenses/BSD-3-Clause.
