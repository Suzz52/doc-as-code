.. Copyright (C) 2025 Qorix, Inc and others.
   SPDX-License-Identifier: MIT

.. _example-architecture:

Example Architecture Specifications
=====================================

This page demonstrates the ``.. spec::`` directive.  Each spec references the
requirement it satisfies via the ``:implements:`` link option.

.. contents:: On this page
   :local:
   :depth: 1


Application Manifest Processor
--------------------------------

.. spec:: Manifest parser component for Adaptive AUTOSAR application manifests
   :id: EX-EX01-SP-001
   :status: accepted
   :domain: adaptive
   :cluster: cluster-01
   :implements: EX-EX01-RQ-001

   The ``ManifestParser`` module within the Rust core reads ARXML files and
   converts ``ApplicationManifest`` XML trees into an internal model.  It uses
   the ``quick-xml`` crate for streaming deserialization and validates every
   element against the generated schema types.

   **Interfaces:**

   * Input  – ARXML file path (``&Path``)
   * Output – ``Result<ApplicationManifest, ParseError>``

.. spec:: Diagnostic reporter for manifest schema violations
   :id: EX-EX01-SP-002
   :status: accepted
   :domain: adaptive
   :cluster: cluster-01
   :implements: EX-EX01-RQ-002

   When ``ManifestParser`` encounters a schema violation it constructs a
   ``Diagnostic`` struct containing:

   * ``severity`` (Error | Warning | Info)
   * ``file``  – absolute path to the ARXML file
   * ``range`` – line/column span of the offending element
   * ``message`` – human-readable description

   Diagnostics are streamed to the IDE extension via the GraphQL subscription
   endpoint ``diagnosticsChanged``.


Classic ARXML Importer
-----------------------

.. spec:: SwComponentType importer for Classic AUTOSAR ARXML files
   :id: EX-EX02-SP-001
   :status: open
   :domain: classic
   :cluster: cluster-01
   :implements: EX-EX02-RQ-001

   A dedicated ``ClassicImporter`` module parses ``SwComponentType`` elements
   from Classic ARXML files and populates the shared in-memory model.  The
   importer is invoked by the VSCode extension command
   ``qorix.importClassicComponent``.


Rust Core API Contract
-----------------------

.. spec:: Semantic versioning and documentation contract for qorix-core
   :id: EX-EX03-SP-001
   :status: accepted
   :domain: shared
   :implements: EX-EX03-RQ-001

   All public symbols in the ``qorix-core`` crate are:

   #. Annotated with ``/// `` doc comments following the Rust API Guidelines.
   #. Covered by at least one ``#[test]`` function in the same module.
   #. Subject to the project semver policy: no breaking changes without a prior
      ``#[deprecated]`` annotation for at least one minor release.


Architecture Specs Traceability
---------------------------------

.. needtable::
   :filter: type == "spec" and "EX-EX0" in id
   :columns: id, title, status, implements, domain
   :style: table
