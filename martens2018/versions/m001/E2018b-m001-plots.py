import numpy as np
import pandas as pd 
from plotnine import *

sim = pd.read_csv('C:/Users/pablo/portega/phd/modeling/reactive-transport/E42018b/versions/m001/E2018b-m001-results.csv', sep='\t')
print(sim.columns)
sim.columns = sim.columns.str.strip()
# sim = sim[['soln', 'step', 'pH', 'pe', 'I_naq', 'Ithree_naq', 'Cl', 'Gold']]
sim = sim.drop(["sim", 'time',"state", "dist_x", 'Unnamed: 15'], axis=1)
print(sim.head())
sim['tot_gold'] = sim.Gold.cumsum()

sim_melted = pd.melt(sim, id_vars=['soln', 'step'])
 # value_vars=['pH', 'pe', 'I_naq', 'Ithree_naq', 'Cl', 'Gold']
# print(sim_melted.head())
sim_melted.soln = sim_melted.soln.astype(str)

simPlots = (ggplot(sim_melted[sim_melted['soln'].isin(('0','1','10','20','29'))], aes(x='step', y='value', color = 'soln')) 
+ geom_point()
+ facet_wrap(('variable'), scales = 'free_y', ncol = 2)
+ theme_bw()
)
print(simPlots)