# iface-rust-graphql — Rust Domain Service ↔ ARXML Gateway (GraphQL)

## Purpose

This document specifies the interface contract between the **Rust Domain Service** (and `qorix_cli`) and the **ARXML Gateway** (Spring Boot + ARTOP). GraphQL is the **primary and only** API surface through which Rust interacts with the EMF/ARTOP model. Rust never accesses EMF classes, Java APIs, or ARXML files directly.

---

## Interface Overview

```
Rust Domain Service / qorix_cli
       │
       │  core::gql_client (generated GraphQL client)
       │  HTTP POST  /graphql
       ▼
ARXML Gateway (Spring Boot + GraphQL endpoint)
       │
       ├── EmfRepository       (in-memory ARTOP/EMF model)
       ├── ArxmlImportService  (ARXML → EMF)
       ├── ArxmlExportService  (EMF → ARXML)
       └── AutosarVersionAdapter (version normalisation)
```

**Key invariant:** Rust uses `core::gql_client`, a generated client from the GraphQL schema. This client is the single, type-safe bridge. All EMF, ARTOP, and Java internals are hidden behind the GraphQL contract.

---

## Transport

| Attribute | Value |
|---|---|
| Protocol | HTTP/1.1 or HTTP/2 |
| Endpoint | `POST /graphql` |
| Base URL | `http://arxml-gateway:8080` (configurable via `--gateway-url`) |
| Content-Type | `application/json` (GraphQL over JSON) |
| Auth | Internal service network; mTLS in production |

---

## GraphQL Schema (Rust-facing contract)

```graphql
# ── Types ──────────────────────────────────────────────────

scalar JSON
scalar FilePath

enum AutosarStack {
  CLASSIC
  ADAPTIVE
}

type Diagnostic {
  severity: String!   # "error" | "warning" | "info"
  code:     String!
  message:  String!
  path:     String
}

type OperationResult {
  success:     Boolean!
  diagnostics: [Diagnostic!]!
  artifacts:   [FilePath!]
}

type MigrationResult {
  success:       Boolean!
  yamlDocuments: JSON
  diagnostics:   [Diagnostic!]!
  steps:         [MigrationStep!]!
}

type MigrationStep {
  name:    String!
  status:  String!   # "success" | "warning" | "failed"
  detail:  String
}

input OperationInput {
  kind:  String!   # "add" | "update" | "delete"
  file:  String!
  path:  String!
  value: JSON
}

# ── Queries ────────────────────────────────────────────────

type Query {
  # Check gateway health and loaded project state
  gatewayStatus: GatewayStatus!

  # Query current in-memory EMF model state as normalized JSON
  modelSnapshot(stack: AutosarStack!): JSON!
}

type GatewayStatus {
  healthy:    Boolean!
  version:    String!
  loadedFiles: [String!]!
}

# ── Mutations ──────────────────────────────────────────────

type Mutation {
  # Load ARXML files into EMF model (replaces any existing model)
  importArxml(
    filePaths: [String!]!
    stack:     AutosarStack!
  ): OperationResult!

  # Apply a list of Rust-computed ops to the EMF model
  applyOps(
    stack:      AutosarStack!
    projectId:  String!
    operations: [OperationInput!]!
  ): OperationResult!

  # Serialize the current EMF model to ARXML files
  exportArxml(
    stack:      AutosarStack!
    outputPath: String!
  ): OperationResult!

  # Full pipeline: import ARXML → normalize → return YAML representation
  migrateArxmlToYaml(
    filePaths: [String!]!
    stack:     AutosarStack!
  ): MigrationResult!
}
```

---

## Mutations — Rust Usage

### `importArxml`

Called by `classic::migration` and `adaptive::migration` when loading an existing ARXML project.

**Rust call site (`core::gql_client`):**
```rust
let result = gql_client
    .import_arxml(vec!["/path/to/project.arxml"], AutosarStack::Classic)
    .await?;
```

**GraphQL request:**
```graphql
mutation ImportArxml($filePaths: [String!]!, $stack: AutosarStack!) {
  importArxml(filePaths: $filePaths, stack: $stack) {
    success
    diagnostics { severity code message path }
    artifacts
  }
}
```

**Variables:**
```json
{
  "filePaths": ["/data/my-project.arxml"],
  "stack": "CLASSIC"
}
```

**Response:**
```json
{
  "data": {
    "importArxml": {
      "success": true,
      "diagnostics": [],
      "artifacts": []
    }
  }
}
```

---

### `applyOps`

Called after Rust computes an `OperationPlan` that needs to be reflected in ARXML. The ops are expressed as structured path-based mutations; the gateway applies them to the in-memory EMF model.

**GraphQL request:**
```graphql
mutation ApplyOps($stack: AutosarStack!, $projectId: String!, $operations: [OperationInput!]!) {
  applyOps(stack: $stack, projectId: $projectId, operations: $operations) {
    success
    diagnostics { severity code message path }
  }
}
```

**Variables:**
```json
{
  "stack": "CLASSIC",
  "projectId": "my-ecu-project",
  "operations": [
    {
      "kind": "update",
      "file": "os-config.yaml",
      "path": "tasks[0].runnables",
      "value": ["MyRunnable", "OtherRunnable"]
    },
    {
      "kind": "add",
      "file": "swc-design.yaml",
      "path": "swcs[1].runnables",
      "value": { "name": "NewRunnable", "period_ms": 10 }
    }
  ]
}
```

