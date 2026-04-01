.. ============================================================
.. QORIX — Software Detailed Design
.. ASPICE: SWE.3
.. Derived from: QDX-SWA-DOC-001 (SWE.2), QDX-SWE-DOC-001 (SWE.1)
..               Qorix Developer C4 Architecture
.. ============================================================

.. _sw_detailed_design:

========================================================
Software Detailed Design
========================================================

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Document ID**
     - QDX-SDD-DOC-001
   * - **Product line**
     - Platform — Qorix Developer (all stacks)
   * - **Component**
     - Qorix Developer Platform — full detailed design
   * - **Version**
     - 0.1.0
   * - **Status**
     - Draft
   * - **Owner**
     - Qorix Developer Engineering Team
   * - **Approved by**
     - TBD — Approval pending
   * - **ASPICE process**
     - SWE.3 — Software Detailed Design
   * - **Parent SWE.2 doc**
     - :ref:`sw_architecture` (QDX-SWA-DOC-001)
   * - **Parent SWE.1 doc**
     - :ref:`sw_requirements` (QDX-SWE-DOC-001)
   * - **Jira epic**
     - QDX-EPIC-PLATFORM-SDD
   * - **Git path**
     - ``docs/sdd/platform/sw_detailed_design.rst``
   * - **Changelog**
     - See :ref:`sdd_changelog`

----

.. contents:: Table of contents
   :depth: 3
   :local:

----


1. Purpose and Scope
====================

This document provides the software detailed design for the Qorix
Developer Platform. It is fully derived from the software architecture
described in :ref:`sw_architecture` (QDX-SWA-DOC-001) and realises
the software requirements in :ref:`sw_requirements` (QDX-SWE-DOC-001).

SWE.3 goes one level below SWE.2. Where SWE.2 specifies component
responsibilities and interfaces, SWE.3 specifies:

- Module decomposition within each component
- Public function and method signatures
- Algorithm descriptions and control flow
- Data structure definitions
- Error handling per function
- Unit test specifications (QDX-UT-NNN) per public function
- Static analysis and coding standard compliance requirements

This document covers all six SDD child documents defined in SWE.2:

- **Section 4** — IDE Layer (``QDX-SDD-IDE-001``)
- **Section 5** — Rust Domain Platform (``QDX-SDD-RUST-001``)
- **Section 6** — ARXML Gateway (``QDX-SDD-GW-001``)
- **Section 7** — Qorix Agent / MCP Layer (``QDX-SDD-MCP-001``)
- **Section 8** — BPCT Subsystem (``QDX-SDD-BPCT-001``)
- **Section 9** — LW-BSW Subsystem (``QDX-SDD-LWBSW-001``)


2. Design Conventions
======================

2.1 Function specification format
-----------------------------------

Each public function is specified as follows:

.. code-block:: text

   Function:     <module>::<function_name>
   Signature:    fn <name>(<params>) -> <return>
   Purpose:      One sentence.
   Preconditions: What must be true before calling.
   Postconditions: What is guaranteed on return.
   Algorithm:    Numbered steps or Mermaid flowchart.
   Error cases:  What is returned / logged on each failure mode.
   SWE.1 refs:   QDX-SWE-NNN
   Unit tests:   QDX-UT-NNN

2.2 Naming conventions
-----------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Element
     - Convention
   * - Rust public functions
     - ``snake_case`` — e.g. ``validate_yaml``, ``load_workspace``
   * - Rust public types / structs
     - ``PascalCase`` — e.g. ``DiagnosticList``, ``OperationPlan``
   * - Rust error types
     - ``PascalCase`` suffixed with ``Error`` — e.g. ``ValidationError``
   * - YAML field names
     - ``snake_case`` matching the Rust struct field name
   * - Unit test IDs
     - ``QDX-UT-NNN`` — sequential, assigned at authoring time
   * - Module path notation
     - ``crate::module::submodule`` — matches Rust module hierarchy

2.3 Static analysis requirements
----------------------------------

All Rust source files in ``core::*``, ``classic::*``, ``adaptive::*``
crates must pass the following checks with zero warnings before merge:

- ``cargo clippy -- -D warnings`` — all Clippy lints as errors
- ``cargo fmt --check`` — Rustfmt formatting enforced
- Maximum cyclomatic complexity per function: 15 (enforced by
  ``cargo-cyclonedx`` or equivalent)
- No ``unsafe`` blocks without ``// SAFETY:`` comment and ADR reference
- No ``unwrap()`` or ``expect()`` in production paths — use ``?`` or
  explicit match

TypeScript / JavaScript (IDE Layer) must pass:

- ``eslint --max-warnings 0`` with the project ESLint config
- ``tsc --noEmit`` — TypeScript strict mode, zero type errors


3. Data Structures
===================

3.1 Core shared types
----------------------

These types are defined in ``core::model`` and used across all crates.

.. code-block:: rust

   /// Severity level for a validation diagnostic.
   #[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
   pub enum Severity {
       Info,
       Warning,
       Error,
   }

   /// A single diagnostic produced by validation or import.
   #[derive(Debug, Clone)]
   pub struct Diagnostic {
       pub severity:  Severity,
       pub code:      String,       // e.g. "CLASSIC-VAL-001"
       pub message:   String,       // Human-readable, actionable
       pub file_path: PathBuf,      // Absolute path to YAML source file
       pub yaml_path: String,       // Dot-notation path e.g. "swcs[0].ports[1].name"
   }

   /// Ordered collection of diagnostics from a validation pass.
   pub type DiagnosticList = Vec<Diagnostic>;

   /// Qualified AUTOSAR name (slash-separated path).
   #[derive(Debug, Clone, PartialEq, Eq, Hash)]
   pub struct QualifiedName(pub String);   // e.g. "/Qorix/Classic/SWC/SpeedSensor"

   /// A typed atomic mutation on a YAML model.
   #[derive(Debug, Clone)]
   pub enum Op {
       Add    { path: String, value: serde_json::Value },
       Update { path: String, value: serde_json::Value },
       Delete { path: String },
   }

   /// An ordered set of Ops proposed by the AI agent or a domain
   /// operation, pending engineer acceptance.
   #[derive(Debug, Clone)]
   pub struct OperationPlan {
       pub ops:         Vec<Op>,
       pub description: String,     // Human-readable summary for review
       pub domain:      Domain,     // Prevents cross-domain application
       pub source:      PlanSource, // AIAssist | DomainOp | Migration
   }

   /// Domain tag — enforces OperationPlan scoping.
   #[derive(Debug, Clone, PartialEq, Eq)]
   pub enum Domain { Classic, Adaptive, Bpct, LwBsw, SCore }

   /// Stack-specific project type, set at creation.
   #[derive(Debug, Clone)]
   pub enum StackType {
       Classic { platform: ClassicPlatform },
       Adaptive { release: String },
       Bpct    { mcu_family: McuFamily },
       LwBsw   { mcu_family: McuFamily },
       SCore,
   }

3.2 Workspace and project model
---------------------------------

.. code-block:: rust

   /// Top-level workspace container — persisted as workspace.yaml.
   #[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
   pub struct Workspace {
       pub name:     String,
       pub version:  String,
       pub projects: Vec<ProjectRef>,
   }

   /// Reference to a project within a workspace.
   #[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
   pub struct ProjectRef {
       pub name:       String,
       pub path:       PathBuf,    // Relative to workspace root
       pub stack_type: StackType,
   }

   /// Provenance record written alongside every generated artefact.
   #[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
   pub struct ProvenanceRecord {
       pub generated_at:    chrono::DateTime<chrono::Utc>,
       pub tool_version:    String,
       pub artop_version:   Option<String>,
       pub source_files:    Vec<SourceFileRef>,
   }

   #[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
   pub struct SourceFileRef {
       pub path:    PathBuf,
       pub git_sha: Option<String>,
   }


4. IDE Layer — Detailed Design (QDX-SDD-IDE-001)
=================================================

4.1 Module decomposition
-------------------------

.. mermaid::

   graph TD
     subgraph IDE ["IDE Layer modules"]
       WM["workspace_manager\nOpen/close/scan workspace"]
       YE["yaml_editor\nLSP host + schema binding"]
       CB["command_bus\nDispatch ops to WASM / DS"]
       WB["wasm_bridge\nJS ↔ WASM type bridge"]
       DD["designers/\nC1–C6 · A1–A6 · BD1–BD6"]
       DP["diagnostics_panel\nMerge + render diagnostics"]
       AI_P["ai_panel\nMCP client + plan review UI"]
       WIZ["wizard/\nProject creation flow"]
     end
     WM --> CB
     YE --> WB
     DD --> CB
     CB --> WB
     CB --> DS_CLIENT["domain_service_client\nHTTP/gRPC thin client"]
     WB --> DP
     DS_CLIENT --> DP
     AI_P --> DS_CLIENT
     WIZ --> WM

4.2 workspace_manager module
-----------------------------

