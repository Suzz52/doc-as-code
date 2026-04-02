.. ============================================================
.. QORIX DEVELOPER— System Requirements Specification
.. ASPICE: SYS.2
.. ============================================================

.. _sys_requirements:

========================================================
System Requirements Specification
========================================================

.. list-table::
   :widths: 25 75
   :header-rows: 0

   * - **Document ID**
     - QDX-SRS-001
   * - **Product line**
     - Platform
   * - **Version**
     - 0.1.0
   * - **Status**
     - Draft
   * - **Owner**
     - Qorix Developer Product and Architecture Team
   * - **Approved by**
     - TBD — Approval pending
   * - **ASPICE process**
     - SYS.2 — System Requirements Analysis
   * - **Elicited by**
     - SYS.1 — Requirements Elicitation (QDX-SER-001, in progress)
   * - **Verified by**
     - SYS.5 — System Verification (QDX-SYS5-DOC-001, in progress)
   * - **Validated by**
     - VAL.1 — Validation (QDX-VAL-001, in progress)
   * - **Risk register**
     - QDX-RMP-001 (in progress)
   * - **Change authority**
     - SUP.10 Change Request process — QDX-CRM-001 (in progress)
   * - **Jira epic**
     - QDX-EPIC-PLATFORM-SYSREQ
   * - **Git path**
     - ``docs/10-sys.2/platform/sys_requirements.rst``
   * - **Changelog**
     - See :ref:`sys_changelog`

----

.. contents:: Table of contents
   :depth: 3
   :local:

----


1. Purpose and Scope
====================

This document specifies the system-level requirements for the Qorix Developer
application as a unified configuration authoring, validation, generation and
engineering-assistance platform for automotive software-defined vehicle
middleware stacks. The application covers authoring and management of
configuration models for Classic, Adaptive, Bootloader and Performance stacks,
including designer-based editing, text-based editing, validation, deterministic
artefact generation, import/export orchestration and explainable AI-assisted
engineering workflows. This document defines externally observable system
behaviour, constraints, interfaces and quality attributes required for product
planning, downstream software requirements derivation and system verification.
Implementation structure, module decomposition and internal code design are out
of scope and belong to SWE.1/SWE.2 work products.

**In scope:**

- Unified authoring and management of configuration models across multiple Qorix-supported stacks
- Hybrid user experience combining visual designers and text-based configuration editing
- Deterministic generation and publication of engineering artefacts, including AUTOSAR ARXML
- Validation, traceability, diagnostics and explainable AI-assisted user guidance
- IDE integration, backend services, workspace/project management and CI-facing outputs

**Out of scope:**

- Detailed software architecture, class/module design and implementation choices
- Runtime behaviour of generated target ECU software beyond generated artefact correctness
- OEM- or project-specific parameter values not owned by the Qorix Developer platform
- Business, commercial and licensing requirements not affecting system behaviour


2. Stakeholders and Intended Audience
======================================

.. list-table::
   :widths: 30 30 40
   :header-rows: 1

   * - Role
     - Name / Team
     - Relevance
   * - System architect
     - Qorix Developer Architecture Team
     - Owns system definition, boundaries and quality objectives
   * - SW requirements lead
     - Qorix Developer Engineering
     - Derives SWE.1 software requirements from this document
   * - QA lead
     - Qorix QA / Validation
     - Derives SYS.5 system test specifications and acceptance criteria
   * - Project manager
     - Product Program Management
     - Release planning, milestone management and compliance tracking
   * - Product owner
     - Stack-specific product owners
     - Prioritisation of scope across Classic, Adaptive, Bootloader and Performance
   * - ASPICE assessor
     - Internal / External
     - Process compliance verification
   * - Integration engineer
     - Customer / Solution Engineering
     - Consumes outputs and validates practical applicability in customer programs
   * - Safety and security lead
     - Functional Safety / Cybersecurity Team
     - Reviews safety-, traceability- and security-relevant system behaviour
   * - QA lead
     - Qorix QA / Validation Team
     - Owns SUP.1 quality assurance plan; verifies process compliance and
       work product conformance at each ASPICE process stage
   * - Risk owner
     - Product Program Management
     - Maintains MAN.5 risk register (QDX-RMP-001); reviews risk-tagged
       requirements at each milestone
   * - Change authority
     - Architecture + Product Management
     - Approves change requests (SUP.10) that modify baselined requirements;
       ensures CR traceability is maintained in Jira


3. Terms, Acronyms and Abbreviations
=====================================

