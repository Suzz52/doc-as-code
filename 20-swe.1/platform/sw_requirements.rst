.. ============================================================
.. QORIX DEVELOPER — Software Requirements Specification
.. ASPICE: SWE.1 
.. Derived from: QDX-SRS-001 (SYS.2), Qorix Developer C4
..               Architecture, Middleware Stakeholders
.. ============================================================

.. _sw_requirements:

========================================================
Software Requirements Specification
========================================================

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Document ID**
     - QDX-SWE-DOC-001
   * - **Product line**
     - Platform — Qorix Developer (Classic + Adaptive AUTOSAR + Bootloader)
   * - **Component**
     - Qorix Developer Platform — all subsystems
   * - **Version**
     - 0.1.0
   * - **Status**
     - Draft
   * - **Owner**
     - Qorix Developer Engineering Team
   * - **Approved by**
     - TBD — Approval pending
   * - **ASPICE process**
     - SWE.1 — Software Requirements Analysis
   * - **Parent SYS doc**
     - QDX-SRS-001 — System Requirements Specification (SYS.2)
   * - **Jira epic**
     - QDX-EPIC-PLATFORM-SWEREQ
   * - **Git path**
     - ``docs/20-swe.1/platform/sw_requirements.rst``
   * - **Changelog**
     - See :ref:`swe_changelog`

----

.. contents:: Table of contents
   :depth: 3
   :local:

----


1. Purpose and Scope
====================

This document specifies the software requirements for the Qorix Developer
platform. It is fully derived from the system requirements in
**QDX-SRS-001** (SYS.2) and is informed by the Qorix Developer C4
architecture description and the Classic AUTOSAR Designer functional
mock-up.

The platform comprises five major software subsystems:

- **IDE Layer** — VS Code Extension and Theia Desktop/Web IDE, including
  six domain-specific Classic AUTOSAR designers (C1–C6), Adaptive
  designers, WASM bridge, diagnostics panel and AI Chat Panel.
- **Rust Domain Platform** — ``qorix_core`` crate tree compiled to three
  targets: HTTP/gRPC domain service, WASM module (``qorix_core_wasm``),
  and CLI binary (``qorix_cli``).
- **ARXML Gateway** — Spring Boot + ARTOP service exposing a GraphQL API
  as the exclusive ARXML import/export boundary.
- **Qorix Agent (MCP Layer)** — AI orchestration layer routing natural
  language intent to structured Rust tool operations via MCP.
- **Config-as-Code model** — six YAML files per Adaptive project, YAML
  files per Classic designer tab, as the source of truth committed to Git.

Software requirements below are numbered ``QDX-SWE-NNN``, directly
corresponding to the ``QDX-SWE-NNN`` column in the SYS.2 traceability
matrix.


2. Relationship to Parent Documents
=====================================

.. mermaid::

   flowchart TD
     SYS["SYS.2 System Requirements\nQDX-SRS-001"]
     SWE["SWE.1 SW Requirements\nThis document · QDX-SWE-DOC-001"]
     SWA["SWE.2 SW Architecture\nQDX-SWA-DOC-001 (TBD)"]
     SDD_RUST["SWE.3 Detailed Design\nRust Domain Platform\nQDX-SDD-RUST-001"]
     SDD_IDE["SWE.3 Detailed Design\nIDE Layer\nQDX-SDD-IDE-001"]
     SDD_GW["SWE.3 Detailed Design\nARXML Gateway\nQDX-SDD-GW-001"]
     SDD_MCP["SWE.3 Detailed Design\nQorix Agent / MCP\nQDX-SDD-MCP-001"]
     TEST["SWE.6 Qualification Tests\nJira Test Cases (QDX-QT-NNN)"]

     SYS -->|"derives"| SWE
     SWE -->|"constrains"| SWA
     SWA -->|"constrains"| SDD_RUST
     SWA -->|"constrains"| SDD_IDE
     SWA -->|"constrains"| SDD_GW
     SWA -->|"constrains"| SDD_MCP
     SWE <-->|"verified by"| TEST


3. Terms, Acronyms and Abbreviations
======================================

.. glossary::

   ADC
      Analog-to-Digital Converter — peripheral hardware abstracted by
      the IOHAB module in the LW-BSW and Classic BSW stacks.

   AI-Assist
      Qorix Developer capability providing domain-aware, explainable
      engineering assistance through the Qorix Agent. Activated per
      designer domain when the corresponding domain extension is
      installed. All suggestions are presented as an OperationPlan
      requiring explicit engineer acceptance before any YAML file
      is modified.

   A1–A6
      Six Adaptive AUTOSAR designer tabs in Qorix Developer:
      A1 Application & Service, A2 Communication, A3 Machine Design,
      A4 Platform Services, A5 Execution Management, A6 Deployment.

   Application Manifest
      AUTOSAR Adaptive artefact (``ApplicationManifest.arxml``)
      describing the executable applications, their processes and
      service dependencies. Generated from the A1 and A5 designer
      configuration in Qorix Developer.

   ara::com
      AUTOSAR Adaptive communication API — the service-oriented
      middleware API for inter-application communication on the
      Adaptive Platform, supporting SOME/IP and DDS transports.

   ara::log
      AUTOSAR Adaptive logging framework — centralised log output
      service configured in the A4 Platform Services designer with
      per-logger name, level and output target settings.

   ara::per
      AUTOSAR Adaptive Persistency service — key-value storage for
      application data, configured in the A4 designer with storage
      area count and schema definitions.

   ara::phm
      AUTOSAR Adaptive Platform Health Management — supervision
      and health monitoring service configured in the A4 designer
      with health channel definitions.

   ara::tsync
      AUTOSAR Adaptive Time Synchronisation service — network time
      protocol integration for distributed Adaptive systems,
      configured in the A4 Platform Services designer.

   ARXML
      AUTOSAR XML — the schema-defined exchange format for AUTOSAR
      engineering models, consumed and produced exclusively via
      the ARTOP-based ARXML Gateway in Qorix Developer.

   ARTOP
      AUTOSAR Tool Platform — Eclipse-based framework providing the
      canonical AUTOSAR metamodel and ARXML read/write capability.
      Used by the Qorix Developer ARXML Gateway (Spring Boot +
      ARTOP) as the sole path for ARXML import and export.

   ASPICE
      Automotive SPICE (Software Process Improvement and Capability
      dEtermination) — process assessment framework for automotive
      software suppliers. Qorix Developer is designed to produce
      ASPICE-compliant evidence artefacts at SWE.1 through SYS.5
      as a natural byproduct of the engineering workflow.

   AUTOSAR
      AUTomotive Open System ARchitecture — standardised software
      framework for ECU software development. Qorix Developer
      supports Classic AUTOSAR (BSW, RTE, COM stack) and Adaptive
      AUTOSAR (service-oriented, ara::com, manifests).

   BD1–BD6
      Six Bootloader (BPCT) designer tabs in Qorix Developer:
      BD1 Project & MCU, BD2 Communication, BD3 Memory & Flash,
      BD4 Core & Diagnostics, BD5 Timing & Hardware,
      BD6 Crypto & Security.

   BPCT
      Bootloader Parameters Configurator Tool — the Qorix Developer
      subsystem for authoring, validating and generating Flash
      Bootloader (FBL) configuration artefacts across six YAML
      source files and six BD designers.

   BSW
      Basic Software — the standardised lower layers of the AUTOSAR
      Classic Platform stack, including OS, COM, diagnostics, memory
      and hardware abstraction modules.

   C1–C6
      Six Classic AUTOSAR designer tabs in Qorix Developer:
      C1 SWC & Interface, C2 Signals & ComStack, C3 ECU & BSW,
      C4 OS & Scheduling, C5 Memory & NvM, C6 RTE & Mapping.

   CAN
      Controller Area Network — mandatory communication bus protocol
      for Classic AUTOSAR and Bootloader (BPCT) projects.
      Configured in the C2 designer (Classic) and BD2 designer
      (BPCT).

   CAN-FD
      CAN with Flexible Data-rate — higher-bandwidth variant of CAN
      (ISO 11898-1) supporting data phases up to 8 Mbit/s.
      Optional in BPCT projects; not supported in LW-BSW.

   CanIf
      CAN Interface — AUTOSAR Classic BSW module providing hardware
      abstraction for the CAN controller and routing PDUs to the
      COM stack. Included in both Full Classic and LW-BSW stacks.

   CDD
      Complex Device Driver — AUTOSAR Classic BSW module containing
      ECU-specific or application-specific implementations that
      cannot be covered by standardised BSW modules, including
      I2C, SPI, sensor and actuator interfaces.

   CDD (LW-BSW)
      In the LW-BSW context, the CDD module provides application-
      specific services including gateway functionality and
      communication interface handling for I2C, SPI and similar
      peripherals.

   COM
      Communication module — AUTOSAR Classic BSW module managing
      signal packing, unpacking, data conversion, periodic
      transmission, deadline monitoring and safety callbacks.
      One of the ten LW-BSW modules.

   Config-as-Code
      Development paradigm where all engineering configuration is
      expressed in human-readable YAML files committed to version
      control. The foundational principle of Qorix Developer —
      every parameter change is a Git commit, every release is a
      tagged SHA.

   Config Insight
      LW-BSW-specific AI-Assist capability providing on-demand
      analytical responses covering scheduling assessment, resource
      budget evaluation, race condition explanation and safety
      violation guidance across the full 10-module configuration.

   Config Report
      Structured output file generated by the LW-BSW pipeline
      alongside the C header files. Contains: OS scheduling map,
      per-module ROM/RAM/CPU resource budget versus target KPIs,
      static race condition detections, and safety violation flags.

   Core Affinity
      Assignment of a process or runnable to one or more specific
      CPU cores on a target machine. Configured in the A5 Execution
      designer (Adaptive) and validated against the core count
      declared in the A3 Machine designer.

   DCM
      Diagnostic Communication Manager — AUTOSAR Classic BSW module
      implementing the UDS protocol (ISO 14229) session and service
      handling. One of the 10 LW-BSW modules (as "Diag").

   DDS
      Data Distribution Service — publish-subscribe middleware
      protocol used as an alternative to SOME/IP in AUTOSAR
      Adaptive communication. Configured in the A2 Communication
      designer as a provider transport option.

   DEM
      Diagnostic Event Manager — AUTOSAR Classic BSW module managing
      the detection, storage and retrieval of Diagnostic Trouble
      Codes (DTCs) in non-volatile memory.

   DEXT
      Data EXTraction file — XML-format ECU description file
      exported from AUTOSAR toolchains (e.g. Tresos, DaVinci).
      Used as an import source in LW-BSW project creation and
      LW-BSW project scaffolding to pre-populate the YAML
      configuration baseline.

   DBC
      Database CAN file — legacy non-AUTOSAR format describing CAN
      network signals, messages and nodes. Supported as an import
      source in LW-BSW project creation and the BPCT BD2 designer.

   DIO
      Digital Input/Output — peripheral type abstracted by the
      IOHAB module in LW-BSW and AUTOSAR Classic.

   DTC
      Diagnostic Trouble Code — standardised fault identifier stored
      in non-volatile memory and retrievable via UDS diagnostic
      services. Managed by the DEM module.

   Domain Extension
      Installable Qorix Developer extension that activates the
      designer set and MCP tool registry for a specific stack
      domain. Classic extension activates C1–C6 and Classic
      AI-Assist tools; Adaptive extension activates A1–A6 and
      Adaptive AI-Assist tools; BPCT extension activates BD1–BD6
      and BPCT AI-Assist tools.

   ECU
      Electronic Control Unit — the embedded hardware and software
      unit that is the primary authoring and generation target of
      Qorix Developer Classic and LW-BSW projects.

   EMM
      ECU Mode Manager — LW-BSW and AUTOSAR Classic BSW module
      responsible for ECU mode transitions (e.g. Normal, Sleep,
      Reset) and managing the conditions for each transition.

   Execution Manifest
      AUTOSAR Adaptive artefact (``ExecutionManifest.arxml``)
      describing process scheduling, resource groups and startup
      configuration. Generated from A5 Execution designer
      configuration in Qorix Developer.

   FBL
      Flash Bootloader — embedded software responsible for receiving
      and flashing firmware updates over a communication bus (CAN,
      CAN-FD, LIN). Configured using the Qorix Developer BPCT
      subsystem (BD1–BD6 designers).

   FBL_PROJECT_NAME
      Macro identifier for the bootloader project, generated in
      ``cfg.h`` from the BD1 designer. Validated as uppercase
      alphanumeric with underscores in the project creation wizard.

   GraphQL
      Query and mutation API technology used by the ARXML Gateway
      to expose AUTOSAR model read and write operations to the
      Rust domain layer via the ``core::gql_client`` generated
      Rust client.

   gRPC
      Remote Procedure Call protocol used between the IDE layer
      and the Rust Domain Service for heavy semantic validation
      and model operations requiring the full loaded domain model.

   HSM
      Hardware Security Module — dedicated security processor on
      the target ECU used for cryptographic key storage and
      operations. The key store address region is defined in the
      BD3 Memory designer and validated against BD6 security
      configuration.

   ICC-2
      Implementation Conformance Class 2 — partial AUTOSAR Classic
      conformance level. Implements a meaningful subset of the
      AUTOSAR standard with a thin RTE and OSEK SC-1 operating
      system. Approximately 10 BSW modules and 600 configuration
      parameters. Target for the Qorix LW-BSW stack.

   ICC-3
      Implementation Conformance Class 3 — full AUTOSAR Classic
      conformance level. Implements the complete AUTOSAR standard
      including full RTE, all OS features, 46+ BSW modules and
      approximately 5,600 configuration parameters.

   Intent Router
      Component of the Qorix Agent MCP layer that determines the
      active stack domain (Classic, Adaptive, or BPCT) from the
      open designer context and routes user prompts to the
      correct domain-specific MCP tool set.

   IOHAB
      I/O Hardware Abstraction — BSW module providing configurable
      interfaces to initialise and control peripheral I/O devices
      including DIO, ADC, ICU and PWM drivers. One of the 10
      LW-BSW modules.

   ISO 14229
      UDS (Unified Diagnostic Services) specification — defines
      the diagnostic communication protocol implemented by the
      DCM/Diag module. The BD4 Core & Diagnostics designer
      configures the UDS session state machine per this standard.

   ISO 15765-2
      CAN Transport Protocol specification — defines segmentation
      and flow control for diagnostic messages over CAN. Implemented
      by the CanTp BSW module.

   LIN
      Local Interconnect Network — secondary communication bus
      protocol (ISO 17987). Optional in LW-BSW projects and BPCT
      multi-channel configurations; not supported as a primary
      channel in BPCT.

   LLM
      Large Language Model — external AI model (e.g. OpenAI GPT
      or self-hosted equivalent) used by the Qorix Agent to
      interpret natural language engineering prompts and return
      structured change proposals. Never writes YAML directly;
      all changes are mediated through the OperationPlan and
      user acceptance gate.

   LSP
      Language Server Protocol — standard protocol providing
      syntax, schema and semantic editing assistance (completion,
      go-to-definition, find-references, rename) in text-based
      editors. Backed by the ``core::yaml`` and
      ``core::validation`` crates in Qorix Developer.

   LW-BSW
      Light Weight Basic Software — Qorix-developed AUTOSAR
      Classic BSW stack targeting small ECUs with tight memory
      and power constraints. ICC-2 conformance, 10 BSW modules,
      ~600 configuration parameters, ~150 KB ROM target,
      ~30 KB RAM target, OSEK SC-1 operating system.

   Machine Manifest
      AUTOSAR Adaptive artefact (``MachineManifest.arxml``)
      describing the target machine hardware, network interfaces,
      CPU cores and memory regions. Generated from the A3 Machine
      designer configuration in Qorix Developer.

   MCP
      Model Context Protocol — structured protocol used by the
      Qorix Agent to expose tool endpoints to the LLM. Each
      domain (Classic, Adaptive, BPCT, LW-BSW) registers its
      own set of MCP tools in the Tool Registry.

   MCAL
      Microcontroller Abstraction Layer — lowest BSW layer
      providing hardware-specific driver implementations for
      peripherals. ECU-hardware-dependent in both Classic and
      LW-BSW architectures.

   MCU
      Microcontroller Unit — the target processor for Classic,
      LW-BSW and Bootloader projects. MCU family selection in
      the project creation wizard drives hardware-dependent
      defaults (flash page size, SPI clock, timer resolution)
      across all relevant designers.

   NM
      Network Management — BSW module implementing the ECU
      network management protocol (OSEK NM or AUTOSAR NM).
      One of the 10 LW-BSW modules; ECU-specific implementation
      selectable at project creation.

   NvM
      Non-Volatile Memory manager — AUTOSAR Classic BSW module
      managing the storage and retrieval of data in EEPROM or
      flash memory. Configured in the C5 Memory & NvM designer
      (Classic) or the NVRAM section of the LW-BSW configuration.

   NvM Block
      A defined unit of non-volatile storage with a block ID,
      size, CRC type and management type (Standard, Redundant,
      Dataset). Defined in the C5 designer (Classic), the BD3
      designer (BPCT) and the LW-BSW NVRAM module configuration.

   OperationPlan
      Structured set of typed model mutation operations (add,
      update, delete at a specific YAML path) proposed by the
      Qorix Agent for engineer review. No YAML file is modified
      until the engineer explicitly accepts the OperationPlan.
      The acceptance event is recorded in the audit log.

   OSEK SC-1
      OSEK/VDX Scalability Class 1 — the minimal OS conformance
      class providing priority-based preemptive scheduling on a
      single core without memory protection. The operating system
      model used by the LW-BSW stack.

   PDU
      Protocol Data Unit — a unit of data transferred over a
      communication bus. In Classic AUTOSAR and LW-BSW, I-PDUs
      (Interaction Layer PDUs) carry signals between SWCs via
      the COM stack. Configured in the C2 designer (Classic)
      and the BD2 designer (BPCT).

   P-Port
      Provide Port — an AUTOSAR Classic SWC port that provides
      (sends) data or services to other SWCs via an interface.

   PWM
      Pulse-Width Modulation — peripheral type abstracted by the
      IOHAB module in LW-BSW and AUTOSAR Classic.

   R-Port
      Require Port — an AUTOSAR Classic SWC port that requires
      (receives) data or services from other SWCs via an interface.

   RTE
      Runtime Environment — auto-generated middleware layer in
      AUTOSAR Classic connecting SWC ports to COM signals, OS
      tasks and NvM blocks. Configured via the C6 RTE & Mapping
      designer. In LW-BSW, a thin AUTOSAR-compliant RTE is used
      with a reduced set of supported port communication patterns.

   RSA2048
      RSA public-key cryptographic algorithm with 2048-bit key
      length — the recommended signature algorithm for BPCT
      secure boot configuration. RSA1024 is flagged as WARNING
      (VR_013) by the BPCT validation engine.

   Rust Domain Service
      The core Qorix Developer backend service — an HTTP/gRPC
      server built from the ``qorix_core`` Rust crate tree.
      Owns the canonical semantic model for Classic and Adaptive
      AUTOSAR, performs cross-file validation, and handles domain
      operations. The same codebase compiles to three targets:
      Domain Service (HTTP/gRPC), WASM module, and CLI binary.

   SecOC
      Secure Onboard Communication — AUTOSAR Classic BSW module
      providing message authentication over the COM stack.
      Referenced in Qorix Developer security configuration
      context.

   Service Instance
      In AUTOSAR Adaptive, a runtime binding of a service
      interface to a specific transport endpoint (SOME/IP port
      or DDS topic) on a specific machine. Configured in the A2
      Communication designer.

   SOME/IP
      Scalable service-Oriented MiddlewarE over IP — the primary
      service discovery and communication protocol for AUTOSAR
      Adaptive. Configured in the A2 Communication designer as
      the default provider transport protocol.

   SWC
      Software Component — a deployable unit in the AUTOSAR
      Classic software architecture with defined ports and
      runnables. Authored in the C1 SWC & Interface designer.

   Template
      A pre-configured project starting point selectable in the
      project creation wizard. Templates pre-populate YAML source
      files with realistic domain-specific defaults for common
      ECU archetypes (e.g. Powertrain Control, Perception
      Pipeline, Secure Boot FBL), reducing initial configuration
      effort.

   Tool Registry
      Component of the Qorix Agent MCP layer that catalogues all
      available MCP tools for each domain (Classic, Adaptive,
      BPCT, LW-BSW). The Intent Router queries the Tool Registry
      to select the correct tool set for the active designer
      context before routing a user prompt.

   UDS
      Unified Diagnostic Services — diagnostic communication
      protocol defined in ISO 14229. Implemented by the DCM/Diag
      module. The BD4 Core & Diagnostics designer configures the
      UDS session state machine (Default, Extended Diagnostic,
      Programming sessions) and Security Unlock sequences.

   VFB
      Virtual Functional Bus — AUTOSAR Classic abstract
      communication medium connecting SWC ports without specifying
      the underlying physical bus. The VFB view is displayed in
      the C1 SWC & Interface designer.

   VR_NNN
      Validation Rule identifier used by the BPCT validation
      engine. Each VR_NNN rule defines a cross-parameter or
      cross-designer constraint. Examples: VR_003 (flash block
      size must be a multiple of MCU page size), VR_007 (watchdog
      timeout must exceed erase timeout when
      DISABLE_DURING_ERASE is FALSE), VR_013 (RSA1024 not
      recommended for automotive secure boot).

   WASM
      WebAssembly — portable binary compilation target allowing
      the Rust domain core (``qorix_core_wasm``) to execute
      directly inside the IDE host (VS Code, Theia) without a
      network call. Enables sub-500 ms in-IDE validation
      latency with results identical to the CI pipeline.

   WdgM
      Watchdog Manager — AUTOSAR Classic BSW module supervising
      software entities and triggering hardware watchdog
      service. Included as a togglable BSW module group in the
      Classic project configuration step.

   Workspace
      The top-level container in Qorix Developer holding one or
      more stack-specific projects under a common root directory.
      Represented as a workspace metadata YAML file. A single
      workspace may contain Classic, Adaptive, Bootloader and
      LW-BSW projects simultaneously.

   YAML
      YAML Ain't Markup Language — the human-readable data
      serialisation format used as the source-of-truth for all
      Qorix Developer project configuration. Every parameter
      change is a line-level text change committable to Git.


