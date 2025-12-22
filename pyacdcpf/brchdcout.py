from pyacdcpf.idx_brchdc import BRDC_STATUS

import numpy as np


def brchdcout(pdc):
    """
    This function checks the status of each DC branch and splits the branchdc
    array to two arrays:

        - brchdc0, which contains the out-of-service branches and
        - brchdc1, which contains the in-service branches.

    The function also returns indices of out-of-service (brchdc0i) and in-service (brchdc1i) branches
    in the original branchdc matrix.
    
    @author: Jef Beerten (KU Leuven)
    @author: Roni Irnawan (Aalborg University)
    @author: Lazar Scekic (University of Montenegro)
    """
    
    # Check if DC branch status flags are valid
    if (pdc['branchdc'][:,BRDC_STATUS]<0).any() or (pdc['branchdc'][:,BRDC_STATUS]>1).any():
        raise Exception('DC branch status flags must be either 0 or 1.\n')
    
    # Find the indices of out-of-service (brchdc0i) and in-service (brchdc1i) branches
    brchdc0i = np.where(pdc['branchdc'][:,BRDC_STATUS] == 0)[0]
    brchdc1i = np.where(pdc['branchdc'][:,BRDC_STATUS] == 1)[0]
    
    # Extract parts of branchdc array corresponding to out-of-service (brchdc0) and in-service (brchdc1) branches
    brchdc0 = pdc['branchdc'][brchdc0i,:]
    brchdc1 = pdc['branchdc'][brchdc1i,:]

    # Return the results
    return brchdc1, brchdc1i, brchdc0, brchdc0i
    