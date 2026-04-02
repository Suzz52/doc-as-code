.. ============================================================
.. QORIX DEVELOPER — Software Architecture Description
.. ASPICE: SWE.2
.. Derived from: QDX-SWE-DOC-001 (SWE.1), Qorix Developer
..               C4 Architecture (L1–L3 + Data Flow)
.. Constrained by: QDX-SYS3-DOC-001 (SYS.3, in progress)
.. Validated by: QDX-VAL-001 (VAL.1, in progress)
.. ============================================================

.. _sw_architecture:

========================================================
Software Architecture Description
========================================================

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Document ID**
     - QDX-SWA-DOC-001
   * - **Product line**
     - Platform — Qorix Developer (all stacks)
   * - **Component**
     - Qorix Developer Platform — full system architecture
   * - **Version**
     - 0.1.0
   * - **Status**
     - Draft
   * - **Owner**
     - Qorix Developer Architecture Team
   * - **Approved by**
     - TBD — Approval pending
   * - **ASPICE process**
     - SWE.2 — Software Architectural Design
   * - **Parent SWE doc**
     - :ref:`sw_requirements` (QDX-SWE-DOC-001)
   * - **Parent SYS.3 doc**
     - QDX-SYS3-DOC-001 — System Architecture Description (SYS.3, in progress)
   * - **Validated by**
     - VAL.1 — Validation (QDX-VAL-001, in progress)
   * - **Jira epic**
     - QDX-EPIC-PLATFORM-SWEARCH
   * - **Git path**
     - ``docs/30-swe.2/platform/sw_architecture.rst``
   * - **Changelog**
     - See :ref:`swa_changelog`

----

.. contents:: Table of contents
   :depth: 3
   :local:

----


1. Purpose and Scope
====================

This document describes the software architecture for the **Qorix
Developer Platform** — a unified configuration authoring, validation,
generation and AI-assisted engineering environment for Classic AUTOSAR,
Adaptive AUTOSAR, Bootloader (BPCT), LW-BSW and Eclipse S-Core stacks.

It realises the requirements specified in :ref:`sw_requirements`
(QDX-SWE-DOC-001) and provides the structural basis for the following
detailed design documents:

- ``QDX-SDD-IDE-001`` — IDE Layer (VS Code Extension / Theia)
- ``QDX-SDD-RUST-001`` — Rust Domain Platform (core, classic, adaptive crates)
- ``QDX-SDD-GW-001`` — ARXML Gateway (Spring Boot + ARTOP)
- ``QDX-SDD-MCP-001`` — Qorix Agent / MCP Layer
- ``QDX-SDD-BPCT-001`` — BPCT subsystem
- ``QDX-SDD-LWBSW-001`` — LW-BSW subsystem

The key architectural concerns addressed in this document are:

- **Subsystem decomposition** — four primary subsystems (IDE Layer,
  Rust Domain Platform, ARXML Gateway, Qorix Agent) and their
  boundaries.
- **Single-codebase, three-target build model** — the Rust domain core
  compiles to HTTP/gRPC service, WebAssembly module and CLI binary
  from one codebase, guaranteeing identical validation behaviour across
  IDE and CI environments.
- **YAML as the canonical model** — ARXML is used only for import and
  export; the Rust domain never calls EMF/ARTOP directly.
- **AI engineering constraints** — the Agent never writes YAML
  directly; all mutations are typed OperationPlans reviewed and
  accepted by the engineer before persistence.
- **Extensibility model** — new stack domains (designers, validators,
  generators, MCP tools) are addable via domain extensions without
  modifying core crates.


2. Architectural Goals and Constraints
=======================================

2.1 Goals
----------

- **Strict subsystem layering** — the IDE Layer, Rust Domain Platform,
  ARXML Gateway and AI/MCP Layer have one-directional dependencies.
  The Rust domain never depends on the IDE layer or the Agent.
- **Validation parity across all deployment targets** — the same Rust
  crate tree that validates in-IDE (WASM) also validates in CI (CLI)
  and in the domain service (HTTP/gRPC). A validation rule change
  applies everywhere simultaneously.
- **ARXML isolation** — the Rust domain crates have zero dependency on
  EMF, ARTOP or any JVM library. The ARXML Gateway is the sole
  import/export boundary, accessed exclusively via the generated
  ``core::gql_client`` GraphQL client.
- **Deterministic generation** — identical validated YAML inputs with
  the same tool version must produce byte-identical ARXML, C headers
  and manifests across all three build targets.
- **Engineer-in-the-loop for AI actions** — no AI-originated mutation
  reaches a YAML file without an explicit engineer acceptance step.
  The Agent produces OperationPlans; it does not apply them.
- **Offline-capable IDE** — YAML authoring, schema validation and
  designer canvas display must function without network connectivity,
  using only the in-process WASM module.

2.2 Constraints
----------------

.. list-table::
   :widths: 45 55
   :header-rows: 1

   * - Constraint
     - Source
   * - Rust domain crates must not import any JVM, EMF or ARTOP library
     - QDX-SWE-039 — ARXML export via ARTOP GraphQL gateway
   * - WASM build target must produce identical validation results to
       the HTTP/gRPC service and CLI binary
     - QDX-SWE-046 — Same Rust core for all build targets
   * - The Qorix Agent must never write to a YAML file directly
     - QDX-SWE-047 — AI-generated OperationPlan, no direct YAML edit
   * - Generation must be refused when ERROR diagnostics remain
     - QDX-SWE-034 — Validation-gated publication
   * - All project source content must be human-readable YAML committed
       to Git; binary project formats are prohibited
     - QDX-SWE-004 — Version-control-friendly YAML persistence
   * - IDE must function offline for authoring, schema validation and
       designer display (WASM path only)
     - QDX-SWE-060 — Offline local authoring and validation
   * - Domain extensions may not modify ``core::*``, ``classic::*`` or
       ``adaptive::*`` crates
     - QDX-SWE-061 — Extension mechanism without core modification
   * - No dynamic memory allocation after initialisation in the Rust
       domain service (safety / determinism)
     - Coding standard QOR-CS-001
   * - Maximum cyclomatic complexity per function: 15
     - Coding standard QOR-CS-001
   * - No Rust ``unsafe`` blocks in ``core::*`` crates without explicit
       Chief Architect approval and documented rationale
     - Coding standard QOR-CS-001


3. Architectural Viewpoints
============================

3.1 Decomposition view — subsystem structure
---------------------------------------------

The platform decomposes into four primary subsystems. The IDE Layer is
the user-facing surface. The Rust Domain Platform is the semantic core.
The ARXML Gateway is the exclusive AUTOSAR interchange boundary. The
Qorix Agent is the AI orchestration layer. All four subsystems share
YAML files as the single source of truth persisted to Git.

.. mermaid::

   graph TD
     subgraph IDE ["IDE Layer — VS Code Ext / Theia"]
       YAML_ED["YAML Editor\nLSP · JSON Schema · squiggles"]
       DESIGNERS["Visual Designers\nC1–C6 · A1–A6 · BD1–BD6"]
       CMD_BUS["Command Bus\nexecute(domain.operation, payload)"]
       WASM_BR["WASM Bridge\nvalidateYaml() · planOps()"]
       DS_CLIENT["Domain Service Client\nHTTP / gRPC"]
       AI_PANEL["AI Chat Panel\nMCP Client"]
       DIAG_PNL["Diagnostics Panel"]
       WIZARD["Project Creation Wizard\nStack · Template · Config · Review"]
     end

     subgraph RUST ["Rust Domain Platform"]
       SVC["Rust Domain Service\nHTTP / gRPC server"]
       WASM["qorix_core_wasm\nWASM build target"]
       CLI["qorix_cli\nCLI build target"]
       subgraph CORE ["core::* crates (shared)"]
         C_MODEL["core::model"]
         C_YAML["core::yaml"]
         C_VAL["core::validation"]
         C_OPS["core::ops"]
         C_GQL["core::gql_client"]
         C_MIG["core::migration"]
       end
       subgraph CL ["classic::* crates"]
         CL_M["classic::model"]
         CL_V["classic::validation"]
         CL_O["classic::ops"]
         CL_MG["classic::migration"]
       end
       subgraph AD ["adaptive::* crates"]
         AD_M["adaptive::model"]
         AD_V["adaptive::validation"]
         AD_O["adaptive::ops"]
         AD_MG["adaptive::migration"]
       end
     end

     subgraph GW ["ARXML Gateway"]
       ARTOP["Spring Boot + ARTOP\nARXML import/export"]
       GQL["GraphQL API\nSchema-versioned SDL"]
     end

     subgraph MCP_L ["Qorix Agent — MCP Layer"]
       ROUTER["Intent Router\nDomain detection + routing"]
       REG["Tool Registry\nClassic · Adaptive · BPCT tools"]
       LLM_C["LLM Client\nOpenAI / self-hosted"]
     end

     subgraph EXT ["External"]
       GIT["Git Repository\nYAML source of truth"]
       LEGACY["Legacy AUTOSAR Tools\nTresos · DaVinci"]
       BUILD["Downstream Build\nCompilers · RTE generators"]
     end

     YAML_ED --> WASM_BR
     DESIGNERS --> CMD_BUS --> WASM_BR
     WASM_BR --> WASM
     WASM_BR --> DS_CLIENT --> SVC
     AI_PANEL --> ROUTER --> REG --> SVC
     ROUTER --> LLM_C
     SVC --> C_GQL --> GQL --> ARTOP
     ARTOP --> LEGACY
     ARTOP --> BUILD
     CLI --> SVC
     WASM_BR --> DIAG_PNL
     SVC --> GIT
     WIZARD --> CMD_BUS

