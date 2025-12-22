from pyacdcpf.idx_convdc import CONVSTATUS, CONV_BUS, PCONV, QCONV
from pyacdcpf.idx_busdc import BUSDC_I, BUSAC_I

import numpy as np


def convout(pdc):
    """
    This function checks the status of each AC-DC converter and splits the convdc
    array to two arrays:

        - conv0, which contains the out-of-service converters and
        - conv1, which contains the in-service converters.

    The function also returns indices of out-of-service (conv0i) and in-service (conv1i) converters
    in the original convdc matrix.

    The function sets the AC bus for out-of-service converters to -1 in pdc['busdc']. To restore the
    converter connections, the function returns a 2D array (conv0busi) containing converter indices along with
    the original buses.

    @author: Jef Beerten (KU Leuven)
    @author: Roni Irnawan (Aalborg University)
    @author: Lazar Scekic (University of Montenegro)
    """

    # Check if converter status flags are valid
    if (pdc['convdc'][:,CONVSTATUS]<0).any() or (pdc['convdc'][:,CONVSTATUS]>1).any():
        raise Exception('AC/DC converter status flags must be either 0 or 1.\n')

    # Find the indices of out-of-service (conv0i) and in-service (conv1i) converters
    conv0i = np.where(pdc['convdc'][:,CONVSTATUS] == 0)[0]
    conv1i = np.where(pdc['convdc'][:,CONVSTATUS] == 1)[0]

    # Extract parts of convdc array corresponding to out-of-service (conv0) and in-service (conv1) converters
    conv0 = pdc['convdc'][conv0i,:]
    conv1 = pdc['convdc'][conv1i,:]

    # Set active and reactive powers for out-of-service converters to 0
    conv0[:,PCONV] = 0.
    conv0[:,QCONV] = 0.

    # Set AC buses for out-of-service converters to 0 in the busdc matrix and store
    # the original AC bus indices for out-of-service converters
    if conv0i.shape[0] > 0:
        idx = [(np.where(x == pdc['busdc'][:,BUSDC_I])[0][0]) for x in conv0[:,CONV_BUS]]
        conv0busi = np.array([idx, pdc['busdc'][idx,BUSAC_I]])
        pdc['busdc'][idx,BUSAC_I] = 0 # TODO: 0 or -1?
    else:
        conv0busi = np.array([])

    # Return the results
    return pdc, conv0busi, conv1, conv1i, conv0, conv0i
