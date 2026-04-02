.. ============================================================
.. QORIX DEVELOPER — Traceability Index
.. ASPICE: Full V-Cycle + Supporting Processes
.. Covers: SYS.1 · SYS.2 · SYS.3 · SYS.4 · SYS.5
..          SWE.1 · SWE.2 · SWE.3 · SWE.4 · SWE.5 · SWE.6
..          VAL.1 · SUP.1 · SUP.8 · SUP.9 · SUP.10
..          MAN.3 · MAN.5 · MAN.6 · PIM.3
.. ============================================================

Traceability
============

V-Development Cycle (End-to-End)
---------------------------------

.. admonition:: ASPICE process coverage

   This index covers the complete ASPICE V-model as shown in the
   Automotive SPICE process reference model. Nodes marked **(in progress)**
   are planned documents with defined owners and target dates in the
   roadmap. All spec blocks below are machine-readable sphinx-needs
   objects — the ``needflow`` and ``needtable`` directives below render
   live dependency graphs from them.

System engineering branch (left side of V)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. spec:: SYS.1 Stakeholder Requirements Elicitation
   :id: QDX-V-SYS1
   :status: in-progress
   :links_from: —

   Stakeholder requirements elicitation output — source of all SYS.2
   system requirements. Document: QDX-SER-001 (in progress).
   Owner: Product Management + Architecture Team.
   Target: 2026-Q3.

.. spec:: SYS.2 System Requirements Baseline
   :id: QDX-V-SYS2
   :status: active
   :implements: QDX-V-SYS1
   :links_from: sys_requirements

   System requirements baseline from process area SYS.2.
   Source document: :ref:`sys_requirements` (QDX-SRS-001).
   44 requirements, all traceable to SWE.1 software requirements.

.. spec:: SYS.3 System Architectural Design
   :id: QDX-V-SYS3
   :status: in-progress
   :implements: QDX-V-SYS2

   System-level architecture describing hardware + software subsystem
   decomposition, physical deployment topology and system interfaces.
   Document: QDX-SYS3-DOC-001 (in progress).
   Owner: Architecture Team. Target: 2026-Q3.

Software engineering branch (left side of V)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. spec:: SWE.1 Software Requirements Baseline
   :id: QDX-V-SWE1
   :status: active
   :implements: QDX-V-SYS2
   :links_from: sw_requirements

   Software requirements decomposition and allocation from SYS.2.
   Source document: :ref:`sw_requirements` (QDX-SWE-DOC-001).
   101 requirements — one per QDX-SWE-NNN. All carry ``:parent:``
   (SYS.2), ``:val_test:`` (VAL.1) and ``:cr_id:`` (SUP.10) fields.

.. spec:: SWE.2 Software Architecture Baseline
   :id: QDX-V-SWE2
   :status: active
   :implements: QDX-V-SWE1
   :links_from: sw_architecture

   Architectural specification of software components and interfaces.
   Source document: :ref:`sw_architecture` (QDX-SWA-DOC-001).
   101 ``QDX-SWA-SP-NNN`` architecture specs, each carrying ``:sys_req:``
   (SYS.2), ``:implements:`` (SWE.1) and ``:cr_id:`` (SUP.10) fields.

.. spec:: SWE.3 Software Detailed Design Baseline
   :id: QDX-V-SWE3
   :status: active
   :implements: QDX-V-SWE2
   :links_from: sw_detailed_design

   Unit-level detailed design and behaviour specification.
   Source document: :ref:`sw_detailed_design` (QDX-SDD-DOC-001).
   79 unit test anchors (QDX-UT-NNN) defined across six SDD documents.

Verification branch (right side of V)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. spec:: SWE.4 Unit Verification Baseline
   :id: QDX-V-SWE4
   :status: active
   :implements: QDX-V-SWE3
   :links_from: sw_unit_verification

   Unit-level verification of SWE.3 detailed design.
   Source document: :ref:`sw_unit_verification` (QDX-SWE4-DOC-001).
   79 unit tests, ≥ 80% line coverage target per crate.

.. spec:: SWE.5 Integration Verification Baseline
   :id: QDX-V-SWE5
   :status: active
   :implements: QDX-V-SWE4
   :links_from: sw_integration_test

   Software subsystem interface and integration verification.
   Source document: :ref:`sw_integration_test` (QDX-SWE5-DOC-001).
   21 integration tests across 6 stages with real (not mocked) counterparts.

.. spec:: SWE.6 Software Qualification Test Baseline
   :id: QDX-V-SWE6
   :status: active
   :implements: QDX-V-SWE5
   :links_from: sw_qualification_test

   End-to-end software qualification against SWE.1 requirements.
   Source document: :ref:`sw_qualification_test` (QDX-SWE6-DOC-001).
   101 test cases (QDX-QT-NNN), one per SWE.1 requirement.
   Each test block carries ``:sys_req:`` and ``:val_test:`` fields.