3.2 Runtime view — three primary data flow paths
-------------------------------------------------

Three data flow paths cover the complete operational scope of the
platform. All three share the same Rust domain crate tree.

**Path 1 — Interactive designer workflow**

.. mermaid::

   sequenceDiagram
     participant Eng as Engineer
     participant Des as Visual Designer / YAML Editor
     participant Bus as Command Bus
     participant WB as WASM Bridge
     participant WASM as qorix_core_wasm
     participant DS as Rust Domain Service
     participant Git as YAML File / Git

     Eng->>Des: Edit element on canvas or YAML directly
     Des->>Bus: execute("classic.addSwc", payload)
     Bus->>WB: planOps(payload)
     WB->>WASM: validateYaml(content, schema_id)
     WASM-->>WB: DiagnosticList (< 500 ms)
     WB->>DS: semantic validation (HTTP/gRPC)
     DS-->>WB: DiagnosticList (cross-file)
     WB-->>Des: Merged diagnostics → Diagnostics Panel
     Des->>Git: YAML updated, committed to source of truth

**Path 2 — AI-assisted engineering workflow**

.. mermaid::

   sequenceDiagram
     participant Eng as Engineer
     participant Panel as AI Chat Panel
     participant Agent as Qorix Agent (Intent Router)
     participant LLM as LLM Backend
     participant DS as Rust Domain Service
     participant WB as WASM Bridge
     participant Git as YAML File / Git
     participant Log as Audit Log

     Eng->>Panel: "Fix all unmapped runnables"
     Panel->>Agent: prompt + active designer context (C6)
     Agent->>Agent: Detect domain = Classic
     Agent->>DS: suggest_runnable_mappings(project_ctx)
     DS-->>Agent: OperationPlan (typed ops on rte-mapping.yaml)
     Agent->>LLM: Explain plan in natural language
     LLM-->>Agent: Explanation text
     Agent-->>Panel: OperationPlan + explanation
     Panel-->>Eng: Review: Accept / Reject
     Eng->>Panel: Accept
     Panel->>WB: Apply ops to in-memory model
     WB->>Git: Write rte-mapping.yaml (atomic save)
     WB->>WB: validateYaml() — post-acceptance re-validation
     WB-->>Panel: Updated diagnostic list
     Panel->>Log: Audit record: event · timestamp · user · outcome

**Path 3 — CI / headless generation pipeline**

.. mermaid::

   sequenceDiagram
     participant CI as CI/CD Pipeline
     participant CLI as qorix_cli
     participant DS as Rust Domain Service
     participant GW as ARXML Gateway (ARTOP)
     participant Out as Generated Output

     CI->>CLI: qorix_cli validate <project-path>
     CLI->>DS: Load all YAML files → unified domain model
     DS->>DS: Run classic::validation + adaptive::validation
     DS-->>CLI: DiagnosticList (JSON, exit 0 or 1)
     CLI->>CI: Structured JSON diagnostics (pass/fail)
     CI->>CLI: qorix_cli generate <project-path> --output <dir>
     CLI->>DS: Validated model available
     CLI->>GW: GraphQL mutation (via core::gql_client)
     GW->>GW: Spring Boot + ARTOP serialise to ARXML
     GW-->>CLI: ARXML artefacts + provenance record
     CLI->>Out: Deterministic ARXML + provenance.json

3.3 Deployment view — build targets and runtime hosts
------------------------------------------------------

.. mermaid::

   graph LR
     subgraph SOURCE ["One Rust codebase"]
       CRATES["core::* + classic::* + adaptive::* + bootloader::* + performance::*\ncrate tree"]
     end

     subgraph TARGET1 ["Build target 1 — IDE (WASM)"]
       W["qorix_core_wasm\n.wasm binary"]
       VSC["VS Code Extension\n(Node.js / Electron)"]
       THEIA["Theia Desktop / Web\n(Node.js / Browser)"]
       W --> VSC
       W --> THEIA
     end

     subgraph TARGET2 ["Build target 2 — Service (HTTP/gRPC)"]
       SVC2["Rust Domain Service\nLinux · systemd / container"]
       GW2["ARXML Gateway\nSpring Boot · JVM · ARTOP"]
       SVC2 -->|"GraphQL (core::gql_client)"| GW2
     end

     subgraph TARGET3 ["Build target 3 — CLI (headless)"]
       CLI2["qorix_cli\nStatically linked binary"]
       CI2["CI/CD Runner\nGitHub Actions · Jenkins"]
       CLI2 --> CI2
     end

     CRATES -->|"wasm-pack"| W
     CRATES -->|"cargo build --release"| SVC2
     CRATES -->|"cargo build --release"| CLI2

3.4 AUTOSAR Classic SWC decomposition
---------------------------------------

Not applicable — Qorix Developer is a desktop/server engineering tool,
not an AUTOSAR SWC deployed on a target ECU. The platform does not
expose SWC-style ports or runnables. The IDE Layer, Rust Domain Service
and ARXML Gateway run on developer workstations and CI servers.


4. Component Specifications
============================

4.1 IDE Layer
--------------

**Responsibility:** Provides the complete user-facing engineering
surface — YAML editor, visual designers (C1–C6, A1–A6, BD1–BD6),
project creation wizard, diagnostics panel, AI Chat Panel and Command
Bus. Hosts the WASM Bridge providing in-process fast validation without
network dependency.

**Realises requirements:**
QDX-SWE-006, QDX-SWE-007, QDX-SWE-008, QDX-SWE-009 through
QDX-SWE-028, QDX-SWE-029, QDX-SWE-030, QDX-SWE-031, QDX-SWE-036,
QDX-SWE-037, QDX-SWE-047 through QDX-SWE-050, QDX-SWE-052,
QDX-SWE-054 through QDX-SWE-060, QDX-SWE-063 through QDX-SWE-076,
QDX-SWE-077 through QDX-SWE-080, QDX-SWE-091 through QDX-SWE-101.

**Provided interfaces:**

.. list-table::
   :widths: 28 20 52
   :header-rows: 1

   * - Interface name
     - Type / Protocol
     - Description
   * - Designer canvas
     - VS Code / Theia UI extension
     - Domain-specific visual editing surface for C1–C6, A1–A6 and
       BD1–BD6 designer tabs
   * - YAML editor
     - LSP + JSON Schema
     - Text-based authoring with schema completion, hover docs,
       go-to-definition and rename-symbol
   * - Diagnostics Panel
     - IDE panel API
     - Merged display of WASM (fast) and Domain Service (deep)
       diagnostics with severity, file and YAML path
   * - AI Chat Panel
     - MCP client (HTTP)
     - Natural language prompt submission and OperationPlan review /
       accept / reject surface
   * - Project Creation Wizard
     - IDE webview
     - Multi-step project creation flow for all supported stacks

**Required interfaces:**

.. list-table::
   :widths: 28 22 50
   :header-rows: 1

   * - Interface name
     - Provider
     - Description
   * - ``validateYaml()`` / ``planOps()``
     - qorix_core_wasm
     - In-process WASM validation and operation planning; no network
   * - Domain Service HTTP/gRPC
     - Rust Domain Service
     - Heavy semantic validation, cross-file resolution, search,
       workspace consistency check
   * - MCP protocol (HTTP)
     - Qorix Agent
     - OperationPlan proposals and natural language explanations

**State machine:**