4. Software Context and Interfaces
====================================

4.1 Subsystem decomposition
-----------------------------

.. mermaid::

   graph TD
     subgraph IDE ["IDE Layer (VS Code Ext / Theia)"]
       YAML_ED["YAML Editor\nLSP + JSON Schema"]
       DESIGNERS["Visual Designers\nC1-C6 Classic · Adaptive"]
       DIAG["Diagnostics Panel"]
       CMD_BUS["Command Bus"]
       WASM_BRIDGE["WASM Bridge\nvalidateYaml() · planOps()"]
       DS_CLIENT["Domain Service Client\nHTTP / gRPC"]
       AI_PANEL["AI Chat Panel\nMCP Client"]
     end

     subgraph RUST ["Rust Domain Platform"]
       DOMAIN_SVC["Rust Domain Service\nHTTP / gRPC server"]
       CORE_WASM["qorix_core_wasm\nWASM build target"]
       CLI["qorix_cli\nCLI build target"]
       subgraph CORE ["core::* crates"]
         CORE_MODEL["core::model"]
         CORE_YAML["core::yaml"]
         CORE_VAL["core::validation"]
         CORE_OPS["core::ops"]
         CORE_GQL["core::gql_client"]
         CORE_MIG["core::migration"]
       end
       subgraph CLASSIC_CRATES ["classic::* crates"]
         CL_MODEL["classic::model"]
         CL_VAL["classic::validation"]
         CL_OPS["classic::ops"]
         CL_MIG["classic::migration"]
       end
       subgraph ADAPTIVE_CRATES ["adaptive::* crates"]
         AD_MODEL["adaptive::model"]
         AD_VAL["adaptive::validation"]
         AD_OPS["adaptive::ops"]
         AD_MIG["adaptive::migration"]
       end
     end

     subgraph GW ["ARXML Gateway"]
       ARTOP_SVC["Spring Boot + ARTOP"]
       GQL_API["GraphQL API"]
     end

     subgraph MCP_LAYER ["Qorix Agent / MCP Layer"]
       INTENT_ROUTER["Intent Router"]
       TOOL_REG["Tool Registry"]
       CL_TOOLS["Classic MCP Tools"]
       AD_TOOLS["Adaptive MCP Tools"]
     end

     YAML_ED --> WASM_BRIDGE
     DESIGNERS --> CMD_BUS --> WASM_BRIDGE
     WASM_BRIDGE --> CORE_WASM
     WASM_BRIDGE --> DS_CLIENT --> DOMAIN_SVC
     AI_PANEL --> MCP_LAYER --> DOMAIN_SVC
     DOMAIN_SVC --> CORE_GQL --> GQL_API --> ARTOP_SVC
     DIAG --> WASM_BRIDGE

4.2 Key interfaces
-------------------

.. list-table::
   :widths: 22 18 20 40
   :header-rows: 1

   * - Interface
     - From
     - To
     - Protocol / contract
   * - WASM in-IDE validation
     - IDE Layer
     - qorix_core_wasm
     - Direct WASM call: ``validateYaml()``, ``planOps()``
   * - Domain service — semantic ops
     - IDE Layer / Agent
     - Rust Domain Service
     - HTTP/gRPC; structured request/response
   * - ARXML import/export
     - Rust Domain Service
     - ARXML Gateway
     - GraphQL (``core::gql_client`` generated client)
   * - MCP tool calls
     - Qorix Agent
     - Rust Domain Service
     - MCP structured tool protocol
   * - LLM backend
     - Qorix Agent
     - OpenAI / self-hosted LLM
     - HTTPS / OpenAI-compatible REST
   * - CI invocation
     - CI/CD pipeline
     - qorix_cli
     - Shell / process — same Rust domain code, headless


5. Software Requirements
==========================

.. admonition:: Requirement writing rules

   - Every ``QDX-SWE-NNN`` must declare a ``:parent:`` referencing the
     ``QDX-SYS-NNN`` it derives from, or ``:parent: INTERNAL`` with
     rationale.
   - Use **SHALL** / **SHOULD** / **MAY** per RFC 2119.
   - One atomic, independently testable statement per block.
   - IDs are permanent — retired requirements get ``:status: Deprecated``.


5.1 Workspace and project management
--------------------------------------

.. req:: Multi-stack workspace initialisation
   :id: QDX-SWE-001
   :parent: QDX-SYS-001
   :status: Draft
   :priority: High
   :rationale: Derived from unified multi-stack workspace support. The
     software must create and maintain a workspace container that holds
     projects for all four supported stacks under a common root.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-001

   The workspace manager **SHALL** initialise a workspace root directory
   containing project subdirectories for one or more of the supported
   stack types (Classic, Adaptive, Bootloader, Performance) and persist
   a workspace metadata file recording the declared projects and their
   stack types.

.. req:: Per-stack project scaffolding
   :id: QDX-SWE-002
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: Derived from project scaffolding. The software must create
     a correctly structured project on demand for each supported stack.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-002

   The project scaffolding module **SHALL** create the full directory
   structure, mandatory YAML source files and metadata files for a new
   project of the requested stack type. For a Classic AUTOSAR project
   this **SHALL** include at minimum: ``swc-design.yaml``,
   ``signals-comstack.yaml``, ``ecu-bsw.yaml``, ``os-scheduling.yaml``,
   ``mem-nvram.yaml``, and ``rte-mapping.yaml``.

.. req:: Source/output directory separation
   :id: QDX-SWE-003
   :parent: QDX-SYS-044
   :status: Draft
   :priority: High
   :rationale: Config-as-Code discipline requires YAML source files and
     generated ARXML/report outputs to be in distinct locations to
     prevent accidental overwrites and enable clean Git diffs.
   :verification: SWE.6 qualification test | Inspection
   :jira: QDX-SWE-006

   The project structure **SHALL** separate user-authored YAML source
   files from generated output artefacts (ARXML, reports, logs) using
   distinct directory paths, such that generated content is never
   co-located with source content.

.. req:: Version-control-friendly YAML persistence
   :id: QDX-SWE-004
   :parent: QDX-SYS-019
   :status: Draft
   :priority: High
   :rationale: All project content must be committable to Git with
     meaningful line-level diffs for review and merge workflows.
   :verification: Inspection | Analysis
   :jira: QDX-SWE-004

   All user-authored configuration **SHALL** be persisted as UTF-8
   encoded YAML files with deterministic key ordering within each file,
   such that a logically unchanged model round-trips to a byte-identical
   YAML representation.

.. req:: Atomic save with integrity protection
   :id: QDX-SWE-005
   :parent: QDX-SYS-033
   :status: Draft
   :priority: High
   :rationale: Derived from configuration integrity protection. Partial
     writes during a crash must not corrupt a previously valid YAML file.
   :verification: SWE.6 qualification test — fault injection
   :jira: QDX-SWE-005

   The file persistence layer **SHALL** write YAML content using an
   atomic write pattern (write to a temporary file, then rename) such
   that an interrupted write leaves the previously committed file intact
   and unmodified.


5.2 Text-based authoring — IDE Layer
--------------------------------------

.. req:: YAML editor with schema-based completion
   :id: QDX-SWE-006
   :parent: QDX-SYS-003
   :status: Draft
   :priority: High
   :rationale: Derived from text-based authoring support. The YAML editor
     must provide structural guidance through schema-driven completion
     and live error indication.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-006

   The YAML editor **SHALL** provide JSON Schema-based autocompletion,
   required-field highlighting and inline error squiggles for all
   supported platform YAML formats, sourced from the active product
   schema version.

.. req:: Language server protocol integration
   :id: QDX-SWE-007
   :parent: QDX-SYS-029
   :status: Draft
   :priority: High
   :rationale: Derived from language-service integration. LSP is the
     standard mechanism for editor diagnostics and navigation.
   :verification: SWE.6 qualification test — interface conformance
   :jira: QDX-SWE-007

   The IDE Layer **SHALL** expose YAML editing assistance — including
   go-to-definition, find-all-references, hover documentation and
   rename symbol — through a Language Server Protocol implementation
   backed by the ``core::yaml`` and ``core::validation`` crates.

.. req:: Localised atomic model mutations
   :id: QDX-SWE-008
   :parent: QDX-SYS-013
   :status: Draft
   :priority: Medium
   :rationale: Derived from localized atomic edits. Designer interactions
     and AI suggestions produce fine-grained mutations that must not
     rewrite unrelated YAML content.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-008

   The ``core::ops`` operation model **SHALL** represent each
   configuration change as a path-targeted add, update or delete
   operation such that applying the operation modifies only the
   specified YAML path and leaves all sibling and parent elements
   unchanged.


5.3 Visual designers — Classic AUTOSAR (C1–C6)
------------------------------------------------

.. req:: C1 — SWC and interface designer
   :id: QDX-SWE-009
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: The SWC designer (C1) is the primary authoring surface for
     Classic AUTOSAR component topology. Derived from designer-based
     authoring support.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-038

   The C1 SWC & Interface designer **SHALL** allow users to create,
   view and edit AUTOSAR Classic Software Components (Atomic, Service,
   Composition), their ports (P-Port, R-Port), port interfaces
   (Sender-Receiver, Client-Server) and data elements, with all changes
   persisted to ``swc-design.yaml`` via the ``classic::ops`` operation
   model.

.. req:: C1 — SWC runnable definition
   :id: QDX-SWE-010
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: Runnables are the executable units of Classic SWCs and
     must be definable in the designer with their trigger and timing.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-039

   The C1 designer **SHALL** allow users to define runnables for each
   Atomic SWC, specifying the trigger type (TIMING, INIT, ISR, DATA
   RECEIVED), period in milliseconds for timing-triggered runnables,
   and exclusive area associations. Runnable definitions **SHALL** be
   persisted in ``swc-design.yaml``.

.. req:: C2 — Signals and ComStack designer
   :id: QDX-SWE-011
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: Signal and I-PDU topology must be editable visually and
     kept in sync with ``signals-comstack.yaml``.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-040

   The C2 Signals & ComStack designer **SHALL** allow users to define
   CAN/LIN/Ethernet bus networks, I-PDUs with CAN IDs, cycle times and
   lengths, and signals with bit positions and data types. It **SHALL**
   display the COM stack layer chain (Com → PduR → CanIf → CanDrv) and
   provide a signal-to-I-PDU matrix view. All definitions **SHALL** be
   persisted to ``signals-comstack.yaml``.

.. req:: C3 — ECU and BSW designer
   :id: QDX-SWE-012
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: ECU and BSW module configuration must be manageable
     within the designer with persistence to ``ecu-bsw.yaml``.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-043

   The C3 ECU & BSW designer **SHALL** allow users to configure ECU
   instances and assign BSW modules to them, and **SHALL** persist all
   ECU and BSW configuration to ``ecu-bsw.yaml``.

.. req:: C4 — OS and scheduling designer
   :id: QDX-SWE-013
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: OS task definitions are the target for runnable-to-task
     mapping in C6 and must be authorable in C4.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-008

   The C4 OS & Scheduling designer **SHALL** allow users to define OS
   tasks with names, priorities, periods and activation types (timing,
   event, ISR), and **SHALL** persist OS configuration to
   ``os-scheduling.yaml``.

.. req:: C5 — Memory and NvM designer
   :id: QDX-SWE-014
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: NvM block definitions are required for calibration data
     and fault storage and must be manageable in the designer.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-053

   The C5 Memory & NvM designer **SHALL** allow users to define memory
   devices (Flash, EEPROM) with total size and sector size, and NvM
   blocks with block ID, length in bytes, CRC type (CRC8, CRC16, CRC32),
   management type (Standard, Redundant, Dataset) and RAM block symbol.
   Storage efficiency analysis **SHALL** be computed and displayed.
   All definitions **SHALL** be persisted to ``mem-nvram.yaml``.

