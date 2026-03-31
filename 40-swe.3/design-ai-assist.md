# Design – AI Assist

This is an Active document, will be updated for any new feature and improvement undertaken.

Context
---------
The AI-Assist system provides an intelligent, multi-agent workflow for processing user queries through natural language interaction. The architecture employs a **human-in-the-loop** approach where users approve/reject operations before execution, ensuring controlled automation.

**Key Characteristics:**

- **Intent-Driven Processing**: Specialized Intent Agent determines query type (explanation vs. generation) and routes with appropriate prompts and tool sets
- **Multi-Agent Orchestration**: Distinct agents handle specific concerns—intent detection, UI rendering, plan execution, and validation
- **WASM-Based Validation**: All operations are validated through WASM-exposed APIs before execution, ensuring domain rule compliance
- **Adaptive Correction Loop**: Failed validations trigger automatic plan corrections via LLM, iterating until validation passes
- **Wizard-Style UX**: ChatUI Render Agent creates structured HTML content to guide users through step-by-step operation approval
- **Tool Ecosystem**: Supports both MCP and non-MCP tools, providing flexible integration with platform capabilities
- **Safety-First Execution**: No operation executes without explicit user approval and successful WASM validation

Architecture Overview
---------------------

### Component Architecture Diagram

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#e1f5ff','primaryTextColor':'#000','primaryBorderColor':'#333','lineColor':'#666','secondaryColor':'#fff4e1','tertiaryColor':'#f0e1ff'}}}%%
graph TB
    subgraph User_Layer["User Interaction Layer"]
        User[User]
    end
    
    subgraph AI_Layer["AI-Assist Chat Layer"]
        AIChat[AI-Assist-Chat<br/>Entry Point]
        ChatUI[ChatUI Render Agent<br/>HTML Generation & Rendering]
    end
    
    subgraph Intelligence_Layer["Intelligence Layer"]
        LLM[LLM<br/>Language Model<br/>Plan Generation]
        Intent[Intent Agent<br/>Query Classification<br/>Prompt Selection]
    end
    
    subgraph Execution_Layer["Execution & Validation Layer"]
        PlanExec[PlanOpsExecution Agent<br/>Operation Orchestration]
        ValidateTool[Validate Agent Tool<br/>Pre-execution Validation]
    end
    
    subgraph Platform_Layer["Platform Integration Layer"]
        WASMBridge[WASM Bridge<br/>API Delegation]
        WASMApi[WASM Exposed API<br/>Domain Logic & Rules]
    end
    
    subgraph Tools["Tool Ecosystem"]
        MCPTools[MCP Tools]
        NonMCPTools[Non-MCP Tools]
    end
    
    User -->|Natural Language Query| AIChat
    AIChat -->|Query + Tools| LLM
    LLM <-->|Intent Analysis| Intent
    Intent -->|Operation Plan| ChatUI
    ChatUI -->|Rendered UI| User
    User -->|Approve/Reject| ChatUI
    ChatUI -->|Operation Parameters| PlanExec
    PlanExec -->|Validation Request| ValidateTool
    ValidateTool -->|Delegate| WASMBridge
    WASMBridge <-->|API Calls| WASMApi
    PlanExec -.->|If Validation Fails| LLM
    PlanExec -->|If Validation Passes| WASMBridge
    WASMBridge -->|Operation Result| PlanExec
    PlanExec -->|Outcome| ChatUI
    
    LLM -.->|Uses| MCPTools
    LLM -.->|Uses| NonMCPTools
    PlanExec -.->|Executes via| MCPTools
    PlanExec -.->|Executes via| NonMCPTools
    
    style User_Layer fill:#e1f5ff,stroke:#333,stroke-width:2px
    style AI_Layer fill:#fff4e1,stroke:#333,stroke-width:2px
    style Intelligence_Layer fill:#f0e1ff,stroke:#333,stroke-width:2px
    style Execution_Layer fill:#e1ffe1,stroke:#333,stroke-width:2px
    style Platform_Layer fill:#ffe1e1,stroke:#333,stroke-width:2px
    style Tools fill:#f5f5f5,stroke:#333,stroke-width:2px
    style User fill:#4a90e2,stroke:#333,stroke-width:2px,color:#fff
    style AIChat fill:#ffd700,stroke:#333,stroke-width:2px,color:#000
    style ChatUI fill:#ffd700,stroke:#333,stroke-width:2px,color:#000
    style LLM fill:#e94b3c,stroke:#333,stroke-width:2px,color:#fff
    style Intent fill:#9b59b6,stroke:#333,stroke-width:2px,color:#fff
    style PlanExec fill:#27ae60,stroke:#333,stroke-width:2px,color:#fff
    style ValidateTool fill:#27ae60,stroke:#333,stroke-width:2px,color:#fff
    style WASMBridge fill:#e74c3c,stroke:#333,stroke-width:2px,color:#fff
    style WASMApi fill:#e74c3c,stroke:#333,stroke-width:2px,color:#fff
    style MCPTools fill:#95a5a6,stroke:#333,stroke-width:2px,color:#fff
    style NonMCPTools fill:#95a5a6,stroke:#333,stroke-width:2px,color:#fff