.. glossary::

   AUTOSAR
      AUTomotive Open System ARchitecture — standardised software framework
      for ECU software development.

   Eclipse S-Core
      Eclipse Foundation project providing a safety-oriented AUTOSAR-independent
      software core for embedded systems.

   ASPICE
      Automotive SPICE — process assessment model for automotive software
      suppliers.

   SYS.2
      ASPICE process: System Requirements Analysis.

   ECU
      Electronic Control Unit.

   ARXML
      AUTOSAR XML exchange format used to represent standardised engineering
      models and configuration data.

   GraphQL
      Query and mutation API technology used by the platform to access,
      inspect and modify structured configuration models.

   LSP
      Language Server Protocol used to provide syntax and semantic editing
      assistance in text-based editors.

   AI-Assist
      Qorix Developer capability providing explainable engineering assistance,
      guided authoring and intent-to-configuration help.

   Designer
      Domain-specific graphical editor provided by the Qorix Developer
      application for authoring or reviewing a configuration model.

   Workspace
      Top-level user project container containing configuration projects,
      schemas, generated outputs and supporting metadata.


4. System Context and Overview
===============================

4.1 System context diagram
---------------------------

.. note::
   Render this diagram locally with ``sphinx-contrib/mermaid`` or view on
   GitHub. The ``.. mermaid::`` directive requires ``sphinxcontrib-mermaid``
   in ``conf.py``.

.. mermaid::

   C4Context
     title System context — Qorix Developer Platform

     Person(user, "Developer / Integrator", "Authors, validates and publishes configuration")
     System(qorix, "Qorix Developer", "Unified configuration authoring and generation platform")
     System_Ext(autosar, "AUTOSAR toolchain / external engineering tools", "Consumes or provides ARXML and related artefacts")
     System_Ext(ci, "CI/CD pipeline", "Build, validation, quality gates and artefact publication")
     System_Ext(jira, "Jira", "Tracking, traceability and work planning")
     System_Ext(llm, "Enterprise LLM services", "AI assistance for guided engineering support")
     System_Ext(vcs, "Version control", "Source control for configuration and generated artefacts")

     Rel(user, qorix, "Uses for configuration authoring, validation and generation")
     Rel(qorix, autosar, "Imports / exports engineering artefacts")
     Rel(qorix, ci, "Provides outputs to and is validated by")
     Rel(qorix, jira, "References work items and traceability IDs")
     Rel(qorix, llm, "Requests bounded AI assistance")
     Rel(qorix, vcs, "Reads / writes version-controlled project content")

4.2 System description
------------------------

Qorix Developer is a unified engineering application for configuration authoring
and code-generation preparation across multiple automotive middleware stacks.
It provides a common workspace and project model in which engineers can create,
edit, validate, trace and publish configuration artefacts for Classic,
Adaptive, Bootloader and Performance domains without requiring separate tools
per stack.

The platform supports a hybrid authoring model. Users may work through visual
Designers for domain-specific editing, through text-based YAML or IDL editors,
or through both in a synchronized way. The system validates user input against
schema and semantic rules, exposes structured model access through APIs and
publishes deterministic outputs suitable for downstream toolchains and customer
integration workflows.

The application also provides bounded and explainable AI assistance to reduce
configuration effort and improve discoverability of configuration intent,
without removing engineer control. Final outputs remain deterministic,
traceable and reviewable, with validation and generation behaviour governed by
platform rules rather than non-deterministic AI decisions.


5. Operational Environment and Constraints
===========================================

5.1 Target hardware
--------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Attribute
     - Value
   * - Target platform
     - Desktop engineering application and associated backend services for configuration authoring across Classic, Adaptive, Bootloader and Performance stacks
   * - Host OS (build)
     - Ubuntu 22.04 LTS or equivalent supported Linux build environment
   * - Host OS (user)
     - Windows 10/11 and Linux desktop environments; browser-based execution environment for web-hosted deployment variants
   * - Compiler / runtime toolchain
     - Node.js-based IDE frontend runtime, Java or Rust backend services, and browser engine/runtime as applicable
   * - Memory constraints
     - System shall support practical engineering workspaces with multiple projects and generated artefacts on standard developer-class workstations