.. req:: C6 — RTE and mapping designer
   :id: QDX-SWE-015
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: The RTE mapping designer is the final integration surface
     connecting runnables, ports, signals and NvM blocks before ARXML
     export. Completeness is a prerequisite for valid ARXML generation.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-041

   The C6 RTE & Mapping designer **SHALL** allow users to map runnables
   to OS tasks, map SWC P-Ports and R-Ports to communication signals,
   and associate NvM blocks to SWC RAM symbols. It **SHALL** display
   ARXML export readiness as a per-designer (C1–C5) completion status
   and a blocking error list. All mapping definitions **SHALL** be
   persisted to ``rte-mapping.yaml``.

.. req:: Unmapped element detection in C6
   :id: QDX-SWE-016
   :parent: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: Unmapped runnables and ports are a primary source of
     incomplete ARXML exports. They must be surfaced as errors before
     generation is permitted.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-047

   The ``classic::validation`` crate **SHALL** detect and report as
   ERROR any runnable that has no task assignment in ``rte-mapping.yaml``
   and any P-Port or R-Port that has no mapped signal, referencing the
   affected SWC name, runnable or port name and the source YAML path.


5.4 Visual designers — Adaptive AUTOSAR
-----------------------------------------

.. req:: A1 — Application and service designer
   :id: QDX-SWE-017
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: The A1 designer is the primary authoring surface for
     AUTOSAR Adaptive service interfaces. It defines the service
     contract — methods, events and data types — before any deployment
     or communication binding is configured.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-048

   The A1 Application & Service designer **SHALL** allow users to
   create, view and edit Adaptive AUTOSAR services with the following
   attributes: service name, namespace, version (major.minor.patch),
   methods (name, input parameters, return type) and events (name,
   event data type). All definitions **SHALL** be persisted to
   ``application-design.yaml`` via the ``adaptive::ops`` operation model.
   The designer **SHALL** display a flat table view listing all services
   with their method and event counts, and a service graph view showing
   cross-service consumer references.

.. req:: A1 — Service cross-reference tracking
   :id: QDX-SWE-018
   :parent: QDX-SYS-008
   :status: Draft
   :priority: High
   :rationale: Services in an Adaptive project reference each other
     through consumer bindings in A2. The designer must surface how
     many consumers depend on each service to support safe refactoring.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-044

   The A1 designer **SHALL** display for each service the count of
   consumer bindings that reference it across the ``communication.yaml``
   of the same project, derived by the ``adaptive::validation`` crate,
   and **SHALL** surface this count in the service properties panel as
   a cross-reference indicator.

.. req:: A2 — Communication and service instance designer
   :id: QDX-SWE-019
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: The A2 designer manages the runtime service binding
     topology — which machine provides which service, which machine
     consumes it, the transport protocol and QoS parameters. This is
     the AUTOSAR Adaptive equivalent of the Classic ComStack designer.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-004

   The A2 Communication designer **SHALL** allow users to define and
   edit service provider instances and service consumer instances with
   the following attributes:

   - **Provider instance**: instance name, referenced service (from
     ``application-design.yaml``), transport protocol (SOME/IP or DDS),
     port number (for SOME/IP), assigned machine, and activation status.
   - **Consumer instance**: instance name, required service reference,
     bound provider instance, assigned machine, and binding status.
   - **QoS configuration per provider**: reliability mode (Reliable/TCP
     or Unreliable/UDP), latency budget in milliseconds, maximum message
     size in KB, and durability policy.

   All definitions **SHALL** be persisted to ``communication.yaml``.
   The designer **SHALL** provide both a binding graph view and a flat
   table view for providers and consumers.

.. req:: A2 — Service binding completeness validation
   :id: QDX-SWE-020
   :parent: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: An unbound consumer instance means a required service
     has no reachable provider at runtime — a deployment error that
     must be detected before ARXML export.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-052

   The ``adaptive::validation`` crate **SHALL** verify that every
   consumer instance declared in ``communication.yaml`` has a resolved
   binding to a provider instance for the same service reference. Any
   consumer instance with no bound provider **SHALL** be reported as
   an ERROR diagnostic referencing the consumer instance name, the
   required service name and the ``communication.yaml`` key path.

.. req:: A3 — Machine design designer
   :id: QDX-SWE-021
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: Machine definitions specify the target hardware topology
     on which applications and services are deployed. CPU architecture,
     core count, RAM and Flash must be definable to drive resource
     constraint checking in A5 and A6.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-021

   The A3 Machine designer **SHALL** allow users to define machines
   with the following attributes: machine name, CPU architecture
   (e.g. ARM A78, ARM Cortex-R52, ARM A53), core count, CPU frequency
   in GHz, RAM capacity in GB, and Flash storage capacity in GB. It
   **SHALL** display a network topology view showing Ethernet links
   between machines, a resource utilisation summary per machine (CPU
   load percentage, RAM usage percentage) derived from the deployment
   and execution configuration, and a flat table view of all machines
   with their hardware attributes and status. All definitions **SHALL**
   be persisted to ``machine-design.yaml``.

.. req:: A3 — Disabled core reference detection
   :id: QDX-SWE-022
   :parent: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: A core referenced in ``execution.yaml`` or
     ``deployment.yaml`` as a core affinity target but marked as
     disabled in ``machine-design.yaml`` will cause a runtime failure.
     This must be detected at validation time.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-054

   The ``adaptive::validation`` crate **SHALL** detect any core affinity
   assignment in ``execution.yaml`` or ``deployment.yaml`` that
   references a CPU core index that is disabled or absent in the
   corresponding machine definition in ``machine-design.yaml``, and
   **SHALL** report each such occurrence as a WARNING diagnostic
   identifying the machine name, the core index and the process or
   deployment entry referencing it.

.. req:: A4 — Platform services designer
   :id: QDX-SWE-023
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: Adaptive platform services (ara::log, ara::tsync,
     ara::phm, ara::per) must be configurable in the designer.
     Their enabled/disabled state and configuration directly affects
     ARXML manifest generation.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-055

   The A4 Platform Services designer **SHALL** allow users to enable or
   disable and configure the following AUTOSAR Adaptive platform
   services: ``ara::log`` (Logging), ``ara::tsync`` (Time
   Synchronisation), ``ara::phm`` (Platform Health Management) and
   ``ara::per`` (Persistency). For each service the designer **SHALL**
   provide configuration of its service-specific parameters:

   - **ara::log**: logger name, log level (DEBUG / INFO / WARN / ERROR),
     output target (Console / File / Console+File) and buffering flag
     per logger.
   - **ara::tsync**: time synchronisation protocol and reference source.
   - **ara::phm**: health channel count and names.
   - **ara::per**: storage area count, names and key-value schema.

   The designer **SHALL** display per-service enabled/disabled status
   and a dependency graph linking platform services to one another.
   All configuration **SHALL** be persisted to ``platform-services.yaml``.

.. req:: A5 — Execution management designer
   :id: QDX-SWE-024
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: Process scheduling policy, priority and core affinity
     are execution manifest attributes that drive OS-level scheduling
     on the target machine. They must be definable and validated before
     ARXML export.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-056

   The A5 Execution designer **SHALL** allow users to define processes
   with the following attributes: process name, associated application
   name, scheduling priority (integer), scheduling policy (SCHED_FIFO /
   SCHED_RR / SCHED_OTHER), and core affinity as a list of zero-indexed
   core indices on the target machine. The designer **SHALL** display:

   - A timeline view showing process scheduling across a configurable
     time window on the target machine's cores.
   - A core affinity map showing which processes are pinned to which
     physical cores.
   - A flat table view with all process attributes and current status.

   All definitions **SHALL** be persisted to ``execution.yaml``.

.. req:: A5 — Scheduling conflict detection
   :id: QDX-SWE-025
   :parent: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: Two SCHED_FIFO processes at the same priority sharing
     a core affinity set can produce starvation. This must be flagged
     at configuration time.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-057

   The ``adaptive::validation`` crate **SHALL** detect and report as
   a WARNING any pair of processes that share one or more core affinity
   indices, use the same scheduling policy of SCHED_FIFO or SCHED_RR,
   and are assigned equal scheduling priorities, identifying the
   process names, the conflicting priority value and the shared core
   indices.

.. req:: A6 — Deployment designer
   :id: QDX-SWE-026
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: The A6 designer is the final integration surface for
     Adaptive AUTOSAR — mapping applications and their processes to
     target machines with core affinity. Completeness of A6 is the
     prerequisite for generating ApplicationManifest, ExecutionManifest
     and MachineManifest ARXML outputs.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-058

   The A6 Deployment designer **SHALL** allow users to define
   application-to-machine deployments specifying: application name,
   associated process name (from ``execution.yaml``), target machine
   name (from ``machine-design.yaml``) and core affinity override if
   different from the execution definition. The designer **SHALL**
   display a mapping view and a flat table view of all deployments with
   status (DEPLOYED / UNDEPLOYED / ERROR). It **SHALL** display an
   ARXML export readiness indicator reporting the validation status of
   each of the six Adaptive designers (A1–A6) and the set of ARXML
   manifest files that will be generated (``ApplicationManifest``,
   ``ExecutionManifest``, ``MachineManifest``). All definitions **SHALL**
   be persisted to ``deployment.yaml``.

.. req:: A6 — Resource constraint validation
   :id: QDX-SWE-027
   :parent: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: Deploying more applications than the target machine's
     RAM or core count can support must be caught before ARXML export,
     not at ECU integration time.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-059

   The ``adaptive::validation`` crate **SHALL** verify for each target
   machine that the aggregate RAM demand of all applications deployed
   to it does not exceed the machine's declared RAM capacity and that
   the number of distinct core affinity assignments does not exceed the
   machine's declared core count. Violations **SHALL** be reported as
   ERROR diagnostics identifying the machine name, the exceeded resource
   type, the aggregate demand and the declared capacity.

.. req:: Adaptive cross-designer consistency check
   :id: QDX-SWE-028
   :parent: QDX-SYS-020
   :status: Draft
   :priority: High
   :rationale: The six Adaptive YAML files form a single coherent model.
     A service defined in A1 but not instantiated in A2, a process in
     A5 not deployed in A6, or a machine in A3 not referenced in A6
     represent incomplete configurations that must be detected before
     ARXML generation is permitted.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-028

   The workspace-level consistency check **SHALL** validate the
   following cross-file invariants for every Adaptive project:

   - Every service defined in ``application-design.yaml`` is referenced
     by at least one provider instance in ``communication.yaml``
     (WARNING if no provider exists).
   - Every provider and consumer instance in ``communication.yaml``
     references a machine declared in ``machine-design.yaml`` (ERROR
     if machine is absent).
   - Every process in ``execution.yaml`` is associated with an
     application deployed in ``deployment.yaml`` (WARNING if process
     is unreferenced).
   - Every deployment entry in ``deployment.yaml`` references a process
     defined in ``execution.yaml`` and a machine defined in
     ``machine-design.yaml`` (ERROR if either reference is absent).

   Violations **SHALL** produce diagnostics with severity, a
   natural-language message, and the YAML file path and key path of
   the offending element.


5.5 Hybrid synchronisation
----------------------------

.. req:: Designer-to-YAML synchronisation
   :id: QDX-SWE-029
   :parent: QDX-SYS-005
   :status: Draft
   :priority: High
   :rationale: Derived from hybrid synchronization. A change via the
     designer canvas must be immediately visible in the YAML editor
     after save, and vice versa.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-007

   After any valid designer operation that results in a model mutation,
   the Command Bus **SHALL** route the corresponding ``core::ops``
   operation through the WASM Bridge, apply it to the in-memory model,
   and serialise the updated model to the YAML source file such that a
   subsequent open of that file in the YAML editor reflects the change.

.. req:: YAML-to-designer synchronisation
   :id: QDX-SWE-030
   :parent: QDX-SYS-005
   :status: Draft
   :priority: High
   :rationale: A user editing YAML directly must see the designer canvas
     update on save or explicit refresh without manual reload.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-051

   When a YAML source file is saved by the YAML editor, the IDE Layer
   **SHALL** re-parse the file via ``core::yaml``, update the in-memory
   model, and refresh all open designer views that display content
   sourced from that file within 2 seconds under nominal conditions.


5.6 Validation subsystem
--------------------------

.. req:: In-IDE WASM fast validation
   :id: QDX-SWE-031
   :parent: QDX-SYS-006
   :status: Draft
   :priority: High
   :rationale: Derived from schema validation and interactive validation
     feedback latency (QDX-SYS-023). Fast local validation must not
     require a network round-trip.
   :verification: SWE.6 qualification test — latency measurement
   :jira: QDX-SWE-031

   The ``qorix_core_wasm`` WASM build target **SHALL** provide a
   ``validateYaml(content, schema_id)`` export that performs JSON Schema
   structural and mandatory-field validation in-process within the IDE
   host, returning a diagnostic list within 500 ms for a single
   medium-sized YAML file without a network call.

.. req:: Deep semantic validation via domain service
   :id: QDX-SWE-032
   :parent: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: Derived from semantic validation. Cross-file and semantic
     rules require the full domain model loaded in the domain service.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-032

   The Rust Domain Service **SHALL** perform deep semantic validation
   on demand, detecting and reporting: unresolved cross-file references,
   duplicate identifiers within scope, incompatible port interface
   pairings, missing runnable-to-task mappings, and undefined signal
   references. Each diagnostic **SHALL** include severity (ERROR,
   WARNING, INFO), a natural-language message, and the YAML file path
   and key path of the offending element.

.. req:: Cross-file reference resolution
   :id: QDX-SWE-033
   :parent: QDX-SYS-008
   :status: Draft
   :priority: High
   :rationale: Derived from cross-file reference management. AUTOSAR
     models are inherently multi-file and references such as signal
     names in rte-mapping.yaml pointing to signals-comstack.yaml must
     resolve at validation time.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-005

   The ``core::validation`` rule engine **SHALL** resolve symbolic
   references between YAML files within the same project boundary during
   semantic validation and report each unresolved reference as an ERROR
   diagnostic with the source file, key path, and the reference value
   that could not be resolved.

.. req:: Validation-gated publication
   :id: QDX-SWE-034
   :parent: QDX-SYS-036
   :status: Draft
   :priority: High
   :rationale: Derived from safe failure on invalid configuration. ARXML
     must not be produced from a model with unresolved ERROR diagnostics.
   :verification: SWE.6 qualification test — negative path
   :jira: QDX-SWE-053

   The generation pipeline **SHALL** refuse to invoke the ARXML Gateway
   and **SHALL** return a non-zero exit code and structured error
   report when the semantic validation step produces one or more
   diagnostics of severity ERROR for the target project.

.. req:: Workspace-level consistency check
   :id: QDX-SWE-035
   :parent: QDX-SYS-020
   :status: Draft
   :priority: High
   :rationale: Derived from workspace consistency checking. A multi-file
     multi-designer project must be checked as a whole before release.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-052

   The Rust Domain Service **SHALL** provide a workspace-consistency-
   check operation that loads all YAML files across all projects in the
   workspace, resolves all cross-file references, runs all applicable
   Classic and Adaptive validation rules, and returns a consolidated
   diagnostic report with per-file and per-designer (C1–C6) summaries
   including ARXML export readiness status per designer.


5.7 Diagnostics and issue reporting
-------------------------------------

.. req:: Diagnostics panel presentation
   :id: QDX-SWE-036
   :parent: QDX-SYS-014
   :status: Draft
   :priority: High
   :rationale: Derived from diagnostics and issue reporting. Validation
     output from both WASM (fast) and domain service (deep) must be
     presented in a unified, actionable panel.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-053

   The Diagnostics Panel **SHALL** display all validation diagnostics
   from both the WASM Bridge and the Domain Service Client, grouped by
   severity (ERROR, WARNING, INFO), with each entry showing: severity
   icon, diagnostic message, affected YAML file name, and the designer
   tab (C1–C6 or Adaptive view) where the element originates. Clicking
   a diagnostic entry **SHALL** navigate the editor to the affected
   YAML line or designer canvas element.

.. req:: Usable diagnostic message quality
   :id: QDX-SWE-037
   :parent: QDX-SYS-042
   :status: Draft
   :priority: Medium
   :rationale: Derived from usable diagnostics quality. Engineers must
     be able to act on diagnostics without decoding internal identifiers.
   :verification: Demonstration | Inspection
   :jira: QDX-SWE-051

   Every diagnostic message produced by ``core::validation``,
   ``classic::validation`` and ``adaptive::validation`` **SHALL** use
   AUTOSAR engineering terminology consistent with the Qorix Designer
   UI labels, reference the affected model element by its user-visible
   name (e.g. SWC name, runnable name, signal name), and include a
   brief corrective action hint where a standard resolution exists.


