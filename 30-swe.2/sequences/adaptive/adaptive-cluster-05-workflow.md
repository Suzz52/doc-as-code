# adaptive-cluster-05-workflow — Execution Designer

## Designer: A5 — Execution Designer
**YAML file:** `execution-manifest.yaml`

## Overview

This workflow covers defining processes, threads, and their scheduling parameters for each application. The Execution Designer maps application executables to processes, configures thread periods, timeslices, and core affinity. It cross-references machine hardware from A3 to validate scheduling feasibility. All execution config is persisted to `execution-manifest.yaml`.

---

## Workflow Steps

1. User opens the Execution Designer (tab A5).
2. Designer loads applications from `application-design.yaml` (A1) and machine topology from `machine-design.yaml` (A3).
3. User creates process entries for each application.
4. User adds thread entries to each process and sets period_ms, timeslice_ms.
5. User assigns core affinity per thread.
6. WASM validates scheduling feasibility (threads fit in timeslice, cores exist on target machine).
7. User reviews the Timeline view to spot scheduling conflicts.
8. User reviews the Core Affinity view to check load distribution.
9. YAML confirmed in sync; execution manifest ready for Deployment Designer (A6).

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE Canvas (A5)
    participant A1YAML as application-design.yaml
    participant A3YAML as machine-design.yaml
    participant ExecYAML as execution-manifest.yaml
    participant WASM as WASM Bridge
    participant Val as Validation Pane
    participant Props as Properties Panel

    User->>IDE: Open Execution Designer (A5)
    IDE->>A1YAML: Load application list (FusionApp, RadarApp, CameraApp)
    IDE->>A3YAML: Load machine core inventory (ComputeECU: 4 cores, SensorECU: 2 cores)
    IDE-->>User: Timeline canvas and application list

    User->>IDE: Select FusionApp → Add Process
    IDE->>ExecYAML: Append process entry {application: FusionApp, name: FusionProcess}
    ExecYAML-->>WASM: Revalidate
    WASM-->>Val: ⚠ Process has no threads

    User->>Props: Add thread "FusionThread_10ms", period_ms = 10, timeslice_ms = 3
    Props->>ExecYAML: Append thread entry
    ExecYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ Thread scheduling parameters valid

    User->>Props: Set core_affinity = [0, 1]
    Props->>ExecYAML: Update thread.core_affinity
    ExecYAML-->>WASM: Revalidate against A3 machine cores
    WASM-->>Val: ✓ Core affinity within machine core count

    User->>IDE: Select RadarApp → Add Process
    IDE->>ExecYAML: Append process {application: RadarApp, name: RadarProcess}
    User->>Props: Add thread "RadarThread_5ms", period_ms = 5, timeslice_ms = 1, core_affinity = [0]
    Props->>ExecYAML: Append thread
    WASM-->>Val: ✓ RadarThread scheduling valid

    User->>IDE: Select CameraApp → Add Process → Add Thread
    User->>Props: CameraThread_33ms, period_ms = 33, timeslice_ms = 10, core_affinity = [0, 1]
    Props->>ExecYAML: Append thread
    WASM-->>Val: ✓ CameraThread valid

    User->>IDE: Switch to Timeline View (⏱ Timeline)
    IDE-->>User: Gantt-style timeline showing FusionThread, RadarThread, CameraThread on cores

    alt Scheduling conflict detected
        WASM-->>Val: ⚠ Core 0 overloaded — FusionThread + RadarThread exceed core budget
        User->>Props: Move FusionThread to core_affinity = [1]
        Props->>ExecYAML: Update core_affinity
        WASM-->>Val: ✓ Core 0 load balanced
    end

    User->>IDE: Switch to Core Affinity View (🎯 Core Affinity)
    IDE-->>User: Core load bars: Core 0 @ 60%, Core 1 @ 55%, Core 2 @ 20%, Core 3 @ 10%

    alt Thread period not feasible on target machine
        WASM-->>Val: ✗ RadarThread period 5ms requires real-time OS — SensorECU does not support RT
        User->>IDE: Move RadarApp to ComputeECU (cross-canvas decision for A6)
    end

    User->>IDE: Confirm YAML in sync (● In Sync indicator)
    IDE-->>User: A5 complete — proceed to Deployment Designer (A6)
```

---

## Key Entities Involved

| Entity | Type | YAML Path |
|---|---|---|
| `FusionProcess` | Process | `processes[0]` |
| `RadarProcess` | Process | `processes[1]` |
| `CameraProcess` | Process | `processes[2]` |
| `FusionThread_10ms` | Thread | `processes[0].threads[0]` |
| Core affinity | Config | `processes[*].threads[*].core_affinity` |
| `restart` policy | Config | `processes[*].restart` |

---

## Validation Rules (WASM — `adaptive::validation`)

- Every application (from A1) must have exactly one process defined.
- Every process must have at least one thread.
- Thread `timeslice_ms` must be < `period_ms`.
- Thread `core_affinity` values must be within `[0, machine.cores - 1]` for the assigned machine (cross-canvas check with A6 deployment binding).
- `restart` policy must be one of: `none`, `on_failure`, `always`.

---

## Outputs

- `execution-manifest.yaml` — process and thread scheduling for all applications.
- Validated execution manifest ready for **A6 Deployment Designer**.
