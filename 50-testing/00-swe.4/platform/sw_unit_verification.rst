.. ============================================================
.. QORIX DEVELOPER — Software Unit Verification
.. ASPICE: SWE.4
.. Derived from: QDX-SDD-DOC-001 (SWE.3), QDX-SWE-DOC-001 (SWE.1)
.. ============================================================

.. _sw_unit_verification:

========================================================
Software Unit Verification Specification
========================================================

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Document ID**
     - QDX-SWE4-DOC-001
   * - **Product line**
     - Platform — Qorix Developer (all stacks)
   * - **Version**
     - 0.1.0
   * - **Status**
     - Draft
   * - **Owner**
     - Qorix Developer Engineering Team
   * - **ASPICE process**
     - SWE.4 — Software Unit Verification
   * - **Parent SWE.3 doc**
     - :ref:`sw_detailed_design` (QDX-SDD-DOC-001)
   * - **Jira epic**
     - QDX-EPIC-PLATFORM-SWE4
   * - **Git path**
     - ``docs/50-testing/00-swe.4/platform/sw_unit_verification.rst``
   * - **Changelog**
     - See :ref:`swe4_changelog`

----

.. contents:: Table of contents
   :depth: 3
   :local:

----


1. Purpose and Scope
====================

This document specifies the software unit verification strategy and
test case catalogue for the Qorix Developer Platform. It is fully
derived from the detailed design in :ref:`sw_detailed_design`
(QDX-SDD-DOC-001).

SWE.4 verifies that each software unit — Rust function, TypeScript
module, or Java service method — correctly implements the detailed
design specified in SWE.3. Unit verification operates on isolated
units with all dependencies either mocked, stubbed, or represented by
test doubles. No network, file system or external service dependency
is permitted in a unit test unless explicitly documented as an
integration boundary (those belong in SWE.5).

**Scope:** All public functions specified in QDX-SDD-DOC-001, sections
4 through 9. Coverage target: ≥ 80% line coverage per crate measured
by ``cargo llvm-cov``.


2. Verification Strategy
=========================

2.1 Unit test framework and tooling
-------------------------------------

.. list-table::
   :widths: 25 35 40
   :header-rows: 1

   * - Language / layer
     - Framework
     - Coverage tool
   * - Rust (all crates)
     - Built-in ``#[test]`` + ``tokio::test`` for async
     - ``cargo llvm-cov`` — per-crate line coverage
   * - TypeScript (IDE Layer)
     - Jest + ts-jest
     - Istanbul (built into Jest)
   * - Java (ARXML Gateway)
     - JUnit 5 + Mockito
     - JaCoCo — line and branch coverage

2.2 Test isolation requirements
---------------------------------

- **File system:** All tests use ``tempfile::tempdir()`` (Rust) or
  ``tmp.Dir`` (TypeScript). No test writes to the project source tree.
- **Network:** All HTTP/gRPC calls are mocked. ``mockito`` for Rust,
  ``jest.mock`` for TypeScript, Mockito for Java.
- **WASM module:** Tests of the ``wasm_bridge`` module stub the WASM
  call with a synchronous mock returning pre-defined ``DiagnosticList``
  fixtures.
- **Domain Service:** Tests of IDE-layer modules use a
  ``MockDomainServiceClient`` that returns canned responses.
- **Timing:** Performance tests (QDX-UT-014, QDX-UT-001) are marked
  ``#[ignore]`` by default and run explicitly in CI performance jobs.

2.3 Entry and exit criteria
-----------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Criterion
     - Definition
   * - Entry
     - SWE.3 function specification complete for the unit under test.
       Unit implementation compiles without warnings.
   * - Exit (pass)
     - All unit tests for the module pass with zero failures.
       Line coverage ≥ 80% for the crate.
       ``cargo clippy -D warnings`` passes.
       ``cargo fmt --check`` passes.
   * - Exit (fail)
     - Any test fails, coverage < 80%, or static analysis warning
       present. Defect raised in Jira with test ID and failure log.

2.4 Static analysis checks (run per-crate on every PR)
--------------------------------------------------------