5.8 Artefact generation and ARXML Gateway
-------------------------------------------

.. req:: Deterministic ARXML generation
   :id: QDX-SWE-038
   :parent: QDX-SYS-009
   :status: Draft
   :priority: High
   :rationale: Derived from deterministic artefact publication and
     deterministic processing for safety-relevant flows. Identical input
     must always produce identical ARXML output.
   :verification: Analysis | SWE.6 qualification test — reproducibility
   :jira: QDX-SWE-038

   The generation pipeline — comprising the Rust Domain Service loading
   the YAML model, the ``core::gql_client`` GraphQL call to the ARXML
   Gateway, and the Spring Boot + ARTOP ARXML serialisation — **SHALL**
   produce byte-identical ARXML output for identical validated YAML
   inputs, identical GraphQL schema version and identical ARTOP library
   version, with no timestamps, random seeds or process IDs embedded in
   the output.

.. req:: ARXML export via ARTOP GraphQL gateway
   :id: QDX-SWE-039
   :parent: QDX-SYS-010
   :status: Draft
   :priority: High
   :rationale: Derived from AUTOSAR artefact export. The ARXML Gateway
     is the sole ARXML production path — the Rust domain never calls
     EMF/ARTOP directly.
   :verification: SWE.6 qualification test — interface conformance
   :jira: QDX-SWE-039

   The Rust Domain Service **SHALL** invoke ARXML export exclusively
   through ``core::gql_client`` GraphQL mutations targeting the ARXML
   Gateway (Spring Boot + ARTOP). The Rust domain crates **SHALL NOT**
   depend on any EMF or ARTOP library directly. The ARXML Gateway
   **SHALL** produce AUTOSAR-schema-valid ARXML for the target schema
   version declared in the project configuration.

.. req:: ARXML import and lossy-conversion reporting
   :id: QDX-SWE-040
   :parent: QDX-SYS-011
   :status: Draft
   :priority: High
   :rationale: Derived from AUTOSAR artefact import. Legacy tools
     (Tresos, DaVinci) produce ARXML that may not map 1:1 to Qorix
     YAML semantics.
   :verification: SWE.6 qualification test — interface conformance
   :jira: QDX-SWE-040

   The ``classic::migration`` and ``adaptive::migration`` crates **SHALL**
   transform imported ARXML (via the ARXML Gateway) into Qorix YAML
   using ``core::migration`` primitives. For each ARXML element that
   cannot be represented in the Qorix YAML model without loss or
   ambiguity, the import operation **SHALL** produce a WARNING diagnostic
   identifying the element path, the nature of the incompatibility and
   the applied default or approximation.

.. req:: Generation provenance recording
   :id: QDX-SWE-041
   :parent: QDX-SYS-015
   :status: Draft
   :priority: High
   :rationale: Derived from traceable generation provenance. Auditors
     must be able to reconstruct which inputs and tool versions produced
     a given ARXML artefact.
   :verification: Inspection | Analysis
   :jira: QDX-SWE-041

   The generation pipeline **SHALL** produce a provenance metadata file
   alongside each generated ARXML output, recording: the Git commit SHA
   or content hash of each source YAML file included in the generation,
   the ``qorix_cli`` or Rust Domain Service version string, the ARXML
   Gateway version string, the ARTOP version, the target AUTOSAR schema
   version, and the UTC timestamp of the generation run.

.. req:: External artefact compatibility status reporting
   :id: QDX-SWE-042
   :parent: QDX-SYS-030
   :status: Draft
   :priority: Medium
   :rationale: Derived from external artefact compatibility reporting.
     Customers need to know which AUTOSAR version each import/export
     targets.
   :verification: SWE.6 qualification test | Inspection
   :jira: QDX-SWE-051

   On completion of any import or export operation, the platform
   **SHALL** report the AUTOSAR schema version targeted (e.g.
   R20-11, R23-11, R24-11), the compatibility status (Fully supported,
   Partially supported with warnings, Unsupported), and any elements
   that were skipped or approximated during conversion.


5.9 Structured model API (GraphQL)
------------------------------------

.. req:: GraphQL API contract for model access
   :id: QDX-SWE-043
   :parent: QDX-SYS-012
   :status: Draft
   :priority: High
   :rationale: Derived from structured model API. Designers and the
     Agent layer require a stable, versioned contract for model reads
     and mutations.
   :verification: SWE.6 qualification test — interface conformance
   :jira: QDX-SWE-043

   The ARXML Gateway **SHALL** expose all AUTOSAR model read and
   write operations through a versioned GraphQL schema. The schema
   **SHALL** be published as a machine-readable SDL file in the
   repository. Breaking schema changes **SHALL** increment the major
   schema version. The ``core::gql_client`` Rust client **SHALL** be
   generated from this SDL file.

.. req:: Search and navigation API
   :id: QDX-SWE-044
   :parent: QDX-SYS-018
   :status: Draft
   :priority: Medium
   :rationale: Derived from search and navigation across model content.
     Search must be backed by an indexed, queryable interface.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-044

   The Rust Domain Service **SHALL** provide a search operation
   accepting a text query and returning matching configuration elements
   (SWC names, signal names, port names, NvM block names, diagnostic
   message text) across all loaded YAML files in the workspace, with
   results including file name, YAML key path and a match excerpt,
   within the performance bound defined in QDX-SWE-056.


5.10 CI/CD and CLI
--------------------

.. req:: Headless CLI for CI validation and generation
   :id: QDX-SWE-045
   :parent: QDX-SYS-031
   :status: Draft
   :priority: Medium
   :rationale: Derived from CI/CD invocation support. The same Rust
     domain code used in the IDE must be available as a headless binary
     for pipeline use.
   :verification: Demonstration | SWE.6 qualification test
   :jira: QDX-SWE-045

   The ``qorix_cli`` binary **SHALL** provide at minimum the following
   subcommands: ``validate <project-path>`` (runs full semantic
   validation, exits non-zero on ERROR), and ``generate <project-path>
   --output <dir>`` (runs validation then invokes the ARXML Gateway to
   produce ARXML outputs). Both subcommands **SHALL** write structured
   diagnostic output to stdout as newline-delimited JSON and **SHALL**
   produce a non-zero exit code when any ERROR diagnostic is present.

.. req:: Same Rust core for all build targets
   :id: QDX-SWE-046
   :parent: QDX-SYS-031
   :status: Draft
   :priority: High
   :rationale: INTERNAL — Architectural constraint to prevent divergence
     between in-IDE validation and CI validation results.
   :verification: Inspection — single crate tree, three build targets
   :jira: QDX-SWE-046

   The ``core::*``, ``classic::*`` and ``adaptive::*`` crates **SHALL**
   compile without conditional compilation flags that alter validation
   or generation logic across the three build targets (Rust Domain
   Service, ``qorix_core_wasm``, ``qorix_cli``). Target-specific code
   **SHALL** be limited to I/O adapters, serialisation entry points and
   build target scaffolding.


5.11 Qorix Agent and AI layer
-------------------------------

.. req:: AI-generated OperationPlan — no direct YAML edit
   :id: QDX-SWE-047
   :parent: QDX-SYS-016
   :status: Draft
   :priority: High
   :rationale: Derived from explainable AI assistance. The LLM must
     never write YAML directly — all changes must flow through typed
     operations with user review.
   :verification: Inspection | SWE.6 qualification test
   :jira: QDX-SWE-047

   The Qorix Agent **SHALL** produce all proposed configuration changes
   as a structured ``OperationPlan`` — a typed list of ``core::ops``
   operations — which is presented to the user with an explanation of
   each operation before any persistent change is applied. The Agent
   **SHALL NOT** write to any YAML file or invoke any generation
   operation without an intermediate user acceptance step.

.. req:: User acceptance gate for AI suggestions
   :id: QDX-SWE-048
   :parent: QDX-SYS-017
   :status: Draft
   :priority: High
   :rationale: Derived from user acceptance of AI suggestions. Final
     engineering responsibility must remain with the human user.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-048

   The AI Chat Panel **SHALL** present each ``OperationPlan`` with an
   explicit Accept and Reject control per plan. Applying the plan to the
   YAML model **SHALL** occur only after the user activates the Accept
   control. A Rejected plan **SHALL** produce no change to any project
   file. The acceptance event **SHALL** be recorded as an audit event
   per QDX-SWE-052.

.. req:: Post-acceptance WASM re-validation
   :id: QDX-SWE-049
   :parent: QDX-SYS-006
   :status: Draft
   :priority: High
   :rationale: INTERNAL — After an AI-originated change is applied, the
     model must be re-validated immediately to detect any introduced
     errors before the user continues.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-049

   Immediately after an accepted ``OperationPlan`` is applied and
   persisted, the WASM Bridge **SHALL** trigger a ``validateYaml()``
   call on all affected YAML files and update the Diagnostics Panel with
   the resulting diagnostic list.

.. req:: Intent Router — Classic vs Adaptive dispatch
   :id: QDX-SWE-050
   :parent: QDX-SYS-016
   :status: Draft
   :priority: Medium
   :rationale: INTERNAL — The Agent must correctly route user messages
     to Classic or Adaptive MCP tool sets based on the active project
     context to avoid cross-domain tool invocations.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-050

   The Intent Router **SHALL** determine the target stack (Classic or
   Adaptive) from the active workspace project context before routing a
   user message to the Tool Registry. Tool calls **SHALL** only be
   dispatched to MCP tools registered for the active stack. Cross-stack
   tool invocations **SHALL** be rejected with a user-visible
   explanation.

.. req:: Configurable AI data transmission control
   :id: QDX-SWE-051
   :parent: QDX-SYS-037
   :status: Draft
   :priority: High
   :rationale: Derived from controlled AI data usage. Enterprises may
     prohibit transmission of project YAML to external LLM services.
   :verification: Inspection | Analysis
   :jira: QDX-SWE-051

   The Qorix Agent **SHALL** read a deployment-level configuration
   setting that controls whether YAML content fragments may be included
   in prompts sent to the configured LLM backend. When this setting is
   disabled, the Agent **SHALL** send only structural metadata (element
   type names, counts, error codes) and **SHALL NOT** transmit user YAML
   content to any external service.


5.12 Security, audit and access control
-----------------------------------------

.. req:: Audit log for critical user actions
   :id: QDX-SWE-052
   :parent: QDX-SYS-035
   :status: Draft
   :priority: Medium
   :rationale: Derived from auditability of user-visible critical actions.
   :verification: Inspection | Analysis
   :jira: QDX-SWE-052

   The platform **SHALL** append an audit record to a structured log
   file for each of the following events: ARXML generation completed,
   ARXML generation failed, ARXML import completed, AI OperationPlan
   accepted, AI OperationPlan rejected, workspace publish initiated.
   Each record **SHALL** include: event type, UTC timestamp, user
   identity (if configured), project path, and outcome.

.. req:: Access control for privileged operations
   :id: QDX-SWE-053
   :parent: QDX-SYS-034
   :status: Draft
   :priority: Medium
   :rationale: Derived from access control for privileged operations.
   :verification: SWE.6 qualification test | Inspection
   :jira: QDX-SWE-053

   When authentication is configured for the deployment, the platform
   **SHALL** require a valid authenticated session before permitting
   ARXML generation, workspace publish or extension installation
   operations. Unauthenticated requests to these operations **SHALL**
   be rejected with an actionable error message.


5.13 Performance requirements
-------------------------------

.. req:: Workspace open time
   :id: QDX-SWE-054
   :parent: QDX-SYS-022
   :status: Draft
   :priority: High
   :rationale: Derived from workspace opening time. 30-second system
     bound must be met by the software implementation.
   :verification: SWE.6 qualification test — performance measurement
   :jira: QDX-SWE-054

   The workspace loading sequence — file system scan, YAML parsing via
   ``core::yaml``, in-memory model construction for all projects —
   **SHALL** complete within 30 seconds on a workstation with the
   defined benchmark workspace (to be specified in TBD-SYS-001).

.. req:: WASM validation latency
   :id: QDX-SWE-055
   :parent: QDX-SYS-023
   :status: Draft
   :priority: High
   :rationale: Interactive feedback latency is 2 seconds at system level;
     the WASM path must complete within 500 ms to leave headroom for
     IDE rendering.
   :verification: SWE.6 qualification test — performance measurement
   :jira: QDX-SWE-055

   The ``qorix_core_wasm`` ``validateYaml()`` function **SHALL** return
   a diagnostic result within 500 ms for a single YAML file of up to
   1 000 lines under nominal IDE host conditions.

.. req:: Search response time
   :id: QDX-SWE-056
   :parent: QDX-SYS-024
   :status: Draft
   :priority: Medium
   :rationale: Derived from search responsiveness. 5-second system bound.
   :verification: SWE.6 qualification test — performance measurement
   :jira: QDX-SWE-056

   The Rust Domain Service search operation **SHALL** return results
   within 5 seconds for a text query against a workspace of up to
   50 YAML files with up to 500 model elements each.

.. req:: ARXML generation completion time
   :id: QDX-SWE-057
   :parent: QDX-SYS-025
   :status: Draft
   :priority: High
   :rationale: Derived from artefact generation completion time. 60-second
     system bound covers the full pipeline end-to-end.
   :verification: SWE.6 qualification test — performance measurement
   :jira: QDX-SWE-057

   The complete generation pipeline — YAML load, semantic validation,
   GraphQL mutation to ARXML Gateway, ARTOP serialisation and file write
   — **SHALL** complete within 60 seconds for a medium-sized validated
   project (definition per TBD-SYS-001) under nominal workstation
   conditions.

.. req:: Non-blocking UI for long-running operations
   :id: QDX-SWE-058
   :parent: QDX-SYS-026
   :status: Draft
   :priority: Medium
   :rationale: Derived from non-blocking UI during long-running operations.
   :verification: Demonstration | SWE.6 qualification test
   :jira: QDX-SWE-058

   Any operation invoked from the IDE Layer that is expected to exceed
   5 seconds (workspace validation, ARXML generation, AI OperationPlan
   computation) **SHALL** execute on a background thread or async task,
   display a progress indicator with a descriptive status message, and
   provide a user-accessible cancellation control.


5.14 Portability and extensibility
------------------------------------

.. req:: Dual IDE host support — VS Code and Theia
   :id: QDX-SWE-059
   :parent: QDX-SYS-027
   :status: Draft
   :priority: High
   :rationale: Derived from IDE integration support. Product strategy
     requires identical functionality across both IDE hosts.
   :verification: SWE.6 qualification test — interface conformance
   :jira: QDX-SWE-059

   The IDE Layer **SHALL** expose identical designer, validation,
   generation and AI assistance functionality in both the VS Code
   Extension and the Theia Desktop/Web IDE host environments. All
   API contracts, WASM bridge interfaces and Command Bus operations
   **SHALL** be host-agnostic.

.. req:: Offline local authoring and validation
   :id: QDX-SWE-060
   :parent: QDX-SYS-043
   :status: Draft
   :priority: Medium
   :rationale: Derived from availability of offline engineering workflows.
     WASM enables local validation without network access.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-060

   Local YAML authoring, WASM-based schema validation and designer
   canvas display **SHALL** be fully functional without network
   connectivity. Operations that explicitly require a network connection
   (Rust Domain Service deep validation, ARXML Gateway generation, LLM
   Agent) **SHALL** fail gracefully with a user-visible offline
   indication and **SHALL NOT** silently return incorrect results.

.. req:: Extension mechanism without core modification
   :id: QDX-SWE-061
   :parent: QDX-SYS-041
   :status: Draft
   :priority: Medium
   :rationale: Derived from extensibility without core modification.
   :verification: Analysis | Demonstration
   :jira: QDX-SWE-061

   New domain designers, validation rule sets or generation targets
   **SHALL** be addable through the platform's extension mechanism
   without modifying ``core::*``, ``classic::*`` or ``adaptive::*``
   crates. The Tool Registry in the Qorix Agent **SHALL** support
   dynamic registration of additional MCP tools at agent startup without
   code changes to the Intent Router.

.. req:: Backward-compatible project migration
   :id: QDX-SWE-062
   :parent: QDX-SYS-040
   :status: Draft
   :priority: Medium
   :rationale: Derived from backward compatibility of project content.
   :verification: SWE.6 qualification test | Analysis
   :jira: QDX-SWE-062

   When a workspace created by an earlier supported Qorix Developer
   version is opened, the platform **SHALL** detect the project schema
   version from the workspace metadata, apply any required YAML
   structure migrations via ``core::migration``, and inform the user of
   any changes applied. A migration **SHALL NOT** silently alter
   engineering model values — only structural schema adaptations are
   permitted.


5.15 Bootloader designers — BPCT (BD1–BD6)
--------------------------------------------

