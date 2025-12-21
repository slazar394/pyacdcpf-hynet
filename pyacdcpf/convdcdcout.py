"""Remove DC-DC converters facing outages from converter matrix.
"""

from sys import stdout, stderr

from numpy import array, where

from pyacdcpf.idx_convdcdc import (STATUS_DCDC, PC_DCDC, PM_DCDC, PLOSS_DCDC)


def convdcdcout(pdc):
    """
    Remove DC-DC converters facing outages from converter matrix.

    The DC-DC converter matrix is split into working (convdcdc1) and non-working
    (convdcdc0) converter matrices. Powers and currents are reset to zero for
    converters with outages.

    Parameters
    ----------
    pdc : dict
        DC power flow case structure containing 'convdcdc' matrix

    Returns
    -------
    pdc : dict
        Modified DC case structure
    convdcdc1 : array
        Working DC-DC converters (status = 1)
    convdcdc1i : array
        Indices of working DC-DC converters
    convdcdc0 : array
        Non-working DC-DC converters (status = 0)
    convdcdc0i : array
        Indices of non-working DC-DC converters

    Notes
    -----
    Unlike AC-DC converters, DC-DC converters don't have AC bus connections,
    so no busdc matrix modification is needed.

    @author: Based on convout() by Jef Beerten (KU Leuven)
    """

    ## Check if convdcdc exists in pdc
    if 'convdcdc' not in pdc or pdc['convdcdc'] is None or pdc['convdcdc'].size == 0:
        ## No DC-DC converters in the system
        return pdc, array([]), array([]), array([]), array([])

    ## DC-DC converter status validity check
    if ((pdc['convdcdc'][:, STATUS_DCDC] < 0).any()
            or (pdc['convdcdc'][:, STATUS_DCDC] > 1).any()):
        stderr.write('DC-DC converter status flags must be either 0 or 1\n')

    ## Define indices
    convdcdc0i = where(pdc['convdcdc'][:, STATUS_DCDC] == 0)[0]
    convdcdc1i = where(pdc['convdcdc'][:, STATUS_DCDC] == 1)[0]

    ## Define converter outage matrix
    convdcdc0 = pdc['convdcdc'][convdcdc0i, :]
    convdcdc1 = pdc['convdcdc'][convdcdc1i, :]

    ## Reset DC-DC converter powers and currents for outages
    ## (only if power flow results columns exist)
    if convdcdc0.shape[1] > PC_DCDC:
        convdcdc0[:, PC_DCDC] = 0.  # Power at from bus
        convdcdc0[:, PM_DCDC] = 0.  # Power at to bus

    if convdcdc0.shape[1] > PLOSS_DCDC:
        convdcdc0[:, PLOSS_DCDC] = 0.  # Losses

    return pdc, convdcdc1, convdcdc1i, convdcdc0, convdcdc0i