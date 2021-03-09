#-----------------------------------------------------------------------
# revenueEarningsChart.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 06/03/2020
# Version: 1.0
#-----------------------------------------------------------------------

#The objective of the code is to take alll the recommendation info from the datascraping file and visualize it with a bar chart

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List
from dataScraping import *

def shares(soup, sharesOutstanding = -1)-> float:
	# We inspect the webpage to finde the html tags of the pbjects that we want
    # Transforms the html to a pandas dataframe
    check = True
    try:
        fundamentals = pd.read_html(str(soup), attrs={'class': 'snapshot-table2'})[0]  # Can only do this if class type is a table
    except:
        check = False

    if check:
    	sharesOutstanding = fundamentals[9][0]
    	if sharesOutstanding == '-':
    		sharesOutstanding = -1
    	else:
    		if sharesOutstanding[-1] == 'B':
    			sharesOutstanding = float(sharesOutstanding[0:-1]) * 1000000000
    		elif sharesOutstanding[-1] == 'M':
    			sharesOutstanding = float(sharesOutstanding[0:-1]) * 1000000
    		elif sharesOutstanding[-1] == 'K':
    			sharesOutstanding = float(sharesOutstanding[0:-1]) * 1000		

    return sharesOutstanding		

def year(soup, years = []) -> List[str]:
	# We inspect the webpage to finde the html tags of the pbjects that we want
    # Transforms the html to a pandas dataframe
    check = True
    try:
        IncomeStatement = pd.read_html(str(soup), attrs={'class': 'table table--overflow align--right'})[0]  # Can only do this if class type is a table
    except:
        check = False

    if check:   
    	#if we can access it we take all the columns that are years to see the timeframe for the data
    	years = IncomeStatement.columns[1:-1]

    return years	
    	
def REchart(Ticker:str, RevenuePast5:List[float], NetIncomePast5:List[float], soup1, soup2):
	#retrieves all the info and data we need for the chart
	years = year(soup1)
	sharesOutstanding = shares(soup2)

	if len(RevenuePast5) != 0 and len(NetIncomePast5) != 0 and sharesOutstanding != -1:
		#Now we plot all the bars for all the different ratinga from 3m , 1m and current
		for i in range(len(years)):
			#to put one on top of another we must plot the first with a value of the sum of all ratings and reduce it after each bar
			#we chose specific color to make it easier to understand visually
			plt.bar(i + 1, RevenuePast5[i], color = (0, 0.75, 0), width = 0.3, zorder = 3)
			plt.bar(i + 1.3, NetIncomePast5[i], color = (0, 0, 1), width = 0.3, zorder = 3)

		#we werent able to label before because it was in a for i in range
		#we create empty bars but with the respective labels and colors
		#We also add the values of each rating to give more info	
		plt.bar(0, 0, color = (0, 0.8, 0), label = 'Revenue', width = 0)	
		plt.bar(0, 0, color = (0, 0, 1), label = 'Earnings', width = 0)		

		#Name the x values with the respective time frames		
		index = np.arange(len(years)) #Gives us an array of evenly spaced numbers in our chosen interval		
		plt.xticks(index + 1, years)

		#We calculate the timeframe with the most amount of ratings and limit the graph to a little above that
		#numberOfRatings = mostRatings(Buy, Overweight, Hold, Underweight, Sell, columnNames)
		#plt.ylim(0, (1.5 * numberOfRatings) // 1)

		#set the size for the labels on both tick axis
		plt.tick_params(axis = 'both', which = 'both', labelsize = 5)

		plt.legend(fontsize = 5) #Show labels
		plt.grid(True, 'both', zorder = 0, alpha = 0.5) #show grid, zorder = 0 so that is below all the bars
		plt.suptitle('Past Revenue and Earnings', weight = 'bold', fontsize = 9) #title in bold and bigger font size
		plt.title('Data from MarketWatch  (Ticker: ' + Ticker.upper() + ')', fontsize = 5)
		plt.xlabel('Years', weight = 'heavy', fontsize = 7, labelpad = 2)
		plt.ylabel('$$$', weight = 'heavy', fontsize = 7, labelpad = 2)

		#Graph bar chart
		plt.get_current_fig_manager().window.setGeometry(315, -35, 325, 300)
		#plt.show()

	else:
		print('Not sufficient Data for Revenue and Net Income for past 5 Years')		