.. admonition:: BPCT scope note

   The Bootloader Parameters Configurator Tool (BPCT) is the Qorix
   Developer subsystem for authoring, validating and generating
   Flash Bootloader (FBL) configuration artefacts. It operates on six
   YAML source files (``bl-project.yaml``, ``bl-communication.yaml``,
   ``bl-memory.yaml``, ``bl-core.yaml``, ``bl-hardware.yaml``,
   ``bl-security.yaml``) and produces ``cfg.h``, ``cfg.c`` and
   ``Makefile.mak`` as generated outputs. All BPCT designers (BD1–BD6)
   follow the same YAML-as-source-of-truth and validation-gated
   generation model as the Classic and Adaptive designers.

.. req:: BPCT project structure and MCU selection (BD1)
   :id: QDX-SWE-063
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: The BD1 designer is the entry point for every bootloader
     project. MCU family selection drives defaults (flash page size, max
     SPI clock, timer resolution, RAM, Flash) that constrain all
     downstream BPCT designers. Derived from project scaffolding.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-063

   The BD1 Project & MCU designer **SHALL** allow users to select the
   target MCU family from the supported set (TC3xx, TC4xx, RH850,
   S32K1xx, S32K3xx, S32Gx) and **SHALL** automatically apply MCU-
   family default values for flash page size, maximum SPI clock, timer
   resolution, RAM capacity and Flash capacity upon selection. Users
   **SHALL** be able to define the following project identity parameters:
   ``FBL_PROJECT_NAME``, ``FBL_ECU_ID``, ``FBL_VERSION_MAJOR``,
   ``FBL_VERSION_MINOR``, ``FBL_VERSION_PATCH`` and
   ``FBL_MCU_CLOCK_MHZ``. All definitions **SHALL** be persisted to
   ``bl-project.yaml``. The designer **SHALL** display an output preview
   showing the corresponding generated ``cfg.h`` macro definitions in
   real time as parameter values are edited.

.. req:: BPCT communication channel configuration (BD2)
   :id: QDX-SWE-064
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: The BD2 designer configures the UDS communication channel
     used by the bootloader for diagnostic and programming sessions.
     Protocol selection (CAN, CAN-FD, LIN, FlexRay, ETH) and UDS
     address configuration are mandatory before any programming session
     can be defined.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-064

   The BD2 Communication designer **SHALL** allow users to add and
   configure one or more communication channels, specifying for each:
   protocol (CAN, CAN-FD, LIN, FlexRay, ETH), baud rate, UDS physical
   request CAN ID (``FBL_UDS_PHYSICAL_REQ_ID``), UDS response CAN ID
   (``FBL_UDS_RESP_ID``) and UDS functional broadcast ID
   (``FBL_UDS_FUNCTIONAL_ID``). The designer **SHALL** display a UDS
   message flow diagram showing the tester-to-ECU physical request,
   response and functional broadcast address interactions for the active
   channel. All configuration **SHALL** be persisted to
   ``bl-communication.yaml``.

.. req:: BPCT memory map and NvM block configuration (BD3)
   :id: QDX-SWE-065
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: The BD3 designer defines the flash memory layout the
     bootloader operates on — bootloader ROM, secure key store, app
     validity flag and application programmable flash regions — and the
     NvM blocks stored in data flash. Start addresses, region sizes and
     protection attributes must be defined here before timing and
     security constraints can be computed in BD5 and BD6.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-065

   The BD3 Memory & Flash designer **SHALL** allow users to define
   flash memory regions with the following attributes per region: start
   address, end address (or size), region type (Bootloader ROM,
   Secure Key Store, App Validity Flag, Application PFlash, DFlash),
   and protection flag. It **SHALL** display a visual flash memory map
   to scale showing all defined regions with their hex addresses, sizes
   and labels. Users **SHALL** be able to define NvM blocks with:
   block ID, name, size in bytes, NvM block type
   (``NvMBlockUseNvRamManagerCRC``, ``NvMBlockUseCRCCompMechanism``),
   and CRC type (CRC16, CRC32). All definitions **SHALL** be persisted
   to ``bl-memory.yaml``.

.. req:: BPCT flash block size constraint validation (BD3)
   :id: QDX-SWE-066
   :parent: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: The configured flash block size must be an integer
     multiple of the MCU-derived erase page size. Violating this
     constraint produces an unflashable configuration.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-066

   The BPCT validation engine **SHALL** verify that
   ``FBL_FLASH_BLOCK_SIZE`` is a positive integer multiple of
   ``FBL_ERASE_PAGE_SIZE`` (derived from the MCU family selected in
   BD1). A non-multiple value **SHALL** be reported as an ERROR
   diagnostic referencing rule ``VR_003``, the configured block size,
   the MCU page size, and the ``bl-memory.yaml`` key path.

.. req:: BPCT core parameters and UDS session configuration (BD4)
   :id: QDX-SWE-067
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: BD4 configures the bootloader core modules — BL Core,
     Boot Manager, Diagnostic, Scheduler, CRC and Callbacks, and OEM
     parameters — and the UDS session state machine (Default, Extended
     Diagnostic, Programming sessions with Security Unlock and ECU
     Reset transitions).
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-067

   The BD4 Core & Diagnostics designer **SHALL** display a UDS session
   state machine diagram showing session transitions between Default
   Session (0x10 01), Extended Diagnostic Session (0x10 03),
   Programming Session (0x10 02) with Security Unlock (0x27 01/02)
   and ECU Reset (0x11 01). Users **SHALL** be able to configure the
   following parameter groups, each with its pre-compile or mixed
   classification displayed: BL Core (``FBL_NUM_MEMORY_SEGMENTS``,
   ``FBL_PROG_SESSION_TIMEOUT_MS``), Boot Manager
   (``FBL_BOOTMGR_APP_VALIDITY_ADDR``,
   ``FBL_BOOTMGR_START_DELAY_MS``, ``FBL_BOOTMGR_FALLBACK_ENABLED``),
   Diagnostic, Scheduler, CRC & Callbacks and OEM parameters.
   All configuration **SHALL** be persisted to ``bl-core.yaml``.

.. req:: BPCT timing, hardware and watchdog configuration (BD5)
   :id: QDX-SWE-068
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: BD5 defines the timing dependency chain from MCU clock
     through timer tick, scheduler cycle, watchdog feed interval and
     UDS P2 server timer to flash erase and write timeouts. These
     parameters have hard ordering constraints between them that must
     be validated as a chain, not as independent values.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-068

   The BD5 Timing & HW designer **SHALL** allow users to configure the
   following timing and watchdog parameters: ``FBL_TIMER_TICK_US``,
   ``FBL_TIMER_P2_SERVER_MS``, ``FBL_TIMER_ERASE_TIMEOUT_MS``,
   ``FBL_TIMER_WRITE_TIMEOUT_MS``, ``FBL_WDG_TIMEOUT_MS`` and
   ``FBL_WDG_DISABLE_DURING_ERASE``. The designer **SHALL** display a
   timing dependency chain diagram showing the derivation path from
   MCU clock (sourced from BD1) through timer tick, scheduler cycle,
   watchdog feed interval and P2 server timer to erase and write
   timeouts, with each node labelled with its computed or configured
   value and its upstream dependency. A "Recalculate Chain" action
   **SHALL** recompute all derived timing values from the current MCU
   clock and display updated values. All configuration **SHALL** be
   persisted to ``bl-hardware.yaml``.

.. req:: BPCT watchdog timeout cross-constraint validation (BD5)
   :id: QDX-SWE-069
   :parent: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: Rule VR_007: when watchdog disable-during-erase is FALSE,
     the watchdog timeout must strictly exceed the flash erase timeout
     to prevent watchdog expiry during an erase operation. This is a
     hard safety constraint for the bootloader.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-069

   The BPCT validation engine **SHALL** implement rule ``VR_007``:
   when ``FBL_WDG_DISABLE_DURING_ERASE`` is ``FALSE``,
   ``FBL_WDG_TIMEOUT_MS`` **SHALL** be strictly greater than
   ``FBL_TIMER_ERASE_TIMEOUT_MS``. A violation **SHALL** be reported
   as an ERROR diagnostic citing rule ``VR_007``, both parameter names,
   their current values, the required minimum value for
   ``FBL_WDG_TIMEOUT_MS`` (``FBL_TIMER_ERASE_TIMEOUT_MS`` + 100 ms
   as a safe default recommendation), and the ``bl-hardware.yaml`` key
   path.

.. req:: BPCT cross-designer timing dependency propagation
   :id: QDX-SWE-070
   :parent: QDX-SYS-008
   :status: Draft
   :priority: High
   :rationale: BD5 timing values depend on BD1 (MCU clock) and BD3
     (flash block size for write timeout derivation). When BD1 or BD3
     values change, BD5 must notify the user that timing values should
     be recalculated to remain consistent with the updated upstream
     inputs.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-070

   When ``FBL_MCU_CLOCK_MHZ`` in ``bl-project.yaml`` or
   ``FBL_FLASH_BLOCK_SIZE`` in ``bl-memory.yaml`` is modified, the
   BPCT validation engine **SHALL** produce an INFO diagnostic on
   ``bl-hardware.yaml`` citing rule ``VR_016`` advising the user to
   recalculate the timing dependency chain. This diagnostic **SHALL**
   reference the changed upstream parameter name, its new value and
   the BD5 parameters that depend on it.

.. req:: BPCT crypto and secure boot configuration (BD6)
   :id: QDX-SWE-071
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: BD6 configures the cryptographic security chain for
     secure flash authentication, secure boot signature verification
     and payload encryption, integrating with the Qorix cybersecurity
     toolchain (SKGT, ASKGT, EKGT, SGT, CGT) for key and certificate
     management.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-071

   The BD6 Crypto & Security designer **SHALL** allow users to configure
   the following security subsystems:

   - **Secure Boot**: enable/disable flag (``FBL_SEC_BOOT_ENABLED``),
     signature algorithm selection (``FBL_SEC_BOOT_SIG_ALGO``:
     RSA2048, RSA4096, ECDSA256), public key flash address
     (``FBL_SEC_BOOT_PUBLIC_KEY_ADDR``) and key source reference to
     the ASKGT toolchain output.
   - **Secure Flash**: hash algorithm (SHA256), authentication scope
     (write+erase).
   - **Encryption**: algorithm selection (AES256), key flash address
     and key source reference to the EKGT toolchain output.

   The designer **SHALL** display the cybersecurity toolchain flow
   (SKGT → ASKGT → EKGT → SGT → CGT) showing each tool's output file
   type and its downstream usage within the BPCT security configuration.
   Key address entries **SHALL** be validated against the flash memory
   map from ``bl-memory.yaml`` to confirm placement in a protected
   region (outside the application flash region). All configuration
   **SHALL** be persisted to ``bl-security.yaml``.

.. req:: BPCT weak cryptographic algorithm detection (BD6)
   :id: QDX-SWE-072
   :parent: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: RSA1024 is considered cryptographically weak for
     automotive secure boot (rule VR_013). The designer must warn
     users who select or import configurations using deprecated
     algorithms before ARXML/header generation is permitted.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-072

   The BPCT validation engine **SHALL** implement rule ``VR_013``:
   when ``FBL_SEC_BOOT_SIG_ALGO`` is set to RSA1024, a WARNING
   diagnostic **SHALL** be produced stating that RSA1024 is not
   recommended for automotive secure boot and recommending RSA2048 or
   ECDSA256 as alternatives. This diagnostic **SHALL NOT** block
   generation but **SHALL** be surfaced in the consolidated validation
   report.

.. req:: BPCT key address placement validation (BD6)
   :id: QDX-SWE-073
   :parent: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: Cryptographic key material stored inside the application
     programmable flash region can be erased during a firmware update.
     Keys must reside in a protected region, validated against the
     memory map defined in BD3.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-073

   The BPCT validation engine **SHALL** verify that each key address
   configured in ``bl-security.yaml`` (``FBL_SEC_BOOT_PUBLIC_KEY_ADDR``
   and encryption key address) falls within a flash region whose
   protection flag is set in ``bl-memory.yaml`` and does not overlap
   with the application programmable flash region. A key address
   outside a protected region **SHALL** be reported as an ERROR
   diagnostic referencing the parameter name, the configured address,
   the conflicting flash region name and the relevant memory map key
   path.

.. req:: BPCT validation rule engine (cross-designer)
   :id: QDX-SWE-074
   :parent: QDX-SYS-020
   :status: Draft
   :priority: High
   :rationale: BPCT parameters span six YAML files with cross-file
     ordering and consistency constraints (VR_NNN rules). A consolidated
     validation pass must evaluate all rules across all six files before
     generation is permitted, matching the workspace-level consistency
     check model used by Classic and Adaptive designers.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-074

   The BPCT validation engine **SHALL** evaluate all defined VR_NNN
   constraint rules across the complete set of six BPCT YAML files in
   a single consolidated validation pass. The pass **SHALL** produce a
   report listing each violation by rule identifier (VR_NNN), severity
   (ERROR, WARNING, INFO), the affected YAML file name, the parameter
   key path, the current value and the required constraint. Generation
   of ``cfg.h``, ``cfg.c`` and ``Makefile.mak`` **SHALL** be refused
   when one or more ERROR-severity rules remain unresolved.

.. req:: BPCT C header and Makefile generation
   :id: QDX-SWE-075
   :parent: QDX-SYS-009
   :status: Draft
   :priority: High
   :rationale: The primary output of BPCT is a set of C pre-compile
     configuration artefacts (cfg.h, cfg.c, Makefile.mak) consumed
     directly by the bootloader build toolchain. Generation must be
     deterministic and schema-version-stamped.
   :verification: SWE.6 qualification test | Analysis
   :jira: QDX-SWE-075

   The BPCT generation engine **SHALL** produce ``cfg.h``, ``cfg.c``
   and ``Makefile.mak`` from validated BPCT YAML sources. Each
   generated file **SHALL** include a header comment marking it as
   auto-generated and recording the BPCT schema version and the source
   YAML file it was derived from. ``cfg.h`` **SHALL** contain
   ``#define`` macros for all pre-compile classified parameters.
   Generation **SHALL** be deterministic: identical validated YAML
   inputs and identical BPCT version **SHALL** produce byte-identical
   output files.

.. req:: BPCT output preview in BD1 designer
   :id: QDX-SWE-076
   :parent: QDX-SYS-014
   :status: Draft
   :priority: Medium
   :rationale: Engineers need immediate feedback on how their YAML
     parameter values translate to generated C macros without running
     a full generation pass. The BD1 output preview provides this
     fast feedback loop.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-076

   The BD1 designer **SHALL** display a real-time output preview panel
   showing the ``cfg.h`` ``#define`` macros that would be generated
   from the current ``bl-project.yaml`` values. The preview **SHALL**
   update within 1 second of any parameter value change in BD1. The
   preview **SHALL** be read-only and **SHALL** be clearly labelled as
   a preview, not a saved generated file.


5.16 AI-Assist — extension-gated designer integration
-------------------------------------------------------

.. req:: AI-Assist availability gated by domain extension
   :id: QDX-SWE-077
   :parent: QDX-SYS-016
   :status: Draft
   :priority: High
   :rationale: AI-Assist for a designer domain is only available when
     the corresponding domain extension is installed. If the Classic
     extension is installed, AI-Assist activates for Classic designers
     (C1–C6). If the Adaptive extension is installed, AI-Assist
     activates for Adaptive designers (A1–A6). If the BPCT extension
     is installed, AI-Assist activates for Bootloader designers (BD1–BD6).
     No domain extension = no AI-Assist for that domain, regardless of
     whether the Qorix Agent is otherwise running.
   :verification: SWE.6 qualification test | Inspection
   :jira: QDX-SWE-077

   The IDE Layer **SHALL** activate AI-Assist capabilities (AI Chat
   Panel context injection, OperationPlan suggestions, AI toolbar
   controls) for a designer domain if and only if the corresponding
   domain extension is detected as installed and active in the current
   IDE host session. The mapping **SHALL** be:

   - Classic extension installed → AI-Assist enabled for C1–C6
     designers.
   - Adaptive extension installed → AI-Assist enabled for A1–A6
     designers.
   - BPCT extension installed → AI-Assist enabled for BD1–BD6
     designers.

   When a domain extension is not installed, the AI Chat Panel **SHALL**
   display a contextual message indicating which extension is required
   to enable AI-Assist for the active designer, and the AI toolbar
   control (✦ AI) **SHALL** be visible but disabled with a tooltip
   identifying the missing extension.

.. req:: AI-Assist context injection per domain
   :id: QDX-SWE-078
   :parent: QDX-SYS-016
   :status: Draft
   :priority: High
   :rationale: When AI-Assist is active for a domain, the Chat Panel
     must inject domain-specific context — the active YAML content,
     current validation diagnostics and the active designer tab — into
     the prompt sent to the Qorix Agent so that suggestions are
     relevant to the engineer's current view.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-078

   When a user submits a prompt in the AI Chat Panel with a domain
   designer open and the corresponding extension installed, the IDE
   Layer **SHALL** include in the prompt context: the active designer
   tab identifier (e.g. C1, A3, BD5), the relevant YAML file content
   or a structured excerpt thereof (subject to the AI data transmission
   control in QDX-SWE-051), and the current diagnostic list for the
   active project. The Qorix Agent Intent Router **SHALL** use the
   designer tab identifier to select the correct domain-specific MCP
   tool set (Classic, Adaptive or BPCT tools).