**4.2.1** ``workspace_manager::open``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``async fn open(path: &Path) -> Result<Workspace, WorkspaceError>``
   * - **Purpose**
     - Parse ``workspace.yaml``, validate project references exist on
       disk, dispatch ``domain_service_client::load_workspace`` for
       semantic model loading, and return the populated Workspace.
   * - **Preconditions**
     - ``path`` points to a directory containing ``workspace.yaml``.
   * - **Postconditions**
     - Returns ``Ok(Workspace)`` with all ``ProjectRef`` entries
       confirmed present on disk. Domain Service has loaded the model.
       Total elapsed time ≤ 30 s for a medium workspace (QDX-SWE-054).
   * - **Algorithm**
     - 1. Read and deserialise ``workspace.yaml`` via ``core::yaml``.
       2. For each ``ProjectRef``, assert the declared path exists.
       3. Collect missing paths into ``Vec<PathBuf>``; if non-empty
          return ``Err(WorkspaceError::MissingProjects(paths))``.
       4. Call ``domain_service_client::load_workspace(&workspace)``
          asynchronously; await with a 30 s timeout.
       5. On timeout return ``Err(WorkspaceError::Timeout)``.
       6. On success return ``Ok(workspace)``.
   * - **Error cases**
     - ``WorkspaceError::NotFound`` — ``workspace.yaml`` absent.
       ``WorkspaceError::ParseError(e)`` — malformed YAML.
       ``WorkspaceError::MissingProjects(Vec<PathBuf>)`` — refs missing.
       ``WorkspaceError::Timeout`` — Domain Service load exceeded 30 s.
   * - **SWE.1 refs**
     - QDX-SWE-001, QDX-SWE-054
   * - **Unit tests**
     - QDX-UT-001 — valid workspace opens successfully within 30 s.
       QDX-UT-002 — missing project ref returns MissingProjects error.
       QDX-UT-003 — malformed workspace.yaml returns ParseError.

**4.2.2** ``workspace_manager::scaffold_project``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn scaffold_project(root: &Path, config: &ProjectConfig) -> Result<ProjectRef, ScaffoldError>``
   * - **Purpose**
     - Create the full directory structure and mandatory YAML source
       files for a new project of the requested stack type.
   * - **Preconditions**
     - ``root`` exists and is writable. ``config.name`` matches
       ``[A-Za-z0-9_]+``. No project with ``config.name`` exists
       under ``root``.
   * - **Postconditions**
     - Project directory created at ``root/config.name/``.
       All mandatory YAML source files written with template defaults.
       A ``src/`` and ``out/`` subdirectory exist (QDX-SWE-003).
       Returns ``Ok(ProjectRef)`` pointing to the new project.
   * - **Algorithm**
     - 1. Validate ``config.name`` against ``[A-Za-z0-9_]+``; return
          ``Err(ScaffoldError::InvalidName)`` if fails.
       2. Assert target directory does not exist; return
          ``Err(ScaffoldError::AlreadyExists)`` if it does.
       3. Create ``root/name/src/`` and ``root/name/out/``.
       4. Dispatch to the stack-specific scaffold function:
          ``classic_scaffold``, ``adaptive_scaffold``,
          ``bpct_scaffold``, ``lwbsw_scaffold``, or
          ``score_scaffold``.
       5. Write ``project.yaml`` metadata file.
       6. Return ``Ok(ProjectRef)``.
   * - **Error cases**
     - ``ScaffoldError::InvalidName`` — name fails regex.
       ``ScaffoldError::AlreadyExists`` — directory collision.
       ``ScaffoldError::IoError(e)`` — file system failure.
   * - **SWE.1 refs**
     - QDX-SWE-002, QDX-SWE-003
   * - **Unit tests**
     - QDX-UT-004 — Classic scaffold creates all six YAML files.
       QDX-UT-005 — Adaptive scaffold creates all six YAML files.
       QDX-UT-006 — BPCT scaffold creates all six bl-*.yaml files.
       QDX-UT-007 — invalid name returns InvalidName error.
       QDX-UT-008 — duplicate name returns AlreadyExists error.

4.3 command_bus module
-----------------------

**4.3.1** ``command_bus::execute``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``async fn execute(cmd: Command) -> Result<CommandResult, BusError>``
   * - **Purpose**
     - Translate a UI action (drag, drop, property edit, button click)
       into a typed domain operation, dispatch it to the WASM bridge
       for local validation, and return the merged result including
       any diagnostics.
   * - **Preconditions**
     - A workspace is open. ``cmd.domain`` matches the active designer.
   * - **Postconditions**
     - The operation is applied to the in-memory model.
       ``CommandResult.diagnostics`` contains the merged WASM +
       Domain Service diagnostic list.
       YAML file is written atomically (QDX-SWE-005) if no ERROR
       diagnostics are present.
   * - **Algorithm**
     - 1. Deserialise ``cmd`` into a typed ``Op`` via
          ``core::ops::parse_command``.
       2. Call ``wasm_bridge::plan_ops(op)`` — returns ``OperationPlan``.
       3. Call ``wasm_bridge::validate_yaml(affected_files)`` — returns
          fast ``DiagnosticList``.
       4. If any ``Severity::Error`` in fast list, return
          ``Ok(CommandResult { applied: false, diagnostics })``
          without writing to disk.
       5. Apply ``OperationPlan`` to in-memory model.
       6. Write YAML atomically via ``core::yaml::atomic_save``.
       7. Dispatch async deep validation to Domain Service; update
          diagnostics panel on response.
       8. Return ``Ok(CommandResult { applied: true, diagnostics })``.
   * - **Error cases**
     - ``BusError::InvalidCommand`` — unknown command string.
       ``BusError::DomainMismatch`` — cmd domain ≠ active designer.
       ``BusError::WasmUnavailable`` — WASM module not initialised.
   * - **SWE.1 refs**
     - QDX-SWE-008, QDX-SWE-029, QDX-SWE-031, QDX-SWE-005
   * - **Unit tests**
     - QDX-UT-009 — valid addSwc command applies and saves.
       QDX-UT-010 — command with ERROR diagnostic does not write file.
       QDX-UT-011 — domain mismatch returns DomainMismatch error.

4.4 wasm_bridge module
-----------------------

**4.4.1** ``wasm_bridge::validate_yaml``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn validate_yaml(content: &str, schema_id: &str) -> DiagnosticList``
   * - **Purpose**
     - Execute in-process WASM validation for a single YAML file
       against the registered JSON Schema and return diagnostics
       within 500 ms (QDX-SWE-055).
   * - **Preconditions**
     - WASM module is initialised. ``schema_id`` is registered.
   * - **Postconditions**
     - Returns ``DiagnosticList`` (may be empty). Does not modify
       any file or model state. Completes within 500 ms for files
       up to 5,000 lines.
   * - **Algorithm**
     - 1. Look up JSON Schema by ``schema_id`` from schema registry.
       2. Parse YAML content with ``core::yaml::parse_loose`` — allows
          partial structures during editing.
       3. Run ``core::validation::run_schema_rules`` against parsed
          content.
       4. Return ``DiagnosticList`` sorted by (file, line, severity).
   * - **Error cases**
     - Returns single ``Diagnostic { severity: Error, code:
       "WASM-001" }`` if schema_id is not registered.
       Returns single ``Diagnostic { severity: Error, code:
       "WASM-002" }`` if YAML is unparseable (not just invalid).
   * - **SWE.1 refs**
     - QDX-SWE-031, QDX-SWE-055, QDX-SWE-060
   * - **Unit tests**
     - QDX-UT-012 — valid YAML returns empty diagnostic list.
       QDX-UT-013 — missing required field returns Error diagnostic.
       QDX-UT-014 — validation completes within 500 ms for 5,000-line file.
       QDX-UT-015 — unknown schema_id returns WASM-001 diagnostic.

4.5 diagnostics_panel module
------------------------------

**4.5.1** ``diagnostics_panel::merge_and_render``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn merge_and_render(wasm: DiagnosticList, deep: DiagnosticList) -> RenderedDiagnostics``
   * - **Purpose**
     - Merge fast WASM diagnostics with deep Domain Service diagnostics,
       deduplicate by (code, file_path, yaml_path), sort by severity
       descending then by file/path, and return a structure ready for
       UI rendering (QDX-SWE-036, QDX-SWE-037).
   * - **Preconditions**
     - Both lists may be empty. No ordering assumption on inputs.
   * - **Postconditions**
     - Returned list contains no duplicates. ERROR items appear before
       WARNING before INFO. Each item has a non-empty, actionable
       ``message`` and a valid ``yaml_path``.
   * - **Algorithm**
     - 1. Concatenate ``wasm`` and ``deep`` into a single list.
       2. Deduplicate: for equal ``(code, file_path, yaml_path)``
          tuples, keep the entry with the higher severity.
       3. Sort: primary key = severity descending; secondary =
          file_path; tertiary = yaml_path.
       4. Wrap in ``RenderedDiagnostics { items, error_count,
          warning_count, info_count }``.
   * - **Error cases**
     - Function is infallible — always returns a valid
       ``RenderedDiagnostics`` (empty if both inputs empty).
   * - **SWE.1 refs**
     - QDX-SWE-036, QDX-SWE-037
   * - **Unit tests**
     - QDX-UT-016 — duplicate diagnostics are deduplicated.
       QDX-UT-017 — ERROR items appear before WARNING in output.
       QDX-UT-018 — empty inputs return empty RenderedDiagnostics.

4.6 wizard module
------------------

**4.6.1** ``wizard::validate_step``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn validate_step(step: &WizardStep, state: &WizardState) -> StepValidation``
   * - **Purpose**
     - Validate all required fields on the current wizard step and
       return a ``StepValidation`` that drives the Continue button
       enabled/disabled state and inline error messages (QDX-SWE-101).
   * - **Preconditions**
     - ``step`` identifies the current step in the sequence for the
       selected stack type.
   * - **Postconditions**
     - Returns ``StepValidation { valid: bool, field_errors: HashMap<FieldId, String> }``.
       If ``valid`` is true, the Continue action is permitted.
   * - **Algorithm**
     - 1. Match on ``step`` variant.
       2. For ``StepProjectName``: validate ``state.project_name``
          against ``^[A-Za-z0-9_]+$``; if fails, insert
          ``"Name must be alphanumeric and underscore only"`` into
          ``field_errors``.
       3. For ``StepBpctProjectId``: validate ``state.fbl_project_name``
          against ``^[A-Z][A-Z0-9_]+$``; if fails, insert error.
       4. For ``StepMcuFamily``: assert ``state.mcu_family`` is Some.
       5. If ``field_errors`` is empty, return ``StepValidation { valid: true, .. }``.
   * - **Error cases**
     - Infallible — validation failures are returned in
       ``field_errors``, not as ``Err``.
   * - **SWE.1 refs**
     - QDX-SWE-101, QDX-SWE-094, QDX-SWE-098
   * - **Unit tests**
     - QDX-UT-019 — valid project name passes validation.
       QDX-UT-020 — name with spaces fails with correct message.
       QDX-UT-021 — lowercase BPCT ID fails validation.
       QDX-UT-022 — empty MCU family blocks step advance.

