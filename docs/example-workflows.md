# Example Workflows

## Example: white wool jumper with a wine stain

**User input**

> How should I wash a white wool jumper with a wine stain?

## Step-by-step processing

### 1. Guardrails
The request passes the initial validation layer.

### 2. Laundry Request Classifier
The request is classified as **Laundry Care** and is allowed to continue through the specialist workflow.

### 3. Fabric Agent
The Fabric Agent identifies wool as a delicate material.

Recommended handling from the project:

- cold water,
- wool or delicate cycle,
- low spin,
- avoid hot water and aggressive spinning.

### 4. Color Agent
The Color Agent identifies the garment as white.

Recommended handling:

- wash separately,
- use a low temperature where appropriate,
- avoid bleach because the fabric is delicate.

### 5. Stain Agent
The Stain Agent identifies wine as the stain type.

Recommended pre-treatment:

- use cold water,
- avoid hot water,
- avoid aggressive rubbing, particularly on delicate fabric.

### 6. Final Instruction Agent
The Final Instruction Agent combines the three specialist outputs and generates one user-facing response.

**Illustrative final output**

> For a white wool jumper with a wine stain, the safest option is cold water and a wool or delicate cycle. Gently pre-treat the stain with cold water and a mild detergent. Wash separately and avoid hot water, bleach, strong spinning and aggressive rubbing. Always check the care label before washing.

## What the example demonstrates

The example illustrates why the system uses task decomposition. The stain treatment cannot be considered independently from the fabric risk. The final recommendation is therefore based on the combination of several constraints rather than a single generic laundry rule.