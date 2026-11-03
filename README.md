# Pulmonary Dynamic Airway Closing Pressure Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Dynamic Airway Closing Pressure ($P_{\text{cl}}$) and Static Recoil Pressure ($P_{\text{st}(L)}$) Analyzer based on Mead's Equal Pressure Point (EPP) physiological formulation.

```mermaid
flowchart TD
    A[Pleural Pressure P_pl & Static Recoil P_st] --> B[Alveolar Pressure P_alv = P_pl + P_st]
    C[Expiratory Airflow & Upstream Resistance] --> D[Frictional Drop: Delta P = Flow * R_us]
    B & D --> E[Intrabronchial Pressure P_bronchial]
    E & A --> F[Transmural Gradient: P_tm = P_bronchial - P_pl]
    F --> G[Equal Pressure Point & Dynamic Closure Risk Assessment]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Mead's EPP Physics**: Models the transition from effort-dependent to effort-independent flow limitation.
- **Dynamic Collapse Prevention**: Identifies premature peripheral airway closure and gas trapping.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
