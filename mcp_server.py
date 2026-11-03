"""
MCP Server for Pulmonary Dynamic Airway Closing Pressure Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import DynamicAirwayClosingPressureClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-pulmonary-dynamic-airway-closing-pressure-pel-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_closing_dynamics",
                        "description": "Calculate dynamic airway closing pressure, static recoil P_st(L), and transmural gradient.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "transpulmonary_pressure_cmh2o": {"type": "number", "description": "Static elastic recoil / transpulmonary pressure (cmH2O)."},
                                "pleural_pressure_cmh2o": {"type": "number", "description": "Intrapleural pressure during expiration (cmH2O)."},
                                "forced_expiratory_flow_l_s": {"type": "number", "description": "Forced expiratory airflow V_dot (L/s)."},
                                "lung_volume_fraction_tlc": {"type": "number", "description": "Current volume fraction of TLC (default: 0.50)."},
                                "upstream_resistance_cmh2o_s_l": {"type": "number", "description": "Upstream airway resistance (default: 2.5 cmH2O*s/L)."}
                            },
                            "required": [
                                "transpulmonary_pressure_cmh2o",
                                "pleural_pressure_cmh2o",
                                "forced_expiratory_flow_l_s"
                            ]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "evaluate_closing_dynamics":
            client = DynamicAirwayClosingPressureClient()
            try:
                res = client.evaluate_closing_dynamics(
                    transpulmonary_pressure_cmh2o=float(args["transpulmonary_pressure_cmh2o"]),
                    pleural_pressure_cmh2o=float(args["pleural_pressure_cmh2o"]),
                    forced_expiratory_flow_l_s=float(args["forced_expiratory_flow_l_s"]),
                    lung_volume_fraction_tlc=float(args.get("lung_volume_fraction_tlc", 0.50)),
                    upstream_resistance_cmh2o_s_l=float(args.get("upstream_resistance_cmh2o_s_l", 2.5))
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
