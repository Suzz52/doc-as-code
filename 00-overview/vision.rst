.. _vision:

Platform Vision
===============

.. raw:: html

   <p style="font-size: 1.15rem; line-height: 1.8; max-width: 740px;
             color: var(--color-foreground-secondary, #444); margin-bottom: 2.5rem;">
     Qorix Developer exists because the automotive software industry has an
     engineering tooling problem. This page states that problem precisely,
     defines the goals the platform commits to solving, and is explicit about
     what is deliberately out of scope.
   </p>

----

The Problem
-----------

Automotive software teams building AUTOSAR-based systems — whether Classic ECU
software, Adaptive platform applications or bootloader configurations — face a
tooling landscape that was not designed for modern software engineering practices.

**Configuration is trapped in proprietary tools.**
AUTOSAR configuration today lives inside closed GUI applications (Tresos,
DaVinci Configurator, similar). There is no way to diff two configuration
baselines meaningfully, no way to run a validation in a CI pipeline with the
same rules that run in the tool, and no way to code-review a parameter change
with the same rigour applied to source code. Configuration management is a
second-class citizen compared to software version control.

**ARXML is a poor source format.**
ARXML files are schema-valid XML representations of the AUTOSAR metamodel.
They are technically precise and standardised — and completely unsuitable as a
day-to-day engineering source format. Binary-scale XML files produce useless
Git diffs. Merge conflicts in ARXML are routinely resolved by accepting one
side wholesale. The result is configuration drift that is discovered at
integration time, not at authoring time.

**Validation only happens in the tool, not in the pipeline.**
Because the validation rules live inside proprietary tool internals, there is
no way to validate a configuration change as part of a pull request, a nightly
build or a release gate. Engineers learn about errors at manual review time —
if at all. Safety-relevant parameter constraints like watchdog timeout
relationships, flash block size alignments and cryptographic key placement
rules are checked (if they are checked at all) by human review.

**Domain knowledge is not machine-readable.**
The expert knowledge of what makes a valid, safe, production-ready AUTOSAR
configuration is distributed across experienced engineers, internal design
guides and tool documentation. It is not expressed as executable rules that
can be run automatically. Onboarding a new engineer means transferring this
knowledge person-to-person, not via tooling.

**AI assistance has no engineering guardrails.**
General-purpose AI tools applied to automotive engineering configuration carry
a critical risk: they can produce plausible-looking changes that violate
domain constraints, AUTOSAR semantics or safety requirements. Without
structured, domain-aware guardrails and explicit engineer approval, AI
assistance in this domain is more likely to introduce subtle errors than to
reduce them.

----

Goals
-----

Qorix Developer commits to the following engineering goals. Each goal maps
to one or more SYS.2 requirements that make it testable and verifiable.

**G-1 — Config-as-Code for all AUTOSAR domains**

Every parameter, every structure, every engineering decision in a Classic,
Adaptive, BPCT or LW-BSW project is persisted as human-readable, diffable,
reviewable YAML committed to Git. A configuration change is a code change:
it goes through a pull request, it has a commit author, it has a timestamp,
and it produces a line-level diff that reviewers can comment on. ARXML
is used exclusively as an import/export interchange format, never as a
source of truth.

*Traceability:* QDX-SYS-019, QDX-SWE-004, ADR-001.

**G-2 — Validation parity across IDE, CI and headless execution**

The same rule set that validates configuration inside the IDE must also run
in a CI pipeline and in a headless CLI invocation. A change that is valid in
the IDE is valid everywhere; a change that fails validation in CI should also
fail immediately in the IDE. This requires a single Rust codebase compiled to
three build targets (service, WASM, CLI) without conditional compilation that
alters business logic.

*Traceability:* QDX-SYS-006, QDX-SWE-046, ADR-002.

**G-3 — Deterministic, reproducible artefact generation**

Identical validated YAML inputs with the same tool version must produce
byte-identical generated artefacts. No timestamps, no random GUIDs, no
environment-dependent serialisation. This property is a prerequisite for
meaningful artefact comparison between releases, for CI-based generation
gates and for safety-aligned traceability of generated outputs back to
their source configuration.

*Traceability:* QDX-SYS-009, QDX-SWE-038, ADR-008.

**G-4 — Machine-executable domain knowledge**

AUTOSAR configuration rules — unmapped runnables, incompatible port
interfaces, flash block size constraints, watchdog timeout ordering, key
address placement, service binding completeness, scheduling conflict
detection — are expressed as executable validation rules in the Rust domain
crates. They run automatically on every save, on every CI run and on every
generation attempt. Expertise is encoded once and benefits every engineer
and every project.

*Traceability:* QDX-SYS-007, QDX-SWE-016, QDX-SWE-032, QDX-SWE-066,
QDX-SWE-069, QDX-SWE-073.

**G-5 — Explainable, engineer-governed AI assistance**

AI assistance in Qorix Developer is always domain-aware, always explainable
and always subject to explicit engineer approval before any change is
persisted. The Qorix Agent produces structured ``OperationPlan`` objects —
typed lists of ``core::ops`` mutations — that engineers review, accept or
reject. The Agent never writes to a YAML file autonomously. Every accepted
plan is recorded in the audit log. Data transmission to external LLM
services is deployment-configurable and can be restricted to structural
metadata only.

*Traceability:* QDX-SYS-016, QDX-SYS-017, QDX-SWE-047, QDX-SWE-048,
QDX-SWE-051, ADR-004.

**G-6 — ASPICE-aligned traceable engineering artefacts**

The platform produces and is itself described by documentation artefacts that
satisfy ASPICE SYS.2, SWE.1, SWE.2, SWE.3, SWE.4, SWE.5 and SWE.6 process
requirements. Requirements, architecture decisions, design specifications,
unit tests, integration tests and qualification tests form a complete
traceability chain — machine-readable, always current and always linked.
There are no manually maintained spreadsheets in the traceability chain.

*Traceability:* QDX-SYS-032, QDX-SWE-041, sphinx-needs documentation set.

**G-7 — Practical engineering productivity at automotive programme scale**

The platform must be fast enough for daily engineering use. Workspace open
≤ 30 s. In-IDE schema validation ≤ 500 ms. Search results ≤ 5 s. Full
generation pipeline ≤ 60 s. These are not aspirational targets — they are
SWE.1 requirements with SWE.6 qualification tests.

*Traceability:* QDX-SWE-054 through QDX-SWE-058.

----

Non-Goals
---------

The following are explicitly out of scope for Qorix Developer. Stating what
the platform will not do is as important as stating what it will.

.. list-table::
   :widths: 35 65
   :header-rows: 1

   * - Non-goal
     - Rationale
   * - **Runtime behaviour of generated ECU software**
     - Qorix Developer generates configuration artefacts. It is not
       responsible for the runtime behaviour of the ECU software that
       consumes those artefacts. Functional safety of the target system
       is the responsibility of the integrating programme.
   * - **OEM- or project-specific parameter value policies**
     - The platform enforces structural and semantic AUTOSAR rules. It does
       not encode OEM-specific engineering guidelines, target-specific
       parameter ranges or customer programme standards. Those belong in
       project-specific extension rule sets, not in the platform core.
   * - **Full AUTOSAR tool replacement**
     - Qorix Developer does not aim to replace every capability of Tresos,
       DaVinci Configurator or similar tools in the short term. It provides
       a modern, version-controlled authoring layer and ARXML exchange via
       the gateway. Coexistence and migration paths are supported; full
       replacement is a long-term directional goal, not a v1 commitment.
   * - **Autonomous AI-driven configuration**
     - The Qorix Agent will never apply configuration changes without explicit
       engineer approval. Fully autonomous AI-driven AUTOSAR configuration
       is not a goal of this platform. Engineer accountability for
       safety-relevant configuration decisions is non-negotiable.
   * - **Target hardware bring-up and flashing toolchains**
     - Qorix Developer generates configuration artefacts for downstream
       build toolchains. It is not a debugger, flasher, oscilloscope
       interface or hardware-in-the-loop test environment.
   * - **Business, commercial and licensing requirements**
     - Pricing, licensing, enterprise contract terms and commercial
       packaging are out of scope for this specification set. They do not
       affect system behaviour and are not represented in the SYS.2/SWE.1
       requirement baseline.
   * - **Performance stack (Eclipse S-Core) — full feature parity**
     - Eclipse S-Core support in the initial releases covers project creation
       and scaffolding. Full designer and validation support is a future
       roadmap item, not a current commitment.

----

Success Criteria
-----------------

Qorix Developer will have succeeded when:

1. An AUTOSAR Classic programme can migrate its complete configuration baseline
   into version-controlled YAML and run full validation and ARXML generation
   in a CI pipeline with no manual steps.

2. An engineer new to the Adaptive AUTOSAR stack can create a correctly
   validated service topology, deployment and execution manifest configuration
   using the A1–A6 designers within a single working day, without reading the
   AUTOSAR standard.

3. A bootloader project can be created, fully validated against all VR_NNN
   cross-designer constraints and generate production-ready ``cfg.h`` and
   Makefile in a single ``qorix_cli generate`` invocation.

4. An ASPICE assessor can navigate from any generated artefact back to the
   system requirement that motivated it, through a machine-readable
   traceability chain, without asking an engineer for help.

5. An AI-suggested configuration change to a safety-relevant parameter is
   reviewed, understood and explicitly approved by an engineer before it
   reaches a YAML file — every time, by design, with no workaround path.
