from numpy import array


def case33_dc():
    """
    Power flow data for the DC part of the 33-bus hybrid test network.
    Test network data is adopted from Ahmed Haytham's PhD thesis titled
    "Optimal Planning and Operation of AC-DC Hybrid Distribution Systems".
    """
    # Initialize a dictionary to store the DC network data
    pdc = dict.fromkeys(['version', 'baseMVAac', 'baseMVAdc', 'pol', 'busdc', 'convdc', 'branchdc'])

    # Define the PyACDC case format version
    pdc['version'] = '1'

    # Define the base MVA for the AC and the DC system
    pdc['baseMVAac'] = 10.0
    pdc['baseMVAdc'] = 100.0
    
    # Define the DC grid topology (1 for monopolar DC grid and 2 for symmetrically-grounded monopolar DC grid)
    pdc['pol'] = 1.0

    # Define the DC bus data
    # busdc_i   busac_i grid    Pdc Vdc basekVdc    Vdcmax  Vdcmin  Cdc
    pdc["busdc"] = array([
        [8, 7, 1, 0.2463, 1.02, 20.67, 1.1, 0.9, 0],
        [9, 0, 1, 0.1263, 1.00, 20.67, 1.1, 0.9, 0],
        [10, 0, 1, -0.1237, 1.00, 20.67, 1.1, 0.9, 0],
        [11, 12, 1, 0.3158, 1.00, 20.67, 1.1, 0.9, 0],
        [16, 15, 1, 0.0632, 1.00, 20.67, 1.1, 0.9, 0],
        [17, 0, 1, -0.1868, 1.00, 20.67, 1.1, 0.9, 0],
        [18, 33, 1, 0.0924, 1.00, 20.67, 1.1, 0.9, 0],
        [21, 20, 1, 0.3158, 1.00, 20.67, 1.1, 0.9, 0],
        [22, 0, 1, -0.0653, 1.00, 20.67, 1.1, 0.9, 0],
        [26, 6, 2, 0.1232, 1.00, 20.67, 1.1, 0.9, 0],
        [27, 0, 2, 0.2105, 1.00, 20.67, 1.1, 0.9, 0],
        [28, 29, 2, 0.1263, 1.00, 20.67, 1.1, 0.9, 0]
    ])

    # Define the DC converter data
    # busdc_i   type_dc type_ac P_g Q_g Vtar    rtf xtf bf  rc  xc  basekVac    Vmax   Vmin   Imax    status  LossA   LossB   LossCrec    LossCinv
    pdc["convdc"] = array([
        [8, 2, 2, 0.00, 0.00, 1.03, 0.00, 0.00, 0.00, 0.0001, 0.16428, 12.66, 1.1, 0.9, 1.2, 1, 0.00, 0.00, 0.00, 0.00],
        [26, 2, 2, 0.00, 0.00, 1.00, 0.00, 0.00, 0.00, 0.0001, 0.16428, 12.66, 1.1, 0.9, 1.2, 1, 0.00, 0.00, 0.00, 0.00],
        [18, 2, 2, 0.00, 0.00, 1.00, 0.00, 0.00, 0.00, 0.0001, 0.16428, 12.66, 1.1, 0.9, 1.2, 1, 0.00, 0.00, 0.00, 0.00],
        [11, 1, 1, 0.25, 0.075, 1.00, 0.00, 0.00, 0.00, 0.0001, 0.16428, 12.66, 1.1, 0.9, 1.2, 1, 0.00, 0.00, 0.00,0.00],
        [28, 1, 1, 0.76, 0.250, 1.00, 0.00, 0.00, 0.00, 0.0001, 0.16428, 12.66, 1.1, 0.9, 1.2, 1, 0.00, 0.00, 0.00,0.00],
        [16, 1, 1, 0.28, 0.092, 1.00, 0.00, 0.00, 0.00, 0.0001, 0.16428, 12.66, 1.1, 0.9, 1.2, 1, 0.00, 0.00, 0.00,0.00],
        [21, 1, 1, -1.20, -0.400, 1.00, 0.00, 0.00, 0.00, 0.0001, 0.16428, 12.66, 1.1, 0.9, 1.2, 1, 0.00, 0.00, 0.00,0.00]
    ])

    # DC branch data
    #   fbusdc  tbusdc  r      l    c   rateA   rateB   rateC   status
    pdc["branchdc"] = array([
        [8, 9, 0.482, 0, 0, 100, 100, 100, 1],
        [9, 10, 0.487, 0, 0, 100, 100, 100, 1],
        [10, 11, 0.092, 0, 0, 100, 100, 100, 1],
        [16, 17, 0.603, 0, 0, 100, 100, 100, 1],
        [17, 18, 0.343, 0, 0, 100, 100, 100, 1],
        [21, 22, 0.332, 0, 0, 100, 100, 100, 1],
        [26, 27, 0.133, 0, 0, 100, 100, 100, 1],
        [27, 28, 0.496, 0, 0, 100, 100, 100, 1],
        [16, 22, 0.936, 0, 0, 100, 100, 100, 1]
    ])

    return pdc