.. ============================================================
.. QORIX DEVELOPER — Software Integration Test Specification
.. ASPICE: SWE.5 
.. Derived from: QDX-SWA-DOC-001 (SWE.2), QDX-SDD-DOC-001 (SWE.3)
.. ============================================================

.. _sw_integration_test:

========================================================
Software Integration Test Specification
========================================================

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Document ID**
     - QDX-SWE5-DOC-001
   * - **Product line**
     - Platform — Qorix Developer (all stacks)
   * - **Version**
     - 0.1.0
   * - **Status**
     - Draft
   * - **Owner**
     - Qorix Developer Validation and Verification Team
   * - **ASPICE process**
     - SWE.5 — Software Integration and Integration Test
   * - **Parent SWE.2 doc**
     - :ref:`sw_architecture` (QDX-SWA-DOC-001)
   * - **Jira epic**
     - QDX-EPIC-PLATFORM-SWE5
   * - **Git path**
     - ``docs/50-testing/01-swe.5/platform/sw_integration_test.rst``
   * - **Changelog**
     - See :ref:`swe5_changelog`

----

.. contents:: Table of contents
   :depth: 3
   :local:

----


1. Purpose and Scope
====================

This document specifies the software integration test strategy and test
cases for the Qorix Developer Platform. It is derived from the
software architecture in :ref:`sw_architecture` (QDX-SWA-DOC-001).

SWE.5 verifies that the integrated software subsystems work correctly
across their defined interfaces. Where SWE.4 tests individual units in
isolation, SWE.5 tests the boundaries between subsystems with real
(not mocked) counterparts:

- IDE Layer ↔ WASM Bridge ↔ ``qorix_core_wasm``
- IDE Layer ↔ Domain Service Client ↔ Rust Domain Service (HTTP/gRPC)
- Rust Domain Service ↔ ARXML Gateway (``core::gql_client`` → GraphQL)
- AI Chat Panel ↔ Qorix Agent ↔ Rust Domain Service (MCP tools)
- ``qorix_cli`` ↔ Rust Domain Service ↔ ARXML Gateway (CI path)
- Project Creation Wizard ↔ ``workspace_manager::scaffold_project``
- BPCT validation engine ↔ cross-designer YAML constraint chain
- LW-BSW subsystem ↔ Classic Domain Service (schema filter boundary)

**Out of scope for SWE.5:** System-level user scenarios (those belong
in SYS.5). External tool interoperability (Tresos, DaVinci) beyond
the ARXML Gateway boundary.


2. Integration Test Strategy
=============================

2.1 Integration order
----------------------

Integration follows a bottom-up strategy reflecting the dependency
hierarchy in QDX-SWA-DOC-001 Section 3.3:

.. mermaid::

   graph LR
     S1["Stage 1\ncore::* crates\n+ build targets\n(WASM · CLI · Service)"]
     S2["Stage 2\nDomain Service API\n(HTTP/gRPC contract)"]
     S3["Stage 3\nARXML Gateway\n(GraphQL boundary)"]
     S4["Stage 4\nIDE Layer ↔ WASM\n+ Domain Service"]
     S5["Stage 5\nQorix Agent\n↔ Domain Service"]
     S6["Stage 6\nEnd-to-end CI path\nqorix_cli full pipeline"]

     S1 --> S2 --> S3 --> S4 --> S5 --> S6

2.2 Test environment
---------------------

.. list-table::
   :widths: 28 72
   :header-rows: 1

   * - Environment element
     - Specification
   * - Rust Domain Service
     - Real binary, started as subprocess. Binds to localhost random
       port. Health-check endpoint polled before tests start.
   * - ARXML Gateway
     - Real Spring Boot process with ARTOP. Starts in test mode with
       deterministic-serialisation flag set. Binds to localhost.
   * - WASM module
     - Real ``qorix_core_wasm`` loaded in Node.js test runner
       (not mocked). Validates against real JSON schemas.
   * - qorix_cli
     - Real CLI binary from the same build as the Domain Service.
   * - LLM Backend (Qorix Agent tests)
     - Stubbed with a deterministic response fixture server.
       Real LLM is not used in integration tests.
   * - File system
     - Temporary directories cleaned up after each test.
   * - YAML fixtures
     - Committed to ``tests/fixtures/`` directory, version-controlled.

