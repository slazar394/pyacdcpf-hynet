from pyacdcpf.idx_busdc import BASE_KVDC, CDC
from pyacdcpf.idx_convdc import RTF, XTF, BF, RCONV, XCONV, ICMAX
from pyacdcpf.idx_brchdc import F_BUSDC, T_BUSDC, BRDC_R, BRDC_L, BRDC_C

import numpy as np


def ext2intpu(baseMVA, pdc):
    """
    This function converts external per unit quantities to internal values using
    AC system base.

    It converts DC system per-unit quantities from their respective bases
    (baseMVAac for AC converter side, baseMVAdc for DC side) to the
    unified AC system base (baseMVA).

    Conversion rules:
    - Impedances: Z_new = Z_old × (S_base_new / S_base_old)
    - Admittances: Y_new = Y_old × (S_base_old / S_base_new)
    - Currents: I_new = I_old × (S_base_old / S_base_new)

    @author: Jef Beerten (KU Leuven)
    @author: Roni Irnawan (Aalborg University)
    @author: Lazar Scekic (University of Montenegro)
    """

    # Extract base power values
    ac_converter_base = pdc['baseMVAac']
    dc_base = pdc['baseMVAdc']

    # Calculate conversion ratios
    impedance_ac_ratio = baseMVA / ac_converter_base
    admittance_ac_ratio = ac_converter_base / baseMVA
    impedance_dc_ratio = baseMVA / dc_base
    admittance_dc_ratio = dc_base / baseMVA

    # Convert AC converter side quantities to system MVA base
    pdc['convdc'][:, RTF] *= impedance_ac_ratio
    pdc['convdc'][:, XTF] *= impedance_ac_ratio
    pdc['convdc'][:, RCONV] *= impedance_ac_ratio
    pdc['convdc'][:, XCONV] *= impedance_ac_ratio
    pdc['convdc'][:, BF] *= admittance_ac_ratio
    pdc['convdc'][:, ICMAX] *= admittance_ac_ratio

    ## Convert DC converter side quantities to system MVA base
    pdc['busdc'][:, CDC] *= admittance_dc_ratio

    # Check for matching base voltages at branch ends
    from_bus_voltage = pdc['busdc'][np.where(pdc['branchdc'][:,F_BUSDC])[0],BASE_KVDC]
    to_bus_voltage = pdc['busdc'][np.where(pdc['branchdc'][:,T_BUSDC])[0],BASE_KVDC]

    if not np.all(from_bus_voltage == to_bus_voltage):
        raise Exception('The DC voltages at both sides of a DC branch do not match.\n')

    # Convert DC branch quantities to system MVA base
    pdc['branchdc'][:, BRDC_R] *= impedance_dc_ratio
    pdc['branchdc'][:, BRDC_L] *= impedance_dc_ratio
    pdc['branchdc'][:, BRDC_C] *= admittance_dc_ratio

    return pdc