Adaptive Cluster 06 – Mappings and Topology Requirements
=========================================================

Scope
-----

Capture logical-to-physical mappings and network topology.

Assumptions
-----------

Mappings are validated against safety and performance constraints.

Requirements
------------

.. req:: Mapping rules
   :id: AD-CL06-RQ-001
   :status: open
   :domain: adaptive
   :cluster: cluster-06
   :tags: adaptive, mappings, topology

   The platform shall support explicit logical-to-physical mapping
   rules that assign software components to machines and bind service
   instances to network endpoints.

.. req:: Topology constraints
   :id: AD-CL06-RQ-002
   :status: open
   :domain: adaptive
   :cluster: cluster-06
   :tags: adaptive, mappings, constraints
   :links: AD-CL06-RQ-001

   The platform validator shall enforce topology constraints (e.g.
   latency budget, bandwidth ceiling, safety-island isolation) and
   report violations as structured diagnostics rather than untyped
   error strings.