.. mermaid::

   stateDiagram-v2
     [*] --> Unloaded
     Unloaded --> Loading : Workspace opened
     Loading --> Ready : YAML files parsed, WASM initialised
     Ready --> Editing : User interaction
     Editing --> Validating : Save / Command Bus dispatch
     Validating --> Editing : Diagnostics returned
     Editing --> Generating : Generate action
     Generating --> Ready : Artefacts written
     Ready --> Unloaded : Workspace closed


4.2 Rust Domain Platform
-------------------------

**Responsibility:** Owns the canonical semantic model for Classic
AUTOSAR, Adaptive AUTOSAR, BPCT and LW-BSW configurations. Performs
all cross-file semantic validation, domain operations, model migrations
and generation orchestration. Compiles from one codebase into three
build targets — HTTP/gRPC service, WASM module and CLI binary — with
identical business logic across all three.

**Realises requirements:**
QDX-SWE-001 through QDX-SWE-005, QDX-SWE-008, QDX-SWE-031 through
QDX-SWE-035, QDX-SWE-038, QDX-SWE-039, QDX-SWE-040, QDX-SWE-041,
QDX-SWE-043, QDX-SWE-044, QDX-SWE-045, QDX-SWE-046, QDX-SWE-054
through QDX-SWE-057, QDX-SWE-060, QDX-SWE-062, QDX-SWE-066,
QDX-SWE-069, QDX-SWE-070, QDX-SWE-072, QDX-SWE-073, QDX-SWE-074,
QDX-SWE-075, QDX-SWE-082 through QDX-SWE-090.

**Sub-components — core::* crates (shared across all domains):**

.. list-table::
   :widths: 22 78
   :header-rows: 1

   * - Crate
     - Responsibility
   * - ``core::model``
     - Common primitives: qualified names, base datatypes, error types,
       diagnostic severity and code definitions
   * - ``core::yaml``
     - Serde-based YAML ↔ Rust struct mapping. Supports partial and
       loose structures for in-progress editing. Serialises model back
       to deterministic YAML with stable key ordering
   * - ``core::validation``
     - Generic rule engine. Executes registered validation rules and
       produces ``Diagnostic { severity, code, message, file, yaml_path }``
       per finding
   * - ``core::ops``
     - Operation model: low-level add/update/delete at YAML paths;
       high-level domain operations in generic form used by both the
       WASM Bridge and the Agent OperationPlan
   * - ``core::gql_client``
     - Generated GraphQL client compiled from the ARXML Gateway SDL.
       The only bridge between Rust domain and EMF/ARTOP. No other
       Rust crate may call the ARXML Gateway directly
   * - ``core::migration``
     - Shared migration utilities for ARXML → YAML semantic
       transformations used by Classic and Adaptive migration crates

**Sub-components — classic::* domain crates:**

.. list-table::
   :widths: 22 78
   :header-rows: 1

   * - Crate
     - Responsibility
   * - ``classic::model``
     - Strongly typed Rust structs for AUTOSAR Classic concepts: SWC,
       ComStack, OS tasks, NvM blocks, ECU, BSW module configuration
   * - ``classic::validation``
     - Semantic rules specific to Classic AUTOSAR: unmapped runnables,
       unresolved port-to-signal mappings, interface consistency,
       incompatible port types, duplicate identifiers
   * - ``classic::ops``
     - Domain operations: ``addSwc``, ``addComSignal``, ``addOsTask``,
       ``mapRunnable``, ``mapPortToSignal``
   * - ``classic::migration``
     - Migration paths from Tresos, DaVinci and other Classic ARXML
       tools. Reports lossy or ambiguous element conversions as
       WARNING diagnostics

**Sub-components — adaptive::* domain crates:**

.. list-table::
   :widths: 22 78
   :header-rows: 1

   * - Crate
     - Responsibility
   * - ``adaptive::model``
     - Strongly typed Rust structs for AUTOSAR Adaptive: Services,
       Applications, Machines, Processes, Deployments, Platform Services
   * - ``adaptive::validation``
     - Semantic rules: unbound consumer instances, disabled core
       references in deployments, scheduling conflicts, resource
       constraint violations, cross-YAML file invariants
   * - ``adaptive::ops``
     - Domain operations: ``addServiceInstance``, ``addMachine``,
       ``configureExecution``, ``deployApplication``
   * - ``adaptive::migration``
     - ARXML → YAML migration for Adaptive AUTOSAR projects with
       lossy-conversion reporting

**Provided interfaces:**

.. list-table::
   :widths: 28 20 52
   :header-rows: 1

   * - Interface name
     - Type / Protocol
     - Description
   * - Domain Service API
     - HTTP / gRPC
     - Semantic validation, cross-file resolution, search, workspace
       consistency check, workspace open, model operations
   * - ``validateYaml(content, schema_id)``
     - WASM export (JS callable)
     - Fast in-process schema validation. Returns DiagnosticList
       within 500 ms for medium-sized files
   * - ``qorix_cli validate``
     - CLI (process / stdout JSON)
     - Headless validation; exits non-zero on ERROR; structured
       newline-delimited JSON diagnostic output
   * - ``qorix_cli generate``
     - CLI (process / stdout JSON)
     - Headless generation; calls Domain Service then ARXML Gateway;
       writes artefacts and provenance.json to output directory
   * - MCP tool endpoints
     - MCP protocol (via Domain Service)
     - Named tool functions callable by the Qorix Agent:
       ``suggest_runnable_mappings``, ``fix_unmapped_signals``,
       ``suggest_service_bindings``, ``propose_deployment``,
       ``suggest_timing_parameters``, ``validate_security_config``

**Required interfaces:**

.. list-table::
   :widths: 28 22 50
   :header-rows: 1

   * - Interface name
     - Provider
     - Description
   * - GraphQL API (ARXML Gateway)
     - ARXML Gateway
     - ARXML model read and write operations via ``core::gql_client``

**State machine (Domain Service):**

.. mermaid::

   stateDiagram-v2
     [*] --> Starting
     Starting --> Idle : HTTP/gRPC server bound, crates initialised
     Idle --> Loading : Workspace open request received
     Loading --> Loaded : All YAML files parsed, model built
     Loaded --> Validating : Validation request (IDE or CLI)
     Validating --> Loaded : DiagnosticList returned
     Loaded --> Generating : Generate request
     Generating --> Loaded : ARXML Gateway call complete
     Loaded --> Idle : Workspace closed


4.3 ARXML Gateway
------------------

**Responsibility:** Provides the exclusive ARXML import and export
boundary for the entire platform. Wraps the AUTOSAR Tool Platform
(ARTOP) and exposes a versioned GraphQL API to the Rust domain layer.
The Rust domain crates have zero dependency on EMF, ARTOP or any JVM
library — the Gateway is the only path for ARXML I/O.

**Realises requirements:**
QDX-SWE-038, QDX-SWE-039, QDX-SWE-040, QDX-SWE-041, QDX-SWE-042,
QDX-SWE-043.

**Provided interfaces:**

.. list-table::
   :widths: 28 20 52
   :header-rows: 1

   * - Interface name
     - Type / Protocol
     - Description
   * - GraphQL API
     - HTTP / GraphQL
     - Versioned schema for AUTOSAR model queries and mutations.
       SDL published as a machine-readable file in the repository.
       ``core::gql_client`` is generated from this SDL
   * - ARXML import endpoint
     - GraphQL mutation
     - Accepts ARXML input, parses via ARTOP, returns Rust-compatible
       model representation. Reports lossy/ambiguous elements as
       structured warnings
   * - ARXML export endpoint
     - GraphQL mutation
     - Accepts domain model from Rust, serialises to ARXML via ARTOP.
       Deterministic: identical input + identical ARTOP version =
       identical ARXML output

**Required interfaces:**

.. list-table::
   :widths: 28 22 50
   :header-rows: 1

   * - Interface name
     - Provider
     - Description
   * - ARTOP metamodel API
     - ARTOP (Eclipse / JVM)
     - Canonical AUTOSAR metamodel and ARXML read/write.
       Internal to the Gateway — not exposed to Rust
   * - GraphQL client
     - ``core::gql_client`` (Rust Domain Platform)
     - The only caller of the Gateway's GraphQL API


4.4 Qorix Agent — MCP Layer
-----------------------------

**Responsibility:** Orchestrates AI-assisted engineering workflows.
Receives natural language prompts from the AI Chat Panel, detects the
active domain (Classic, Adaptive, BPCT or LW-BSW) from the designer
context, routes to the correct domain tool set, invokes the LLM
backend for explanation generation, and returns a typed OperationPlan
to the engineer for review. Never writes to a YAML file directly.