**4.6.2** ``wizard::get_step_sequence``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn get_step_sequence(stack: &StackType) -> Vec<WizardStep>``
   * - **Purpose**
     - Return the ordered step sequence for the given stack type,
       matching the per-stack sequences mandated in QDX-SWE-101.
   * - **Preconditions**
     - ``stack`` is a valid ``StackType`` variant.
   * - **Postconditions**
     - Returns a non-empty ``Vec<WizardStep>`` in display order.
       Classic returns 5 steps; Adaptive, BPCT and LW-BSW return 4;
       S-Core returns 3.
   * - **Algorithm**
     - Pattern-match on ``stack`` and return the appropriate
       fixed sequence. Sequences are compile-time constants.
   * - **Error cases**
     - Infallible.
   * - **SWE.1 refs**
     - QDX-SWE-101, QDX-SWE-091
   * - **Unit tests**
     - QDX-UT-023 — Classic returns exactly 5 steps.
       QDX-UT-024 — BPCT returns exactly 4 steps with MCUConfig step.
       QDX-UT-025 — S-Core returns exactly 3 steps.

5. Rust Domain Platform — Detailed Design (QDX-SDD-RUST-001)
=============================================================

5.1 Module decomposition
-------------------------

.. mermaid::

   graph TD
     subgraph CORE ["core::* crates"]
       CM["core::model\nShared types & error defs"]
       CY["core::yaml\nYAML ↔ Rust serde bridge"]
       CV["core::validation\nRule engine"]
       CO["core::ops\nOp + OperationPlan model"]
       CG["core::gql_client\nGenerated GraphQL client"]
       CMG["core::migration\nARXML → YAML primitives"]
     end
     subgraph CL ["classic::* crates"]
       CLM["classic::model\nSWC, COM, OS, NvM types"]
       CLV["classic::validation\nClassic semantic rules"]
       CLO["classic::ops\naddSwc, mapRunnable, etc."]
       CLMG["classic::migration\nTresos / DaVinci import"]
     end
     subgraph AD ["adaptive::* crates"]
       ADM["adaptive::model\nService, Machine, Exec types"]
       ADV["adaptive::validation\nAdaptive semantic rules"]
       ADO["adaptive::ops\naddServiceInstance, etc."]
       ADMG["adaptive::migration\nAdaptive ARXML import"]
     end
     subgraph TARGETS ["Build targets"]
       SVC["Rust Domain Service\nHTTP / gRPC"]
       WASM["qorix_core_wasm\nWASM"]
       CLI["qorix_cli\nCLI"]
     end
     CM --> CY --> CV --> CO --> CG
     CLM --> CLV --> CLO --> CLMG
     ADM --> ADV --> ADO --> ADMG
     CORE --> CL
     CORE --> AD
     CL --> SVC
     AD --> SVC
     CORE --> WASM
     CORE --> CLI

5.2 core::yaml module
----------------------

**5.2.1** ``core::yaml::load``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn load<T: DeserializeOwned>(path: &Path) -> Result<T, YamlError>``
   * - **Purpose**
     - Read a YAML source file from disk and deserialise it into a
       typed Rust struct using serde.
   * - **Preconditions**
     - ``path`` is an absolute path to a readable UTF-8 YAML file.
   * - **Postconditions**
     - Returns ``Ok(T)`` with all fields populated. File is not
       modified.
   * - **Algorithm**
     - 1. Read file contents as UTF-8 string; on IO failure return
          ``Err(YamlError::IoError(e))``.
       2. Parse YAML with ``serde_yaml::from_str``; on failure return
          ``Err(YamlError::ParseError { path, source: e })``.
       3. Return ``Ok(value)``.
   * - **Error cases**
     - ``YamlError::IoError(e)`` — file unreadable.
       ``YamlError::ParseError { path, source }`` — invalid YAML or
       schema mismatch.
   * - **SWE.1 refs**
     - QDX-SWE-004
   * - **Unit tests**
     - QDX-UT-026 — valid file deserialises correctly.
       QDX-UT-027 — missing file returns IoError.
       QDX-UT-028 — malformed YAML returns ParseError with path.

**5.2.2** ``core::yaml::atomic_save``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn atomic_save<T: Serialize>(path: &Path, value: &T) -> Result<(), YamlError>``
   * - **Purpose**
     - Serialise ``value`` to YAML with stable key ordering and write
       atomically to ``path`` using write-to-temp-then-rename, preventing
       partial-write corruption (QDX-SWE-005, QDX-ADR-008).
   * - **Preconditions**
     - Parent directory of ``path`` exists and is writable.
   * - **Postconditions**
     - On ``Ok``: ``path`` contains the new YAML content. No partial
       write is visible at any point. Previous content is replaced.
     - On ``Err``: ``path`` is unchanged.
   * - **Algorithm**
     - 1. Serialise ``value`` to YAML string with stable key ordering.
       2. Create temp file ``path.with_extension("yaml.tmp")`` in same
          directory.
       3. Write full YAML string to temp file.
       4. Flush and sync temp file to disk (``fsync``).
       5. Rename temp file to ``path`` (atomic on POSIX systems).
       6. Return ``Ok(())``.
   * - **Error cases**
     - ``YamlError::IoError(e)`` — write, sync or rename failure.
       On error, temp file is removed if it exists.
   * - **SWE.1 refs**
     - QDX-SWE-005
   * - **Unit tests**
     - QDX-UT-029 — saved file content matches serialised input.
       QDX-UT-030 — temp file is cleaned up on write failure.
       QDX-UT-031 — YAML key order is stable across two saves.

5.3 core::validation module
-----------------------------

**5.3.1** ``core::validation::run``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn run(rules: &[Box<dyn ValidationRule>], ctx: &ValidationContext) -> DiagnosticList``
   * - **Purpose**
     - Execute all registered validation rules against the given context
       and return the merged diagnostic list sorted by severity then
       by file and path.
   * - **Preconditions**
     - ``rules`` is non-empty. ``ctx`` contains the loaded model for
       at least one YAML file.
   * - **Postconditions**
     - Returns ``DiagnosticList`` containing all findings from all
       rules. Returns empty list if no rules fire. Does not modify
       model state.
   * - **Algorithm**
     - 1. For each rule in ``rules``, call ``rule.check(ctx)`` and
          collect the returned ``DiagnosticList``.
       2. Concatenate all lists.
       3. Sort: primary = severity descending; secondary = file_path;
          tertiary = yaml_path.
       4. Return merged list.
   * - **Error cases**
     - Infallible. Rule panics are caught via ``std::panic::catch_unwind``
       and converted to a single ``Severity::Error`` diagnostic with
       code ``"CORE-VAL-PANIC"`` and the rule name in the message.
   * - **SWE.1 refs**
     - QDX-SWE-031, QDX-SWE-032, QDX-SWE-037
   * - **Unit tests**
     - QDX-UT-032 — no rules returns empty list.
       QDX-UT-033 — two rules with findings return merged sorted list.
       QDX-UT-034 — panicking rule produces CORE-VAL-PANIC diagnostic.

**5.3.2** ``ValidationRule`` trait

.. code-block:: rust

   /// Implemented by every domain validation rule.
   pub trait ValidationRule: Send + Sync {
       /// Unique code for this rule — e.g. "CLASSIC-VAL-016".
       fn code(&self) -> &'static str;

       /// Human-readable rule description for documentation.
       fn description(&self) -> &'static str;

       /// Execute the rule against the model context.
       fn check(&self, ctx: &ValidationContext) -> DiagnosticList;
   }

5.4 classic::validation module
--------------------------------

The Classic validation module registers the following rules, each
implementing ``ValidationRule``. Rules are invoked by
``core::validation::run`` for every Classic project validation pass.

.. list-table::
   :widths: 18 18 64
   :header-rows: 1

   * - Rule code
     - Severity
     - Check description
   * - CLASSIC-VAL-001
     - Error
     - Every ``Runnable`` defined in ``swc-design.yaml`` has a
       corresponding entry in ``rte-mapping.yaml`` ``runnable_to_task``.
       Missing mappings block generation (QDX-SWE-016).
   * - CLASSIC-VAL-002
     - Error
     - Every ``P-Port`` with a ``SenderReceiver`` interface in
       ``swc-design.yaml`` has a signal mapping in
       ``signals-comstack.yaml``. Unmapped ports block generation.
   * - CLASSIC-VAL-003
     - Error
     - Every ``OS Task`` referenced in ``rte-mapping.yaml`` is declared
       in ``os-scheduling.yaml``. Forward references are not permitted.
   * - CLASSIC-VAL-004
     - Warning
     - Every interface defined in ``swc-design.yaml`` is referenced by
       at least one port. Unreferenced interfaces are flagged as
       potential dead configuration.
   * - CLASSIC-VAL-005
     - Error
     - No two SWCs share the same ``QualifiedName`` within the same
       project. Duplicate identifiers block generation.
   * - CLASSIC-VAL-006
     - Warning
     - CAN signal bit positions in ``signals-comstack.yaml`` do not
       overlap within the same PDU. Overlapping signals are flagged.