.. list-table::
   :widths: 35 65
   :header-rows: 1

   * - Check
     - Tool / command
   * - Lint (Rust)
     - ``cargo clippy -- -D warnings``
   * - Format (Rust)
     - ``cargo fmt --check``
   * - Cyclomatic complexity ≤ 15 (Rust)
     - ``cargo cyclonedx`` or equivalent
   * - No ``unsafe`` without SAFETY comment (Rust)
     - Custom Clippy lint ``undocumented_unsafe_blocks``
   * - No ``unwrap()`` / ``expect()`` in production (Rust)
     - Clippy ``unwrap_used``, ``expect_used`` lints
   * - Type safety (TypeScript)
     - ``tsc --noEmit --strict``
   * - Lint (TypeScript)
     - ``eslint --max-warnings 0``
   * - Coverage (Java)
     - JaCoCo line ≥ 80%, branch ≥ 70%


3. Unit Test Catalogue
=======================

3.1 workspace_manager module (QDX-UT-001 to QDX-UT-008)
---------------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-001
     - ``open``
     - Valid ``workspace.yaml`` with two projects both present on disk.
       Mock Domain Service returns loaded model in 100 ms.
     - ``Ok(Workspace)``. Elapsed ≤ 30 s.
     - QDX-SWE-001, QDX-SWE-054
   * - QDX-UT-002
     - ``open``
     - ``workspace.yaml`` declares a project path that does not exist
       on disk.
     - ``Err(WorkspaceError::MissingProjects([missing_path]))``.
     - QDX-SWE-001
   * - QDX-UT-003
     - ``open``
     - File at path is not valid YAML (random bytes).
     - ``Err(WorkspaceError::ParseError)``.
     - QDX-SWE-001
   * - QDX-UT-004
     - ``scaffold_project``
     - Classic stack config, valid name, empty temp dir.
     - ``Ok(ProjectRef)``. Six files present in ``src/``:
       ``swc-design.yaml``, ``signals-comstack.yaml``,
       ``ecu-bsw.yaml``, ``os-scheduling.yaml``,
       ``mem-nvram.yaml``, ``rte-mapping.yaml``.
     - QDX-SWE-002
   * - QDX-UT-005
     - ``scaffold_project``
     - Adaptive stack config, valid name.
     - ``Ok(ProjectRef)``. Six files in ``src/``:
       ``application-design.yaml``, ``communication.yaml``,
       ``machine-design.yaml``, ``platform-services.yaml``,
       ``execution.yaml``, ``deployment.yaml``.
     - QDX-SWE-002
   * - QDX-UT-006
     - ``scaffold_project``
     - BPCT stack config, valid name, TC3xx MCU family.
     - ``Ok(ProjectRef)``. Six ``bl-*.yaml`` files in ``src/``.
       ``bl-project.yaml`` contains TC3xx MCU defaults.
     - QDX-SWE-002, QDX-SWE-063
   * - QDX-UT-007
     - ``scaffold_project``
     - Name ``"My Project"`` — contains space.
     - ``Err(ScaffoldError::InvalidName)``.
     - QDX-SWE-002
   * - QDX-UT-008
     - ``scaffold_project``
     - Valid name but directory already exists at target path.
     - ``Err(ScaffoldError::AlreadyExists)``.
     - QDX-SWE-002

3.2 command_bus module (QDX-UT-009 to QDX-UT-011)
---------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-009
     - ``execute``
     - Command ``classic.addSwc`` with valid payload. WASM mock returns
       empty diagnostic list. Domain Service mock returns empty list.
     - ``CommandResult { applied: true }``. YAML file written.
       File content contains new SWC entry.
     - QDX-SWE-008, QDX-SWE-029
   * - QDX-UT-010
     - ``execute``
     - Valid command but WASM mock returns one ``Severity::Error``
       diagnostic for a required field.
     - ``CommandResult { applied: false }``. YAML file unchanged.
       ``diagnostics`` contains the Error entry.
     - QDX-SWE-031, QDX-SWE-034
   * - QDX-UT-011
     - ``execute``
     - Command with domain tag ``Classic`` dispatched while active
       designer is ``Adaptive``.
     - ``Err(BusError::DomainMismatch)``.
     - QDX-SWE-008

