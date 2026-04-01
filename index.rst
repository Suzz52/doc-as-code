.. raw:: html

   <div style="text-align: center; margin: 3rem 0 2rem 0;">

.. image:: /_assets/icons/Qorix_Developer-Icon-Full.png
   :alt: Qorix Developer
   :align: center
   :width: 420px

.. raw:: html

   <h1 style="font-size: 2.6rem; font-weight: 700; margin-top: 1.5rem; letter-spacing: -0.02em;">
     Welcome to the Qorix Developer Documentation Portal
   </h1>
   </div>

----

Documentation as Code — Engineering Knowledge at the Speed of Software
-----------------------------------------------------------------------

Qorix Developer treats documentation as a first-class engineering artefact.
Every requirement, architecture decision, design specification and test case
lives alongside source code in Git — versioned, reviewable and always in
sync with the software it describes. There are no stale Word documents,
no locked PDFs and no tribal knowledge living outside the repository.

This portal is generated directly from ``.rst`` source files committed to the
same monorepo as the Qorix Developer platform itself. A change to a
requirement, a new validation rule or a revised architecture decision
propagates through the entire document set automatically on the next build.
Pull requests carry documentation diffs beside code diffs. Reviewers see
exactly what changed and why. The rendered portal is the single source of
truth — for engineers, for architects, for QA leads and for ASPICE assessors.

ASPICE-Aligned V-Cycle Traceability
-------------------------------------

The documentation structure follows the ASPICE V-model from system-level
requirements all the way down to qualification evidence:

.. list-table::
   :widths: 12 20 45 23
   :header-rows: 1

   * - Stage
     - Document ID
     - Purpose
     - RST Source
   * - **SYS.2**
     - QDX-SRS-001
     - System Requirements — externally observable behaviour, interfaces and
       quality attributes for the Qorix Developer platform
     - ``10-sys.2/``
   * - **SWE.1**
     - QDX-SWE-DOC-001
     - Software Requirements — 101 atomic, independently testable requirements
       derived from SYS.2 and traceable to qualification tests
     - ``20-swe.1/``
   * - **SWE.2**
     - QDX-SWA-DOC-001
     - Software Architecture — subsystem decomposition, interface contracts,
       ADRs and 101 architecture specs realising SWE.1
     - ``30-swe.2/``
   * - **SWE.3**
     - QDX-SDD-DOC-001
     - Detailed Design — public function signatures, algorithms, data structures
       and 79 unit test anchors across six subsystem SDD documents
     - ``40-swe.3/``
   * - **SWE.4**
     - QDX-SWE4-DOC-001
     - Unit Verification — 79 unit tests with isolation requirements, coverage
       targets (≥ 80 % per crate) and static analysis rules
     - ``50-testing/00-swe.4/``
   * - **SWE.5**
     - QDX-SWE5-DOC-001
     - Integration Tests — 21 interface-boundary tests across six integration
       stages verifying subsystem contracts with real (not mocked) counterparts
     - ``50-testing/01-swe.5/``
   * - **SWE.6**
     - QDX-SWE6-DOC-001
     - Qualification Tests — 101 end-to-end test cases, one per SWE.1
       requirement, executed on the released platform build
     - ``50-testing/02-swe.6/``

Every ``QDX-SWE-NNN`` requirement is linked forward to a
``QDX-SWA-SP-NNN`` architecture spec, a SWE.3 design element, a
``QDX-UT-NNN`` unit test and a ``QDX-QT-NNN`` qualification test. The
:doc:`traceability/index` page renders the full chain using
`sphinx-needs <https://sphinx-needs.readthedocs.io>`_ need-flow graphs
and need-tables — no manual traceability matrices to maintain.

How It Works
-------------

The following tools and conventions keep the documentation living and
trustworthy:

**sphinx-needs** provides the ``.. req::``, ``.. spec::`` and related
directives that turn every requirement, architecture spec and test case
into a typed, linkable object with machine-readable attributes
(``id``, ``status``, ``parent``, ``implements``, ``verification``).
Broken links and missing traces are build errors, not review comments.

**Sphinx + ReadTheDocs** renders the portal from RST source on every
merge to ``main``. The rendered output is the only documentation delivery
— engineers are never asked to read raw RST or maintain a separate
published site.

**Git + pull requests** are the review and approval mechanism. Every
requirement change, ADR update or new test case goes through the same
PR workflow as source code. CODEOWNERS ensures that requirement changes
require architecture review and that design changes require crate-lead
sign-off.

**Mermaid diagrams** embedded in the RST render live subsystem
decomposition views, data flow paths, state machines and ADR decision
flows. Diagrams live in the same commit as the prose that references them
and are never out of date.

**Jira integration** keeps work items and document IDs cross-referenced
through the ``:jira:`` field on every requirement block. A Jira ticket
can trace to the exact requirement it implements; a requirement can link
back to the Jira epic that drives it.

The result is an engineering knowledge base that is as accurate as the
last merged pull request, as searchable as a website and as reviewable
as source code.

----

.. toctree::
   :maxdepth: 2
   :caption: Handbook

   00-overview/index
   10-sys.2/index
   20-swe.1/index
   30-swe.2/index
   40-swe.3/index
   50-testing/index
   traceability/index