**5.4.1** ``classic::validation::UnmappedRunnableRule``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn check(&self, ctx: &ValidationContext) -> DiagnosticList``
   * - **Purpose**
     - Detect every Runnable in swc-design.yaml that has no
       corresponding entry in rte-mapping.yaml runnable_to_task.
   * - **Algorithm**
     - 1. Collect all ``runnable.name`` values from
          ``ctx.classic.swc_design.runnables``.
       2. Collect all ``runnable`` values from
          ``ctx.classic.rte_mapping.runnable_to_task``.
       3. Compute set difference: defined minus mapped.
       4. For each unmapped runnable, emit ``Diagnostic {
          severity: Error, code: "CLASSIC-VAL-001",
          message: "Runnable '<name>' has no task assignment in
          rte-mapping.yaml. Add an entry to runnable_to_task.",
          file_path: rte_mapping_path, yaml_path: "runnable_to_task" }``.
   * - **SWE.1 refs**
     - QDX-SWE-015, QDX-SWE-016
   * - **Unit tests**
     - QDX-UT-035 — all runnables mapped returns empty list.
       QDX-UT-036 — one unmapped runnable returns one Error.
       QDX-UT-037 — message contains runnable name and actionable text.

5.5 adaptive::validation module
---------------------------------

.. list-table::
   :widths: 18 18 64
   :header-rows: 1

   * - Rule code
     - Severity
     - Check description
   * - ADAPTIVE-VAL-001
     - Error
     - Every ``RequiredServiceInstance`` in ``communication.yaml``
       is satisfied by a ``ProvidedServiceInstance`` with a matching
       interface name either in the same project or declared as
       external. Unbound consumers block generation (QDX-SWE-020).
   * - ADAPTIVE-VAL-002
     - Error
     - Every application in ``deployment.yaml`` references a machine
       declared in ``machine-design.yaml``. Deployment to an undeclared
       machine blocks generation (QDX-SWE-027).
   * - ADAPTIVE-VAL-003
     - Error
     - No process in ``execution.yaml`` is assigned to a core index
       that exceeds the ``cpu_core_count`` declared in
       ``machine-design.yaml`` (QDX-SWE-022).
   * - ADAPTIVE-VAL-004
     - Error
     - No two processes in ``execution.yaml`` are assigned identical
       scheduling priority within the same resource group
       (QDX-SWE-025).
   * - ADAPTIVE-VAL-005
     - Warning
     - Every service defined in ``application-design.yaml`` is
       referenced by at least one entry in ``communication.yaml``.
       Unreferenced services are flagged.
   * - ADAPTIVE-VAL-006
     - Error
     - The sum of ``cpu_budget_percent`` across all processes assigned
       to the same machine does not exceed 100% (QDX-SWE-027).

5.6 core::ops module
---------------------

**5.6.1** ``core::ops::apply``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn apply(plan: &OperationPlan, model: &mut DomainModel) -> Result<(), OpsError>``
   * - **Purpose**
     - Apply all ``Op`` entries in an ``OperationPlan`` to the in-memory
       domain model in order. On any failure, roll back all previously
       applied ops and return an error (QDX-SWE-008).
   * - **Preconditions**
     - ``plan.domain`` matches the domain of ``model``. Engineer has
       accepted the plan (acceptance is enforced by the caller — the
       AI Chat Panel acceptance gate).
   * - **Postconditions**
     - On ``Ok``: all ops applied to ``model``; model is consistent.
     - On ``Err``: ``model`` is in the same state as before the call
       (rollback guaranteed).
   * - **Algorithm**
     - 1. Clone ``model`` as ``snapshot`` for rollback.
       2. For each ``op`` in ``plan.ops`` in order:
          a. Match on ``Op`` variant and apply to model.
          b. On failure: restore ``model`` from ``snapshot``,
             return ``Err(OpsError::ApplyFailed { op_index, source })``.
       3. Return ``Ok(())``.
   * - **Error cases**
     - ``OpsError::DomainMismatch`` — plan domain ≠ model domain.
       ``OpsError::InvalidPath(path)`` — target YAML path does not exist.
       ``OpsError::ApplyFailed { op_index, source }`` — op failed;
       model rolled back.
   * - **SWE.1 refs**
     - QDX-SWE-008, QDX-SWE-047, QDX-SWE-048
   * - **Unit tests**
     - QDX-UT-038 — single Add op applies to model correctly.
       QDX-UT-039 — failed op mid-plan rolls back all prior ops.
       QDX-UT-040 — domain mismatch returns DomainMismatch error.

5.7 Domain Service — workspace and generation functions
--------------------------------------------------------

**5.7.1** ``domain_service::load_workspace``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``async fn load_workspace(ws: &Workspace) -> Result<LoadedWorkspace, ServiceError>``
   * - **Purpose**
     - Parse all YAML source files for every project in the workspace,
       build the unified in-memory domain model, and run the initial
       cross-file validation pass.
   * - **Preconditions**
     - All ``ProjectRef`` paths in ``ws`` exist on disk.
   * - **Postconditions**
     - Returns ``Ok(LoadedWorkspace)`` containing parsed models for all
       projects and the initial ``DiagnosticList``. Workspace open
       time ≤ 30 s (QDX-SWE-054).
   * - **Algorithm**
     - 1. For each project in ``ws.projects``, load all stack YAML
          files via ``core::yaml::load``.
       2. Build typed domain model per stack
          (``classic::model`` or ``adaptive::model``).
       3. Run ``core::validation::run`` with the full cross-file
          rule set for each stack.
       4. Return ``Ok(LoadedWorkspace { models, diagnostics })``.
   * - **Error cases**
     - ``ServiceError::ParseError { path, source }`` — YAML file
       unparseable.
       ``ServiceError::Timeout`` — load exceeded 30 s.
   * - **SWE.1 refs**
     - QDX-SWE-001, QDX-SWE-033, QDX-SWE-035, QDX-SWE-054
   * - **Unit tests**
     - QDX-UT-041 — workspace with valid YAML loads all models.
       QDX-UT-042 — corrupt YAML file returns ParseError with path.
       QDX-UT-043 — cross-file reference errors appear in DiagnosticList.

**5.7.2** ``domain_service::generate``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``async fn generate(project: &ProjectRef, output_dir: &Path) -> Result<GenerationResult, ServiceError>``
   * - **Purpose**
     - Validate the project, refuse generation if ERROR diagnostics
       exist, invoke the ARXML Gateway for ARXML-producing stacks,
       write output artefacts to ``output_dir``, and write
       ``provenance.json`` (QDX-SWE-038, QDX-SWE-041).
   * - **Preconditions**
     - Project model is loaded. ``output_dir`` exists and is writable.
   * - **Postconditions**
     - On ``Ok``: artefact files written to ``output_dir``.
       ``provenance.json`` written with tool version, ARTOP version,
       source file Git SHAs and UTC timestamp. Generation is
       deterministic — identical inputs produce identical outputs.
     - On ``Err(GenerationBlocked)``: no files written to ``output_dir``.
   * - **Algorithm**
     - 1. Run ``core::validation::run`` on the loaded model.
       2. If any ``Severity::Error`` in result: return
          ``Err(ServiceError::GenerationBlocked { diagnostics })``.
       3. Dispatch to stack-specific generator:
          - Classic / Adaptive: ``core::gql_client::generate_arxml``
          - BPCT / LW-BSW: ``bpct::generator::emit`` /
            ``lwbsw::generator::emit``
       4. Write artefacts to ``output_dir/src/out/``.
       5. Build and write ``ProvenanceRecord`` to
          ``output_dir/provenance.json``.
       6. Return ``Ok(GenerationResult { artefacts, provenance })``.
   * - **Error cases**
     - ``ServiceError::GenerationBlocked { diagnostics }`` — ERRORs.
       ``ServiceError::GatewayError(e)`` — ARXML Gateway failure.
       ``ServiceError::IoError(e)`` — output write failure.
   * - **SWE.1 refs**
     - QDX-SWE-034, QDX-SWE-038, QDX-SWE-039, QDX-SWE-041, QDX-SWE-057
   * - **Unit tests**
     - QDX-UT-044 — generation refused when ERROR diagnostic present.
       QDX-UT-045 — provenance.json written with correct tool version.
       QDX-UT-046 — identical YAML produces identical ARXML output.


6. ARXML Gateway — Detailed Design (QDX-SDD-GW-001)
=====================================================

6.1 Module decomposition
-------------------------

.. mermaid::

   graph TD
     subgraph GW ["ARXML Gateway — Spring Boot modules"]
       GQL_API["graphql/\nSchema resolvers + mutations"]
       ARTOP_SVC["artop_service/\nARTOP wrapper + EMF ops"]
       IMPORT["import/\nARXML → domain model"]
       EXPORT["export/\nDomain model → ARXML"]
       PROV["provenance/\nVersion + schema stamping"]
     end
     GQL_API --> ARTOP_SVC
     ARTOP_SVC --> IMPORT
     ARTOP_SVC --> EXPORT
     EXPORT --> PROV

6.2 GraphQL schema (SDL contract)
-----------------------------------

The ARXML Gateway publishes a versioned GraphQL SDL. The ``core::gql_client``
Rust crate is generated from this SDL. Breaking SDL changes increment
the major version (QDX-SWE-043, QDX-ADR-007).

Key mutations exposed:

.. code-block:: graphql

   type Mutation {
     importArxml(input: ImportInput!): ImportResult!
     generateArxml(input: GenerateInput!): GenerateResult!
   }

   input ImportInput {
     arxmlContent: String!
     targetStack:  StackType!
   }

   type ImportResult {
     model:        DomainModelPayload!
     warnings:     [ConversionWarning!]!
   }

   input GenerateInput {
     model:        DomainModelPayload!
     schemaVersion: String!
   }

   type GenerateResult {
     artefacts:    [Artefact!]!
     artopVersion: String!
   }

6.3 artop_service — import function
--------------------------------------