3.3 wasm_bridge module (QDX-UT-012 to QDX-UT-015)
---------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-012
     - ``validate_yaml``
     - Well-formed SWC design YAML, all required fields present.
     - ``DiagnosticList`` is empty.
     - QDX-SWE-031
   * - QDX-UT-013
     - ``validate_yaml``
     - YAML with ``name`` field missing from a required SWC entry.
     - ``DiagnosticList`` contains one ``Severity::Error`` entry.
       ``yaml_path`` contains the path to the missing field.
     - QDX-SWE-031
   * - QDX-UT-014
     - ``validate_yaml``
     - YAML file with 5,000 lines, all valid. Measure wall-clock time.
     - Validation completes. Elapsed ≤ 500 ms.
     - QDX-SWE-055
   * - QDX-UT-015
     - ``validate_yaml``
     - ``schema_id`` not present in schema registry.
     - Returns ``DiagnosticList`` containing one entry with
       ``code = "WASM-001"`` and ``severity = Error``.
     - QDX-SWE-031

3.4 diagnostics_panel module (QDX-UT-016 to QDX-UT-018)
---------------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-016
     - ``merge_and_render``
     - WASM list and deep list both contain the same diagnostic
       (same code, file, yaml_path) at different severity levels.
     - Returned list has length 1. Item has the higher severity
       (Error beats Warning).
     - QDX-SWE-036
   * - QDX-UT-017
     - ``merge_and_render``
     - Input contains two Warnings and one Error in arbitrary order.
     - Output[0] has ``severity = Error``. Output[1] and [2]
       are the Warnings.
     - QDX-SWE-036
   * - QDX-UT-018
     - ``merge_and_render``
     - Both input lists are empty.
     - ``RenderedDiagnostics { error_count: 0, warning_count: 0,
       info_count: 0, items: [] }``.
     - QDX-SWE-036

3.5 wizard module (QDX-UT-019 to QDX-UT-025)
----------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-019
     - ``validate_step``
     - Step = ``StepProjectName``. State has name = ``"ECU_Speed_v1"``.
     - ``StepValidation { valid: true, field_errors: {} }``.
     - QDX-SWE-094, QDX-SWE-101
   * - QDX-UT-020
     - ``validate_step``
     - Step = ``StepProjectName``. State has name = ``"ECU Speed v1"``
       (contains spaces).
     - ``valid: false``. ``field_errors`` contains entry for
       ``project_name`` field with message referencing alphanumeric
       constraint.
     - QDX-SWE-094, QDX-SWE-101
   * - QDX-UT-021
     - ``validate_step``
     - Step = ``StepBpctProjectId``. State has
       ``fbl_project_name = "my_project"`` (lowercase).
     - ``valid: false``. ``field_errors`` contains entry for
       ``fbl_project_name``.
     - QDX-SWE-098, QDX-SWE-101
   * - QDX-UT-022
     - ``validate_step``
     - Step = ``StepMcuFamily``. State has ``mcu_family = None``.
     - ``valid: false``. ``field_errors`` contains MCU family entry.
     - QDX-SWE-094, QDX-SWE-098
   * - QDX-UT-023
     - ``get_step_sequence``
     - Stack = ``StackType::Classic { .. }``.
     - Returns ``Vec<WizardStep>`` of length 5 in order:
       Type, Platform, Template, Configuration, Review.
     - QDX-SWE-101
   * - QDX-UT-024
     - ``get_step_sequence``
     - Stack = ``StackType::Bpct { .. }``.
     - Returns ``Vec<WizardStep>`` of length 4 in order:
       Type, Template, MCUConfig, Review. Contains MCUConfig step.
     - QDX-SWE-101
   * - QDX-UT-025
     - ``get_step_sequence``
     - Stack = ``StackType::SCore``.
     - Returns ``Vec<WizardStep>`` of length 3.
     - QDX-SWE-101

3.6 core::yaml module (QDX-UT-026 to QDX-UT-031)
--------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-026
     - ``load``
     - Write a known struct to a temp file, load it back.
     - ``Ok(T)``. All fields match original struct.
     - QDX-SWE-004
   * - QDX-UT-027
     - ``load``
     - Path points to non-existent file.
     - ``Err(YamlError::IoError(..))``
     - QDX-SWE-004
   * - QDX-UT-028
     - ``load``
     - File contains ``": unclosed_string`` — invalid YAML.
     - ``Err(YamlError::ParseError { path, .. })``. ``path``
       matches the input file path.
     - QDX-SWE-004
   * - QDX-UT-029
     - ``atomic_save``
     - Save a struct to temp path, reload with ``load``.
     - Reloaded value equals original struct.
     - QDX-SWE-005
   * - QDX-UT-030
     - ``atomic_save``
     - Mock the rename step to fail after temp write.
     - ``Err(YamlError::IoError)``. No ``.yaml.tmp`` file remains.
       Original target file unchanged.
     - QDX-SWE-005
   * - QDX-UT-031
     - ``atomic_save``
     - Save same struct twice to same path.
     - Both resulting files are byte-identical (stable key ordering).
     - QDX-SWE-038

