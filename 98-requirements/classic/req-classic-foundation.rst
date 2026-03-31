Classic Platform – Foundation Requirements
==========================================

Scope
-----

Document foundational requirements for AUTOSAR Classic support.

Assumptions
-----------

Classic components modeled alongside Adaptive assets when needed.

Requirements
------------

.. req:: Classic component modeling
   :id: CL-BASE-RQ-001
   :status: open
   :domain: classic
   :tags: classic, component, modeling

   The platform shall support modeling of AUTOSAR Classic software
   components (SWCs), including atomic, composition, and service SWC
   types, expressed in the platform YAML schema.

.. req:: Basic RTE integration
   :id: CL-BASE-RQ-002
   :status: open
   :domain: classic
   :tags: classic, rte, integration
   :links: CL-BASE-RQ-001

   The platform shall generate RTE configuration stubs compatible with
   AUTOSAR Classic RTE generators from the component model, enabling
   round-trip validation against an existing ECU project.
