# Isaac Menninga, 2015

#import dependencies
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm, scipy.stats.stats as stats

def main():
	#list of each country in data set
	country_list = ['Angola', 'Benin', 'Cameroon', 'Chad', 'Equatorial_Guinea', 'Eritrea', 'Gabon', 'Gambia', 'Ghana', 'Liberia', 'Malawi', 'Mali', 'Morocco', 'Mozambique', 'Senegal', 'Sierra_Leone', 'Tanzania', 'Togo', 'Uganda', 'Zambia']
	
	#initialize data frame to store results for each country
	pearson_results = pd.DataFrame(columns = ['country', 'precip', 'f_rain', 'f_cold', 'f_heat'])
	spearman_results = pd.DataFrame(columns = ['country', 'precip', 'f_rain', 'f_cold', 'f_heat'])
	
	#initialize data frame to store results for each country
	pearson_results = pd.DataFrame(columns = ['country', 'precip', 'f_rain', 'f_cold', 'f_heat'])
	spearman_results = pd.DataFrame(columns = ['country', 'precip', 'f_rain', 'f_cold', 'f_heat'])
	
	for country in country_list:
		#load data on country
		data = load_data(country)
		#conduct statistical analysis
		pearson_results = pearson_results.append(pearson_correlation(data, country), ignore_index = True)
		spearman_results = spearman_results.append(spearman_correlation(data, country), ignore_index = True)
		
	#make plots
	for variable in ['precip', 'f_rain', 'f_cold', 'f_heat']:
		make_plot(data[variable], data.Year, '../results/' + variable + '_over_time.pdf')
	
	#make table containing results
	make_stats_table(pearson_results, spearman_results)
	

def load_conflict_data(country_name):
	'''This function is used to grab data on conflict occurances in a specific country. 
	The function takes one input, which is the name of the country you want to grab data for. Returns the data as a pandas data frame.'''
	
	#path is a string containing the path for the data files
	path = "../data/ACLED/" + country_name + '.xlsx'

	#read from excel file
	data = pd.read_excel(path)

	#only return necessary columns
	data = data[['YEAR', 'EVENT_TYPE', 'ACTOR1', 'LOCATION', 'FATALITIES']]
	data.columns = ['Year', 'Event_type', 'Actor', 'Location', 'Fatalities']
	data['Count'] = 1
	
	return data

