import argparse
import pdb
import sys
import os.path
from os import path

import numpy as np
import cmocean
import datetime

import xarray as xr
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

def water_depth(csv_file, max_depth, num_obs=7500):
    """                                                                                           
    read in water depth data from csv file                                                        
    alternatively, generate an array of random numbers within a specified range                   
                                                                                                  
    Args:                                                                                         
      csv_file (str): path to water depth csv file                                                
      max_depth (float): maximum flood depth                                                      
                                                                                                  
    Kwargs:                                                                                       
      num_obs (int): number of 'observations' in randomly generated array                         
                                                                                                  
    """

    if path.exists(csv_file):
        df = pd.read_csv(csv_file)
        max_depth = 10.0
    else:
        df = pd.DataFrame({'Depth (m)': (max_depth * np.random.rand(num_obs) ),
                           }
                          )

    return df, max_depth

def log_func(x,a,b):
    """                                                                                           
    function to calculate a logarithm with constants a and b                                      
                                                                                                  
    Args:                                                                                         
      x (Pandas.core.series.Series class): flood depth data                                       
      a (int): value of logarithmic curve intercept (Y = a + b*log(x) )                           
      b (int): value of logarithmic curve factor (Y = a + b*log(x) )                              
                                                                                                  
    """

    return a + b*np.log(x)

def power_law(x,a,b):
    """                                                                                           
    function to calculate the power law with constants a and b                                    
                                                                                                  
    Args:                                                                                         
      x (Pandas.core.series.Series class): flood depth data                                       
      a (int): value of logarithmic curve intercept (Y = a + b*log(x) )                           
      b (int): value of logarithmic curve factor (Y = a + b*log(x) )                              
                                                                                                  
    """

    return a * np.power(x,b)

def v_curve(max_damage, vcurve, max_depth, power=False, log=False, a=107000, b=11500):
    """                                                                                           
    define a vulnerability curve for the relationship between flood depth (m) and damage (£)      
                                                                                                  
    Args:                                                                                         
      max_damage (int): maximum damage value for customised vulnerability curve                   
      vcurve (bool): select whether to use specific vulnerability curve, or create one            
      max_depth (float): maximum flood depth value within postcode                                
      power (bool): use power law to create vulnerability curve                                   
      log (bool): use logarithmic function to create vulnerability curve                          
      a (int): value of logarithmic curve intercept (Y = a + b*log(x) )                           
      b (int): value of logarithmic curve factor (Y = a + b*log(x) )                              
                                                                                                  
    """

    # calculate flood depth multiplication factor                                                 
    mf = max_depth / 10.0

    # create DataFrame to hold vulnerability curve data for quick plotting                        

    if vcurve:
        vc = pd.DataFrame(
            {"Depth (m)": (0.0001, mf*0.5, mf*1.5, mf*2.5, mf*3.5, mf*4.5,
                           mf*5.5, mf*6.5, mf*7.5, mf*8.5, mf*9.5),
                "Damage (£)": (0, 50000, 80000, 95000, 105000, 112500, 120000,
                               125000, 130000, 132500, 134000),}
            )
    else:
        md = max_damage
        vc = pd.DataFrame(
            {"Depth (m)": (0.00001, mf*0.01, mf*1.0, mf*2.0, mf*3.0, mf*4.0,
                           mf*5.0, mf*6.0, mf*7.0, mf*8.0, mf*9.0, mf*10.0),
             "Damage (£)": (0, md*0.35, md*0.58, md*0.69, md*0.76, md*0.82, md*0.88,
                               md*0.92, md*0.95, md*0.98, md*0.99, md),}
            )

    # if desired, replace with power law or logarithmic function curves                           
    if power:
        vc = power_law(vc.loc[:, "Depth (m)"], max_damage, 0.1)
    elif log:
        vc = log_func(vc.loc[:, "Depth (m)"], a, b)

    return vc

