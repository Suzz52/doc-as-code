Shared AI Assist Requirements
==============================

Scope
-----

Define AI-assisted modeling and code generation expectations.

Assumptions
-----------

AI interactions respect governance and traceability.

Requirements
------------

.. req:: AI prompt logging
   :id: SH-AI-RQ-001
   :status: open
   :domain: shared
   :tags: shared, ai, logging, governance

   All AI prompt interactions shall be logged with a unique trace ID,
   timestamp, and the identity of the requesting user or service, to
   support audit and reproducibility requirements.

.. req:: AI suggestion explainability
   :id: SH-AI-RQ-002
   :status: open
   :domain: shared
   :tags: shared, ai, explainability
   :links: SH-AI-RQ-001

   Every AI-generated suggestion presented to the user shall include a
   brief rationale indicating which model artefacts or rules were used
   to derive the suggestion.
