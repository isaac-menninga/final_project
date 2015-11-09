# Climate change and conflict
## Isaac Menninga, Nov. 2015, Quest University Canada

Climate change has many effects on natural systems. Rainfall, humidity, temperature and wind patterns will drastically change into the future. Each of these can affect a variety of things such as crop yield, human health, and infrastructure integrity. These effects will be felt soonest, and in the most extremes in developing countries, where people do not have access to the same infrastructure or technology for crisis response. As the effects of climate change continue to escalate in severity, billions of people may be displaced or unable to cope with the severe changes. The goal of the study is to determine if there is a relationship between climate change and the occurrence of conflict in developing countries. 

The code analyzes data about climate change and conflict in 30 different countries in Africa. Five main variables will be assessed, for each country, to determine their interaction with the occurrence of conflict. These variables are:

Mean temperature
Mean monthly precipitation
The frequency of exceptionally hot days
The frequency of exceptionally cold days
The proportion of rain that falls during heavy rainfall events

Each of these will be compared with the frequency of conflict events in each country. For each comparison, standard statistical methods will be used to determine if the two are correlated. 

The flow of the program is outlined below.

Data formatting and loading - loads climate data for each country, and the data about conflicts for each of those countries. The format for the data is pandas data frame. 
Data analysis - for each climate variable, a simple regression and correlation analysis will be performed. This data will not be visualized at this stage, but instead will be compared between countries to see if the relationship between variables is similar in different countries. One set of tests will also be performed on the combined data from all the countries involved. 
Data visualization - the results from above will be plotted. Most plots will be simple scatter plots, with lines of best fit overlaid. Other data will be visualized to show the variance in the data, and the strength of the correlation, if it exists. Plots will be saved in pdf format.