3.7 core::validation module (QDX-UT-032 to QDX-UT-034)
--------------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-032
     - ``run``
     - Zero rules registered. Valid context.
     - Returns empty ``DiagnosticList``.
     - QDX-SWE-031
   * - QDX-UT-033
     - ``run``
     - Two rules: rule A returns one Warning, rule B returns one Error.
     - Merged list has length 2. First item is Error (severity sort).
     - QDX-SWE-031, QDX-SWE-037
   * - QDX-UT-034
     - ``run``
     - One rule whose ``check()`` panics with a string message.
     - Returns one diagnostic with ``code = "CORE-VAL-PANIC"``,
       ``severity = Error``. No process crash.
     - QDX-SWE-031

3.8 classic::validation rules (QDX-UT-035 to QDX-UT-037)
----------------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-035
     - ``UnmappedRunnableRule::check``
     - Context has 3 runnables, all present in runnable_to_task.
     - Empty ``DiagnosticList``.
     - QDX-SWE-015, QDX-SWE-016
   * - QDX-UT-036
     - ``UnmappedRunnableRule::check``
     - Context has 3 runnables; one (``"FaultHandler"``) absent from
       runnable_to_task.
     - One ``Diagnostic``, ``severity = Error``,
       ``code = "CLASSIC-VAL-001"``.
     - QDX-SWE-016
   * - QDX-UT-037
     - ``UnmappedRunnableRule::check``
     - Same as QDX-UT-036.
     - Diagnostic ``message`` contains ``"FaultHandler"`` and the text
       ``"Add an entry to runnable_to_task"``.
     - QDX-SWE-037

3.9 core::ops module (QDX-UT-038 to QDX-UT-040)
-------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-038
     - ``apply``
     - OperationPlan with single ``Op::Add`` at valid model path.
     - ``Ok(())``. Model contains the new element at the path.
     - QDX-SWE-008, QDX-SWE-047
   * - QDX-UT-039
     - ``apply``
     - OperationPlan with two ops; the second op targets an
       invalid path.
     - ``Err(OpsError::InvalidPath)``. Model identical to
       pre-call state (rollback verified).
     - QDX-SWE-008
   * - QDX-UT-040
     - ``apply``
     - Plan ``domain = Adaptive`` applied to Classic ``DomainModel``.
     - ``Err(OpsError::DomainMismatch)``.
     - QDX-SWE-047, QDX-SWE-079

3.10 domain_service functions (QDX-UT-041 to QDX-UT-046)
----------------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-041
     - ``load_workspace``
     - Workspace with valid Classic and Adaptive YAML fixtures.
     - ``Ok(LoadedWorkspace)``. Both models populated.
       ``diagnostics`` empty for clean fixtures.
     - QDX-SWE-001, QDX-SWE-033
   * - QDX-UT-042
     - ``load_workspace``
     - One YAML file in workspace has syntax error.
     - ``Err(ServiceError::ParseError { path })`` where ``path``
       identifies the corrupt file.
     - QDX-SWE-001
   * - QDX-UT-043
     - ``load_workspace``
     - Classic workspace where ``rte-mapping.yaml`` references a
       signal not defined in ``signals-comstack.yaml``.
     - ``Ok(LoadedWorkspace)``. ``diagnostics`` contains one
       cross-file Error diagnostic.
     - QDX-SWE-033, QDX-SWE-035
   * - QDX-UT-044
     - ``generate``
     - Loaded model with one ERROR diagnostic. ARXML Gateway mocked.
     - ``Err(ServiceError::GenerationBlocked { diagnostics })``.
       No files written to output dir.
     - QDX-SWE-034
   * - QDX-UT-045
     - ``generate``
     - Clean model (no errors). ARXML Gateway mock returns artefact.
     - ``Ok(GenerationResult)``. ``provenance.json`` written with
       non-empty ``tool_version`` and UTC timestamp.
     - QDX-SWE-041
   * - QDX-UT-046
     - ``generate``
     - Identical clean model called twice. ARXML Gateway mock is
       deterministic.
     - Both calls return identical ARXML bytes.
     - QDX-SWE-038

