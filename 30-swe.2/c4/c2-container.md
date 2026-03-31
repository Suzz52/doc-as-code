# C2 – Containers: Qorix Developer

## Overview

Zooming into Qorix Developer, the platform is composed of four major container groups: **IDE Clients** (VS Code / Theia), the **Rust Domain Platform** (core + WASM + CLI + service), the **ARXML Gateway** (Spring Boot + ARTOP + GraphQL), and the **AI / MCP Layer** (Qorix Agent + LLM).

---

## Mermaid Diagram

```mermaid
C4Container
    title Container Diagram – Qorix Developer

    Person(configEng, "Configuration Engineer")
    Person(sysArch, "System Architect")
    Person(migEng, "Migration Engineer")
    Person(ciSystem, "CI / Build System")

    System_Ext(llm, "LLM Backend", "OpenAI or self-hosted model")
    System_Ext(legacyTools, "Legacy AUTOSAR Tools", "EB Tresos, Davinci, SystemDesk")
    System_Ext(buildToolchain, "Downstream Build Toolchain")
    System_Ext(gitRepo, "Git Repository", "YAML source of truth")

    System_Boundary(qorix, "Qorix Developer") {

        %% IDE Clients
        Container(vscode, "VS Code Extension", "TypeScript / React", "YAML editing with schema completion. Hosts Classic & Adaptive graphical designers. Integrates WASM bridge and MCP AI chat panel.")
        Container(theia, "Theia IDE", "TypeScript / React", "Desktop/web alternative IDE. Identical contracts and APIs as VS Code extension.")

        %% Rust Domain Platform
        Container(rustCore, "Rust Domain Core", "Rust (library crates)", "Canonical model for Classic & Adaptive. Owns: YAML<->model mapping, semantic validation, ops engine, migration pipeline. Single source of truth.")
        Container(rustWasm, "Rust WASM Module", "Rust → WASM (npm pkg)", "Compiled subset of domain logic. Runs in-IDE for low-latency validation and planOps. No network calls required.")
        Container(rustCli, "Rust CLI (qorix_cli)", "Rust binary", "Headless CI entry point. Commands: validate, generate-arxml, migrate. Strict exit code contract (0/1) with JSON diagnostics to stdout.")
        Container(rustSvc, "Rust Domain Service", "Rust / Axum (HTTP+gRPC)", "Long-running backend. Endpoints: /validate, /planOps, /applyOpsAndSync. Used by IDE and MCP agent for heavy operations.")

        %% ARXML Gateway
        Container(arxmlGw, "ARXML Gateway", "Spring Boot + ARTOP + GraphQL", "ARXML import/export hub. Manages EMF/ARTOP models internally. Exposes GraphQL API to Rust. REST endpoints for CI (/import, /export).")

        %% AI / MCP Layer
        Container(mcpAgent, "Developer Agent (MCP)", "TypeScript / Node", "Orchestrates LLM and Rust Domain Service. Routes user intent to domain-specific tool calls. Ensures AI mutations go through Rust ops only.")
    }

    %% User → IDE
    Rel(configEng, vscode, "Edits YAML, uses designers", "UI")
    Rel(sysArch, vscode, "Topology design, canvases", "UI")
    Rel(migEng, vscode, "ARXML import, migration wizard", "UI")
    Rel(configEng, theia, "Alternative browser/desktop IDE", "UI")

    %% CI → CLI
    Rel(ciSystem, rustCli, "qorix validate / generate-arxml / migrate", "CLI / Shell")
    Rel(gitRepo, ciSystem, "Triggers pipeline on push", "Git webhook")

    %% IDE → WASM (fast path)
    Rel(vscode, rustWasm, "validateYaml, planOps", "WASM API (in-process)")
    Rel(theia, rustWasm, "validateYaml, planOps", "WASM API (in-process)")

    %% IDE → Rust Service (heavy path)
    Rel(vscode, rustSvc, "Heavy ops, generate-arxml, cross-file validation", "HTTP/gRPC")
    Rel(theia, rustSvc, "Heavy ops, generate-arxml, cross-file validation", "HTTP/gRPC")

    %% IDE → MCP Agent (AI path)
    Rel(vscode, mcpAgent, "AI chat messages + YAML context", "MCP Protocol")
    Rel(theia, mcpAgent, "AI chat messages + YAML context", "MCP Protocol")

    %% MCP → LLM + Rust
    Rel(mcpAgent, llm, "Natural language prompts, intent extraction", "HTTPS")
    Rel(mcpAgent, rustSvc, "Tool calls: validate_project, plan_ops", "HTTP/JSON")

    %% Rust Service → ARXML Gateway
    Rel(rustSvc, arxmlGw, "importArxml, exportArxml, applyOps", "GraphQL HTTP")
    Rel(rustCli, arxmlGw, "importArxml, exportArxml (CI batch)", "GraphQL HTTP")

    %% WASM + CLI share Rust Core
    Rel(rustWasm, rustCore, "Compiled from", "Rust crate dependency")
    Rel(rustCli, rustCore, "Links against", "Rust crate dependency")
    Rel(rustSvc, rustCore, "Links against", "Rust crate dependency")

    %% ARXML Gateway → External
    Rel(arxmlGw, legacyTools, "ARXML file import", "File / ARXML")
    Rel(arxmlGw, buildToolchain, "ARXML file export", "File / ARXML")
```