2.3 Entry and exit criteria
-----------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Criterion
     - Definition
   * - Entry
     - All SWE.4 unit tests pass (exit criteria met). All subsystem
       binaries build successfully. Integration test fixtures committed.
   * - Exit (pass)
     - All integration test cases in this document pass. No ERROR
       severity defects open against any SWE.5 test ID.
   * - Exit (fail)
     - Any test fails. Defect raised in Jira with QDX-IT-NNN reference.

2.4 Interface under test
-------------------------

Each integration test targets a specific interface from the SWE.2
architecture. The interface under test column maps to the SWE.2
provided/required interface tables.


3. Integration Test Cases
==========================

3.1 Stage 1 — Build target parity (QDX-IT-001 to QDX-IT-002)
--------------------------------------------------------------

These tests verify that the three Rust build targets produce identical
validation results for the same input, realising QDX-ADR-002
(single codebase, three targets).

**QDX-IT-001** — WASM and Domain Service validation parity

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - ``validateYaml()`` (WASM) vs Domain Service validation endpoint
   * - **Preconditions**
     - Rust Domain Service running. WASM module loaded in Node.js.
       Classic project fixtures available.
   * - **Test steps**
     - 1. Load ``tests/fixtures/classic/valid_project/`` YAML files.
       2. Call ``wasm_bridge::validate_yaml`` on each file.
       3. Call Domain Service ``POST /validate`` with same files.
       4. Compare DiagnosticList from both calls.
   * - **Expected result**
     - Both DiagnosticLists are structurally identical: same count,
       same codes, same yaml_paths. Severity levels match.
   * - **SWE.1 refs**
     - QDX-SWE-031, QDX-SWE-046
   * - **SWE.2 arch element**
     - Rust Domain Platform — ``qorix_core_wasm`` + Domain Service

**QDX-IT-002** — CLI and Domain Service validation parity

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - ``qorix_cli validate`` vs Domain Service validation endpoint
   * - **Preconditions**
     - Both CLI binary and Domain Service built from same Rust source.
   * - **Test steps**
     - 1. Run ``qorix_cli validate <project_path>`` on Classic fixture.
       2. Call Domain Service ``POST /validate`` with same project.
       3. Compare diagnostic JSON outputs.
   * - **Expected result**
     - CLI JSON output and Domain Service response contain identical
       diagnostic entries. CLI exits with code 0 for clean project,
       code 1 for project with errors.
   * - **SWE.1 refs**
     - QDX-SWE-045, QDX-SWE-046
   * - **SWE.2 arch element**
     - Rust Domain Platform — ``qorix_cli`` + Domain Service

3.2 Stage 2 — Domain Service API contract (QDX-IT-003 to QDX-IT-005)
----------------------------------------------------------------------

**QDX-IT-003** — Domain Service validates cross-file references
correctly

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Domain Service HTTP API — ``POST /validate-workspace``
   * - **Preconditions**
     - Domain Service running. Fixture: Classic project where
       ``rte-mapping.yaml`` references runnable ``"FaultHandler"``
       not defined in ``swc-design.yaml``.
   * - **Test steps**
     - 1. ``POST /validate-workspace`` with the cross-file fixture.
       2. Inspect returned DiagnosticList.
   * - **Expected result**
     - Response contains at least one ``Severity::Error`` with
       ``code = "CLASSIC-VAL-001"`` and ``yaml_path`` pointing to
       the missing mapping in ``rte-mapping.yaml``.
   * - **SWE.1 refs**
     - QDX-SWE-032, QDX-SWE-033, QDX-SWE-035
   * - **SWE.2 arch element**
     - Rust Domain Platform — Domain Service + ``classic::validation``

**QDX-IT-004** — Domain Service blocks generation on ERROR

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Domain Service HTTP API — ``POST /generate``
   * - **Preconditions**
     - Domain Service running. Project fixture with one ERROR
       diagnostic (unmapped runnable).
   * - **Test steps**
     - 1. ``POST /generate`` with the errored project.
       2. Inspect HTTP response.
   * - **Expected result**
     - HTTP 422 (Unprocessable Entity). Response body contains
       ``"blocked": true`` and the DiagnosticList with ERROR entries.
       No files written to the output directory.
   * - **SWE.1 refs**
     - QDX-SWE-034, QDX-SWE-038
   * - **SWE.2 arch element**
     - Rust Domain Platform — Domain Service + ``core::validation``