def expected_damage(depth, vc):
    """                                                                                           
    calculate expected damage using water depth information and vulnerability curve               
                                                                                                  
    Args:                                                                                         
      depth (Pandas DataFrame object): flood depth data                                           
      vc (Pandas DataFrame object): vulnerability curve                                           
                                                                                                  
    """

    # initialise DataFrame                                                                        
    dm = depth

    # divide depth data into bins                                                                 
    dm['Bins'] = pd.cut(depth['Depth (m)'],
                        vc.loc[:, 'Depth (m)'].values)

    # size of label object                                                                        
    nl = vc.loc[:, 'Damage (£)'].shape[0]

    # calculate expected damage for each bin                                                      
    dm['Damage (£)'] = pd.cut(depth['Depth (m)'],
                              vc.loc[:, 'Depth (m)'].values,
                              labels=vc.loc[:, 'Damage (£)'].values[0:nl-1])

    return dm


def create_plots(damage, vc, max_damage, max_depth, file_type):
    """                                                                                           
    produce a plot of water depth against damage using gridded data                               
    overlay the vulnerability curve                                                               
                                                                                                  
    Args:                                                                                         
      damage (Pandas DataFrame object): flood damage data                                         
      vc (Pandas DataFrame object): vulnerability curve                                           
      max_damage (int): maximum damage value for customised vulnerability curve                   
      max_depth (float): maximum flood depth within specified postcode                            
      file_type (str): output file type (png, pdf, etc)                                           
                                                                                                  
    """

    # plot 1 --> vulnerability curve plot                                                         
    fig, ax = plt.subplots(figsize=[9,6]) # set up plots and specify size                         
    fili = './vcurve_gbp{0}_{1}m.{2}'.format(max_damage, max_depth, file_type)
    ax.plot(vc.loc[:, "Depth (m)"], vc.loc[:, "Damage (£)"],c='k')
    ax.set(xlabel='Inundation depth (m)', ylabel='Damage (£)',
           title='Inundation depth-damage function') # add axis labels                            
    ax.grid() # add gridlines and plot                                                            
    fig.savefig(fili,dpi=200)

    # plot 2 --> scatter plot of flood depth data                                                 
    fig, ax = plt.subplots(figsize=[9,6])
    fili = './depth_scatter_gbp{0}_{1}m.{2}'.format(max_damage, max_depth, file_type)
    ax.scatter(damage.loc[:, 'Depth (m)'], damage.loc[:, 'Damage (£)'], s=5)
    ax.plot(vc.loc[:, "Depth (m)"], vc.loc[:, "Damage (£)"], c='k')
    ax.set(xlabel='Inundation depth (m)', ylabel='Damage (£)',
           title='Inundation depth-damage function (gridded data)')
    ax.grid()
    fig.savefig(fili,dpi=200)

    # plot 3 --> histogram of flood depth observations                                            
    fig, ax = plt.subplots(figsize=[9,6])
    fili = './depth_hist_gbp{0}_{1}m.{2}'.format(max_damage, max_depth, file_type)
    binwidth = 0.1
    hist_bins = np.arange(0, 10+binwidth, binwidth)
    n, bins, patches = ax.hist(damage.loc[:,'Depth (m)'], len(hist_bins), density=True)
    ax.set(xlabel='Inundation depth (m)', ylabel='Probability density',
           title='Histogram of inundation depth')
    fig.savefig(fili, dpi=200)

    # plot 4: histogram of damage observations                                                    
    fig, ax = plt.subplots(figsize=[9,6])
    fili = './damage_hist_gbp{0}_{1}m.{2}'.format(max_damage, max_depth, file_type)
    binwidth = 1000
    hist_bins = np.arange(0, max_damage+binwidth, binwidth)
    n, bins, patches = ax.hist(damage.loc[:, 'Damage (£)'], len(hist_bins), density=True)
    ax.set(xlabel='Expected damage (£)', ylabel='Probability density',
           title='Histogram of expected damage')
    fig.savefig(fili, dpi=200)
