Adaptive Cluster 02 – Service Modeling Requirements
====================================================

Scope
-----

Capture service modeling for Adaptive deployments.

Assumptions
-----------

Modeling aligns to AUTOSAR Adaptive service contracts.

Requirements
------------

.. req:: Service templates
   :id: AD-CL02-RQ-001
   :status: open
   :domain: adaptive
   :cluster: cluster-02
   :tags: adaptive, service-modeling, templates

   The platform shall provide reusable service templates that encode
   common AUTOSAR Adaptive service patterns (e.g. event-driven,
   request-response) to reduce boilerplate in application models.

.. req:: Service versioning
   :id: AD-CL02-RQ-002
   :status: open
   :domain: adaptive
   :cluster: cluster-02
   :tags: adaptive, service-modeling, versioning
   :links: AD-CL02-RQ-001

   Service definitions shall carry a semantic version identifier and
   the platform shall validate that consuming applications declare
   compatible version ranges at model validation time.