**6.3.1** ``ArtopService::importArxml``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``ImportResult importArxml(ImportInput input)``
   * - **Purpose**
     - Parse ARXML content via ARTOP, traverse the EMF model, map
       to the domain model JSON payload, and report any elements that
       cannot be represented in the Qorix YAML schema as structured
       warnings (QDX-SWE-040).
   * - **Preconditions**
     - ``input.arxmlContent`` is valid XML. ``input.targetStack``
       determines which AUTOSAR schema version to use.
   * - **Postconditions**
     - Returns ``ImportResult`` with populated ``model`` payload and
       any ``warnings`` for lossy elements. ARTOP instance is released
       after completion.
   * - **Algorithm**
     - 1. Load ARXML content into ARTOP resource set.
       2. Traverse EMF model top-down collecting typed elements.
       3. Map each element to the Qorix domain model JSON payload.
       4. For elements with no equivalent in the Qorix schema, emit
          ``ConversionWarning { element_path, reason }``.
       5. Release ARTOP resource set.
       6. Return ``ImportResult { model, warnings }``.
   * - **Error cases**
     - ``GatewayException.INVALID_ARXML`` — XML parse failure.
       ``GatewayException.SCHEMA_MISMATCH`` — AUTOSAR schema version
       not supported.
   * - **SWE.1 refs**
     - QDX-SWE-040, QDX-SWE-042, QDX-SWE-062
   * - **Unit tests**
     - QDX-UT-047 — valid Classic ARXML imports with zero warnings.
       QDX-UT-048 — ICC-3-only element produces ConversionWarning.
       QDX-UT-049 — invalid XML returns INVALID_ARXML exception.

6.4 artop_service — export function
--------------------------------------

**6.4.1** ``ArtopService::generateArxml``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``GenerateResult generateArxml(GenerateInput input)``
   * - **Purpose**
     - Receive the validated domain model payload from Rust, build the
       ARTOP EMF model, serialise to ARXML, and return the artefact
       bytes. Output must be deterministic: identical input and ARTOP
       version produces identical bytes (QDX-SWE-038).
   * - **Preconditions**
     - ``input.model`` is a complete, validated domain model payload.
       No ERROR diagnostics exist (enforced by ``domain_service::generate``
       before calling this function).
   * - **Postconditions**
     - Returns ``GenerateResult`` with ARXML artefact bytes and
       ARTOP version string. No timestamps or random GUIDs embedded
       in output.
   * - **Algorithm**
     - 1. Construct ARTOP resource set from ``input.model`` payload.
       2. Set deterministic serialisation options: fixed element
          order, no generated timestamps, no random GUIDs.
       3. Serialise to ARXML bytes.
       4. Return ``GenerateResult { artefacts, artopVersion }``.
   * - **Error cases**
     - ``GatewayException.SERIALISATION_FAILED`` — EMF model invalid.
   * - **SWE.1 refs**
     - QDX-SWE-038, QDX-SWE-039, QDX-SWE-041
   * - **Unit tests**
     - QDX-UT-050 — identical input produces identical ARXML bytes.
       QDX-UT-051 — output contains artopVersion in provenance payload.
       QDX-UT-052 — no timestamp fields in generated ARXML.

7. Qorix Agent / MCP Layer — Detailed Design (QDX-SDD-MCP-001)
===============================================================

7.1 Module decomposition
-------------------------

.. mermaid::

   graph TD
     subgraph MCP ["Qorix Agent modules"]
       IR["intent_router\nDomain detect + dispatch"]
       TR["tool_registry\nMCP tool catalogue"]
       CL_T["classic_tools\nsuggest_runnable_mappings etc."]
       AD_T["adaptive_tools\nsuggest_service_bindings etc."]
       BP_T["bpct_tools\nsuggest_timing_parameters etc."]
       LW_T["lwbsw_tools\nconfig_insight"]
       DTC["data_transmission_control\nContent filter for LLM"]
       AUDIT["audit_logger\nEvent recording"]
     end
     IR --> TR
     TR --> CL_T & AD_T & BP_T & LW_T
     IR --> DTC --> LLM["LLM Backend"]
     CL_T & AD_T & BP_T & LW_T --> DS["Rust Domain Service"]
     IR --> AUDIT

7.2 intent_router module
-------------------------

**7.2.1** ``intent_router::route``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``async fn route(req: AgentRequest) -> Result<OperationPlan, AgentError>``
   * - **Purpose**
     - Detect the active domain from the designer context in the
       request, retrieve the matching tool set from the Tool Registry,
       call the appropriate domain tool via the Domain Service, obtain
       LLM explanation, and return a typed ``OperationPlan``
       (QDX-SWE-050, QDX-SWE-079).
   * - **Preconditions**
     - ``req.context.active_designer`` is a valid designer tab ID
       (e.g. ``"C6"``, ``"A2"``, ``"BD5"``).
       The domain extension for the active designer is installed
       (QDX-SWE-077).
   * - **Postconditions**
     - Returns ``Ok(OperationPlan)`` scoped to the detected domain.
       The plan contains no ops targeting files outside that domain.
       Audit record written for the routing event.
   * - **Algorithm**
     - 1. Parse ``req.context.active_designer`` to determine
          ``Domain`` (C* → Classic, A* → Adaptive, BD* → Bpct).
       2. Check Tool Registry for domain extension availability;
          return ``Err(AgentError::DomainExtensionNotInstalled)``
          if absent.
       3. Apply data transmission control:
          if ``config.exclude_yaml_content`` is true, strip YAML
          content from ``req.context`` before LLM call.
       4. Look up domain tool function in Tool Registry.
       5. Call domain tool via Domain Service; receive typed ops.
       6. Call LLM backend for natural language explanation of ops.
       7. Build ``OperationPlan { ops, description, domain, source: AIAssist }``.
       8. Write audit record via ``audit_logger::record``.
       9. Return ``Ok(plan)``.
   * - **Error cases**
     - ``AgentError::DomainExtensionNotInstalled`` — extension absent.
       ``AgentError::DomainMismatch`` — ops outside detected domain.
       ``AgentError::LlmError(e)`` — LLM backend unreachable.
       ``AgentError::ToolError(e)`` — Domain Service tool call failed.
   * - **SWE.1 refs**
     - QDX-SWE-047, QDX-SWE-050, QDX-SWE-051, QDX-SWE-077,
       QDX-SWE-078, QDX-SWE-079
   * - **Unit tests**
     - QDX-UT-053 — C6 designer routes to Classic tool set.
       QDX-UT-054 — BD5 designer routes to BPCT tool set.
       QDX-UT-055 — missing extension returns DomainExtensionNotInstalled.
       QDX-UT-056 — content excluded when data_transmission_control set.

7.3 audit_logger module
------------------------

**7.3.1** ``audit_logger::record``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn record(event: AuditEvent) -> Result<(), AuditError>``
   * - **Purpose**
     - Append a structured audit record to the project audit log file
       for critical user actions including generation, publication,
       AI OperationPlan acceptance and ARXML import (QDX-SWE-052).
   * - **Preconditions**
     - Audit log directory exists and is writable.
   * - **Postconditions**
     - ``AuditEvent`` appended as newline-delimited JSON to
       ``<project>/out/audit.log``. Each record has UTC timestamp,
       event type, user identity, project path and outcome.
   * - **Algorithm**
     - 1. Serialise ``event`` to JSON with ``serde_json::to_string``.
       2. Open audit log file in append mode.
       3. Write serialised JSON + ``\n``.
       4. Return ``Ok(())``.
   * - **Error cases**
     - ``AuditError::IoError(e)`` — file write failure. On error,
       the operation that triggered the audit event is NOT rolled back.
       Audit failures are logged to stderr but do not block the
       triggering operation.
   * - **SWE.1 refs**
     - QDX-SWE-052
   * - **Unit tests**
     - QDX-UT-057 — event written as valid JSON with UTC timestamp.
       QDX-UT-058 — two events produce two newline-separated records.
       QDX-UT-059 — audit failure does not propagate to caller.


8. BPCT Subsystem — Detailed Design (QDX-SDD-BPCT-001)
=======================================================

8.1 Module decomposition
-------------------------

.. mermaid::

   graph TD
     subgraph BPCT ["BPCT subsystem modules"]
       BM["bpct::model\nFBL types, MCU family defaults"]
       BV["bpct::validation\nVR_NNN rule engine"]
       BO["bpct::ops\nMCU default apply, security configure"]
       BG["bpct::generator\nbl-*.yaml → .h / Makefile"]
       BMC["bpct::mcu_defaults\nMCU family hardware constant table"]
     end
     BMC --> BM --> BV
     BM --> BO
     BM --> BG

8.2 BPCT data structures
-------------------------

.. code-block:: rust

   /// MCU family identifier — drives hardware defaults.
   #[derive(Debug, Clone, PartialEq, Eq)]
   pub enum McuFamily {
       Tc3xx, Tc4xx, Rh850, S32k1xx, S32k3xx, S32gx,
   }

   /// Hardware constants derived from MCU family selection.
   #[derive(Debug, Clone)]
   pub struct McuDefaults {
       pub flash_page_size_bytes: u32,
       pub max_spi_clock_mhz:     u32,
       pub timer_resolution_us:   u32,
       pub ram_bytes:             u64,
       pub flash_bytes:           u64,
       pub mcu_clock_mhz:         u32,
   }

   /// Security profile selected in the project creation wizard.
   #[derive(Debug, Clone, PartialEq, Eq)]
   pub enum SecurityProfile {
       None,
       SecureBoot,       // RSA2048 signature only
       FullSecurity,     // RSA2048 + AES256 encryption
   }

8.3 bpct::mcu_defaults module
-------------------------------

