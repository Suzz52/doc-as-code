.. Copyright (C) 2025 Qorix, Inc and others.
   SPDX-License-Identifier: MIT

.. _example-requirements:

Example Requirements
====================

This page demonstrates the ``.. req::`` directive and the project-wide ID scheme.
All IDs follow the pattern ``XX-YYYY-RQ-NNN``.

.. contents:: On this page
   :local:
   :depth: 1


Application Design Requirements
--------------------------------

.. req:: The platform shall support Adaptive AUTOSAR application manifests
   :id: EX-EX01-RQ-001
   :status: open
   :asil: B
   :domain: adaptive
   :cluster: cluster-01
   :source: AUTOSAR AP Specification R23-11

   The developer-platform tooling must be able to parse, validate, and render
   Adaptive AUTOSAR application manifests (``ApplicationManifest`` elements) as
   defined in the AUTOSAR Adaptive Platform Specification.

.. req:: The platform shall detect schema violations in application manifests
   :id: EX-EX01-RQ-002
   :status: open
   :asil: B
   :domain: adaptive
   :cluster: cluster-01
   :source: AUTOSAR AP Specification R23-11

   Any schema violation found during manifest parsing must be reported to the
   IDE extension with a human-readable diagnostic message including the file path,
   line number, and violation description.

.. req:: The platform shall support Classic AUTOSAR component descriptions
   :id: EX-EX02-RQ-001
   :status: open
   :asil: QM
   :domain: classic
   :cluster: cluster-01
   :source: AUTOSAR Classic Platform R22-11

   The tooling must be able to import and display software component descriptions
   (``SwComponentType``) from AUTOSAR Classic ARXML files.

.. req:: The Rust core runtime shall expose a stable API surface
   :id: EX-EX03-RQ-001
   :status: accepted
   :asil: A
   :domain: shared
   :source: Platform Architecture Decision AD-0001

   All public items in the ``qorix-core`` crate must be documented, versioned
   using semantic versioning, and covered by at least one unit test.  Breaking
   changes must be announced via a deprecation period of at least one minor
   version.


Requirements Traceability Table
---------------------------------

The table below lists all requirements on this page together with their
architecture specifications and test cases.

.. needtable::
   :filter: type == "req" and "EX-EX0" in id
   :columns: id, title, status, asil, domain
   :style: table
