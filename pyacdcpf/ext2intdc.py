from pyacdcpf.idx_busdc import GRIDDC, BUSAC_I, BUSDC_I
from pyacdcpf.idx_convdcdc import C_BUSDC, M_BUSDC
from pyacdcpf.idx_convdc import CONV_BUS
from pyacdcpf.idx_brchdc import F_BUSDC, T_BUSDC

import numpy as np


def ext2intdc(pdc):
    """
    This function converts external DC bus numbers (possibly non-consecutive) to
    consecutive internal bus numbers, starting at 0.

    In addition to the modified system structure, the function returns:

        - i2edcpmt - permutation array showing how DC buses were reordered, which maps new (sorted)
          row positions to original row positions in the busdc matrix
        - i2edc - lookup array mapping internal bus numbers to original external bus numbers. It
          has [0] prepended, so i2edc[k] gives the original external bus number for internal bus k (k=0 is dummy,
          k>=1 are actual buses).

    @author: Jef Beerten (KU Leuven)
    @author: Roni Irnawan (Aalborg University)
    @author: Lazar Scekic (University of Montenegro)
    """

    # Extract the DC grid numbers and check if there are gaps between the
    # consecutive numbers 
    griddc = np.unique(pdc['busdc'][:,GRIDDC])
    if griddc.shape[0] > 1 and any(np.gradient(np.sort(griddc))>1.):
        raise Exception('DC grid numbering is not successive.\n')

    # Sort the busdc matrix by DC grid number (primary), then AC grid connection (secondary)
    sort_key = np.lexsort((pdc['busdc'][:, BUSAC_I] == 0, pdc['busdc'][:, GRIDDC]))
    pdc['busdc'] = pdc['busdc'][sort_key, :]
    i2edcpmt = sort_key

    # Rename the DC buses
    i2edc = pdc['busdc'][:, BUSDC_I].astype(int)
    e2idc = np.zeros(max(i2edc) + 1)
    e2idc[i2edc] = np.arange(1, pdc['busdc'].shape[0] + 1)
    i2edc = np.r_[[0], i2edc]

    # Apply numbering changes to the buses, DC branches, AC-DC converters and DC-DC converters
    pdc['busdc'][:, BUSDC_I] = e2idc[pdc['busdc'][:, BUSDC_I].astype(int)]
    pdc['branchdc'][:, F_BUSDC] = e2idc[pdc['branchdc'][:, F_BUSDC].astype(int)]
    pdc['branchdc'][:, T_BUSDC] = e2idc[pdc['branchdc'][:, T_BUSDC].astype(int)]
    pdc['convdc'][:, CONV_BUS] = e2idc[pdc['convdc'][:, CONV_BUS].astype(int)]

    if 'convdcdc' in pdc and pdc['convdcdc'] is not None and pdc['convdcdc'].shape[0] > 0:
        pdc['convdcdc'][:, C_BUSDC] = e2idc[pdc['convdcdc'][:, C_BUSDC].astype(int)]
        pdc['convdcdc'][:, M_BUSDC] = e2idc[pdc['convdcdc'][:, M_BUSDC].astype(int)]

    # Return the results
    return i2edcpmt, i2edc, pdc
