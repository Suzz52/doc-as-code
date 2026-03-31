# Classic AUTOSAR BSW/Modules → Qorix Designers (C1–C6)

This document maps the provided Classic AUTOSAR BSW modules into the Qorix Classic H1 Foundation designer categories:
- **C1** SWC & Interface
- **C2** Signals & PDU / ComStack
- **C3** ECU & BSW Module
- **C4** OS & Scheduling
- **C5** Memory & NvM
- **C6** RTE & Mapping

> Scope note: List is BSW/module-centric; therefore **C1** has no direct entries.

---

## C1 — SWC & Interface Designer
**Purpose**
- Focuses on Software Components (SWC), ports, interfaces, data types, runnable definitions.
- Not a BSW module bucket.

**Modules**
- None from the provided list.

---

## C2 — Signals & PDU / ComStack Designer
**Purpose**
- End-to-end communication configuration: signals, PDUs, routing, bus interfaces, transports, network management.
- Includes diagnostics transports and IP-based comm stacks.

### V2X / V2X-related
- **CV2x** — Cellular Vehicle-to-Everything Stack
- **CnV2xM** — C-V2X Manager
- **CnV2xMsg** — C-V2X Message Handler
- **CnV2xNet** — C-V2X Network Layer
- **CnV2xSec** — C-V2X Security Module
- **V2xBtp** — V2X Basic Transport Protocol
- **V2xDM** — V2X Data Management
- **V2xFac** — V2X Facility Layer
- **V2xGn** — V2X GeoNetworking
- **V2xM** — V2X Manager

### CAN stack
- **Can** — CAN Driver
- **CanIf** — CAN Interface
- **CanNm** — CAN Network Management
- **CanSM** — CAN State Manager
- **CanTSyn** — CAN Time Synchronization
- **CanTp** — CAN Transport Protocol
- **CanTrcv** — CAN Transceiver Driver

### LIN stack
- **Lin** — LIN Driver
- **LinIf** — LIN Interface
- **LinSM** — LIN State Manager
- **LinTp** — LIN Transport Protocol
- **LinTrcv** — LIN Transceiver Driver

### FlexRay stack
- **Fr** — FlexRay Driver
- **FrIf** — FlexRay Interface
- **FrNm** — FlexRay Network Management
- **FrSM** — FlexRay State Manager
- **FrTSyn** — FlexRay Time Synchronization
- **FrTp** — FlexRay Transport Protocol
- **FrArTp** — FlexRay Transport Protocol
- **FrTrcv** — FlexRay Transceiver Driver

### Ethernet + IP stack
- **Eth** — Ethernet Driver
- **EthIf** — Ethernet Interface
- **EthSM** — Ethernet State Manager
- **EthSwt** — Ethernet Switch Driver
- **EthTSyn** — Ethernet Time Synchronization
- **EthTrcv** — Ethernet Transceiver Driver
- **SoAd** — Socket Adaptor
- **TcpIp** — TCP/IP Stack
- **Sd** — Service Discovery
- **SomeIpTp** — SOME/IP Transport Protocol
- **UdpNm** — UDP Network Management
- **DoIP** — Diagnostics over IP

### COM/PDU routing + multiplexing
- **Com** — Communication Module
- **IpduM** — I-PDU Multiplexer
- **PduR** — PDU Router

### Communication management / network management
- **ComM** — Communication Manager
- **Nm** — Network Management

### Diagnostics (transport/communication side)
- **Dcm** — Diagnostic Communication Manager
- **LdCom** — Local Diagnostics Communication
- **Dlt** — Diagnostic Log and Trace (comm/logging plane)
- **Xcp** — Universal Measurement and Calibration Protocol

### J1939 (CAN-based higher layer)
- **J1939Dcm** — J1939 Diagnostic Communication Manager
- **J1939Nm** — J1939 Network Management
- **J1939Rm** — J1939 Request Manager
- **J1939Tp** — J1939 Transport Protocol