**Realises requirements:**
QDX-SWE-047, QDX-SWE-048, QDX-SWE-049, QDX-SWE-050, QDX-SWE-051,
QDX-SWE-052, QDX-SWE-053, QDX-SWE-077, QDX-SWE-078, QDX-SWE-079,
QDX-SWE-080, QDX-SWE-089.

**Sub-components:**

.. list-table::
   :widths: 22 78
   :header-rows: 1

   * - Component
     - Responsibility
   * - Intent Router
     - Identifies the active stack domain from the open designer tab
       identifier (C1–C6, A1–A6, BD1–BD6) and routes the user prompt
       to the correct domain tool set in the Tool Registry. Rejects
       cross-domain OperationPlans.
   * - Tool Registry
     - Catalogues all available MCP tools. Provides discovery for
       Shared, Classic, Adaptive, BPCT and LW-BSW tool sets.
       Supports dynamic registration at Agent startup for domain
       extension tools.
   * - Classic MCP Tools
     - ``suggest_runnable_mappings``, ``fix_unmapped_signals``,
       ``balance_core_load`` — callable via the Domain Service
   * - Adaptive MCP Tools
     - ``suggest_service_bindings``, ``propose_deployment``,
       ``fix_execution_graph`` — callable via the Domain Service
   * - BPCT MCP Tools
     - ``suggest_timing_parameters``, ``validate_security_config``,
       ``fix_cross_designer_violations`` — callable via the Domain
       Service
   * - LW-BSW Config Insight
     - Scheduling assessment, resource budget evaluation, race
       condition explanation, safety violation guidance — analytical
       read-only outputs composed from Domain Service query results

**Provided interfaces:**

.. list-table::
   :widths: 28 20 52
   :header-rows: 1

   * - Interface name
     - Type / Protocol
     - Description
   * - MCP agent endpoint
     - HTTP / MCP protocol
     - Receives prompt + context from AI Chat Panel. Returns
       OperationPlan + explanation. Enforces domain scoping.

**Required interfaces:**

.. list-table::
   :widths: 28 22 50
   :header-rows: 1

   * - Interface name
     - Provider
     - Description
   * - Domain Service MCP tools
     - Rust Domain Service
     - Named tool functions for each domain returning typed ops
   * - LLM backend
     - OpenAI / self-hosted
     - Natural language interpretation and explanation generation.
       Subject to ``FBL_WDG_DISABLE_DURING_ERASE``-equivalent data
       transmission control (QDX-SWE-051)

**Agent interaction constraint — no direct YAML writes:**

.. mermaid::

   flowchart TD
     PROMPT["Engineer prompt\nvia AI Chat Panel"] --> ROUTER["Intent Router\nDetect domain from context"]
     ROUTER --> TOOLCALL["Domain MCP tool call\nvia Rust Domain Service"]
     TOOLCALL --> OPS["OperationPlan\nTyped ops on specific YAML paths"]
     OPS --> LLM["LLM Backend\nGenerate explanation"]
     LLM --> PANEL["AI Chat Panel\nPresent plan + explanation"]
     PANEL --> DECISION{Engineer\nAccepts?}
     DECISION -->|"Accept"| APPLY["WASM Bridge applies ops\nAtomic YAML write"]
     DECISION -->|"Reject"| DISCARD["Plan discarded\nNo file modified"]
     APPLY --> REVALIDATE["WASM re-validates\nPost-acceptance check"]
     APPLY --> AUDIT["Audit log record\nevent · timestamp · user · outcome"]


5. Architectural Decisions (ADR)
=================================

Each significant architectural decision gets a permanent record.
ADRs are never deleted — superseded decisions are marked Superseded.

.. list-table::
   :widths: 13 34 13 40
   :header-rows: 1

   * - ADR ID
     - Decision
     - Status
     - Rationale and consequences
   * - QDX-ADR-001
     - YAML as the canonical model; ARXML used only for
       import/export
     - Accepted
     - YAML is human-readable, diff-friendly and Git-native.
       ARXML is a binary-schema exchange format not suited to
       version-controlled authoring. Consequence: a translation
       layer (ARXML Gateway) is required; lossy import elements
       must be reported and managed.
   * - QDX-ADR-002
     - Single Rust codebase compiled to three build targets
       (WASM, HTTP/gRPC service, CLI binary)
     - Accepted
     - Guarantees identical validation behaviour in IDE and CI.
       Eliminates the class of defect where a bug is present in
       CI but not in the IDE or vice versa. Consequence: the
       crate tree must compile to all three targets without
       conditional compilation that alters business logic
       (QDX-SWE-046).
   * - QDX-ADR-003
     - Rust domain crates have zero JVM / ARTOP / EMF dependency
     - Accepted
     - :cr_id: —
     - Enables WASM and CLI compilation without a JVM runtime.
       Decouples ARTOP version upgrades from Rust build.
       Consequence: ``core::gql_client`` is the only path to
       ARXML functionality; changes to the GraphQL schema require
       regenerating the client and rebuilding.
   * - QDX-ADR-004
     - The Qorix Agent never writes to a YAML file directly
     - Accepted
     - :cr_id: —
     - Preserves engineer accountability for all configuration
       changes in safety-relevant automotive contexts. AI
       suggestions are OperationPlans presented for review;
       the engineer is the final authority. Consequence: all
       Agent-originated changes require an extra interaction
       step (QDX-SWE-047, QDX-SWE-048).
   * - QDX-ADR-005
     - AI-Assist activated per domain by domain extension
       installation
     - Accepted
     - Allows Classic, Adaptive and BPCT AI capabilities to
       ship and be licenced independently. Prevents AI tools
       from one domain being invoked in another domain's
       context. Consequence: the Tool Registry must support
       dynamic registration at Agent startup (QDX-SWE-077,
       QDX-SWE-061).
   * - QDX-ADR-006
     - LW-BSW and Full Classic BSW share the C1–C6 designer
       canvas; project type flag at creation applies schema
       filter
     - Accepted
     - Avoids duplicating six designer implementations. ICC-2
       is a structural subset of ICC-3 at the concept level.
       Consequence: the schema loading mechanism must be
       per-project-type; the LW-BSW JSON Schema is a strict
       subset of the Classic schema.
   * - QDX-ADR-007
     - ARXML Gateway exposes a versioned GraphQL SDL; breaking
       changes increment major schema version
     - Accepted
     - Enables ``core::gql_client`` to be generated from the SDL
       and ensures the Rust domain always knows the API contract.
       Consequence: SDL file must be published in the repository
       and client regeneration must be part of the build
       pipeline on schema change (QDX-SWE-043).
   * - QDX-ADR-008
     - Atomic YAML save (write-to-temp then rename)
     - Accepted
     - :cr_id: —
     - Prevents partial-write corruption of YAML source files if
       the process is interrupted during a save operation.
       Consequence: all file persistence in the platform must
       use this pattern; direct file writes are prohibited
       (QDX-SWE-005).


6. Cross-Cutting Concerns
==========================

6.1 Error handling strategy
-----------------------------

All components use a unified diagnostic model. The Rust domain crates
produce ``Diagnostic { severity, code, message, file_path, yaml_path }``
structs. The IDE Layer merges diagnostics from the WASM Bridge (fast,
in-process) and the Domain Service (deep, cross-file) and presents them
in the Diagnostics Panel. Generation is blocked on unresolved ERROR
diagnostics.

.. mermaid::

   flowchart TD
     DETECT["Issue detected\nin validation rule or op"] --> CLASSIFY{Severity?}
     CLASSIFY -->|"INFO"| INFO["Advisory diagnostic\nReturned in DiagnosticList"]
     CLASSIFY -->|"WARNING"| WARN["Warning diagnostic\nGeneration not blocked"]
     CLASSIFY -->|"ERROR"| ERR["Error diagnostic\nGeneration BLOCKED"]
     ERR --> PANEL["Diagnostics Panel\nseverity · message · file · yaml_path"]
     WARN --> PANEL
     INFO --> PANEL
     PANEL --> ENG["Engineer resolves\nand saves"]
     ENG --> RECHECK["Re-validation triggered\nWASM + Domain Service"]
     RECHECK -->|"No ERRORs"| RELEASE["Generation permitted"]
     RECHECK -->|"ERRORs remain"| ERR

6.2 Concurrency and task model
--------------------------------

The Rust Domain Service is a multi-threaded HTTP/gRPC server. The WASM
module executes single-threaded within the IDE host JavaScript runtime.
The CLI binary is single-threaded and processes one project at a time.

