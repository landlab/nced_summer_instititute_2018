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
from landlab.components import FastscapeEroder, SinkFiller
from landlab.components import ChiFinder, SteepnessFinder
from landlab.plot import imshow_grid #function, not objects
from landlab.plot import channel_profile as prf #functions, not objects
from matplotlib import pyplot as plt
import numpy as np

## Make a grid that is 100 by 100 with dx=dy=100. m
rmg1 = RasterModelGrid((100,100),100.)
## Add elevation field to the grid.
z1 = rmg1.add_ones('node','topographic__elevation')
## Add noise to initial landscape
z1[rmg1.core_nodes] += np.random.rand(len(rmg1.core_nodes))

## Instantiate process components
ld1 = LinearDiffuser(rmg1, linear_diffusivity=0.1)
fr1 = FlowRouter(rmg1, method='D8')
fse1 = FastscapeEroder(rmg1, K_sp = 1e-5, m_sp=0.5, n_sp=1.)
sf1 = SinkFiller(rmg1, routing='D8')

## instantiate helper components
chif = ChiFinder(rmg1)
steepf = SteepnessFinder(rmg1)

## Set some variables
rock_up_rate = 1e-3 #m/yr
dt = 1000 # yr
rock_up_len = dt*rock_up_rate # m

## Time loop where evolution happens
for i in range(500):
    z1[rmg1.core_nodes] += rock_up_len #uplift only the core nodes
    ld1.run_one_step(dt) #linear diffusion happens.
    sf1.run_one_step() #sink filling happens, time step not needed
    fr1.run_one_step() #flow routing happens, time step not needed
    fse1.run_one_step(dt) #fluvial incision happens
    ## optional print statement
    print('i', i)
   
## to see what fields are created:
#rmg1.at_node.keys()    
    
## Plotting the topography
plt.figure(1)
imshow_grid(rmg1, 'topographic__elevation')

## More plotting...

## find the location of the largest channels
profile_IDs = prf.channel_nodes(rmg1, rmg1.at_node['topographic__steepest_slope'],
                                 rmg1.at_node['drainage_area'],
                                 rmg1.at_node['flow__receiver_node'],
                                 number_of_channels=2)

## find the distances upstream at each node along the profile
profile_upstream_dists = prf.get_distances_upstream(rmg1, 
                                                    len(rmg1.at_node['topographic__steepest_slope']),
                                                    profile_IDs, 
                                                    rmg1.at_node['flow__link_to_receiver_node'])


## plot elevation vs. distance
plt.figure(2)
plt.plot(profile_upstream_dists[0], z1[profile_IDs[0]],'b-', label='chan 1')
plt.plot(profile_upstream_dists[1], z1[profile_IDs[1]],'r-', label= 'chan 2')
plt.title('elevation profiles')
plt.ylabel('elevation [m]')
plt.xlabel('distance upstream [m]')

## plot slope vs. drainage area
plt.figure(3)
plt.loglog(rmg1.at_node['drainage_area'][profile_IDs[0]], 
           rmg1.at_node['topographic__steepest_slope'][profile_IDs[0]],'b*')
plt.loglog(rmg1.at_node['drainage_area'][profile_IDs[1]], 
           rmg1.at_node['topographic__steepest_slope'][profile_IDs[1]],'r*')
plt.title('slope area data')
plt.ylabel('drainage area [m^2]')
plt.xlabel('slope [.]')

## Calculate channel steepness index
steepf.calculate_steepnesses()

## plot channel steepness index across the grid
plt.figure(4)
imshow_grid(rmg1, 'channel__steepness_index')
plt.title('channel steepness')

## Calculate chi index
chif.calculate_chi()

## plot chi index across the grid
plt.figure(5)
imshow_grid(rmg1, 'channel__chi_index')
plt.title('chi index')

## plot channel steepness vs. distnace upstream
plt.figure(6)
plt.plot(profile_upstream_dists[0], rmg1.at_node['channel__steepness_index'][profile_IDs[0]], 'bx',
         label='channel 1')
plt.plot(profile_upstream_dists[1], rmg1.at_node['channel__steepness_index'][profile_IDs[1]], 'rx',
         label='channel 1')
plt.title('steepness along channel')
plt.ylabel('steepness [m]')
plt.xlabel('distance [m]')

## plot chi vs. elevation profile
plt.figure(7)
plt.plot(rmg1.at_node['channel__chi_index'][profile_IDs[0]], 
         rmg1.at_node['topographic__elevation'][profile_IDs[0]], 'bx',
         label='channel 1')
plt.plot(rmg1.at_node['channel__chi_index'][profile_IDs[1]], 
         rmg1.at_node['topographic__elevation'][profile_IDs[1]], 'rx',
         label='channel 1')
plt.title('chi-elevation plot')
plt.ylabel('elevation [m]')
plt.xlabel('chi index [m]')

#need to run for about 4000 time steps, or 4,000,000 years to reach SS