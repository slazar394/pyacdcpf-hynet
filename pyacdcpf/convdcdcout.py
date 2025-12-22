from pyacdcpf.idx_convdcdc import (STATUS_DCDC, PC_DCDC, PM_DCDC, PLOSS_DCDC)

import numpy as np


def convdcdcout(pdc):
    """
    This function checks the status of each DC/DC converter and splits the convdcdc
    array to two arrays:

        - convdcdc0, which contains the out-of-service converters and
        - convdcdc1, which contains the in-service converters.

    The function also returns indices of out-of-service (convdcdc0i) and in-service (convdcdc1i) converters
    in the original convdcdc matrix.

    @author: Lazar Scekic (University of Montenegro)
    """

    # Check if DC-DC converters exist in the system
    if 'convdcdc' not in pdc or pdc['convdcdc'] is None or pdc['convdcdc'].size == 0:
        return pdc, np.array([]), np.array([]), np.array([]), np.array([])

    # Check if converter status flags are valid
    if (pdc['convdcdc'][:, STATUS_DCDC] < 0).any() or (pdc['convdcdc'][:, STATUS_DCDC] > 1).any():
        raise Exception('DC/DC converter status flags must be either 0 or 1.\n')

    # Find the indices of out-of-service (convdcdc0i) and in-service (convdcdc1i) converters
    convdcdc0i = np.where(pdc['convdcdc'][:, STATUS_DCDC] == 0)[0]
    convdcdc1i = np.where(pdc['convdcdc'][:, STATUS_DCDC] == 1)[0]

    # Extract parts of convdcdc array corresponding to out-of-service (convdcdc0) and in-service (convdcdc1) converters
    convdcdc0 = pdc['convdcdc'][convdcdc0i, :]
    convdcdc1 = pdc['convdcdc'][convdcdc1i, :]

    # Reset power flow results for out-of-service DC-DC converters
    if convdcdc0.shape[1] > PC_DCDC:
        convdcdc0[:, PC_DCDC] = 0.
        convdcdc0[:, PM_DCDC] = 0.
        convdcdc0[:, PLOSS_DCDC] = 0.

    # Return the results
    return pdc, convdcdc1, convdcdc1i, convdcdc0, convdcdc0i