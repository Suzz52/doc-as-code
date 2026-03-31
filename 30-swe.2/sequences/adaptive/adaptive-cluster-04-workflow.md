# adaptive-cluster-04-workflow — Platform Services Designer

## Designer: A4 — Platform Services Designer
**YAML file:** `platform-services.yaml`

## Overview

This workflow covers configuring Adaptive AUTOSAR platform services per machine — including logging (DLT), time synchronisation (StbM), persistency (KVS), update manager, and credential manager. The designer presents a services overview canvas and per-service configuration forms. All platform service bindings are per-machine and validated against the machine topology defined in A3.

---

## Workflow Steps

1. User opens the Platform Services Designer (tab A4).
2. Designer loads machine inventory from `machine-design.yaml` (A3 output).
3. User enables or configures platform services for each machine.
4. User sets logging level, log sinks, and DLT daemon config.
5. User sets time sync protocol and accuracy requirements.
6. User configures persistency KVS paths and credential manager settings.
7. WASM validates per-machine service configs (required fields, compatible protocols).
8. User reviews Services Overview to confirm all machines have required platform services.
9. YAML confirmed in sync; platform services ready for Execution Designer (A5).

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE Canvas (A4)
    participant A3YAML as machine-design.yaml
    participant PlatYAML as platform-services.yaml
    participant WASM as WASM Bridge
    participant Val as Validation Pane
    participant Props as Properties Panel

    User->>IDE: Open Platform Services Designer (A4)
    IDE->>A3YAML: Load machine inventory
    A3YAML-->>IDE: Render ComputeECU, SensorECU, CameraECU in Services Overview

    User->>IDE: Select ComputeECU → enable Logging (DLT)
    IDE->>PlatYAML: Append logging entry for ComputeECU
    PlatYAML-->>WASM: Revalidate
    WASM-->>Val: ⚠ Logging enabled but log_level not set

    User->>Props: Set log_level = "Info", sink = "dlt-daemon"
    Props->>PlatYAML: Update logging.log_level, logging.sink
    PlatYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ Logging configuration valid

    User->>IDE: Select ComputeECU → enable Time Sync (StbM)
    IDE->>PlatYAML: Append time_sync entry
    User->>Props: Set protocol = "IEEE-802.1AS", sync_interval_ms = 250
    Props->>PlatYAML: Update time_sync config
    PlatYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ Time sync configuration valid

    User->>IDE: Select ComputeECU → enable Persistency (KVS)
    User->>Props: Set key_value_store_path = "/var/qorix/kvs"
    Props->>PlatYAML: Update persistency config
    PlatYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ KVS path valid

    User->>IDE: Select ComputeECU → enable Credential Manager
    User->>Props: Set enabled = true, key_store = "/etc/qorix/certs"
    Props->>PlatYAML: Update credential_manager config
    PlatYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ Credential manager configured

    User->>IDE: Select SensorECU → enable Logging only
    Props->>PlatYAML: Append minimal logging config for SensorECU
    PlatYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ SensorECU platform services valid

    User->>IDE: Switch to Configuration view (⚙ Configuration)
    IDE-->>User: Config form: DLT, StbM, KVS, CredMgr — per machine

    alt Missing required platform service
        WASM-->>Val: ⚠ CameraECU has no time_sync configured — required for SOME/IP
        User->>IDE: Enable time sync for CameraECU
        Props->>PlatYAML: Append time_sync entry for CameraECU
        WASM-->>Val: ✓ All machines have required platform services
    end

    User->>IDE: Switch to Services Overview (⚡ Services Overview)
    IDE-->>User: All 3 machines — logging ✓, time_sync ✓, persistency ✓

    User->>IDE: Confirm YAML in sync (● In Sync indicator)
    IDE-->>User: A4 complete — proceed to Execution Designer (A5)
```

---

## Key Entities Involved

| Entity | Type | YAML Path |
|---|---|---|
| Logging (DLT) | Platform Service | `machines[*].logging` |
| Time Sync (StbM/IEEE-802.1AS) | Platform Service | `machines[*].time_sync` |
| Persistency (KVS) | Platform Service | `machines[*].persistency` |
| Credential Manager | Platform Service | `machines[*].credential_manager` |
| Update Manager | Platform Service | `machines[*].update_manager` |
| Firewall | Platform Service | `machines[*].firewall` |

---

## Validation Rules (WASM — `adaptive::validation`)

- Logging requires `log_level` (one of: Off, Fatal, Error, Warn, Info, Debug, Verbose) and at least one `sink`.
- Time sync `protocol` must be one of: `IEEE-802.1AS`, `NTP`, `CUSTOM`.
- KVS `key_value_store_path` must be a valid absolute filesystem path.
- Machines with SOME/IP bindings (from A2) must have time sync enabled.
- Firewall `allowed_endpoints` and `denied_endpoints` must not overlap.

---

## Outputs

- `platform-services.yaml` — per-machine platform service configuration.
- Validated platform service inventory ready for **A5 Execution Designer**.
