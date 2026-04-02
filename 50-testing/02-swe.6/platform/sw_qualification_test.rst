.. ============================================================
.. QORIX DEVELOPER — Software Qualification Test Specification
.. ASPICE: SWE.6
.. Derived from: QDX-SWE-DOC-001 (SWE.1), QDX-SWA-DOC-001 (SWE.2)
..               QDX-SWE5-DOC-001 (SWE.5)
.. ============================================================

.. _sw_qualification_test:

========================================================
Software Qualification Test Specification
========================================================

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Document ID**
     - QDX-SWE6-DOC-001
   * - **Product line**
     - Platform — Qorix Developer (all stacks)
   * - **Version**
     - 0.1.0
   * - **Status**
     - Draft
   * - **Owner**
     - Qorix Developer Validation and Verification Team
   * - **ASPICE process**
     - SWE.6 — Software Qualification Test
   * - **Parent SWE.1 doc**
     - :ref:`sw_requirements` (QDX-SWE-DOC-001)
   * - **Companion SYS.5 doc**
     - QDX-SYS5-DOC-001 — System Verification Specification (SYS.5, in progress)
   * - **Companion VAL.1 doc**
     - QDX-VAL-001 — Validation Plan and Test Records (VAL.1, in progress)
   * - **Jira epic**
     - QDX-EPIC-PLATFORM-SWE6
   * - **Git path**
     - ``docs/50-testing/02-swe.6/platform/sw_qualification_test.rst``
   * - **Changelog**
     - See :ref:`swe6_changelog`

----

.. contents:: Table of contents
   :depth: 3
   :local:

----


1. Purpose and Scope
====================

This document specifies the software qualification test strategy and
test case catalogue for the Qorix Developer Platform. It is fully
derived from the software requirements in :ref:`sw_requirements`
(QDX-SWE-DOC-001) and provides complete SWE.1 ↔ SWE.6 traceability.

SWE.6 demonstrates that the fully integrated software — all subsystems
assembled as they will be released — correctly implements every
requirement specified in SWE.1. Unlike SWE.4 (unit isolation) and
SWE.5 (subsystem interfaces), SWE.6 tests are conducted on the
complete platform as it will be delivered, using the released
binaries in a representative test environment.

One qualification test case (``QDX-QT-NNN``) exists for every
software requirement (``QDX-SWE-NNN``). The test case verifies the
requirement directly, using the verification method specified in
the SWE.1 ``:verification:`` field.

**Total test cases:** 101 (QDX-QT-001 through QDX-QT-101).


2. Qualification Test Strategy
================================

2.1 Test environment
---------------------

The SWE.6 qualification test environment uses the complete released
platform build — the same artefacts that will be delivered to
customers — in the following configuration:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Component
     - Configuration
   * - Qorix Developer IDE Extension
     - Installed in VS Code stable from release VSIX
   * - Rust Domain Service
     - Released binary, deployed as system service on Linux test host
   * - ARXML Gateway
     - Released JAR with production ARTOP version
   * - qorix_cli
     - Released binary on system PATH
   * - Test host
     - Linux x86_64, 16 GB RAM, 8-core CPU (documented specification)
   * - YAML fixtures
     - Qualification fixtures from ``tests/qualification/``
       committed at the same Git tag as the release

2.2 Qualification test approach
---------------------------------

Four test approaches are used, matching the verification methods in
SWE.1:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Approach
     - Definition
   * - Functional test
     - Exercise the feature through the released user interface or API.
       Verify the specified behaviour is observed.
   * - Demonstration
     - Operate the feature and verify the result against the SWE.1
       SHALL statement. Typically used for designer capabilities and
       wizard flows.
   * - Inspection
     - Review generated artefacts (YAML, ARXML, .h files, reports)
       or configuration files for specified content.
   * - Performance measurement
     - Measure elapsed time for a specified operation. Compare against
       the numerical threshold in the SWE.1 requirement.
   * - Analysis
     - Review the implementation against the SWE.3 specification for
       requirements that are verified by design rather than test.

2.3 Entry and exit criteria
-----------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Criterion
     - Definition
   * - Entry
     - SWE.5 integration tests all passed. Release build complete
       and tagged. Qualification fixtures committed at same tag.
   * - Exit (pass)
     - All 101 test cases pass with status PASS. No ERROR severity
       defects open against any QDX-QT-NNN. Test execution log
       archived with release package.
   * - Exit (blocked)
     - Any CRITICAL or MAJOR defect open. Test execution paused
       pending fix. Defect root cause traced to SWE.1 requirement
       and SWE.3 design element.

2.4 Test case status values
-----------------------------

Each test case carries one of: **PASS** — requirement verified.
**FAIL** — requirement not met, defect raised.
**BLOCKED** — cannot execute; dependency not available.
**NOT RUN** — deferred to next test cycle.


3. Qualification Test Cases
=============================

3.1 Workspace and project management (QDX-QT-001 to QDX-QT-005)
-----------------------------------------------------------------


3.1 Workspace, project and wizard (QDX-QT-001–005, QDX-QT-091–101)
--------------------------------------------------------------------

**QDX-QT-001** — Multi-stack workspace initialisation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-001
   * - **SYS.2 req**
     - QDX-SYS-001
   * - **VAL.1 val. test**
     - QDX-VAT-001 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-001.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-001. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-001 and QDX-SWE-001.

**QDX-QT-002** — Per-stack project scaffolding

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-002
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-002 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-002.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-002. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-002 and QDX-SWE-002.

