.. Copyright (C) 2025 Qorix, Inc and others.
   SPDX-License-Identifier: MIT

.. _example-tests:

Example Test Cases
==================

This page demonstrates the ``.. test::`` directive.  Each test case links back
to the requirement(s) and architecture spec(s) it verifies via ``:verifies:``.

.. contents:: On this page
   :local:
   :depth: 1


Manifest Parsing Tests
-----------------------

.. test:: Parsing a valid Adaptive AUTOSAR application manifest succeeds
   :id: EX-EX01-TC-001
   :status: open
   :domain: adaptive
   :cluster: cluster-01
   :verifies: EX-EX01-RQ-001 EX-EX01-SP-001

   **Prerequisites:** A syntactically valid ``ApplicationManifest.arxml`` sample
   file is present in ``tests/fixtures/``.

   **Steps:**

   1. Call ``ManifestParser::parse(&path)`` with the fixture file path.
   2. Assert the result is ``Ok``.
   3. Assert the returned ``ApplicationManifest`` model contains the expected
      process name and executable list.

   **Expected outcome:** Parse succeeds and the model reflects all elements
   defined in the fixture file.

.. test:: Parsing a manifest with an unknown element emits a diagnostic
   :id: EX-EX01-TC-002
   :status: open
   :domain: adaptive
   :cluster: cluster-01
   :verifies: EX-EX01-RQ-002 EX-EX01-SP-002

   **Prerequisites:** A fixture file containing an element not defined in the
   AUTOSAR AP schema is present in ``tests/fixtures/invalid/``.

   **Steps:**

   1. Call ``ManifestParser::parse(&path)`` with the invalid fixture.
   2. Collect all emitted ``Diagnostic`` items.
   3. Assert at least one diagnostic with ``severity == Error`` is present.
   4. Assert the diagnostic ``message`` is non-empty and references the
      offending element name.

   **Expected outcome:** Parsing completes (no panic), and one or more error
   diagnostics are returned describing the schema violation.


Classic Importer Tests
-----------------------

.. test:: Importing a Classic ARXML file populates the component model
   :id: EX-EX02-TC-001
   :status: open
   :domain: classic
   :cluster: cluster-01
   :verifies: EX-EX02-RQ-001 EX-EX02-SP-001

   **Prerequisites:** A fixture Classic ARXML file containing at least one
   ``SwComponentType`` element is present in ``tests/fixtures/classic/``.

   **Steps:**

   1. Invoke ``ClassicImporter::import(&path)``.
   2. Assert the result is ``Ok``.
   3. Assert the returned model contains the expected component name and ports.

   **Expected outcome:** All ``SwComponentType`` elements from the fixture are
   present in the returned model without data loss.


Rust Core API Tests
--------------------

.. test:: All public qorix-core symbols have doc comments and unit tests
   :id: EX-EX03-TC-001
   :status: open
   :domain: shared
   :verifies: EX-EX03-RQ-001 EX-EX03-SP-001

   **Prerequisites:** The ``qorix-core`` crate source tree is available.

   **Steps:**

   1. Run ``cargo doc --no-deps -p qorix-core`` and assert exit code 0.
   2. Run ``cargo test -p qorix-core`` and assert all tests pass.
   3. Run ``cargo test -p qorix-core -- --list`` and verify that every public
      module contains at least one test entry.

   **Expected outcome:** Documentation builds without warnings and all unit
   tests pass.


Test Case Traceability Table
------------------------------

.. needtable::
   :filter: type == "test" and "EX-EX0" in id
   :columns: id, title, status, verifies, domain
   :style: table
