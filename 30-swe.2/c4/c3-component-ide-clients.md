# C3 – Components: IDE Clients (VS Code Extension + Theia)

## Overview

The IDE client layer (VS Code Extension and Theia IDE) provides all user-facing interaction surfaces: YAML editing, graphical designers, diagnostics, AI chat, and migration wizard. Both IDEs share identical internal component contracts — they differ only in their host shell (VS Code vs Theia/browser). The component architecture follows a clear two-path model: **fast & local via WASM** for instant feedback, **heavy & persistent via Rust Domain Service** for cross-cutting operations.

---

## Mermaid Diagram

```mermaid
C4Component
    title Component Diagram – IDE Clients (VS Code Extension / Theia)

    Container_Ext(rustWasm, "Rust WASM Module", "Rust → WASM npm pkg", "In-process validation and planOps. Returns diagnostics and operation plans without network calls.")
    Container_Ext(rustSvc, "Rust Domain Service", "Rust / Axum", "Heavy operations: cross-file validation, generate-arxml, apply ops. Exposes HTTP/gRPC endpoints.")
    Container_Ext(mcpAgent, "Developer Agent (MCP)", "TypeScript / Node", "AI orchestration. Receives user chat messages + YAML context, returns OperationPlan and explanations.")

    System_Boundary(ide, "IDE Client (VS Code Extension / Theia)") {

        Component(yamlEditors, "YAML Editors", "TypeScript / VS Code Language Client", "One editor per YAML file (Classic and Adaptive). Provides syntax highlighting, JSON Schema-based structural validation, code completion, and go-to-definition. On every keystroke, sends current doc to WASM Bridge for fast diagnostics.")

        Component(classicDesigners, "Classic Designers", "TypeScript / React canvas", "Visual canvases bound to Classic YAML files:\n- SWC Designer (swc-design.yaml)\n- Signals & ComStack Designer (signals-comstack.yaml)\n- ECU/BSW Designer (ecu-bsw.yaml)\n- OS Designer (os-config.yaml)\n- NvM Designer (nvm-config.yaml)\n- RTE Designer (rte-mapping.yaml)\nDesigners do not manage models directly — they edit YAML via Command Bus ops.")

        Component(adaptiveDesigners, "Adaptive Designers", "TypeScript / React canvas", "Visual canvases bound to Adaptive YAML files:\n- Application & Service Designer (application-design.yaml)\n- Communication Designer (communication-design.yaml)\n- Machine Designer (machine-design.yaml)\n- Platform Services Designer (platform-services.yaml)\n- Execution Designer (execution-manifest.yaml)\n- Deployment Designer (deployment-manifest.yaml)\nDesigners emit ops to Command Bus; YAML is the source of truth.")

        Component(wasmBridge, "WASM Bridge", "TypeScript wrapper (wasm-bindgen)", "JS/TS facade over the Rust WASM module. Provides JS-friendly async APIs:\n- validateYaml(stack, yamlDocs) → Diagnostic[]\n- planOps(stack, yamlDocs, intent) → OperationPlan\nRoutes calls in-process; no HTTP overhead.")

        Component(commandBus, "Command Bus", "TypeScript event bus", "Abstraction layer for complex operations triggered by designers or keyboard shortcuts. Translates UI actions into typed ops:\n- execute('classic.addSwc', payload)\n- execute('adaptive.addServiceInstance', payload)\nOps are passed to Domain Service Client for Rust processing.")

        Component(domainSvcClient, "Domain Service Client", "TypeScript HTTP/gRPC client", "Thin client to Rust Domain Service. Sends structured requests for heavy operations:\n- POST /validate (cross-file, cross-canvas)\n- POST /planOps (large migration, complex AI plans)\n- POST /applyOpsAndSync (apply ops → sync ARXML)\nReceives new YAML + diagnostics in response.")

        Component(diagnosticsPanel, "Diagnostics Panel", "TypeScript / VS Code Problems API", "Aggregates and displays validation messages from two sources:\n- WASM (fast, local, per-keystroke)\n- Rust Domain Service (deep, cross-cutting, on demand)\nShows severity (error/warning/info), code, message, and precise YAML path link.")

        Component(aiChatPanel, "AI Chat Panel", "TypeScript / MCP client", "MCP client in the IDE:\n- Accepts user natural language input.\n- Gathers context: YAML fragments, current diagnostics, active designer state.\n- Sends context + prompt to Developer Agent (MCP).\n- Receives OperationPlan and explanation; presents diff for user review before apply.")

        Component(migrationWizard, "Migration Wizard", "TypeScript / React multi-step UI", "Step-by-step ARXML import and migration UI:\n1. Load single or multi-file ARXML project.\n2. Runs autorepair & normalization (infer runnable timing, normalize signals).\n3. Presents migration diagnostics with AI-assisted fix proposals.\n4. Applies accepted fixes via Command Bus → Domain Service Client.")
    }

    %% YAML Editor → WASM (fast path)
    Rel(yamlEditors, wasmBridge, "Send YAML on every edit for instant diagnostics", "In-process call")
    Rel(wasmBridge, rustWasm, "validateYaml(stack, yamlDocs)", "WASM API")
    Rel(wasmBridge, diagnosticsPanel, "Stream Diagnostic[] results", "TypeScript callback")

    %% Designers → Command Bus → Domain Service
    Rel(classicDesigners, commandBus, "Emit typed ops on user action", "TypeScript event")
    Rel(adaptiveDesigners, commandBus, "Emit typed ops on user action", "TypeScript event")
    Rel(commandBus, domainSvcClient, "Forward ops for Rust processing", "TypeScript call")
    Rel(domainSvcClient, rustSvc, "POST /validate, /planOps, /applyOpsAndSync", "HTTP/gRPC")
    Rel(domainSvcClient, diagnosticsPanel, "Update with deep validation results", "TypeScript callback")

    %% AI Chat → MCP Agent
    Rel(aiChatPanel, mcpAgent, "User prompt + YAML context + diagnostics", "MCP Protocol")
    Rel(aiChatPanel, wasmBridge, "Pre-validate AI-proposed ops before show", "In-process call")
    Rel(aiChatPanel, commandBus, "Apply accepted OperationPlan ops", "TypeScript event")

    %% Migration Wizard
    Rel(migrationWizard, domainSvcClient, "Trigger importArxml, migration pipeline", "HTTP/gRPC")
    Rel(migrationWizard, aiChatPanel, "Surface AI-assisted fix proposals", "TypeScript call")
    Rel(migrationWizard, commandBus, "Apply accepted migration fixes", "TypeScript event")

    %% Editors update on designer changes and vice versa (bidirectional sync)
    Rel(classicDesigners, yamlEditors, "YAML text update (bidirectional binding)", "TypeScript event")
    Rel(adaptiveDesigners, yamlEditors, "YAML text update (bidirectional binding)", "TypeScript event")
    Rel(yamlEditors, classicDesigners, "Canvas refresh on YAML change", "TypeScript event")
    Rel(yamlEditors, adaptiveDesigners, "Canvas refresh on YAML change", "TypeScript event")
```

