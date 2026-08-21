# Laundry Care Agent — Multi-Agent AI System

> Multi-agent laundry-care system originally developed as an academic AI project and later extended into a functional Python and Streamlit prototype through AI-assisted development.

**Context:** Postgraduate Programme in Artificial Intelligence applied to Marketing — IPAM  
**Module:** Introduction to Artificial Intelligence  
**Co-developed by:** Lisbeth Chavez Oliveira & Luiza Callizo

## Project overview

Laundry decisions often involve several variables at once. A single garment can require different rules because of its fabric, colour and stain type, and those rules may conflict.

The system was designed to reduce common laundry mistakes such as:

- shrinking delicate fabrics,
- damaging colours,
- using the wrong temperature,
- applying an unsafe stain treatment.

Instead of relying on one general-purpose response, the solution decomposes the problem across specialised agents and then combines their outputs into one final user-facing recommendation.

The original academic project defined the **multi-agent architecture, prompt logic and workflow** in a professor-guided assignment, using OpenAI tools as part of the design and prototyping process.

This portfolio version extends that original work into a **working rule-based Python prototype with CLI and Streamlit interfaces**, created through **AI-assisted development**.

## Development approach & authorship

This project intentionally distinguishes between **system design** and **software implementation**.

- The original multi-agent concept, agent roles, routing logic and prompt structure were developed as part of the academic project.
- OpenAI tools were used to support the original design and prototyping process.
- The later Python and Streamlit implementation was produced through AI-assisted coding, translating the existing architecture into an executable prototype.
- The purpose of this portfolio version is to demonstrate the ability to define a problem, structure an agentic workflow, direct AI-assisted implementation, inspect the resulting logic, test behaviour and iterate on the product.

It should therefore be read as evidence of **AI-assisted prototyping, agentic-system thinking and implementation literacy**, not as a claim that every line of Python was written manually or that this is production-grade software engineering.

## Functional Python prototype

The repository includes an executable implementation of the workflow:

```text
User input
   ↓
Guardrails
   ↓
Laundry Request Classifier
   ├── Out of scope → Clarification Agent
   └── Laundry care
          ↓
      Fabric Agent
          ↓
      Color Agent
          ↓
      Stain Agent
          ↓
      Final Instruction Agent
          ↓
      User response
```

The prototype is intentionally **deterministic and rule-based** rather than dependent on an external LLM API. This makes the orchestration, routing and specialist decision logic directly inspectable and runnable without credentials or paid services.

## Interactive Streamlit interface

A lightweight web interface is included in [`streamlit_app.py`](streamlit_app.py). It allows a user to:

- enter a laundry-care request in natural language,
- try predefined examples,
- receive the final recommendation,
- see whether a request was completed, rejected or redirected,
- inspect the complete agent execution trace.

The interface makes the agent workflow easier to demonstrate to non-technical users while keeping the underlying orchestration visible.

### Run the web interface locally

Install the dependency:

```bash
pip install -r requirements.txt
```

Then launch Streamlit:

```bash
streamlit run streamlit_app.py
```

The application will open in the browser and can be used without an API key.

## Command-line interface

From the repository root:

```bash
python app.py "How should I wash a white wool jumper with a wine stain?"
```

To inspect the complete agent trace:

```bash
python app.py "How should I wash a white wool jumper with a wine stain?" --debug
```

The debug mode exposes the structured outputs produced at each stage, making the orchestration easier to inspect and troubleshoot.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The test suite covers:

- the original white-wool-and-wine example,
- out-of-scope routing to the Clarification Agent,
- guardrail rejection of an empty request,
- a synthetic-fabric / dark-colour / grease-stain workflow.

## Repository structure

```text
ai-agent-laundry-care/
├── app.py
├── streamlit_app.py
├── requirements.txt
├── laundry_care/
│   ├── __init__.py
│   ├── agents.py
│   ├── models.py
│   └── workflow.py
├── tests/
│   └── test_workflow.py
├── docs/
├── prompts/
├── pyproject.toml
└── README.md
```

## System architecture

```mermaid
flowchart LR
    A[User request] --> B[Guardrails]
    B --> C[Laundry Request Classifier]
    C -->|Laundry Care| D[Fabric Agent]
    D --> E[Color Agent]
    E --> F[Stain Agent]
    F --> G[Final Instruction Agent]
    C -->|Else / Not Laundry| H[Clarification Agent]
    G --> I[Final user guidance]
    H --> I
```

