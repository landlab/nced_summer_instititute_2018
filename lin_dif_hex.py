#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 22:08:48 2018

@author: nicgaspar
"""

## Linear diffusion model on a hex grid

## First import what you need
from landlab import HexModelGrid
from landlab.components import LinearDiffuser
from landlab.plot import imshow_grid
from matplotlib import pyplot as plt

## Make a grid that is 50 by 50 with dx=dy=20. m,
## except that doesn't work for Hex! so make it 51 by 50
hmg1 = HexModelGrid(51,50,20.)
## Add elevation data to the grid.
z1 = hmg1.add_ones('node','topographic__elevation')

## Instantiate linear diffusion object
ld1 = LinearDiffuser(hmg1, linear_diffusivity=0.1)

## Set some variables
rock_up_rate = 5e-4 #m/yr
dt = 1000 # yr, time step
rock_up_len = dt*rock_up_rate # m

## Time loop where the evolution happens.
for i in range(1500):
    z1[hmg1.core_nodes] += rock_up_len #uplift only the core nodes
    ld1.run_one_step(dt) #diffusion happens
 
## Plot the topography to see what comes out.
plt.figure(2)
imshow_grid(hmg1, 'topographic__elevation')

#need to run for about 2000 time steps, or 2,000,000 years to reach SSf