def load_climate_data(country_name):
	'''This function is used to grab data on climate for each country.
	The function takes one input, which is the name of the country to grab data on. The function returns the data as a pandas data frame.'''
	
	#extreme filename is a dictionary containing the file extension corresponding to each variable for extreme weather patterns
	extremes_filename = {'f_extreme_heat' : 'TX90p.csiro_mk3_0.abs.txt', 'f_extreme_cold' : 'TX10p.csiro_mk3_0.abs.txt', 'f_heavy_rain' : 'R95pct.csiro_mk3_0.anom.txt'}

	#mean filename is a dictionary containing the file extension corresponding to each variable for mean temperature and precipitation
	mean_filename = {'temperature' : 'temp.csiro_mk3_5.anom.txt', 'precipitation' : 'precip.csiro_mk3_5.anom.txt'}

	#contains the file path for each group of variables
	#Extremes/... contains data on extreme weather, Mean/... contains mean temperature and precipitation data
	directories = ['/Model/Extremes/Timeseries/', '/Model/Mean/Timeseries/Anomalies/']
	
	#initializes data frame
	data = pd.DataFrame()
	
	# for each group of variables
	for directory in directories:
		# if the data is for extremes, iterate over extremes_variables and gets the final path for each file to grab
		if directory == '/Model/Extremes/Timeseries/':
			
			#gets the variable name from a list of variables
			#each variable corresponds to the end of the name of the file
			for file in extremes_filename:
				#variable for column names
				colnames = ['Year', 'Annual_' + file, 'JFM_' + file, 'AMJ_' + file, 'JAS_' + file, 'OND_' + file]
				
				#path is equal to the file path for the data file containing data on the current variable
				#concatonates country name, directory names and file names to form the specific file path
				path = '../data/climate/' + country_name + directory + country_name + '.ts.' + extremes_filename[file]
				
				#if the data frame is empty, set data equal to the contents of the first file
				if data.empty:
					data = pd.read_table(path, delimiter = '\s+', header = None, names = colnames, skiprows = 15, nrows = 120, error_bad_lines = True, index_col='Year')
					
				#if the data frame is not empty, concatonate the data from the second file to the first
				else:
					data_2 = pd.read_table(path, delimiter = '\s+', header = None, names = colnames, skiprows = 15, nrows = 120, error_bad_lines = True, index_col='Year')
					#data_2 = data_2.reset_index()
					#data = data.reset_index(drop = True)
					data = data.join(data_2)   

		# if the data is for means, iterate over mean_variables and get the final path for each data file
		elif directory == '/Model/Mean/Timeseries/Anomalies/':
			
			#gets the variable name from a list of variables
			#each variable corresponds to the end of the name of the file
			for file in mean_filename:
				#for column names
				colnames = ['Year', 'Annual_' + file, 'JFM_' + file, 'AMJ_' + file, 'JAS_' + file, 'OND_' + file]
				
				#path is equal to the file path for the data file containing data on the current variable
				#concatonates country name, directory names and file names to form the specific file path
				path = '../data/climate/' + country_name + directory + country_name + '.ts.' + mean_filename[file]
				
				#if the data frame is empty, set data equal to the contents of the first file
				if data.empty:
					data = pd.read_table(path, delimiter = '\s+', header = None, names = colnames, skiprows = 15, nrows = 120, error_bad_lines = True, index_col='Year')
					
				#if the data frame is not empty, concatonate the data from the second file to the first
				else:
					data_2 = pd.read_table(path, delimiter = '\s+', header = None, names = colnames, skiprows = 15, nrows = 120, error_bad_lines = True, index_col='Year')
					#data_2 = data_2.reset_index()
					#data = data.reset_index(drop = True)
					data = data.join(data_2)
	
	#reduces the size of the data
	data = data[['Annual_f_extreme_cold', 'Annual_f_extreme_heat', 'Annual_f_heavy_rain', 'Annual_precipitation', 'Annual_temperature']]
	
	#drop nan rows
	data = data.dropna()
	
	#drop the last row (inelegant solution to a problem!)
	data = data.drop(data.tail(1).index)
	
	#return final formatted data frame
	return data

def load_data(current_country):
	'''This function loads and munges data into a pandas data frame. 
	
	Usage: load_data(list_of_countries_to_load)'''
	
	#load data on climate for the country
	climate_data = load_climate_data(current_country)
	#load data on conflict in the country
	conflict_data = load_conflict_data(current_country)

	#create smaller data set to work with
	climate_small_data = climate_data[['Annual_precipitation', 'Annual_f_heavy_rain', 'Annual_f_extreme_cold', 'Annual_f_extreme_heat']]
	conflict_small_data = conflict_data[['Fatalities', 'Year', 'Count']]

	#rename columns
	climate_small_data.columns = ['precip', 'f_rain', 'f_cold', 'f_heat']

	#group conflict data by year
	conflict_small_data = conflict_small_data.groupby('Year').sum()

	#make indices the same type for merging
	#reset index to make 'Year' a column not an index
	conflict_small_data = conflict_small_data.reset_index().astype(float)
	climate_small_data = climate_small_data.reset_index().astype(float)

	# Generate predicted values for missing climate data from 2000 - 2046
	# Initialize data frame
	data_pred = pd.DataFrame()
	#iterate for each column
	for column in climate_small_data.columns:
		#linear regression for each column variable
		if column != 'Year':
			#linear model
			lm = sm.formula.ols(formula = column + " ~ Year", data = climate_small_data).fit()

			#range of missing date values
			xnew = pd.DataFrame({'Year' : range(2001, 2046)})

			#predict missing values for column variable
			y_pred = lm.predict(xnew)

			#create data frame from predicted values
			y_pred_df = pd.DataFrame({'Year' : range(2001, 2046), column : y_pred})

			#merge data into initialized data frame
			if data_pred.empty:
				data_pred = y_pred_df
			else:
				data_pred = data_pred.merge(y_pred_df)

	#concatenate the predicted values into previous data frame
	climate_small_data = pd.concat([climate_small_data, data_pred]).sort_values('Year')

	#merge the data, and drop Nan to get overlapping data
	final_data = climate_small_data.merge(conflict_small_data, how = 'outer').dropna()

	return final_data