```
---
### Agent Interaction Flow

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#4a90e2','primaryTextColor':'#fff','primaryBorderColor':'#333','lineColor':'#666','secondaryColor':'#e94b3c','tertiaryColor':'#f39c12'}}}%%
graph LR
    User((User))
    
    subgraph Agents["Multi-Agent System"]
        direction TB
        AIChat[AI-Assist-Chat]
        Intent[Intent Agent]
        ChatUI[ChatUI Render Agent]
        PlanExec[PlanOpsExecution Agent]
        Validate[Validate Agent Tool]
    end
    
    LLM{LLM<br/>Decision<br/>Engine}
    WASM[WASM Layer]
    
    User -->|1. Query| AIChat
    AIChat -->|2. Query + Tools| LLM
    LLM -->|3. Initial Plan| Intent
    Intent -->|4. Classified Intent| LLM
    LLM -->|5. Operation Plan| Intent
    Intent -->|6. Plan Structure| ChatUI
    ChatUI -->|7. Wizard UI| User
    User -->|8. Approval| PlanExec
    PlanExec -->|9. Validate| Validate
    Validate -->|10. Check Rules| WASM
    WASM -->|11. Valid| PlanExec
    PlanExec -->|12. Execute| WASM
    WASM -->|13. Result| PlanExec
    PlanExec -->|14. Outcome| ChatUI
    ChatUI -->|15. Rendered Result| User
    
    WASM -.->|Validation Failed| LLM
    LLM -.->|Corrected Plan| Intent
    
    style User fill:#4a90e2,stroke:#333,stroke-width:3px,color:#fff
    style LLM fill:#e94b3c,stroke:#333,stroke-width:3px,color:#fff
    style WASM fill:#f39c12,stroke:#333,stroke-width:3px,color:#000
    style Agents fill:#ecf0f1,stroke:#333,stroke-width:2px
    style AIChat fill:#3498db,stroke:#333,stroke-width:2px,color:#fff
    style Intent fill:#9b59b6,stroke:#333,stroke-width:2px,color:#fff
    style ChatUI fill:#1abc9c,stroke:#333,stroke-width:2px,color:#fff
    style PlanExec fill:#27ae60,stroke:#333,stroke-width:2px,color:#fff
    style Validate fill:#e67e22,stroke:#333,stroke-width:2px,color:#fff
```
---

Sequence Diagrams
-----------------

