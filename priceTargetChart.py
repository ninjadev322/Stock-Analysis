#-----------------------------------------------------------------------
# priceTargetChart.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 08/03/2020
# Version: 1.0
#-----------------------------------------------------------------------

#The objective of the code is to take alll the recommendation info from the datascraping file and visualize it with a bar chart

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List
from dataScraping import *	

def PTchart(Ticker:str, price:float, HighTarget:float, LowTarget:float, AverageTarget:float, NumberOfRatings:float):
	#retrieves all the info and data we need for the chart 
	price = float(price)

	if price != -1 and HighTarget != -1 and AverageTarget != -1 and LowTarget != -1:
		#we plot a line with the target and then plot a point with just the price
		plt.plot([LowTarget, AverageTarget, HighTarget], [1, 1, 1], color = (0, 0, 0.5), marker = '|', markersize = 15, linewidth = 1.5)
		plt.plot(price, 1, color = (0.8, 0, 0), marker = 'o')

		#set the size for the labels on both tick axis
		plt.tick_params(axis = 'both', which = 'both', labelsize = 5)

		for a, b in zip([LowTarget, AverageTarget, HighTarget], [1, 1, 1]):
			plt.text(a * 0.975, b * 1.01, str(a), fontsize = 5)
		plt.text(price * 0.975, 1.005, str(price), fontsize = 5)	

		#plt.legend(fontsize = 5) #Show labels
		plt.grid(True, 'both', zorder = 0, alpha = 0.5) #show grid, zorder = 0 so that is below all the bars
		plt.suptitle('Analyst Price Targets', weight = 'bold', fontsize = 9) #title in bold and bigger font size
		plt.title('Data from MarketWatch  (Ticker: ' + Ticker.upper() + ')', fontsize = 5)
		plt.xlabel('Price', weight = 'heavy', fontsize = 7, labelpad = 2)
		plt.ylabel('')

		#Graph bar chart
		plt.get_current_fig_manager().window.setGeometry(640, -35, 325, 300)
		#plt.show()	

	else:
		print('Not sufficient Data for Analyst Price Targets')	

