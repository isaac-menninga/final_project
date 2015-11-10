# Isaac Menninga, 2015
# script to load data for one country
import pandas as pd

# load conflict data
def load_conflict_data(country_name):
	#path is a string containing the path for the data files
    path = "../data/ACLED/" + country_name + '.xlsx'
	
	#read from excel file
    data = pd.read_excel(path)
	
	#only return necessary columns
    data = data[['EVENT_DATE', 'YEAR', 'EVENT_TYPE', 'ACTOR1', 'LOCATION', 'FATALITIES']]
    return(data)

#load climate data
def load_climate_data(country_name):
	#extreme variables is a dictionary containing the file extension corresponding to each variable for extreme weather patterns
    extremes_variables = {'f_extreme_heat' : 'TX90p.hadex.abs', 'f_extreme_cold' : 'TX10p.hadex.abs', 'f_heavy_rain' : 'R95pct.hadex.anom'}
	
	#mean variables is a dictionary containing the file extension corresponding to each variable for mean temperature and precipitation
    mean_variables = {'temperature' : 'temp.cru.abs', 'precipitation' : 'precip.cru.abs'}
	
	#contains the file path for each group of variables
	#Extremes/... contains data on extreme weather, Mean/... contains mean temperature and precipitation data
    directories = ['/Extremes/Timeseries/', '/Mean/Timeseries/Absolute/']
	
	# for each group of variables
    for directory in directories:
		# if the data is for extremes, iterate over extremes_variables and gets the final path for each file to grab
        if directory == '/Extremes/Timeseries/':
            for variable in extremes_variables:
                path = '../data/climate/' + country_name + directory + country_name + '.ts.obs.' + extremes_variables[variable]
				# pandas read each data file
				
		# if the data is for means, iterate over mean_variables and get the final path for each data file
        elif directory == '/Mean/Timeseries/Absolute/':
            for variable in mean_variables:
                path = '../data/climate/' + country_name + directory + country_name + '.ts.obs.' + mean_variables[variable]
				# pandas read each data file