```mermaid
sequenceDiagram
    participant User
    box AI-Assist Chat
        participant AIChat as AI-Assist-Chat
        participant ChatUI as ChatUI Render Agent
    end
    participant LLM
    participant Intent as Intent Agent
    participant PlanExec as PlanOpsExecution Agent
    participant Validate as Validate Agent Tool
    participant WASMBridge as WASM Bridge
    participant WASMApi as WASM Exposed API
 
    User->>AIChat: Enters natural language query
    AIChat->>LLM: Sends query with available tools<br/>(MCP & non-MCP tools)
   
    LLM->>LLM: Analyzes query intent<br/>Creates set of plan operations
    LLM->>Intent: Sends query with initial analysis
   
    Intent->>Intent: Determines intent type<br/>(Explanation/Generation/Both)
    Intent->>Intent: Prepares required prompt<br/>& tool set
    Intent->>LLM: Sends query with specialized prompt<br/>& designated tools
   
    LLM->>LLM: Processes with Intent context<br/>Generates operation plan
    LLM->>Intent: Returns operation plan
   
    Intent->>ChatUI: Sends operation plan<br/>& content structure
   
    ChatUI->>ChatUI: Creates HTML tree content<br/>Based on operation plan
    ChatUI->>ChatUI: Renders on Chat UI
    ChatUI->>User: Displays operation plan<br/>with action options
   
    User->>ChatUI: Reviews operation plan<br/>& provides approval/rejection
    ChatUI->>PlanExec: Forwards user action<br/>& operation parameters
   
    PlanExec->>Validate: Calls validate command<br/>for active operation
    Validate->>WASMBridge: Delegates to WASM API
    WASMBridge->>WASMApi: Invokes validation logic
    WASMApi->>WASMBridge: Returns validation result
    WASMBridge->>Validate: Returns validation status
   
    alt Validation Success (True)
        Validate->>PlanExec: Returns validation ✓
        PlanExec->>WASMBridge: Calls designated operation<br/>tool (single or multiple)
        WASMBridge->>WASMApi: Executes operation(s)
        WASMApi->>WASMBridge: Returns operation outcome
        WASMBridge->>PlanExec: Returns outcome
        PlanExec->>PlanExec: Processes outcome<br/>Updates plan state
        PlanExec->>ChatUI: Sends operation result<br/>& next operation
        ChatUI->>ChatUI: Updates HTML tree<br/>Renders result
        ChatUI->>User: Displays result<br/>& next operation wizard
       
        alt More Operations in Plan
            User->>ChatUI: Approves/Rejects next operation
            ChatUI->>PlanExec: Forwards next operation approval
            PlanExec->>Validate: Validates next operation
            Note over PlanExec,WASMApi: Cycle repeats for each operation
        else Plan Complete
            User->>ChatUI: Acknowledges completion
            ChatUI->>User: Workflow complete
        end
    else Validation Failure (False)
        Validate->>PlanExec: Returns validation ✗
        PlanExec->>LLM: Sends validation error<br/>& correction request
        LLM->>LLM: Analyzes error<br/>Updates operation plan
        LLM->>Intent: Sends corrected plan
        Intent->>ChatUI: Sends updated plan<br/>with corrections
        ChatUI->>ChatUI: Updates HTML tree<br/>with corrections
        ChatUI->>User: Displays corrected plan<br/>& validation errors
        User->>ChatUI: Approves/Rejects corrected operation
        ChatUI->>PlanExec: Forwards corrected operation
        Note over PlanExec,WASMApi: Loop continues until<br/>validation passes
    end

```
---

Schema
------

### PlanOps Envelope Schema

The PlanOps envelope defines the structure for operation plans passed between agents. Each plan contains a summary, ordered operations array, and warnings for execution.