5.2 Regulatory and standards constraints
-----------------------------------------

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Standard
     - Applicability
   * - ASPICE SYS.2
     - This document is the primary work product for system requirements analysis
   * - ISO 26262
     - Applicable to safety-relevant development process expectations, traceability and determinism objectives where product deployment requires it
   * - AUTOSAR Classic 4.2.2 / 4.3.1
     - Supported import/export and compatibility target where relevant
   * - AUTOSAR Adaptive R20-11 / R23-11 / R24-11
     - Supported import/export and compatibility target where relevant
   * - Eclipse S-Core
     - Applicable for Performance stack integration and related engineering models where relevant
   * - RFC 2119
     - Requirement wording convention for SHALL / SHOULD / MAY usage in this document

5.3 Interface constraints
--------------------------

The following pre-agreed interfaces constrain the system design space:

- The system shall support AUTOSAR-compatible interchange through ARXML for supported Classic and Adaptive flows.
- The system shall support structured model access through a stable GraphQL-based API for internal and extension-facing interactions.
- The system shall support text-based authoring for human-readable configuration formats used by the platform, including YAML-based models where applicable.
- The system shall operate within IDE integration environments aligned with Eclipse Theia and Visual Studio Code extension models.
- AI assistance shall be bounded so that generated or suggested user actions remain explainable, reviewable and non-authoritative until accepted by the engineer.


6. System Requirements
=======================

.. admonition:: Requirement writing rules

   - Every requirement uses **SHALL** (mandatory), **SHOULD** (recommended),
     or **MAY** (optional) per RFC 2119.
   - One requirement per block — no compound requirements with "and/or".
   - Each requirement is independently testable.
   - IDs are permanent — never reuse a retired ID.

.. _QDX-SYS-001:

6.1 Functional requirements
-----------------------------

.. req:: Unified multi-stack workspace support
   :id: QDX-SYS-001
   :status: Draft
   :priority: High
   :rationale: Qorix Developer is positioned as one environment across multiple middleware stacks.
   :verification: SYS.5 system test | Demonstration
   :jira: QDX-001
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-001 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-001 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** allow a user to create and manage a workspace containing one or more configuration projects for Classic, Adaptive, Bootloader and Performance stacks within the same application environment.

.. req:: Project scaffolding
   :id: QDX-SYS-002
   :status: Draft
   :priority: High
   :rationale: Standard project creation is required for repeatability and onboarding.
   :verification: SYS.5 system test | Inspection
   :jira: QDX-002
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-002 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-002 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** provide project creation templates that initialise the folder structure, mandatory metadata and default model files required for each supported stack type.

.. req:: Text-based authoring support
   :id: QDX-SYS-003
   :status: Draft
   :priority: High
   :rationale: Human-readable configuration is a core product value and enables version-controlled parallel authoring.
   :verification: SYS.5 system test
   :jira: QDX-003
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-003 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-003 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** support text-based authoring of platform configuration models in the supported human-readable source formats defined by the product line.

.. req:: Designer-based authoring support
   :id: QDX-SYS-004
   :status: Draft
   :priority: High
   :rationale: Domain-specific designers are a key usability and product differentiation capability.
   :verification: Demonstration | SYS.5 system test
   :jira: QDX-004
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-004 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-004 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** provide domain-specific graphical designers for supported engineering domains and shall allow users to create, view and edit configuration content through those designers.

.. req:: Hybrid synchronization
   :id: QDX-SYS-005
   :status: Draft
   :priority: High
   :rationale: Users require seamless switching between graphical and textual authoring without data loss.
   :verification: SYS.5 system test
   :jira: QDX-005
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-005 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-005 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** keep designer-based and text-based representations of the same configuration model logically synchronized such that a valid user change in one representation is reflected in the other representation after save or refresh.

.. req:: Schema validation
   :id: QDX-SYS-006
   :status: Draft
   :priority: High
   :rationale: Early defect detection is a primary system objective.
   :verification: SYS.5 system test
   :jira: QDX-006
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-006 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-006 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** validate edited configuration content against the applicable syntax, schema and mandatory field rules before allowing a publish or generation action to complete successfully.

.. req:: Semantic validation
   :id: QDX-SYS-007
   :status: Draft
   :priority: High
   :rationale: Schema-valid content can still be semantically invalid for engineering use.
   :verification: SYS.5 system test | Analysis
   :jira: QDX-007
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-007 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-007 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** detect and report semantic validation violations, including unresolved references, incompatible mappings, duplicate identifiers and missing mandatory cross-model relationships.

.. req:: Cross-file reference management
   :id: QDX-SYS-008
   :status: Draft
   :priority: High
   :rationale: The platform relies on sharded and multi-file model authoring.
   :verification: SYS.5 system test
   :jira: QDX-008
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-008 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-008 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** support references between configuration elements located in different files within the same workspace or project boundary where such references are defined by the supported data model.

