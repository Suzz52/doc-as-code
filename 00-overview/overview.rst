Overview
========

Qorix Developer is a unified engineering platform for AUTOSAR-centric
configuration authoring, validation, and deterministic artifact generation.
Across the SYS.2, SWE.1, and SWE.2 baselines, the platform is defined as a
single product that supports Classic AUTOSAR, Adaptive AUTOSAR, Bootloader
(BPCT), and related stack extensions while keeping YAML as the canonical
source of truth.

Purpose
-------

The platform provides a consistent workflow from system-level requirements to
software implementation structure:

- **SYS.2 viewpoint**: defines externally observable system behavior,
  boundaries, quality attributes, and operational constraints.
- **SWE.1 viewpoint**: derives software requirements and subsystem-level
  obligations from SYS.2.
- **SWE.2 viewpoint**: defines architectural decomposition, interfaces,
  layering rules, and runtime data flows that realize SWE.1.

Platform Scope
--------------

The combined specification describes a product that includes:

- Hybrid authoring through visual designers and text-based YAML editing.
- Rule-based validation with diagnostics and generation gating.
- Deterministic output generation for downstream toolchains (for example,
  AUTOSAR ARXML and related generated artifacts).
- AI-assisted engineering support with explicit engineer approval before any
  configuration mutation is persisted.
- Project/workspace operation in IDE contexts and CI-compatible execution
  paths.

Core Subsystems
---------------

From the software architecture baseline, the platform is organized into four
primary subsystems:

1. **IDE Layer**

   - VS Code/Theia-based user surface.
   - Designers, YAML editing, diagnostics views, and command orchestration.

2. **Rust Domain Platform**

   - Shared domain core for models, validation, operations, and migrations.
   - Built for three targets: service (HTTP/gRPC), WASM, and CLI.

3. **ARXML Gateway**

   - GraphQL-based boundary for ARXML import/export.
   - Isolates AUTOSAR metamodel/ARTOP dependencies from the Rust domain core.

4. **Qorix Agent (MCP Layer)**

   - AI intent routing and plan generation.
   - Produces structured operation plans; does not directly write YAML.

Key Engineering Principles
--------------------------

The overview aligns SYS.2/SWE.1/SWE.2 around these platform principles:

- **YAML-first, version-control-friendly modeling**.
- **Deterministic validation and generation behavior across IDE, service, and
  CI execution paths**.
- **Strict subsystem boundaries and one-directional layering**.
- **ARXML boundary isolation via the gateway**.
- **Explainable, bounded AI assistance with engineer-in-the-loop approval**.
- **Traceability from requirements to architecture and verification artifacts**.

End-to-End Workflow Summary
---------------------------

At a high level, the intended lifecycle is:

1. Engineers author or update configuration in designers and/or YAML.
2. The domain core validates syntax and semantics and reports diagnostics.
3. Errors gate generation and publication until resolved.
4. Approved changes are persisted as human-readable YAML and tracked in Git.
5. Imports/exports requiring AUTOSAR exchange are routed through the ARXML
   gateway.
6. AI assistance may propose changes as structured plans, but application of
   those plans remains under explicit engineer control.

Traceability Context
--------------------

This overview is synthesized from:

- **SYS.2** System Requirements Specification
- **SWE.1** Software Requirements Specification
- **SWE.2** Software Architecture Description

Together, these define the product intent (what the system must do), software
obligations (what software must provide), and architectural realization (how
software is organized to satisfy those obligations).
