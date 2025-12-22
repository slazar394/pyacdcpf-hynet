from pypower.idx_brch import BR_STATUS

import numpy as np


def brchout(ppc):
    """
    This function checks the status of each AC branch and splits the branch
    array to two arrays:

        - brch0, which contains the out-of-service branches and
        - brch1, which contains the in-service branches.

    The function also returns indices of out-of-service (brch0i) and in-service (brch1i) branches
    in the original branch matrix.

    @author: Jef Beerten (KU Leuven)
    @author: Roni Irnawan (Aalborg University)
    @author: Lazar Scekic (University of Montenegro)
    """
    
    # Check if AC branch status flags are valid
    if (ppc['branch'][:,BR_STATUS]<0).any() or (ppc['branch'][:,BR_STATUS]>1).any():
        raise Exception('AC branch status flags must be either 0 or 1.\n')
    
    # Find the indices of out-of-service (brch0i) and in-service (brch1i) branches
    brch0i = np.where(ppc['branch'][:,BR_STATUS] == 0)[0]
    brch1i = np.where(ppc['branch'][:,BR_STATUS] == 1)[0]
    
    # Extract parts of branch array corresponding to out-of-service (brch0) and in-service (brch1) branches
    brch0 = ppc['branch'][brch0i,:]
    brch1 = ppc['branch'][brch1i,:]

    # Return the results
    return brch1, brch1i, brch0, brch0i
    