### High-throughput / audio-video / SDU routing
- **HTTMS** — High-Throughput Transport Management Service
- **IEEE1722Tp** — IEEE 1722 Transport Protocol
- **LSduR** — Large SDU Router

### Security (network-facing and comm-protection)
- **SecOC** — Secure Onboard Communication
- **Mka** — MACsec Key Agreement
- **IKE** — Internet Key Exchange
- **Firewall** — Firewall Module
- **Mirror** — Bus Mirroring Module
- **WEth** — Wireless Ethernet Driver
- **WEthTrcv** — Wireless Ethernet Transceiver

### Data distribution
- **Dds** — Data Distribution Service

---

## C3 — ECU & BSW Module Designer
**Purpose**
- ECU configuration baseline and “general” BSW services.
- HW drivers (non-network) and platform/system modules.

### ECU/system management
- **EcuC** — ECU Configuration
- **EcuM** — ECU State Manager
- **BswM** — Basic Software Mode Manager

### I/O and MCU peripherals (non-network)
- **Mcu** — Microcontroller Driver
- **Port** — Port Driver
- **Dio** — Digital Input/Output Driver
- **Adc** — Analog-to-Digital Converter Driver
- **Gpt** — General Purpose Timer Driver
- **Icu** — Input Capture Unit Driver
- **Ocu** — Output Compare Unit Driver
- **Pwm** — Pulse Width Modulation Driver
- **Spi** — SPI Driver
- **Wdg** — Watchdog Driver
- **WdgIf** — Watchdog Interface
- **WdgM** — Watchdog Manager

### Complex/device-specific
- **Cdd** — Complex Device Driver
- **ChrgM** — Charging Manager
- **SwCluC** — Software Cluster Connection

### Diagnostics (event/error management & tracing infrastructure)
- **Dem** — Diagnostic Event Manager
- **Det** — Default Error Tracer
- **FiM** — Function Inhibition Manager
- **CorTst** — Core Test Module

### Crypto core services (platform-facing)
- **CryIf** — Cryptographic Interface
- **Crypto** — Cryptographic Driver
- **Csm** — Crypto Service Manager
- **KeyM** — Key Manager

### Time services (platform)
- **StbM** — Synchronization Time Base Manager
- **Tm** — Time Service Module

### Utilities / libraries / tests
- **Crc** — Cyclic Redundancy Check Library
- **RamTst** — RAM Test Module
- **FlsTst** — Flash Test Module

---

## C4 — OS & Scheduling Designer
**Purpose**
- AUTOSAR OS: tasks, ISRs, counters, alarms, schedule tables.

**Modules**
- **Os** — Operating System

---

## C5 — Memory & NvM Designer
**Purpose**
- Flash/EEPROM drivers, abstraction layers, NvM block configuration, memory services.

### Memory drivers and abstractions
- **Fls** — Flash Driver
- **Eep** — EEPROM Driver
- **Fee** — Flash EEPROM Emulation
- **Ea** — EEPROM Abstraction
- **MemIf** — Memory Abstraction Interface
- **MemAcc** — Memory Access Library
- **Mem** — Memory Module
- **MemMap** — Memory Mapping

### Nv data management
- **NvM** — NVRAM Manager
- **BndM** — Bulk NvData Manager

---

## C6 — RTE & Mapping Designer
**Purpose**
- RTE layer and integration/mapping artifacts (runnables ↔ tasks, ports ↔ signals, transformation).

**Modules**
- **Rte** — Runtime Environment
- **Arti** — AUTOSAR Runtime Interface
- **Xfrm** — Transformation Module

---

## Classification rules used (for consistency)
1. **Anything primarily about signals/PDUs, routing, bus stacks, transport protocols, NM, IP stacks → C2.**
2. **ECU base services and non-network peripheral drivers → C3.**
3. **OS configuration only → C4.**
4. **Flash/EEPROM/NvM and related abstraction/mapping → C5.**
5. **RTE + integration/mapping/transformation → C6.**
6. **SWC/interfaces/datatypes (not BSW modules) → C1.**