3.11 ARXML Gateway (QDX-UT-047 to QDX-UT-052)
-----------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-047
     - ``importArxml``
     - Valid Classic ARXML with standard SWC and COM stack elements.
     - ``ImportResult`` with non-null model. ``warnings`` list empty.
     - QDX-SWE-040
   * - QDX-UT-048
     - ``importArxml``
     - ARXML containing an ICC-3-only element (OBD service) not
       present in Qorix Classic schema.
     - ``ImportResult`` with ``warnings`` list containing one entry
       describing the ICC-3 element and the reason.
     - QDX-SWE-040, QDX-SWE-042
   * - QDX-UT-049
     - ``importArxml``
     - Input string is not valid XML.
     - Throws ``GatewayException.INVALID_ARXML``.
     - QDX-SWE-040
   * - QDX-UT-050
     - ``generateArxml``
     - Identical ``GenerateInput`` submitted twice.
     - Both responses contain byte-identical ARXML content.
     - QDX-SWE-038
   * - QDX-UT-051
     - ``generateArxml``
     - Valid model input.
     - ``GenerateResult.artopVersion`` is non-empty string.
     - QDX-SWE-041
   * - QDX-UT-052
     - ``generateArxml``
     - Valid model input. Inspect returned ARXML bytes.
     - No ``<TIMESTAMP>`` or ``<UUID>`` elements present in output.
     - QDX-SWE-038

3.12 intent_router module (QDX-UT-053 to QDX-UT-056)
------------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-053
     - ``route``
     - Request with ``active_designer = "C6"``. Classic extension
       installed. Domain Service mock returns Classic ops.
     - ``Ok(OperationPlan { domain: Classic, .. })``.
     - QDX-SWE-050, QDX-SWE-077
   * - QDX-UT-054
     - ``route``
     - Request with ``active_designer = "BD5"``. BPCT extension
       installed. Domain Service mock returns BPCT ops.
     - ``Ok(OperationPlan { domain: Bpct, .. })``.
     - QDX-SWE-050, QDX-SWE-080
   * - QDX-UT-055
     - ``route``
     - Request with ``active_designer = "C1"``. No domain extension
       installed for Classic.
     - ``Err(AgentError::DomainExtensionNotInstalled)``.
     - QDX-SWE-077
   * - QDX-UT-056
     - ``route``
     - Request with ``config.exclude_yaml_content = true``.
       Inspect the payload sent to the LLM mock.
     - LLM mock receives prompt with no YAML file content.
       OperationPlan is still returned.
     - QDX-SWE-051

3.13 audit_logger module (QDX-UT-057 to QDX-UT-059)
-----------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-057
     - ``record``
     - Valid ``AuditEvent`` with UTC timestamp.
     - ``Ok(())``. File contains one JSON line. Parsed JSON has
       non-null ``timestamp`` and ``event_type``.
     - QDX-SWE-052
   * - QDX-UT-058
     - ``record``
     - Two sequential calls with different events.
     - File contains two newline-separated JSON objects.
     - QDX-SWE-052
   * - QDX-UT-059
     - ``record``
     - Audit log directory is read-only (chmod 444).
     - ``Err(AuditError::IoError)``. Calling operation is not
       affected (audit error does not propagate).
     - QDX-SWE-052

3.14 bpct::mcu_defaults (QDX-UT-060 to QDX-UT-061)
----------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-060
     - ``get``
     - ``McuFamily::Tc3xx``.
     - Returns ``McuDefaults`` with ``flash_page_size_bytes = 256``,
       ``max_spi_clock_mhz = 80``, ``mcu_clock_mhz = 200``.
     - QDX-SWE-063, QDX-SWE-098
   * - QDX-UT-061
     - ``get``
     - All six MCU family variants called in sequence.
     - All return ``McuDefaults`` with ``mcu_clock_mhz > 0``.
     - QDX-SWE-063

