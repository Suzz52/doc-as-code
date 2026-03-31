# classic-cluster-05-workflow — Memory & NvM Designer

## Designer: C5 — Memory & NvM Designer
**YAML file:** `mem-nvram.yaml`

## Overview

This workflow covers defining AUTOSAR NvM (Non-Volatile Memory) blocks, their layout in NVRAM, and device capacity configuration in the Memory & NvM Designer. The Memory Map view shows blocks allocated against device address space. Users create NvM blocks, set sizes, RAM mirror config, and CRC protection. Validation checks total block usage against device capacity and block ID uniqueness.

---

## Workflow Steps

1. User opens the Memory & NvM Designer (tab C5).
2. User selects the target NVRAM device and sets total capacity.
3. User creates NvM blocks for each persistent data set.
4. User configures each block: size, NvM block type, RAM mirror, CRC type, write cycle.
5. WASM validates: total block sizes fit within device capacity, unique block IDs, valid CRC types.
6. User reviews the Memory Map view to see block layout visually.
7. User reviews the Block List view for a tabular audit.
8. User reviews the Device Usage view for capacity analysis.
9. YAML confirmed in sync; NvM config ready for RTE Mapping (C6).

---

## Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant IDE as IDE Canvas (C5)
    participant NvmYAML as mem-nvram.yaml
    participant WASM as WASM Bridge
    participant Val as Validation Pane
    participant Props as Properties Panel

    User->>IDE: Open Memory & NvM Designer (C5)
    IDE->>NvmYAML: Load existing NvM block definitions
    NvmYAML-->>IDE: Render Memory Map with existing allocations

    User->>Props: Set NVRAM device: name="EEPROM_1", capacity_bytes=65536
    Props->>NvmYAML: Append nvram_device entry
    NvmYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ Device configured

    User->>Props: Create NvM block: name="CalibrationData", size_bytes=256
    User->>Props: block_type = NVM_BLOCK_NATIVE, crc_type = CRC_16, ram_mirror = true
    Props->>NvmYAML: Append nvm_block entry
    NvmYAML-->>WASM: Revalidate block layout
    WASM-->>Val: ✓ CalibrationData block allocated at offset 0x0000

    User->>Props: Create NvM block: name="OdometerValue", size_bytes=8
    User->>Props: block_type = NVM_BLOCK_REDUNDANT, crc_type = CRC_32, write_cycle_limit=100000
    Props->>NvmYAML: Append nvm_block entry
    NvmYAML-->>WASM: Revalidate
    WASM-->>Val: ✓ OdometerValue block allocated (redundant — 2x space reserved)

    User->>Props: Create NvM block: name="FaultMemory", size_bytes=4096
    User->>Props: block_type = NVM_BLOCK_DATASET, dataset_count=8, crc_type=CRC_16
    Props->>NvmYAML: Append nvm_block entry
    NvmYAML-->>WASM: Revalidate layout
    WASM-->>Val: ✓ FaultMemory block allocated (4096 * 8 datasets = 32768 bytes)

    User->>IDE: Switch to Memory Map View (💾 Memory Map)
    IDE-->>User: Visual bar: [CalibrationData 256B][OdometerValue 16B][FaultMemory 32KB] / 64KB total

    alt Device capacity exceeded
        WASM-->>Val: ✗ Total NvM allocation 68608 bytes exceeds device capacity 65536 bytes
        User->>Props: Reduce FaultMemory dataset_count = 6 (→ 24576 bytes)
        Props->>NvmYAML: Update dataset_count
        WASM-->>Val: ✓ Total allocation 24852 bytes fits within 65536 bytes
    end

    alt Duplicate block ID
        WASM-->>Val: ✗ Block ID 0x0003 assigned to both "CalibrationData" and "SensorOffset"
        User->>Props: Assign unique block_id = 0x0004 to SensorOffset
        Props->>NvmYAML: Update block_id
        WASM-->>Val: ✓ All block IDs unique
    end

    User->>IDE: Switch to Block List View (≡ Block List)
    IDE-->>User: Table: block name, ID, size, type, CRC, RAM mirror, device — all OK

    User->>IDE: Switch to Device Usage View (📊 Device Usage)
    IDE-->>User: Capacity bar: 38% used — 39KB free

    User->>IDE: Confirm YAML in sync (● In Sync indicator)
    IDE-->>User: C5 complete — proceed to RTE & Mapping (C6)
```

---

## Key Entities Involved

| Entity | Type | YAML Path |
|---|---|---|
| `EEPROM_1` | NVRAM Device | `nvram_devices[0]` |
| `CalibrationData` | NvM Block (NATIVE) | `nvm_blocks[0]` |
| `OdometerValue` | NvM Block (REDUNDANT) | `nvm_blocks[1]` |
| `FaultMemory` | NvM Block (DATASET) | `nvm_blocks[2]` |
| Block ID | Config | `nvm_blocks[*].block_id` |
| CRC type | Config | `nvm_blocks[*].crc_type` |

---

## Validation Rules (WASM — `classic::validation`)

- Sum of all NvM block allocations (including REDUNDANT×2 and DATASET×dataset_count) must fit within device capacity.
- Every NvM block must have a unique `block_id` within the project.
- `block_type` must be one of: `NVM_BLOCK_NATIVE`, `NVM_BLOCK_REDUNDANT`, `NVM_BLOCK_DATASET`.
- `crc_type` must be one of: `NVM_CRC_8`, `NVM_CRC_16`, `NVM_CRC_32`, `NVM_CRC_NONE`.
- `dataset_count` is only valid when `block_type = NVM_BLOCK_DATASET`; ignored otherwise.
- `write_cycle_limit` must be positive if specified.

---

## Outputs

- `mem-nvram.yaml` — all NvM block definitions, device config, and layout.
- Validated NvM layout ready for RTE data element binding in **C6 RTE & Mapping**.
