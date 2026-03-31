Shared IDE Integration Requirements
====================================

Scope
-----

Outline IDE integration expectations across VS Code and Theia.

Assumptions
-----------

Extensions surface validation results and model navigation.

Requirements
------------

.. req:: YAML diagnostics in IDE
   :id: SH-IDE-RQ-001
   :status: open
   :domain: shared
   :tags: shared, ide, yaml, diagnostics

   The IDE extension shall display real-time YAML validation diagnostics
   (errors, warnings, hints) inline in the editor without requiring a
   separate build step.

.. req:: GraphQL introspection in IDE
   :id: SH-IDE-RQ-002
   :status: open
   :domain: shared
   :tags: shared, ide, graphql
   :links: SH-IDE-RQ-001

   The IDE extension shall support GraphQL schema introspection so that
   users can browse available queries and mutations from within the editor.