.. req:: Deterministic artefact publication
   :id: QDX-SYS-009
   :status: Draft
   :priority: High
   :rationale: Determinism is essential for traceability, safety-aligned development and CI use.
   :verification: Analysis | SYS.5 system test
   :jira: QDX-009
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-009 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-009 (VAL.1 — pending QDX-VAL-001)
   :risk_id: QDX-RISK-001 (QDX-RMP-001)

   The system **SHALL** produce identical generated outputs for identical validated inputs, generation settings and tool version.

.. req:: AUTOSAR artefact export
   :id: QDX-SYS-010
   :status: Draft
   :priority: High
   :rationale: External toolchain interoperability is mandatory for customer adoption.
   :verification: SYS.5 system test — interface conformance
   :jira: QDX-010
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-010 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-010 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** export supported Classic and Adaptive engineering models to AUTOSAR-compliant ARXML for the product versions and domains supported by the release.

.. req:: AUTOSAR artefact import
   :id: QDX-SYS-011
   :status: Draft
   :priority: High
   :rationale: Migration and coexistence with existing toolchains are required business capabilities.
   :verification: SYS.5 system test — interface conformance
   :jira: QDX-011
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-011 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-011 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** import supported external engineering artefacts into the Qorix Developer workspace and report any unsupported, lossy or ambiguous conversion conditions to the user.

.. req:: Structured model API
   :id: QDX-SYS-012
   :status: Draft
   :priority: High
   :rationale: Designers and extensions require consistent structured access to model data.
   :verification: SYS.5 system test — interface conformance
   :jira: QDX-012
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-012 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-012 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** expose structured access to configuration model data and mutations through a documented API contract suitable for use by internal components and approved extensions.

.. req:: Localized atomic edits
   :id: QDX-SYS-013
   :status: Draft
   :priority: Medium
   :rationale: Fine-grained changes are needed for designer interactions and merge-friendly editing.
   :verification: SYS.5 system test
   :jira: QDX-013
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-013 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-013 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** support localized atomic modification of configuration models such that a change to one model element does not require unrelated model elements to be rewritten by the platform.

.. req:: Diagnostics and issue reporting
   :id: QDX-SYS-014
   :status: Draft
   :priority: High
   :rationale: Usable validation requires actionable diagnostics.
   :verification: SYS.5 system test | Demonstration
   :jira: QDX-014
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-014 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-014 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** present validation and processing issues with severity, location and user-actionable diagnostic information.

.. req:: Traceable generation provenance
   :id: QDX-SYS-015
   :status: Draft
   :priority: High
   :rationale: Engineering outputs must be reviewable and attributable.
   :verification: Inspection | Analysis
   :jira: QDX-015
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-015 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-015 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** record generation provenance sufficient to identify the source workspace content, generation configuration and tool version used to produce a generated artefact.

.. req:: Explainable AI assistance
   :id: QDX-SYS-016
   :status: Draft
   :priority: High
   :rationale: AI assistance is required, but recommendations must remain understandable and engineer-controlled.
   :verification: Demonstration | Inspection
   :jira: QDX-016
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-016 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-016 (VAL.1 — pending QDX-VAL-001)
   :risk_id: QDX-RISK-002 (QDX-RMP-001)

   The system **SHALL** provide AI-assisted guidance, recommendation or content suggestion features together with an explanation or traceable basis for each user-visible recommendation.

.. req:: User acceptance of AI suggestions
   :id: QDX-SYS-017
   :status: Draft
   :priority: High
   :rationale: Final engineering accountability must remain with the human user.
   :verification: SYS.5 system test
   :jira: QDX-017
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-017 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-017 (VAL.1 — pending QDX-VAL-001)
   :risk_id: QDX-RISK-002 (QDX-RMP-001)

   The system **SHALL** require explicit user acceptance before any AI-originated suggestion is committed into the persistent project content.

.. req:: Search and navigation across model content
   :id: QDX-SYS-018
   :status: Draft
   :priority: Medium
   :rationale: Large workspaces require efficient discoverability.
   :verification: SYS.5 system test | Demonstration
   :jira: QDX-018
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-018 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-018 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** provide search and navigation functions that allow users to locate configuration elements, references, diagnostics and generated artefacts within a workspace.

.. req:: Version-control-friendly storage
   :id: QDX-SYS-019
   :status: Draft
   :priority: High
   :rationale: Parallel authoring and review require merge-friendly project content.
   :verification: Inspection | Analysis
   :jira: QDX-019
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-019 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-019 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** persist project source content in a version-control-friendly form suitable for textual diff, review and merge workflows.