.. list-table::
   :widths: 28 18 18 36
   :header-rows: 1

   * - Component / operation
     - Execution context
     - Trigger
     - Shared resource and protection
   * - WASM ``validateYaml()``
     - JS main thread (IDE)
     - User edit / save event
     - In-process; no shared state with Domain Service
   * - Domain Service validation
     - Rust async thread pool
     - HTTP/gRPC request from IDE or CLI
     - Project model: per-request read lock; write lock on
       mutation operations
   * - ARXML Gateway GraphQL
     - Spring Boot thread pool (JVM)
     - GraphQL mutation from ``core::gql_client``
     - ARTOP model: JVM-side locking within Spring Boot
   * - Agent MCP tool call
     - Agent process (async)
     - Prompt submitted from AI Chat Panel
     - Domain Service request: stateless tool calls
   * - CLI ``generate`` command
     - Single process, sequential
     - CI pipeline invocation
     - File system writes: atomic save pattern (QDX-ADR-008)

6.3 Memory model
-----------------

The Rust domain targets developer workstations and CI runners — not
embedded ECU targets. The memory model is therefore standard desktop
process allocation. The key constraint is reproducibility and
correctness, not memory budget.

.. list-table::
   :widths: 28 20 52
   :header-rows: 1

   * - Memory region / component
     - Allocation strategy
     - Notes
   * - Rust Domain Service heap
     - Dynamic (std allocator)
     - Standard Rust heap allocation for domain model data
       structures. Model size is bounded by project YAML file
       sizes.
   * - WASM module linear memory
     - WASM linear memory (static upper bound at compile time)
     - Sized for single-file validation. Cross-file operations
       delegate to the Domain Service.
   * - CLI process heap
     - Dynamic (std allocator)
     - Same as Domain Service. Process exits after completion;
       no long-lived allocations.
   * - Spring Boot / ARTOP JVM heap
     - JVM managed (-Xmx configured at deployment)
     - ARTOP model size scales with ARXML file complexity.
       JVM heap size must be configured per deployment.
   * - YAML source files (Git)
     - File system — text files
     - All project configuration persisted as UTF-8 YAML.
       No binary blobs in the project source tree.

6.4 Security and AI data transmission
---------------------------------------

The Qorix Agent includes a deployment-level configuration control
governing whether project YAML content may be included in prompts sent
to the LLM backend (QDX-SWE-051). When disabled, only structural
metadata (element type names, counts, diagnostic codes) is transmitted.
This control is enforced in the Intent Router before any LLM call is
made — it is not enforced at the LLM client level.

Access control for privileged operations (ARXML generation, workspace
publish, extension installation) is enforced when authentication is
configured for the deployment (QDX-SWE-053). The audit log records all
critical user actions including generation, publication, AI
OperationPlan acceptance and import events (QDX-SWE-052).


7. Architecture Traceability Matrix
=====================================

.. note::
   Maps each architectural element to the SYS.2 system requirements and
   SWE.1 software requirements it realises, the SWE.5 integration tests
   that verify subsystem interfaces, and the SYS.4 system integration
   tests that verify end-to-end system boundaries
   (QDX-SYS4-DOC-001, in progress).

.. list-table::
   :widths: 20 14 28 14 14 10
   :header-rows: 1

   * - Architectural element
     - SYS.2 req
     - Realises SW requirements (SWE.1)
     - SWE.5 integ. test
     - SYS.4 sys. integ. test
     - Status
   * - IDE Layer — YAML Editor + LSP
     - QDX-SYS-003
     - QDX-SWE-006, QDX-SWE-007, QDX-SWE-008
     - QDX-IT-001
     - —
     - Draft
   * - IDE Layer — Visual Designers (C1–C6)
     - QDX-SYS-004
     - QDX-SWE-009 through QDX-SWE-016
     - —
     - —
     - Draft
   * - IDE Layer — Visual Designers (A1–A6)
     - QDX-SYS-004
     - QDX-SWE-017 through QDX-SWE-028
     - QDX-IT-011, QDX-IT-012
     - —
     - Draft
   * - IDE Layer — Visual Designers (BD1–BD6)
     - QDX-SYS-004
     - QDX-SWE-063 through QDX-SWE-076
     - QDX-IT-013, QDX-IT-014
     - —
     - Draft
   * - IDE Layer — Command Bus
     - QDX-SYS-013
     - QDX-SWE-008, QDX-SWE-029, QDX-SWE-030
     - QDX-IT-002
     - —
     - Draft
   * - IDE Layer — WASM Bridge
     - QDX-SYS-006
     - QDX-SWE-031, QDX-SWE-049, QDX-SWE-055, QDX-SWE-060
     - QDX-IT-003
     - —
     - Draft
   * - IDE Layer — Domain Service Client
     - QDX-SYS-007
     - QDX-SWE-032, QDX-SWE-033, QDX-SWE-035, QDX-SWE-044
     - QDX-IT-004, QDX-IT-005
     - —
     - Draft
   * - IDE Layer — Diagnostics Panel
     - QDX-SYS-014
     - QDX-SWE-036, QDX-SWE-037
     - —
     - —
     - Draft
   * - IDE Layer — AI Chat Panel
     - QDX-SWE-047, QDX-SWE-048, QDX-SWE-077, QDX-SWE-078,
       QDX-SWE-079
     - QDX-IT-010, QDX-IT-015
     - Draft
   * - IDE Layer — Project Creation Wizard
     - QDX-SYS-002
     - QDX-SWE-091 through QDX-SWE-101
     - QDX-IT-019, QDX-IT-021
     - —
     - Draft
   * - Rust Domain Platform — core::model
     - QDX-SYS-009
     - QDX-SWE-001, QDX-SWE-003, QDX-SWE-004
     - —
     - —
     - Draft
   * - Rust Domain Platform — core::yaml
     - QDX-SYS-019
     - QDX-SWE-004, QDX-SWE-005, QDX-SWE-008
     - —
     - —
     - Draft
   * - Rust Domain Platform — core::validation
     - QDX-SWE-031, QDX-SWE-032, QDX-SWE-033, QDX-SWE-034,
       QDX-SWE-037
     - QDX-IT-003, QDX-IT-004
     - Draft
   * - Rust Domain Platform — core::ops
     - QDX-SYS-013
     - QDX-SWE-008, QDX-SWE-013
     - —
     - —
     - Draft
   * - Rust Domain Platform — core::gql_client
     - QDX-SYS-012
     - QDX-SWE-039, QDX-SWE-043
     - QDX-IT-007, QDX-IT-008
     - —
     - Draft
   * - Rust Domain Platform — core::migration
     - QDX-SYS-011
     - QDX-SWE-040, QDX-SWE-062
     - QDX-IT-007
     - —
     - Draft
   * - Rust Domain Platform — classic::* crates
     - QDX-SYS-004
     - QDX-SWE-009 through QDX-SWE-016, QDX-SWE-038
     - QDX-IT-006
     - —
     - Draft
   * - Rust Domain Platform — adaptive::* crates
     - QDX-SYS-004
     - QDX-SWE-017 through QDX-SWE-028, QDX-SWE-038
     - QDX-IT-006, QDX-IT-011, QDX-IT-012
     - —
     - Draft
   * - Rust Domain Platform — qorix_core_wasm
     - QDX-SYS-006
     - QDX-SWE-031, QDX-SWE-046, QDX-SWE-055, QDX-SWE-060
     - QDX-IT-003
     - —
     - Draft
   * - Rust Domain Platform — qorix_cli
     - QDX-SWE-038, QDX-SWE-041, QDX-SWE-045, QDX-SWE-046,
       QDX-SWE-057
     - QDX-IT-009
     - Draft
   * - Rust Domain Platform — Domain Service (HTTP/gRPC)
     - QDX-SWE-032, QDX-SWE-035, QDX-SWE-044, QDX-SWE-052,
       QDX-SWE-053, QDX-SWE-054, QDX-SWE-056
     - QDX-IT-004, QDX-IT-005
     - Draft
   * - ARXML Gateway — Spring Boot + ARTOP
     - QDX-SWE-038, QDX-SWE-039, QDX-SWE-040, QDX-SWE-041,
       QDX-SWE-042, QDX-SWE-057
     - QDX-IT-006, QDX-IT-007
     - Draft
   * - ARXML Gateway — GraphQL API / SDL
     - QDX-SYS-012
     - QDX-SWE-043
     - QDX-IT-008
     - —
     - Draft
   * - Qorix Agent — Intent Router
     - QDX-SYS-016
     - QDX-SWE-050, QDX-SWE-051, QDX-SWE-079
     - QDX-IT-010
     - —
     - Draft
   * - Qorix Agent — Tool Registry
     - QDX-SYS-016
     - QDX-SWE-050, QDX-SWE-061, QDX-SWE-077, QDX-SWE-080
     - —
     - —
     - Draft
   * - Qorix Agent — Classic / Adaptive / BPCT MCP Tools
     - QDX-SYS-016
     - QDX-SWE-047, QDX-SWE-078, QDX-SWE-080, QDX-SWE-089
     - QDX-IT-010, QDX-IT-015, QDX-IT-018
     - —
     - Draft
   * - LW-BSW subsystem (schema filter + generators)
     - QDX-SYS-002
     - QDX-SWE-081 through QDX-SWE-090
     - QDX-IT-016, QDX-IT-017, QDX-IT-018
     - —
     - Draft
   * - BPCT validation rule engine
     - QDX-SWE-066, QDX-SWE-069, QDX-SWE-070, QDX-SWE-072,
       QDX-SWE-073, QDX-SWE-074
     - QDX-IT-013
     - Draft


