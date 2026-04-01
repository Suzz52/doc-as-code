Traceability
============

V-Development Cycle (End-to-End)
--------------------------------

.. spec:: SYS.2 System Requirements Baseline
   :id: QDX-V-SYS2
   :status: active

   System requirements baseline from process area SYS.2.

.. spec:: SWE.1 Software Requirements Baseline
   :id: QDX-V-SWE1
   :status: active
   :implements: QDX-V-SYS2

   Software requirements decomposition and allocation from SYS.2.

.. spec:: SWE.2 Software Architecture Baseline
   :id: QDX-V-SWE2
   :status: active
   :implements: QDX-V-SWE1

   Architectural specification of software components and interfaces.

.. spec:: SWE.3 Software Detailed Design Baseline
   :id: QDX-V-SWE3
   :status: active
   :implements: QDX-V-SWE2

   Unit-level detailed design and behavior specification.

.. spec:: SWE.4 Unit Verification Baseline
   :id: QDX-V-SWE4
   :status: active
   :implements: QDX-V-SWE3

   Unit-level verification of SWE.3 detailed design.

.. spec:: SWE.5 Integration Verification Baseline
   :id: QDX-V-SWE5
   :status: active
   :implements: QDX-V-SWE4

   Interface and subsystem integration verification.

.. spec:: SWE.6 Qualification Verification Baseline
   :id: QDX-V-SWE6
   :status: active
   :implements: QDX-V-SWE5

   End-to-end software qualification against SWE.1 requirements.

.. needflow::
   :types: spec
   :filter: id.startswith('QDX-V-')
   :show_link_names:

V-Model Stage Chain Index
-------------------------

.. needtable::
   :types: spec
   :filter: id.startswith('QDX-V-')
   :columns: id, title, status, implements
   :sort: id

Process Artefact Indexes
------------------------

SYS.2 → SWE.1 (parent-child)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: id.startswith('QDX-SWE-')
   :columns: id, title, status, parent
   :sort: id

SWE.1 → SWE.2 (implemented-by)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: id.startswith('QDX-SWE-')
   :columns: id, title, implemented_by
   :sort: id

SWE.2 Specs
~~~~~~~~~~~

.. needtable::
   :types: spec
   :filter: id.startswith('QDX-SWA-SP-')
   :columns: id, title, status, implements
   :sort: id

SWE.4/SWE.5/SWE.6 Verification Specs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: spec
   :filter: id in ['QDX-SWE4-SPEC-001', 'QDX-SWE5-SPEC-001', 'QDX-SWE6-SPEC-001']
   :columns: id, title, status, verification, implements
   :sort: id
