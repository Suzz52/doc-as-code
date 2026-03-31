# classic-cluster-07-workflow — AI-Assist Workflow (Classic)

## Designer: All Classic Designers (C1–C6) — AI-Assist Integration
**Context:** Cross-canvas AI-assisted configuration fixes and proposals for Classic AUTOSAR

## Overview

This workflow covers the AI-Assist integration pattern across all six Classic AUTOSAR designers. Users invoke the AI chat bar from any designer canvas. The MCP agent classifies the intent, routes to the appropriate Classic-specific Rust tool, and returns a structured `OperationPlan` for user review. AI never writes YAML directly — all mutations are Rust-computed ops, re-validated by WASM after apply.

---

## Workflow Steps

1. User encounters validation errors (unmapped runnables, ComStack gaps, NvM conflicts, etc.) or wants to accelerate configuration.
2. User opens the AI chat bar and types a natural language intent.
3. MCP agent assembles context (all 6 YAML files + current diagnostics).
4. LLM classifies intent → `intentType` + `stack: classic`.
5. MCP calls `POST /planOps` on Rust Domain Service.
6. Rust computes deterministic `OperationPlan`.
7. MCP returns diff + LLM explanation.
8. User reviews diff and approves or rejects.
9. On approval: WASM re-validates; if clean, YAML is updated.

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE (AI Chat Panel)
    participant MCP as Developer Agent (MCP)
    participant LLM as LLM Backend
    participant Rust as Rust Domain Service
    participant WASM as WASM Bridge
    participant YAML as YAML Files (all 6 Classic)

    Note over User,YAML: Example 1: Fix unmapped runnables (C1 → C4)

    User->>IDE: Type: "Fix all unmapped runnables"
    IDE->>MCP: prompt + context(stack=classic, all YAML, diagnostics)
    MCP->>LLM: Classify intent
    LLM-->>MCP: {stack: classic, intentType: fix-unmapped-runnables}

    MCP->>Rust: POST /planOps {stack:classic, intentType:fix-unmapped-runnables, yamlDocuments}
    Rust-->>MCP: OperationPlan {ops:[{add runnable ReadSpeed_10ms to Task_10ms}, {add ComputeBrake to Task_10ms}], summary:"Mapped 2 runnables to Task_10ms based on timing match", warnings:[]}

    MCP-->>IDE: Diff: os-scheduling.yaml +2 runnable entries + explanation
    IDE-->>User: Show diff preview

    User->>IDE: Approve
    IDE->>WASM: validateYaml(classic, updatedYamlDocs)
    WASM-->>IDE: ✓ 0 errors — all runnables mapped
    IDE->>Rust: POST /applyOpsAndSync
    Rust-->>IDE: Updated os-scheduling.yaml
    IDE-->>User: ✓ Applied — C1 warnings cleared

    Note over User,YAML: Example 2: Fix ComStack errors (C2)

    User->>IDE: Type: "Fix ComStack routing errors"
    MCP->>LLM: Classify
    LLM-->>MCP: {stack: classic, intentType: fix-comstack-errors}

    MCP->>Rust: POST /planOps {intentType:fix-comstack-errors}
    Rust-->>MCP: OperationPlan {ops:[{add PduR routing for VehicleSpeedIPdu → CAN1}, {fix signal bit_position overlap}], summary:"Added missing PduR route and corrected signal packing"}

    MCP-->>IDE: Diff: signals-comstack.yaml 2 changes
    User->>IDE: Approve
    IDE->>WASM: Re-validate
    WASM-->>IDE: ✓ Clean
    IDE->>Rust: Apply
    Rust-->>IDE: Updated signals-comstack.yaml

    Note over User,YAML: Example 3: Suggest NvM layout (C5)

    User->>IDE: Type: "Suggest optimal NvM block layout for my data sets"
    MCP->>LLM: Classify
    LLM-->>MCP: {stack: classic, intentType: suggest-nvm-layout}

    MCP->>Rust: POST /planOps {intentType:suggest-nvm-layout}
    Rust-->>MCP: OperationPlan {ops:[reorder blocks by access frequency, set CRC_16 on redundant blocks], summary:"Optimised block layout — 22% less fragmentation", warnings:["EEPROM_1 at 78% capacity"]}

    MCP-->>IDE: Diff: mem-nvram.yaml reordered + warning shown
    User->>IDE: Approve
    IDE->>WASM: Re-validate
    WASM-->>IDE: ✓ NvM layout valid
    IDE->>Rust: Apply

    Note over User,YAML: Example 4: Suggest runnable mappings (C6)

    User->>IDE: Type: "Suggest optimal runnable-to-task mappings"
    MCP->>LLM: Classify
    LLM-->>MCP: {stack: classic, intentType: suggest-runnable-mappings}

    MCP->>Rust: POST /planOps {intentType:suggest-runnable-mappings}
    Rust-->>MCP: OperationPlan {ops:[move DiagRunnable from Task_10ms to Task_100ms], summary:"Balances CPU load — Task_10ms drops from 92% to 65%"}

    MCP-->>IDE: Diff: rte-mapping.yaml + os-scheduling.yaml changes
    User->>IDE: Approve
    IDE->>WASM: Re-validate (classic, all 6 docs)
    WASM-->>IDE: ✓ Clean
    IDE->>Rust: Apply
    Rust-->>IDE: Updated YAML files
    IDE-->>User: ✓ Task_10ms CPU load 65%
```

---

## AI Intent → Tool Mapping (Classic Stack)

| User Intent (natural language) | Classified `intentType` | Rust Tool |
|---|---|---|
| "Fix unmapped runnables" | `fix-unmapped-runnables` | `fix_unmapped_runnables` |
| "Fix ComStack / PDU routing errors" | `fix-comstack-errors` | `fix_comstack_errors` |
| "Suggest runnable task assignments" | `suggest-runnable-mappings` | `suggest_runnable_mappings` |
| "Fix unbound signals" | `fix-unmapped-signals` | `fix_unmapped_signals` |
| "Suggest NvM block layout" | `suggest-nvm-layout` | `suggest_nvm_layout` |
| "Validate the whole project" | (shared) | `validate_project` |
| "Summarize all errors" | (shared) | `summarize_diagnostics` |

---

## AI-Assist Integration Points per Designer

| Designer | Primary AI-Assist capability |
|---|---|
| C1 SWC & Interface | Suggest port-interface type corrections |
| C2 Signals & ComStack | Fix signal-to-PDU packing, PduR routing gaps |
| C3 ECU & BSW | Resolve BSW dependency chain, MCAL pin conflicts |
| C4 OS & Scheduling | Map all unmapped runnables, balance CPU load |
| C5 Memory & NvM | Suggest NvM layout, fix capacity overcommit |
| C6 RTE & Mapping | Auto-wire RTE connections, suggest runnable mappings |

---

## Safety Invariants

- LLM never writes `swc-design.yaml`, `os-scheduling.yaml`, or any YAML file directly.
- All mutations are `core::ops` `OperationPlan` entries computed deterministically by Rust.
- WASM re-validates all 6 YAML files after every approved AI change.
- User must explicitly approve every diff; rejected diffs leave no state.
- Cross-canvas changes (e.g., runnable mapping touching both C1 and C4) are expressed as a single atomic `OperationPlan` applied together.

---

## Outputs

- Updated YAML files in affected designers, all validated clean.
- Structured `OperationPlan` audit trail for every AI-applied change.
