Overview Glossary
=================

.. glossary::

   AI-Assist
      Explainable engineering assistance capability that proposes structured
      actions while keeping final control with the engineer.

   ARTOP
      AUTOSAR Tool Platform used in the ARXML Gateway to parse and generate
      AUTOSAR exchange models.

   ARXML
      AUTOSAR XML exchange format used for import/export of standardized
      AUTOSAR engineering artifacts.

   ASPICE
      Automotive process assessment framework used as the process baseline for
      SYS.2, SWE.1, and SWE.2 work products.

   BPCT
      Bootloader Parameters Configurator Tool domain in Qorix Developer for
      bootloader-focused configuration authoring and generation.

   Config-as-Code
      Development paradigm where configuration is maintained as
      human-readable, version-controlled YAML artifacts.

   Deterministic Generation
      Property that identical validated inputs and tool versions produce
      byte-identical outputs.

   Domain Core
      Shared Rust implementation that owns model, validation, operations,
      migrations, and shared business rules across execution targets.

   Engineer-in-the-Loop
      Governance pattern where AI-suggested changes are only applied after
      explicit user approval.

   IDE Layer
      User-facing subsystem (for example VS Code/Theia) providing designers,
      YAML editing, diagnostics, and workflow orchestration.

   MCP Layer
      Orchestration layer that routes user intent and AI interactions to
      structured domain operations.

   OperationPlan
      Structured plan of proposed configuration operations generated for
      review/approval before persistence.

   Qorix Developer
      Unified platform for automotive configuration authoring, validation,
      generation, and traceable engineering workflows.

   Rust Domain Platform
      Software subsystem implemented in Rust and built for service, WASM, and
      CLI targets to preserve validation and rules parity.

   SWE.1
      ASPICE software requirements analysis process defining software-level
      requirements derived from system requirements.

   SWE.2
      ASPICE software architectural design process defining subsystem
      decomposition, interfaces, and runtime interactions.

   SYS.2
      ASPICE system requirements analysis process defining system behavior,
      constraints, and externally visible expectations.

   Validation Gating
      Rule that blocks generation/publication when unresolved ERROR-level
      diagnostics are present.

   Workspace
      Top-level project container holding configuration sources, generated
      outputs, schemas, and metadata.

   YAML
      Human-readable canonical persistence format for configuration models
      within Qorix Developer.