**QDX-IT-005** — Domain Service search returns results within SLA

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Domain Service HTTP API — ``GET /search?q=``
   * - **Preconditions**
     - Domain Service running with medium Classic workspace loaded
       (~100 SWCs, ~200 signals).
   * - **Test steps**
     - 1. ``GET /search?q=Speed``. Measure elapsed time.
   * - **Expected result**
     - HTTP 200. Results contain all elements with "Speed" in name.
       Elapsed ≤ 500 ms (QDX-SWE-056).
   * - **SWE.1 refs**
     - QDX-SWE-044, QDX-SWE-056
   * - **SWE.2 arch element**
     - Rust Domain Platform — Domain Service search API

3.3 Stage 3 — ARXML Gateway boundary (QDX-IT-006 to QDX-IT-008)
-----------------------------------------------------------------

**QDX-IT-006** — Full generation pipeline: YAML → Domain Service → Gateway → ARXML

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - ``core::gql_client`` → ARXML Gateway GraphQL API
   * - **Preconditions**
     - Domain Service and ARXML Gateway both running. Clean Classic
       Powertrain Control fixture project.
   * - **Test steps**
     - 1. Load project via Domain Service.
       2. ``POST /generate`` — Domain Service calls Gateway via
          ``core::gql_client``.
       3. Inspect returned ARXML and provenance.json.
   * - **Expected result**
     - ARXML files written to output dir. File names match expected
       set for Powertrain Control template. ``provenance.json``
       contains ``artop_version`` and ``tool_version``.
       ARXML is valid XML parseable by standard XML parser.
   * - **SWE.1 refs**
     - QDX-SWE-038, QDX-SWE-039, QDX-SWE-041
   * - **SWE.2 arch element**
     - ARXML Gateway — Spring Boot + ARTOP; ``core::gql_client``

**QDX-IT-007** — ARXML import round-trip: ARXML → import → re-export → compare

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - ARXML Gateway import + export GraphQL mutations
   * - **Preconditions**
     - Gateway running. Reference Classic ARXML fixture (produced by
       DaVinci — committed to ``tests/fixtures/import/``).
   * - **Test steps**
     - 1. ``importArxml`` mutation with reference fixture.
       2. Take returned model payload.
       3. ``generateArxml`` mutation with that payload.
       4. Compare output ARXML against reference fixture using
          a semantic ARXML comparator (element names, values).
   * - **Expected result**
     - All elements present in reference ARXML are present in
       re-exported ARXML. Any elements reported as ConversionWarnings
       during import are absent in re-export (not silently dropped).
   * - **SWE.1 refs**
     - QDX-SWE-040, QDX-SWE-042, QDX-SWE-062
   * - **SWE.2 arch element**
     - ARXML Gateway — importArxml + generateArxml

**QDX-IT-008** — GraphQL schema version is discoverable

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - ARXML Gateway GraphQL API — introspection
   * - **Preconditions**
     - ARXML Gateway running.
   * - **Test steps**
     - 1. Send GraphQL introspection query to Gateway.
       2. Check ``schemaVersion`` field in response.
   * - **Expected result**
     - Introspection response returns a non-empty ``schemaVersion``
       string matching the version in the published SDL file.
   * - **SWE.1 refs**
     - QDX-SWE-043
   * - **SWE.2 arch element**
     - ARXML Gateway — GraphQL API / SDL

3.4 Stage 4 — IDE Layer integration (QDX-IT-009 to QDX-IT-012)
---------------------------------------------------------------

**QDX-IT-009** — CLI full pipeline: validate then generate (headless)

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - ``qorix_cli`` ↔ Domain Service ↔ ARXML Gateway (full path)
   * - **Preconditions**
     - All three services running. Clean Classic fixture.
   * - **Test steps**
     - 1. ``qorix_cli validate <project>`` — expect exit 0.
       2. ``qorix_cli generate <project> --output <dir>``.
       3. Check output directory for ARXML files and provenance.json.
   * - **Expected result**
     - validate exits 0. generate exits 0. ARXML and provenance.json
       present. Generation completes within 60 s for medium project
       (QDX-SWE-057).
   * - **SWE.1 refs**
     - QDX-SWE-038, QDX-SWE-041, QDX-SWE-045, QDX-SWE-057
   * - **SWE.2 arch element**
     - Rust Domain Platform — ``qorix_cli`` (CI path)

