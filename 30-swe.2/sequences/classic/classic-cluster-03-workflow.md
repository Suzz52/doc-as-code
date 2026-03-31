# classic-cluster-03-workflow — ECU & BSW Designer

## Designer: C3 — ECU & BSW Designer
**YAML file:** `ecu-bsw.yaml`

## Overview

This workflow covers configuring the ECU board, BSW modules, and MCAL bindings in the ECU & BSW Designer. The Board View renders the ECU with its peripheral slots (CAN, LIN, SPI, Dio, Adc, Pwm ports). Users configure which BSW modules are active, set ECUC module parameters, and bind MCAL drivers to physical hardware pins. Validation checks BSW dependency ordering, MCAL binding completeness, and ECUC parameter ranges.

---

## Workflow Steps

1. User opens the ECU & BSW Designer (tab C3).
2. Designer loads CanIf channel definitions from `signals-comstack.yaml` (C2 output).
3. User selects active BSW modules from the module stack (ComStack, MCAL, OS, NvM, etc.).
4. User configures ECUC parameters for each module (timeouts, buffer sizes, error handling).
5. User binds MCAL drivers to physical pins (e.g., CAN controller → CAN1 transceiver).
6. User configures GPIO/Dio channel assignments.
7. WASM validates BSW dependency graph, ECUC parameter ranges, MCAL pin conflicts.
8. User reviews Board View and BSW Module Stack view.
9. YAML confirmed in sync; ECU/BSW config ready for OS Scheduling (C4) and NvM (C5).

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE Canvas (C3)
    participant C2YAML as signals-comstack.yaml
    participant BswYAML as ecu-bsw.yaml
    participant WASM as WASM Bridge
    participant Val as Validation Pane
    participant Props as Properties Panel

    User->>IDE: Open ECU & BSW Designer (C3)
    IDE->>C2YAML: Load CanIf channel definitions (CAN1, CAN2...)
    C2YAML-->>IDE: Render board with CAN bus slots

    User->>IDE: Click Board View → select CAN controller slot
    User->>Props: Bind CanController → CAN1 transceiver, baudrate = 500kbps
    Props->>BswYAML: Append can_controller entry {channel: CAN1, baudrate: 500}
    BswYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ CAN controller binding valid

    User->>IDE: Switch to BSW Module Stack View
    IDE-->>User: Show module stack: OS, Com, PduR, CanIf, CanDrv, Dio, Adc...

    User->>IDE: Enable "Com" module
    Props->>BswYAML: Append bsw_module {name: Com, enabled: true}
    BswYAML-->>WASM: Revalidate dependency graph
    WASM-->>Val: ✓ Com requires PduR — PduR already enabled

    User->>IDE: Enable "CanSM" (CAN State Manager)
    Props->>BswYAML: Append CanSM module
    BswYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ CanSM → CanIf dependency satisfied

    User->>Props: Configure Com module: PDU buffer size = 256, retry_count = 3
    Props->>BswYAML: Update bsw_module.ecuc_params
    BswYAML-->>WASM: Revalidate ECUC param ranges
    WASM-->>Val: ✓ ECUC parameters in valid range

    User->>IDE: Switch to Pin Configuration View
    User->>Props: Assign Dio channel "LED_OUT" → Port A, Pin 1, direction = OUTPUT
    Props->>BswYAML: Append dio_channel entry
    BswYAML-->>WASM: Revalidate pin assignments
    WASM-->>Val: ✓ Dio channel assigned

    User->>Props: Assign Adc channel "BatteryVoltage" → ADC0, resolution = 12bit
    Props->>BswYAML: Append adc_channel entry
    BswYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ ADC binding valid

    alt BSW dependency missing
        WASM-->>Val: ✗ CanIf enabled but CanDrv not active
        User->>IDE: Enable CanDrv in BSW stack
        Props->>BswYAML: Append CanDrv module
        WASM-->>Val: ✓ BSW dependency chain satisfied
    end

    alt ECUC param out of range
        WASM-->>Val: ✗ Com PDU buffer size 4096 exceeds maximum 512
        User->>Props: Set buffer_size = 256
        Props->>BswYAML: Update param value
        WASM-->>Val: ✓ ECUC parameter valid
    end

    alt Pin conflict
        WASM-->>Val: ✗ Pin PA1 already assigned to Dio "LED_OUT" — cannot assign to Pwm
        User->>Props: Move Pwm channel to PA2
        Props->>BswYAML: Update pin assignment
        WASM-->>Val: ✓ No pin conflicts
    end

    User->>IDE: Confirm YAML in sync (● In Sync indicator)
    IDE-->>User: C3 complete — proceed to OS & Scheduling (C4)
```

---

## Key Entities Involved

| Entity | Type | YAML Path |
|---|---|---|
| `Com` | BSW Module | `bsw_modules[0]` |
| `PduR` | BSW Module | `bsw_modules[1]` |
| `CanIf` | BSW Module | `bsw_modules[2]` |
| `CanDrv` | BSW Module (MCAL) | `bsw_modules[3]` |
| `LED_OUT` | Dio Channel | `dio_channels[0]` |
| `BatteryVoltage` | ADC Channel | `adc_channels[0]` |
| CAN controller binding | MCAL | `can_controllers[0]` |

---

## Validation Rules (WASM — `classic::validation`)

- Every enabled BSW module's upstream dependencies must also be enabled.
- Com requires PduR; CanIf requires CanDrv; CanSM requires CanIf.
- ECUC parameters must be within module-specified valid ranges.
- No two MCAL channels may share the same physical pin.
- CanIf channel names must match exactly the CanIf channels defined in `signals-comstack.yaml`.
- Dio direction must be one of: `INPUT`, `OUTPUT`, `INPUT_OUTPUT`.

---

## Outputs

- `ecu-bsw.yaml` — BSW module stack, ECUC parameters, MCAL pin assignments.
- Validated ECU/BSW config ready for task scheduling in **C4 OS & Scheduling** and NvM layout in **C5 Memory & NvM**.