---

## Component Descriptions

### YAML Editors
- One editor instance per YAML file per stack (Classic: 6 files; Adaptive: 6 files).
- JSON Schema–backed for structural completion and validation (field names, enums, required keys).
- Bidirectional binding with graphical designers: a YAML text edit immediately refreshes the canvas; a canvas drag-drop immediately updates the YAML text.
- Every keystroke sends the current document set to the WASM Bridge for fast diagnostics.

### Classic Designers (6 canvases)
Visual canvases for AUTOSAR Classic configuration:

| Designer | YAML File | Domain |
|---|---|---|
| SWC Designer | `swc-design.yaml` | SWCs, ports, interfaces, runnables |
| Signals & ComStack | `signals-comstack.yaml` | Signals, I-PDUs, PDUs, COM/PduR/CanIf routing |
| ECU / BSW Designer | `ecu-bsw.yaml` | ECUC, BSW modules, MCAL bindings |
| OS Designer | `os-config.yaml` | Tasks, ISRs, alarms, OS events |
| NvM Designer | `nvm-config.yaml` | NvM blocks, memory layout, device assignments |
| RTE Designer | `rte-mapping.yaml` | Runnable-to-task mappings, port connections |

### Adaptive Designers (6 canvases)
Visual canvases for AUTOSAR Adaptive configuration:

