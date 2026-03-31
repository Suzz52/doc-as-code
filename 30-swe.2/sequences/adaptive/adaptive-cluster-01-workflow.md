# adaptive-cluster-01-workflow — Application & Service Designer

## Designer: A1 — Application & Service Designer
**YAML file:** `application-design.yaml`

## Overview

This workflow covers the end-to-end sequence of defining Adaptive AUTOSAR applications and their service interfaces inside the Application & Service Designer. The designer exposes services (methods, events, data types) and the dependency graph between producer and consumer applications. Every user action on the canvas is bidirectionally synced to `application-design.yaml` and validated in real time via WASM.

---

## Workflow Steps

1. User opens the Application & Service Designer (tab A1).
2. User creates or selects a service block on the service canvas.
3. User adds methods and events to the service using the Element Palette.
4. User sets service properties (namespace, version) in the Properties panel.
5. WASM validates method signatures and data type references on each edit.
6. User reviews the Flat View table to verify all services, methods, and events.
7. User resolves any validation errors shown in the Validation pane.
8. YAML is confirmed in sync; canvas is ready for Communication Designer (A2).

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE Canvas (A1)
    participant Palette as Element Palette
    participant Props as Properties Panel
    participant WASM as WASM Bridge
    participant YAML as application-design.yaml
    participant Val as Validation Pane

    User->>IDE: Open Application & Service Designer (A1)
    IDE->>YAML: Load existing service definitions
    YAML-->>IDE: Render RadarService, CameraService, FusionService blocks

    User->>Palette: Click "+ Service"
    Palette->>IDE: Add new service block to canvas
    IDE->>YAML: Append service entry (partial, name pending)

    User->>Props: Set namespace = "perception", version = "1.0.0"
    Props->>YAML: Update service.namespace, service.version
    YAML-->>WASM: Trigger revalidation (debounced 300ms)
    WASM-->>Val: Diagnostic[] — no errors

    User->>Palette: Click "+ Method"
    Palette->>IDE: Add method item to selected service
    User->>Props: Set method name = "ProcessFrame", return_type = "FusedResult"
    Props->>YAML: Append method entry
    YAML-->>WASM: Revalidate
    WASM-->>Val: ✓ Method signature valid

    User->>Palette: Click "+ Event"
    Palette->>IDE: Add event item to selected service
    User->>Props: Set event name = "OnFusionComplete", payload = "FusionEvent"
    Props->>YAML: Append event entry
    YAML-->>WASM: Revalidate
    WASM-->>Val: ✓ Event payload type resolved

    User->>IDE: Draw dependency arrow from RadarService → FusionService
    IDE->>YAML: Record service dependency binding
    YAML-->>WASM: Revalidate cross-service references
    WASM-->>Val: ✓ All service bindings resolvable

    User->>IDE: Switch to Flat View (≡ Flat)
    IDE-->>User: Table: 3 Services, 7 Methods, 3 Events — all OK

    alt Validation error present
        Val-->>User: ⚠ DataType "ObjectList" not defined
        User->>Props: Add missing DataType via palette
        Props->>YAML: Append datatype entry
        YAML-->>WASM: Revalidate
        WASM-->>Val: ✓ All types resolved
    end

    User->>IDE: Confirm YAML in sync (● In Sync indicator)
    IDE-->>User: A1 complete — proceed to Communication Designer (A2)
```

---

## Key Entities Involved

| Entity | Type | YAML Path |
|---|---|---|
| `RadarService` | Service | `services[0]` |
| `CameraService` | Service | `services[1]` |
| `FusionService` | Service | `services[2]` |
| `GetObjectList` | Method | `services[0].methods[0]` |
| `OnObjectDetected` | Event | `services[0].events[0]` |
| `ProcessFrame` | Method | `services[2].methods[0]` |
| `OnFusionComplete` | Event | `services[2].events[0]` |

---

## Validation Rules (WASM — `adaptive::validation`)

- Every method must declare a `return_type` that resolves to a defined datatype.
- Every event must declare a `payload` type that resolves to a defined datatype.
- Service `namespace` must be a valid reverse-domain identifier.
- No two services in the same namespace may share a name.
- Service `version` must follow semver (`major.minor.patch`).

---

## Outputs

- `application-design.yaml` — updated with all service interfaces.
- Validated service graph ready for binding in **A2 Communication Designer**.
