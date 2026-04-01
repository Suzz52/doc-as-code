.. _roadmap:

Platform Roadmap
================

.. raw:: html

   <p style="font-size: 1.15rem; line-height: 1.8; max-width: 740px;
             color: var(--color-foreground-secondary, #444); margin-bottom: 2.5rem;">
     The Qorix Developer roadmap is organised by quarter and aligned to the
     ASPICE V-cycle baselines. Each milestone delivers a coherent, testable
     capability increment — not a partial feature — so that engineering teams
     can adopt the platform progressively without workflow disruption.
   </p>

.. admonition:: Roadmap status
   :class: note

   This roadmap reflects the current planning baseline. Items marked
   **TBD** have an owner and target date but are pending confirmation.
   Architecture dependencies are noted where a milestone is gated on
   an upstream TBD being resolved. See the open issues sections of
   QDX-SWA-DOC-001 (SWE.2) and QDX-SDD-DOC-001 (SWE.3) for the
   corresponding technical TBDs.

----

Q1 2026 — Domain Core and Gateway Foundation
----------------------------------------------

**Theme:** Establish the skeleton of every subsystem and prove the
end-to-end generation pipeline on a minimal Classic AUTOSAR project.

.. list-table::
   :widths: 5 30 65
   :header-rows: 1

   * - #
     - Milestone
     - Description
   * - 1.1
     - **core::* crate baseline**
     - ``core::model``, ``core::yaml``, ``core::validation``, ``core::ops``
       and ``core::migration`` implemented, unit-tested (≥ 80 % coverage)
       and compiled to all three build targets (service, WASM, CLI) with
       zero conditional business-logic compilation flags. Validates
       QDX-SWE-046 (same Rust core for all build targets).
   * - 1.2
     - **classic::* domain crates**
     - ``classic::model``, ``classic::validation`` (rules CLASSIC-VAL-001
       through 006), ``classic::ops`` and ``classic::migration`` implemented.
       The six Classic YAML source files (swc-design, signals-comstack,
       ecu-bsw, os-scheduling, mem-nvram, rte-mapping) load, validate and
       round-trip correctly.
   * - 1.3
     - **ARXML Gateway skeleton**
     - Spring Boot + ARTOP process starts, exposes GraphQL SDL, handles
       ``importArxml`` and ``generateArxml`` mutations for a minimal Classic
       SWC. ``core::gql_client`` generated from the SDL. End-to-end path:
       YAML → Domain Service → Gateway → ARXML is green for the
       Powertrain Control template.
   * - 1.4
     - **qorix_cli validate + generate**
     - ``validate`` exits 0 on clean project, 1 on ERROR diagnostics, with
       newline-delimited JSON on stdout. ``generate`` calls the Domain
       Service and Gateway and writes ARXML + ``provenance.json``.
   * - 1.5
     - **SWE.2 / SWE.3 documentation baseline**
     - QDX-SWA-DOC-001 (SWE.2) and QDX-SDD-DOC-001 (SWE.3) first drafts
       committed and building in the portal. All 101 SWE.1 requirements
       linked to a ``QDX-SWA-SP-NNN`` architecture spec.

**Key TBDs gating Q1:**

- ``TBD-SWA-001`` — Domain Service HTTP/gRPC API surface (endpoint names,
  request/response schemas, error codes).
- ``TBD-SWA-002`` — ARXML Gateway GraphQL SDL publication policy and
  ``core::gql_client`` regeneration trigger.

----

Q2 2026 — IDE Extensions and WASM Integration
-----------------------------------------------

**Theme:** Put the domain core into the hands of engineers inside VS Code and
Theia with functional Classic designers and in-process WASM validation.

.. list-table::
   :widths: 5 30 65
   :header-rows: 1

   * - #
     - Milestone
     - Description
   * - 2.1
     - **qorix_core_wasm build target**
     - ``validateYaml(content, schema_id)`` WASM export integrated into the
       VS Code extension via the WASM Bridge. Returns ``DiagnosticList``
       within 500 ms for single-file validation without a network call.
       QDX-SWE-031 and QDX-SWE-055 pass SWE.6 qualification tests.
   * - 2.2
     - **YAML editor with LSP and schema completion**
     - JSON Schema-backed autocompletion, required-field squiggles,
       hover documentation and go-to-definition for all six Classic YAML
       formats. QDX-SWE-006 and QDX-SWE-007 pass.
   * - 2.3
     - **Classic designers C1 and C2**
     - C1 SWC & Interface designer (SWC topology, ports, interfaces,
       runnables) and C2 Signals & ComStack designer (CAN networks,
       I-PDUs, signals, COM stack layer chain) operational with Command
       Bus / WASM Bridge integration. Designer-to-YAML and YAML-to-designer
       synchronisation (QDX-SWE-029, QDX-SWE-030) pass.
   * - 2.4
     - **Diagnostics Panel**
     - Merged display of WASM fast + Domain Service deep diagnostics.
       Severity sort, YAML file and path attribution, click-to-navigate.
       QDX-SWE-036 and QDX-SWE-037 pass.
   * - 2.5
     - **Project Creation Wizard — Classic AUTOSAR**
     - Welcome screen, platform version selection (H1 / R4.x), template
       selection (6 templates), project configuration step (MCU family,
       BSW module toggles), review and confirm. QDX-SWE-091 through
       QDX-SWE-094 and QDX-SWE-100/101 pass.
   * - 2.6
     - **SWE.4 unit test suite — IDE Layer and core::***
     - QDX-UT-001 through QDX-UT-034 green. Coverage ≥ 80 % per crate.
       ``cargo clippy -D warnings`` and ``cargo fmt --check`` enforced on
       every PR via GitHub Actions.

**Key TBDs gating Q2:**

- ``TBD-SWA-004`` — Deployment topology for Domain Service and ARXML Gateway
  in desktop (local) vs. server-hosted modes.

----

Q3 2026 — AUTOSAR Modelling, Full Classic and Adaptive
-------------------------------------------------------

**Theme:** Complete the Classic designer set, deliver the full Adaptive A1–A6
designer set, and establish the Adaptive manifest generation pipeline.

.. list-table::
   :widths: 5 30 65
   :header-rows: 1

   * - #
     - Milestone
     - Description
   * - 3.1
     - **Classic designers C3 — C6**
     - C3 ECU & BSW, C4 OS & Scheduling, C5 Memory & NvM, C6 RTE & Mapping
       operational. Unmapped runnable and port detection (QDX-SWE-016).
       Generation readiness indicator in C6. QDX-SWE-009 through
       QDX-SWE-016 pass SWE.6 qualification tests.
   * - 3.2
     - **adaptive::* domain crates**
     - ``adaptive::model``, ``adaptive::validation`` (rules ADAPTIVE-VAL-001
       through 006), ``adaptive::ops`` and ``adaptive::migration``
       implemented. Cross-file service binding, resource constraint,
       scheduling conflict and deployment consistency checks operational.
       QDX-SWE-017 through QDX-SWE-028 pass.
   * - 3.3
     - **Adaptive designers A1 — A6**
     - A1 Application & Service, A2 Communication, A3 Machine Design,
       A4 Platform Services, A5 Execution Management, A6 Deployment all
       operational. Adaptive ARXML gateway path (ApplicationManifest,
       ExecutionManifest, MachineManifest generation) end-to-end green.
       QDX-IT-011 and QDX-IT-012 pass.
   * - 3.4
     - **Project Creation Wizard — Adaptive**
     - Template selection (6 templates including Perception Pipeline,
       High-Performance Compute), configuration step (CPU architecture,
       platform service toggles), review and confirm. QDX-SWE-095 and
       QDX-SWE-096 pass.
   * - 3.5
     - **Workspace-level consistency check**
     - ``domain_service::load_workspace`` cross-file validation pass across
       all projects in the workspace. Per-designer export readiness
       indicators in C6 and A6. QDX-SWE-035 passes.
   * - 3.6
     - **ARXML import round-trip**
     - ``importArxml`` → ``generateArxml`` round-trip with DaVinci/Tresos
       reference fixtures. Lossy-conversion warnings reported accurately.
       QDX-IT-007 passes. Reference fixtures committed to
       ``tests/fixtures/import/``.
   * - 3.7
     - **SWE.5 integration test suite — Stages 1–4**
     - QDX-IT-001 through QDX-IT-012 green against real (not mocked)
       Domain Service, WASM and Gateway instances.

**Key TBDs gating Q3:**

- ``TBD-SDD-002`` — Adaptive::validation unit tests (QDX-UT-080+). Blocked
  on ``adaptive::model`` struct definitions being finalised.
- ``TBD-SWA-003`` — BPCT and LW-BSW crate structure confirmation.

----

Q4 2026 — Bootloader (BPCT), LW-BSW and AI-Assist
---------------------------------------------------

**Theme:** Deliver the BPCT BD1–BD6 designer set, LW-BSW 10-module
configuration, and the Qorix Agent MCP layer with domain-specific AI-Assist.

.. list-table::
   :widths: 5 30 65
   :header-rows: 1

   * - #
     - Milestone
     - Description
   * - 4.1
     - **bpct::* domain crates**
     - ``bpct::model``, ``bpct::validation`` (VR_003, VR_007, VR_010,
       VR_013, VR_015, VR_020), ``bpct::ops``, ``bpct::generator`` and
       ``bpct::mcu_defaults`` implemented. MCU defaults table for all six
       MCU families. QDX-UT-060 through QDX-UT-068 green.
   * - 4.2
     - **BPCT designers BD1 — BD6**
     - All six BPCT designers operational. VR_NNN cross-designer validation
       pass. C header and Makefile generation deterministic. BPCT project
       creation wizard (QDX-SWE-097 / QDX-SWE-098). QDX-SWE-063 through
       QDX-SWE-076 pass SWE.6 qualification tests. QDX-IT-013 and
       QDX-IT-014 pass.
   * - 4.3
     - **lwbsw::* domain crates**
     - ``lwbsw::model``, ``lwbsw::validation`` (ResourceBudgetRule,
       Icc2ConformanceRule), ``lwbsw::generator``, ``lwbsw::scheduling``
       and ``lwbsw::import`` (DEXT/DBC) implemented. Config Report
       generation (scheduling map, resource budget, race conditions,
       safety violations). QDX-UT-069 through QDX-UT-079 green.
   * - 4.4
     - **LW-BSW designer and project wizard**
     - 10-module configuration views. ECU/DEXT and DBC import in wizard.
       ICC-2 schema filter enforced. LW-BSW project creation (QDX-SWE-099).
       QDX-SWE-081 through QDX-SWE-090 pass. QDX-IT-016 through
       QDX-IT-018 pass.
   * - 4.5
     - **Qorix Agent MCP Layer**
     - Intent Router, Tool Registry, Classic MCP tools (suggest_runnable_
       mappings, fix_unmapped_signals, balance_core_load), Adaptive MCP
       tools (suggest_service_bindings, propose_deployment), BPCT MCP tools
       (suggest_timing_parameters, validate_security_config,
       fix_cross_designer_violations), LW-BSW Config Insight. OperationPlan
       review/accept/reject flow. Audit log. Data transmission control.
       QDX-SWE-047 through QDX-SWE-053 and QDX-SWE-077 through
       QDX-SWE-080 pass. QDX-IT-015 passes.
   * - 4.6
     - **SWE.5 integration test suite — Stages 5–6**
     - QDX-IT-013 through QDX-IT-021 green.
   * - 4.7
     - **SWE.6 qualification baseline**
     - All 101 QDX-QT-NNN tests executed on the released platform build.
       Test execution log archived. SWE.6 sign-off.

**Key TBDs gating Q4:**

- ``TBD-SDD-004`` — LW-BSW DEXT/DBC import module function specifications.
- ``TBD-SWE6-004`` — Controlled LLM test environment for AI-Assist
  qualification tests.
- ``TBD-SWE5-004`` — Agent data transmission control integration test with
  real LLM and data-capture proxy.

----

Future Direction (Post-Q4)
---------------------------

The following items are on the product direction horizon but are not
committed to a specific quarter. They will be moved into the quarterly
backlog as upstream TBDs are resolved and capacity is confirmed.

.. list-table::
   :widths: 35 65
   :header-rows: 1

   * - Item
     - Description
   * - **Eclipse S-Core full support**
     - ``score::model``, ``score::validation``, ``score::ops`` crate
       structure and designer set. Gated on TBD-SWA-005 and TBD-SDD-005.
   * - **BPCT and LW-BSW bpct::* / lwbsw::* full crate spec**
     - Detailed function specifications for remaining modules. Gated on
       TBD-SWA-003 and TBD-SDD-003.
   * - **Multi-workspace and team collaboration features**
     - Shared workspace validation, cross-project reference resolution,
       team-level audit dashboards.
   * - **Extended AUTOSAR schema version support**
     - R24-11 Adaptive and AUTOSAR 4.4 Classic import/export. Gated on
       TBD-SWE-002 (schema version confirmation).
   * - **Performance measurement dashboard**
     - Documented benchmark fixture, automated timing regression tests
       for QDX-SWE-054 through 058. Gated on TBD-SWE-001 and TBD-SWE6-002.
   * - **LLM backend self-hosted deployment option**
     - Full self-hosted LLM configuration with YAML content transmission
       controls for enterprise air-gapped deployments.
