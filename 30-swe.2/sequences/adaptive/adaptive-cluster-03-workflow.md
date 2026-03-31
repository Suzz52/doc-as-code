# adaptive-cluster-03-workflow — Machine Designer

## Designer: A3 — Machine Designer
**YAML file:** `machine-design.yaml`

## Overview

This workflow covers defining machine (ECU/HPC) hardware topology in the Machine Designer. Users model machines with their CPU cores, memory regions, and network interfaces. Validation cross-references the execution and deployment requirements from later designers to confirm hardware feasibility. All topology is persisted to `machine-design.yaml`.

---

## Workflow Steps

1. User opens the Machine Designer (tab A3).
2. User adds machine blocks (ECU/HPC nodes) to the topology canvas.
3. User configures each machine with CPU type, core count, and memory regions.
4. User adds network interface nodes and connects machines via network links.
5. WASM validates hardware resource specs (core count, RAM, storage).
6. User reviews the Resources view to check memory/CPU utilization forecasts.
7. User resolves any capacity constraint warnings.
8. YAML confirmed in sync; topology ready for Platform Services (A4) and Execution (A5).

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE Canvas (A3)
    participant Palette as Element Palette
    participant Props as Properties Panel
    participant MachYAML as machine-design.yaml
    participant WASM as WASM Bridge
    participant Val as Validation Pane

    User->>IDE: Open Machine Designer (A3)
    IDE->>MachYAML: Load existing machine topology
    MachYAML-->>IDE: Render existing machine nodes (or empty canvas)

    User->>Palette: Click "+ Machine"
    Palette->>IDE: Add machine block "ComputeECU" to canvas
    IDE->>MachYAML: Append machine entry {name: ComputeECU}
    MachYAML-->>WASM: Revalidate
    WASM-->>Val: ⚠ Machine has no CPU defined yet

    User->>Props: Set CPU = "ARM A78", cores = 4
    Props->>MachYAML: Update machine.cpu, machine.cores
    MachYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ CPU configuration valid

    User->>Props: Add memory region: RAM = 8192 MB
    Props->>MachYAML: Append machine.memory_regions[]
    MachYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ Memory region valid

    User->>Palette: Click "+ Machine"
    Palette->>IDE: Add machine block "SensorECU"
    User->>Props: Set CPU = "ARM A55", cores = 2, RAM = 4096 MB
    Props->>MachYAML: Append SensorECU definition
    MachYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ SensorECU valid

    User->>Palette: Click "+ Network Interface"
    Palette->>IDE: Add Ethernet interface node
    User->>Props: Set interface = "eth0", protocol = "SOME/IP", bandwidth = "1 Gbps"
    Props->>MachYAML: Append network_interfaces[]
    MachYAML-->>WASM: Revalidate

    User->>IDE: Draw network link: ComputeECU.eth0 ↔ SensorECU.eth0
    IDE->>MachYAML: Append network link entry
    MachYAML-->>WASM: Revalidate cross-machine reachability
    WASM-->>Val: ✓ Network topology connected

    User->>IDE: Switch to Table View (≡ Table)
    IDE-->>User: Table: ComputeECU (A78, 4 cores, 8 GB), SensorECU (A55, 2 cores, 4 GB)

    User->>IDE: Switch to Resources View (📊 Resources)
    IDE-->>User: CPU and RAM budget bars for each machine

    alt Resource overcommit warning
        WASM-->>Val: ⚠ ComputeECU RAM budget 97% — add memory or rebalance apps
        User->>Props: Increase RAM = 16384 MB
        Props->>MachYAML: Update memory_regions
        WASM-->>Val: ✓ Resource constraints satisfied
    end

    User->>IDE: Confirm YAML in sync (● In Sync indicator)
    IDE-->>User: A3 complete — proceed to Platform Services (A4)
```

---

## Key Entities Involved

| Entity | Type | YAML Path |
|---|---|---|
| `ComputeECU` | Machine | `machines[0]` |
| `SensorECU` | Machine | `machines[1]` |
| `CameraECU` | Machine | `machines[2]` |
| CPU config | Hardware | `machines[*].cpu` |
| Memory regions | Hardware | `machines[*].memory_regions[]` |
| Network interfaces | Hardware | `machines[*].network_interfaces[]` |
| Network links | Topology | `network_links[]` |

---

## Validation Rules (WASM — `adaptive::validation`)

- Every machine must have at least one CPU defined with a valid core count (≥ 1).
- Memory regions must have unique names and positive sizes.
- Network links must connect two valid machine interfaces; dangling endpoints are errors.
- SOME/IP-bound services (from A2) require machines to have at least one network interface.
- IPC-bound services require both endpoints to eventually be deployed on the same machine (checked cross-canvas at A6).

---

## Outputs

- `machine-design.yaml` — full hardware topology with CPU, memory, and network config.
- Validated machine inventory ready for **A4 Platform Services** and **A5 Execution Designer**.
