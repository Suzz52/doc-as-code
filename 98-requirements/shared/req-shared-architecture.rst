Shared Architecture Requirements
================================

Scope
-----

Capture requirements common to both Adaptive and Classic domains.

Assumptions
-----------

Shared services align to platform governance.

Requirements
------------

.. req:: Shared data models
   :id: SH-ARCH-RQ-001
   :status: open
   :domain: shared
   :tags: shared, architecture, data-model

   The platform shall provide a common data model layer usable by both
   Adaptive and Classic domain modules without duplication.

.. req:: Security posture
   :id: SH-ARCH-RQ-002
   :status: open
   :domain: shared
   :tags: shared, architecture, security
   :links: SH-ARCH-RQ-001

   The platform shall enforce a defined security posture covering
   authentication, authorisation, and audit logging across all shared
   services.