**QDX-IT-010** — WASM Bridge: edit triggers fast validation and
diagnostics panel update

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - IDE Layer Command Bus → WASM Bridge → ``qorix_core_wasm``
   * - **Preconditions**
     - WASM module loaded. Classic fixture workspace open in test harness.
   * - **Test steps**
     - 1. Dispatch ``classic.addSwc`` command with valid payload.
       2. Observe WASM validation response.
       3. Dispatch ``classic.removePort`` command that creates an
          unmapped-signal condition.
       4. Observe WASM response.
   * - **Expected result**
     - Step 2: empty DiagnosticList. YAML file updated.
       Step 4: DiagnosticList contains one Error with
       ``code = "CLASSIC-VAL-002"``. YAML write blocked.
       Both responses arrive within 500 ms.
   * - **SWE.1 refs**
     - QDX-SWE-008, QDX-SWE-029, QDX-SWE-031, QDX-SWE-055
   * - **SWE.2 arch element**
     - IDE Layer — Command Bus + WASM Bridge

**QDX-IT-011** — Adaptive cross-designer consistency: A2 binding
validated against A1 services

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Domain Service ``/validate-workspace`` — adaptive::validation
       cross-file rules
   * - **Preconditions**
     - Domain Service running. Adaptive Perception Pipeline fixture.
   * - **Test steps**
     - 1. Load valid Adaptive fixture. Validate → expect no errors.
       2. Edit ``communication.yaml`` to add an unbound consumer
          (``RequiredServiceInstance`` with no matching provider).
       3. Validate workspace again.
   * - **Expected result**
     - Step 1: clean. Step 3: DiagnosticList contains Error with
       ``code = "ADAPTIVE-VAL-001"`` referencing the unbound consumer.
   * - **SWE.1 refs**
     - QDX-SWE-020, QDX-SWE-028, QDX-SWE-035
   * - **SWE.2 arch element**
     - Rust Domain Platform — ``adaptive::validation``

**QDX-IT-012** — Adaptive manifest generation produces all three manifests

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Domain Service generate → ARXML Gateway → Adaptive manifests
   * - **Preconditions**
     - Clean Adaptive Perception Pipeline fixture. All services running.
   * - **Test steps**
     - 1. ``POST /generate`` for Adaptive project.
       2. List files in output directory.
   * - **Expected result**
     - Output contains: ``ApplicationManifest.arxml``,
       ``ExecutionManifest.arxml``, ``MachineManifest.arxml``.
       All three are well-formed XML.
   * - **SWE.1 refs**
     - QDX-SWE-026, QDX-SWE-038, QDX-SWE-039
   * - **SWE.2 arch element**
     - ARXML Gateway — Adaptive manifest generation

3.5 Stage 5 — Qorix Agent integration (QDX-IT-013 to QDX-IT-015)
-----------------------------------------------------------------

**QDX-IT-013** — BPCT VR rule engine triggered by cross-file edit

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Domain Service ``/validate-workspace`` — ``bpct::validation``
       VR_007 cross-designer rule
   * - **Preconditions**
     - Domain Service running. BPCT fixture: TC3xx, valid watchdog
       and erase timeout values.
   * - **Test steps**
     - 1. Validate clean BPCT project — expect no errors.
       2. Edit ``bl-hardware.yaml``: set ``FBL_WDG_TIMEOUT_MS = 1500``
          while ``FBL_TIMER_ERASE_TIMEOUT_MS = 2000``.
       3. Validate again.
   * - **Expected result**
     - Step 3: Error with ``code = "VR_007"``. Message contains both
       timeout values and recommended minimum.
   * - **SWE.1 refs**
     - QDX-SWE-069, QDX-SWE-074
   * - **SWE.2 arch element**
     - Rust Domain Platform — BPCT validation rule engine

**QDX-IT-014** — BPCT generation produces C headers from bl-*.yaml

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Domain Service generate (BPCT path) → ``bpct::generator``
   * - **Preconditions**
     - Clean BPCT TC3xx fixture. Domain Service running.
   * - **Test steps**
     - 1. ``POST /generate`` for BPCT project.
       2. Inspect output directory.
       3. Open ``cfg.h`` and check macros.
   * - **Expected result**
     - Six output files present. ``cfg.h`` contains
       ``#define FBL_FLASH_PAGE_SIZE  256`` (matching TC3xx default).
       Makefile present.
   * - **SWE.1 refs**
     - QDX-SWE-063, QDX-SWE-075
   * - **SWE.2 arch element**
     - BPCT subsystem — ``bpct::generator``