.. req:: AI-Assist OperationPlan scoped to active domain
   :id: QDX-SWE-079
   :parent: QDX-SYS-017
   :status: Draft
   :priority: High
   :rationale: An AI suggestion generated in the context of a Classic
     designer must only produce operations targeting Classic YAML files.
     Cross-domain mutations from a single AI suggestion are not
     permitted — they bypass the domain-specific validation layers.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-079

   An OperationPlan generated by the Qorix Agent in response to a
   prompt submitted from within a domain designer **SHALL** only contain
   ``core::ops`` operations targeting YAML files belonging to that
   designer's domain. An OperationPlan that would modify files outside
   the active domain **SHALL** be rejected by the Intent Router, and
   the user **SHALL** be informed that cross-domain changes require
   separate domain sessions.

.. req:: AI-Assist BPCT domain tools
   :id: QDX-SWE-080
   :parent: QDX-SYS-016
   :status: Draft
   :priority: Medium
   :rationale: INTERNAL — The BPCT domain requires its own MCP tool set
     registered in the Tool Registry, analogous to Classic and Adaptive
     tool sets, so the Intent Router can route BPCT-context prompts to
     the correct tools.
   :verification: Inspection | SWE.6 qualification test
   :jira: QDX-SWE-080

   The Qorix Agent Tool Registry **SHALL** include a BPCT MCP tool set,
   activated when the BPCT extension is installed, providing at minimum
   the following tools: ``suggest_timing_parameters`` (proposes
   consistent BD5 timing values given MCU clock and flash constraints),
   ``validate_security_config`` (analyses BD6 configuration against
   current VR rules and suggests remediation), and
   ``fix_cross_designer_violations`` (proposes parameter changes to
   resolve VR_NNN cross-file constraint violations). These tools
   **SHALL** only be callable through the structured OperationPlan and
   user acceptance gate defined in QDX-SWE-047 and QDX-SWE-048.


5.17 LW-BSW — Light Weight BSW configuration support
------------------------------------------------------

.. admonition:: LW-BSW scope note

   The Qorix Light Weight BSW (LW-BSW) is a Qorix-developed AUTOSAR
   Classic BSW stack targeted at small ECUs with tight memory and
   power constraints. It implements ICC-2 conformance with 10 BSW
   modules (COM, Diag, CanTp, CanIf, CDD, Operating System, IOHAB,
   EMM, NM), approximately 600 configuration parameters, a thin AUTOSAR
   Compliant RTE, an OSEK SC-1 operating system, and bus-level
   compatibility with full AUTOSAR Classic ECUs. Qorix Developer
   provides the configuration, validation, generation and AI-assisted
   insight tooling for LW-BSW projects through the LW-BSW extension.

   The LW-BSW configuration workflow in Qorix Developer follows the
   same YAML-as-source-of-truth model as Classic and Adaptive, with
   the following inputs: ECU/DEXT extract (``.xml``), legacy non-AUTOSAR
   DBC files (``.dbc``), and the LW-BSW PDF config schema. Outputs are
   module configuration ``.h`` and ``.c`` files plus a structured
   Config Report.

.. req:: LW-BSW project creation and ECU/DEXT import
   :id: QDX-SWE-081
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: LW-BSW projects begin by importing an existing ECU
     description (DEXT extract as XML) or a legacy non-AUTOSAR DBC
     file. Qorix Developer must harmonise these inputs against the
     LW-BSW config schema to produce a valid YAML configuration
     baseline, reducing the integration time from 20 person-days
     (Classic) to the LW-BSW target of 6 person-days.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-081

   The LW-BSW project scaffolding **SHALL** accept as import inputs
   an ECU/DEXT XML extract and/or a legacy non-AUTOSAR DBC file. The
   import processor **SHALL** parse the provided inputs, map
   extractable configuration elements to the corresponding LW-BSW
   YAML schema fields, and produce a pre-populated LW-BSW project
   YAML set as the initial configuration baseline. Elements in the
   import that have no LW-BSW equivalent **SHALL** be reported as
   WARNING diagnostics identifying the element name, its source file
   and the reason it cannot be mapped. The generated YAML baseline
   **SHALL** be committed to the project as the editable source of
   truth.

.. req:: LW-BSW module configuration — ten BSW modules
   :id: QDX-SWE-082
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: LW-BSW exposes approximately 600 configuration parameters
     across 10 modules. Each module must be configurable through a
     dedicated designer view that surfaces only LW-BSW-applicable
     parameters, preventing misconfiguration with full Classic BSW
     parameter sets.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-082

   The LW-BSW designer **SHALL** provide a dedicated configuration
   view for each of the following ten LW-BSW modules, persisting
   all parameters to the corresponding module YAML file:

   - **COM** — signal packing/unpacking, data type mapping, byte
     order, scaling, periodic transmission periods, deadline monitoring
     windows, safety hooks and callbacks.
   - **Diag** — UDS service subset selection (ISO 14229), DTC log and
     retrieve configuration, boot mode entry/exit parameters.
   - **CanTp** — transport layer parameters per ISO 15765-2: block
     size, STmin, N_As, N_Bs, N_Cs, N_Ar, N_Br, N_Cr timeouts,
     padding byte.
   - **CanIf** — CAN hardware abstraction parameters, PDU routing
     table, gateway routing to CDD.
   - **CDD** — ECU-specific complex driver configuration: I2C, SPI,
     sensor and actuator interface parameters, gateway function
     configuration.
   - **Operating System** — OSEK SC-1 task definitions (name,
     priority, activation type, stack size), ISR definitions,
     alarms and events.
   - **IOHAB** — DIO, ADC, ICU and PWM driver abstraction channel
     configuration.
   - **EMM** — ECU mode transition definitions, mode request sources,
     wake-up source assignments.
   - **NM** — Network management protocol selection (OSEK NM or
     AUTOSAR NM), NM node identifier, message ID, timeout parameters.
   - **NVRAM / EEPROM** — NvM block definitions with block ID,
     size, CRC type and EEPROM address mapping.

.. req:: LW-BSW CAN and optional LIN communication configuration
   :id: QDX-SWE-083
   :parent: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: LW-BSW supports CAN as mandatory and LIN as optional.
     The communication designer must enforce this constraint and expose
     only the protocol features applicable to LW-BSW (no FlexRay,
     no Ethernet).
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-083

   The LW-BSW communication designer **SHALL** allow configuration of
   CAN channels as a mandatory communication medium and LIN channels
   as an optional medium. The designer **SHALL NOT** offer FlexRay
   or Ethernet configuration options for LW-BSW projects. For each
   CAN channel the designer **SHALL** allow configuration of: baud
   rate, PDU routing table entries (PDU ID, direction, DLC, CAN ID),
   and CanIf gateway routing entries to CDD. For each LIN channel
   (when enabled): schedule table, frame definitions and LIN node
   type (master/slave).

.. req:: LW-BSW resource budget validation
   :id: QDX-SWE-084
   :parent: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: The LW-BSW target KPIs define hard upper bounds:
     ROM ≤ 150 KB, RAM ≤ 30 KB, platform init time ≤ 100 ms, CPU
     load < 10%, COM send < 100 µs, COM receive < 10 µs, task jitter
     < 2 µs, interrupt latency < 2 µs. The tool must estimate and
     warn when a configuration is likely to breach these bounds before
     code generation, so the engineer can adjust rather than discover
     the violation during target integration.
   :verification: SWE.6 qualification test | Analysis
   :jira: QDX-SWE-084

   The LW-BSW validation engine **SHALL** estimate ROM consumption,
   RAM consumption, and CPU load contribution from the current
   module configuration and produce WARNING diagnostics when any
   estimated value approaches or exceeds the LW-BSW target KPI
   bounds: ROM > 130 KB (warning threshold), ROM > 150 KB (error),
   RAM > 25 KB (warning), RAM > 30 KB (error), estimated CPU load
   > 8% (warning), > 10% (error). Estimates **SHALL** be displayed
   in a resource budget summary panel alongside the target KPI
   bounds and the current estimated values.

.. req:: LW-BSW OS scheduling map and race condition analysis
   :id: QDX-SWE-085
   :parent: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: The Config Report (slide 6 of LWASR_V0_1_0) requires
     a scheduling map and detection of potential runtime race
     conditions. With an OSEK SC-1 single-core priority-preemptive
     OS, race conditions arise when two tasks at different priorities
     access shared resources without exclusive area protection.
     Detecting these statically before code generation prevents
     runtime fault investigations.
   :verification: SWE.6 qualification test | Analysis
   :jira: QDX-SWE-085

   The LW-BSW validation engine **SHALL** produce a scheduling map
   showing all configured OS tasks with their priorities, periods,
   activation types and estimated worst-case execution time slots
   on a single-core timeline. The engine **SHALL** perform a static
   analysis to detect potential race conditions: shared resource
   accesses by tasks at different priorities without an intervening
   exclusive area or GetResource/ReleaseResource guard **SHALL** be
   reported as WARNING diagnostics identifying the resource name,
   the task names involved and their priority levels.

.. req:: LW-BSW Config Report generation
   :id: QDX-SWE-086
   :parent: QDX-SYS-015
   :status: Draft
   :priority: High
   :rationale: The LW-BSW configuration idea (slide 6) specifies a
     Config Report as a mandatory output alongside the generated
     .h and .c files. The report consolidates scheduling map,
     resource consumption estimates, race condition findings and
     safety violation detections into a single reviewable artefact
     for the integrating engineer and for ASPICE process evidence.
   :verification: SWE.6 qualification test | Inspection
   :jira: QDX-SWE-086

   The LW-BSW generation pipeline **SHALL** produce a Config Report
   alongside the generated module configuration ``.h`` and ``.c``
   files. The Config Report **SHALL** contain:

   - **Scheduling map** — all OS tasks with priority, period,
     activation type and core utilisation.
   - **Resource consumption** — estimated ROM (KB), RAM (KB) and
     CPU load (%) per module and total, compared against LW-BSW
     target KPI bounds.
   - **Potential race conditions** — list of shared resource
     accesses without exclusive area protection, with task names
     and priority levels.
   - **Safety violations** — list of any configuration parameters
     that violate the LW-BSW safety constraints (hook/callback
     assignments, diagnostic session timeouts, watchdog parameters).

   The Config Report **SHALL** be generated as a structured output
   file (JSON or YAML) and optionally as a human-readable HTML
   report. Generation of the Config Report **SHALL** be deterministic
   for identical validated YAML inputs and identical LW-BSW tool
   version.

.. req:: LW-BSW module configuration ``.h`` and ``.c`` generation
   :id: QDX-SWE-087
   :parent: QDX-SYS-009
   :status: Draft
   :priority: High
   :rationale: The primary deliverable of the LW-BSW tooling is the
     set of generated module configuration source files consumed by
     the LW-BSW build toolchain. Generation must be deterministic,
     schema-version-stamped and blocked by unresolved ERROR
     diagnostics.
   :verification: SWE.6 qualification test | Analysis
   :jira: QDX-SWE-087

   The LW-BSW generation engine **SHALL** produce one ``.h`` and one
   ``.c`` configuration file per LW-BSW module from the validated
   YAML sources. Each generated file **SHALL** include an
   auto-generated header comment recording the LW-BSW schema version,
   the source YAML file and the Qorix Developer tool version.
   Generation **SHALL** be deterministic: identical validated YAML
   inputs and tool version **SHALL** produce byte-identical output
   files. Generation **SHALL** be refused when one or more ERROR
   diagnostics are present in the current project validation state.

.. req:: LW-BSW bus-level compatibility check with Classic AUTOSAR
   :id: QDX-SWE-088
   :parent: QDX-SYS-007
   :status: Draft
   :priority: Medium
   :rationale: A key LW-BSW value proposition is bus-level
     interoperability with full Classic AUTOSAR ECUs on the same CAN
     network. The tool must verify that the configured CAN PDU IDs,
     signal layouts and CanTp parameters in the LW-BSW project are
     consistent with the DBC or ARXML description of the wider network,
     so the LW-BSW ECU can communicate correctly with Classic ECUs
     without integration-time surprises.
   :verification: SWE.6 qualification test | Analysis
   :jira: QDX-SWE-088

   When a DBC file or ARXML network description has been imported into
   the LW-BSW project, the LW-BSW validation engine **SHALL** verify
   bus-level compatibility by checking that: each configured CAN PDU
   ID in the LW-BSW project matches a PDU ID in the network
   description, each signal bit position and length matches the
   corresponding signal definition in the network description, and
   CAN baud rates are consistent. Mismatches **SHALL** be reported
   as WARNING diagnostics identifying the PDU or signal name, the
   value in the LW-BSW project and the value in the network
   description.

.. req:: LW-BSW AI-Assist Config Insight
   :id: QDX-SWE-089
   :parent: QDX-SYS-016
   :status: Draft
   :priority: High
   :rationale: The LW-BSW configuration idea (slide 6) explicitly shows
     AI Assist providing Config Insight covering scheduling map, resource
     consumption, race conditions and safety violations. This is a
     higher-level analytical capability than the fix-oriented AI tools
     in Classic and Adaptive — the LW-BSW AI layer must reason across
     the full 10-module configuration and provide interpretive insight,
     not just localised fix suggestions.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-089

   When the LW-BSW extension is installed and AI-Assist is active
   (per QDX-SWE-077), the Qorix Agent **SHALL** provide a Config
   Insight capability for LW-BSW projects. Config Insight **SHALL**
   be accessible from the LW-BSW designer and **SHALL** provide
   on-demand analysis responses covering:

   - **Scheduling assessment** — whether the current OS task
     configuration respects the task jitter (< 2 µs) and interrupt
     latency (< 2 µs) KPIs given the configured priorities and periods.
   - **Resource assessment** — whether the combined module
     configuration is trending toward or beyond the 150 KB ROM /
     30 KB RAM budget, with module-level contributors identified.
   - **Race condition explanation** — natural-language explanation
     of any detected shared-resource race conditions and suggested
     exclusive area or priority-ceiling remediation.
   - **Safety violation guidance** — explanation of any detected
     safety constraint violations and the relevant LW-BSW safety
     rule.

   Config Insight responses **SHALL** be read-only analytical output.
   Any suggested parameter changes **SHALL** be proposed as a
   structured OperationPlan subject to the user acceptance gate in
   QDX-SWE-048. The LW-BSW AI-Assist **SHALL** be gated by the
   LW-BSW extension per QDX-SWE-077.

.. req:: LW-BSW ICC-2 conformance constraint enforcement
   :id: QDX-SWE-090
   :parent: QDX-SYS-006
   :status: Draft
   :priority: High
   :rationale: LW-BSW targets ICC-2 (Implementation Conformance Class 2)
     rather than the full ICC-3 of Classic BSW. This means certain
     AUTOSAR Classic APIs, service ports and configuration constructs
     are not supported. The designer must prevent engineers from
     configuring ICC-3-only features that will not be available in
     the LW-BSW runtime, producing a clear error rather than a silent
     build failure.
   :verification: SWE.6 qualification test | Inspection
   :jira: QDX-SWE-090

   The LW-BSW designer **SHALL** restrict all parameter and feature
   selections to those supported within AUTOSAR ICC-2 conformance.
   Any configuration element that requires ICC-3 support (full AUTOSAR
   RTE with complex port-based communication, full OS conformance
   beyond OSEK SC-1, OBD / J1939 diagnostic services, FlexRay or
   Ethernet communication) **SHALL NOT** be offered as a selectable
   option in the LW-BSW designer. If an imported DEXT or ARXML
   contains ICC-3-only elements, each such element **SHALL** be
   reported as a WARNING during import identifying the element name
   and the ICC-2 limitation that prevents its use.


5.18 Project creation wizard
------------------------------

.. admonition:: Scope note

   The project creation wizard is the entry point for every new Qorix
   Developer project. It guides the engineer through a structured
   multi-step flow: stack type selection, platform or variant selection,
   template selection, project configuration (name, target hardware,
   module toggles), and a final review screen before the project is
   created. The wizard supports all supported stacks — Classic AUTOSAR,
   Adaptive AUTOSAR, Bootloader (BPCT), LW-BSW and Eclipse S-Core —
   each with a tailored step sequence appropriate to that stack.

.. req:: Project creation wizard — welcome and stack selection
   :id: QDX-SWE-091
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: The welcome screen is the first touchpoint for any new
     project. It must present all supported stack types clearly so the
     engineer can choose the correct one without consulting external
     documentation. Recent projects must also be accessible from this
     screen to support the common workflow of resuming work.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-091

   The project creation wizard **SHALL** present a welcome screen
   displaying all supported stack types as selectable cards, each
   showing the stack name, a brief description of its intended domain
   and the primary designer set it activates. The supported stack type
   cards **SHALL** include at minimum: AUTOSAR Classic, AUTOSAR
   Adaptive, Bootloader (BPCT), LW-BSW and Eclipse S-Core. The welcome
   screen **SHALL** also display a list of recent projects with stack
   type, last modified timestamp and designer count, allowing the
   engineer to re-open an existing project without navigating away.

