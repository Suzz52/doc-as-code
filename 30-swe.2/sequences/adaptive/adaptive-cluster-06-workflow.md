# adaptive-cluster-06-workflow — Deployment Designer

## Designer: A6 — Deployment Designer
**YAML file:** `deployment-manifest.yaml`

## Overview

This workflow covers binding applications and their processes to target machines. The Deployment Designer is the final integration canvas — it draws together services (A1), communication (A2), machine topology (A3), platform services (A4), and execution manifests (A5) into a complete deployment map. Every application must be deployed to exactly one machine. Validation confirms resource constraints, IPC binding feasibility, and complete deployment coverage.

---

## Workflow Steps

1. User opens the Deployment Designer (tab A6).
2. Designer loads all prior outputs: applications (A1), machines (A3), processes (A5).
3. User drags application nodes onto target machine nodes in the Mapping View.
4. WASM validates resource fit (CPU, RAM) per machine.
5. WASM cross-validates IPC bindings (from A2) — both endpoints must be on the same machine.
6. User reviews the Table View to confirm all deployments.
7. User runs the Validation view to get the full cross-canvas checklist.
8. On full pass, system is declared ready for ARXML generation.

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE Canvas (A6)
    participant A1YAML as application-design.yaml
    participant A3YAML as machine-design.yaml
    participant A5YAML as execution-manifest.yaml
    participant DepYAML as deployment-manifest.yaml
    participant WASM as WASM Bridge
    participant Val as Validation Pane
    participant RustSvc as Rust Domain Service

    User->>IDE: Open Deployment Designer (A6)
    IDE->>A1YAML: Load application list (FusionApp, RadarApp, CameraApp)
    IDE->>A3YAML: Load machine inventory (ComputeECU, SensorECU, CameraECU)
    IDE->>A5YAML: Load process bindings
    IDE-->>User: Mapping canvas with undeployed app nodes and machine targets

    User->>IDE: Drag FusionApp → ComputeECU
    IDE->>DepYAML: Append deployment {application: FusionApp, process: FusionProcess, machine: ComputeECU}
    DepYAML-->>WASM: Revalidate resource fit
    WASM-->>Val: ✓ ComputeECU has sufficient CPU and RAM for FusionApp

    User->>IDE: Drag RadarApp → SensorECU
    IDE->>DepYAML: Append deployment {application: RadarApp, machine: SensorECU}
    DepYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ SensorECU resource constraints satisfied

    User->>IDE: Drag CameraApp → CameraECU
    IDE->>DepYAML: Append deployment {application: CameraApp, machine: CameraECU}
    DepYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ All applications deployed

    WASM-->>WASM: Cross-validate IPC bindings from communication-design.yaml
    WASM-->>Val: ✓ No IPC bindings span different machines

    alt Resource overcommit
        WASM-->>Val: ⚠ SensorECU RAM budget exceeded — RadarApp requires 3 GB, only 2 GB available
        User->>IDE: Drag RadarApp → ComputeECU instead
        IDE->>DepYAML: Update deployment.machine = ComputeECU
        WASM-->>Val: ✓ Resource constraints satisfied
    end

    alt Missing deployment
        WASM-->>Val: ✗ CameraApp not deployed to any machine
        User->>IDE: Drag CameraApp to CameraECU
        DepYAML-->>WASM: Revalidate
        WASM-->>Val: ✓ All 3 applications deployed
    end

    User->>IDE: Switch to Table View (≡ Table)
    IDE-->>User: Table: FusionApp/ComputeECU, RadarApp/SensorECU, CameraApp/CameraECU — all DEPLOYED

    User->>IDE: Switch to Validation View (✓ Validation)
    IDE-->>User: ✓ All applications deployed, ✓ Resource constraints OK, ℹ ARXML export ready

    User->>IDE: Trigger full cross-canvas validation
    IDE->>RustSvc: POST /validate {stack: adaptive, projectId, yamlDocuments: all 6}
    RustSvc-->>IDE: Full Diagnostic[] — 0 errors, 0 warnings

    User->>RustSvc: Generate ARXML (POST /applyOpsAndSync with syncArxml: true)
    RustSvc-->>IDE: ApplicationManifest.arxml, ExecutionManifest.arxml, MachineManifest.arxml
    IDE-->>User: ✓ ARXML artifacts generated successfully
```

---

## Key Entities Involved

| Entity | Type | YAML Path |
|---|---|---|
| `FusionApp → ComputeECU` | Deployment | `deployments[0]` |
| `RadarApp → SensorECU` | Deployment | `deployments[1]` |
| `CameraApp → CameraECU` | Deployment | `deployments[2]` |
| Core affinity | Runtime | `deployments[*].core_affinity` |
| Process reference | Runtime | `deployments[*].process` |

---

## Validation Rules (WASM + Rust Domain Service — `adaptive::validation`)

- Every application must be deployed to exactly one machine.
- Target machine must have sufficient CPU and RAM for the process (cross-referenced from A5 execution manifest).
- IPC bindings (from A2) require both provider and consumer to be on the same machine.
- Core affinity values must not exceed the target machine's core count (from A3).
- All 6 YAML files must pass full cross-canvas validation before ARXML generation is permitted.

---

## Outputs

- `deployment-manifest.yaml` — complete application-to-machine deployment map.
- Full cross-canvas validation pass (all 6 designers).
- **ARXML artifacts:** `ApplicationManifest.arxml`, `ExecutionManifest.arxml`, `MachineManifest.arxml` generated via ARXML Gateway.
