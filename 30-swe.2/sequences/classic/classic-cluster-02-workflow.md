# classic-cluster-02-workflow — Signals & ComStack Designer

## Designer: C2 — Signals & ComStack Designer
**YAML file:** `signals-comstack.yaml`

## Overview

This workflow covers defining communication signals, I-PDUs, PDUs, and the COM/PduR/CanIf routing stack in the Signals & ComStack Designer. Signals are bound to SWC ports (from C1), packed into I-PDUs, routed through PduR, and transmitted via CanIf channels. The Network Graph view shows bus topology with PDUs and signals. Validation ensures complete routing paths from SWC data element to bus frame.

---

## Workflow Steps

1. User opens the Signals & ComStack Designer (tab C2).
2. Designer loads SWC port data elements from `swc-design.yaml` (C1 output).
3. User defines signals (name, data type, byte order).
4. User binds each signal to an SWC port data element.
5. User creates I-PDUs and assigns signals to I-PDU positions.
6. User creates PDU routing paths in PduR.
7. User configures CanIf channels and assigns I-PDUs to channels.
8. WASM validates the complete routing chain (signal → I-PDU → PduR → CanIf → bus).
9. User reviews the Signal/PDU Matrix view.
10. YAML confirmed in sync; ComStack ready for ECU/BSW (C3) and RTE mapping (C6).

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE Canvas (C2)
    participant C1YAML as swc-design.yaml
    participant CommYAML as signals-comstack.yaml
    participant WASM as WASM Bridge
    participant Val as Validation Pane
    participant Props as Properties Panel

    User->>IDE: Open Signals & ComStack Designer (C2)
    IDE->>C1YAML: Load SWC port data elements (VehicleSpeed, BrakePressure...)
    C1YAML-->>IDE: Render signal sources from SWC ports on Network Graph

    User->>Props: Define signal: name="VehicleSpeedSignal", type=Float32, byte_order=big_endian
    Props->>CommYAML: Append signal definition
    CommYAML-->>WASM: Revalidate
    WASM-->>Val: ⚠ Signal not yet bound to SWC port

    User->>IDE: Bind VehicleSpeedSignal → SpeedSensor.SpeedOut (data element)
    IDE->>CommYAML: Update signal.port_binding
    CommYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ Signal bound to SWC port data element

    User->>Palette: Click "+ I-PDU"
    User->>Props: Name = "VehicleSpeedIPdu", length = 8 bytes
    Props->>CommYAML: Append ipdu entry
    CommYAML-->>WASM: Revalidate
    WASM-->>Val: ⚠ I-PDU has no signals assigned

    User->>IDE: Assign VehicleSpeedSignal → VehicleSpeedIPdu (drag signal to I-PDU slot)
    IDE->>CommYAML: Update ipdu.signals[], set bit_position = 0, bit_length = 32
    CommYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ Signal packed into I-PDU

    User->>Palette: Click "+ PduR Route"
    User->>Props: Route: VehicleSpeedIPdu → CanIf_Channel_CAN1
    Props->>CommYAML: Append pdur_routing entry
    CommYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ PduR routing path defined

    User->>Palette: Click "+ CanIf Channel"
    User->>Props: Name = "CAN1", baudrate = 500kbps, network_handle = 0
    Props->>CommYAML: Append canif_channel entry
    CommYAML-->>WASM: Revalidate full routing chain
    WASM-->>Val: ✓ Signal → I-PDU → PduR → CanIf → CAN1 routing complete

    alt Signal overlap in I-PDU
        WASM-->>Val: ✗ Signal "BrakeSignal" overlaps bits 0-31 with "VehicleSpeedSignal"
        User->>Props: Adjust bit_position = 32 for BrakeSignal
        Props->>CommYAML: Update signal bit_position
        WASM-->>Val: ✓ No signal overlaps in I-PDU
    end

    alt Unbound signal
        WASM-->>Val: ⚠ Signal "EngineRPM" not bound to any SWC port
        User->>IDE: Bind signal to SWC port or delete if unused
        WASM-->>Val: ✓ All signals bound
    end

    User->>IDE: Switch to Signal/PDU Matrix View
    IDE-->>User: Matrix: all signals, I-PDU assignments, PduR routes, CanIf channels

    User->>IDE: Confirm YAML in sync (● In Sync indicator)
    IDE-->>User: C2 complete — proceed to ECU & BSW (C3)
```

---

## Key Entities Involved

| Entity | Type | YAML Path |
|---|---|---|
| `VehicleSpeedSignal` | Signal | `signals[0]` |
| `VehicleSpeedIPdu` | I-PDU | `ipdus[0]` |
| PduR route | Routing | `pdur_routings[0]` |
| `CAN1` | CanIf Channel | `canif_channels[0]` |
| Signal bit position | Config | `ipdus[0].signals[0].bit_position` |

---

## Validation Rules (WASM — `classic::validation`)

- Every signal must be bound to exactly one SWC port data element (from `swc-design.yaml`).
- Signals within an I-PDU must not have overlapping bit ranges.
- Total signal bits in an I-PDU must not exceed `length_bytes * 8`.
- Every I-PDU must have at least one PduR routing path.
- Every PduR routing path must terminate at a valid CanIf channel.
- CanIf channel baudrate must be a valid CAN standard (125k, 250k, 500k, 1M).

---

## Outputs

- `signals-comstack.yaml` — all signals, I-PDUs, PduR routing, and CanIf channel config.
- Validated ComStack ready for BSW module config in **C3 ECU & BSW** and port-signal mapping in **C6 RTE & Mapping**.
