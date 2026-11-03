"""
Example usage of Pulmonary Dynamic Airway Closing Pressure Skill.
Demonstrates patent airway vs flow-limiting equal pressure point vs severe premature dynamic closure.
"""

import json
from client import DynamicAirwayClosingPressureClient


def main():
    print("=== Testing Pulmonary Dynamic Airway Closing Pressure Skill ===")
    client = DynamicAirwayClosingPressureClient()

    # 1. Healthy patent airway during mid-expiration (P_st=8 cmH2O, P_pl=15 cmH2O, Flow=2.0 L/s, R_us=2.0)
    res_patent = client.evaluate_closing_dynamics(
        transpulmonary_pressure_cmh2o=8.0,
        pleural_pressure_cmh2o=15.0,
        forced_expiratory_flow_l_s=2.0,
        lung_volume_fraction_tlc=0.60,
        upstream_resistance_cmh2o_s_l=2.0
    )
    print("\n[Case 1: Stable Patent Airway]")
    print(json.dumps(res_patent, indent=2))

    # 2. Dynamic flow limitation at Equal Pressure Point (P_st=5.0, P_pl=20.0, Flow=2.5, R_us=2.0 -> Delta P = 5.0, P_tm = 0)
    res_epp = client.evaluate_closing_dynamics(
        transpulmonary_pressure_cmh2o=5.0,
        pleural_pressure_cmh2o=20.0,
        forced_expiratory_flow_l_s=2.5,
        lung_volume_fraction_tlc=0.50,
        upstream_resistance_cmh2o_s_l=2.0
    )
    print("\n[Case 2: Equal Pressure Point / Choke Point]")
    print(json.dumps(res_epp, indent=2))

    # 3. Pathological airway collapse / lost recoil (P_st=2.5, high effort P_pl=25.0, Flow=1.5, R_us=4.0 -> P_tm = -3.5 cmH2O)
    res_collapse = client.evaluate_closing_dynamics(
        transpulmonary_pressure_cmh2o=2.5,
        pleural_pressure_cmh2o=25.0,
        forced_expiratory_flow_l_s=1.5,
        lung_volume_fraction_tlc=0.35,
        upstream_resistance_cmh2o_s_l=4.0
    )
    print("\n[Case 3: Premature Dynamic Small Airway Collapse]")
    print(json.dumps(res_collapse, indent=2))

    # Assertions
    assert res_patent["transmural_pressure_gradient_cmh2o"] > 0
    assert res_epp["transmural_pressure_gradient_cmh2o"] == 0.0
    assert res_collapse["transmural_pressure_gradient_cmh2o"] < 0
    print("\n[SUCCESS] All Airway Closing Pressure test cases passed!")


if __name__ == "__main__":
    main()
