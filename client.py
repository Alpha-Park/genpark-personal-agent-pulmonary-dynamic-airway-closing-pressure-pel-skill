"""
Pulmonary Dynamic Airway Closing Pressure & Elastic Recoil Client.
Zero-mock pure Python standard library implementation.
Calculates dynamic airway closing pressure (P_cl), static lung elastic recoil (P_st(L)),
and equal pressure point (EPP) transmural gradient to evaluate small airway collapse.
"""

import math
from typing import Dict, Any, Optional


class DynamicAirwayClosingPressureClient:
    """
    Computes airway closing pressure (P_cl), transmural pressure gradient,
    and elastic recoil pressure P_st(L) based on Mead's equal pressure point (EPP) model.
    """

    def __init__(self):
        pass

    def evaluate_closing_dynamics(
        self,
        transpulmonary_pressure_cmh2o: float,
        pleural_pressure_cmh2o: float,
        forced_expiratory_flow_l_s: float,
        lung_volume_fraction_tlc: float = 0.50,
        upstream_resistance_cmh2o_s_l: float = 2.5
    ) -> Dict[str, Any]:
        """
        Calculates dynamic intrabronchial pressure, static recoil, and closing pressure threshold.
        transpulmonary_pressure_cmh2o: P_L = P_alveolar - P_pleural (cmH2O).
        pleural_pressure_cmh2o: Intrapleural driving pressure during expiration (cmH2O).
        forced_expiratory_flow_l_s: Expiratory airflow V_dot (L/s).
        lung_volume_fraction_tlc: Current lung volume as fraction of Total Lung Capacity (0.0 to 1.0).
        upstream_resistance_cmh2o_s_l: Resistance of airways upstream from EPP (cmH2O * s / L).
        """
        if transpulmonary_pressure_cmh2o <= 0:
            raise ValueError("Transpulmonary pressure must be positive.")
        if forced_expiratory_flow_l_s < 0:
            raise ValueError("Flow rate must be non-negative.")
        if not (0.05 <= lung_volume_fraction_tlc <= 1.0):
            raise ValueError("Lung volume fraction must be between 0.05 and 1.0 TLC.")

        # Alveolar pressure: P_alv = P_pleural + P_st(L)
        # where P_st(L) is static elastic recoil pressure of the lung
        p_st_l_cmh2o = transpulmonary_pressure_cmh2o

        # Alveolar driving pressure during forced expiration:
        p_alv_cmh2o = pleural_pressure_cmh2o + p_st_l_cmh2o

        # Pressure drop along upstream bronchial segment:
        # Delta P_us = Flow * R_us
        delta_p_upstream = forced_expiratory_flow_l_s * upstream_resistance_cmh2o_s_l

        # Intrabronchial pressure at choke point:
        p_bronchial_cmh2o = p_alv_cmh2o - delta_p_upstream

        # Transmural pressure across the airway wall:
        # P_tm = P_bronchial - P_pleural
        # At the Equal Pressure Point (EPP), P_tm = 0. Downstream from EPP, P_tm < 0 (compressive).
        transmural_pressure_cmh2o = p_bronchial_cmh2o - pleural_pressure_cmh2o

        # Critical dynamic closing pressure:
        # P_cl is the external compressive threshold where airway lumen occludes.
        # Typically P_cl occurs when P_tm drops below -2.0 to -5.0 cmH2O in floppy airways,
        # or earlier in loss of parenchymal tethering (emphysema/aging).
        airway_compression_margin_cmh2o = transmural_pressure_cmh2o

        # Clinical evaluation:
        # In healthy individuals at 50% TLC: P_st(L) ~ 6-12 cmH2O.
        # In emphysema / premature small airway collapse: P_st(L) < 4 cmH2O, EPP migrates upstream to non-cartilaginous bronchioles.
        if transmural_pressure_cmh2o > 3.0:
            classification = "Patent Airway / Stable Bronchial Patency"
            clinical_status = "Positive transmural pressure gradient maintains open lumen throughout expiration."
            collapse_risk = "Negligible"
        elif transmural_pressure_cmh2o >= 0.0:
            classification = "Equal Pressure Point Boundary / Nascent Dynamic Compression"
            clinical_status = "Intrabronchial pressure balances peribronchial pleural pressure; normal physiologic flow-limiting segment."
            collapse_risk = "Mild Physiological"
        elif transmural_pressure_cmh2o >= -4.0:
            classification = "Moderate Small Airway Compression / Dynamic Flow Limitation"
            clinical_status = "Negative transmural pressure compresses downstream non-cartilaginous airways; expiratory wheezing risk."
            collapse_risk = "Moderate"
        else:
            classification = "Premature Airway Closure / Severe Bronchial Choke"
            clinical_status = "Critical transmural negative gradient causing peripheral gas trapping and small airway collapse."
            collapse_risk = "High / Pathological Closure"

        return {
            "status": "success",
            "lung_volume_fraction_tlc": round(lung_volume_fraction_tlc, 2),
            "static_elastic_recoil_pst_cmh2o": round(p_st_l_cmh2o, 2),
            "alveolar_pressure_cmh2o": round(p_alv_cmh2o, 2),
            "upstream_pressure_drop_cmh2o": round(delta_p_upstream, 2),
            "intrabronchial_pressure_cmh2o": round(p_bronchial_cmh2o, 2),
            "transmural_pressure_gradient_cmh2o": round(transmural_pressure_cmh2o, 2),
            "evaluation": {
                "classification": classification,
                "collapse_risk": collapse_risk,
                "clinical_status": clinical_status
            }
        }
