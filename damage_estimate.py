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

import flood_func as ff 

"""
Calculate the expected damage for a given risk (e.g. particular asset in a reinsurer's portfolio)
located in a given postcode, for which the precise location is unknown. 
"""

def main(inargs): 
    """
    calculate the expected damage for a given risk (e.g. building) within a 
    given postcode, using information on water depth across that postcode 
    """

    # read in water depth data from csv file, or generate array of depth values 
    # if not reading from csv file, number and range of depth 'observations' can be specified 
    df, max_depth = ff.water_depth(inargs.csv_depth_file, inargs.max_depth)

    # define or create vulnerability curve
    vc = ff.v_curve(inargs.max_damage, inargs.vcurve, max_depth)

    # calculate expected damage using specified vulnerability curve data
    damage = ff.expected_damage(df, vc)

    # specify the maximum damage before plotting 
    if inargs.vcurve:
        max_damage = 134000
        print('have used specified vulnerability curve')
    else:
        max_damage = inargs.max_damage
        print('have calculated vulnerability curve')

    # produce a series of plots 
    ff.create_plots(damage, vc, max_damage, max_depth, inargs.output_file_type)


if __name__ == '__main__':
    description='Calculate the expected damage from a given flood event, for a given risk'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("csv_depth_file", type=str, help="Depth csv file")
    parser.add_argument("max_damage", type=int, default=134000, 
                        help="Maximum damage for customised vulnerability curve")
    parser.add_argument("max_depth", type=float, default=10, 
                        help="Maximum flood depth within specified postcode")
    parser.add_argument("--output_file_type", type=str, default="png", help="Output file type")
    parser.add_argument("--vcurve", action="store_false", default=True,
                        help="Use specified vulnerability curve")
    
    args = parser.parse_args()

    main(args)
