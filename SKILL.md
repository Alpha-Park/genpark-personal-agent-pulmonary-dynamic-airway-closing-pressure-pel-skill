---
name: genpark-personal-agent-pulmonary-dynamic-airway-closing-pressure-pel-skill
description: Dynamic Airway Closing Pressure (P_cl) and Static Recoil Pressure (P_st(L)) analyzer. Evaluates small airway compressibility, peripheral airway closing volume thresholds, and dynamic flow limitation based on equal pressure point (EPP) theory.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - pulmonary
  - airway-mechanics
  - closing-pressure
  - elastic-recoil
  - openclaw
  - genpark
  - mcp
---

# Pulmonary Dynamic Airway Closing Pressure Skill

## Overview
This skill implements Mead's equal pressure point (EPP) model of dynamic airway compression:
- **Alveolar Driving Pressure**: Sum of pleural driving pressure ($P_{\text{pl}}$) and lung static elastic recoil ($P_{\text{st}(L)}$).
- **Intrabronchial Pressure Profile**: Accounts for frictional upstream pressure drops ($\Delta P_{\text{us}} = \dot{V} \cdot R_{\text{us}}$).
- **Transmural Pressure Gradient ($P_{\text{tm}}$)**: The differential between internal bronchial pressure and surrounding pleural pressure. When $P_{\text{tm}} < 0$, compressive forces cause small airway narrowing or dynamic airway closure.

## Mathematical Formulation
1. **Alveolar Pressure**:
   $$P_{\text{alv}} = P_{\text{pl}} + P_{\text{st}(L)}$$
2. **Upstream Pressure Drop**:
   $$\Delta P_{\text{us}} = \dot{V} \times R_{\text{us}}$$
3. **Intrabronchial Pressure**:
   $$P_{\text{bronchial}} = P_{\text{alv}} - \Delta P_{\text{us}}$$
4. **Transmural Pressure**:
   $$P_{\text{tm}} = P_{\text{bronchial}} - P_{\text{pl}} = P_{\text{st}(L)} - (\dot{V} \times R_{\text{us}})$$

## Usage
```python
from client import DynamicAirwayClosingPressureClient

client = DynamicAirwayClosingPressureClient()
res = client.evaluate_closing_dynamics(
    transpulmonary_pressure_cmh2o=8.0,
    pleural_pressure_cmh2o=15.0,
    forced_expiratory_flow_l_s=2.0
)
print(res["evaluation"]["classification"])
```