3.15 bpct::validation VR_007 rule (QDX-UT-062 to QDX-UT-065)
--------------------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-062
     - ``VR007WatchdogRule::check``
     - ``wdg_timeout_ms = 2100``, ``erase_timeout_ms = 2000``,
       ``disable_during_erase = false``.
     - Empty ``DiagnosticList``. Constraint satisfied.
     - QDX-SWE-069
   * - QDX-UT-063
     - ``VR007WatchdogRule::check``
     - ``wdg_timeout_ms = 1500``, ``erase_timeout_ms = 2000``,
       ``disable_during_erase = false``.
     - One diagnostic. ``code = "VR_007"``, ``severity = Error``.
     - QDX-SWE-069
   * - QDX-UT-064
     - ``VR007WatchdogRule::check``
     - ``wdg_timeout_ms = 1500``, ``erase_timeout_ms = 2000``,
       ``disable_during_erase = true``.
     - Empty ``DiagnosticList``. Rule skipped when disabled.
     - QDX-SWE-069
   * - QDX-UT-065
     - ``VR007WatchdogRule::check``
     - ``wdg_timeout_ms = 1500``, ``erase_timeout_ms = 2000``.
     - Diagnostic ``message`` contains both values (1500, 2000)
       and a suggested minimum value (2100).
     - QDX-SWE-037, QDX-SWE-069

3.16 bpct::generator (QDX-UT-066 to QDX-UT-068)
-------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-066
     - ``emit``
     - Valid TC3xx BpctModel, no-security profile.
     - ``Ok``. ``cfg.h`` present. Contains
       ``#define FBL_FLASH_PAGE_SIZE  256``.
     - QDX-SWE-075
   * - QDX-UT-067
     - ``emit``
     - Valid model with ``SecurityProfile::FullSecurity``.
     - ``bl-security.yaml`` generated with
       ``FBL_SEC_BOOT_ENABLED = TRUE`` and algorithm = ``RSA2048``.
     - QDX-SWE-075
   * - QDX-UT-068
     - ``emit``
     - Complete BpctModel for any MCU family.
     - Exactly six output files written to temp dir.
     - QDX-SWE-075

3.17 lwbsw::validation (QDX-UT-069 to QDX-UT-073)
---------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-069
     - ``ResourceBudgetRule::check``
     - 10-module model with total ROM = 120 KB, RAM = 25 KB,
       CPU = 7%.
     - Empty ``DiagnosticList``.
     - QDX-SWE-084
   * - QDX-UT-070
     - ``ResourceBudgetRule::check``
     - Module set with ROM estimate = 200 KB (exceeds 150 KB target).
     - One diagnostic, ``code = "LWBSW-VAL-001"``,
       ``severity = Error``.
     - QDX-SWE-084
   * - QDX-UT-071
     - ``ResourceBudgetRule::check``
     - Module set with CPU estimate = 15% (exceeds 10% target).
     - One diagnostic, ``code = "LWBSW-VAL-003"``,
       ``severity = Error``.
     - QDX-SWE-084
   * - QDX-UT-072
     - ``Icc2ConformanceRule::check``
     - LW-BSW YAML with no ICC-3 fields.
     - Empty ``DiagnosticList``.
     - QDX-SWE-090
   * - QDX-UT-073
     - ``Icc2ConformanceRule::check``
     - LW-BSW YAML containing an ICC-3-only field path.
     - One diagnostic, ``code = "LWBSW-VAL-010"``,
       ``severity = Warning``. Message contains the field path.
     - QDX-SWE-090

3.18 lwbsw::scheduling (QDX-UT-074 to QDX-UT-076)
---------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-074
     - ``build_scheduling_map``
     - Three tasks with disjoint module sets. No shared resources.
     - ``SchedulingMap`` with 3 entries. ``race_conditions`` empty.
     - QDX-SWE-085
   * - QDX-UT-075
     - ``build_scheduling_map``
     - Two tasks both accessing COM buffer with no mutex defined.
     - ``race_conditions`` contains one entry describing the
       shared resource and the two task names.
     - QDX-SWE-085
   * - QDX-UT-076
     - ``build_scheduling_map``
     - Default 10-module model with standard task periods.
     - ``cpu_load_estimate_percent`` is between 5% and 10%.
     - QDX-SWE-085

3.19 lwbsw::generator (QDX-UT-077 to QDX-UT-079)
--------------------------------------------------

