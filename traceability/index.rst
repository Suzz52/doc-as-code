.. ============================================================
.. QORIX DEVELOPER — Traceability Index
.. ASPICE: V-Cycle End-to-End (SYS.2 → SWE.1 → SWE.2 → SWE.3
..          → SWE.4 → SWE.5 → SWE.6)
.. ============================================================

Traceability
============

V-Development Cycle (End-to-End)
---------------------------------

.. spec:: SYS.2 System Requirements Baseline
   :id: QDX-V-SYS2
   :status: active
   :links_from: sys_requirements

   System requirements baseline from process area SYS.2.
   Source document: :ref:`sys_requirements` (QDX-SRS-001).

.. spec:: SWE.1 Software Requirements Baseline
   :id: QDX-V-SWE1
   :status: active
   :implements: QDX-V-SYS2
   :links_from: sw_requirements

   Software requirements decomposition and allocation from SYS.2.
   Source document: :ref:`sw_requirements` (QDX-SWE-DOC-001).

.. spec:: SWE.2 Software Architecture Baseline
   :id: QDX-V-SWE2
   :status: active
   :implements: QDX-V-SWE1
   :links_from: sw_architecture

   Architectural specification of software components and interfaces.
   Source document: :ref:`sw_architecture` (QDX-SWA-DOC-001).

.. spec:: SWE.3 Software Detailed Design Baseline
   :id: QDX-V-SWE3
   :status: active
   :implements: QDX-V-SWE2
   :links_from: sw_detailed_design

   Unit-level detailed design and behavior specification.
   Source document: :ref:`sw_detailed_design` (QDX-SDD-DOC-001).

.. spec:: SWE.4 Unit Verification Baseline
   :id: QDX-V-SWE4
   :status: active
   :implements: QDX-V-SWE3
   :links_from: sw_unit_verification

   Unit-level verification of SWE.3 detailed design.
   Source document: :ref:`sw_unit_verification` (QDX-SWE4-DOC-001).

.. spec:: SWE.5 Integration Verification Baseline
   :id: QDX-V-SWE5
   :status: active
   :implements: QDX-V-SWE4
   :links_from: sw_integration_test

   Interface and subsystem integration verification.
   Source document: :ref:`sw_integration_test` (QDX-SWE5-DOC-001).

.. spec:: SWE.6 Qualification Verification Baseline
   :id: QDX-V-SWE6
   :status: active
   :implements: QDX-V-SWE5
   :links_from: sw_qualification_test

   End-to-end software qualification against SWE.1 requirements.
   Source document: :ref:`sw_qualification_test` (QDX-SWE6-DOC-001).

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


Document Cross-Reference Map
-----------------------------

.. list-table::
   :widths: 20 20 20 20 20
   :header-rows: 1

   * - Process Stage
     - Document ID
     - Document Title
     - RST Ref Target
     - Parent Document
   * - SYS.2
     - QDX-SRS-001
     - System Requirements Specification
     - :ref:`sys_requirements`
     - — (top of V-cycle)
   * - SWE.1
     - QDX-SWE-DOC-001
     - Software Requirements Specification
     - :ref:`sw_requirements`
     - :ref:`sys_requirements`
   * - SWE.2
     - QDX-SWA-DOC-001
     - Software Architecture Description
     - :ref:`sw_architecture`
     - :ref:`sw_requirements`
   * - SWE.3
     - QDX-SDD-DOC-001
     - Software Detailed Design
     - :ref:`sw_detailed_design`
     - :ref:`sw_architecture` + :ref:`sw_requirements`
   * - SWE.4
     - QDX-SWE4-DOC-001
     - Software Unit Verification Specification
     - :ref:`sw_unit_verification`
     - :ref:`sw_detailed_design`
   * - SWE.5
     - QDX-SWE5-DOC-001
     - Software Integration Test Specification
     - :ref:`sw_integration_test`
     - :ref:`sw_architecture`
   * - SWE.6
     - QDX-SWE6-DOC-001
     - Software Qualification Test Specification
     - :ref:`sw_qualification_test`
     - :ref:`sw_requirements` + :ref:`sw_integration_test`


Process Artefact Indexes
------------------------

SYS.2 → SWE.1 (system-to-software requirements)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: id.startswith('QDX-SWE-') and not id.startswith('QDX-SWE-DOC')
   :columns: id, title, status, parent
   :sort: id