def pearson_correlation(data, country):
	'''This function calculates Pearson's correlation for an input data set. 
	Usage: pearson_correlation(dataframe, country_name)
	
	Output: series containing the results for the test, for each variable.'''
	#initializes series to store results from Pearson's correlation test
	pearson_coefficient = pd.Series(index = ['country', 'precip', 'f_rain', 'f_cold', 'f_heat'])
	pearson_coefficient['country'] = country
	
	#for each x-variable
	for column in data:
		if (column != 'Year') & (column != 'Fatalities') & (column != 'Count'):
			#conduct statistical test of current variable vs. conflicts/year
			pearson = stats.pearsonr(data[column], data.Count)
			#put results in initialized results array
			pearson_coefficient[column] = pearson
			
	return pearson_coefficient

def spearman_correlation(data, country):
	'''This function calculates Spearman's rank correlation for an input data set. 
	Usage: spearman_correlation(dataframe, country_name)
	
	Output: series containing the results for the test, for each variable.'''
	#initializes series to store results from Spearman's rank correlation
	spearman_coefficient = pd.Series(index = ['country', 'precip', 'f_rain', 'f_cold', 'f_heat'])
	spearman_coefficient['country'] = country
	
	#for each x-variable
	for column in data:
		if (column != 'Year') & (column != 'Fatalities') & (column != 'Count'):
			#conduct statistical test of current variable vs. conflicts/year
			spearman = stats.spearmanr(a = data[column], b = data.Count)
			#put results in initialized results array
			spearman_coefficient[column] = spearman
			
	return spearman_coefficient

def munge_results(coefficient_data, column):
	'''This function compiles the results for a statistical test into a workable data frame.
	Usage: munge_results(dataframe, variable_name)
	
	output: dataframe containing reformatted results from statistical tests. '''
	
	#initialize data frame to store mean results of each statistical test
	coefficients = pd.DataFrame()
	
	#for each country in data set
	for country in coefficient_data['country']:
		# creates a variable containing values for a row
		row = tuple(coefficient_data[coefficient_data.country == country][column])
		#adds row to data frame
		coefficients[country] = row[0]
	
	#transposes data frame to make country name the index, and 'coefficient' and 'p_value' columns
	coefficients = coefficients.T
	coefficients.columns = ['coefficient', 'p_value']
	
	return coefficients

def make_stats_table(pearson_data, spearman_data):
	'''This function takes results for each statistical test and finds the mean of the results from all countries. Inputs are data frames containing the results from each statistical test.
	
	Usage: stats_table(pearson_results, spearman_results)
	
	Output: saved file containing the mean of the results from the statistical tests. '''

	#initializes column names for results data frame
	mean_results = pd.DataFrame(columns = ['variable', 'pearson_coefficient', 'pearson_p_value', 'spearman_coefficient', 'spearman_p_value'])
	
	#for each variable in results table
	for column in pearson_data:
		if column != 'country':
			#munge results to get p_value and coefficient values separately
			munged_pearson = munge_results(pearson_data, column).mean()
			munged_spearman = munge_results(spearman_data, column).mean()
			
			#construct a row from the results for the current variable
			new_row = pd.DataFrame({'variable' : [column], 'pearson_coefficient' : [munged_pearson[0]], 'pearson_p_value' : [munged_pearson[1]],
								   'spearman_coefficient' : [munged_spearman[0]], 'spearman_p_value' : [munged_spearman[1]]})
			#append row to results data frame
			mean_results = mean_results.append(new_row, ignore_index = True)
	
	#sets index to variable
	mean_results.index = mean_results.variable
	#deletes variable column
	del mean_results['variable']
	#saves the table
	mean_results.to_csv('../results/correlation_results.csv')

def make_plot(y, x, filename):
	'''This function creates line plots from x and y inputs and saves them to file.'''

	#initialize plot
	plt.plot(x, y)
	
	#label names equal to the input variables
	plt.xlabel(x.name)
	plt.ylabel(y.name)
	
	#save figure to results directory
	plt.savefig(filename)
	
	plt.close()
	
main()