.. req:: Classic AUTOSAR — platform version selection step
   :id: QDX-SWE-092
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: Classic AUTOSAR projects must declare a target platform
     version at creation time because the ARXML schema, BSW module set
     and YAML schema all depend on the selected release. Presenting
     this as a distinct step prevents misconfigured projects where the
     schema and the target toolchain are mismatched.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-092

   When AUTOSAR Classic is selected, the wizard **SHALL** present a
   platform version selection step offering at minimum:

   - **Classic H1 Foundation** — based on AUTOSAR R22-11, full BSW
     support (50+ modules), Classic COM (CAN, LIN, FlexRay), memory
     and diagnostics; recommended for new production programmes.
   - **Classic R4.x Legacy** — AUTOSAR 4.0–4.4 compatibility mode,
     migration path to H1, legacy toolchain support; module set
     limited to R4.x scope.

   The selected platform version **SHALL** be persisted in the project
   metadata and used to select the correct JSON Schema, validation
   rule set and ARXML Gateway target schema for the project lifetime.

.. req:: Classic AUTOSAR — template selection step
   :id: QDX-SWE-093
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: Pre-configured project templates reduce initial
     configuration effort for common ECU archetypes. A blank option
     must always be available. Templates must pre-populate YAML files
     with realistic starter configurations, not empty stubs.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-093

   The Classic AUTOSAR project creation wizard **SHALL** present a
   template selection step with the following built-in templates at
   minimum: Blank project (empty YAML stubs, full manual control),
   Powertrain Control (engine/transmission/throttle SWCs with CAN),
   Body Control (door/window/lighting/climate modules), Gateway ECU
   (CAN/LIN/FlexRay routing with NM), Sensor Fusion (multi-sensor
   acquisition for ADAS), and Actuator Control (motor/PWM/feedback).
   Selecting a template **SHALL** pre-populate the YAML source files
   created during scaffolding with the template's default values.

.. req:: Classic AUTOSAR — project configuration step
   :id: QDX-SWE-094
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: Project identity, target ECU definition and BSW module
     selection are the minimum information needed to produce a valid
     initial project structure. MCU family selection drives
     hardware-dependent defaults in the C3 and C5 designers.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-094

   The Classic AUTOSAR configuration step **SHALL** collect: project
   name (alphanumeric and underscore, real-time format validation),
   optional description, ECU name, microcontroller family selection
   (TC39x Infineon AURIX, S32K3 NXP, RH850 Renesas, TMS570 TI, STM32
   STMicroelectronics — each pre-populating flash page size and timer
   defaults), and BSW module toggles for: Communication Stack (CanIf,
   LinIf, PduR, Com), Diagnostics (DCM, DEM), Memory and NvM, and
   Watchdog and Safety (WdgM). Each toggle **SHALL** display a brief
   description of the modules it activates.

.. req:: Adaptive AUTOSAR — template selection step
   :id: QDX-SWE-095
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: Adaptive projects have a different starting point than
     Classic — the primary dimension is service topology and deployment
     context, not BSW module set. Templates must reflect real Adaptive
     AUTOSAR programme archetypes.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-095

   The Adaptive AUTOSAR project creation wizard **SHALL** present a
   template selection step with the following built-in templates at
   minimum: Blank project, Perception Pipeline (Radar/Camera/Fusion
   services with SOME/IP bindings), High-Performance Compute (multi-
   core with DDS), Central Gateway (multi-Ethernet routing), ADAS
   Controller (lane-keeping/ACC/sensor fusion pre-integrated), and
   Infotainment (media/connectivity/UI application templates).

.. req:: Adaptive AUTOSAR — project configuration step
   :id: QDX-SWE-096
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: Adaptive projects target high-performance compute
     hardware. Machine architecture and platform service selection
     at creation time drive the initial ``machine-design.yaml`` and
     ``platform-services.yaml`` content.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-096

   The Adaptive AUTOSAR configuration step **SHALL** collect: project
   name (alphanumeric and underscore, real-time validation), optional
   description, machine name, CPU architecture selection (ARM
   Cortex-A78 Quad-core, ARM Cortex-A76 Hexa-core, NVIDIA Orin
   12-core ARM+GPU, Intel x86\_64 8-core, Qualcomm Snapdragon
   Octa-core — each pre-populating core count, frequency and RAM
   defaults in ``machine-design.yaml``), and platform service toggles
   for ``ara::log``, ``ara::tsync``, ``ara::phm`` and ``ara::per``,
   each with a description of the service's role.

.. req:: Bootloader (BPCT) — template selection step
   :id: QDX-SWE-097
   :parent: QDX-SYS-002
   :status: Draft
   :priority: Medium
   :rationale: Common bootloader configurations recur across programmes.
     Pre-configured templates accelerate project creation and reduce
     the risk of misconfigured initial VR_NNN constraints.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-097

   The Bootloader project creation wizard **SHALL** present a template
   selection step with the following built-in templates at minimum:
   Blank project (safe defaults, full manual control), CAN
   Single-Channel FBL (500 kbps, UDS addresses pre-configured, no
   secure boot), CAN-FD High-Speed FBL (2 Mbit/s data phase, extended
   PDU size), Secure Boot FBL (RSA2048 + AES256, HSM key store region
   pre-defined in memory map), and Multi-Channel Gateway FBL (CAN
   primary + optional LIN, gateway routing pre-configured).

.. req:: Bootloader (BPCT) — MCU and project configuration step
   :id: QDX-SWE-098
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: The target MCU family is the primary selection for
     bootloader projects — it drives flash page size, erase timeout,
     SPI clock constraints and timer resolution across all six BD
     designers. Selecting MCU family, communication protocol and
     security profile at creation time prevents downstream constraint
     violations in BD5 and BD6 that are expensive to resolve after
     the memory map is defined.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-098

   When Bootloader (BPCT) is selected, the wizard **SHALL** collect:

   - **FBL project identifier** — the ``FBL_PROJECT_NAME`` macro
     value, validated as uppercase alphanumeric with underscores.
   - **ECU ID** — the ``FBL_ECU_ID`` hexadecimal value.
   - **Version triplet** — ``FBL_VERSION_MAJOR``,
     ``FBL_VERSION_MINOR``, ``FBL_VERSION_PATCH``.
   - **MCU family** — selection from: TC3xx (Infineon AURIX),
     TC4xx (Infineon AURIX Gen2), RH850 (Renesas), S32K1xx (NXP),
     S32K3xx (NXP), S32Gx (NXP). On selection the wizard **SHALL**
     immediately display the MCU-derived hardware defaults: flash
     page size, maximum SPI clock, timer resolution, RAM capacity
     and Flash capacity — applied to all six BPCT YAML files.
   - **Communication protocol** — CAN (mandatory, always enabled),
     with CAN-FD and LIN as optional additions.
   - **Security profile** — None (no secure boot), Secure Boot only
     (RSA2048 default), or Full Security (RSA2048 + AES256
     encryption), pre-populating ``bl-security.yaml`` accordingly.

   On completion the wizard **SHALL** scaffold the six BPCT source
   files (``bl-project.yaml``, ``bl-communication.yaml``,
   ``bl-memory.yaml``, ``bl-core.yaml``, ``bl-hardware.yaml``,
   ``bl-security.yaml``) with MCU-derived defaults and activate
   the BD1–BD6 designer tabs.

.. req:: LW-BSW — project configuration step
   :id: QDX-SWE-099
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: LW-BSW project creation must distinguish itself from
     Full Classic at the wizard level. The engineer selects LW-BSW
     explicitly and the wizard reflects the constrained module scope
     (10 modules, ICC-2). DEXT and DBC import is available at creation
     time to pre-populate the configuration baseline and reduce the
     20-person-day integration overhead to the 6-person-day target.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-099

   When LW-BSW is selected, the wizard **SHALL** collect: project
   name (alphanumeric and underscore), optional description, MCU
   family (same set as Classic — MCU applies ICC-2 resource budget
   defaults of ROM ≤ 150 KB and RAM ≤ 30 KB), optional DEXT XML
   and/or DBC import file (with a preview of elements that will map
   successfully and those that will be reported as WARNING),
   communication scope (CAN mandatory; LIN optional; FlexRay and
   Ethernet **SHALL NOT** be offered), and a read-only module scope
   confirmation panel listing the 10 active LW-BSW modules (COM,
   Diag, CanTp, CanIf, CDD, OS, IOHAB, EMM, NM, NVRAM) and the
   ICC-2 conformance level.

.. req:: Project creation — review and confirmation step
   :id: QDX-SWE-100
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: A review screen is the final opportunity for the
     engineer to verify all selections before YAML files are written
     and designer tabs are activated. It must show the full set of
     designers and pre-configured components that will be created —
     not just field values.
   :verification: SWE.6 qualification test | Demonstration
   :jira: QDX-SWE-100

   The final step of the project creation wizard for all stack types
   **SHALL** display a read-only review screen showing: stack type
   and variant (e.g. AUTOSAR Classic H1, Bootloader BPCT TC3xx),
   template selected, project name and target hardware, the complete
   list of designer tabs that will be activated with their short codes
   (C1–C6, A1–A6, BD1–BD6) and names, and a bulleted list of YAML
   elements pre-populated by the selected template. A "Create Project"
   action **SHALL** trigger scaffolding, display a progress indicator
   describing each file being created, and on completion navigate
   directly into the project workspace with all activated designer
   tabs visible.

.. req:: Project creation — step navigation and per-stack sequences
   :id: QDX-SWE-101
   :parent: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: A multi-step wizard must enforce forward progress only
     when each step is valid, allow backward navigation without data
     loss, and show the engineer their current position at all times.
     Each stack has a different number of steps reflecting its
     configuration complexity.
   :verification: SWE.6 qualification test
   :jira: QDX-SWE-101

   The project creation wizard **SHALL** display a persistent step
   indicator showing all steps in the current stack's sequence and
   highlighting the active step. The "Continue" action **SHALL** be
   disabled when any required field on the current step is empty or
   invalid, with an inline error message identifying the issue. The
   "Back" action **SHALL** navigate to the previous step preserving
   all entered values. The step sequence **SHALL** be:

   - **Classic AUTOSAR**: 5 steps — Type → Platform → Template →
     Configuration → Review.
   - **Adaptive AUTOSAR**: 4 steps — Type → Template →
     Configuration → Review.
   - **Bootloader (BPCT)**: 4 steps — Type → Template →
     MCU Configuration → Review.
   - **LW-BSW**: 4 steps — Type → Template → Configuration →
     Review.
   - **Eclipse S-Core**: 3 steps — Type → Configuration → Review.


6. Software Requirements Traceability Matrix
=============================================

.. note::
   This is the ASPICE SWE.1 ↔ SWE.6 traceability record.
   ``SWE.5 integ.`` column identifies integration-level tests for
   interface boundaries (WASM bridge, Domain Service API, GraphQL,
   BPCT and LW-BSW generation engines, project creation wizard).