The workflow is sequential: each specialist contributes a specific layer of analysis before the final instruction is generated.

## Agents and responsibilities

| Component | Responsibility |
|---|---|
| **Guardrails** | Validate whether the request can continue through the workflow |
| **Laundry Request Classifier** | Determine whether the request is about laundry care or should be redirected |
| **Fabric Agent** | Identify fabric type and define conservative washing constraints |
| **Color Agent** | Assess colour-related risks such as separation, temperature and bleach use |
| **Stain Agent** | Identify supported stain types and recommend a conservative pre-treatment approach |
| **Final Instruction Agent** | Combine specialist outputs into one clear, practical response |
| **Clarification Agent** | Handle requests outside the laundry-care scope or requests that cannot be processed clearly |

## Why multi-agent instead of a single agent?

A single agent could generate a generic recommendation, but it may fail to prioritise competing constraints.

For example, a wine stain may require pre-treatment, while a wool garment requires particularly cautious handling. The system therefore separates responsibility across fabric safety, colour protection and stain treatment before producing the final recommendation.

This architecture makes the workflow more modular, easier to inspect and easier to debug, while reducing the risk of contradictory advice.

## Example workflow

**User request:**  
> “How should I wash a white wool jumper with a wine stain?”

The Python workflow processes the request as follows:

1. **Guardrails** — validates the request.
2. **Laundry Request Classifier** — classifies it as laundry care.
3. **Fabric Agent** — identifies wool as delicate and recommends cold water, a wool/delicate cycle and low spin.
4. **Color Agent** — identifies white and recommends separation while avoiding bleach because the fabric is delicate.
5. **Stain Agent** — identifies wine and recommends gentle cold-water pre-treatment while avoiding heat and aggressive rubbing.
6. **Final Instruction Agent** — combines the structured outputs into one user-facing recommendation.

**Prototype output:**

> Recommended approach: use cold water and a wool or delicate cycle, with low spin. Gently pre-treat with cold water and a mild detergent. Wash the garment separately from dark or strongly coloured items. Avoid heat, aggressive rubbing, bleach, high spin. Always check the garment care label before washing.

## Guardrails and scope control

The implementation includes a first validation layer before specialist processing and a classifier that separates supported laundry-care requests from unrelated requests.

Requests outside the supported domain are routed to the Clarification Agent instead of being processed by the Fabric, Color and Stain agents.

More detail is available in [`docs/guardrails.md`](docs/guardrails.md).

## Agent prompts and structured outputs

The original academic project also defined constrained prompt behaviour for specialist agents, including a Fabric Agent that returned explicit classification flags rather than free-form prose.

The Python prototype preserves the same design principle through structured dataclass outputs and a visible execution trace.

A portfolio version of the original prompt design is available in [`prompts/agent-prompts.md`](prompts/agent-prompts.md).

## What this project demonstrates

- AI-assisted Python prototyping
- Translation of an existing AI concept into an executable workflow
- Multi-agent system decomposition
- Sequential workflow orchestration
- Task routing and classification
- Specialist-agent design
- Guardrails and scope control
- Structured outputs with Python dataclasses
- Conflict-aware decision logic
- Debuggable execution traces
- Test-driven validation of key workflow behaviours
- AI-assisted Streamlit interface prototyping
- Translation of backend workflow logic into a user-facing prototype
- Human-friendly response synthesis

## Project status

**Working portfolio prototype with CLI and web interface.**

The repository contains the original system-design documentation, an AI-assisted Python implementation of the workflow and a Streamlit interface for interactive demonstration. The current prototype is rule-based and educational; it is **not** a production laundry-care service and does not provide guaranteed garment-care correctness.

Possible future iterations include:

- optional LLM-backed specialist agents,
- richer confidence and uncertainty handling,
- expanded fabric and stain taxonomies,
- public deployment of the Streamlit demo,
- logging and evaluation datasets.

## Documentation

- [`docs/architecture.md`](docs/architecture.md) — system components and orchestration logic
- [`docs/guardrails.md`](docs/guardrails.md) — scope control and safety layer
- [`docs/example-workflows.md`](docs/example-workflows.md) — example request processing
- [`prompts/agent-prompts.md`](prompts/agent-prompts.md) — structured prompt examples from the project

---

### About this portfolio project

This repository reframes and extends an academic group project as a professional case study focused on **agent architecture, orchestration, scope control, AI-assisted implementation and user-facing prototyping**.