8. Open Issues and TBDs
========================

.. list-table::
   :widths: 15 50 20 15
   :header-rows: 1

   * - Issue ID
     - Description
     - Owner
     - Target date
   * - TBD-SWA-001
     - Define the exact HTTP/gRPC API surface of the Rust Domain
       Service — endpoint names, request/response schemas, error
       codes. This is the primary interface contract for SWE.5
       integration testing.
     - Architecture Team
     - 2026-04-30
   * - TBD-SWA-002
     - Publish the ARXML Gateway GraphQL SDL to the repository and
       establish the schema versioning policy and regeneration
       trigger for ``core::gql_client``.
     - ARXML Gateway Lead
     - 2026-04-30
   * - TBD-SWA-003
     - Define the BPCT and LW-BSW crate structure (e.g.
       ``bpct::validation``, ``lwbsw::validation``) within the
       Rust Domain Platform crate tree. Confirm whether BPCT and
       LW-BSW follow the same Classic domain crate pattern.
     - Rust Domain Platform Lead
     - 2026-05-15
   * - TBD-SWA-004
     - Specify the deployment topology for the Rust Domain Service
       and ARXML Gateway in desktop (local) vs. server-hosted
       deployment modes. Define the JVM heap sizing guidelines for
       ARTOP in each mode.
     - Platform Engineering
     - 2026-05-15
   * - TBD-SWA-005
     - Define the Eclipse S-Core crate structure (``score::model``,
       ``score::validation``, ``score::ops``) and its integration
       point with the existing Classic/Adaptive domain architecture.
     - S-Core Integration Lead
     - 2026-06-01
   * - TBD-SWA-006
     - Confirm approver names and approval date for formal release
       baseline of this document. Depends on TBD-SYS-005.
     - Program Management
     - 2026-04-15


.. _swa_changelog:

9. Changelog
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
     - Initial SWE.2 draft derived from QDX-SWE-DOC-001 (SWE.1)
       and Qorix Developer C4 Architecture (L1 System Context,
       L2 Containers, L3 Components, Data Flow). Covers all four
       subsystems (IDE Layer, Rust Domain Platform, ARXML Gateway,
       Qorix Agent), three build targets, three data flow paths,
       eight ADRs, full architecture traceability matrix mapping
       all 101 SWE.1 requirements to architectural elements and
       SWE.5 integration tests.


----

*This document is version-controlled in Git at*
``docs/30-swe.2/platform/sw_architecture.rst``.
*Authoritative version is HEAD of* ``main``.
*Architectural decisions (ADR) require Chief Architect approval.
All changes require a PR with minimum two approvals from CODEOWNERS.*

10. Architecture Specifications (SWE.2)
=======================================

.. spec:: Multi-stack workspace initialisation architecture
   :id: QDX-SWA-SP-001
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-001
   :sys_req: QDX-SYS-001

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-001 (Multi-stack workspace initialisation).

.. spec:: Per-stack project scaffolding architecture
   :id: QDX-SWA-SP-002
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-002
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-002 (Per-stack project scaffolding).

.. spec:: Source/output directory separation architecture
   :id: QDX-SWA-SP-003
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-003
   :sys_req: QDX-SYS-044

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-003 (Source/output directory separation).

.. spec:: Version-control-friendly YAML persistence architecture
   :id: QDX-SWA-SP-004
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-004
   :sys_req: QDX-SYS-019

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-004 (Version-control-friendly YAML persistence).

.. spec:: Atomic save with integrity protection architecture
   :id: QDX-SWA-SP-005
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-005
   :sys_req: QDX-SYS-033

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-005 (Atomic save with integrity protection).

.. spec:: YAML editor with schema-based completion architecture
   :id: QDX-SWA-SP-006
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-006
   :sys_req: QDX-SYS-003

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-006 (YAML editor with schema-based completion).

.. spec:: Language server protocol integration architecture
   :id: QDX-SWA-SP-007
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-007
   :sys_req: QDX-SYS-029

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-007 (Language server protocol integration).

.. spec:: Localised atomic model mutations architecture
   :id: QDX-SWA-SP-008
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-008
   :sys_req: QDX-SYS-013

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-008 (Localised atomic model mutations).

.. spec:: C1 — SWC and interface designer architecture
   :id: QDX-SWA-SP-009
   :status: Draft
   :domain: classic
   :cr_id: —
   :implements: QDX-SWE-009
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-009 (C1 — SWC and interface designer).

.. spec:: C1 — SWC runnable definition architecture
   :id: QDX-SWA-SP-010
   :status: Draft
   :domain: classic
   :cr_id: —
   :implements: QDX-SWE-010
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-010 (C1 — SWC runnable definition).

.. spec:: C2 — Signals and ComStack designer architecture
   :id: QDX-SWA-SP-011
   :status: Draft
   :domain: classic
   :cr_id: —
   :implements: QDX-SWE-011
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-011 (C2 — Signals and ComStack designer).

.. spec:: C3 — ECU and BSW designer architecture
   :id: QDX-SWA-SP-012
   :status: Draft
   :domain: classic
   :cr_id: —
   :implements: QDX-SWE-012
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-012 (C3 — ECU and BSW designer).

.. spec:: C4 — OS and scheduling designer architecture
   :id: QDX-SWA-SP-013
   :status: Draft
   :domain: classic
   :cr_id: —
   :implements: QDX-SWE-013
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-013 (C4 — OS and scheduling designer).

.. spec:: C5 — Memory and NvM designer architecture
   :id: QDX-SWA-SP-014
   :status: Draft
   :domain: classic
   :cr_id: —
   :implements: QDX-SWE-014
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-014 (C5 — Memory and NvM designer).

.. spec:: C6 — RTE and mapping designer architecture
   :id: QDX-SWA-SP-015
   :status: Draft
   :domain: classic
   :cr_id: —
   :implements: QDX-SWE-015
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-015 (C6 — RTE and mapping designer).

.. spec:: Unmapped element detection in C6 architecture
   :id: QDX-SWA-SP-016
   :status: Draft
   :domain: classic
   :cr_id: —
   :implements: QDX-SWE-016
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-016 (Unmapped element detection in C6).

.. spec:: A1 — Application and service designer architecture
   :id: QDX-SWA-SP-017
   :status: Draft
   :domain: adaptive
   :cr_id: —
   :implements: QDX-SWE-017
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-017 (A1 — Application and service designer).

.. spec:: A1 — Service cross-reference tracking architecture
   :id: QDX-SWA-SP-018
   :status: Draft
   :domain: adaptive
   :cr_id: —
   :implements: QDX-SWE-018
   :sys_req: QDX-SYS-008

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-018 (A1 — Service cross-reference tracking).

.. spec:: A2 — Communication and service instance designer architecture
   :id: QDX-SWA-SP-019
   :status: Draft
   :domain: adaptive
   :cr_id: —
   :implements: QDX-SWE-019
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-019 (A2 — Communication and service instance designer).

.. spec:: A2 — Service binding completeness validation architecture
   :id: QDX-SWA-SP-020
   :status: Draft
   :domain: adaptive
   :cr_id: —
   :implements: QDX-SWE-020
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-020 (A2 — Service binding completeness validation).

.. spec:: A3 — Machine design designer architecture
   :id: QDX-SWA-SP-021
   :status: Draft
   :domain: adaptive
   :cr_id: —
   :implements: QDX-SWE-021
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-021 (A3 — Machine design designer).

.. spec:: A3 — Disabled core reference detection architecture
   :id: QDX-SWA-SP-022
   :status: Draft
   :domain: adaptive
   :cr_id: —
   :implements: QDX-SWE-022
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-022 (A3 — Disabled core reference detection).

