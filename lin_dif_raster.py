#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 22:08:48 2018

@author: nicgaspar
"""

## Linear diffusion model on a raster

## Import what you need
from landlab import RasterModelGrid
from landlab.components import LinearDiffuser
from landlab.plot import imshow_grid
from matplotlib import pyplot as plt

## Make a grid that is 50 by 50 with dx=dy=20. m
## Intantiate raster grid object
rmg1 = RasterModelGrid((50,50),20.)
## add elevation data to the grid
z1 = rmg1.add_ones('node','topographic__elevation')

## instantiate linear diffusion object
ld1 = LinearDiffuser(rmg1, linear_diffusivity=0.1)

## set some variables
rock_up_rate = 5e-4 #m/yr
dt = 1000 # yr
rock_up_len = dt*rock_up_rate # m

## time loop where evolution happens
for i in range(500):
    z1[rmg1.core_nodes] += rock_up_len # uplift only the core nodes
    ld1.run_one_step(dt) # diffuse landscape
    
## plot topography    
plt.figure(1)
imshow_grid(rmg1, 'topographic__elevation')

#need to run for about 2000 time steps, or 2,000,000 years to reach SS