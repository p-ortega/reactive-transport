import os
import numpy as np 
import pandas as pd
from plotnine import *
import re

path = 'C:/Users/pablo/portega/phd/modeling/reactive-transport/E42018b'
os.chdir(path)

files = []

for r, d, f in os.walk(path+'/input/calib-raw/'):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))

# p = []
# for f in files:
# 	parameter = re.search('/input/(.*).csv', f)
# 	p.append(parameter.group(1))
# print(p)
data = pd.DataFrame(columns = ['days'])

for f in files:
	parameter = re.search('/input/calib-raw/(.*).csv', f)
	temp = pd.read_csv(f, header = None)
	temp.columns = ['days', parameter.group(1)]
	data = pd.merge(data, temp, on = 'days', how = 'outer')
data = data.drop_duplicates()
data = data.dropna(axis=0, how='all', thresh=None, subset=None, inplace=False)
data.to_csv('input/calibration-data.csv', index = False)