**Response:**
```json
{
  "data": {
    "applyOps": {
      "success": true,
      "diagnostics": [
        {
          "severity": "warning",
          "code": "ARXML-COMPAT-001",
          "message": "Task budget at 78% — review timing",
          "path": "tasks[0]"
        }
      ]
    }
  }
}
```

---

### `exportArxml`

Called when Rust needs to produce ARXML files (for downstream build toolchain, legacy tool interop, or CI artifact). Always called after `applyOps` if ARXML output is required.

**GraphQL request:**
```graphql
mutation ExportArxml($stack: AutosarStack!, $outputPath: String!) {
  exportArxml(stack: $stack, outputPath: $outputPath) {
    success
    diagnostics { severity code message path }
    artifacts
  }
}
```

**Variables:**
```json
{
  "stack": "ADAPTIVE",
  "outputPath": "/out/arxml"
}
```

**Response:**
```json
{
  "data": {
    "exportArxml": {
      "success": true,
      "diagnostics": [],
      "artifacts": [
        "/out/arxml/machine-design.arxml",
        "/out/arxml/application-design.arxml",
        "/out/arxml/execution-manifest.arxml"
      ]
    }
  }
}
```

---

### `migrateArxmlToYaml`

Convenience pipeline mutation: loads ARXML, normalizes via `AutosarVersionAdapter`, runs autorepair, and returns the YAML representation. Used by the migration wizard flow.

**Variables:**
```json
{
  "filePaths": ["/legacy/tresos-export.arxml"],
  "stack": "CLASSIC"
}
```

**Response:**
```json
{
  "data": {
    "migrateArxmlToYaml": {
      "success": true,
      "yamlDocuments": {
        "swc-design.yaml": "...",
        "os-config.yaml": "..."
      },
      "diagnostics": [],
      "steps": [
        { "name": "parse",      "status": "success", "detail": "Loaded 2 ARXML files" },
        { "name": "normalize",  "status": "success", "detail": "Version R4.3 → normalized" },
        { "name": "autorepair", "status": "warning",  "detail": "Inferred timing for 3 runnables" }
      ]
    }
  }
}
```

---

## Import / Export Flows

### Import Flow (ARXML → YAML)

```
ARXML files on disk
      │
      ▼  importArxml mutation
ARXML Gateway  →  ArxmlImportService  →  EmfRepository (in-memory)
      │
      ▼  modelSnapshot query (optional) or migrateArxmlToYaml
Rust Domain Service  →  Rust model (classic::model / adaptive::model)
      │
      ▼
YAML files (written by Rust, saved to Git)
```

### Export Flow (YAML → ARXML)

```
YAML files (from Git)
      │
      ▼  Rust loads YAML → Rust model → computes Ops[]
Rust Domain Service
      │
      ▼  applyOps mutation
ARXML Gateway  →  EmfRepository updated
      │
      ▼  exportArxml mutation
ArxmlExportService  →  ARXML files on disk
```

---

## AUTOSAR Version Handling

The `AutosarVersionAdapter` in the gateway normalises schema version differences transparently. Rust does not need to specify or handle AUTOSAR version numbers explicitly.

| AUTOSAR Release | Stack | Status |
|---|---|---|
| R4.2.x, R4.3.x | Classic | Supported |
| R4.4.x | Classic | Supported |
| R19-11, R20-11 | Adaptive | Supported |
| R21-11, R22-11 | Adaptive | Supported |

Version normalisation happens in `AutosarVersionAdapter` on `importArxml`. The GraphQL schema and Rust model always see a version-agnostic view.

---

## Error Handling

| GraphQL error scenario | Rust behaviour |
|---|---|
| `importArxml` returns `success: false` | Abort migration pipeline; propagate diagnostics to IDE / CLI stdout |
| `applyOps` returns `success: false` | Do not proceed to `exportArxml`; report diagnostics |
| `exportArxml` returns `success: false` | Report artifact generation failure; exit code 1 in CLI |
| HTTP connection refused | `core::gql_client` retries 3× with exponential backoff; then returns `GatewayUnavailable` error |
| GraphQL schema mismatch | Fail fast at client generation time (compile-time schema check via `graphql-client` crate) |

---

## Schema Versioning & Client Generation

- `core::gql_client` is **generated** from the GraphQL SDL at build time using the `graphql-client` Rust crate.
- Any breaking change to the GraphQL schema requires a coordinated update of both the gateway and `core::gql_client`.
- Non-breaking additions (new fields, new mutations) are safe and do not require `core::gql_client` regeneration until they are used.
- The gateway schema is the **contract owner**; Rust is the **consumer**.

```
[Build time]
ARXML Gateway schema.graphql
         │
         ▼  graphql-client codegen
core::gql_client/src/generated.rs
         │
         ▼  rustc compile check
Rust Domain Service binary
```

---

## Key Design Constraints

- **Rust never touches EMF classes.** `core::gql_client` is the only bridge — no Java interop, no JNI, no shared memory.
- **GraphQL is the stable versioned contract.** EMF internals, ARTOP API changes, and Java dependency upgrades are absorbed by the gateway without affecting Rust.
- **Operations are expressed as path-based mutations.** Rust never sends EMF-specific concepts (EObjects, EReferences) — only generic `OperationInput` entries with file, path, kind, and value.
- **Import and export are the only ARXML IO paths.** No other component reads or writes ARXML files; all file IO is gateway-owned.
