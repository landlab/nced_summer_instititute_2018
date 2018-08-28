#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 22:08:48 2018

@author: nicgaspar
"""

## Linear diffusion and channels on a raster

## Import what is needed
from landlab import RasterModelGrid
from landlab.components import LinearDiffuser, FlowRouter
from landlab.components import FastscapeEroder
from landlab.plot import imshow_grid
from matplotlib import pyplot as plt


## Make a grid that is 100 by 100 with dx=dy=100. m
rmg1 = RasterModelGrid((100,100),100.)
## Add elevation field to the grid.
z1 = rmg1.add_ones('node','topographic__elevation')

## Instantiate process components
ld1 = LinearDiffuser(rmg1, linear_diffusivity=0.1)
fr1 = FlowRouter(rmg1, method='D8')
fse1 = FastscapeEroder(rmg1, K_sp = 1e-5, m_sp=0.5, n_sp=1.)

## Set some variables
rock_up_rate = 1e-3 #m/yr
dt = 1000 # yr
rock_up_len = dt*rock_up_rate # m

## Time loop where evolution happens
for i in range(500):
    z1[rmg1.core_nodes] += rock_up_len #uplift only the core nodes
    ld1.run_one_step(dt) #linear diffusion happens.
    fr1.run_one_step() #flow routing happens, time step not needed
    fse1.run_one_step(dt) #fluvial incision happens
    ## optional print statement
    print('i', i)
    
## Plotting the topography
plt.figure(1)
imshow_grid(rmg1, 'topographic__elevation')

#need to run for about 4000 time steps, or 4,000,000 years to reach SS