| Designer | YAML File | Domain |
|---|---|---|
| Application & Service | `application-design.yaml` | Executables, service interfaces, ports |
| Communication | `communication-design.yaml` | SOME/IP, service discovery, network bindings |
| Machine Designer | `machine-design.yaml` | Machine manifest, hardware resources, OS config |
| Platform Services | `platform-services.yaml` | Logging, time sync, persistency, update manager |
| Execution | `execution-manifest.yaml` | Process definitions, functional groups, startup config |
| Deployment | `deployment-manifest.yaml` | Application-to-machine bindings, service deployment |

### WASM Bridge
- Thin TypeScript/JS wrapper generated by `wasm-bindgen`.
- Provides async-friendly APIs over synchronous WASM calls.
- Runs in-process — zero network overhead, sub-millisecond round-trips.
- Supports both Classic and Adaptive stacks via the `stack` parameter.

### Command Bus
- Central event bus decoupling designers from the domain service client.
- All designer user actions are expressed as typed operation payloads.
- Enables undo/redo, operation logging, and AI plan preview before apply.

### Domain Service Client
- Thin HTTP/gRPC client; no business logic.
- Manages retry, timeout, and error surfacing to the diagnostics panel.
- Handles both the "apply ops" write path and the "validate only" read path.

### Diagnostics Panel
- Merges WASM (fast) and Rust Service (deep) diagnostics into one unified view.
- Maps YAML path references to clickable editor locations.
- Severity: `error` (🔴), `warning` (🟡), `info` (🔵).

### AI Chat Panel
- MCP client: sends a structured context packet (prompt + YAML fragments + diagnostics) to the Developer Agent.
- Receives back an `OperationPlan` (structured diff) and a human-readable explanation.
- Shows the proposed diff for user review; only applies when the user confirms.
- Can optionally pre-validate proposed ops via WASM before presenting.

### Migration Wizard
- Multi-step UI for onboarding existing ARXML projects.
- Step 1: File selection (single or multi-file ARXML).
- Step 2: Autorepair & normalization (infer runnable timing, normalize signals, deduplicate).
- Step 3: Migration diagnostics with AI-assisted fix proposals.
- Step 4: Apply accepted fixes via Command Bus.

---

## Two-Path Architecture

```
Fast & Local (WASM path)
  User edits YAML
  → YAML Editor sends doc to WASM Bridge
  → wasmBridge.validateYaml(stack, docs)
  → Diagnostics Panel updated instantly (no network)

Heavy & Persistent (Rust Service path)
  User triggers generate-arxml / large migration / cross-file validation
  → Designer → Command Bus → Domain Service Client
  → POST /applyOpsAndSync on Rust Domain Service
  → Rust calls ARXML Gateway if ARXML output needed
  → New YAML + diagnostics returned to IDE
```

---

## Key Design Principles

- **Designers never own the model.** They emit YAML ops via the Command Bus; the Rust domain is always the model authority.
- **Bidirectional binding is lossless.** A YAML edit and a canvas drag-drop are equivalent; neither is "more real" than the other.
- **AI is always presented as a diff.** The AI Chat Panel never applies changes silently; every AI-proposed OperationPlan goes through user review.
- **WASM replaces file-save validation.** Feedback is continuous and in-process, not deferred to a build step.
- **Classic and Adaptive share the same IDE shell.** All designers, editors, command bus, and WASM bridge are stack-parameterised; no duplicate implementations.