.. spec:: A4 — Platform services designer architecture
   :id: QDX-SWA-SP-023
   :status: Draft
   :domain: adaptive
   :cr_id: —
   :implements: QDX-SWE-023
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-023 (A4 — Platform services designer).

.. spec:: A5 — Execution management designer architecture
   :id: QDX-SWA-SP-024
   :status: Draft
   :domain: adaptive
   :cr_id: —
   :implements: QDX-SWE-024
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-024 (A5 — Execution management designer).

.. spec:: A5 — Scheduling conflict detection architecture
   :id: QDX-SWA-SP-025
   :status: Draft
   :domain: adaptive
   :cr_id: —
   :implements: QDX-SWE-025
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-025 (A5 — Scheduling conflict detection).

.. spec:: A6 — Deployment designer architecture
   :id: QDX-SWA-SP-026
   :status: Draft
   :domain: adaptive
   :cr_id: —
   :implements: QDX-SWE-026
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-026 (A6 — Deployment designer).

.. spec:: A6 — Resource constraint validation architecture
   :id: QDX-SWA-SP-027
   :status: Draft
   :domain: adaptive
   :cr_id: —
   :implements: QDX-SWE-027
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-027 (A6 — Resource constraint validation).

.. spec:: Adaptive cross-designer consistency check architecture
   :id: QDX-SWA-SP-028
   :status: Draft
   :domain: adaptive
   :cr_id: —
   :implements: QDX-SWE-028
   :sys_req: QDX-SYS-020

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-028 (Adaptive cross-designer consistency check).

.. spec:: Designer-to-YAML synchronisation architecture
   :id: QDX-SWA-SP-029
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-029
   :sys_req: QDX-SYS-005

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-029 (Designer-to-YAML synchronisation).

.. spec:: YAML-to-designer synchronisation architecture
   :id: QDX-SWA-SP-030
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-030
   :sys_req: QDX-SYS-005

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-030 (YAML-to-designer synchronisation).

.. spec:: In-IDE WASM fast validation architecture
   :id: QDX-SWA-SP-031
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-031
   :sys_req: QDX-SYS-006

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-031 (In-IDE WASM fast validation).

.. spec:: Deep semantic validation via domain service architecture
   :id: QDX-SWA-SP-032
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-032
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-032 (Deep semantic validation via domain service).

.. spec:: Cross-file reference resolution architecture
   :id: QDX-SWA-SP-033
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-033
   :sys_req: QDX-SYS-008

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-033 (Cross-file reference resolution).

.. spec:: Validation-gated publication architecture
   :id: QDX-SWA-SP-034
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-034
   :sys_req: QDX-SYS-036

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-034 (Validation-gated publication).

.. spec:: Workspace-level consistency check architecture
   :id: QDX-SWA-SP-035
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-035
   :sys_req: QDX-SYS-020

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-035 (Workspace-level consistency check).

.. spec:: Diagnostics panel presentation architecture
   :id: QDX-SWA-SP-036
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-036
   :sys_req: QDX-SYS-014

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-036 (Diagnostics panel presentation).

.. spec:: Usable diagnostic message quality architecture
   :id: QDX-SWA-SP-037
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-037
   :sys_req: QDX-SYS-042

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-037 (Usable diagnostic message quality).

.. spec:: Deterministic ARXML generation architecture
   :id: QDX-SWA-SP-038
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-038
   :sys_req: QDX-SYS-009

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-038 (Deterministic ARXML generation).

.. spec:: ARXML export via ARTOP GraphQL gateway architecture
   :id: QDX-SWA-SP-039
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-039
   :sys_req: QDX-SYS-010

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-039 (ARXML export via ARTOP GraphQL gateway).

.. spec:: ARXML import and lossy-conversion reporting architecture
   :id: QDX-SWA-SP-040
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-040
   :sys_req: QDX-SYS-011

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-040 (ARXML import and lossy-conversion reporting).

.. spec:: Generation provenance recording architecture
   :id: QDX-SWA-SP-041
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-041
   :sys_req: QDX-SYS-015

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-041 (Generation provenance recording).

.. spec:: External artefact compatibility status reporting architecture
   :id: QDX-SWA-SP-042
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-042
   :sys_req: QDX-SYS-030

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-042 (External artefact compatibility status reporting).

.. spec:: GraphQL API contract for model access architecture
   :id: QDX-SWA-SP-043
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-043
   :sys_req: QDX-SYS-012

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-043 (GraphQL API contract for model access).

.. spec:: Search and navigation API architecture
   :id: QDX-SWA-SP-044
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-044
   :sys_req: QDX-SYS-018

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-044 (Search and navigation API).

.. spec:: Headless CLI for CI validation and generation architecture
   :id: QDX-SWA-SP-045
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-045
   :sys_req: QDX-SYS-031

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-045 (Headless CLI for CI validation and generation).

.. spec:: Same Rust core for all build targets architecture
   :id: QDX-SWA-SP-046
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-046
   :sys_req: QDX-SYS-031

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-046 (Same Rust core for all build targets).

.. spec:: AI-generated OperationPlan — no direct YAML edit architecture
   :id: QDX-SWA-SP-047
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-047
   :sys_req: QDX-SYS-016

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-047 (AI-generated OperationPlan — no direct YAML edit).

.. spec:: User acceptance gate for AI suggestions architecture
   :id: QDX-SWA-SP-048
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-048
   :sys_req: QDX-SYS-017

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-048 (User acceptance gate for AI suggestions).

.. spec:: Post-acceptance WASM re-validation architecture
   :id: QDX-SWA-SP-049
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-049
   :sys_req: QDX-SYS-006

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-049 (Post-acceptance WASM re-validation).

.. spec:: Intent Router — Classic vs Adaptive dispatch architecture
   :id: QDX-SWA-SP-050
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-050
   :sys_req: QDX-SYS-016

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-050 (Intent Router — Classic vs Adaptive dispatch).

.. spec:: Configurable AI data transmission control architecture
   :id: QDX-SWA-SP-051
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-051
   :sys_req: QDX-SYS-037

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-051 (Configurable AI data transmission control).

.. spec:: Audit log for critical user actions architecture
   :id: QDX-SWA-SP-052
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-052
   :sys_req: QDX-SYS-035

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-052 (Audit log for critical user actions).

.. spec:: Access control for privileged operations architecture
   :id: QDX-SWA-SP-053
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-053
   :sys_req: QDX-SYS-034

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-053 (Access control for privileged operations).

.. spec:: Workspace open time architecture
   :id: QDX-SWA-SP-054
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-054
   :sys_req: QDX-SYS-022

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-054 (Workspace open time).

.. spec:: WASM validation latency architecture
   :id: QDX-SWA-SP-055
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-055
   :sys_req: QDX-SYS-023

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-055 (WASM validation latency).

.. spec:: Search response time architecture
   :id: QDX-SWA-SP-056
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-056
   :sys_req: QDX-SYS-024

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-056 (Search response time).

.. spec:: ARXML generation completion time architecture
   :id: QDX-SWA-SP-057
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-057
   :sys_req: QDX-SYS-025

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-057 (ARXML generation completion time).

.. spec:: Non-blocking UI for long-running operations architecture
   :id: QDX-SWA-SP-058
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-058
   :sys_req: QDX-SYS-026

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-058 (Non-blocking UI for long-running operations).

.. spec:: Dual IDE host support — VS Code and Theia architecture
   :id: QDX-SWA-SP-059
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-059
   :sys_req: QDX-SYS-027

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-059 (Dual IDE host support — VS Code and Theia).

.. spec:: Offline local authoring and validation architecture
   :id: QDX-SWA-SP-060
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-060
   :sys_req: QDX-SYS-043

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-060 (Offline local authoring and validation).

.. spec:: Extension mechanism without core modification architecture
   :id: QDX-SWA-SP-061
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-061
   :sys_req: QDX-SYS-041

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-061 (Extension mechanism without core modification).

.. spec:: Backward-compatible project migration architecture
   :id: QDX-SWA-SP-062
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-062
   :sys_req: QDX-SYS-040

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-062 (Backward-compatible project migration).

.. spec:: BPCT project structure and MCU selection (BD1) architecture
   :id: QDX-SWA-SP-063
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-063
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-063 (BPCT project structure and MCU selection (BD1)).

.. spec:: BPCT communication channel configuration (BD2) architecture
   :id: QDX-SWA-SP-064
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-064
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-064 (BPCT communication channel configuration (BD2)).

