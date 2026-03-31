Traceability
============

SYS.2 → SWE.1 (parent-child)
----------------------------

.. needtable::
   :types: req
   :filter: id.startswith("QDX-SWE-")
   :columns: id, title, status, parent
   :sort: id

SWE.1 → SWE.2 (implemented-by)
------------------------------

.. needtable::
   :types: req
   :filter: id.startswith("QDX-SWE-")
   :columns: id, title, implemented_by
   :sort: id

SWE.2 Specs
-----------

.. needtable::
   :types: spec
   :columns: id, title, status, implements
   :sort: id
