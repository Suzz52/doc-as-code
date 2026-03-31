# classic-cluster-01-workflow — SWC & Interface Designer

## Designer: C1 — SWC & Interface Designer
**YAML file:** `swc-design.yaml`

## Overview

This workflow covers defining AUTOSAR Classic Software Components (SWCs), their ports (Provided/Required/Client-Server/Sender-Receiver), interfaces, runnables, and inter-runnable variables in the SWC & Interface Designer. The canvas displays the Virtual Functional Bus (VFB) view showing SWC port connections. Every change is bidirectionally synced to `swc-design.yaml` and validated by WASM in real time.

---

## Workflow Steps

1. User opens the SWC & Interface Designer (tab C1).
2. User creates SWC blocks on the VFB canvas.
3. User adds ports (P-Port / R-Port) to each SWC.
4. User creates interface definitions (SenderReceiver or ClientServer) and assigns to ports.
5. User connects ports between SWCs via data element links.
6. User adds runnables to each SWC's Internal Behavior.
7. WASM validates port types, interface compatibility, and runnable declarations.
8. User reviews the Flat View table to audit all SWCs, ports, and interfaces.
9. YAML confirmed in sync; SWC design ready for ComStack (C2) and OS Scheduling (C4).

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE Canvas (C1)
    participant Palette as Element Palette
    participant Props as Properties Panel
    participant WASM as WASM Bridge
    participant YAML as swc-design.yaml
    participant Val as Validation Pane

    User->>IDE: Open SWC & Interface Designer (C1)
    IDE->>YAML: Load existing SWC definitions
    YAML-->>IDE: Render SWC blocks on VFB canvas

    User->>Palette: Click "+ SWC"
    Palette->>IDE: Add new SWC block to canvas
    User->>Props: Set name = "SpeedSensor", category = "SENSOR"
    Props->>YAML: Append swc entry {name: SpeedSensor, category: SENSOR}
    YAML-->>WASM: Revalidate (debounced 300ms)
    WASM-->>Val: ⚠ SWC has no ports defined

    User->>Palette: Click "+ P-Port"
    Palette->>IDE: Add P-Port to SpeedSensor
    User->>Props: Set port name = "SpeedOut", interface = "SpeedInterface" (SR)
    Props->>YAML: Append port entry
    YAML-->>WASM: Revalidate
    WASM-->>Val: ⚠ Interface "SpeedInterface" not yet defined

    User->>Palette: Click "+ Interface (SR)"
    User->>Props: Define SpeedInterface: data element "VehicleSpeed" (Float32)
    Props->>YAML: Append interface definition
    YAML-->>WASM: Revalidate
    WASM-->>Val: ✓ P-Port interface resolved

    User->>Palette: Click "+ SWC" → "BrakeController"
    User->>Props: Add R-Port "SpeedIn" with interface = "SpeedInterface"
    Props->>YAML: Append BrakeController with R-Port
    YAML-->>WASM: Revalidate
    WASM-->>Val: ✓ Port interface types match

    User->>IDE: Draw connection: SpeedSensor.SpeedOut → BrakeController.SpeedIn
    IDE->>YAML: Record port connection
    YAML-->>WASM: Revalidate connection
    WASM-->>Val: ✓ Sender-Receiver connection valid

    User->>Props: Add runnable to SpeedSensor: "ReadSpeed_10ms", trigger = "TimingEvent"
    Props->>YAML: Append runnable under swc.internal_behavior
    YAML-->>WASM: Revalidate
    WASM-->>Val: ⚠ Runnable "ReadSpeed_10ms" not yet mapped to OS task (resolved in C4)

    User->>Props: Add runnable to BrakeController: "ComputeBrake_10ms"
    Props->>YAML: Append runnable
    YAML-->>WASM: Revalidate
    WASM-->>Val: ⚠ Runnable not mapped to OS task — expected in C4

    User->>IDE: Switch to Flat View (≡ Flat)
    IDE-->>User: Table: 2 SWCs, 3 ports, 1 SR interface, 2 runnables

    alt Type mismatch on port connection
        WASM-->>Val: ✗ Port type mismatch — SpeedIn expects Float32, SpeedOut sends Uint16
        User->>Props: Update data element type to Float32
        Props->>YAML: Update interface.data_element.type
        WASM-->>Val: ✓ Type mismatch resolved
    end

    User->>IDE: Confirm YAML in sync (● In Sync indicator)
    IDE-->>User: C1 complete — proceed to Signals & ComStack (C2)
```

---

## Key Entities Involved

| Entity | Type | YAML Path |
|---|---|---|
| `SpeedSensor` | SWC | `swcs[0]` |
| `BrakeController` | SWC | `swcs[1]` |
| `SpeedOut` | P-Port (SR) | `swcs[0].ports[0]` |
| `SpeedIn` | R-Port (SR) | `swcs[1].ports[0]` |
| `SpeedInterface` | Interface (SR) | `interfaces[0]` |
| `ReadSpeed_10ms` | Runnable | `swcs[0].internal_behavior.runnables[0]` |
| `ComputeBrake_10ms` | Runnable | `swcs[1].internal_behavior.runnables[0]` |

---

## Validation Rules (WASM — `classic::validation`)

- Every port must reference a declared interface.
- SR P-Port and R-Port must reference the same interface with compatible data element types.
- CS P-Port (Server) and R-Port (Client) must reference the same ClientServer interface.
- Runnable trigger type must be one of: `TimingEvent`, `DataReceivedEvent`, `InitEvent`, `BackgroundEvent`.
- Runnables without OS task mapping produce warnings (resolved in C4).

---

## Outputs

- `swc-design.yaml` — all SWCs, ports, interfaces, and runnables.
- Validated SWC graph ready for signal binding in **C2 Signals & ComStack** and task mapping in **C4 OS & Scheduling**.