**QDX-QT-003** — Source/output directory separation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-003
   * - **SYS.2 req**
     - QDX-SYS-044
   * - **VAL.1 val. test**
     - QDX-VAT-003 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-003.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-003 and QDX-SWE-003.

**QDX-QT-004** — Version-control-friendly YAML persistence

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-004
   * - **SYS.2 req**
     - QDX-SYS-019
   * - **VAL.1 val. test**
     - QDX-VAT-004 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-004.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-004 and QDX-SWE-004.

**QDX-QT-005** — Atomic save with integrity protection

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-005
   * - **SYS.2 req**
     - QDX-SYS-033
   * - **VAL.1 val. test**
     - QDX-VAT-005 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-005.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-005. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-005 and QDX-SWE-005.


3.2 YAML editor and LSP (QDX-QT-006–008)
------------------------------------------

**QDX-QT-006** — YAML editor with schema-based completion

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-006
   * - **SYS.2 req**
     - QDX-SYS-003
   * - **VAL.1 val. test**
     - QDX-VAT-006 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-006.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-006. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-006 and QDX-SWE-006.

**QDX-QT-007** — Language server protocol integration

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-007
   * - **SYS.2 req**
     - QDX-SYS-029
   * - **VAL.1 val. test**
     - QDX-VAT-007 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-007.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-007. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-001
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-007 and QDX-SWE-007.

**QDX-QT-008** — Localised atomic model mutations

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-008
   * - **SYS.2 req**
     - QDX-SYS-013
   * - **VAL.1 val. test**
     - QDX-VAT-008 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-008.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-008. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-008 and QDX-SWE-008.


3.3 Classic AUTOSAR designers C1–C6 (QDX-QT-009–016)
------------------------------------------------------

**QDX-QT-009** — C1 — SWC and interface designer

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-009
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-009 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-009.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-009. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-009 and QDX-SWE-009.

**QDX-QT-010** — C1 — SWC runnable definition

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-010
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-010 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-010.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-010. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-010 and QDX-SWE-010.

**QDX-QT-011** — C2 — Signals and ComStack designer

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-011
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-011 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-011.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-011. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-011 and QDX-SWE-011.

**QDX-QT-012** — C3 — ECU and BSW designer

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-012
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-012 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-012.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-012. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-012 and QDX-SWE-012.

**QDX-QT-013** — C4 — OS and scheduling designer

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-013
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-013 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-013.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-013. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-013 and QDX-SWE-013.

**QDX-QT-014** — C5 — Memory and NvM designer

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-014
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-014 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-014.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-014. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-014 and QDX-SWE-014.

**QDX-QT-015** — C6 — RTE and mapping designer

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-015
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-015 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-015.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-015. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-015 and QDX-SWE-015.

**QDX-QT-016** — Unmapped element detection in C6

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-016
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-016 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-016.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-016. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-016 and QDX-SWE-016.


3.4 Adaptive AUTOSAR designers A1–A6 (QDX-QT-017–028)
-------------------------------------------------------

**QDX-QT-017** — A1 — Application and service designer

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-017
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-017 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-017.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-017. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-017 and QDX-SWE-017.

**QDX-QT-018** — A1 — Service cross-reference tracking

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-018
   * - **SYS.2 req**
     - QDX-SYS-008
   * - **VAL.1 val. test**
     - QDX-VAT-018 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-018.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-018. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-018 and QDX-SWE-018.

**QDX-QT-019** — A2 — Communication and service instance de

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-019
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-019 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-019.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-019. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-011
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-019 and QDX-SWE-019.

**QDX-QT-020** — A2 — Service binding completeness validati

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-020
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-020 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-020.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-020. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-020 and QDX-SWE-020.

**QDX-QT-021** — A3 — Machine design designer

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-021
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-021 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-021.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-021. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-021 and QDX-SWE-021.

**QDX-QT-022** — A3 — Disabled core reference detection

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-022
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-022 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-022.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-022. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-022 and QDX-SWE-022.

**QDX-QT-023** — A4 — Platform services designer

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-023
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-023 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-023.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-023. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-023 and QDX-SWE-023.

**QDX-QT-024** — A5 — Execution management designer

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-024
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-024 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-024.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-024. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-024 and QDX-SWE-024.

**QDX-QT-025** — A5 — Scheduling conflict detection

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-025
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-025 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-025.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-025. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-025 and QDX-SWE-025.

**QDX-QT-026** — A6 — Deployment designer

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-026
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-026 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-026.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-026. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-026 and QDX-SWE-026.

**QDX-QT-027** — A6 — Resource constraint validation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-027
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-027 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-027.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-027. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-027 and QDX-SWE-027.

**QDX-QT-028** — Adaptive cross-designer consistency check

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-028
   * - **SYS.2 req**
     - QDX-SYS-020
   * - **VAL.1 val. test**
     - QDX-VAT-028 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-028.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-028. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-012
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-028 and QDX-SWE-028.


3.5 Validation and synchronisation (QDX-QT-029–037)
-----------------------------------------------------

**QDX-QT-029** — Designer-to-YAML synchronisation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-029
   * - **SYS.2 req**
     - QDX-SYS-005
   * - **VAL.1 val. test**
     - QDX-VAT-029 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-029.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-029. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-002
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-029 and QDX-SWE-029.