**8.3.1** ``bpct::mcu_defaults::get``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn get(family: &McuFamily) -> McuDefaults``
   * - **Purpose**
     - Return the compile-time hardware constant table for the given
       MCU family. These defaults are applied to all six ``bl-*.yaml``
       source files on project creation (QDX-SWE-063, QDX-SWE-098).
   * - **Preconditions**
     - None — all MCU families are covered.
   * - **Postconditions**
     - Returns ``McuDefaults`` with all fields set to canonical values
       for the family.
   * - **Algorithm**
     - Pattern-match on ``family`` and return compile-time constant.
       No file I/O, no network call.
   * - **MCU defaults table:**

     .. list-table::
        :widths: 14 14 14 14 14 15 15
        :header-rows: 1

        * - MCU
          - Page (B)
          - SPI (MHz)
          - Timer (µs)
          - RAM
          - Flash
          - Clock
        * - TC3xx
          - 256
          - 80
          - 100
          - 6 MB
          - 16 MB
          - 200 MHz
        * - TC4xx
          - 256
          - 100
          - 50
          - 8 MB
          - 32 MB
          - 300 MHz
        * - RH850
          - 512
          - 50
          - 100
          - 4 MB
          - 8 MB
          - 160 MHz
        * - S32K1xx
          - 2048
          - 25
          - 500
          - 256 KB
          - 512 KB
          - 112 MHz
        * - S32K3xx
          - 4096
          - 50
          - 100
          - 512 KB
          - 4 MB
          - 240 MHz
        * - S32Gx
          - 4096
          - 80
          - 50
          - 4 GB
          - 64 MB
          - 1000 MHz

   * - **SWE.1 refs**
     - QDX-SWE-063, QDX-SWE-098
   * - **Unit tests**
     - QDX-UT-060 — TC3xx returns flash_page_size_bytes = 256.
       QDX-UT-061 — all six MCU families return non-zero clock value.

8.4 bpct::validation module — VR_NNN rule engine
-------------------------------------------------

The BPCT validation module implements the VR_NNN cross-designer
constraint rule engine (QDX-SWE-074). Each VR rule implements
``ValidationRule`` and is registered in the BPCT rule set.

.. list-table::
   :widths: 12 14 74
   :header-rows: 1

   * - Rule
     - Severity
     - Constraint
   * - VR_003
     - Error
     - ``flash_block_size_bytes`` in ``bl-memory.yaml`` must be a
       non-zero integer multiple of ``flash_page_size_bytes`` from
       ``bl-project.yaml`` (derived from MCU family). Violation blocks
       generation (QDX-SWE-066).
   * - VR_007
     - Error
     - When ``FBL_WDG_DISABLE_DURING_ERASE = FALSE`` in
       ``bl-hardware.yaml``, ``FBL_WDG_TIMEOUT_MS`` must exceed
       ``FBL_TIMER_ERASE_TIMEOUT_MS`` from ``bl-hardware.yaml``.
       Violation blocks generation (QDX-SWE-069).
   * - VR_010
     - Error
     - ``FBL_CAN_BAUDRATE`` in ``bl-communication.yaml`` must be one
       of the values supported by the selected MCU family CAN
       controller (QDX-SWE-064).
   * - VR_013
     - Warning
     - ``FBL_SEC_SIGNATURE_ALGORITHM = RSA1024`` triggers a warning.
       RSA1024 is not recommended for automotive secure boot.
       Generation is not blocked (QDX-SWE-072).
   * - VR_015
     - Error
     - HSM key store start address in ``bl-security.yaml`` must not
       overlap any application PFlash region defined in
       ``bl-memory.yaml`` (QDX-SWE-073).
   * - VR_020
     - Error
     - ``FBL_TIMER_P2_SERVER_MS`` in ``bl-hardware.yaml`` must be
       less than ``FBL_TIMER_ERASE_TIMEOUT_MS`` (QDX-SWE-070).

**8.4.1** ``bpct::validation::VR007WatchdogRule``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn check(&self, ctx: &ValidationContext) -> DiagnosticList``
   * - **Purpose**
     - Detect the case where watchdog timeout is shorter than the
       erase timeout when ``DISABLE_DURING_ERASE`` is false, which
       would cause a spurious watchdog reset during flash erase
       (QDX-SWE-069).
   * - **Algorithm**
     - 1. Read ``FBL_WDG_DISABLE_DURING_ERASE`` from
          ``ctx.bpct.hardware.wdg_disable_during_erase``.
       2. If ``true``: return empty list (constraint not applicable).
       3. Read ``wdg_timeout_ms`` and ``erase_timeout_ms`` from
          ``ctx.bpct.hardware``.
       4. If ``wdg_timeout_ms`` ≤ ``erase_timeout_ms``: emit
          ``Diagnostic { severity: Error, code: "VR_007",
          message: "FBL_WDG_TIMEOUT_MS (<wdg_timeout_ms> ms) must
          exceed FBL_TIMER_ERASE_TIMEOUT_MS (<erase_timeout_ms> ms)
          when DISABLE_DURING_ERASE = FALSE.
          Increase FBL_WDG_TIMEOUT_MS to at least
          <erase_timeout_ms + 100> ms.",
          file_path: hardware_yaml_path,
          yaml_path: "wdg.FBL_WDG_TIMEOUT_MS" }``.
       5. Return diagnostic list.
   * - **SWE.1 refs**
     - QDX-SWE-069, QDX-SWE-074
   * - **Unit tests**
     - QDX-UT-062 — wdg=2100, erase=2000 returns empty list.
       QDX-UT-063 — wdg=1500, erase=2000 returns VR_007 Error.
       QDX-UT-064 — disable_during_erase=true skips check.
       QDX-UT-065 — message contains both values and suggested fix.

8.5 bpct::generator module
----------------------------

**8.5.1** ``bpct::generator::emit``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn emit(model: &BpctModel, output_dir: &Path) -> Result<Vec<PathBuf>, GeneratorError>``
   * - **Purpose**
     - Generate the BPCT C header files and Makefile from the validated
       ``BpctModel``, write them to ``output_dir``, and return the
       list of written file paths (QDX-SWE-075).
   * - **Preconditions**
     - ``model`` has passed all VR_NNN validation rules with zero
       ERROR diagnostics. ``output_dir`` is writable.
   * - **Postconditions**
     - Files written: ``cfg.h``, ``FblHdr_Cfg.h``, ``FblDiag_Cfg.h``,
       ``FblWd_Cfg.h``, ``FblSec_Cfg.h``, ``Makefile.bpct``.
       Each ``#define`` macro value matches the corresponding
       ``bl-*.yaml`` parameter. Returns list of written paths.
   * - **Algorithm**
     - 1. For each output file, instantiate the corresponding
          Handlebars template with model values.
       2. Write each rendered template to ``output_dir`` via
          ``core::yaml::atomic_save`` equivalent for text files.
       3. Return ``Ok(written_paths)``.
   * - **Error cases**
     - ``GeneratorError::TemplateError(e)`` — template rendering failed.
       ``GeneratorError::IoError(e)`` — file write failed.
   * - **SWE.1 refs**
     - QDX-SWE-075, QDX-SWE-076
   * - **Unit tests**
     - QDX-UT-066 — TC3xx model produces valid cfg.h with correct macros.
       QDX-UT-067 — secure boot model sets FBL_SEC_BOOT_ENABLED = TRUE.
       QDX-UT-068 — six output files written for a complete model.


9. LW-BSW Subsystem — Detailed Design (QDX-SDD-LWBSW-001)
===========================================================

9.1 Module decomposition
-------------------------

.. mermaid::

   graph TD
     subgraph LWBSW ["LW-BSW subsystem modules"]
       LM["lwbsw::model\n10-module config types"]
       LV["lwbsw::validation\nICC-2 rules + resource budget"]
       LG["lwbsw::generator\n.h/.c + Config Report"]
       LI["lwbsw::import\nDEXT / DBC import + mapping"]
       LS["lwbsw::scheduling\nOS scheduling map + race detection"]
     end
     LM --> LV
     LM --> LG
     LI --> LM
     LM --> LS --> LG

9.2 LW-BSW data structures
----------------------------

.. code-block:: rust

   /// Resource budget targets for LW-BSW validation.
   pub struct LwBswTargets {
       pub rom_bytes_max:         u32,   // 150_000
       pub ram_bytes_max:         u32,   // 30_000
       pub cpu_load_percent_max:  u8,    // 10
       pub init_time_ms_max:      u32,   // 100
       pub task_jitter_us_max:    u32,   // 2
       pub interrupt_latency_us_max: u32, // 2
       pub com_send_us_max:       u32,   // 100
   }

   /// One LW-BSW OS task entry in the scheduling map.
   pub struct SchedulingEntry {
       pub task_name:      String,
       pub period_ms:      u32,
       pub priority:       u8,
       pub modules:        Vec<String>,  // modules executing in this task
       pub estimated_us:   u32,
   }

9.3 lwbsw::validation module
------------------------------

**9.3.1** ``lwbsw::validation::ResourceBudgetRule``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn check(&self, ctx: &ValidationContext) -> DiagnosticList``
   * - **Purpose**
     - Validate that the configured LW-BSW module set remains within
       the ROM, RAM and CPU budget targets for the selected MCU family
       (QDX-SWE-084).
   * - **Algorithm**
     - 1. Sum estimated ROM contribution for each enabled module
          from ``lwbsw::model::MODULE_ROM_ESTIMATES`` table.
       2. Sum estimated RAM contribution similarly.
       3. If ROM sum > ``targets.rom_bytes_max``: emit Error
          ``"LWBSW-VAL-001"`` with current and max values.
       4. If RAM sum > ``targets.ram_bytes_max``: emit Error
          ``"LWBSW-VAL-002"``.
       5. Run ``lwbsw::scheduling::estimate_cpu_load`` to get
          estimated CPU load percent.
       6. If CPU > ``targets.cpu_load_percent_max``: emit Error
          ``"LWBSW-VAL-003"``.
       7. Return collected diagnostics.
   * - **SWE.1 refs**
     - QDX-SWE-084, QDX-SWE-090
   * - **Unit tests**
     - QDX-UT-069 — 10 modules within budget returns empty list.
       QDX-UT-070 — ROM overrun returns LWBSW-VAL-001 Error.
       QDX-UT-071 — CPU overrun returns LWBSW-VAL-003 Error.