**QDX-IT-015** — Agent OperationPlan is scoped to Classic domain

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Qorix Agent Intent Router → Domain Service MCP tools →
       OperationPlan response
   * - **Preconditions**
     - Domain Service running. Agent stub server running with
       deterministic LLM fixture. Classic project loaded.
   * - **Test steps**
     - 1. Submit prompt ``"Fix all unmapped runnables"`` with
          ``active_designer = "C6"``.
       2. Inspect returned OperationPlan.
       3. Attempt to apply plan to an Adaptive model.
   * - **Expected result**
     - Step 2: OperationPlan has ``domain = Classic``. All ops target
       ``rte-mapping.yaml`` only.
       Step 3: ``Err(OpsError::DomainMismatch)`` returned.
   * - **SWE.1 refs**
     - QDX-SWE-047, QDX-SWE-050, QDX-SWE-079
   * - **SWE.2 arch element**
     - Qorix Agent — Intent Router + Classic MCP Tools

3.6 Stage 6 — LW-BSW subsystem boundary (QDX-IT-016 to QDX-IT-018)
--------------------------------------------------------------------

**QDX-IT-016** — LW-BSW project creation and schema filter applied

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - ``workspace_manager::scaffold_project`` (LW-BSW) →
       ``lwbsw::validation`` schema filter boundary
   * - **Preconditions**
     - Domain Service running. Clean temp workspace.
   * - **Test steps**
     - 1. Scaffold LW-BSW project (TC3xx, CAN only).
       2. Validate the scaffolded project.
       3. Manually add an ICC-3-only field to the YAML.
       4. Validate again.
   * - **Expected result**
     - Step 2: no errors (scaffold produces valid ICC-2 YAML).
       Step 4: Warning with ``code = "LWBSW-VAL-010"`` for the
       ICC-3 field. No Error (generation not blocked by Warning).
   * - **SWE.1 refs**
     - QDX-SWE-081, QDX-SWE-082, QDX-SWE-090
   * - **SWE.2 arch element**
     - LW-BSW subsystem — schema filter + ``lwbsw::validation``

**QDX-IT-017** — LW-BSW resource budget violation blocks generation

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Domain Service generate (LW-BSW path) — resource budget
       validation gate
   * - **Preconditions**
     - LW-BSW project fixture with ROM estimate exceeding 150 KB.
   * - **Test steps**
     - 1. ``POST /generate`` with over-budget LW-BSW project.
       2. Inspect response.
   * - **Expected result**
     - HTTP 422. ``"blocked": true``. DiagnosticList contains
       ``code = "LWBSW-VAL-001"`` Error.
       No .h or .c files written to output dir.
   * - **SWE.1 refs**
     - QDX-SWE-034, QDX-SWE-084
   * - **SWE.2 arch element**
     - LW-BSW subsystem — ``lwbsw::validation`` + generate gate

**QDX-IT-018** — LW-BSW Config Report generated alongside headers

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Domain Service generate (LW-BSW path) → ``lwbsw::generator``
   * - **Preconditions**
     - Clean within-budget LW-BSW TC3xx fixture.
   * - **Test steps**
     - 1. ``POST /generate``.
       2. List output directory.
       3. Open ``LwBsw_ConfigReport.txt``.
   * - **Expected result**
     - 21 files in output dir (20 source + 1 report). Report
       contains sections: Scheduling Map, Resource Budget
       (ROM/RAM/CPU actuals vs targets), Race Conditions.
   * - **SWE.1 refs**
     - QDX-SWE-086, QDX-SWE-087
   * - **SWE.2 arch element**
     - LW-BSW subsystem — ``lwbsw::generator``

3.7 Project creation wizard integration (QDX-IT-019 to QDX-IT-021)
--------------------------------------------------------------------

**QDX-IT-019** — Wizard completes and scaffold produces correct files
for Classic project

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Wizard → ``workspace_manager::scaffold_project`` (Classic)
   * - **Preconditions**
     - Workspace manager available. Temp workspace directory.
   * - **Test steps**
     - 1. Drive wizard to completion: Classic H1, Powertrain Control
          template, name = ``"ECU_Test_001"``, TC39x MCU.
       2. Wizard calls scaffold on "Create Project".
       3. Inspect project directory.
   * - **Expected result**
     - Project directory created. Six YAML source files present.
       ``swc-design.yaml`` pre-populated with Powertrain Control
       SWC stubs. ``project.yaml`` records stack type = Classic H1.
   * - **SWE.1 refs**
     - QDX-SWE-002, QDX-SWE-091, QDX-SWE-093, QDX-SWE-094
   * - **SWE.2 arch element**
     - IDE Layer — Project Creation Wizard + workspace_manager