.. list-table::
   :widths: 15 30 14 14 12 5
   :header-rows: 1

   * - SW Req ID
     - Title
     - Parent SYS req
     - SWE.6 qual. test
     - SWE.5 integ. test
     - Status
   * - QDX-SWE-001
     - Multi-stack workspace initialisation
     - QDX-SYS-001
     - QDX-QT-001
     - —
     - Draft
   * - QDX-SWE-002
     - Per-stack project scaffolding
     - QDX-SYS-002
     - QDX-QT-002
     - —
     - Draft
   * - QDX-SWE-003
     - Source/output directory separation
     - QDX-SYS-044
     - QDX-QT-003
     - —
     - Draft
   * - QDX-SWE-004
     - Version-control-friendly YAML persistence
     - QDX-SYS-019
     - QDX-QT-004
     - —
     - Draft
   * - QDX-SWE-005
     - Atomic save with integrity protection
     - QDX-SYS-033
     - QDX-QT-005
     - —
     - Draft
   * - QDX-SWE-006
     - YAML editor with schema-based completion
     - QDX-SYS-003
     - QDX-QT-006
     - —
     - Draft
   * - QDX-SWE-007
     - Language server protocol integration
     - QDX-SYS-029
     - QDX-QT-007
     - QDX-IT-001
     - Draft
   * - QDX-SWE-008
     - Localised atomic model mutations
     - QDX-SYS-013
     - QDX-QT-008
     - —
     - Draft
   * - QDX-SWE-009
     - C1 — SWC and interface designer
     - QDX-SYS-004
     - QDX-QT-009
     - —
     - Draft
   * - QDX-SWE-010
     - C1 — SWC runnable definition
     - QDX-SYS-004
     - QDX-QT-010
     - —
     - Draft
   * - QDX-SWE-011
     - C2 — Signals and ComStack designer
     - QDX-SYS-004
     - QDX-QT-011
     - —
     - Draft
   * - QDX-SWE-012
     - C3 — ECU and BSW designer
     - QDX-SYS-004
     - QDX-QT-012
     - —
     - Draft
   * - QDX-SWE-013
     - C4 — OS and scheduling designer
     - QDX-SYS-004
     - QDX-QT-013
     - —
     - Draft
   * - QDX-SWE-014
     - C5 — Memory and NvM designer
     - QDX-SYS-004
     - QDX-QT-014
     - —
     - Draft
   * - QDX-SWE-015
     - C6 — RTE and mapping designer
     - QDX-SYS-004
     - QDX-QT-015
     - —
     - Draft
   * - QDX-SWE-016
     - Unmapped element detection in C6
     - QDX-SYS-007
     - QDX-QT-016
     - —
     - Draft
   * - QDX-SWE-017
     - A1 — Application and service designer
     - QDX-SYS-004
     - QDX-QT-017
     - —
     - Draft
   * - QDX-SWE-018
     - A1 — Service cross-reference tracking
     - QDX-SYS-008
     - QDX-QT-018
     - —
     - Draft
   * - QDX-SWE-019
     - A2 — Communication and service instance de
     - QDX-SYS-004
     - QDX-QT-019
     - QDX-IT-011
     - Draft
   * - QDX-SWE-020
     - A2 — Service binding completeness validati
     - QDX-SYS-007
     - QDX-QT-020
     - —
     - Draft
   * - QDX-SWE-021
     - A3 — Machine design designer
     - QDX-SYS-004
     - QDX-QT-021
     - —
     - Draft
   * - QDX-SWE-022
     - A3 — Disabled core reference detection
     - QDX-SYS-007
     - QDX-QT-022
     - —
     - Draft
   * - QDX-SWE-023
     - A4 — Platform services designer
     - QDX-SYS-004
     - QDX-QT-023
     - —
     - Draft
   * - QDX-SWE-024
     - A5 — Execution management designer
     - QDX-SYS-004
     - QDX-QT-024
     - —
     - Draft
   * - QDX-SWE-025
     - A5 — Scheduling conflict detection
     - QDX-SYS-007
     - QDX-QT-025
     - —
     - Draft
   * - QDX-SWE-026
     - A6 — Deployment designer
     - QDX-SYS-004
     - QDX-QT-026
     - —
     - Draft
   * - QDX-SWE-027
     - A6 — Resource constraint validation
     - QDX-SYS-007
     - QDX-QT-027
     - —
     - Draft
   * - QDX-SWE-028
     - Adaptive cross-designer consistency check
     - QDX-SYS-020
     - QDX-QT-028
     - QDX-IT-012
     - Draft
   * - QDX-SWE-029
     - Designer-to-YAML synchronisation
     - QDX-SYS-005
     - QDX-QT-029
     - QDX-IT-002
     - Draft
   * - QDX-SWE-030
     - YAML-to-designer synchronisation
     - QDX-SYS-005
     - QDX-QT-030
     - QDX-IT-002
     - Draft
   * - QDX-SWE-031
     - In-IDE WASM fast validation
     - QDX-SYS-006
     - QDX-QT-031
     - QDX-IT-003
     - Draft
   * - QDX-SWE-032
     - Deep semantic validation via domain servic
     - QDX-SYS-007
     - QDX-QT-032
     - QDX-IT-004
     - Draft
   * - QDX-SWE-033
     - Cross-file reference resolution
     - QDX-SYS-008
     - QDX-QT-033
     - —
     - Draft
   * - QDX-SWE-034
     - Validation-gated publication
     - QDX-SYS-036
     - QDX-QT-034
     - —
     - Draft
   * - QDX-SWE-035
     - Workspace-level consistency check
     - QDX-SYS-020
     - QDX-QT-035
     - QDX-IT-005
     - Draft
   * - QDX-SWE-036
     - Diagnostics panel presentation
     - QDX-SYS-014
     - QDX-QT-036
     - —
     - Draft
   * - QDX-SWE-037
     - Usable diagnostic message quality
     - QDX-SYS-042
     - QDX-QT-037
     - —
     - Draft
   * - QDX-SWE-038
     - Deterministic ARXML generation
     - QDX-SYS-009
     - QDX-QT-038
     - QDX-IT-006
     - Draft
   * - QDX-SWE-039
     - ARXML export via ARTOP GraphQL gateway
     - QDX-SYS-010
     - QDX-QT-039
     - QDX-IT-007
     - Draft
   * - QDX-SWE-040
     - ARXML import and lossy-conversion reportin
     - QDX-SYS-011
     - QDX-QT-040
     - QDX-IT-007
     - Draft
   * - QDX-SWE-041
     - Generation provenance recording
     - QDX-SYS-015
     - QDX-QT-041
     - —
     - Draft
   * - QDX-SWE-042
     - External artefact compatibility status rep
     - QDX-SYS-030
     - QDX-QT-042
     - —
     - Draft
   * - QDX-SWE-043
     - GraphQL API contract for model access
     - QDX-SYS-012
     - QDX-QT-043
     - QDX-IT-008
     - Draft
   * - QDX-SWE-044
     - Search and navigation API
     - QDX-SYS-018
     - QDX-QT-044
     - —
     - Draft
   * - QDX-SWE-045
     - Headless CLI for CI validation and generat
     - QDX-SYS-031
     - QDX-QT-045
     - QDX-IT-009
     - Draft
   * - QDX-SWE-046
     - Same Rust core for all build targets
     - QDX-SYS-031
     - QDX-QT-046
     - —
     - Draft
   * - QDX-SWE-047
     - AI-generated OperationPlan — no direct YAM
     - QDX-SYS-016
     - QDX-QT-047
     - QDX-IT-010
     - Draft
   * - QDX-SWE-048
     - User acceptance gate for AI suggestions
     - QDX-SYS-017
     - QDX-QT-048
     - —
     - Draft
   * - QDX-SWE-049
     - Post-acceptance WASM re-validation
     - QDX-SYS-006
     - QDX-QT-049
     - —
     - Draft
   * - QDX-SWE-050
     - Intent Router — Classic vs Adaptive dispat
     - QDX-SYS-016
     - QDX-QT-050
     - —
     - Draft
   * - QDX-SWE-051
     - Configurable AI data transmission control
     - QDX-SYS-037
     - QDX-QT-051
     - —
     - Draft
   * - QDX-SWE-052
     - Audit log for critical user actions
     - QDX-SYS-035
     - QDX-QT-052
     - —
     - Draft
   * - QDX-SWE-053
     - Access control for privileged operations
     - QDX-SYS-034
     - QDX-QT-053
     - —
     - Draft
   * - QDX-SWE-054
     - Workspace open time
     - QDX-SYS-022
     - QDX-QT-054
     - —
     - Draft
   * - QDX-SWE-055
     - WASM validation latency
     - QDX-SYS-023
     - QDX-QT-055
     - —
     - Draft
   * - QDX-SWE-056
     - Search response time
     - QDX-SYS-024
     - QDX-QT-056
     - —
     - Draft
   * - QDX-SWE-057
     - ARXML generation completion time
     - QDX-SYS-025
     - QDX-QT-057
     - —
     - Draft
   * - QDX-SWE-058
     - Non-blocking UI for long-running operation
     - QDX-SYS-026
     - QDX-QT-058
     - —
     - Draft
   * - QDX-SWE-059
     - Dual IDE host support — VS Code and Theia
     - QDX-SYS-027
     - QDX-QT-059
     - —
     - Draft
   * - QDX-SWE-060
     - Offline local authoring and validation
     - QDX-SYS-043
     - QDX-QT-060
     - —
     - Draft
   * - QDX-SWE-061
     - Extension mechanism without core modificat
     - QDX-SYS-041
     - QDX-QT-061
     - —
     - Draft
   * - QDX-SWE-062
     - Backward-compatible project migration
     - QDX-SYS-040
     - QDX-QT-062
     - —
     - Draft
   * - QDX-SWE-063
     - BPCT project structure and MCU selection (
     - QDX-SYS-002
     - QDX-QT-063
     - —
     - Draft
   * - QDX-SWE-064
     - BPCT communication channel configuration (
     - QDX-SYS-004
     - QDX-QT-064
     - —
     - Draft
   * - QDX-SWE-065
     - BPCT memory map and NvM block configuratio
     - QDX-SYS-004
     - QDX-QT-065
     - —
     - Draft
   * - QDX-SWE-066
     - BPCT flash block size constraint validatio
     - QDX-SYS-007
     - QDX-QT-066
     - —
     - Draft
   * - QDX-SWE-067
     - BPCT core parameters and UDS session confi
     - QDX-SYS-004
     - QDX-QT-067
     - —
     - Draft
   * - QDX-SWE-068
     - BPCT timing, hardware and watchdog configu
     - QDX-SYS-004
     - QDX-QT-068
     - —
     - Draft
   * - QDX-SWE-069
     - BPCT watchdog timeout cross-constraint val
     - QDX-SYS-007
     - QDX-QT-069
     - —
     - Draft
   * - QDX-SWE-070
     - BPCT cross-designer timing dependency prop
     - QDX-SYS-008
     - QDX-QT-070
     - —
     - Draft
   * - QDX-SWE-071
     - BPCT crypto and secure boot configuration 
     - QDX-SYS-004
     - QDX-QT-071
     - —
     - Draft
   * - QDX-SWE-072
     - BPCT weak cryptographic algorithm detectio
     - QDX-SYS-007
     - QDX-QT-072
     - —
     - Draft
   * - QDX-SWE-073
     - BPCT key address placement validation (BD6
     - QDX-SYS-007
     - QDX-QT-073
     - —
     - Draft
   * - QDX-SWE-074
     - BPCT validation rule engine (cross-designe
     - QDX-SYS-020
     - QDX-QT-074
     - QDX-IT-013
     - Draft
   * - QDX-SWE-075
     - BPCT C header and Makefile generation
     - QDX-SYS-009
     - QDX-QT-075
     - QDX-IT-014
     - Draft
   * - QDX-SWE-076
     - BPCT output preview in BD1 designer
     - QDX-SYS-014
     - QDX-QT-076
     - —
     - Draft
   * - QDX-SWE-077
     - AI-Assist availability gated by domain ext
     - QDX-SYS-016
     - QDX-QT-077
     - —
     - Draft
   * - QDX-SWE-078
     - AI-Assist context injection per domain
     - QDX-SYS-016
     - QDX-QT-078
     - QDX-IT-015
     - Draft
   * - QDX-SWE-079
     - AI-Assist OperationPlan scoped to active d
     - QDX-SYS-017
     - QDX-QT-079
     - —
     - Draft
   * - QDX-SWE-080
     - AI-Assist BPCT domain tools
     - QDX-SYS-016
     - QDX-QT-080
     - —
     - Draft
   * - QDX-SWE-081
     - LW-BSW project creation and ECU/DEXT impor
     - QDX-SYS-002
     - QDX-QT-081
     - QDX-IT-016
     - Draft
   * - QDX-SWE-082
     - LW-BSW module configuration — ten BSW modu
     - QDX-SYS-004
     - QDX-QT-082
     - —
     - Draft
   * - QDX-SWE-083
     - LW-BSW CAN and optional LIN communication 
     - QDX-SYS-004
     - QDX-QT-083
     - —
     - Draft
   * - QDX-SWE-084
     - LW-BSW resource budget validation
     - QDX-SYS-007
     - QDX-QT-084
     - —
     - Draft
   * - QDX-SWE-085
     - LW-BSW OS scheduling map and race conditio
     - QDX-SYS-007
     - QDX-QT-085
     - —
     - Draft
   * - QDX-SWE-086
     - LW-BSW Config Report generation
     - QDX-SYS-015
     - QDX-QT-086
     - —
     - Draft
   * - QDX-SWE-087
     - LW-BSW module configuration ``.h`` and ``.
     - QDX-SYS-009
     - QDX-QT-087
     - QDX-IT-017
     - Draft
   * - QDX-SWE-088
     - LW-BSW bus-level compatibility check with 
     - QDX-SYS-007
     - QDX-QT-088
     - —
     - Draft
   * - QDX-SWE-089
     - LW-BSW AI-Assist Config Insight
     - QDX-SYS-016
     - QDX-QT-089
     - QDX-IT-018
     - Draft
   * - QDX-SWE-090
     - LW-BSW ICC-2 conformance constraint enforc
     - QDX-SYS-006
     - QDX-QT-090
     - —
     - Draft
   * - QDX-SWE-091
     - Project creation wizard — welcome and stac
     - QDX-SYS-002
     - QDX-QT-091
     - QDX-IT-019
     - Draft
   * - QDX-SWE-092
     - Classic AUTOSAR — platform version selecti
     - QDX-SYS-002
     - QDX-QT-092
     - —
     - Draft
   * - QDX-SWE-093
     - Classic AUTOSAR — template selection step
     - QDX-SYS-002
     - QDX-QT-093
     - —
     - Draft
   * - QDX-SWE-094
     - Classic AUTOSAR — project configuration st
     - QDX-SYS-002
     - QDX-QT-094
     - —
     - Draft
   * - QDX-SWE-095
     - Adaptive AUTOSAR — template selection step
     - QDX-SYS-002
     - QDX-QT-095
     - —
     - Draft
   * - QDX-SWE-096
     - Adaptive AUTOSAR — project configuration s
     - QDX-SYS-002
     - QDX-QT-096
     - —
     - Draft
   * - QDX-SWE-097
     - Bootloader (BPCT) — template selection ste
     - QDX-SYS-002
     - QDX-QT-097
     - —
     - Draft
   * - QDX-SWE-098
     - Bootloader (BPCT) — MCU and project config
     - QDX-SYS-002
     - QDX-QT-098
     - QDX-IT-020
     - Draft
   * - QDX-SWE-099
     - LW-BSW — project configuration step
     - QDX-SYS-002
     - QDX-QT-099
     - —
     - Draft
   * - QDX-SWE-100
     - Project creation — review and confirmation
     - QDX-SYS-002
     - QDX-QT-100
     - QDX-IT-021
     - Draft
   * - QDX-SWE-101
     - Project creation — step navigation and per
     - QDX-SYS-002
     - QDX-QT-101
     - —
     - Draft


7. Open Issues and TBDs
========================

.. list-table::
   :widths: 15 50 20 15
   :header-rows: 1

   * - Issue ID
     - Description
     - Owner
     - Target date
   * - TBD-SWE-001
     - Define the benchmark workspace specification (file count, element
       count, YAML line count) for performance requirements QDX-SWE-054,
       023, 024, 025. Depends on TBD-SYS-001.
     - Architecture + QA
     - 2026-04-15
   * - TBD-SWE-002
     - Confirm supported AUTOSAR Classic schema versions (4.2.2 / 4.3.1)
       and Adaptive schema versions (R20-11 / R23-11 / R24-11) for each
       release baseline. Drives QDX-SWE-039 and QDX-SWE-040.
     - Domain Architects
     - 2026-04-22
   * - TBD-SWE-003
     - Define the exact GraphQL schema SDL publication mechanism and
       versioning policy for QDX-SWE-043. Confirm whether SDL is
       co-located in the ARXML Gateway repo or the monorepo docs.
     - ARXML Gateway Lead
     - 2026-04-22
   * - TBD-SWE-004
     - RESOLVED v0.4.0 — Bootloader BPCT requirements added as
       QDX-SWE-063 through QDX-SWE-076 in section 5.15. The BPCT
       extension AI-Assist tools added as QDX-SWE-077 through 080
       in section 5.16.
     - Bootloader lead
     - Closed 2026-03-31
   * - TBD-SWE-007
     - Specify the Performance stack YAML file structure and designer
       requirements (profiling, benchmark configuration, trace targets)
       — not yet covered; no mockup available. Note: LW-BSW has been
       added as a separate product line (section 5.17, QDX-SWE-081
       through 090) and is distinct from the Performance stack.
       Requires a dedicated SWE.1 section or companion document
       QDX-SWE-DOC-PERF-001.
     - Performance lead
     - 2026-05-15
   * - TBD-SWE-005
     - Finalise provenance metadata file format (JSON / YAML / SPDX-
       inspired) and confirm storage location relative to generated ARXML
       for QDX-SWE-041.
     - Architecture Team
     - 2026-04-22
   * - TBD-SWE-006
     - Confirm approver names and approval date for formal release
       baseline of this document. Depends on TBD-SYS-005.
     - Program Management
     - 2026-04-10


.. _swe_changelog:

8. Changelog
=============

.. list-table::
   :widths: 15 15 20 50
   :header-rows: 1

   * - Version
     - Date
     - Author
     - Change description
   * - 0.6.0
     - 2026-03-31
     - Qorix Platform Engineering   
     - Added section 5.18: Project Creation Wizard requirements
       QDX-SWE-091 through QDX-SWE-101. Covers: welcome and stack
       selection (091), Classic platform version selection (092),
       Classic template selection (093), Classic configuration step
       with MCU family and BSW module toggles (094), Adaptive template
       selection (095), Adaptive configuration step with CPU
       architecture and platform services (096), Bootloader BPCT MCU
       and project configuration step including FBL project ID,
       communication protocol and security profile (097), Bootloader
       template selection (098), LW-BSW configuration step with DEXT
       import and ICC-2 scope confirmation (099), review and
       confirmation step for all stacks (100), step navigation and
       per-stack step sequence definition (101). Traceability matrix
       expanded to 101 rows. Bootloader project creation gap from
       project-creation.html mockup resolved.
   * - 0.5.0
     - 2026-03-31
     - Qorix Platform Engineering   
     - Added LW-BSW (Light Weight BSW) product line requirements
       QDX-SWE-081 through QDX-SWE-090 in section 5.17. Covers:
       ECU/DEXT import (081), 10-module BSW configuration (082),
       CAN/LIN communication with protocol scope enforcement (083),
       resource budget KPI validation — ROM ≤ 150 KB / RAM ≤ 30 KB
       / CPU < 10% (084), OS scheduling map and race condition
       analysis (085), Config Report generation (086), module .h/.c
       generation (087), bus-level Classic AUTOSAR compatibility
       check (088), AI-Assist Config Insight (089), ICC-2 conformance
       constraint enforcement (090). Traceability matrix expanded to
       90 rows (QDX-QT-081 through QDX-QT-090, QDX-IT-016 through
       018). Updated TBD-SWE-007 to clarify LW-BSW is separate from
       Performance stack.
   * - 0.4.0
     - 2026-03-31
     - Qorix Platform Engineering   
     - Added Bootloader BPCT designer requirements QDX-SWE-063 through
       QDX-SWE-076 (section 5.15): BD1–BD6 designers, cross-designer
       timing chain, VR_NNN validation rules (VR_003, VR_007, VR_013,
       VR_016), C header/Makefile generation, output preview. Added
       AI-Assist extension-gated requirements QDX-SWE-077 through
       QDX-SWE-080 (section 5.16): per-domain extension gate, context
       injection, scoped OperationPlan, BPCT MCP tools. Resolved
       TBD-SWE-004 (Bootloader). Traceability matrix expanded to 80
       rows (QDX-QT-063 through QDX-QT-080, QDX-IT-013 through 015).
   * - 0.3.0
     - 2026-03-31
     - Qorix Platform Engineering   
     - Renumbered all requirement IDs to clean sequential QDX-SWE-001
       through QDX-SWE-062. Removed all alpha suffixes (003a, 004a–m2,
       005b, 007a, 016b, 017b, 020a, 031b) and re-grouped by functional
       area. Traceability matrix rebuilt from corrected IDs. No
       requirement content changed — ID renaming only.
   * - 0.2.0
     - 2026-03-31
     - Qorix Platform Engineering   
     - Added full Adaptive AUTOSAR designer requirements (A1–A6):
       QDX-SWE-048 through 004m2 and QDX-SWE-028. Replaced single
       placeholder QDX-SWE-048 with seven designer-level requirements
       and five associated validation requirements derived from the
       Adaptive AUTOSAR designer mockup (HighPerformanceCompute_v2
       project). Updated traceability matrix with 12 new rows
       (QDX-QT-050 through QDX-QT-059, QDX-IT-011, QDX-IT-012).
       Resolved TBD-SWE-004 for Adaptive; split into TBD-SWE-004
       (Bootloader) and TBD-SWE-007 (Performance).
   * - 0.1.0
     - 2026-03-30
     - Qorix Platform Engineering   
     - Initial SWE.1 draft derived from QDX-SRS-001 (SYS.2),
       Qorix Developer C4 architecture and Classic designer mockup.
       Full traceability matrix populated. Bootloader and Performance
       stacks marked TBD-SWE-004.


----

*This document is version-controlled in Git at*
``docs/20-swe.1/platform/sw_requirements.rst``.
*Authoritative version is HEAD of* ``main``.
*All changes require a pull request with minimum two approvals from
CODEOWNERS. Requirement ID retirement requires Chief Architect and Product Program Manager sign-off.*