.. spec:: SYS.4 System Integration and Verification
   :id: QDX-V-SYS4
   :status: in-progress
   :implements: QDX-V-SYS3

   System-level integration test verifying assembled system across
   hardware, OS, IDE host and external tool (ARTOP, Git, CI runner)
   boundaries. Document: QDX-SYS4-DOC-001 (in progress).
   Owner: Platform Engineering + QA. Target: 2026-Q4.

.. spec:: SYS.5 System Verification Baseline
   :id: QDX-V-SYS5
   :status: in-progress
   :implements: QDX-V-SYS4

   Verification that the integrated system satisfies SYS.2 requirements
   on the released platform build in a representative environment.
   Document: QDX-SYS5-DOC-001 (in progress). Test IDs: QDX-SVT-NNN.
   Owner: QA / Validation Team. Target: 2026-Q4.

.. spec:: VAL.1 Validation Baseline
   :id: QDX-V-VAL1
   :status: in-progress
   :implements: QDX-V-SYS2

   Validation that the complete system satisfies original stakeholder
   needs in representative operational conditions. Distinct from SWE.6
   (software built correctly) — VAL.1 asks whether the right software
   was built. Document: QDX-VAL-001 (in progress). Test IDs: QDX-VAT-NNN.
   Owner: Product Management + QA. Target: 2026-Q4.

.. needflow::
   :types: spec
   :filter: id.startswith('QDX-V-')
   :show_link_names:

V-Model Stage Chain Index
--------------------------

.. needtable::
   :types: spec
   :filter: id.startswith('QDX-V-')
   :columns: id, title, status, implements
   :sort: id


Document Cross-Reference Map
-----------------------------

.. list-table::
   :widths: 8 18 28 22 24
   :header-rows: 1

   * - Process
     - Document ID
     - Document Title
     - RST Ref / Status
     - Parent Documents
   * - SYS.1
     - QDX-SER-001
     - Stakeholder Requirements Elicitation
     - *In progress*
     - — (top of V-cycle)
   * - SYS.2
     - QDX-SRS-001
     - System Requirements Specification
     - :ref:`sys_requirements`
     - QDX-SER-001 (SYS.1)
   * - SYS.3
     - QDX-SYS3-DOC-001
     - System Architecture Description
     - *In progress*
     - QDX-SRS-001 (SYS.2)
   * - SWE.1
     - QDX-SWE-DOC-001
     - Software Requirements Specification
     - :ref:`sw_requirements`
     - QDX-SRS-001 (SYS.2) + QDX-SYS3-DOC-001 (SYS.3)
   * - SWE.2
     - QDX-SWA-DOC-001
     - Software Architecture Description
     - :ref:`sw_architecture`
     - QDX-SWE-DOC-001 (SWE.1) + QDX-SYS3-DOC-001 (SYS.3)
   * - SWE.3
     - QDX-SDD-DOC-001
     - Software Detailed Design
     - :ref:`sw_detailed_design`
     - QDX-SWA-DOC-001 (SWE.2) + QDX-SWE-DOC-001 (SWE.1)
   * - SWE.4
     - QDX-SWE4-DOC-001
     - Software Unit Verification Specification
     - :ref:`sw_unit_verification`
     - QDX-SDD-DOC-001 (SWE.3)
   * - SWE.5
     - QDX-SWE5-DOC-001
     - Software Integration Test Specification
     - :ref:`sw_integration_test`
     - QDX-SWA-DOC-001 (SWE.2)
   * - SWE.6
     - QDX-SWE6-DOC-001
     - Software Qualification Test Specification
     - :ref:`sw_qualification_test`
     - QDX-SWE-DOC-001 (SWE.1)
   * - SYS.4
     - QDX-SYS4-DOC-001
     - System Integration Test Specification
     - *In progress*
     - QDX-SYS3-DOC-001 (SYS.3)
   * - SYS.5
     - QDX-SYS5-DOC-001
     - System Verification Specification
     - *In progress*
     - QDX-SRS-001 (SYS.2)
   * - VAL.1
     - QDX-VAL-001
     - Validation Plan and Test Records
     - *In progress*
     - QDX-SRS-001 (SYS.2) + QDX-SER-001 (SYS.1)


Process Artefact Indexes
------------------------

SYS.1 → SYS.2 (elicitation → system requirements)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: id.startswith('QDX-SYS-')
   :columns: id, title, status, elicited_from, sys_arch
   :sort: id

SYS.2 → SWE.1 (system-to-software requirements)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: id.startswith('QDX-SWE-') and not id.startswith('QDX-SWE-DOC')
   :columns: id, title, status, parent, val_test
   :sort: id

