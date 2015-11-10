# Isaac Menninga, 2015
# script to load data for one country
import pandas as pd
import matplotlib.pyplot as plt

# load conflict data
def load_conflict_data(country_name):
    '''This function is used to grab data on conflict occurances in a specific country. 
    The function takes one input, which is the name of the country you want to grab data for. Returns the data as a pandas data frame.'''
    
    #path is a string containing the path for the data files
    path = "../data/ACLED/" + country_name + '.xlsx'

    #read from excel file
    data = pd.read_excel(path)

    #only return necessary columns
    data = data[['EVENT_DATE', 'YEAR', 'EVENT_TYPE', 'ACTOR1', 'LOCATION', 'FATALITIES']]
    return(data)

#load climate data
def load_climate_data(country_name):
    '''This function is used to grab data on climate for each country.
    The function takes one input, which is the name of the country to grab data on. The function returns the data as a pandas data frame.'''
    
    #extreme variables is a dictionary containing the file extension corresponding to each variable for extreme weather patterns
    extremes_variables = {'f_extreme_heat' : 'TX90p.hadex.abs', 'f_extreme_cold' : 'TX10p.hadex.abs', 'f_heavy_rain' : 'R95pct.hadex.anom'}

    #mean variables is a dictionary containing the file extension corresponding to each variable for mean temperature and precipitation
    mean_variables = {'temperature' : 'temp.cru.abs', 'precipitation' : 'precip.cru.abs'}

    #contains the file path for each group of variables
    #Extremes/... contains data on extreme weather, Mean/... contains mean temperature and precipitation data
    directories = ['/Observed/Extremes/Timeseries/', '/Observed/Mean/Timeseries/Absolute/']
    
    data = pd.DataFrame()
    # for each group of variables
    for directory in directories:
        # if the data is for extremes, iterate over extremes_variables and gets the final path for each file to grab
        if directory == '/Observed/Extremes/Timeseries/':
            #gets the variable name from a list of variables
            #each variable corresponds to the end of the name of the file
            for variable in extremes_variables:
                #path is equal to the file path for the data file containing data on the current variable
                #concatonates country name, directory names and file names to form the specific file path
                path = '../data/climate/' + country_name + directory + country_name + '.ts.obs.' + extremes_variables[variable] + '.txt'
                
                #if the data frame is empty, set data equal to the contents of the first file
                if data.empty:
                    data = pd.read_table(path, delimiter = '\s+', header = 7)
                    
                #if the data frame is not empty, concatonate the data from the second file to the first
                else:
                    data_2 = pd.read_table(path, delimiter = '\s+', header = 7)
                    data = pd.concat([data, data_2], axis = 1)   

        # if the data is for means, iterate over mean_variables and get the final path for each data file
        elif directory == '/Observed/Mean/Timeseries/Absolute/':
            #gets the variable name from a list of variables
            #each variable corresponds to the end of the name of the file
            for variable in mean_variables:
                #path is equal to the file path for the data file containing data on the current variable
                #concatonates country name, directory names and file names to form the specific file path
                path = '../data/climate/' + country_name + directory + country_name + '.ts.obs.' + mean_variables[variable] + '.txt'
                
                #if the data frame is empty, set data equal to the contents of the first file
                if data.empty:
                    data = pd.read_table(path, delimiter = '\s+', header = 7)
                    
                #if the data frame is not empty, concatonate the data from the second file to the first
                else:
                    data_2 = pd.read_table(path, delimiter = '\s+', header = 7)
                    data = pd.concat([data, data_2], axis = 1)   
    
    #renames columns to clarify which variable corresponds to which set of months
    #note: DJF = Dec., Jan., Feb., MAM = Mar., Apr., May., ... etc.
    data.columns = ['YEAR', 'Annual TX90p', 'DJF TX90p', 'MAM TX90p', 'JJA TX90p', 'SON TX90p', 'YEAR', 'Annual TX10p', 'DJF TX10p', 'MAM TX10p', 'JJA TX10p', 'SON TX10p', 'YEAR', 'Annual R95pct', 'DJF R95pct', 'MAM R95pct', 'JJA R95pct', 'SON R95pct', 'YEAR', 'Annual precip', 'JFM precip', 'AMJ precip', 'JAS precip', 'OND precip', 'YEAR', 'Annual temp', 'JFM temp', 'AMJ temp', 'JAS temp', 'OND temp']
    
    #sets index to year for data range from available data
    data.index = list(range(1960, 1960 + len(data.index)))
    
    #deletes unnecessary year columns
    del data['YEAR']
    
    #return final formatted data frame
    return data