.. spec:: BPCT memory map and NvM block configuration (BD3) architecture
   :id: QDX-SWA-SP-065
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-065
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-065 (BPCT memory map and NvM block configuration (BD3)).

.. spec:: BPCT flash block size constraint validation (BD3) architecture
   :id: QDX-SWA-SP-066
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-066
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-066 (BPCT flash block size constraint validation (BD3)).

.. spec:: BPCT core parameters and UDS session configuration (BD4) architecture
   :id: QDX-SWA-SP-067
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-067
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-067 (BPCT core parameters and UDS session configuration (BD4)).

.. spec:: BPCT timing, hardware and watchdog configuration (BD5) architecture
   :id: QDX-SWA-SP-068
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-068
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-068 (BPCT timing, hardware and watchdog configuration (BD5)).

.. spec:: BPCT watchdog timeout cross-constraint validation (BD5) architecture
   :id: QDX-SWA-SP-069
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-069
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-069 (BPCT watchdog timeout cross-constraint validation (BD5)).

.. spec:: BPCT cross-designer timing dependency propagation architecture
   :id: QDX-SWA-SP-070
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-070
   :sys_req: QDX-SYS-008

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-070 (BPCT cross-designer timing dependency propagation).

.. spec:: BPCT crypto and secure boot configuration (BD6) architecture
   :id: QDX-SWA-SP-071
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-071
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-071 (BPCT crypto and secure boot configuration (BD6)).

.. spec:: BPCT weak cryptographic algorithm detection (BD6) architecture
   :id: QDX-SWA-SP-072
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-072
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-072 (BPCT weak cryptographic algorithm detection (BD6)).

.. spec:: BPCT key address placement validation (BD6) architecture
   :id: QDX-SWA-SP-073
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-073
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-073 (BPCT key address placement validation (BD6)).

.. spec:: BPCT validation rule engine (cross-designer) architecture
   :id: QDX-SWA-SP-074
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-074
   :sys_req: QDX-SYS-020

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-074 (BPCT validation rule engine (cross-designer)).

.. spec:: BPCT C header and Makefile generation architecture
   :id: QDX-SWA-SP-075
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-075
   :sys_req: QDX-SYS-009

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-075 (BPCT C header and Makefile generation).

.. spec:: BPCT output preview in BD1 designer architecture
   :id: QDX-SWA-SP-076
   :status: Draft
   :domain: bootloader
   :cr_id: —
   :implements: QDX-SWE-076
   :sys_req: QDX-SYS-014

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-076 (BPCT output preview in BD1 designer).

.. spec:: AI-Assist availability gated by domain extension architecture
   :id: QDX-SWA-SP-077
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-077
   :sys_req: QDX-SYS-016

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-077 (AI-Assist availability gated by domain extension).

.. spec:: AI-Assist context injection per domain architecture
   :id: QDX-SWA-SP-078
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-078
   :sys_req: QDX-SYS-016

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-078 (AI-Assist context injection per domain).

.. spec:: AI-Assist OperationPlan scoped to active domain architecture
   :id: QDX-SWA-SP-079
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-079
   :sys_req: QDX-SYS-017

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-079 (AI-Assist OperationPlan scoped to active domain).

.. spec:: AI-Assist BPCT domain tools architecture
   :id: QDX-SWA-SP-080
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-080
   :sys_req: QDX-SYS-016

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-080 (AI-Assist BPCT domain tools).

.. spec:: LW-BSW project creation and ECU/DEXT import architecture
   :id: QDX-SWA-SP-081
   :status: Draft
   :domain: lw-bsw
   :cr_id: —
   :implements: QDX-SWE-081
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-081 (LW-BSW project creation and ECU/DEXT import).

.. spec:: LW-BSW module configuration — ten BSW modules architecture
   :id: QDX-SWA-SP-082
   :status: Draft
   :domain: lw-bsw
   :cr_id: —
   :implements: QDX-SWE-082
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-082 (LW-BSW module configuration — ten BSW modules).

.. spec:: LW-BSW CAN and optional LIN communication configuration architecture
   :id: QDX-SWA-SP-083
   :status: Draft
   :domain: lw-bsw
   :cr_id: —
   :implements: QDX-SWE-083
   :sys_req: QDX-SYS-004

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-083 (LW-BSW CAN and optional LIN communication configuration).

.. spec:: LW-BSW resource budget validation architecture
   :id: QDX-SWA-SP-084
   :status: Draft
   :domain: lw-bsw
   :cr_id: —
   :implements: QDX-SWE-084
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-084 (LW-BSW resource budget validation).

.. spec:: LW-BSW OS scheduling map and race condition analysis architecture
   :id: QDX-SWA-SP-085
   :status: Draft
   :domain: lw-bsw
   :cr_id: —
   :implements: QDX-SWE-085
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-085 (LW-BSW OS scheduling map and race condition analysis).

.. spec:: LW-BSW Config Report generation architecture
   :id: QDX-SWA-SP-086
   :status: Draft
   :domain: lw-bsw
   :cr_id: —
   :implements: QDX-SWE-086
   :sys_req: QDX-SYS-015

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-086 (LW-BSW Config Report generation).

.. spec:: LW-BSW module configuration ``.h`` and ``.c`` generation architecture
   :id: QDX-SWA-SP-087
   :status: Draft
   :domain: lw-bsw
   :cr_id: —
   :implements: QDX-SWE-087
   :sys_req: QDX-SYS-009

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-087 (LW-BSW module configuration ``.h`` and ``.c`` generation).

.. spec:: LW-BSW bus-level compatibility check with Classic AUTOSAR architecture
   :id: QDX-SWA-SP-088
   :status: Draft
   :domain: lw-bsw
   :cr_id: —
   :implements: QDX-SWE-088
   :sys_req: QDX-SYS-007

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-088 (LW-BSW bus-level compatibility check with Classic AUTOSAR).

.. spec:: LW-BSW AI-Assist Config Insight architecture
   :id: QDX-SWA-SP-089
   :status: Draft
   :domain: lw-bsw
   :cr_id: —
   :implements: QDX-SWE-089
   :sys_req: QDX-SYS-016

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-089 (LW-BSW AI-Assist Config Insight).

.. spec:: LW-BSW ICC-2 conformance constraint enforcement architecture
   :id: QDX-SWA-SP-090
   :status: Draft
   :domain: lw-bsw
   :cr_id: —
   :implements: QDX-SWE-090
   :sys_req: QDX-SYS-006

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-090 (LW-BSW ICC-2 conformance constraint enforcement).

.. spec:: Project creation wizard — welcome and stack selection architecture
   :id: QDX-SWA-SP-091
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-091
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-091 (Project creation wizard — welcome and stack selection).

.. spec:: Classic AUTOSAR — platform version selection step architecture
   :id: QDX-SWA-SP-092
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-092
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-092 (Classic AUTOSAR — platform version selection step).

.. spec:: Classic AUTOSAR — template selection step architecture
   :id: QDX-SWA-SP-093
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-093
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-093 (Classic AUTOSAR — template selection step).

.. spec:: Classic AUTOSAR — project configuration step architecture
   :id: QDX-SWA-SP-094
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-094
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-094 (Classic AUTOSAR — project configuration step).

.. spec:: Adaptive AUTOSAR — template selection step architecture
   :id: QDX-SWA-SP-095
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-095
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-095 (Adaptive AUTOSAR — template selection step).

.. spec:: Adaptive AUTOSAR — project configuration step architecture
   :id: QDX-SWA-SP-096
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-096
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-096 (Adaptive AUTOSAR — project configuration step).

.. spec:: Bootloader (BPCT) — template selection step architecture
   :id: QDX-SWA-SP-097
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-097
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-097 (Bootloader (BPCT) — template selection step).

.. spec:: Bootloader (BPCT) — MCU and project configuration step architecture
   :id: QDX-SWA-SP-098
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-098
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-098 (Bootloader (BPCT) — MCU and project configuration step).

.. spec:: LW-BSW — project configuration step architecture
   :id: QDX-SWA-SP-099
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-099
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-099 (LW-BSW — project configuration step).

.. spec:: Project creation — review and confirmation step architecture
   :id: QDX-SWA-SP-100
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-100
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-100 (Project creation — review and confirmation step).

.. spec:: Project creation — step navigation and per-stack sequences architecture
   :id: QDX-SWA-SP-101
   :status: Draft
   :domain: shared
   :cr_id: —
   :implements: QDX-SWE-101
   :sys_req: QDX-SYS-002

   Defines the SWE.2 architectural structures, interfaces, and behavioral constraints that realize QDX-SWE-101 (Project creation — step navigation and per-stack sequences).