**QDX-QT-030** — YAML-to-designer synchronisation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-030
   * - **SYS.2 req**
     - QDX-SYS-005
   * - **VAL.1 val. test**
     - QDX-VAT-030 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-030.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-030. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-002
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-030 and QDX-SWE-030.

**QDX-QT-031** — In-IDE WASM fast validation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-031
   * - **SYS.2 req**
     - QDX-SYS-006
   * - **VAL.1 val. test**
     - QDX-VAT-031 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-031.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-031. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-003
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-031 and QDX-SWE-031.

**QDX-QT-032** — Deep semantic validation via domain servic

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-032
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-032 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-032.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-032. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-004
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-032 and QDX-SWE-032.

**QDX-QT-033** — Cross-file reference resolution

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-033
   * - **SYS.2 req**
     - QDX-SYS-008
   * - **VAL.1 val. test**
     - QDX-VAT-033 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-033.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-033. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-033 and QDX-SWE-033.

**QDX-QT-034** — Validation-gated publication

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-034
   * - **SYS.2 req**
     - QDX-SYS-036
   * - **VAL.1 val. test**
     - QDX-VAT-034 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-034.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-034. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-034 and QDX-SWE-034.

**QDX-QT-035** — Workspace-level consistency check

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-035
   * - **SYS.2 req**
     - QDX-SYS-020
   * - **VAL.1 val. test**
     - QDX-VAT-035 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-035.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-035. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-005
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-035 and QDX-SWE-035.

**QDX-QT-036** — Diagnostics panel presentation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-036
   * - **SYS.2 req**
     - QDX-SYS-014
   * - **VAL.1 val. test**
     - QDX-VAT-036 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-036.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-036. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-036 and QDX-SWE-036.

**QDX-QT-037** — Usable diagnostic message quality

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-037
   * - **SYS.2 req**
     - QDX-SYS-042
   * - **VAL.1 val. test**
     - QDX-VAT-037 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-037.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-037 and QDX-SWE-037.


3.6 Generation, gateway and CLI (QDX-QT-038–046)
--------------------------------------------------

**QDX-QT-038** — Deterministic ARXML generation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-038
   * - **SYS.2 req**
     - QDX-SYS-009
   * - **VAL.1 val. test**
     - QDX-VAT-038 (pending QDX-VAL-001)
   * - **Approach**
     - Analysis — static review of implementation and SWE.3 specification
   * - **Test steps**
     - 1. Review QDX-SDD-DOC-001 section for the implementing
       module. 2. Verify the design satisfies the SHALL statement
       in QDX-SWE-038 and the constraint is architecturally enforced.
   * - **Expected result**
     - Design review confirms the constraint is enforced. Reviewer
       sign-off recorded in the test execution log.
   * - **SWE.5 integ. ref**
     - QDX-IT-006
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-038 and QDX-SWE-038.

**QDX-QT-039** — ARXML export via ARTOP GraphQL gateway

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-039
   * - **SYS.2 req**
     - QDX-SYS-010
   * - **VAL.1 val. test**
     - QDX-VAT-039 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-039.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-039. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-007
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-039 and QDX-SWE-039.

**QDX-QT-040** — ARXML import and lossy-conversion reportin

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-040
   * - **SYS.2 req**
     - QDX-SYS-011
   * - **VAL.1 val. test**
     - QDX-VAT-040 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-040.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-040. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-007
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-040 and QDX-SWE-040.

**QDX-QT-041** — Generation provenance recording

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-041
   * - **SYS.2 req**
     - QDX-SYS-015
   * - **VAL.1 val. test**
     - QDX-VAT-041 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-041.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-041 and QDX-SWE-041.

**QDX-QT-042** — External artefact compatibility status rep

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-042
   * - **SYS.2 req**
     - QDX-SYS-030
   * - **VAL.1 val. test**
     - QDX-VAT-042 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-042.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-042 and QDX-SWE-042.

**QDX-QT-043** — GraphQL API contract for model access

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-043
   * - **SYS.2 req**
     - QDX-SYS-012
   * - **VAL.1 val. test**
     - QDX-VAT-043 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-043.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-043. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-008
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-043 and QDX-SWE-043.

**QDX-QT-044** — Search and navigation API

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-044
   * - **SYS.2 req**
     - QDX-SYS-018
   * - **VAL.1 val. test**
     - QDX-VAT-044 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-044.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-044. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-044 and QDX-SWE-044.

**QDX-QT-045** — Headless CLI for CI validation and generat

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-045
   * - **SYS.2 req**
     - QDX-SYS-031
   * - **VAL.1 val. test**
     - QDX-VAT-045 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-045.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-045. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-009
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-045 and QDX-SWE-045.

**QDX-QT-046** — Same Rust core for all build targets

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-046
   * - **SYS.2 req**
     - QDX-SYS-031
   * - **VAL.1 val. test**
     - QDX-VAT-046 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-046.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-046 and QDX-SWE-046.


3.7 AI-Assist and Qorix Agent (QDX-QT-047–053)
------------------------------------------------

**QDX-QT-047** — AI-generated OperationPlan — no direct YAM

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-047
   * - **SYS.2 req**
     - QDX-SYS-016
   * - **VAL.1 val. test**
     - QDX-VAT-047 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-047.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - QDX-IT-010
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-047 and QDX-SWE-047.

**QDX-QT-048** — User acceptance gate for AI suggestions

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-048
   * - **SYS.2 req**
     - QDX-SYS-017
   * - **VAL.1 val. test**
     - QDX-VAT-048 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-048.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-048. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-048 and QDX-SWE-048.

