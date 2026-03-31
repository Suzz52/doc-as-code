# adaptive-cluster-07-workflow — AI-Assist Workflow (Adaptive)

## Designer: All Adaptive Designers (A1–A6) — AI-Assist Integration
**Context:** Cross-canvas AI-assisted configuration fixes and proposals

## Overview

This workflow covers the AI-Assist integration pattern across all six Adaptive AUTOSAR designers. The user invokes the AI chat panel from any designer, the MCP agent classifies the intent, calls the Rust Domain Service for a structured `OperationPlan`, and presents a diff for user review and approval. AI never writes YAML directly — all mutations go through Rust ops and are re-validated by WASM after apply.

---

## Workflow Steps

1. User encounters a validation error or wants to accelerate a configuration task.
2. User opens the AI chat bar and types a natural language intent.
3. MCP agent sends prompt + current YAML context + diagnostics to LLM Backend.
4. LLM classifies the intent (stack, intentType).
5. MCP agent calls `POST /planOps` on Rust Domain Service.
6. Rust computes a structured `OperationPlan` (never guessed by LLM).
7. MCP returns `OperationPlan` + LLM explanation to IDE.
8. IDE shows diff preview to user.
9. User approves or rejects.
10. On approval: WASM re-validates the updated YAML; if clean, changes are written.

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
    participant YAML as YAML Files (all 6)

    Note over User,YAML: Example: "Fix missing service bindings in the communication layer"

    User->>IDE: Type in AI bar: "Fix missing service bindings"
    IDE->>MCP: prompt + context(stack=adaptive, projectId, yamlSnippets, diagnostics)

    MCP->>LLM: Send prompt + context
    LLM-->>MCP: intent {stack: adaptive, intentType: fix-missing-service-bindings}

    MCP->>Rust: POST /planOps {stack:adaptive, intentType:fix-missing-service-bindings, yamlDocuments}
    Rust-->>MCP: OperationPlan {ops: [{kind:add, file:communication-design.yaml, path:bindings, value:{...}}], summary:"Added 2 missing bindings", warnings:[]}

    MCP-->>IDE: OperationPlan + explanation ("I found 2 unbound consumers in FusionService...")
    IDE-->>User: Show diff: +2 binding entries in communication-design.yaml

    alt User approves
        User->>IDE: Click "Apply changes"
        IDE->>WASM: validateYaml(adaptive, updatedYamlDocs)
        WASM-->>IDE: Diagnostic[] — 0 errors
        IDE->>Rust: POST /applyOpsAndSync {planId, syncArxml: false}
        Rust-->>IDE: updatedYamlDocuments
        IDE->>YAML: Write updated communication-design.yaml
        IDE-->>User: ✓ Changes applied — canvas and YAML in sync
    else User rejects
        User->>IDE: Click "Dismiss"
        IDE-->>User: Diff discarded — no changes written
    end

    Note over User,YAML: Example 2: "Map RadarApp and FusionApp to optimal machines"

    User->>IDE: Type: "Suggest optimal machine mapping for radar and fusion apps"
    IDE->>MCP: prompt + context(all 6 YAML files, machine resources from A3)
    MCP->>LLM: Classify → {stack:adaptive, intentType:suggest-execution-mapping}
    MCP->>Rust: POST /planOps {intentType:suggest-execution-mapping}
    Rust-->>MCP: OperationPlan {ops: [{update deployment.machine for FusionApp → ComputeECU},...], summary:"Mapped 3 apps based on RAM fit and core affinity"}
    MCP-->>IDE: Diff: deployment-manifest.yaml + explanation
    User->>IDE: Approve
    IDE->>WASM: Re-validate (adaptive, all docs)
    WASM-->>IDE: ✓ Clean
    IDE->>Rust: Apply ops
    Rust-->>IDE: Updated deployment-manifest.yaml

    Note over User,YAML: Example 3: "Resolve machine resource issues on ComputeECU"

    User->>IDE: Type: "Resolve resource overcommit on ComputeECU"
    MCP->>Rust: POST /planOps {intentType:resolve-machine-resource-issues}
    Rust-->>MCP: OperationPlan {ops: [{move CameraApp to CameraECU}], warnings:["CameraECU CPU budget now 75%"]}
    MCP-->>IDE: Diff + explanation
    User->>IDE: Approve
    IDE->>WASM: Re-validate
    WASM-->>IDE: ✓ All resource constraints satisfied
    IDE->>Rust: Apply
    Rust-->>IDE: Updated deployment-manifest.yaml
```

---

## AI Intent → Tool Mapping (Adaptive Stack)

| User Intent (natural language) | Classified `intentType` | Rust Tool |
|---|---|---|
| "Fix missing service bindings" | `fix-missing-service-bindings` | `fix_missing_service_bindings` |
| "Map apps to optimal machines" | `suggest-execution-mapping` | `suggest_execution_mapping` |
| "Resolve resource overcommit" | `resolve-machine-resource-issues` | `resolve_machine_resource_issues` |
| "Suggest SOME/IP bindings" | `suggest-service-bindings` | `suggest_service_bindings` |
| "Validate the whole project" | `validate_project` | `validate_project` |
| "Summarize issues" | `summarize_diagnostics` | `summarize_diagnostics` |

---

## Safety Invariants

- LLM never writes YAML or calls the ARXML Gateway directly.
- Every proposed change is expressed as a `core::ops` `OperationPlan` from Rust.
- WASM re-validates all affected YAML documents before changes are written.
- User must explicitly approve every AI-proposed diff.
- Plan is discarded without trace if user rejects.

---

## Outputs

- Updated YAML files in affected designers, all validated clean.
- Structured `OperationPlan` audit trail for every AI-applied change.
