## Expected damage technical challenge 

Python code to calculate the expected damage for a given risk (e.g. particular asset
in a reinsurer's portfolio) located in a given postcode, for which the precise location 
is unknown. In a given flood event, the water depths observed within this postcode are 
given in 'depths.csv'. 

### Flood depth and relationship between depth and damage (vulnerability curve) 

Depth observations are taken from a gridded dataset, with pixels of uniform size. 
75% of the postcode is inundated, all of which is represented in this collection of observations. 
The minimum flood depth observed is 0 metres, and the maximum flood depth is 10 metres. The relationship
between water depth at the risk's location and damage to that risk is detailed in 'damage_estimate.py'. 
The set of flood depths and / or vulnerability curve are likely to change between usages of this program.

### Setting up the Conda environment

To setup the required python packages to run this code, type the following into the command line: 

conda create -n	myenv --file package_list.txt

### Running the code 

python damage_estimate.py depths.csv 200000 10 png --vcurve

arg1 --> csv_depth_file path (string)
arg2 --> maximum damage for customised vulnerability curve (integer)
arg3 --> maximum flood depth within specified postcode (float)
arg4 (optional) --> output file type (string)
arg5 (optional) --> use specified vulnerability curve, or calculate (boolean)