.. req:: Workspace consistency checking
   :id: QDX-SYS-020
   :status: Draft
   :priority: High
   :rationale: Multi-stack workspaces need whole-system checks beyond single-file validation.
   :verification: SYS.5 system test
   :jira: QDX-020
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-020 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-020 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** provide a workspace-level consistency check that evaluates all relevant projects and referenced configuration artefacts participating in a publish or release workflow.

.. req:: Extensible domain support
   :id: QDX-SYS-021
   :status: Draft
   :priority: Medium
   :rationale: Product evolution requires adding new designers and domains without redefining the whole platform.
   :verification: Analysis | Demonstration
   :jira: QDX-021
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-021 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-021 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** support extension-based addition of new domain-specific editors, validations or generators through controlled product extension mechanisms.

6.2 Performance requirements
------------------------------

.. req:: Workspace opening time
   :id: QDX-SYS-022
   :status: Draft
   :priority: High
   :rationale: The application must remain practical for daily engineering workflows.
   :verification: SYS.5 system test — performance measurement
   :jira: QDX-022
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-022 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-022 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** open a valid medium-sized workspace under nominal workstation conditions within 30 seconds.

.. req:: Interactive validation feedback latency
   :id: QDX-SYS-023
   :status: Draft
   :priority: High
   :rationale: Editing productivity depends on responsive feedback.
   :verification: SYS.5 system test — performance measurement
   :jira: QDX-023
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-023 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-023 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** present syntax and schema validation feedback for a single user edit within 2 seconds under nominal workstation conditions for a medium-sized file.

.. req:: Search responsiveness
   :id: QDX-SYS-024
   :status: Draft
   :priority: Medium
   :rationale: Search is a primary navigation activity in large workspaces.
   :verification: SYS.5 system test — performance measurement
   :jira: QDX-024
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-024 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-024 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** return search results for indexed workspace content within 5 seconds under nominal workstation conditions for a medium-sized workspace.

.. req:: Artefact generation completion time
   :id: QDX-SYS-025
   :status: Draft
   :priority: High
   :rationale: Generation must be practical for iterative engineering and CI usage.
   :verification: SYS.5 system test — performance measurement
   :jira: QDX-025
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-025 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-025 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** complete generation of supported release artefacts for a medium-sized validated project within 60 seconds under nominal workstation conditions.

.. req:: Non-blocking UI during long-running operations
   :id: QDX-SYS-026
   :status: Draft
   :priority: Medium
   :rationale: Users must retain control and visibility during heavy operations.
   :verification: Demonstration | SYS.5 system test
   :jira: QDX-026
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-026 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-026 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** provide progress indication and cancellation support for user-initiated operations that exceed 5 seconds of execution time.

6.3 Interface requirements
----------------------------

.. req:: IDE integration support
   :id: QDX-SYS-027
   :status: Draft
   :priority: High
   :rationale: Product strategy requires operation within supported IDE ecosystems.
   :verification: SYS.5 system test — interface conformance
   :jira: QDX-027
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-027 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-027 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** provide integration with supported IDE host environments used by the product release, including extension activation, project access and editor contribution behaviour.

.. req:: GraphQL contract conformance
   :id: QDX-SYS-028
   :status: Draft
   :priority: High
   :rationale: Structured model access is a platform backbone for designers and services.
   :verification: SYS.5 system test — interface conformance
   :jira: QDX-028
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-028 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-028 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** expose model query and mutation operations through a versioned API contract with documented request and response semantics.

.. req:: Language-service integration
   :id: QDX-SYS-029
   :status: Draft
   :priority: High
   :rationale: Text-based editing requires standard editing assistance integration.
   :verification: SYS.5 system test — interface conformance
   :jira: QDX-029
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-029 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-029 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** provide language-service-backed diagnostics and editing assistance for supported text-based model formats within the integrated editor experience.

.. req:: External artefact compatibility reporting
   :id: QDX-SYS-030
   :status: Draft
   :priority: Medium
   :rationale: Interoperability limitations must be visible during customer migration scenarios.
   :verification: SYS.5 system test | Inspection
   :jira: QDX-030
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-030 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-030 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** report the target standard version and compatibility status associated with each imported or exported supported external artefact.

