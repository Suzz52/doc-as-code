.. _overview:

Platform Overview
=================

.. raw:: html

   <p style="font-size: 1.15rem; line-height: 1.8; max-width: 740px;
             color: var(--color-foreground-secondary, #444); margin-bottom: 2.5rem;">
     Qorix Developer is a unified engineering platform for automotive
     software-defined vehicle middleware — bringing together AUTOSAR Classic,
     Adaptive, Bootloader and LW-BSW authoring, validation, generation and
     AI-assisted workflows into a single, traceable, version-controlled product.
   </p>

----

The Problem Qorix Developer Solves
------------------------------------

Automotive software teams working across Classic AUTOSAR, Adaptive AUTOSAR
and bootloader domains have historically operated with a fragmented toolchain:
separate GUI tools per domain, ARXML files checked in as binary blobs,
validation rules buried in proprietary tool internals, configuration parameters
scattered across disconnected spreadsheets, and no programmatic access to the
engineering model for CI/CD pipelines.

The consequences are familiar — configuration drift between design documents
and generated artefacts, merge conflicts on binary files, validation that only
runs on an engineer's local machine, and a complete inability to review what
actually changed between two configuration baselines.

Qorix Developer is the answer to all of this. It replaces opaque tool-centric
workflows with a model-driven, YAML-first, version-controlled engineering
environment where configuration is code, validation is always-on, generation
is deterministic, and every artefact is traceable to a requirement.

----

What the Platform Is
---------------------

Qorix Developer is simultaneously three things:

**An engineering IDE** — a VS Code and Theia extension providing domain-specific
visual designers (C1–C6 for Classic AUTOSAR, A1–A6 for Adaptive, BD1–BD6 for
Bootloader), a YAML editor with schema-driven completion and LSP diagnostics,
a project creation wizard for all supported stacks, an AI Chat Panel for guided
engineering assistance, and a Diagnostics Panel that merges fast in-process and
deep cross-file validation results in real time.

**A validation and generation engine** — a Rust domain platform compiled from a
single codebase into three build targets: an HTTP/gRPC domain service for deep
semantic validation and generation, a WebAssembly module for in-IDE sub-500 ms
local validation, and a CLI binary for headless CI pipelines. The same rule set
runs everywhere — what is valid in the IDE is valid in CI, always.

**A documentation and traceability system** — every requirement, design decision,
validation rule and generated artefact is traceable through a sphinx-needs
powered documentation-as-code pipeline. Requirements are RST blocks with
machine-readable IDs. Architecture decisions are permanent ADR records.
Test cases link back to the requirements they verify. The portal you are
reading now is built from the same repository as the software it describes.

----

Supported Engineering Domains
------------------------------

.. list-table::
   :widths: 20 30 50
   :header-rows: 1

   * - Domain
     - Designers
     - Scope
   * - **Classic AUTOSAR**
     - C1 — C6
     - SWC and interface authoring, COM stack and signal design, ECU and BSW
       configuration, OS scheduling, NvM and memory layout, RTE and runnable
       mapping. Generates deterministic ARXML via ARTOP.
   * - **Adaptive AUTOSAR**
     - A1 — A6
     - Service interface and application design, communication and service
       instance binding, machine design and resource modelling, platform
       services (ara::log / ara::per / ara::phm / ara::tsync), execution
       management and scheduling, deployment mapping. Generates
       ApplicationManifest, ExecutionManifest and MachineManifest ARXML.
   * - **Bootloader (BPCT)**
     - BD1 — BD6
     - MCU selection and FBL project identity, UDS communication channel
       configuration, memory and NvM layout, core bootloader parameters and
       UDS session state machine, timing and watchdog constraint chain,
       cryptographic and secure boot configuration. Generates ``cfg.h``,
       ``cfg.c`` and ``Makefile``.
   * - **LW-BSW**
     - Classic C1–C6 (ICC-2 filtered)
     - Light Weight BSW for small ECUs — 10 modules (COM, Diag, CanTp, CanIf,
       CDD, OS, IOHAB, EMM, NM, NVRAM), OSEK SC-1, ≈ 150 KB ROM target.
       ECU/DEXT and DBC import. Generates module ``.h`` / ``.c`` files and a
       Config Report with scheduling map, resource budget and race condition
       analysis.
   * - **Eclipse S-Core**
     - Wizard only (initial)
     - Safety-oriented AUTOSAR-independent stack for embedded systems.
       Project creation and configuration scaffolding.

----

Core Subsystems
---------------

The platform architecture is decomposed into four primary subsystems with
strict one-directional layering. The Rust domain never depends on the IDE
layer or the Agent; the Agent never writes YAML directly.

.. raw:: html

   <div style="background: var(--color-background-secondary, #f7f7f8);
               border-left: 4px solid #1a7fd4;
               border-radius: 6px;
               padding: 1.4rem 1.6rem;
               margin: 1.5rem 0 2rem 0;">
   <strong style="display:block; font-size: 1rem; margin-bottom: 0.6rem;">
     Layering rule — enforced by crate dependency graph
   </strong>
   IDE Layer → Rust Domain Service (HTTP/gRPC) → ARXML Gateway (GraphQL)<br/>
   IDE Layer → qorix_core_wasm (in-process WASM)<br/>
   IDE Layer → Qorix Agent (MCP) → Rust Domain Service
   </div>

**1. IDE Layer (VS Code Extension / Theia)**

The user-facing surface. Provides six Classic designers (C1–C6), six
Adaptive designers (A1–A6), six Bootloader designers (BD1–BD6), a YAML
editor with JSON Schema completion and LSP hover/go-to-definition, a Command
Bus that translates designer interactions into typed ``core::ops`` operations,
a WASM Bridge for in-process fast validation without a network call, a Domain
Service Client for deep semantic validation and generation requests, an AI
Chat Panel backed by the Qorix Agent MCP endpoint, a Diagnostics Panel
merging WASM and domain-service results, and a Project Creation Wizard
supporting all five stack types.

**2. Rust Domain Platform**

The semantic core. Owns the canonical domain models for Classic and
Adaptive AUTOSAR, BPCT and LW-BSW. Executes all validation rules via the
``core::validation`` rule engine. Applies and rolls back ``core::ops``
operation plans. Produces all generation outputs (ARXML via the gateway,
BPCT C headers, LW-BSW module files). Compiled from one codebase into:

- **Rust Domain Service** — HTTP/gRPC server, multi-threaded, for deep
  cross-file semantic validation, workspace consistency checks, search,
  generation orchestration and MCP tool endpoints.
- **qorix_core_wasm** — WebAssembly build target loaded in-process inside
  the IDE host. Returns ``DiagnosticList`` within 500 ms for single-file
  schema validation without any network dependency.
- **qorix_cli** — statically linked CLI binary for ``validate`` and
  ``generate`` subcommands in CI pipelines.

The same validation rule set runs in all three targets. A rule change in
``classic::validation`` takes effect in the IDE, in CI and in the service
simultaneously on the next build.

**3. ARXML Gateway (Spring Boot + ARTOP)**

The exclusive ARXML import and export boundary. Wraps the AUTOSAR Tool
Platform (ARTOP) and exposes a versioned GraphQL SDL to the Rust domain
layer via the ``core::gql_client`` generated client. The Rust domain
crates have zero dependency on EMF, ARTOP or any JVM library — the
gateway is the only path for ARXML I/O. All ARXML generation is
deterministic: identical validated model + identical ARTOP version =
byte-identical ARXML output.

**4. Qorix Agent — MCP Layer**

The AI orchestration layer. Receives natural language engineering prompts
from the IDE AI Chat Panel, detects the active domain from the open designer
tab (C* → Classic, A* → Adaptive, BD* → BPCT), routes to the correct
domain-specific MCP tool set via the Tool Registry, calls the Rust Domain
Service for typed operation proposals, invokes the LLM backend for
natural-language explanation, and returns a typed ``OperationPlan`` for
engineer review. The Agent never writes to a YAML file directly — the
engineer must explicitly accept the plan before any change is persisted.

----

Key Engineering Principles
---------------------------

Six principles are enforced at the architecture level and validated through
the SWE.4/SWE.5/SWE.6 test suites:

.. list-table::
   :widths: 30 70
   :header-rows: 0

   * - **YAML as canonical model**
     - All project configuration is persisted as UTF-8 YAML with stable key
       ordering. ARXML is used only for import and export through the gateway.
       Human-readable, diff-friendly, Git-native. (ADR-001)
   * - **Single codebase, three build targets**
     - The ``core::*``, ``classic::*``, ``adaptive::*`` crates compile to
       HTTP/gRPC service, WASM and CLI without conditional compilation that
       alters validation or generation logic. Eliminates the class of defect
       where IDE validation diverges from CI. (ADR-002, QDX-SWE-046)
   * - **ARXML isolation**
     - Rust domain crates have zero JVM/EMF/ARTOP dependency. The gateway is
       the only ARXML path, accessed exclusively via ``core::gql_client``.
       Decouples ARTOP upgrades from the Rust build. (ADR-003)
   * - **Deterministic generation**
     - Identical validated inputs + identical tool version = byte-identical
       outputs. No timestamps, random GUIDs or non-deterministic serialisation
       in generated artefacts. (ADR-008, QDX-SWE-038)
   * - **Engineer-in-the-loop for AI**
     - The Qorix Agent produces ``OperationPlan`` structs for review. It does
       not apply changes autonomously. Every accepted plan is recorded in the
       audit log. (ADR-004, QDX-SWE-047, QDX-SWE-048)
   * - **Validation-gated generation**
     - Generation and publication are refused when any ``Severity::Error``
       diagnostic is present. The error count is surfaced in the Diagnostics
       Panel and in the CLI exit code. (QDX-SWE-034)

----

End-to-End Workflow
--------------------

A typical engineering session on Qorix Developer follows this path:

.. list-table::
   :widths: 8 30 62
   :header-rows: 1

   * - Step
     - Action
     - What happens in the platform
   * - 1
     - **Open workspace**
     - ``workspace_manager::open`` reads ``workspace.yaml``, verifies all
       project paths, calls ``domain_service::load_workspace`` which parses
       all YAML files, builds the domain model and runs an initial
       cross-file validation pass. Total ≤ 30 s.
   * - 2
     - **Author in designer or YAML editor**
     - Designer interactions dispatch ``core::ops`` operations through the
       Command Bus. The WASM Bridge validates in-process (< 500 ms) and
       updates the Diagnostics Panel. YAML files are written atomically
       (write-to-temp + rename) only when no ERROR diagnostics are present.
   * - 3
     - **Resolve diagnostics**
     - The Diagnostics Panel shows merged WASM (fast, single-file) and
       Domain Service (deep, cross-file) results sorted by severity.
       Clicking a diagnostic navigates to the affected YAML line or designer
       element. Generation is blocked until all ERRORs are resolved.
   * - 4
     - **Use AI Assist (optional)**
     - The engineer types a prompt in the AI Chat Panel (e.g. "Fix all
       unmapped runnables"). The Qorix Agent detects the active domain,
       calls the appropriate MCP tool on the Domain Service, receives a
       typed ``OperationPlan``, asks the LLM for a natural-language
       explanation, and presents the plan with Accept / Reject controls.
       No YAML is written until Accept is clicked.
   * - 5
     - **Generate artefacts**
     - ``domain_service::generate`` runs a final validation pass, refuses if
       ERRORs remain, calls ``core::gql_client`` GraphQL mutations to the
       ARXML Gateway (for Classic/Adaptive) or invokes ``bpct::generator``
       / ``lwbsw::generator`` directly. Writes deterministic outputs to
       ``out/`` and a ``provenance.json`` recording tool version, ARTOP
       version, source file Git SHAs and UTC timestamp.
   * - 6
     - **CI pipeline validation**
     - The same Rust crate tree runs headless via ``qorix_cli validate`` and
       ``qorix_cli generate``. Structured newline-delimited JSON diagnostics
       on stdout. Non-zero exit on any ERROR. Byte-identical output to the
       IDE path for identical inputs.
   * - 7
     - **Commit and review**
     - YAML source files, generated artefacts and ``provenance.json`` are
       committed to Git. PR reviewers see line-level diffs of configuration
       changes. Documentation changes go through the same PR workflow.

----

Documentation-as-Code Architecture
-------------------------------------

The documentation portal is itself an engineering artefact governed by the
same principles as the software it describes.

Every SYS.2 requirement, SWE.1 software requirement, SWE.2 architecture
specification, SWE.3 design element, SWE.4 unit test, SWE.5 integration test
and SWE.6 qualification test is a ``sphinx-needs`` typed block with a
permanent machine-readable ID. Broken traceability links are build errors.
The ``needflow`` directive renders live dependency graphs. The ``needtable``
directive generates traceability matrices from the live document graph — not
from manually maintained spreadsheets.

Changes to requirements go through the same pull request workflow as code
changes. CODEOWNERS ensures that requirement changes require architecture
review and that design changes require crate-lead sign-off. The rendered
portal at any given Git SHA is an accurate reflection of the engineering
decisions and obligations at that point in time.

----

Where to Go Next
-----------------

.. list-table::
   :widths: 35 65
   :header-rows: 0

   * - :doc:`vision`
     - The problem statement, goals and non-goals that motivate every
       architectural and product decision in the platform.
   * - :doc:`roadmap`
     - Quarter-by-quarter delivery plan with capability milestones and
       open TBDs.
   * - :doc:`glossary`
     - Authoritative definitions for every acronym and domain term used
       across the documentation set.
   * - :ref:`sys_requirements`
     - SYS.2 System Requirements Specification (QDX-SRS-001) — the top
       of the traceability chain.
   * - :ref:`sw_requirements`
     - SWE.1 Software Requirements Specification (QDX-SWE-DOC-001) — 101
       atomic, testable requirements derived from SYS.2.
   * - :ref:`sw_architecture`
     - SWE.2 Software Architecture Description (QDX-SWA-DOC-001) — four
       subsystems, three build targets, eight ADRs and the full traceability
       matrix.