SWE.1 → SWE.2 (requirements implemented by architecture specs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: id.startswith('QDX-SWE-') and not id.startswith('QDX-SWE-DOC')
   :columns: id, title, implemented_by
   :sort: id

SWE.2 Architecture Specs
~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: spec
   :filter: id.startswith('QDX-SWA-SP-')
   :columns: id, title, status, implements
   :sort: id

SWE.4 / SWE.5 / SWE.6 Verification Specs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: spec
   :filter: id in ['QDX-SWE4-SPEC-001', 'QDX-SWE5-SPEC-001', 'QDX-SWE6-SPEC-001']
   :columns: id, title, status, verification, implements
   :sort: id


Full V-Cycle Traceability Summary
----------------------------------

.. list-table::
   :widths: 18 18 16 16 16 16
   :header-rows: 1

   * - SYS.2 (SRS)
     - SWE.1 (SRS)
     - SWE.2 (SAD)
     - SWE.3 (SDD)
     - SWE.4 (UT)
     - SWE.5 (IT) → SWE.6 (QT)
   * - QDX-SYS-001
     - QDX-SWE-001
     - QDX-SWA-SP-001
     - workspace_manager::open
     - QDX-UT-001 to 003
     - — → QDX-QT-001
   * - QDX-SYS-002
     - QDX-SWE-002
     - QDX-SWA-SP-002
     - workspace_manager::scaffold_project
     - QDX-UT-004 to 008
     - — → QDX-QT-002
   * - QDX-SYS-003
     - QDX-SWE-003
     - QDX-SWA-SP-003
     - project structure (SWE.3 §4.2)
     - —
     - — → QDX-QT-003
   * - QDX-SYS-004 (partial)
     - QDX-SWE-004
     - QDX-SWA-SP-004
     - core::yaml::load
     - QDX-UT-026 to 028
     - — → QDX-QT-004
   * - QDX-SYS-033
     - QDX-SWE-005
     - QDX-SWA-SP-005
     - core::yaml::atomic_save
     - QDX-UT-029 to 031
     - — → QDX-QT-005
   * - QDX-SYS-006
     - QDX-SWE-031
     - QDX-SWA-SP-031
     - wasm_bridge::validate_yaml
     - QDX-UT-012 to 015
     - QDX-IT-003 → QDX-QT-031
   * - QDX-SYS-007
     - QDX-SWE-032
     - QDX-SWA-SP-032
     - domain_service::load_workspace
     - QDX-UT-041 to 043
     - QDX-IT-004 → QDX-QT-032
   * - QDX-SYS-009
     - QDX-SWE-038
     - QDX-SWA-SP-038
     - domain_service::generate
     - QDX-UT-046
     - QDX-IT-006 → QDX-QT-038
   * - QDX-SYS-016
     - QDX-SWE-047 to 050
     - QDX-SWA-SP-047 to 050
     - intent_router::route
     - QDX-UT-053 to 056
     - QDX-IT-010, 015 → QDX-QT-047 to 050
   * - QDX-SYS-007
     - QDX-SWE-069
     - QDX-SWA-SP-069
     - bpct::validation::VR007WatchdogRule
     - QDX-UT-062 to 065
     - QDX-IT-013 → QDX-QT-069
   * - QDX-SYS-007
     - QDX-SWE-084
     - QDX-SWA-SP-084
     - lwbsw::validation::ResourceBudgetRule
     - QDX-UT-069 to 071
     - — → QDX-QT-084


Requirement Coverage Statistics
---------------------------------

.. list-table::
   :widths: 20 20 20 20 20
   :header-rows: 1

   * - SYS.2 total
     - SWE.1 total
     - SWE.2 arch spec total
     - SWE.4 UT total
     - SWE.5 IT / SWE.6 QT total
   * - 44 requirements
     - 101 requirements
     - 101 architecture specs
     - 79 unit tests
     - 21 integration tests / 101 qualification tests

All ``QDX-SWE-NNN`` software requirements derive from a ``QDX-SYS-NNN``
system requirement.  Each ``QDX-SWE-NNN`` is realised by exactly one
``QDX-SWA-SP-NNN`` architecture specification and verified by one
``QDX-QT-NNN`` qualification test.  79 unit tests (``QDX-UT-NNN``) cover
the SWE.3 detailed design functions.  21 integration tests
(``QDX-IT-NNN``) verify subsystem interface boundaries.

See the per-document traceability matrices:

- **SYS.2 ↔ SWE.1**: :ref:`sw_requirements` §6 (traceability matrix)
- **SWE.2 ↔ SWE.1**: :ref:`sw_architecture` §7 (architecture traceability matrix)
- **SWE.3 ↔ SWE.1/SWE.2**: :ref:`sw_detailed_design` §11 (SWE.3 traceability matrix)
- **SWE.4 ↔ SWE.3**: :ref:`sw_unit_verification` §3 (unit test catalogue)
- **SWE.5 ↔ SWE.2**: :ref:`sw_integration_test` §3 (integration test cases)
- **SWE.6 ↔ SWE.1**: :ref:`sw_qualification_test` §3 (qualification test cases)