SWE.1 → SWE.2 (requirements implemented by architecture specs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: spec
   :filter: id.startswith('QDX-SWA-SP-')
   :columns: id, title, status, implements, sys_req, cr_id
   :sort: id

SWE.2 → SWE.3 / SWE.4 (design and unit verification)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: req
   :filter: id.startswith('QDX-SWE-') and not id.startswith('QDX-SWE-DOC')
   :columns: id, title, verification
   :sort: id

SWE.5 Integration Tests (subsystem interface verification)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: spec
   :filter: id.startswith('QDX-IT-') or id.startswith('QDX-SWE5')
   :columns: id, title, status, implements
   :sort: id

SWE.6 → SWE.1 → SYS.2 (qualification test chain)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: spec
   :filter: id.startswith('QDX-QT-') or id.startswith('QDX-SWE6')
   :columns: id, title, status, implements
   :sort: id

SYS.5 System Verification Tests (pending QDX-SYS5-DOC-001)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: spec
   :filter: id.startswith('QDX-SVT-')
   :columns: id, title, status, implements
   :sort: id

VAL.1 Validation Tests (pending QDX-VAL-001)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. needtable::
   :types: spec
   :filter: id.startswith('QDX-VAT-')
   :columns: id, title, status, implements
   :sort: id


Supporting Process Compliance Index
-------------------------------------

This section serves as the ASPICE supporting process compliance index.
Each row shows the current coverage status for assessors reviewing
processes outside the primary V-cycle engineering activities.

.. list-table::
   :widths: 10 18 18 20 34
   :header-rows: 1

   * - Process
     - Document
     - Status
     - Owner
     - Coverage summary
   * - **SUP.1**
     - QDX-QAP-001
     - In progress
     - QA Lead
     - Quality Assurance Plan. Partial: sphinx-needs traceability chain
       provides objective evidence. Missing: formal QA plan, independent QA
       role definition, audit schedule and work product conformance criteria.
   * - **SUP.8**
     - Git + CODEOWNERS
     - Active
     - All crate leads
     - Configuration Management. Fully covered: YAML-as-source-of-truth
       in Git, PR reviews enforced by CODEOWNERS, atomic saves prevent
       partial-write corruption, ``provenance.json`` records every
       generation baseline.
   * - **SUP.9**
     - QDX-PRM-001
     - In progress
     - Platform Engineering Lead
     - Problem Resolution Management. Jira exists but lacks a formally
       defined state machine (Detected → Analysed → Root Cause →
       Resolved → Verified → Closed) with severity classification
       and escalation criteria.
   * - **SUP.10**
     - QDX-CRM-001
     - In progress
     - Architecture + PM
     - Change Request Management. ``:cr_id:`` fields added to all
       ``.. req::`` and ``.. spec::`` blocks. Jira CR workflow to be
       formally defined with impact analysis, approval and verification
       states.
   * - **SUP.11**
     - N/A (conditional)
     - Not required
     - AI/MCP Lead
     - Machine Learning Data Management. Only required if Qorix trains
       its own ML model. Current Qorix Agent uses external LLM as a
       service. Reassess when/if MLE.1–4 scope is adopted.
   * - **MAN.3**
     - QDX-PMP-001
     - In progress
     - Program Management
     - Project Management. Roadmap RST exists. Missing: formal project
       management plan with estimation method, resource allocation,
       milestone tracking and progress monitoring criteria.
   * - **MAN.5**
     - QDX-RMP-001
     - In progress
     - Program Management
     - Risk Management. ``:risk_id:`` fields added to 6 safety/AI/
       performance requirements in QDX-SRS-001. Formal risk register
       and mitigation tracking plan in progress.
   * - **MAN.6**
     - QDX-MEA-001
     - In progress
     - QA Lead
     - Measurement. No measurement program currently. Plan: define
       process metrics (requirement stability index, test pass rate,
       open defect count by severity, CI failure rate), collection method,
       action thresholds and a dashboard table in the portal.
   * - **PIM.3**
     - QDX-PIM-001
     - In progress
     - Architecture + QA
     - Process Improvement. No formal improvement program. Plan: define
       improvement opportunity identification process, planning and
       effectiveness verification at each quarterly milestone.


Full V-Cycle Traceability Chain
---------------------------------

Representative rows showing the complete chain from SYS.1 stakeholder
input through to VAL.1 validation evidence for selected requirements.

.. list-table::
   :widths: 9 9 11 11 10 10 10 10 10 10
   :header-rows: 1

   * - SYS.1 source
     - SYS.2 req
     - SWE.1 req
     - SWE.2 spec
     - SWE.3 fn
     - SWE.4 UT
     - SWE.5 IT
     - SWE.6 QT
     - SYS.5 SVT
     - VAL.1 VAT
   * - QDX-SER-001
     - QDX-SYS-001
     - QDX-SWE-001
     - QDX-SWA-SP-001
     - workspace_manager ::open
     - QDX-UT-001–003
     - —
     - QDX-QT-001
     - QDX-SVT-001
     - QDX-VAT-001
   * - QDX-SER-001
     - QDX-SYS-006
     - QDX-SWE-031
     - QDX-SWA-SP-031
     - wasm_bridge ::validate_yaml
     - QDX-UT-012–015
     - QDX-IT-003
     - QDX-QT-031
     - QDX-SVT-006
     - QDX-VAT-031
   * - QDX-SER-001
     - QDX-SYS-007
     - QDX-SWE-032
     - QDX-SWA-SP-032
     - domain_service ::load_workspace
     - QDX-UT-041–043
     - QDX-IT-004
     - QDX-QT-032
     - QDX-SVT-007
     - QDX-VAT-032
   * - QDX-SER-001
     - QDX-SYS-009
     - QDX-SWE-038
     - QDX-SWA-SP-038
     - domain_service ::generate
     - QDX-UT-046
     - QDX-IT-006
     - QDX-QT-038
     - QDX-SVT-009
     - QDX-VAT-038
   * - QDX-SER-001
     - QDX-SYS-016
     - QDX-SWE-047
     - QDX-SWA-SP-047
     - intent_router ::route
     - QDX-UT-053–056
     - QDX-IT-010, 015
     - QDX-QT-047
     - QDX-SVT-016
     - QDX-VAT-047
   * - QDX-SER-001
     - QDX-SYS-007
     - QDX-SWE-069
     - QDX-SWA-SP-069
     - VR007WatchdogRule ::check
     - QDX-UT-062–065
     - QDX-IT-013
     - QDX-QT-069
     - QDX-SVT-007b
     - QDX-VAT-069
   * - QDX-SER-001
     - QDX-SYS-007
     - QDX-SWE-084
     - QDX-SWA-SP-084
     - ResourceBudgetRule ::check
     - QDX-UT-069–071
     - QDX-IT-017
     - QDX-QT-084
     - QDX-SVT-007c
     - QDX-VAT-084


Coverage Statistics
--------------------

.. list-table::
   :widths: 20 16 16 16 16 16
   :header-rows: 1

   * - Layer
     - Document
     - IDs
     - Total
     - Status
     - Coverage
   * - SYS.1 elicitation
     - QDX-SER-001
     - QDX-SER-NNN
     - TBD
     - In progress
     - Planning
   * - SYS.2 system reqs
     - QDX-SRS-001
     - QDX-SYS-001…044
     - 44
     - Active
     - 100%
   * - SWE.1 SW reqs
     - QDX-SWE-DOC-001
     - QDX-SWE-001…101
     - 101
     - Active
     - 100%
   * - SWE.2 arch specs
     - QDX-SWA-DOC-001
     - QDX-SWA-SP-001…101
     - 101
     - Active
     - 100%
   * - SWE.3 design fns
     - QDX-SDD-DOC-001
     - QDX-UT-NNN anchors
     - 79
     - Active
     - 100%
   * - SWE.4 unit tests
     - QDX-SWE4-DOC-001
     - QDX-UT-001…079
     - 79
     - Active
     - 100%
   * - SWE.5 integ. tests
     - QDX-SWE5-DOC-001
     - QDX-IT-001…021
     - 21
     - Active
     - 100%
   * - SWE.6 qual. tests
     - QDX-SWE6-DOC-001
     - QDX-QT-001…101
     - 101
     - Active
     - 100%
   * - SYS.4 sys. integ. tests
     - QDX-SYS4-DOC-001
     - QDX-SIT-NNN
     - TBD
     - In progress
     - Planning
   * - SYS.5 sys. verif. tests
     - QDX-SYS5-DOC-001
     - QDX-SVT-001…044
     - 44 planned
     - In progress
     - Planning
   * - VAL.1 val. tests
     - QDX-VAL-001
     - QDX-VAT-001…101
     - 101 planned
     - In progress
     - Planning

Per-document traceability matrices:

- **SYS.2 ↔ SWE.1 ↔ SYS.5**: :ref:`sys_requirements` §7
- **SWE.1 ↔ SWE.6 ↔ VAL.1**: :ref:`sw_requirements` §6
- **SWE.2 ↔ SWE.1 ↔ SYS.2 ↔ SYS.4**: :ref:`sw_architecture` §7
- **SWE.3 ↔ SWE.1 / SWE.2**: :ref:`sw_detailed_design` §11
- **SWE.4 ↔ SWE.3**: :ref:`sw_unit_verification` §3
- **SWE.5 ↔ SWE.2**: :ref:`sw_integration_test` §3
- **SWE.6 ↔ SWE.1 ↔ SYS.2 ↔ VAL.1**: :ref:`sw_qualification_test` §3 and §5
