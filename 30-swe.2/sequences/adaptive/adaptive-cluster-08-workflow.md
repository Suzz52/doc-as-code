# adaptive-cluster-08-workflow — ARXML Export & Migration (Adaptive)

## Designer: A6 Deployment Designer → ARXML Gateway
**Context:** End-to-end ARXML generation and legacy ARXML import/migration for Adaptive stack

## Overview

This workflow covers two complementary flows:
1. **Export:** Converting a completed, validated Adaptive AUTOSAR YAML project to ARXML artifacts (ApplicationManifest, ExecutionManifest, MachineManifest) for downstream toolchains.
2. **Import/Migration:** Loading an existing Adaptive ARXML project into Qorix, running autorepair/normalization, and producing the six YAML files as the new source of truth.

Both flows go through the Rust Domain Service and ARXML Gateway (Spring Boot + ARTOP + GraphQL). Rust never touches ARXML or EMF directly.

---

## Part 1 — Export Flow (YAML → ARXML)

### Workflow Steps

1. All 6 Adaptive YAML files are validated (full cross-canvas pass).
2. User triggers "Generate ARXML" from the Deployment Designer or CLI.
3. Rust Domain Service computes an `OperationPlan` for the full model sync.
4. `core::gql_client` sends `applyOps` mutation to ARXML Gateway.
5. ARXML Gateway applies ops to EMF/ARTOP model.
6. `exportArxml` mutation triggers serialization to `.arxml` files.
7. ARXML artifacts are written to the output directory.

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE (A6 Deployment Designer)
    participant Rust as Rust Domain Service
    participant GQL as ARXML Gateway (GraphQL)
    participant EMF as EMF / ARTOP Model
    participant FS as ARXML Files

    User->>IDE: Click "Generate ARXML" (all 6 YAML validated, 0 errors)

    IDE->>Rust: POST /applyOpsAndSync {stack:adaptive, syncArxml:true, yamlDocuments}
    Rust->>Rust: Load all 6 YAML → adaptive model → compute Ops[]

    Rust->>GQL: mutation applyOps(stack:ADAPTIVE, projectId, operations:[...])
    GQL->>EMF: Apply structured ops to ARTOP model
    EMF-->>GQL: OK

    Rust->>GQL: mutation exportArxml(stack:ADAPTIVE, outputPath:"/out/arxml")
    GQL->>EMF: Serialize model → ARXML
    EMF->>FS: Write ApplicationManifest.arxml
    EMF->>FS: Write ExecutionManifest.arxml
    EMF->>FS: Write MachineManifest.arxml
    FS-->>GQL: Artifact paths
    GQL-->>Rust: {success:true, artifacts:[...]}

    Rust-->>IDE: Updated YAML + artifact manifest
    IDE-->>User: ✓ ARXML generated: ApplicationManifest.arxml, ExecutionManifest.arxml, MachineManifest.arxml
```

---

## Part 2 — Import / Migration Flow (ARXML → YAML)

### Workflow Steps

1. User opens Migration Wizard and selects Adaptive ARXML files.
2. ARXML Gateway loads files into EMF/ARTOP model via `importArxml`.
3. `adaptive::migration` pipeline runs: parse → normalize → autorepair → report.
4. Normalized YAML files are generated and written to the project directory.
5. WASM validates the generated YAML files.
6. User reviews migration diagnostics and AI-assisted fix proposals for any warnings.
7. User accepts fixes; YAML files are confirmed as new source of truth.

```mermaid
sequenceDiagram
    actor User
    participant Wizard as Migration Wizard
    participant Rust as Rust Domain Service
    participant GQL as ARXML Gateway (GraphQL)
    participant EMF as EMF / ARTOP Model
    participant WASM as WASM Bridge
    participant YAML as Generated YAML Files
    participant MCP as Developer Agent (MCP)

    User->>Wizard: Open Migration Wizard, select Adaptive ARXML files

    Wizard->>Rust: POST /migrate {stack:adaptive, arxmlPaths:[...]}
    Rust->>GQL: mutation importArxml(filePaths:[...], stack:ADAPTIVE)
    GQL->>EMF: Parse ARXML → populate ARTOP model
    EMF-->>GQL: Model loaded
    GQL-->>Rust: {success:true}

    Rust->>GQL: mutation migrateArxmlToYaml(filePaths:[...], stack:ADAPTIVE)
    GQL-->>Rust: {yamlDocuments:{...}, steps:[parse✓, normalize✓, autorepair⚠], diagnostics:[...]}

    Note over Rust: adaptive::migration pipeline runs internally

    Rust->>YAML: Write application-design.yaml
    Rust->>YAML: Write communication-design.yaml
    Rust->>YAML: Write machine-design.yaml
    Rust->>YAML: Write platform-services.yaml
    Rust->>YAML: Write execution-manifest.yaml
    Rust->>YAML: Write deployment-manifest.yaml

    Rust-->>Wizard: Migration result {steps, diagnostics, yamlPaths}
    Wizard-->>User: Migration report: parse ✓, normalize ✓, autorepair ⚠ (2 inferred)

    Wizard->>WASM: validateYaml(adaptive, allGeneratedYamlDocs)
    WASM-->>Wizard: Diagnostic[] — 2 warnings

    Wizard-->>User: Show 2 autorepair warnings (inferred service bindings)

    alt AI-assisted fix
        User->>MCP: "Review autorepair suggestions"
        MCP->>Rust: POST /planOps {intentType:fix-missing-service-bindings}
        Rust-->>MCP: OperationPlan
        MCP-->>Wizard: Proposed fixes
        User->>Wizard: Accept fixes
        Wizard->>WASM: Re-validate
        WASM-->>Wizard: ✓ 0 warnings
    end

    Wizard-->>User: ✓ Migration complete — 6 YAML files ready as source of truth
```

---

## ARXML Artifacts Produced (Adaptive Export)

| Artifact | Content |
|---|---|
| `ApplicationManifest.arxml` | Service interfaces, methods, events, data types |
| `ExecutionManifest.arxml` | Process definitions, thread configs, functional groups |
| `MachineManifest.arxml` | Hardware topology, platform services, network config |

---

## Migration Autorepair Capabilities (Adaptive)

| Autorepair Action | Trigger |
|---|---|
| Infer service binding transport | Binding has no transport specified → default SOME/IP |
| Normalize service interface names | CamelCase/snake_case normalisation |
| Infer thread period from OS config | Thread with no period → derived from execution manifest context |
| Missing machine → create placeholder | Application deployed to undefined machine |

---

## Key Design Constraints

- Rust never reads or writes `.arxml` files directly — all ARXML IO goes through the ARXML Gateway.
- Import/export flows are identical between IDE (interactive) and CLI (`qorix generate-arxml`, `qorix migrate`) — same Rust domain core.
- The generated YAML is the new source of truth after migration — ARXML is not kept as working copy.
- ARXML version normalisation (R19-11 vs R21-11 etc.) is handled transparently by `AutosarVersionAdapter` inside the gateway.