**QDX-IT-020** — BPCT wizard completion applies MCU defaults to YAML

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Wizard → ``workspace_manager::scaffold_project`` (BPCT)
       → ``bpct::mcu_defaults::get``
   * - **Preconditions**
     - Workspace manager available. Temp dir.
   * - **Test steps**
     - 1. Drive BPCT wizard: CAN Single-Channel template,
          name = ``"FBL_PROJ_TC3XX"``, TC3xx MCU, No Security.
       2. Inspect ``bl-project.yaml`` and ``bl-hardware.yaml``.
   * - **Expected result**
     - ``bl-project.yaml`` contains ``flash_page_size: 256``.
       ``bl-hardware.yaml`` contains ``timer_resolution_us: 100``.
       ``bl-security.yaml`` contains ``FBL_SEC_BOOT_ENABLED: false``.
   * - **SWE.1 refs**
     - QDX-SWE-063, QDX-SWE-097, QDX-SWE-098
   * - **SWE.2 arch element**
     - IDE Layer — BPCT Wizard + workspace_manager + bpct::mcu_defaults

**QDX-IT-021** — Wizard review screen reflects all wizard selections

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Interface under test**
     - Wizard state → review step rendering → scaffold call
   * - **Preconditions**
     - Wizard test harness. Any stack type.
   * - **Test steps**
     - 1. Drive Adaptive wizard: Perception Pipeline template,
          name = ``"PerceptionPipeline_v1"``, Orin machine.
       2. Navigate to review step.
       3. Inspect rendered review state.
   * - **Expected result**
     - Review shows: stack = ``"AUTOSAR Adaptive R23"``,
       template = ``"Perception Pipeline"``,
       designers list includes A1 through A6 with correct names.
       "Create Project" button is enabled.
   * - **SWE.1 refs**
     - QDX-SWE-095, QDX-SWE-096, QDX-SWE-100
   * - **SWE.2 arch element**
     - IDE Layer — Project Creation Wizard (review step)


4. Regression Test Policy
==========================

All integration tests are automated and run on every PR targeting
``main``. They are also run nightly against the ``develop`` branch.

Any defect found in integration testing that causes a test case to
fail must:

1. Be raised in Jira with the QDX-IT-NNN reference.
2. Block merge of the triggering PR.
3. Be re-tested with the same test case after the fix is applied.
4. Have the defect closure verified by the test lead.


5. Open Issues
===============

.. list-table::
   :widths: 15 55 15 15
   :header-rows: 1

   * - Issue ID
     - Description
     - Owner
     - Target date
   * - TBD-SWE5-001
     - Integration tests QDX-IT-022 onwards for Adaptive designer
       A3–A6 canvas ↔ Domain Service flows (deployment constraint
       validation, scheduling conflict detection). Blocked on
       TBD-SWA-001 (Domain Service API surface).
     - Adaptive Domain Lead
     - 2026-05-30
   * - TBD-SWE5-002
     - Integration test for LW-BSW DEXT/DBC import boundary:
       import preview in wizard ↔ ``lwbsw::import`` module.
       Blocked on TBD-SDD-004 and TBD-SDD-007.
     - LW-BSW Lead
     - 2026-06-01
   * - TBD-SWE5-003
     - Define test fixtures for ARXML import round-trip (QDX-IT-007).
       Requires a reference ARXML file exported from DaVinci or Tresos
       that exercises the full Classic schema supported by Qorix.
     - ARXML Gateway Lead
     - 2026-05-01
   * - TBD-SWE5-004
     - Agent integration test for AI data transmission control
       (QDX-SWE-051) with a real deployment configuration toggle.
       Currently uses stub LLM — needs a controlled test environment
       with real LLM and data-capture proxy.
     - AI/MCP Lead
     - 2026-06-15


.. _swe5_changelog:

6. Changelog
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
     - Initial draft derived from QDX-SWA-DOC-001 (SWE.2). Defines
       21 integration test cases (QDX-IT-001 to QDX-IT-021) across
       six integration stages. Covers WASM/CLI/Service parity,
       Domain Service API, ARXML Gateway boundary, IDE Layer,
       Qorix Agent, LW-BSW subsystem, BPCT, and project creation
       wizard integration. Environment specification, entry/exit
       criteria and regression policy defined.

----

*This document is version-controlled in Git at*
``docs/50-testing/01-swe.5/platform/sw_integration_test.rst``.