.. req:: CI/CD invocation support
   :id: QDX-SYS-031
   :status: Draft
   :priority: Medium
   :rationale: Automated validation and generation are required for product integration workflows.
   :verification: Demonstration | SYS.5 system test
   :jira: QDX-031
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-031 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-031 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** provide a non-interactive execution mode or equivalent automation interface suitable for CI/CD-triggered validation and generation workflows.

6.4 Safety and security requirements
--------------------------------------

.. req:: Deterministic processing for safety-relevant flows
   :id: QDX-SYS-032
   :status: Draft
   :priority: High
   :rationale: Safety-aligned engineering requires reproducible outputs and predictable processing.
   :verification: Analysis | SYS.5 test
   :jira: QDX-032
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-032 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-032 (VAL.1 — pending QDX-VAL-001)
   :risk_id: QDX-RISK-003 (QDX-RMP-001)

   The system **SHALL** ensure that safety-relevant generation and validation workflows are deterministic with respect to validated input content, configuration and released tool version.

.. req:: Configuration integrity protection
   :id: QDX-SYS-033
   :status: Draft
   :priority: High
   :rationale: Project data must not be silently corrupted or overwritten.
   :verification: SYS.5 system test | Analysis
   :jira: QDX-033
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-033 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-033 (VAL.1 — pending QDX-VAL-001)
   :risk_id: QDX-RISK-004 (QDX-RMP-001)

   The system **SHALL** protect persisted project content against partial write corruption by using an atomic save or equivalent integrity-preserving persistence mechanism.

.. req:: Access control for privileged operations
   :id: QDX-SYS-034
   :status: Draft
   :priority: Medium
   :rationale: Certain actions such as publication, extension management or remote AI usage may require controlled access.
   :verification: SYS.5 system test | Inspection
   :jira: QDX-034
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-034 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-034 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** enforce authentication or authorization controls for privileged operations where such controls are configured for the deployment.

.. req:: Auditability of user-visible critical actions
   :id: QDX-SYS-035
   :status: Draft
   :priority: Medium
   :rationale: Traceability and compliance require reconstructable action history.
   :verification: Inspection | Analysis
   :jira: QDX-035
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-035 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-035 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** record auditable events for user-visible critical actions including generation, publication, import and acceptance of AI-originated changes.

.. req:: Safe failure on invalid configuration
   :id: QDX-SYS-036
   :status: Draft
   :priority: High
   :rationale: Invalid inputs shall not lead to silent generation of misleading outputs.
   :verification: SYS.5 system test
   :jira: QDX-036
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-036 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-036 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** prevent successful publication of an artefact when blocking validation errors remain unresolved.

.. req:: Controlled AI data usage
   :id: QDX-SYS-037
   :status: Draft
   :priority: High
   :rationale: Enterprise AI usage requires bounded data exposure.
   :verification: Inspection | Analysis
   :jira: QDX-037
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-037 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-037 (VAL.1 — pending QDX-VAL-001)
   :risk_id: QDX-RISK-002 (QDX-RMP-001)

   The system **SHALL** provide deployment-configurable controls governing whether project content may be transmitted to an external AI service.

6.5 Non-functional requirements
---------------------------------

.. req:: Explainability of generated outputs
   :id: QDX-SYS-038
   :status: Draft
   :priority: High
   :rationale: Engineers must be able to understand produced outputs and decisions.
   :verification: Analysis | Demonstration
   :jira: QDX-038
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-038 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-038 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** provide sufficient traceability from generated outputs back to source model elements and generation context to support engineering review.

.. req:: Product portability
   :id: QDX-SYS-039
   :status: Draft
   :priority: Medium
   :rationale: Cross-platform availability is required for broad engineering adoption.
   :verification: Demonstration | Inspection
   :jira: QDX-039
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-039 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-039 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** support execution in each host environment declared as supported by the released product baseline.

.. req:: Backward compatibility of project content
   :id: QDX-SYS-040
   :status: Draft
   :priority: Medium
   :rationale: Upgrades must not unnecessarily break existing workspaces.
   :verification: SYS.5 system test | Analysis
   :jira: QDX-040
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-040 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-040 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** provide a defined migration or compatibility mechanism for project content created by earlier supported product versions.

.. req:: Extensibility without core modification
   :id: QDX-SYS-041
   :status: Draft
   :priority: Medium
   :rationale: New domains and customer-specific capabilities should be addable without destabilising the core platform.
   :verification: Analysis | Demonstration
   :jira: QDX-041
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-041 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-041 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** allow supported extensions to add editors, validations or generation capabilities without requiring modification of the released core product for each extension instance.

