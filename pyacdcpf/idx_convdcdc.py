"""
DC-DC converter branch matrix for constant D operation.

Columns 0-8 must be included in input matrix (case file):
    0.  C_BUSDC        from bus (Vm-side, higher voltage)
    1.  M_BUSDC        to bus (Vc-side, lower voltage)
    2.  D_RATIO        voltage ratio D = Vc/Vm (p.u.)
    3.  R_DCDC         series resistance (p.u.)
    4.  G_DCDC         shunt conductance (p.u.)
    5.  RATE_DCDC    power rating (MW)
    6.  L_DCDC         series inductance (p.u.) - for dynamics only
    7.  C_DCDC         shunt capacitance (p.u.) - for dynamics only
    8.  STATUS_DCDC    status (1=on, 0=off)

Columns 9-12 added after power flow solution:
    9.  PF_DCDC        power at from bus (Vm-side) (MW)
   10.  PT_DCDC        power at to bus (Vc-side) (MW)
   11.  PLOSS_DCDC     total losses (MW)
   12.  IC_DCDC        current at Vc-side (kA)
"""

# Column indices
C_BUSDC = 0
M_BUSDC = 1
D_RATIO = 2
R_DCDC = 3
G_DCDC = 4
RATE_DCDC = 5
L_DCDC = 6
C_DCDC = 7      
STATUS_DCDC = 8

# Added after power flow
PC_DCDC = 9
PM_DCDC = 10
PLOSS_DCDC = 11