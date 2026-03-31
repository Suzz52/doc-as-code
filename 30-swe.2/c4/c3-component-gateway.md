# C3 – Components: ARXML Gateway

## Overview

The ARXML Gateway is a **Spring Boot + ARTOP + GraphQL** container. It is the sole bridge between the Rust domain world and the ARXML/EMF world. Rust components never access EMF classes directly — they communicate exclusively through the GraphQL API exposed by this container.

---

## Mermaid Diagram

```mermaid
C4Component
    title Component Diagram – ARXML Gateway (Spring Boot + ARTOP + GraphQL)

    Container_Ext(rustSvc, "Rust Domain Service", "Rust", "Calls GraphQL mutations and queries to import/export ARXML and apply domain operations.")
    Container_Ext(rustCli, "Rust CLI", "Rust", "Calls /import and /export REST endpoints in CI/batch mode.")
    Container_Ext(codeGen, "CodeGen", "External", "Reads ARXML files for code generation (Xtend, RTE generators, BSW generators).")
    System_Ext(legacyTools, "Legacy AUTOSAR Tools", "EB Tresos, Davinci, SystemDesk — source of ARXML files for import.")
    System_Ext(buildToolchain, "Downstream Build Toolchain", "Consumes exported ARXML files.")

    System_Boundary(gateway, "ARXML Gateway") {

        Component(restLayer, "REST Layer", "Spring Boot REST Controller", "Exposes optional /import and /export HTTP endpoints for CI batch use. Entry point for CLI calls. Delegates to ArxmlImportService and ArxmlExportService.")

        Component(gqlEndpoint, "GraphQL Endpoint", "Spring GraphQL (graphql-java)", "Primary API surface for Rust. Exposes typed schema with mutations and queries to:\n- Import ARXML into EMF\n- Export ARXML from EMF\n- Apply Rust OperationPlan ops to EMF model\n- Query current model state")

        Component(emfRepository, "EmfRepository", "Java / EMF", "Loads and stores EMF model instances in memory. Handles multi-file ARXML projects. Acts as in-memory AUTOSAR model store shared by import, export, and op-apply services.")

        Component(arxmlImport, "ArxmlImportService", "Java / ARTOP", "Reads ARXML from the filesystem. Parses and populates EMF model instances via ARTOP libraries. Exposes the loaded model via GraphQL for Rust consumption.")

        Component(arxmlExport, "ArxmlExportService", "Java / ARTOP", "Serializes the current EMF model back to ARXML files. Triggered by Rust via GraphQL mutation after ops are applied. Produces ARXML compatible with Classic and Adaptive tool chains.")

        Component(versionAdapter, "AutosarVersionAdapter", "Java", "Maps different AUTOSAR schema versions (e.g., R4.x, R19-11, R21-11) to a normalized EMF view. Ensures GraphQL API is version-agnostic; callers do not need to know the underlying AUTOSAR release.")
    }

    %% External callers → REST Layer
    Rel(rustCli, restLayer, "POST /import, GET /export (CI batch)", "HTTP REST")

    %% External callers → GraphQL Endpoint
    Rel(rustSvc, gqlEndpoint, "GraphQL mutations: importArxml, exportArxml, applyOps, queries: model state", "HTTP GraphQL")

    %% REST → Services
    Rel(restLayer, arxmlImport, "Trigger import from ARXML file", "Java call")
    Rel(restLayer, arxmlExport, "Trigger ARXML serialization", "Java call")

    %% GraphQL → internal components
    Rel(gqlEndpoint, emfRepository, "Read/write EMF model instances", "Java call")
    Rel(gqlEndpoint, arxmlImport, "Invoke import pipeline", "Java call")
    Rel(gqlEndpoint, arxmlExport, "Invoke export/serialization", "Java call")
    Rel(gqlEndpoint, versionAdapter, "Normalize AUTOSAR version on read", "Java call")

    %% Import/Export ↔ Repository
    Rel(arxmlImport, emfRepository, "Populate EMF model after parse", "Java call")
    Rel(arxmlExport, emfRepository, "Read EMF model for serialization", "Java call")
    Rel(versionAdapter, emfRepository, "Normalize version on model load", "Java call")

    %% External file flows
    Rel(legacyTools, restLayer, "ARXML files provided for import", "File / ARXML")
    Rel(arxmlExport, buildToolchain, "Writes exported ARXML files", "File / ARXML")
    Rel(arxmlExport, codeGen, "ARXML consumed by code generators", "File / ARXML")
```

---

## Component Descriptions

### REST Layer
- Spring Boot `@RestController` providing optional HTTP endpoints.
- `/import` — accepts an ARXML file path or upload for CI/batch import.
- `/export` — triggers ARXML serialization and returns a file path or stream.
- Used primarily by `qorix_cli` in CI pipelines. The Rust Domain Service uses GraphQL, not REST.

### GraphQL Endpoint
- The **primary API surface** for all Rust consumers.
- Defined by a typed schema; callers issue queries and mutations.
- Key mutations exposed:
  - `importArxml(filePaths: [String!]!)` — load ARXML into EMF
  - `exportArxml(outputPath: String!)` — serialize EMF to ARXML
  - `applyOps(ops: [OperationInput!]!)` — apply Rust-computed ops to EMF model
- Key queries:
  - Read model state, validate consistency

### EmfRepository
- Holds all in-memory EMF `EObject` instances for the current AUTOSAR project.
- Handles multi-file ARXML projects (a single project can span many `.arxml` files).
- Acts as the shared in-memory state between Import, Export, and op-apply logic.
- **Never exposed directly to Rust** — only accessed through GraphQL.

### ArxmlImportService
- Invokes ARTOP's ARXML parser to load `.arxml` files from the filesystem.
- Populates `EmfRepository` with the resulting EMF model tree.
- Normalizes via `AutosarVersionAdapter` on load.
- Called by both the GraphQL endpoint (IDE/interactive) and the REST layer (CI batch).

### ArxmlExportService
- Reads the current EMF model from `EmfRepository`.
- Serializes it back to `.arxml` file(s) using ARTOP's writer APIs.
- Triggered by Rust via a GraphQL `exportArxml` mutation after all ops have been applied.
- Produces ARXML compatible with downstream toolchains and legacy AUTOSAR tools.

### AutosarVersionAdapter
- Abstracts AUTOSAR schema version differences (Classic R4.x series, Adaptive releases).
- Maps version-specific EMF model constructs to a normalized view that the GraphQL schema can express uniformly.
- Ensures the GraphQL API remains stable as AUTOSAR schema versions evolve.

---

## Data Flows

### Import Flow (ARXML → YAML)
```
ARXML files → ArxmlImportService → EmfRepository
EmfRepository → GraphQL Endpoint → Rust Domain Service
Rust Domain Service → Rust model → YAML files
```

### Export Flow (YAML → ARXML)
```
YAML files → Rust Domain Service → Rust model → GraphQL mutations (applyOps)
GraphQL Endpoint → EmfRepository → ArxmlExportService → ARXML files
```

---

## Key Design Constraints

- **Rust never touches EMF.** `core::gql_client` (a generated GraphQL client) is the only bridge. All Rust code that needs ARXML data goes through GraphQL mutations/queries.
- **Spring Boot / EMF are implementation details.** The GraphQL contract is the stable interface; ARTOP and EMF internals can evolve without affecting Rust.
- **Version adapter is the AUTOSAR compatibility layer.** New AUTOSAR schema versions are absorbed here, not propagated into Rust model changes.
- **Classic and Adaptive share this gateway.** Both stacks use the same Spring Boot service; the ARTOP libraries support both Classic and Adaptive ARXML.