.. req:: Usable diagnostics quality
   :id: QDX-SYS-042
   :status: Draft
   :priority: Medium
   :rationale: Diagnostics must reduce engineering effort rather than merely signal failure.
   :verification: Demonstration | Inspection
   :jira: QDX-042
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-042 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-042 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** present blocking and non-blocking issues using terminology understandable by the intended engineering audience and shall associate issues with the affected model context.

.. req:: Availability of offline engineering workflows
   :id: QDX-SYS-043
   :status: Draft
   :priority: Medium
   :rationale: Core engineering work shall remain possible in restricted environments.
   :verification: SYS.5 system test
   :jira: QDX-043
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-043 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-043 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** support local authoring, local validation and local viewing of project content without requiring continuous network connectivity, except for explicitly remote-backed functions.

.. req:: Separation of source and generated content
   :id: QDX-SYS-044
   :status: Draft
   :priority: Medium
   :rationale: Clean engineering workflows require separation of editable source from derived outputs.
   :verification: Inspection | SYS.5 system test
   :jira: QDX-044
   :elicited_from: QDX-SER-001 — Stakeholder Requirements (SYS.1)
   :sys_arch: QDX-SYS3-SP-044 (SYS.3 — pending QDX-SYS3-DOC-001)
   :val_test: QDX-VAT-044 (VAL.1 — pending QDX-VAL-001)

   The system **SHALL** maintain a clear separation between user-authored source content and generated output content within the project structure or output configuration.


7. System Requirements Traceability Matrix
===========================================

.. note::
   This matrix is the ASPICE SYS.2 ↔ SYS.5 traceability record.
   Update it every time a requirement is added, modified, or deprecated.

