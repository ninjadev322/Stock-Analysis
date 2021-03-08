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

def prices(soup) -> float:
	# We inspect the webpage to finde the html tags of the pbjects that we want
	# Transforms the html to a pandas dataframe
	check = True
	try:
		fundamentals = pd.read_html(str(soup), attrs={'class': 'snapshot-table2'})[0]  # Can only do this if class type is a table
	except:
		check = False

	if check:
		price = fundamentals[11][10]
		if price == '-':
			price = -1

	return price			

def main ():
	check = True
	try:
		Ticker = str(input('Ticker: '))
		#First we access to website with an url request
		url5 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/analystestimates?mod=mw_quote_tab'
		req5 = Request(url5, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
		webpage_coded5 = urlopen(req5, timeout = 1).read() #We open the page and read all the raw info
    	#webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

		soup5 = BeautifulSoup(webpage_coded5, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

		#####################################################################################################################################

		url2 = 'http://finviz.com/quote.ashx?t=' + Ticker
		req2 = Request(url2, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
		webpage_coded2 = urlopen(req2, timeout = 4).read() #We open the page and read all the raw info
	    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

		soup2 = BeautifulSoup(webpage_coded2, 'html.parser') #Parsing(breaking the code down into relevant info the html code

		#####################################################################################################################################

	except:
		#tell the user that we cannot analize this ticker
		print('Not sufficient Data for this Ticker...')
		check = False


	if check:
		#retrieves all the info and data we need for the chart
		HighTarget, LowTarget, AverageTarget, NumberOfRatings = PriceTargets(soup5)
		price = prices(soup2)
		price = float(price)

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
		plt.get_current_fig_manager().window.setGeometry(0, 220, 400, 290)
		plt.show()	









if __name__ == '__main__': main()