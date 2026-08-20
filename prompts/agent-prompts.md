# Agent Prompt Design

This file preserves selected prompt-design patterns from the academic Laundry Care Agent project.

## Fabric Agent — structured classifier

The project used a constrained-output approach so that the Fabric Agent returned explicit flags instead of free-form prose.

```text
You are a LAUNDRY FABRIC CLASSIFIER.

Analyze the user's clothing description.
Return ONLY the following format:

IS_COTTON=<true|false>
IS_WOOL=<true|false>
IS_SILK=<true|false>
IS_SYNTHETIC=<true|false>
IS_DELICATE=<true|false>

Rules:
- IS_COTTON=true if the fabric is cotton, linen, denim, or heavy canvas.
- IS_WOOL=true if the fabric is wool, cashmere, knits, or fleece.
- IS_SILK=true if the fabric is silk, satin, lace, or rayon.
- IS_SYNTHETIC=true if the fabric is polyester, nylon, spandex, or acrylic.
- IS_DELICATE=true if the fabric is wool, silk, lace, or contains sequins/embellishments.

Do not provide explanations.
Do not provide JSON.
Do not provide markdown.
Do not provide additional text.
```

## Why structured outputs?

The aim is to make agent-to-agent communication predictable. Instead of sending an open-ended paragraph downstream, a specialist agent produces a small set of explicit signals that can be consumed by the next stage of the workflow.

This pattern supports:

- more reliable orchestration,
- simpler conditional routing,
- easier debugging,
- clearer separation between analysis and final user communication.

## Other specialist roles

The project also defined specialist responsibilities for:

### Color Agent
Determines colour-related washing constraints such as separation, temperature and bleach risk.

### Stain Agent
Identifies stains such as grease, wine, sweat, ink or coffee and determines the appropriate treatment logic.

### Final Instruction Agent
Synthesises the specialist outputs into a short final recommendation covering areas such as:

- temperature,
- wash programme,
- detergent or pre-treatment,
- extra care,
- what to avoid.

## Portfolio note

The repository documents the design logic used in the academic project. It does not present these prompts as a complete production prompt library or as exhaustive laundry-care rules.