# classic-cluster-04-workflow — OS & Scheduling Designer

## Designer: C4 — OS & Scheduling Designer
**YAML file:** `os-scheduling.yaml`

## Overview

This workflow covers defining AUTOSAR OS tasks, ISRs, alarms, events, and OS applications in the OS & Scheduling Designer. The Timeline view shows task periods graphically. Users assign runnables (from C1) to tasks here — this is where the "runnable not mapped" warnings from C1 are resolved. Validation checks CPU budget, runnable coverage, alarm consistency, and OS application partitioning.

---

## Workflow Steps

1. User opens the OS & Scheduling Designer (tab C4).
2. Designer loads runnables from `swc-design.yaml` (C1) — shows unmapped runnables as pending.
3. User creates OS tasks (periodic, event-triggered, background).
4. User sets task period, priority, and stack size.
5. User assigns runnables to tasks (resolving C1 warnings).
6. User creates alarms and links them to tasks.
7. User creates OS ISRs for interrupt-driven execution.
8. WASM validates: all runnables mapped, CPU budget feasible, alarm periods consistent.
9. User reviews Timeline view for scheduling conflicts.
10. User reviews CPU Load view for budget analysis.
11. YAML confirmed in sync; OS config ready for RTE Mapping (C6).

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE Canvas (C4)
    participant C1YAML as swc-design.yaml
    participant OsYAML as os-scheduling.yaml
    participant WASM as WASM Bridge
    participant Val as Validation Pane
    participant Props as Properties Panel

    User->>IDE: Open OS & Scheduling Designer (C4)
    IDE->>C1YAML: Load all runnables (ReadSpeed_10ms, ComputeBrake_10ms...)
    C1YAML-->>IDE: Show unmapped runnables as pending items in left panel

    User->>Props: Create Task: name="Task_10ms", period_ms=10, priority=5, stack_bytes=2048
    Props->>OsYAML: Append task entry
    OsYAML-->>WASM: Revalidate
    WASM-->>Val: ⚠ Task_10ms has no runnables assigned

    User->>IDE: Drag ReadSpeed_10ms → Task_10ms
    IDE->>OsYAML: Append task.runnables = [ReadSpeed_10ms]
    OsYAML-->>WASM: Revalidate (cross-file: swc-design.yaml)
    WASM-->>Val: ✓ Runnable ReadSpeed_10ms mapped to Task_10ms

    User->>IDE: Drag ComputeBrake_10ms → Task_10ms
    IDE->>OsYAML: Update task.runnables = [ReadSpeed_10ms, ComputeBrake_10ms]
    OsYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ All runnables for 10ms period mapped

    User->>Props: Create Task: name="Task_100ms", period_ms=100, priority=3
    Props->>OsYAML: Append task entry
    User->>IDE: Drag DiagnosticRunnable → Task_100ms
    IDE->>OsYAML: Update task.runnables
    WASM-->>Val: ✓ Task_100ms runnable mapping valid

    User->>Props: Create Alarm: name="Alarm_10ms", task_ref="Task_10ms", period_ms=10
    Props->>OsYAML: Append alarm entry
    OsYAML-->>WASM: Revalidate alarm timing
    WASM-->>Val: ✓ Alarm period matches task period

    User->>Props: Create ISR: name="CanRxISR", category=CAT2, priority=10
    Props->>OsYAML: Append isr entry
    OsYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ ISR priority within valid range

    User->>IDE: Switch to Timeline View (⏱ Timeline)
    IDE-->>User: Gantt showing Task_10ms (10ms period), Task_100ms (100ms period), CanRxISR

    alt Runnable not mapped (from C1 warning)
        WASM-->>Val: ⚠ Runnable "InitRunnable" not mapped to any task
        User->>Props: Create Task_Init with trigger=InitEvent, assign InitRunnable
        OsYAML-->>WASM: Revalidate
        WASM-->>Val: ✓ All runnables mapped to OS tasks
    end

    alt CPU budget exceeded
        WASM-->>Val: ⚠ Task_10ms estimated CPU load 92% — exceeds 80% budget threshold
        User->>IDE: Move DiagRunnable to Task_100ms
        IDE->>OsYAML: Update task runnable assignments
        WASM-->>Val: ✓ Task_10ms CPU load 65% — within budget
    end

    User->>IDE: Switch to CPU Load View
    IDE-->>User: CPU bars: Task_10ms 65%, Task_100ms 20%, ISR budget 5%

    alt Priority inversion risk
        WASM-->>Val: ⚠ Task_10ms (priority 5) may be blocked by Task_100ms (priority 3) — check resource locking
        User->>Props: Adjust priorities: Task_10ms → 8, Task_100ms → 3
        WASM-->>Val: ✓ Priority ordering correct
    end

    User->>IDE: Confirm YAML in sync (● In Sync indicator)
    IDE-->>User: C4 complete — proceed to Memory & NvM (C5)
```

---

## Key Entities Involved

| Entity | Type | YAML Path |
|---|---|---|
| `Task_10ms` | OS Task | `tasks[0]` |
| `Task_100ms` | OS Task | `tasks[1]` |
| `ReadSpeed_10ms` | Runnable ref | `tasks[0].runnables[0]` |
| `Alarm_10ms` | OS Alarm | `alarms[0]` |
| `CanRxISR` | ISR | `isrs[0]` |
| `Task_Init` | OS Task | `tasks[2]` |

---

## Validation Rules (WASM — `classic::validation`)

- Every runnable declared in `swc-design.yaml` must be assigned to exactly one OS task.
- Task priority must be unique across all tasks (no two tasks at the same priority level).
- ISR category must be `CAT1` or `CAT2`; CAT1 ISRs may not call OS services.
- Alarm `task_ref` must reference a valid defined task.
- Alarm period must equal or be a multiple of the referenced task's period.
- Estimated CPU load per task period must not exceed configurable budget threshold (default 80%).

---

## Outputs

- `os-scheduling.yaml` — all tasks, ISRs, alarms, events, and runnable assignments.
- All C1 "runnable not mapped" warnings resolved.
- Validated OS config ready for RTE wiring in **C6 RTE & Mapping**.