**QDX-QT-049** — Post-acceptance WASM re-validation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-049
   * - **SYS.2 req**
     - QDX-SYS-006
   * - **VAL.1 val. test**
     - QDX-VAT-049 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-049.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-049. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-049 and QDX-SWE-049.

**QDX-QT-050** — Intent Router — Classic vs Adaptive dispat

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-050
   * - **SYS.2 req**
     - QDX-SYS-016
   * - **VAL.1 val. test**
     - QDX-VAT-050 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-050.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-050. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-050 and QDX-SWE-050.

**QDX-QT-051** — Configurable AI data transmission control

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-051
   * - **SYS.2 req**
     - QDX-SYS-037
   * - **VAL.1 val. test**
     - QDX-VAT-051 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-051.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-051 and QDX-SWE-051.

**QDX-QT-052** — Audit log for critical user actions

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-052
   * - **SYS.2 req**
     - QDX-SYS-035
   * - **VAL.1 val. test**
     - QDX-VAT-052 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-052.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-052 and QDX-SWE-052.

**QDX-QT-053** — Access control for privileged operations

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-053
   * - **SYS.2 req**
     - QDX-SYS-034
   * - **VAL.1 val. test**
     - QDX-VAT-053 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-053.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-053 and QDX-SWE-053.


3.8 Performance requirements (QDX-QT-054–058)
-----------------------------------------------

**QDX-QT-054** — Workspace open time

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-054
   * - **SYS.2 req**
     - QDX-SYS-022
   * - **VAL.1 val. test**
     - QDX-VAT-054 (pending QDX-VAL-001)
   * - **Approach**
     - Performance measurement — timed execution, compare to numerical threshold
   * - **Test steps**
     - 1. Prepare the representative fixture as specified in the
       SWE.1 requirement. 2. Execute the operation. 3. Measure
       elapsed wall-clock time on the documented test host.
   * - **Expected result**
     - Operation completes within the time threshold specified in
       QDX-SWE-054. Result logged in milliseconds.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-054 and QDX-SWE-054.

**QDX-QT-055** — WASM validation latency

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-055
   * - **SYS.2 req**
     - QDX-SYS-023
   * - **VAL.1 val. test**
     - QDX-VAT-055 (pending QDX-VAL-001)
   * - **Approach**
     - Performance measurement — timed execution, compare to numerical threshold
   * - **Test steps**
     - 1. Prepare the representative fixture as specified in the
       SWE.1 requirement. 2. Execute the operation. 3. Measure
       elapsed wall-clock time on the documented test host.
   * - **Expected result**
     - Operation completes within the time threshold specified in
       QDX-SWE-055. Result logged in milliseconds.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-055 and QDX-SWE-055.

**QDX-QT-056** — Search response time

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-056
   * - **SYS.2 req**
     - QDX-SYS-024
   * - **VAL.1 val. test**
     - QDX-VAT-056 (pending QDX-VAL-001)
   * - **Approach**
     - Performance measurement — timed execution, compare to numerical threshold
   * - **Test steps**
     - 1. Prepare the representative fixture as specified in the
       SWE.1 requirement. 2. Execute the operation. 3. Measure
       elapsed wall-clock time on the documented test host.
   * - **Expected result**
     - Operation completes within the time threshold specified in
       QDX-SWE-056. Result logged in milliseconds.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-056 and QDX-SWE-056.

**QDX-QT-057** — ARXML generation completion time

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-057
   * - **SYS.2 req**
     - QDX-SYS-025
   * - **VAL.1 val. test**
     - QDX-VAT-057 (pending QDX-VAL-001)
   * - **Approach**
     - Performance measurement — timed execution, compare to numerical threshold
   * - **Test steps**
     - 1. Prepare the representative fixture as specified in the
       SWE.1 requirement. 2. Execute the operation. 3. Measure
       elapsed wall-clock time on the documented test host.
   * - **Expected result**
     - Operation completes within the time threshold specified in
       QDX-SWE-057. Result logged in milliseconds.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-057 and QDX-SWE-057.

**QDX-QT-058** — Non-blocking UI for long-running operation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-058
   * - **SYS.2 req**
     - QDX-SYS-026
   * - **VAL.1 val. test**
     - QDX-VAT-058 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-058.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-058. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-058 and QDX-SWE-058.


3.9 Portability and extensibility (QDX-QT-059–062)
----------------------------------------------------

**QDX-QT-059** — Dual IDE host support — VS Code and Theia

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-059
   * - **SYS.2 req**
     - QDX-SYS-027
   * - **VAL.1 val. test**
     - QDX-VAT-059 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-059.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-059. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-059 and QDX-SWE-059.

**QDX-QT-060** — Offline local authoring and validation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-060
   * - **SYS.2 req**
     - QDX-SYS-043
   * - **VAL.1 val. test**
     - QDX-VAT-060 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-060.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-060. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-060 and QDX-SWE-060.

**QDX-QT-061** — Extension mechanism without core modificat

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-061
   * - **SYS.2 req**
     - QDX-SYS-041
   * - **VAL.1 val. test**
     - QDX-VAT-061 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Review QDX-SDD-DOC-001 section for the implementing
       module. 2. Verify the design satisfies the SHALL statement
       in QDX-SWE-061 and the constraint is architecturally enforced.
   * - **Expected result**
     - Design review confirms the constraint is enforced. Reviewer
       sign-off recorded in the test execution log.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-061 and QDX-SWE-061.

