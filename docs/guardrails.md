# Guardrails and Scope Control

## Purpose

The Laundry Care Agent System includes a guardrail layer before the request is processed by specialist agents.

Its role is to prevent the workflow from blindly processing every input and to ensure that requests remain within the intended laundry-care domain.

## Validation flow

1. The user submits a request.
2. The request passes through **Guardrails**.
3. The **Laundry Request Classifier** decides whether the request belongs to the supported domain.
4. Supported requests proceed to the specialist workflow.
5. Unsupported or unclear requests are routed to the **Clarification Agent**.

## Supported scope

The project defines laundry-care requests as questions related to areas such as:

- washing,
- drying,
- ironing,
- stains,
- fabric care,
- clothing care.

## Out-of-scope handling

Requests outside that scope are not sent through the Fabric, Color and Stain agents. Instead, the Clarification Agent explains that the system supports laundry and clothing-care questions and asks the user to reformulate.

## Why this matters

In an agentic workflow, guardrails are not only about harmful content. They are also about **task boundaries and workflow control**.

A specialised system should know when it has enough context to act, when a request belongs to its domain, and when it should stop or ask for clarification.

## Practical limitation

This academic project defines the guardrail and routing logic conceptually. It does not claim production-grade safety validation, exhaustive fabric-care knowledge or guaranteed correctness for every garment. Users should still consult the garment care label when making real-world decisions.