.. list-table::
   :widths: 15 35 20 15 15
   :header-rows: 1

   * - Req ID
     - Title
     - Derived SW req (SWE.1)
     - System test (SYS.5)
     - Status
   * - QDX-SYS-001
     - Unified multi-stack workspace support
     - QDX-SWE-001
     - QDX-ST-001
     - Draft
   * - QDX-SYS-002
     - Project scaffolding
     - QDX-SWE-002
     - QDX-ST-002
     - Draft
   * - QDX-SYS-003
     - Text-based authoring support
     - QDX-SWE-003
     - QDX-ST-003
     - Draft
   * - QDX-SYS-004
     - Designer-based authoring support
     - QDX-SWE-004
     - QDX-ST-004
     - Draft
   * - QDX-SYS-005
     - Hybrid synchronization
     - QDX-SWE-005
     - QDX-ST-005
     - Draft
   * - QDX-SYS-006
     - Schema validation
     - QDX-SWE-006
     - QDX-ST-006
     - Draft
   * - QDX-SYS-007
     - Semantic validation
     - QDX-SWE-007
     - QDX-ST-007
     - Draft
   * - QDX-SYS-008
     - Cross-file reference management
     - QDX-SWE-008
     - QDX-ST-008
     - Draft
   * - QDX-SYS-009
     - Deterministic artefact publication
     - QDX-SWE-009
     - QDX-ST-009
     - Draft
   * - QDX-SYS-010
     - AUTOSAR artefact export
     - QDX-SWE-010
     - QDX-ST-010
     - Draft
   * - QDX-SYS-011
     - AUTOSAR artefact import
     - QDX-SWE-011
     - QDX-ST-011
     - Draft
   * - QDX-SYS-012
     - Structured model API
     - QDX-SWE-012
     - QDX-ST-012
     - Draft
   * - QDX-SYS-013
     - Localized atomic edits
     - QDX-SWE-013
     - QDX-ST-013
     - Draft
   * - QDX-SYS-014
     - Diagnostics and issue reporting
     - QDX-SWE-014
     - QDX-ST-014
     - Draft
   * - QDX-SYS-015
     - Traceable generation provenance
     - QDX-SWE-015
     - QDX-ST-015
     - Draft
   * - QDX-SYS-016
     - Explainable AI assistance
     - QDX-SWE-016
     - QDX-ST-016
     - Draft
   * - QDX-SYS-017
     - User acceptance of AI suggestions
     - QDX-SWE-017
     - QDX-ST-017
     - Draft
   * - QDX-SYS-018
     - Search and navigation across model content
     - QDX-SWE-018
     - QDX-ST-018
     - Draft
   * - QDX-SYS-019
     - Version-control-friendly storage
     - QDX-SWE-019
     - QDX-ST-019
     - Draft
   * - QDX-SYS-020
     - Workspace consistency checking
     - QDX-SWE-020
     - QDX-ST-020
     - Draft
   * - QDX-SYS-021
     - Extensible domain support
     - QDX-SWE-021
     - QDX-ST-021
     - Draft
   * - QDX-SYS-022
     - Workspace opening time
     - QDX-SWE-022
     - QDX-ST-022
     - Draft
   * - QDX-SYS-023
     - Interactive validation feedback latency
     - QDX-SWE-023
     - QDX-ST-023
     - Draft
   * - QDX-SYS-024
     - Search responsiveness
     - QDX-SWE-024
     - QDX-ST-024
     - Draft
   * - QDX-SYS-025
     - Artefact generation completion time
     - QDX-SWE-025
     - QDX-ST-025
     - Draft
   * - QDX-SYS-026
     - Non-blocking UI during long-running operations
     - QDX-SWE-026
     - QDX-ST-026
     - Draft
   * - QDX-SYS-027
     - IDE integration support
     - QDX-SWE-027
     - QDX-ST-027
     - Draft
   * - QDX-SYS-028
     - GraphQL contract conformance
     - QDX-SWE-028
     - QDX-ST-028
     - Draft
   * - QDX-SYS-029
     - Language-service integration
     - QDX-SWE-029
     - QDX-ST-029
     - Draft
   * - QDX-SYS-030
     - External artefact compatibility reporting
     - QDX-SWE-030
     - QDX-ST-030
     - Draft
   * - QDX-SYS-031
     - CI/CD invocation support
     - QDX-SWE-031
     - QDX-ST-031
     - Draft
   * - QDX-SYS-032
     - Deterministic processing for safety-relevant flows
     - QDX-SWE-032
     - QDX-ST-032
     - Draft
   * - QDX-SYS-033
     - Configuration integrity protection
     - QDX-SWE-033
     - QDX-ST-033
     - Draft
   * - QDX-SYS-034
     - Access control for privileged operations
     - QDX-SWE-034
     - QDX-ST-034
     - Draft
   * - QDX-SYS-035
     - Auditability of user-visible critical actions
     - QDX-SWE-035
     - QDX-ST-035
     - Draft
   * - QDX-SYS-036
     - Safe failure on invalid configuration
     - QDX-SWE-036
     - QDX-ST-036
     - Draft
   * - QDX-SYS-037
     - Controlled AI data usage
     - QDX-SWE-037
     - QDX-ST-037
     - Draft
   * - QDX-SYS-038
     - Explainability of generated outputs
     - QDX-SWE-038
     - QDX-ST-038
     - Draft
   * - QDX-SYS-039
     - Product portability
     - QDX-SWE-039
     - QDX-ST-039
     - Draft
   * - QDX-SYS-040
     - Backward compatibility of project content
     - QDX-SWE-040
     - QDX-ST-040
     - Draft
   * - QDX-SYS-041
     - Extensibility without core modification
     - QDX-SWE-041
     - QDX-ST-041
     - Draft
   * - QDX-SYS-042
     - Usable diagnostics quality
     - QDX-SWE-042
     - QDX-ST-042
     - Draft
   * - QDX-SYS-043
     - Availability of offline engineering workflows
     - QDX-SWE-043
     - QDX-ST-043
     - Draft
   * - QDX-SYS-044
     - Separation of source and generated content
     - QDX-SWE-044
     - QDX-ST-044
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
   * - TBD-SYS-001
     - Finalise release-specific definition of medium-sized workspace and performance benchmark dataset for SYS-022 to SYS-025.
     - Architecture + QA
     - 2026-04-15
   * - TBD-SYS-002
     - Confirm exact supported host environments and packaging variants for desktop and browser-hosted deployments.
     - Product Management
     - 2026-04-15
   * - TBD-SYS-003
     - Baseline the exact supported AUTOSAR import/export subset for each stack and release.
     - Domain Architects
     - 2026-04-22
   * - TBD-SYS-004
     - Define deployment-specific policy controls for external AI usage, data retention and audit requirements.
     - Security Lead
     - 2026-04-22
   * - TBD-SYS-005
     - Allocate concrete owner and approver names for the formal release baseline of this document.
     - Program Management
     - 2026-04-10


.. _sys_changelog:

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
     - 2026-03-30
     - Suresh Chamuah created draft based on SYS.2 template and Qorix Developer product roadmap
     - Initial platform-level system requirements draft


----

*This document is version-controlled in Git. The authoritative version is
the HEAD of the ``main`` branch. All changes must be submitted via pull
request with a minimum of two approvals from the defined CODEOWNERS.*