**QDX-QT-062** — Backward-compatible project migration

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-062
   * - **SYS.2 req**
     - QDX-SYS-040
   * - **VAL.1 val. test**
     - QDX-VAT-062 (pending QDX-VAL-001)
   * - **Approach**
     - Analysis — static review of implementation and SWE.3 specification
   * - **Test steps**
     - 1. Review QDX-SDD-DOC-001 section for the implementing
       module. 2. Verify the design satisfies the SHALL statement
       in QDX-SWE-062 and the constraint is architecturally enforced.
   * - **Expected result**
     - Design review confirms the constraint is enforced. Reviewer
       sign-off recorded in the test execution log.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-062 and QDX-SWE-062.


3.10 Bootloader BPCT (QDX-QT-063–076)
---------------------------------------

**QDX-QT-063** — BPCT project structure and MCU selection (

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-063
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-063 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-063.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-063. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-063 and QDX-SWE-063.

**QDX-QT-064** — BPCT communication channel configuration (

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-064
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-064 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-064.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-064. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-064 and QDX-SWE-064.

**QDX-QT-065** — BPCT memory map and NvM block configuratio

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-065
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-065 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-065.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-065. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-065 and QDX-SWE-065.

**QDX-QT-066** — BPCT flash block size constraint validatio

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-066
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-066 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-066.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-066. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-066 and QDX-SWE-066.

**QDX-QT-067** — BPCT core parameters and UDS session confi

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-067
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-067 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-067.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-067. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-067 and QDX-SWE-067.

**QDX-QT-068** — BPCT timing, hardware and watchdog configu

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-068
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-068 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-068.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-068. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-068 and QDX-SWE-068.

**QDX-QT-069** — BPCT watchdog timeout cross-constraint val

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-069
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-069 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-069.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-069. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-069 and QDX-SWE-069.

**QDX-QT-070** — BPCT cross-designer timing dependency prop

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-070
   * - **SYS.2 req**
     - QDX-SYS-008
   * - **VAL.1 val. test**
     - QDX-VAT-070 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-070.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-070. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-070 and QDX-SWE-070.

**QDX-QT-071** — BPCT crypto and secure boot configuration 

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-071
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-071 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-071.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-071. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-071 and QDX-SWE-071.

**QDX-QT-072** — BPCT weak cryptographic algorithm detectio

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-072
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-072 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-072.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-072. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-072 and QDX-SWE-072.

**QDX-QT-073** — BPCT key address placement validation (BD6

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-073
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-073 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-073.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-073. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-073 and QDX-SWE-073.

**QDX-QT-074** — BPCT validation rule engine (cross-designe

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-074
   * - **SYS.2 req**
     - QDX-SYS-020
   * - **VAL.1 val. test**
     - QDX-VAT-074 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-074.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-074. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-013
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-074 and QDX-SWE-074.

**QDX-QT-075** — BPCT C header and Makefile generation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-075
   * - **SYS.2 req**
     - QDX-SYS-009
   * - **VAL.1 val. test**
     - QDX-VAT-075 (pending QDX-VAL-001)
   * - **Approach**
     - Analysis — static review of implementation and SWE.3 specification
   * - **Test steps**
     - 1. Review QDX-SDD-DOC-001 section for the implementing
       module. 2. Verify the design satisfies the SHALL statement
       in QDX-SWE-075 and the constraint is architecturally enforced.
   * - **Expected result**
     - Design review confirms the constraint is enforced. Reviewer
       sign-off recorded in the test execution log.
   * - **SWE.5 integ. ref**
     - QDX-IT-014
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-075 and QDX-SWE-075.

**QDX-QT-076** — BPCT output preview in BD1 designer

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-076
   * - **SYS.2 req**
     - QDX-SYS-014
   * - **VAL.1 val. test**
     - QDX-VAT-076 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-076.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-076. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-076 and QDX-SWE-076.


3.11 AI-Assist domain tools (QDX-QT-077–080)
----------------------------------------------

**QDX-QT-077** — AI-Assist availability gated by domain ext

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-077
   * - **SYS.2 req**
     - QDX-SYS-016
   * - **VAL.1 val. test**
     - QDX-VAT-077 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-077.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-077 and QDX-SWE-077.

**QDX-QT-078** — AI-Assist context injection per domain

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-078
   * - **SYS.2 req**
     - QDX-SYS-016
   * - **VAL.1 val. test**
     - QDX-VAT-078 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-078.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-078. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-015
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-078 and QDX-SWE-078.

**QDX-QT-079** — AI-Assist OperationPlan scoped to active d

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-079
   * - **SYS.2 req**
     - QDX-SYS-017
   * - **VAL.1 val. test**
     - QDX-VAT-079 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-079.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-079. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-079 and QDX-SWE-079.

**QDX-QT-080** — AI-Assist BPCT domain tools

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-080
   * - **SYS.2 req**
     - QDX-SYS-016
   * - **VAL.1 val. test**
     - QDX-VAT-080 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-080.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-080 and QDX-SWE-080.


3.12 LW-BSW subsystem (QDX-QT-081–090)
----------------------------------------

**QDX-QT-081** — LW-BSW project creation and ECU/DEXT impor

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-081
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-081 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-081.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-081. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-016
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-081 and QDX-SWE-081.

**QDX-QT-082** — LW-BSW module configuration — ten BSW modu

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-082
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-082 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-082.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-082. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-082 and QDX-SWE-082.

**QDX-QT-083** — LW-BSW CAN and optional LIN communication 

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-083
   * - **SYS.2 req**
     - QDX-SYS-004
   * - **VAL.1 val. test**
     - QDX-VAT-083 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-083.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-083. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-083 and QDX-SWE-083.

**QDX-QT-084** — LW-BSW resource budget validation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-084
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-084 (pending QDX-VAL-001)
   * - **Approach**
     - Analysis — static review of implementation and SWE.3 specification
   * - **Test steps**
     - 1. Review QDX-SDD-DOC-001 section for the implementing
       module. 2. Verify the design satisfies the SHALL statement
       in QDX-SWE-084 and the constraint is architecturally enforced.
   * - **Expected result**
     - Design review confirms the constraint is enforced. Reviewer
       sign-off recorded in the test execution log.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-084 and QDX-SWE-084.

**QDX-QT-085** — LW-BSW OS scheduling map and race conditio

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-085
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-085 (pending QDX-VAL-001)
   * - **Approach**
     - Analysis — static review of implementation and SWE.3 specification
   * - **Test steps**
     - 1. Review QDX-SDD-DOC-001 section for the implementing
       module. 2. Verify the design satisfies the SHALL statement
       in QDX-SWE-085 and the constraint is architecturally enforced.
   * - **Expected result**
     - Design review confirms the constraint is enforced. Reviewer
       sign-off recorded in the test execution log.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-085 and QDX-SWE-085.

**QDX-QT-086** — LW-BSW Config Report generation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-086
   * - **SYS.2 req**
     - QDX-SYS-015
   * - **VAL.1 val. test**
     - QDX-VAT-086 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-086.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-086 and QDX-SWE-086.

**QDX-QT-087** — LW-BSW module configuration ``.h`` and ``.

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-087
   * - **SYS.2 req**
     - QDX-SYS-009
   * - **VAL.1 val. test**
     - QDX-VAT-087 (pending QDX-VAL-001)
   * - **Approach**
     - Analysis — static review of implementation and SWE.3 specification
   * - **Test steps**
     - 1. Review QDX-SDD-DOC-001 section for the implementing
       module. 2. Verify the design satisfies the SHALL statement
       in QDX-SWE-087 and the constraint is architecturally enforced.
   * - **Expected result**
     - Design review confirms the constraint is enforced. Reviewer
       sign-off recorded in the test execution log.
   * - **SWE.5 integ. ref**
     - QDX-IT-017
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-087 and QDX-SWE-087.

**QDX-QT-088** — LW-BSW bus-level compatibility check with 

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-088
   * - **SYS.2 req**
     - QDX-SYS-007
   * - **VAL.1 val. test**
     - QDX-VAT-088 (pending QDX-VAL-001)
   * - **Approach**
     - Analysis — static review of implementation and SWE.3 specification
   * - **Test steps**
     - 1. Review QDX-SDD-DOC-001 section for the implementing
       module. 2. Verify the design satisfies the SHALL statement
       in QDX-SWE-088 and the constraint is architecturally enforced.
   * - **Expected result**
     - Design review confirms the constraint is enforced. Reviewer
       sign-off recorded in the test execution log.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-088 and QDX-SWE-088.

**QDX-QT-089** — LW-BSW AI-Assist Config Insight

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-089
   * - **SYS.2 req**
     - QDX-SYS-016
   * - **VAL.1 val. test**
     - QDX-VAT-089 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Load the qualification fixture for QDX-SWE-089.
       2. Operate the platform feature specified in the requirement.
       3. Observe and record the outcome.
   * - **Expected result**
     - The software behaves as specified in the SHALL statement
       of QDX-SWE-089. All conditions in the requirement body are met.
   * - **SWE.5 integ. ref**
     - QDX-IT-018
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-089 and QDX-SWE-089.

**QDX-QT-090** — LW-BSW ICC-2 conformance constraint enforc

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-090
   * - **SYS.2 req**
     - QDX-SYS-006
   * - **VAL.1 val. test**
     - QDX-VAT-090 (pending QDX-VAL-001)
   * - **Approach**
     - Inspection — review configuration files, YAML content, or generated artefact structure
   * - **Test steps**
     - 1. Execute the feature that produces the artefact or
       configuration under inspection. 2. Open the output and
       verify it contains the elements specified in QDX-SWE-090.
   * - **Expected result**
     - All required elements present. No prohibited elements
       present. Structure matches the SWE.1 SHALL statement.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if all expected results are observed and recorded.
       FAIL if any condition is not met — raise Jira defect
       referencing QDX-QT-090 and QDX-SWE-090.


3.14 Project creation wizard (QDX-QT-091 to QDX-QT-101)
-------------------------------------------------------

**QDX-QT-091** — Project creation wizard — welcome and stac

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-091
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-091 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Open the Qorix Developer project creation wizard.
       2. Navigate through the step sequence for the stack type
       relevant to QDX-SWE-091. 3. Verify the UI, validation and
       scaffolding behaviour specified in the requirement.
   * - **Expected result**
     - Wizard step sequence, field validation, back/continue
       navigation and scaffolding output all match the SHALL
       statement of QDX-SWE-091.
   * - **SWE.5 integ. ref**
     - QDX-IT-019
   * - **Pass/Fail criteria**
     - PASS if wizard behaviour matches specification. FAIL
       raises defect referencing QDX-QT-091 and QDX-SWE-091.

**QDX-QT-092** — Classic AUTOSAR — platform version selecti

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-092
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-092 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Open the Qorix Developer project creation wizard.
       2. Navigate through the step sequence for the stack type
       relevant to QDX-SWE-092. 3. Verify the UI, validation and
       scaffolding behaviour specified in the requirement.
   * - **Expected result**
     - Wizard step sequence, field validation, back/continue
       navigation and scaffolding output all match the SHALL
       statement of QDX-SWE-092.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if wizard behaviour matches specification. FAIL
       raises defect referencing QDX-QT-092 and QDX-SWE-092.

**QDX-QT-093** — Classic AUTOSAR — template selection step

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-093
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-093 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Open the Qorix Developer project creation wizard.
       2. Navigate through the step sequence for the stack type
       relevant to QDX-SWE-093. 3. Verify the UI, validation and
       scaffolding behaviour specified in the requirement.
   * - **Expected result**
     - Wizard step sequence, field validation, back/continue
       navigation and scaffolding output all match the SHALL
       statement of QDX-SWE-093.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if wizard behaviour matches specification. FAIL
       raises defect referencing QDX-QT-093 and QDX-SWE-093.

**QDX-QT-094** — Classic AUTOSAR — project configuration st

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-094
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-094 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Open the Qorix Developer project creation wizard.
       2. Navigate through the step sequence for the stack type
       relevant to QDX-SWE-094. 3. Verify the UI, validation and
       scaffolding behaviour specified in the requirement.
   * - **Expected result**
     - Wizard step sequence, field validation, back/continue
       navigation and scaffolding output all match the SHALL
       statement of QDX-SWE-094.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if wizard behaviour matches specification. FAIL
       raises defect referencing QDX-QT-094 and QDX-SWE-094.

**QDX-QT-095** — Adaptive AUTOSAR — template selection step

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-095
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-095 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Open the Qorix Developer project creation wizard.
       2. Navigate through the step sequence for the stack type
       relevant to QDX-SWE-095. 3. Verify the UI, validation and
       scaffolding behaviour specified in the requirement.
   * - **Expected result**
     - Wizard step sequence, field validation, back/continue
       navigation and scaffolding output all match the SHALL
       statement of QDX-SWE-095.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if wizard behaviour matches specification. FAIL
       raises defect referencing QDX-QT-095 and QDX-SWE-095.

**QDX-QT-096** — Adaptive AUTOSAR — project configuration s

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-096
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-096 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Open the Qorix Developer project creation wizard.
       2. Navigate through the step sequence for the stack type
       relevant to QDX-SWE-096. 3. Verify the UI, validation and
       scaffolding behaviour specified in the requirement.
   * - **Expected result**
     - Wizard step sequence, field validation, back/continue
       navigation and scaffolding output all match the SHALL
       statement of QDX-SWE-096.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if wizard behaviour matches specification. FAIL
       raises defect referencing QDX-QT-096 and QDX-SWE-096.

**QDX-QT-097** — Bootloader (BPCT) — template selection ste

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-097
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-097 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Open the Qorix Developer project creation wizard.
       2. Navigate through the step sequence for the stack type
       relevant to QDX-SWE-097. 3. Verify the UI, validation and
       scaffolding behaviour specified in the requirement.
   * - **Expected result**
     - Wizard step sequence, field validation, back/continue
       navigation and scaffolding output all match the SHALL
       statement of QDX-SWE-097.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if wizard behaviour matches specification. FAIL
       raises defect referencing QDX-QT-097 and QDX-SWE-097.

**QDX-QT-098** — Bootloader (BPCT) — MCU and project config

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-098
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-098 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Open the Qorix Developer project creation wizard.
       2. Navigate through the step sequence for the stack type
       relevant to QDX-SWE-098. 3. Verify the UI, validation and
       scaffolding behaviour specified in the requirement.
   * - **Expected result**
     - Wizard step sequence, field validation, back/continue
       navigation and scaffolding output all match the SHALL
       statement of QDX-SWE-098.
   * - **SWE.5 integ. ref**
     - QDX-IT-020
   * - **Pass/Fail criteria**
     - PASS if wizard behaviour matches specification. FAIL
       raises defect referencing QDX-QT-098 and QDX-SWE-098.

**QDX-QT-099** — LW-BSW — project configuration step

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-099
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-099 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Open the Qorix Developer project creation wizard.
       2. Navigate through the step sequence for the stack type
       relevant to QDX-SWE-099. 3. Verify the UI, validation and
       scaffolding behaviour specified in the requirement.
   * - **Expected result**
     - Wizard step sequence, field validation, back/continue
       navigation and scaffolding output all match the SHALL
       statement of QDX-SWE-099.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if wizard behaviour matches specification. FAIL
       raises defect referencing QDX-QT-099 and QDX-SWE-099.

**QDX-QT-100** — Project creation — review and confirmation

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-100
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-100 (pending QDX-VAL-001)
   * - **Approach**
     - Functional demonstration — operate the feature and verify observable output
   * - **Test steps**
     - 1. Open the Qorix Developer project creation wizard.
       2. Navigate through the step sequence for the stack type
       relevant to QDX-SWE-100. 3. Verify the UI, validation and
       scaffolding behaviour specified in the requirement.
   * - **Expected result**
     - Wizard step sequence, field validation, back/continue
       navigation and scaffolding output all match the SHALL
       statement of QDX-SWE-100.
   * - **SWE.5 integ. ref**
     - QDX-IT-021
   * - **Pass/Fail criteria**
     - PASS if wizard behaviour matches specification. FAIL
       raises defect referencing QDX-QT-100 and QDX-SWE-100.

**QDX-QT-101** — Project creation — step navigation and per

.. list-table::
   :widths: 20 80
   :header-rows: 0   * - **Traces to (SWE.1)**
     - QDX-SWE-101
   * - **SYS.2 req**
     - QDX-SYS-002
   * - **VAL.1 val. test**
     - QDX-VAT-101 (pending QDX-VAL-001)
   * - **Approach**
     - Functional test — exercise the feature and verify the software requirement is met
   * - **Test steps**
     - 1. Open the Qorix Developer project creation wizard.
       2. Navigate through the step sequence for the stack type
       relevant to QDX-SWE-101. 3. Verify the UI, validation and
       scaffolding behaviour specified in the requirement.
   * - **Expected result**
     - Wizard step sequence, field validation, back/continue
       navigation and scaffolding output all match the SHALL
       statement of QDX-SWE-101.
   * - **SWE.5 integ. ref**
     - —
   * - **Pass/Fail criteria**
     - PASS if wizard behaviour matches specification. FAIL
       raises defect referencing QDX-QT-101 and QDX-SWE-101.



4. Test Execution Log Template
================================

For each test cycle, the following log is completed per test case:

.. list-table::
   :widths: 20 18 18 22 22
   :header-rows: 1

   * - Test ID
     - Date executed
     - Tester
     - Status
     - Defect ID (if FAIL)
   * - QDX-QT-001
     - TBD
     - TBD
     - NOT RUN
     - —
   * - QDX-QT-002
     - TBD
     - TBD
     - NOT RUN
     - —
   * - [... continue for all 101 test cases ...]
     -
     -
     -
     -
   * - QDX-QT-101
     - TBD
     - TBD
     - NOT RUN
     - —


5. Traceability Summary
========================

.. list-table::
   :widths: 17 17 17 17 16 16
   :header-rows: 1

   * - SWE.1 total
     - SWE.6 total
     - SWE.4 UT total
     - SWE.5 IT total
     - VAL.1 val. tests
     - SWE.6 coverage
   * - 101 requirements
     - 101 test cases
     - 79 unit tests
     - 21 integration tests
     - 101 planned (QDX-VAT-001..101, pending QDX-VAL-001)
     - 100% SWE.1 coverage

Every ``QDX-SWE-NNN`` requirement has exactly one ``QDX-QT-NNN``
qualification test (SWE.6) and one planned ``QDX-VAT-NNN`` validation
test (VAL.1). Every qualification test traces to its parent
``QDX-SWE-NNN`` software requirement and the grandparent system
requirement ``QDX-SYS-NNN``. SWE.6 verifies that the software is built
correctly against SWE.1 requirements. VAL.1 verifies that the right
software was built — i.e. that it satisfies actual stakeholder needs
in representative operational conditions. Both chains are required for
full ASPICE V-cycle closure. See ``QDX-VAL-001`` (in progress) for the
VAL.1 validation plan and ``QDX-SYS5-DOC-001`` (in progress) for the
SYS.5 system verification specification.


6. Open Issues
===============

.. list-table::
   :widths: 15 55 15 15
   :header-rows: 1

   * - Issue ID
     - Description
     - Owner
     - Target date
   * - TBD-SWE6-001
     - Qualification fixtures for Adaptive A3–A6 designers
       (QDX-QT-021 through QDX-QT-028) need representative
       YAML files covering the deployment constraint and
       scheduling conflict scenarios. Blocked on Adaptive
       designer implementation (roadmap April–June 2026).
     - Adaptive Domain Lead
     - 2026-06-30
   * - TBD-SWE6-002
     - Performance test infrastructure for QDX-QT-054 through
       QDX-QT-058: documented test host specification, benchmark
       fixture file sizes and measurement scripts. Hardware
       must be documented and reproducible across test runs.
     - Platform Engineering
     - 2026-04-30
   * - TBD-SWE6-003
     - Qualification fixtures for LW-BSW Config Report
       (QDX-QT-086) — need a fixture that generates a Config
       Report with at least one detected race condition and one
       resource budget warning for complete test coverage.
     - LW-BSW Lead
     - 2026-06-01
   * - TBD-SWE6-004
     - AI-Assist qualification tests (QDX-QT-047 through
       QDX-QT-053, QDX-QT-077 through QDX-QT-080) require a
       controlled LLM test environment with repeatable outputs.
       Qualification cannot use a live production LLM.
       Deterministic test LLM configuration to be defined.
     - AI/MCP Lead
     - 2026-06-15


.. _swe6_changelog:

7. Changelog
=============

.. list-table::
   :widths: 15 15 20 50
   :header-rows: 1

   * - Version
     - Date
     - Author
     - Change description
   * - 0.1.0
     - 2026-03-31
     - Qorix Platform Engineering
     - Initial draft. 101 qualification test cases (QDX-QT-001 to
       QDX-QT-101) — one per SWE.1 requirement. Test approach
       assigned per verification method from SWE.1. Full
       SWE.1 ↔ SWE.6 traceability. Strategy, environment,
       entry/exit criteria, execution log template and
       traceability summary defined.

----

*This document is version-controlled in Git at*
``docs/50-testing/02-swe.6/platform/sw_qualification_test.rst``.
*All 101 qualification tests must achieve PASS status and the
execution log must be archived before a release baseline receives
SWE.6 sign-off.*