---

## Container Responsibilities

### IDE Clients

| Container | Technology | Responsibility |
|---|---|---|
| VS Code Extension | TypeScript / React | YAML editing, schema completion, Classic & Adaptive graphical designers, WASM bridge, AI chat panel |
| Theia IDE | TypeScript / React | Desktop/web alternative; identical APIs and contracts as VS Code |

- Classic designers: SWC, ComStack, ECU/BSW, OS, NvM, RTE
- Adaptive designers: Application, Communication, Machine, Platform Services, Execution, Deployment
- Fast path → WASM for instant feedback; heavy path → Rust Domain Service

### Rust Domain Platform

| Container | Technology | Responsibility |
|---|---|---|
| Rust Domain Core | Rust (crates) | Canonical model, YAML↔model, validation, ops, migration — single source of truth |
| Rust WASM Module | Rust → WASM npm pkg | In-IDE validation & planOps; no network; compiled subset of core |
| Rust CLI | Rust binary | Headless CI/batch entry point; same domain core as service |
| Rust Domain Service | Rust / Axum HTTP+gRPC | Long-running backend for IDE and MCP; /validate, /planOps, /applyOpsAndSync |

**Key principle:** `rustCore` is a library shared by WASM, CLI, and Service — no parallel implementations.

### ARXML Gateway

| Container | Technology | Responsibility |
|---|---|---|
| ARXML Gateway | Spring Boot + ARTOP + GraphQL | ARXML-only import/export; EMF model management; GraphQL interface to Rust |

- Rust uses only the GraphQL API; it never touches EMF classes directly.
- Import flow: `ARXML → EMF → GraphQL → Rust model → YAML`
- Export flow: `YAML → Rust model → GraphQL mutations → EMF → ARXML`

### AI / MCP Layer

| Container | Technology | Responsibility |
|---|---|---|
| Developer Agent (MCP) | TypeScript / Node | Intent routing, tool registry, safe AI orchestration via Rust ops |
| LLM Backend | External (OpenAI / self-hosted) | Natural language understanding, plan explanations |

---

## Key Architectural Decisions at C2

- **WASM for speed, Rust Service for depth.** Fast & local = WASM; heavy & persistent = Rust service + gateway.
- **CLI as headless pipeline entry point.** Same codebase as IDE, strict exit code contracts for CI.
- **AI is always wrapped in Rust.** The MCP agent never mutates files or EMF directly — all changes are Rust `OperationPlan` instances, validated before apply.
- **Spring Boot / EMF are implementation details.** They sit behind the GraphQL contract and are invisible to all other containers.
