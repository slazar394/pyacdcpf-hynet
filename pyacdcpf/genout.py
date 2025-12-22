from pypower.idx_gen import GEN_STATUS

import numpy as np


def genout(ppc):
    """
    This function checks the status of each generator and splits the generator
    array to two arrays:

        - gen0, which contains the out-of-service generators and
        - gen1, which contains the in-service generators.

    The function also returns indices of out-of-service (gen0i) and in-service (gen1i) generators
    in the original generator matrix.

    @author: Jef Beerten (KU Leuven)
    @author: Roni Irnawan (Aalborg University)
    @author: Lazar Scekic (University of Montenegro)
    """

    # Check if AC generator status flags are valid
    if (ppc['gen'][:,GEN_STATUS]<0).any() or (ppc['gen'][:,GEN_STATUS]>1).any():
        raise Exception('Generator status flags must be either 0 or 1.\n')

    # Find the indices of out-of-service (gen0i) and in-service (gen1i) generators
    gen0i = np.where(ppc['gen'][:, GEN_STATUS] == 0)[0]
    gen1i = np.where(ppc['gen'][:, GEN_STATUS] > 0)[0]

    # Extract parts of generator array corresponding to out-of-service (gen0) and in-service (gen1) generators
    gen0 = ppc['gen'][gen0i, :]
    gen1 = ppc['gen'][gen1i, :]

    # Return the results
    return gen1, gen1i, gen0, gen0i