**Schema Location:** [artifacts/ai-assist/planops evelope schema.json](artifacts/ai-assist/planops%20evelope%20schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://qorix.com/schemas/operation-plan.schema.json",
  "title": "OperationPlan",
  "description": "Schema for CRUD operation plans targeting apply_operation() method in Qorix platform. (c) 2026 Qorix",
  "type": "object",
  "required": ["summary", "ops", "warnings"],
  "properties": {
    "summary": {
      "type": "string",
      "description": "High-level description of the entire operation plan and its purpose",
      "minLength": 1,
      "maxLength": 500,
      "examples": [
        "Comprehensive CRUD operation plan for SwcDesign and SignalsComStack models",
        "Batch update operation for vehicle network configuration"
      ]
    },
    "ops": {
      "type": "array",
      "description": "Ordered array of operations to be executed sequentially. Each operation maps to apply_operation(yaml_in, op_json) parameters.",
      "minItems": 1,
      "items": {
        "$ref": "#/definitions/Operation"
      }
    },
    "warnings": {
      "type": "array",
      "description": "Array of warning messages about the operation plan execution, validation rules, or constraints",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 500
      },
      "examples": [
        [
          "CREATE operations skip validation to allow partial initialization",
          "UPDATE operations require full validation and block on errors",
          "Operations must be executed sequentially for state consistency"
        ]
      ]
    }
  },
  "additionalProperties": false,
  "definitions": {
    "Operation": {
      "type": "object",
      "description": "Single CRUD operation with all required parameters for apply_operation() method",
      "required": ["op_name", "description", "yaml_in", "op_json"],
      "properties": {
        "op_name": {
          "type": "string",
          "description": "Unique identifier for the operation using snake_case naming convention",
          "pattern": "^[a-z][a-z0-9_]*[a-z0-9]$",
          "minLength": 3,
          "maxLength": 100,
          "examples": [
            "create_swc_field",
            "update_signal",
            "delete_bus",
            "read_application"
          ]
        },
        "description": {
          "type": "string",
          "description": "Human-readable explanation of what this operation does and its expected effect",
          "minLength": 10,
          "maxLength": 300,
          "examples": [
            "Create a new field entity in SwcDesign component",
            "Update signal properties like length or byte order",
            "Delete a bus entity from SignalsComStack network"
          ]
        },
        "yaml_in": {
          "type": "string",
          "description": "YAML-formatted input containing the domain model state (SwcDesign or SignalsComStack). Maps to first parameter of apply_operation(yaml_in, op_json).",
          "minLength": 10,
          "pattern": "^(swc_design:|signals_comstack:)",
          "examples": [
            "swc_design:\n  name: \"ExampleComponent\"\n  version: \"1.0.0\"\n  application: []\n  field: []",
            "signals_comstack:\n  name: \"VehicleNetwork\"\n  version: \"1.0.0\"\n  buses: []\n  signals: []\n  ipdus: []"
          ]
        },
        "op_json": {
          "type": "string",
          "description": "JSON-formatted operation specification conforming to UiOpV2 enum structure. Maps to second parameter of apply_operation(yaml_in, op_json). Must be valid JSON containing one of: Create, Update, Delete, or Read operation.",
          "minLength": 10,
          "contentMediaType": "application/json",
          "examples": [
            "{\"Create\": {\"entity_type\": \"Field\", \"parent_id\": null, \"data\": {\"name\": \"newField\", \"type\": \"uint32\"}}}",
            "{\"Update\": {\"entity_type\": \"Field\", \"id\": \"field-uuid-001\", \"updates\": {\"type\": \"uint32\"}}}",
            "{\"Delete\": {\"entity_type\": \"Field\", \"id\": \"field-uuid-999\"}}",
            "{\"Read\": {\"entity_type\": \"Field\", \"id\": \"field-uuid-read-001\"}}"
          ]
        }
      },
      "additionalProperties": false
    }
  },
  "examples": [
    {
      "summary": "Basic field creation operation plan",
      "ops": [
        {
          "op_name": "create_swc_field",
          "description": "Create a new field entity in SwcDesign component",
          "yaml_in": "swc_design:\n  name: \"ExampleComponent\"\n  version: \"1.0.0\"\n  application: []\n  field: []",
          "op_json": "{\"Create\": {\"entity_type\": \"Field\", \"parent_id\": null, \"data\": {\"name\": \"newField\", \"type\": \"uint32\", \"init_value\": \"0\"}}}"
        }
      ],
      "warnings": [
        "CREATE operations skip validation to allow partial initialization",
        "Each operation must be executed with result YAML as input to next"
      ]
    }
  ]
}
```

**Key Schema Elements:**

- **summary** (required): High-level description of the operation plan
- **ops** (required): Array of ordered operations, each containing:
  - `op_name`: Unique snake_case identifier
  - `description`: Human-readable explanation
  - `yaml_in`: YAML-formatted domain model state
  - `op_json`: JSON operation spec (Create/Update/Delete/Read)
- **warnings** (required): Execution rules and constraints

**Usage Flow:**
1. LLM generates operation plan conforming to this schema
2. Intent Agent validates plan structure
3. ChatUI Render Agent presents plan to user
4. PlanOpsExecution Agent executes each operation via WASM bridge
5. Each operation's result YAML becomes input for next operation

### Sample Payload

A complete example demonstrating a multi-step operation plan for creating and updating SwcDesign entities.

**Sample Location:** [artifacts/ai-assist/planops-sample-payload.yaml](artifacts/ai-assist/planops-sample-payload.yaml)

```yaml
summary: "Create SwcDesign component with application and field entities, then update field properties"