**9.3.2** ``lwbsw::validation::Icc2ConformanceRule``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn check(&self, ctx: &ValidationContext) -> DiagnosticList``
   * - **Purpose**
     - Detect any ICC-3-only configuration element present in the
       LW-BSW YAML files and emit a WARNING for each, preventing
       accidental ICC-3 configuration in a LW-BSW project
       (QDX-SWE-090).
   * - **Algorithm**
     - 1. Load the set of ICC-3-only field paths from the
          ``ICC3_ONLY_FIELDS`` compile-time constant.
       2. For each field path in ``ICC3_ONLY_FIELDS``, check
          whether it exists in the parsed model.
       3. If present, emit ``Diagnostic { severity: Warning,
          code: "LWBSW-VAL-010",
          message: "Field '<path>' is ICC-3 only and is not
          supported in LW-BSW (ICC-2). This element will be
          ignored during generation.",
          yaml_path: field_path }``.
   * - **SWE.1 refs**
     - QDX-SWE-090
   * - **Unit tests**
     - QDX-UT-072 — clean LW-BSW config returns no ICC-3 warnings.
       QDX-UT-073 — ICC-3 field present returns Warning with field path.

9.4 lwbsw::scheduling module
------------------------------

**9.4.1** ``lwbsw::scheduling::build_scheduling_map``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn build_scheduling_map(model: &LwBswModel) -> SchedulingMap``
   * - **Purpose**
     - Produce the OS scheduling map showing which modules execute
       in which tasks at which periods, and flag potential race
       conditions between tasks sharing a resource (QDX-SWE-085).
   * - **Preconditions**
     - ``model`` is a validated LW-BSW model with OS task assignments.
   * - **Postconditions**
     - Returns ``SchedulingMap`` with: a ``Vec<SchedulingEntry>`` for
       each task, a ``Vec<RaceCondition>`` for detected race conditions,
       and a ``cpu_load_estimate_percent`` value.
   * - **Algorithm**
     - 1. Group enabled modules by their configured OS task.
       2. For each group, sum estimated execution time from
          ``MODULE_TIMING_ESTIMATES`` table.
       3. Compute ``cpu_load_estimate_percent`` as
          ``sum(task_time_us / task_period_us * 100)`` across all tasks.
       4. Detect race conditions: for each pair of tasks sharing a
          common resource (COM buffer, NvM block, CDD interface),
          flag if neither holds a mutex or uses message-queue pattern.
       5. Return ``SchedulingMap { entries, race_conditions, cpu_load_estimate_percent }``.
   * - **SWE.1 refs**
     - QDX-SWE-085, QDX-SWE-086
   * - **Unit tests**
     - QDX-UT-074 — three tasks, no shared resources, no race conditions.
       QDX-UT-075 — two tasks sharing COM buffer without mutex flagged.
       QDX-UT-076 — cpu_load_estimate within expected range for defaults.

9.5 lwbsw::generator module
-----------------------------

**9.5.1** ``lwbsw::generator::emit``

.. list-table::
   :widths: 20 80
   :header-rows: 0

   * - **Signature**
     - ``fn emit(model: &LwBswModel, output_dir: &Path) -> Result<GenerationResult, GeneratorError>``
   * - **Purpose**
     - Generate ``.h`` and ``.c`` configuration files for all ten
       LW-BSW modules and produce the Config Report (QDX-SWE-087,
       QDX-SWE-086).
   * - **Postconditions**
     - Files written to ``output_dir``: one ``.h`` + ``.c`` pair per
       module (20 files), plus ``LwBsw_ConfigReport.txt`` containing
       the scheduling map, resource budget table, race condition list
       and safety flags.
   * - **Algorithm**
     - 1. For each of the 10 modules, render the corresponding
          Handlebars template with model values.
       2. Call ``lwbsw::scheduling::build_scheduling_map`` to get
          scheduling data for the Config Report.
       3. Render Config Report template with scheduling map, budget
          actuals vs targets, and race condition list.
       4. Write all files atomically.
       5. Return ``Ok(GenerationResult { files_written, report_path })``.
   * - **SWE.1 refs**
     - QDX-SWE-086, QDX-SWE-087
   * - **Unit tests**
     - QDX-UT-077 — 10-module model produces 20 source files + report.
       QDX-UT-078 — Config Report contains ROM/RAM/CPU actuals vs targets.
       QDX-UT-079 — race conditions appear in Config Report when detected.


10. Unit Test Specifications (SWE.4)
======================================

.. note::
   Unit test IDs ``QDX-UT-NNN`` are the SWE.4 evidence anchor.
   Each test is implemented as a Rust ``#[test]`` or TypeScript
   ``describe/it`` block in the corresponding test module.
   Test coverage target: ≥ 80% line coverage per crate measured
   by ``cargo llvm-cov``.

.. list-table::
   :widths: 12 18 30 20 20
   :header-rows: 1

   * - Test ID
     - Module
     - Description
     - SWE.1 ref
     - Expected result
   * - QDX-UT-001
     - workspace_manager
     - Valid workspace opens within 30 s
     - QDX-SWE-001, QDX-SWE-054
     - Ok(Workspace), elapsed ≤ 30 s
   * - QDX-UT-002
     - workspace_manager
     - Missing project ref returns error
     - QDX-SWE-001
     - Err(MissingProjects)
   * - QDX-UT-003
     - workspace_manager
     - Malformed workspace.yaml returns ParseError
     - QDX-SWE-001
     - Err(ParseError)
   * - QDX-UT-004
     - workspace_manager
     - Classic scaffold creates 6 YAML files
     - QDX-SWE-002
     - 6 files present in src/
   * - QDX-UT-005
     - workspace_manager
     - Adaptive scaffold creates 6 YAML files
     - QDX-SWE-002
     - 6 files present in src/
   * - QDX-UT-006
     - workspace_manager
     - BPCT scaffold creates all bl-*.yaml files
     - QDX-SWE-002
     - 6 bl-*.yaml files present
   * - QDX-UT-007
     - workspace_manager
     - Invalid project name returns InvalidName
     - QDX-SWE-002
     - Err(ScaffoldError::InvalidName)
   * - QDX-UT-008
     - workspace_manager
     - Duplicate project name returns AlreadyExists
     - QDX-SWE-002
     - Err(ScaffoldError::AlreadyExists)
   * - QDX-UT-009
     - command_bus
     - Valid addSwc command applies and saves
     - QDX-SWE-008
     - CommandResult { applied: true }
   * - QDX-UT-010
     - command_bus
     - ERROR diagnostic prevents YAML write
     - QDX-SWE-031, QDX-SWE-034
     - CommandResult { applied: false }
   * - QDX-UT-011
     - command_bus
     - Domain mismatch returns BusError
     - QDX-SWE-008
     - Err(BusError::DomainMismatch)
   * - QDX-UT-012
     - wasm_bridge
     - Valid YAML returns empty DiagnosticList
     - QDX-SWE-031
     - DiagnosticList is empty
   * - QDX-UT-013
     - wasm_bridge
     - Missing required field returns Error diagnostic
     - QDX-SWE-031
     - DiagnosticList contains Severity::Error
   * - QDX-UT-014
     - wasm_bridge
     - Validation completes within 500 ms (5000 lines)
     - QDX-SWE-055
     - elapsed ≤ 500 ms
   * - QDX-UT-015
     - wasm_bridge
     - Unknown schema_id returns WASM-001 diagnostic
     - QDX-SWE-031
     - Diagnostic { code: "WASM-001" }
   * - QDX-UT-016
     - diagnostics_panel
     - Duplicate diagnostics are deduplicated
     - QDX-SWE-036
     - List length = unique count
   * - QDX-UT-017
     - diagnostics_panel
     - ERROR items appear before WARNING in output
     - QDX-SWE-036
     - First item severity = Error
   * - QDX-UT-018
     - diagnostics_panel
     - Empty inputs return empty RenderedDiagnostics
     - QDX-SWE-036
     - error_count = warning_count = info_count = 0
   * - QDX-UT-026
     - core::yaml
     - Valid file deserialises correctly
     - QDX-SWE-004
     - Ok(T) with expected field values
   * - QDX-UT-027
     - core::yaml
     - Missing file returns IoError
     - QDX-SWE-004
     - Err(YamlError::IoError)
   * - QDX-UT-028
     - core::yaml
     - Malformed YAML returns ParseError with path
     - QDX-SWE-004
     - Err(ParseError) with file_path set
   * - QDX-UT-029
     - core::yaml
     - Saved file content matches input
     - QDX-SWE-005
     - Loaded value equals saved value
   * - QDX-UT-030
     - core::yaml
     - Temp file cleaned up on write failure
     - QDX-SWE-005
     - No .yaml.tmp file remains
   * - QDX-UT-031
     - core::yaml
     - YAML key order is stable across two saves
     - QDX-SWE-038
     - File byte-identical on re-save
   * - QDX-UT-035
     - classic::validation
     - All runnables mapped returns empty list
     - QDX-SWE-016
     - DiagnosticList is empty
   * - QDX-UT-036
     - classic::validation
     - One unmapped runnable returns one Error
     - QDX-SWE-016
     - DiagnosticList length = 1, code = CLASSIC-VAL-001
   * - QDX-UT-037
     - classic::validation
     - Message contains runnable name and actionable text
     - QDX-SWE-037
     - message contains runnable name and "Add an entry"
   * - QDX-UT-044
     - domain_service
     - Generation refused with ERROR diagnostic
     - QDX-SWE-034
     - Err(GenerationBlocked)
   * - QDX-UT-045
     - domain_service
     - Provenance.json written with tool version
     - QDX-SWE-041
     - provenance.tool_version is non-empty
   * - QDX-UT-046
     - domain_service
     - Identical YAML produces identical ARXML
     - QDX-SWE-038
     - Byte-identical output on two consecutive calls
   * - QDX-UT-062
     - bpct::validation
     - WDG > erase timeout passes VR_007
     - QDX-SWE-069
     - DiagnosticList is empty
   * - QDX-UT-063
     - bpct::validation
     - WDG < erase timeout triggers VR_007 Error
     - QDX-SWE-069
     - Diagnostic { code: "VR_007", severity: Error }
   * - QDX-UT-066
     - bpct::generator
     - TC3xx model produces correct cfg.h macros
     - QDX-SWE-075
     - FBL_FLASH_PAGE_SIZE = 256 in cfg.h
   * - QDX-UT-069
     - lwbsw::validation
     - 10 modules within budget returns empty list
     - QDX-SWE-084
     - DiagnosticList is empty
   * - QDX-UT-070
     - lwbsw::validation
     - ROM overrun returns LWBSW-VAL-001 Error
     - QDX-SWE-084
     - Diagnostic { code: "LWBSW-VAL-001" }
   * - QDX-UT-077
     - lwbsw::generator
     - 10-module model produces 20 source files + report
     - QDX-SWE-087
     - files_written = 21 (20 + report)
   * - QDX-UT-079
     - lwbsw::generator
     - Race conditions in Config Report when detected
     - QDX-SWE-086
     - Report contains race_conditions section