.. list-table::
   :widths: 12 14 40 18 16
   :header-rows: 1

   * - Test ID
     - Function under test
     - Test description and stimulus
     - Expected result
     - SWE.1 ref
   * - QDX-UT-077
     - ``emit``
     - Complete 10-module LwBswModel.
     - 21 files written: 20 source files (.h / .c pairs) + 1 report.
     - QDX-SWE-086, QDX-SWE-087
   * - QDX-UT-078
     - ``emit``
     - Valid model with known ROM/RAM values.
     - Config Report contains ROM and RAM actuals alongside the
       150 KB / 30 KB targets.
     - QDX-SWE-086
   * - QDX-UT-079
     - ``emit``
     - Model with one detected race condition from scheduling.
     - Config Report ``race_conditions`` section is non-empty.
     - QDX-SWE-086


4. Defect Management
=====================

All test failures raise a Jira defect with the following mandatory
fields:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Field
     - Required content
   * - Summary
     - ``[QDX-UT-NNN] <Function under test> — <brief failure description>``
   * - Unit test ID
     - ``QDX-UT-NNN`` — links to this document
   * - SWE.1 requirement
     - ``QDX-SWE-NNN`` — the violated requirement
   * - Failure evidence
     - Full test output and stack trace pasted or attached
   * - Severity
     - Critical (Error diagnostic wrong) / Major (wrong return value) /
       Minor (message text incorrect) / Trivial (formatting)
   * - Assignee
     - Owning crate lead


5. Coverage Report
===================

Coverage is measured per crate on every merge to ``main``. The
following targets must be met before a release baseline is cut:

.. list-table::
   :widths: 35 20 20 25
   :header-rows: 1

   * - Crate / module
     - Line target
     - Branch target
     - Measurement command
   * - ``core::yaml``
     - ≥ 90%
     - ≥ 85%
     - ``cargo llvm-cov --package core_yaml``
   * - ``core::validation``
     - ≥ 90%
     - ≥ 85%
     - ``cargo llvm-cov --package core_validation``
   * - ``core::ops``
     - ≥ 90%
     - ≥ 85%
     - ``cargo llvm-cov --package core_ops``
   * - ``classic::validation``
     - ≥ 85%
     - ≥ 80%
     - ``cargo llvm-cov --package classic_validation``
   * - ``adaptive::validation``
     - ≥ 85%
     - ≥ 80%
     - ``cargo llvm-cov --package adaptive_validation``
   * - ``bpct::validation``
     - ≥ 85%
     - ≥ 80%
     - ``cargo llvm-cov --package bpct_validation``
   * - ``lwbsw::validation``
     - ≥ 85%
     - ≥ 80%
     - ``cargo llvm-cov --package lwbsw_validation``
   * - IDE Layer (TypeScript)
     - ≥ 80%
     - ≥ 70%
     - ``jest --coverage``
   * - ARXML Gateway (Java)
     - ≥ 80%
     - ≥ 70%
     - ``mvn jacoco:report``


6. Open Issues
===============

.. list-table::
   :widths: 15 55 15 15
   :header-rows: 1

   * - Issue ID
     - Description
     - Owner
     - Target date
   * - TBD-SWE4-001
     - Unit tests QDX-UT-080 through QDX-UT-NNN for Adaptive
       designer module functions (A1–A6 canvas, sync, Adaptive
       validation rules ADAPTIVE-VAL-001 through 006). Blocked on
       TBD-SDD-002.
     - Adaptive Domain Lead
     - 2026-05-30
   * - TBD-SWE4-002
     - Unit tests for ``lwbsw::import::from_dext`` and
       ``from_dbc`` (DEXT/DBC import, field mapping, lossy-conversion
       warning generation). Blocked on TBD-SDD-004.
     - LW-BSW Lead
     - 2026-06-01
   * - TBD-SWE4-003
     - Performance test harness for QDX-UT-001 (workspace open
       ≤ 30 s) and QDX-UT-014 (WASM validation ≤ 500 ms). These
       tests require representative fixture files and a controlled
       CI runner with documented hardware specification.
     - Platform Engineering
     - 2026-04-30


.. _swe4_changelog:

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
     - Initial draft derived from QDX-SDD-DOC-001 (SWE.3). Covers
       79 unit tests (QDX-UT-001 to QDX-UT-079) across 19 modules and
       crates. Defines verification strategy, test isolation
       requirements, static analysis checks, entry/exit criteria,
       defect management fields and coverage targets per crate.

----

*This document is version-controlled in Git at*
``docs/50-testing/00-swe.4/platform/sw_unit_verification.rst``.
*All unit tests must pass and coverage targets must be met before
a SWE.4 sign-off is given on a release baseline.*