ops:
  - op_name: "create_swc_component"
    description: "Initialize a new SwcDesign component with basic metadata"
    yaml_in: |
      swc_design:
        name: "VehicleSpeedController"
        version: "1.0.0"
        application: []
        field: []
    op_json: |
      {
        "Create": {
          "entity_type": "SwcDesign",
          "parent_id": null,
          "data": {
            "name": "VehicleSpeedController",
            "version": "1.0.0",
            "description": "Main controller for vehicle speed management"
          }
        }
      }

  - op_name: "create_application_entity"
    description: "Create an application entity within the SwcDesign component"
    yaml_in: |
      swc_design:
        name: "VehicleSpeedController"
        version: "1.0.0"
        application: []
        field: []
    op_json: |
      {
        "Create": {
          "entity_type": "Application",
          "parent_id": "swc-design-uuid-001",
          "data": {
            "name": "SpeedMonitorApp",
            "type": "RealTimeApp",
            "priority": 10
          }
        }
      }

  - op_name: "create_field_vehicle_speed"
    description: "Create a field entity for storing current vehicle speed value"
    yaml_in: |
      swc_design:
        name: "VehicleSpeedController"
        version: "1.0.0"
        application:
          - name: "SpeedMonitorApp"
            type: "RealTimeApp"
            priority: 10
        field: []
    op_json: |
      {
        "Create": {
          "entity_type": "Field",
          "parent_id": "app-uuid-001",
          "data": {
            "name": "currentSpeed",
            "type": "uint32",
            "init_value": "0",
            "unit": "km/h"
          }
        }
      }

  - op_name: "update_field_speed_limit"
    description: "Update the field to add maximum speed constraint"
    yaml_in: |
      swc_design:
        name: "VehicleSpeedController"
        version: "1.0.0"
        application:
          - name: "SpeedMonitorApp"
            type: "RealTimeApp"
            priority: 10
        field:
          - name: "currentSpeed"
            type: "uint32"
            init_value: "0"
            unit: "km/h"
    op_json: |
      {
        "Update": {
          "entity_type": "Field",
          "id": "field-uuid-001",
          "updates": {
            "max_value": "250",
            "description": "Current vehicle speed with 250 km/h limit"
          }
        }
      }

  - op_name: "create_field_target_speed"
    description: "Create another field for target/desired speed"
    yaml_in: |
      swc_design:
        name: "VehicleSpeedController"
        version: "1.0.0"
        application:
          - name: "SpeedMonitorApp"
            type: "RealTimeApp"
            priority: 10
        field:
          - name: "currentSpeed"
            type: "uint32"
            init_value: "0"
            unit: "km/h"
            max_value: "250"
            description: "Current vehicle speed with 250 km/h limit"
    op_json: |
      {
        "Create": {
          "entity_type": "Field",
          "parent_id": "app-uuid-001",
          "data": {
            "name": "targetSpeed",
            "type": "uint32",
            "init_value": "0",
            "unit": "km/h",
            "max_value": "250",
            "description": "Desired target speed for cruise control"
          }
        }
      }

warnings:
  - "CREATE operations skip validation to allow partial initialization"
  - "UPDATE operations require full validation and block on errors"
  - "Operations must be executed sequentially for state consistency"
  - "Each operation's output YAML becomes input for the next operation"
  - "Validation errors trigger automatic plan correction via LLM"
  - "User approval required before executing each operation"
```

**Sample Highlights:**

- **5 Sequential Operations**: Create component → Create application → Create field → Update field → Create another field
- **State Progression**: Each operation's `yaml_in` reflects the cumulative state from previous operations
- **Mixed CRUD**: Demonstrates both CREATE and UPDATE operations
- **Domain Context**: SwcDesign domain with realistic vehicle speed controller scenario
- **Validation Rules**: Comprehensive warnings covering execution constraints

---