11. SWE.3 Traceability Matrix
==============================

.. note::
   Maps every detailed design element (module, function, data structure)
   to the SWE.1 requirement it realises and the SWE.4 unit test
   that verifies it.

.. list-table::
   :widths: 22 18 35 15 10
   :header-rows: 1

   * - Design element
     - Module / crate
     - Realises SWE.1
     - SWE.4 unit test
     - Status
   * - Workspace open + timeout
     - workspace_manager
     - QDX-SWE-001, QDX-SWE-054
     - QDX-UT-001 to 003
     - Draft
   * - Project scaffold (all stacks)
     - workspace_manager
     - QDX-SWE-002, QDX-SWE-003
     - QDX-UT-004 to 008
     - Draft
   * - Command Bus execute
     - command_bus
     - QDX-SWE-008, QDX-SWE-029, QDX-SWE-031, QDX-SWE-034
     - QDX-UT-009 to 011
     - Draft
   * - WASM validateYaml
     - wasm_bridge
     - QDX-SWE-031, QDX-SWE-055, QDX-SWE-060
     - QDX-UT-012 to 015
     - Draft
   * - Diagnostics merge + render
     - diagnostics_panel
     - QDX-SWE-036, QDX-SWE-037
     - QDX-UT-016 to 018
     - Draft
   * - Wizard step validation
     - wizard
     - QDX-SWE-094, QDX-SWE-098, QDX-SWE-101
     - QDX-UT-019 to 025
     - Draft
   * - YAML load / atomic_save
     - core::yaml
     - QDX-SWE-004, QDX-SWE-005, QDX-SWE-038
     - QDX-UT-026 to 031
     - Draft
   * - Validation rule engine
     - core::validation
     - QDX-SWE-031, QDX-SWE-032, QDX-SWE-037
     - QDX-UT-032 to 034
     - Draft
   * - Classic unmapped runnable rule
     - classic::validation
     - QDX-SWE-015, QDX-SWE-016
     - QDX-UT-035 to 037
     - Draft
   * - Classic validation rule set
     - classic::validation
     - QDX-SWE-009 to 016
     - QDX-UT-035 to 037
     - Draft
   * - Adaptive validation rule set
     - adaptive::validation
     - QDX-SWE-017 to 028
     - TBD
     - Draft
   * - OperationPlan apply + rollback
     - core::ops
     - QDX-SWE-008, QDX-SWE-047, QDX-SWE-048
     - QDX-UT-038 to 040
     - Draft
   * - Domain Service load_workspace
     - domain_service
     - QDX-SWE-001, QDX-SWE-033, QDX-SWE-035, QDX-SWE-054
     - QDX-UT-041 to 043
     - Draft
   * - Domain Service generate
     - domain_service
     - QDX-SWE-034, QDX-SWE-038, QDX-SWE-039, QDX-SWE-041
     - QDX-UT-044 to 046
     - Draft
   * - ARXML Gateway importArxml
     - artop_service
     - QDX-SWE-040, QDX-SWE-042, QDX-SWE-062
     - QDX-UT-047 to 049
     - Draft
   * - ARXML Gateway generateArxml
     - artop_service
     - QDX-SWE-038, QDX-SWE-039, QDX-SWE-041
     - QDX-UT-050 to 052
     - Draft
   * - Intent Router route
     - intent_router
     - QDX-SWE-047, QDX-SWE-050, QDX-SWE-051, QDX-SWE-077 to 079
     - QDX-UT-053 to 056
     - Draft
   * - Audit logger record
     - audit_logger
     - QDX-SWE-052
     - QDX-UT-057 to 059
     - Draft
   * - MCU defaults table
     - bpct::mcu_defaults
     - QDX-SWE-063, QDX-SWE-098
     - QDX-UT-060 to 061
     - Draft
   * - BPCT VR_007 watchdog rule
     - bpct::validation
     - QDX-SWE-069, QDX-SWE-074
     - QDX-UT-062 to 065
     - Draft
   * - BPCT VR_NNN rule set
     - bpct::validation
     - QDX-SWE-066, QDX-SWE-069 to 074
     - QDX-UT-062 to 065
     - Draft
   * - BPCT C header generator
     - bpct::generator
     - QDX-SWE-075, QDX-SWE-076
     - QDX-UT-066 to 068
     - Draft
   * - LW-BSW resource budget rule
     - lwbsw::validation
     - QDX-SWE-084, QDX-SWE-090
     - QDX-UT-069 to 071
     - Draft
   * - LW-BSW ICC-2 conformance rule
     - lwbsw::validation
     - QDX-SWE-090
     - QDX-UT-072 to 073
     - Draft
   * - LW-BSW scheduling map
     - lwbsw::scheduling
     - QDX-SWE-085, QDX-SWE-086
     - QDX-UT-074 to 076
     - Draft
   * - LW-BSW header + Config Report gen
     - lwbsw::generator
     - QDX-SWE-086, QDX-SWE-087
     - QDX-UT-077 to 079
     - Draft


12. Open Issues and TBDs
=========================

.. list-table::
   :widths: 15 50 20 15
   :header-rows: 1

   * - Issue ID
     - Description
     - Owner
     - Target date
   * - TBD-SDD-001
     - Define full function specifications for the Adaptive designer
       modules (A1–A6 canvas, sync, cross-file validation triggers).
       Depends on TBD-SWA-001 (Domain Service API surface).
     - IDE Layer Lead
     - 2026-05-15
   * - TBD-SDD-002
     - Define all ``adaptive::validation`` unit tests (QDX-UT-NNN
       series for ADAPTIVE-VAL-001 through 006). Blocked on
       ``adaptive::model`` struct definitions being finalised.
     - Adaptive Domain Lead
     - 2026-05-30
   * - TBD-SDD-003
     - Specify ``bpct::*`` and ``lwbsw::*`` crate structure in full,
       pending confirmation from TBD-SWA-003 that they follow the
       Classic domain crate pattern.
     - Rust Domain Platform Lead
     - 2026-05-15
   * - TBD-SDD-004
     - Define the LW-BSW DEXT/DBC import module
       (``lwbsw::import::from_dext`` and ``from_dbc``) including
       field-mapping rules and lossy-conversion warning catalogue.
     - LW-BSW Lead
     - 2026-06-01
   * - TBD-SDD-005
     - Specify the S-Core detailed design (``score::model``,
       ``score::validation``, ``score::ops``) once TBD-SWA-005 is
       resolved and S-Core crate structure is confirmed.
     - S-Core Integration Lead
     - 2026-07-01
   * - TBD-SDD-006
     - Define complete function specifications for
       ``core::gql_client`` — the generated GraphQL client. Depends on
       TBD-SWA-002 (GraphQL SDL publication).
     - ARXML Gateway Lead
     - 2026-05-15
   * - TBD-SDD-007
     - Specify ``lwbsw::import::preview`` — the DEXT/DBC import preview
       function used by the project creation wizard to show which
       elements will map successfully vs which will be flagged as
       WARNING (QDX-SWE-099).
     - LW-BSW Lead / Wizard Lead
     - 2026-06-01


.. _sdd_changelog:

13. Changelog
==============

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
     - Initial SWE.3 draft derived from QDX-SWA-DOC-001 (SWE.2) and
       QDX-SWE-DOC-001 (SWE.1). Covers all six SDD child documents:
       IDE Layer (Section 4), Rust Domain Platform (Section 5),
       ARXML Gateway (Section 6), Qorix Agent/MCP (Section 7),
       BPCT subsystem (Section 8), LW-BSW subsystem (Section 9).
       Defines 79 unit tests (QDX-UT-001 to QDX-UT-079), 3 shared
       data structures, 15 public function specifications with full
       pre/postconditions, algorithms and error cases, 4 Mermaid
       module decomposition diagrams, full SWE.3 traceability matrix
       mapping all 101 SWE.1 requirements to design elements and
       SWE.4 unit tests, and 7 open TBDs for items blocked on
       upstream architecture decisions.


----

*This document is version-controlled in Git at*
``docs/sdd/platform/sw_detailed_design.rst``.
*Authoritative version is HEAD of* ``main``.
*All changes require a PR with minimum two approvals from CODEOWNERS.
Function-level changes require the owning crate lead as a required reviewer.*
