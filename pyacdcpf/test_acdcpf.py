"""
Run AC/DC power flow on CIGRE B4 network and print results
"""

from pyacdcpf.Cases.PowerflowAC.cigre_b4_ac import cigre_b4_ac
from pyacdcpf.Cases.PowerflowAC.case5_stagg import case5_stagg
from pyacdcpf.Cases.PowerflowDC.cigre_b4_dc import cigre_b4_dc
from pyacdcpf.Cases.PowerflowDC.case5_stagg_MTDCslack import case5_stagg_MTDCslack
from pyacdcpf.runacdcpf import runacdcpf

# Load case data - use simpler case5_stagg for testing
caseac = case5_stagg()
casedc = case5_stagg_MTDCslack()

# Run power flow
resultsac, resultsdc, converged = runacdcpf(caseac, casedc)