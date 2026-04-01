.. _glossary_overview:

Glossary
========

.. raw:: html

   <p style="font-size: 1.1rem; line-height: 1.8; max-width: 740px;
             color: var(--color-foreground-secondary, #444); margin-bottom: 2rem;">
     Authoritative definitions for every acronym, domain term and Qorix
     Developer concept used across the documentation set. Terms defined here
     are the canonical source — if a term in a requirement, design document or
     test specification diverges from this glossary, the glossary wins.
   </p>

.. glossary::
   :sorted:

   ADC
      Analog-to-Digital Converter. Peripheral type abstracted by the IOHAB
      BSW module in LW-BSW and Classic AUTOSAR stacks.

   ADR
      Architecture Decision Record. A permanent, numbered record of a
      significant architectural decision made during the development of
      Qorix Developer. ADRs are never deleted — superseded decisions are
      marked Superseded and the superseding ADR is referenced. See
      :ref:`sw_architecture` §5.

   AI-Assist
      Qorix Developer capability providing domain-aware, explainable
      engineering assistance through the Qorix Agent. Activated per designer
      domain when the corresponding domain extension is installed. All
      suggestions are presented as a typed ``OperationPlan`` requiring
      explicit engineer acceptance before any YAML file is modified. See
      also: :term:`Engineer-in-the-Loop`, :term:`OperationPlan`.

   ara::com
      AUTOSAR Adaptive communication API — the service-oriented middleware
      API for inter-application communication on the Adaptive Platform,
      supporting SOME/IP and DDS transports.

   ara::log
      AUTOSAR Adaptive logging framework. Centralised log output service
      configured in the A4 Platform Services designer with per-logger name,
      level and output target settings.

   ara::per
      AUTOSAR Adaptive Persistency service. Key-value storage for application
      data, configured in the A4 designer with storage area count and schema
      definitions.

   ara::phm
      AUTOSAR Adaptive Platform Health Management. Supervision and health
      monitoring service configured in the A4 designer with health channel
      definitions.

   ara::tsync
      AUTOSAR Adaptive Time Synchronisation service. Network time protocol
      integration for distributed Adaptive systems, configured in the A4
      Platform Services designer.

   ARTOP
      AUTOSAR Tool Platform. Eclipse-based framework providing the canonical
      AUTOSAR metamodel and ARXML read/write capability. Used by the ARXML
      Gateway (Spring Boot + ARTOP) as the sole path for ARXML import and
      export. The Rust domain crates have zero dependency on ARTOP.

   ARXML
      AUTOSAR XML. The schema-defined exchange format for AUTOSAR engineering
      models, consumed and produced exclusively via the ARTOP-based ARXML
      Gateway in Qorix Developer. ARXML is never used as a source format —
      YAML is the canonical model.

   ASPICE
      Automotive SPICE (Software Process Improvement and Capability
      dEtermination). Process assessment framework for automotive software
      suppliers. Qorix Developer produces ASPICE-compliant work products at
      SYS.2, SWE.1, SWE.2, SWE.3, SWE.4, SWE.5 and SWE.6 as natural
      by-products of the engineering workflow.

   AUTOSAR
      AUTomotive Open System ARchitecture. Standardised software framework
      for ECU software development. Qorix Developer supports Classic AUTOSAR
      (BSW, RTE, COM stack) and Adaptive AUTOSAR (service-oriented, ara::com,
      manifests).

   BD1–BD6
      Six Bootloader (BPCT) designer tabs in Qorix Developer:
      BD1 Project & MCU, BD2 Communication, BD3 Memory & Flash,
      BD4 Core & Diagnostics, BD5 Timing & Hardware, BD6 Crypto & Security.

   BPCT
      Bootloader Parameters Configurator Tool. The Qorix Developer subsystem
      for authoring, validating and generating Flash Bootloader (FBL)
      configuration artefacts across six YAML source files and six BD
      designers (BD1–BD6). Produces ``cfg.h``, ``cfg.c`` and ``Makefile``.

   BSW
      Basic Software. The standardised lower layers of the AUTOSAR Classic
      Platform stack, including OS, COM, diagnostics, memory and hardware
      abstraction modules.

   C1–C6
      Six Classic AUTOSAR designer tabs in Qorix Developer:
      C1 SWC & Interface, C2 Signals & ComStack, C3 ECU & BSW,
      C4 OS & Scheduling, C5 Memory & NvM, C6 RTE & Mapping.

   CAN
      Controller Area Network. Mandatory communication bus protocol for
      Classic AUTOSAR and BPCT projects.

   CAN-FD
      CAN with Flexible Data-rate (ISO 11898-1). Higher-bandwidth variant
      supporting data phases up to 8 Mbit/s. Optional in BPCT projects.

   CanIf
      CAN Interface. AUTOSAR Classic BSW module providing hardware
      abstraction for the CAN controller and routing PDUs to the COM stack.

   CDD
      Complex Device Driver. AUTOSAR Classic BSW module for ECU-specific
      implementations including I2C, SPI, sensor and actuator interfaces.

   CLI
      Command-Line Interface. The ``qorix_cli`` binary providing ``validate``
      and ``generate`` subcommands for headless CI/CD pipeline use. Built
      from the same Rust crate tree as the Domain Service and WASM module.

   COM
      Communication module. AUTOSAR Classic BSW module managing signal
      packing, unpacking, data conversion, periodic transmission, deadline
      monitoring and safety callbacks. One of the ten LW-BSW modules.

   Command Bus
      IDE Layer component that translates designer interactions (drag, drop,
      property edits) into typed ``core::ops`` operations and dispatches them
      through the WASM Bridge.

   Config-as-Code
      Development paradigm where all engineering configuration is expressed
      in human-readable YAML files committed to version control. Every
      parameter change is a Git commit; every release is a tagged SHA.

   Config Insight
      LW-BSW-specific AI-Assist capability providing analytical responses
      covering scheduling assessment, resource budget evaluation, race
      condition explanation and safety violation guidance across the full
      10-module configuration.

   Config Report
      Structured output file generated by the LW-BSW pipeline alongside
      module ``.h`` and ``.c`` files. Contains: OS scheduling map,
      per-module ROM/RAM/CPU resource budget vs. target KPIs, static race
      condition detections and safety violation flags.

   CODEOWNERS
      Git repository configuration file declaring mandatory reviewers for
      specific file paths. In Qorix Developer, requirement changes require
      architecture review and design changes require crate-lead sign-off.

   Core Affinity
      Assignment of a process or runnable to one or more specific CPU cores
      on a target machine. Configured in A5 (Adaptive) and validated against
      the core count declared in A3.

   DBC
      Database CAN file. Legacy non-AUTOSAR format describing CAN network
      signals, messages and nodes. Supported as an import source in LW-BSW
      project creation.

   DCM
      Diagnostic Communication Manager. AUTOSAR Classic BSW module
      implementing the UDS protocol (ISO 14229). One of the 10 LW-BSW
      modules.

   DEM
      Diagnostic Event Manager. AUTOSAR Classic BSW module managing DTCs in
      non-volatile memory.

   Deterministic Generation
      Property that identical validated YAML inputs with the same tool version
      produce byte-identical generated artefacts. No timestamps, random GUIDs
      or environment-dependent serialisation. Enforced by ADR-008.

   DEXT
      Data EXTraction file. XML-format ECU description file exported from
      AUTOSAR toolchains (e.g. Tresos, DaVinci). Used as an import source in
      LW-BSW project creation to pre-populate the YAML configuration baseline.

   Diagnostic
      A structured validation finding produced by the Rust domain validation
      rule engine. Each diagnostic carries: ``severity`` (INFO, WARNING,
      ERROR), ``code`` (e.g. ``"CLASSIC-VAL-001"``), ``message`` (actionable,
      human-readable text), ``file_path`` and ``yaml_path``.

   DiagnosticList
      Ordered collection of ``Diagnostic`` structs returned by a validation
      pass. An empty ``DiagnosticList`` means the model is valid for the
      executed rule set.

   DIO
      Digital Input/Output. Peripheral type abstracted by the IOHAB module.

   Domain Core
      The shared Rust crate tree (``core::*``, ``classic::*``,
      ``adaptive::*``, ``bpct::*``, ``lwbsw::*``) that owns all domain
      models, validation rules, operations, migrations and generation logic.
      Compiled to three build targets without altering business logic.

   Domain Extension
      Installable Qorix Developer extension that activates the designer set
      and MCP tool registry for a specific stack domain. Classic extension
      activates C1–C6 and Classic AI-Assist; Adaptive activates A1–A6;
      BPCT activates BD1–BD6.

   DTC
      Diagnostic Trouble Code. Standardised fault identifier stored in
      non-volatile memory and retrievable via UDS diagnostic services.

   ECU
      Electronic Control Unit. The embedded hardware and software unit that
      is the primary authoring and generation target of Qorix Developer
      Classic and LW-BSW projects.

   EMF
      Eclipse Modelling Framework. Java/JVM-based metamodelling framework
      used by ARTOP. The Rust domain crates have zero dependency on EMF.

   EMM
      ECU Mode Manager. BSW module responsible for ECU mode transitions
      (Normal, Sleep, Reset). One of the 10 LW-BSW modules.

   Engineer-in-the-Loop
      Governance principle enforced by ADR-004: AI-originated configuration
      changes are only applied after explicit engineer acceptance of a typed
      ``OperationPlan``. The Qorix Agent never writes to YAML directly.

   FBL
      Flash Bootloader. Embedded software responsible for receiving and
      flashing firmware updates over a communication bus. Configured using
      the BPCT subsystem (BD1–BD6 designers).

   GraphQL
      Query and mutation API technology used by the ARXML Gateway to expose
      AUTOSAR model read and write operations to the Rust domain layer via
      the ``core::gql_client`` generated Rust client.

   gRPC
      Remote Procedure Call protocol used between the IDE Layer and the Rust
      Domain Service for deep semantic validation and model operations.

   HSM
      Hardware Security Module. Dedicated security processor on the target
      ECU used for cryptographic key storage. Key store address is defined
      in BD3 and validated against BD6 security configuration.

   ICC-2
      Implementation Conformance Class 2. Partial AUTOSAR Classic conformance
      level with ≈ 10 BSW modules and ≈ 600 configuration parameters. Target
      for the Qorix LW-BSW stack.

   ICC-3
      Implementation Conformance Class 3. Full AUTOSAR Classic conformance
      with 46+ BSW modules and ≈ 5,600 configuration parameters.

   IDE Layer
      The user-facing subsystem (VS Code Extension / Theia). Provides all
      designers, the YAML editor, the Command Bus, the WASM Bridge, the
      Domain Service Client, the AI Chat Panel, the Diagnostics Panel and
      the Project Creation Wizard.

   Intent Router
      Qorix Agent component that detects the active stack domain from the
      open designer tab (C* → Classic, A* → Adaptive, BD* → BPCT) and
      routes user prompts to the correct domain-specific MCP tool set.

   IOHAB
      I/O Hardware Abstraction. BSW module providing configurable interfaces
      to DIO, ADC, ICU and PWM peripheral drivers. One of the 10 LW-BSW
      modules.

   ISO 14229
      UDS (Unified Diagnostic Services) specification. Defines the diagnostic
      communication protocol implemented by the DCM/Diag module.

   ISO 15765-2
      CAN Transport Protocol specification. Defines segmentation and flow
      control for diagnostic messages over CAN. Implemented by CanTp.

   LIN
      Local Interconnect Network (ISO 17987). Optional communication bus
      protocol in LW-BSW projects and BPCT multi-channel configurations.

   LLM
      Large Language Model. External AI model used by the Qorix Agent for
      natural language interpretation and explanation generation. The LLM
      never writes YAML directly; all changes are mediated through the
      ``OperationPlan`` and user acceptance gate.

   LSP
      Language Server Protocol. Standard protocol providing syntax, schema
      and semantic editing assistance (completion, go-to-definition,
      find-references, rename) in text-based editors.

   LW-BSW
      Light Weight Basic Software. Qorix-developed AUTOSAR Classic BSW stack
      targeting small ECUs with tight memory constraints. ICC-2 conformance,
      10 BSW modules, ≈ 600 configuration parameters, ≈ 150 KB ROM target,
      ≈ 30 KB RAM target, OSEK SC-1 operating system.

   MCP
      Model Context Protocol. Structured protocol used by the Qorix Agent
      to expose tool endpoints to the LLM. Each domain registers its own
      MCP tools in the Tool Registry.

   MCU
      Microcontroller Unit. Target processor for Classic, LW-BSW and
      Bootloader projects. MCU family selection in the project creation
      wizard drives hardware-dependent defaults (flash page size, SPI clock,
      timer resolution).

   NM
      Network Management. BSW module implementing the ECU network management
      protocol (OSEK NM or AUTOSAR NM). One of the 10 LW-BSW modules.

   NvM
      Non-Volatile Memory manager. AUTOSAR Classic BSW module managing the
      storage and retrieval of data in EEPROM or flash memory.

   OperationPlan
      Typed, ordered set of ``core::ops`` mutations (add, update, delete at
      a specific YAML path) proposed by the Qorix Agent or a domain operation
      for engineer review. No YAML file is modified until the engineer
      explicitly accepts the plan. Acceptance is recorded in the audit log.

   OSEK SC-1
      OSEK/VDX Scalability Class 1. Minimal OS conformance class providing
      priority-based preemptive scheduling on a single core without memory
      protection. The operating system model used by the LW-BSW stack.

   PDU
      Protocol Data Unit. A unit of data transferred over a communication
      bus. I-PDUs carry signals between SWCs via the COM stack.

   Provenance Record
      Metadata file (``provenance.json``) written alongside every generated
      artefact recording: Git SHAs of source YAML files, tool version, ARTOP
      version, target AUTOSAR schema version and UTC timestamp of generation.

   Qorix Agent
      The AI orchestration subsystem (MCP Layer). Routes engineering prompts
      to domain MCP tools, obtains LLM explanations and returns typed
      ``OperationPlan`` objects. Never writes to YAML directly.

   Qorix Developer
      Unified platform for automotive configuration authoring, validation,
      deterministic artefact generation, and traceable engineering workflows
      across Classic AUTOSAR, Adaptive AUTOSAR, Bootloader (BPCT), LW-BSW
      and Eclipse S-Core stacks.

   RST
      reStructuredText. The markup language used for all Qorix Developer
      documentation source files. Documents are compiled by Sphinx with
      the sphinx-needs extension to produce the rendered documentation portal.

   RTE
      Runtime Environment. Auto-generated middleware layer in AUTOSAR Classic
      connecting SWC ports to COM signals, OS tasks and NvM blocks.
      Configured via the C6 RTE & Mapping designer.

   Rust Domain Platform
      Software subsystem implemented in Rust. Owns the canonical semantic
      models for all supported domains. Compiled from one codebase to three
      build targets: HTTP/gRPC Domain Service, WASM module and CLI binary.

   SecOC
      Secure Onboard Communication. AUTOSAR Classic BSW module providing
      message authentication over the COM stack.

   SOME/IP
      Scalable service-Oriented MiddlewarE over IP. Primary service discovery
      and communication protocol for AUTOSAR Adaptive. Configured in the A2
      Communication designer.

   sphinx-needs
      Sphinx extension providing ``.. req::``, ``.. spec::`` and related
      directives that turn requirements, architecture specs and test cases
      into typed, linkable, machine-readable objects with IDs, attributes and
      cross-references. Broken traceability links are build errors.

   SWC
      Software Component. A deployable unit in AUTOSAR Classic with defined
      ports and runnables. Authored in the C1 SWC & Interface designer.

   SWE.1
      ASPICE software requirements analysis process. Produces the Software
      Requirements Specification (QDX-SWE-DOC-001), 101 atomic testable
      software requirements derived from the SYS.2 system requirements.

   SWE.2
      ASPICE software architectural design process. Produces the Software
      Architecture Description (QDX-SWA-DOC-001) defining subsystem
      decomposition, interface contracts, ADRs and 101 architecture specs.

   SWE.3
      ASPICE software detailed design process. Produces the Software Detailed
      Design (QDX-SDD-DOC-001) specifying public function signatures,
      algorithms, data structures and unit test anchors.

   SWE.4
      ASPICE software unit verification process. Produces the Unit
      Verification Specification (QDX-SWE4-DOC-001) with 79 unit tests,
      coverage targets and static analysis rules.

   SWE.5
      ASPICE software integration and integration test process. Produces the
      Integration Test Specification (QDX-SWE5-DOC-001) with 21 interface-
      boundary test cases across six integration stages.

   SWE.6
      ASPICE software qualification test process. Produces the Qualification
      Test Specification (QDX-SWE6-DOC-001) with 101 end-to-end test cases,
      one per SWE.1 requirement.

   SYS.2
      ASPICE system requirements analysis process. Produces the System
      Requirements Specification (QDX-SRS-001) defining externally observable
      system behaviour, constraints and quality attributes. Top of the
      Qorix Developer traceability chain.

   Template
      A pre-configured project starting point selectable in the project
      creation wizard. Templates pre-populate YAML source files with
      realistic domain-specific defaults for common ECU archetypes
      (e.g. Powertrain Control, Perception Pipeline, Secure Boot FBL).

   Tool Registry
      Qorix Agent component cataloguing all available MCP tools for each
      domain. The Intent Router queries the Tool Registry to select the
      correct tool set for the active designer context.

   UDS
      Unified Diagnostic Services (ISO 14229). Diagnostic communication
      protocol implemented by the DCM/Diag module. The BD4 Core &
      Diagnostics designer configures the UDS session state machine.

   Validation Gating
      Rule enforced by the generation pipeline: ``domain_service::generate``
      refuses to produce output artefacts and returns a non-zero exit code
      when any ``Severity::Error`` diagnostic is present. Implements
      QDX-SWE-034.

   VFB
      Virtual Functional Bus. AUTOSAR Classic abstract communication medium
      connecting SWC ports. The VFB view is displayed in the C1 designer.

   VR_NNN
      Validation Rule identifier used by the BPCT validation engine.
      Each VR_NNN rule defines a cross-parameter or cross-designer
      constraint verified in a single consolidated validation pass before
      generation. Examples: ``VR_003`` (flash block size alignment),
      ``VR_007`` (watchdog timeout vs. erase timeout),
      ``VR_013`` (RSA1024 not recommended for secure boot).

   WASM
      WebAssembly. Portable binary compilation target. The
      ``qorix_core_wasm`` build target runs the Rust domain core directly
      inside the IDE host (VS Code, Theia) without a network call, enabling
      sub-500 ms in-IDE validation with results identical to the CI pipeline.

   WdgM
      Watchdog Manager. AUTOSAR Classic BSW module supervising software
      entities and triggering the hardware watchdog service.

   Workspace
      Top-level container in Qorix Developer holding one or more
      stack-specific projects under a common root directory. Represented as
      ``workspace.yaml``. A single workspace may contain Classic, Adaptive,
      Bootloader and LW-BSW projects simultaneously.

   YAML
      YAML Ain't Markup Language. The human-readable, version-control-
      friendly serialisation format used as the canonical source of truth
      for all Qorix Developer project configuration. Every parameter change
      is a line-level text change committable to Git. ARXML is produced
      from YAML via the gateway; YAML is never produced from ARXML as a
      working format.

   A1–A6
      Six Adaptive AUTOSAR designer tabs in Qorix Developer:
      A1 Application & Service, A2 Communication, A3 Machine Design,
      A4 Platform Services, A5 Execution Management, A6 Deployment.
