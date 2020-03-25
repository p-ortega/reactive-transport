import pandas as pd
import os
# Then get third party modules.
from win32com.client import Dispatch
import matplotlib.pyplot as plt
import pint

def selected_array(db_path, input_string, name):
   """Load database via COM and run input string.
   """
   dbase = Dispatch('IPhreeqcCOM.Object')
   dbase.OutputFileOn = True
   dbase.OutputFilename = name + ".out"
   dbase.LoadDatabase(db_path)
   dbase.RunString(input_string)
   return dbase.GetSelectedOutputArray()

# background solution data
molesNaCl = 39
bgSol = {
'pH': 7.0, 
'pe': 4.0,
'dens': 1.0,
'temp': 25.0,
'units': 'ppm',
'Na' : molesNaCl*22.98,
'Cl' : molesNaCl*35.45
}
print(bgSol)

# lixiviant solution data
molesNaCl = 39
lix = {
'pH': 7.0, 
'pe': 4.0,
'dens': 1.0,
'temp': 25.0,
'units': 'ppm',
'Na' : molesNaCl*22.98,
'Cl' : molesNaCl*35.45
}
# print(lix)
# phrFile = """
# SOLUTION 1  Background solution
#         units   {units}
#         pH      {pH}
#         pe      {pe}
#         density {dens}
#         temp    {temp}
#         Na 		{Na}
#         Cl 		{Cl}
# EQUILIBRIUM_PHASES
# 		chalcopyrite	0	1
# """.format(**bgSol)

phrFile = '''
SOLUTION 0
 pH 6 charge; N(5) 1e-3; Na 0.1; Cl 0.1
SOLUTION 1-31
 pH 4 charge; N(5) 0.1; Na 0.1; Cl 0.1
 -water 0.3333
END

TRANSPORT
-cells 30
-lengths 3.333e-4
-boundary_conditions 1 1
-punch_cells 0-31
-shifts 10
# -fix_current -1e-10
-flow_direction diffusion_only
-time 2 min 1
-multi_d true 1e-9 1 0.0 1.0
-implicit true 5
USER_GRAPH 1 implicit Nernst-Planck solution : concentrations
-headings  dist H+ NO3- Na+ Cl-
-initial_solutions false
-axis_scale y_axis 0.0 0.12
-axis_scale x_axis 0 10
-axis_titles "Distance / mm" mmol/kgw
-plot_concentration_vs x
 1 if total_time <> 1200 then end
10 graph_x dist * 1e3
20 graph_y mol("H+")*1e3, mol("NO3-")*1e3, mol("Na+")*1e3, mol("Cl-")*1e3
USER_GRAPH 2 implicit Nernst-Planck solution : potential
-init false
-axis_scale x_axis 0 10
-axis_titles "Distance / mm" "potential / mV"
-plot_concentration_vs x
 1 if total_time <> 1200 then end
10 graph_x dist * 1e3
20 graph_y pot_V * 1e3
USER_GRAPH 3 Nernst-Planck solution : current
-axis_scale x_axis 0 20
-axis_titles "Time / min" "current / A"
-plot_concentration_vs t
 1 if cell_no <> 1 then end
10 graph_x total_time / 60
20 gr
'''

result = selected_array('C:/Program Files/USGS/phreeqc-3.5.0-14000-x64/database/minteq.dat', phrFile, "E2018b-m001")