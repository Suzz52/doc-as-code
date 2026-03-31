Adaptive Cluster 05 – Deployment Model Requirements
====================================================

Scope
-----

Define deployment descriptors for Adaptive nodes.

Assumptions
-----------

Deployment artifacts generated from YAML/GraphQL models.

Requirements
------------

.. req:: Deployment packaging
   :id: AD-CL05-RQ-001
   :status: open
   :domain: adaptive
   :cluster: cluster-05
   :tags: adaptive, deployment, packaging

   The platform shall generate deployment packages (OCI images or
   Adaptive Platform manifest bundles) from the deployment model
   without manual post-processing steps.

.. req:: Artifact signing
   :id: AD-CL05-RQ-002
   :status: open
   :domain: adaptive
   :cluster: cluster-05
   :tags: adaptive, deployment, security, signing
   :links: AD-CL05-RQ-001

   Generated deployment artifacts shall be cryptographically signed
   using a configurable key provider so that integrity can be verified
   on the target machine before installation.
