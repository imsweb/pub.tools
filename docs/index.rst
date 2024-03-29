===================================
pub.tools
===================================

pub.tools provides a few useful functions, namely interacting with NCBI's PubMed APIs to get publication
information, and building citations out of publication metadata. We use dataclasses
to express the valid parameters for generating these publication citations, see the
`schema` section for details.


View the source code at `<https://github.com/imsweb/pub.tools>`_

.. toctree::
   :maxdepth: 2

   entrez
   citations
   schema
   formatting