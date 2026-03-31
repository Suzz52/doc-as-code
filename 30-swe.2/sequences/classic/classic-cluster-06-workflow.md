# classic-cluster-06-workflow — RTE & Mapping Designer

## Designer: C6 — RTE & Mapping Designer
**YAML file:** `rte-mapping.yaml`

## Overview

This workflow covers the final integration step in Classic AUTOSAR design — wiring the Runtime Environment (RTE). The RTE & Mapping Designer connects SWC ports (C1) to communication signals (C2) and maps runnables (C1) to OS tasks (C4). This is the cross-cutting integration canvas: every SWC port must be connected either to another SWC port (intra-ECU) or to a ComStack signal (inter-ECU). Validation is the most comprehensive in the Classic pipeline, producing errors for any unconnected port or unmapped runnable.

---

## Workflow Steps

1. User opens the RTE & Mapping Designer (tab C6).
2. Designer loads all SWC ports (C1), signals (C2), and task assignments (C4).
3. User draws port-to-port connections for intra-ECU communication.
4. User draws port-to-signal connections for inter-ECU communication via ComStack.
5. User reviews runnable-to-task mappings imported from C4 (auto-populated).
6. User adds client-server port connections (CS interface wiring).
7. WASM validates: all ports connected, all runnables mapped, data type consistency.
8. User runs full cross-canvas validation via Rust Domain Service.
9. On clean pass, system is ready for ARXML generation.

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE Canvas (C6)
    participant C1YAML as swc-design.yaml
    participant C2YAML as signals-comstack.yaml
    participant C4YAML as os-scheduling.yaml
    participant RteYAML as rte-mapping.yaml
    participant WASM as WASM Bridge
    participant Val as Validation Pane
    participant RustSvc as Rust Domain Service

    User->>IDE: Open RTE & Mapping Designer (C6)
    IDE->>C1YAML: Load SWC ports and runnables
    IDE->>C2YAML: Load signals and ComStack
    IDE->>C4YAML: Load task-runnable assignments
    IDE-->>User: Flow View canvas: SWC port nodes on left, signal nodes on right

    Note over IDE: Runnable-to-task mappings auto-populated from C4

    User->>IDE: Draw connection: SpeedSensor.SpeedOut (P-Port) → BrakeController.SpeedIn (R-Port)
    IDE->>RteYAML: Append port_to_port_connection {from: SpeedSensor.SpeedOut, to: BrakeController.SpeedIn}
    RteYAML-->>WASM: Revalidate (cross-file: swc-design.yaml)
    WASM-->>Val: ✓ Intra-ECU SR connection valid — data type Float32 matches

    User->>IDE: Draw connection: SpeedSensor.SpeedOut → VehicleSpeedSignal (ComStack)
    IDE->>RteYAML: Append port_to_signal_connection {port: SpeedSensor.SpeedOut, signal: VehicleSpeedSignal}
    RteYAML-->>WASM: Revalidate (cross-file: signals-comstack.yaml)
    WASM-->>Val: ✓ Port-to-signal binding valid — data type Float32 consistent

    User->>IDE: View runnable-to-task table
    IDE-->>User: ReadSpeed_10ms → Task_10ms, ComputeBrake_10ms → Task_10ms (from C4)
    IDE-->>Val: ✓ All runnables mapped (no pending warnings from C1)

    User->>IDE: Draw CS connection: BrakeController.DiagClient → DiagServer.DiagServer_Port
    IDE->>RteYAML: Append client_server_connection
    RteYAML-->>WASM: Revalidate CS interface wiring
    WASM-->>Val: ✓ Client-Server connection valid

    alt Unconnected P-Port
        WASM-->>Val: ✗ SpeedSensor.DebugOut (P-Port) not connected to any R-Port or signal
        User->>IDE: Connect DebugOut → DebugConsole.DebugIn
        IDE->>RteYAML: Append missing connection
        WASM-->>Val: ✓ All ports connected
    end

    alt Data type mismatch on port-to-signal binding
        WASM-->>Val: ✗ BrakeController.BrakeOut (Uint8) incompatible with BrakeSignal (Float32)
        User->>IDE: Update swc-design.yaml — change BrakeOut type to Float32
        C1YAML-->>WASM: Revalidate cross-canvas
        WASM-->>Val: ✓ Type mismatch resolved
    end

    alt Runnable still unmapped
        WASM-->>Val: ✗ Runnable "PostRunInit" not mapped to any OS task
        User->>IDE: Navigate to C4, add Task_Init, assign PostRunInit
        C4YAML-->>RteYAML: Cross-canvas sync
        WASM-->>Val: ✓ All runnables mapped
    end

    User->>IDE: Switch to Table View (≡ Table)
    IDE-->>User: Table: all port connections, signal bindings, runnable-task mappings — all OK

    User->>IDE: Trigger full cross-canvas validation
    IDE->>RustSvc: POST /validate {stack: classic, projectId, yamlDocuments: all 6}
    RustSvc-->>IDE: Diagnostic[] — 0 errors, 0 warnings

    User->>RustSvc: Generate ARXML (POST /applyOpsAndSync syncArxml:true)
    RustSvc-->>IDE: ECU-Extract.arxml, SWC-Extract.arxml, System-Extract.arxml
    IDE-->>User: ✓ ARXML artifacts generated successfully
```

---

## Key Entities Involved

| Entity | Type | YAML Path |
|---|---|---|
| SpeedSensor.SpeedOut → BrakeController.SpeedIn | Port-to-port (SR) | `port_connections[0]` |
| SpeedSensor.SpeedOut → VehicleSpeedSignal | Port-to-signal | `signal_mappings[0]` |
| ReadSpeed_10ms → Task_10ms | Runnable-to-task | `runnable_mappings[0]` |
| BrakeController.DiagClient → DiagServer | Client-server wiring | `cs_connections[0]` |

---

## Validation Rules (WASM + Rust Domain Service — `classic::validation`)

- Every SWC P-Port must be connected to at least one R-Port or signal.
- Every SWC R-Port must be connected to exactly one P-Port or signal.
- SR port-to-port connections must use the same interface and matching data element types.
- CS client port must connect to a server port with the same operation list.
- Port-to-signal bindings must have matching data types between port data element and signal type.
- Every runnable from `swc-design.yaml` must appear in exactly one runnable-task mapping.
- All 6 YAML files must pass full cross-canvas validation before ARXML generation is permitted.

---

## Outputs

- `rte-mapping.yaml` — all port connections, signal bindings, and runnable-to-task mappings.
- Full cross-canvas validation pass (all 6 Classic designers).
- **ARXML artifacts:** `ECU-Extract.arxml`, `SWC-Extract.arxml`, `System-Extract.arxml` generated via ARXML Gateway.
