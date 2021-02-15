#-----------------------------------------------------------------------
# recomBarChart.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 12/02/2020
# Version: 1.0
#-----------------------------------------------------------------------

#The objective of the code is to take alll the recommendation info from the datascraping file and visualize it with a bar chart

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List
from dataScraping import *

def mostRatings(Buy:List[int], Overweight:List[int], Hold:List[int], Underweight:List[int], Sell:List[int], columnNames:List[str])	-> int:
	#start off with the first timeframe being the biggest
	numberOfRatings = Buy[0] + Overweight[0] + Hold[0] + Underweight[0] + Sell[0]
	#Check to see which one is the biggest and change te value of the variable if true
	for i in range(len(columnNames)):
		if (Buy[i] + Overweight[i] + Hold[i] + Underweight[i] + Sell[i]) > numberOfRatings:
			numberOfRatings = Buy[i] + Overweight[i] + Hold[i] + Underweight[i] + Sell[i]

	return numberOfRatings		

def main ():
	#First we access to website with an url request
	Ticker = 'sndr'
	url5 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/analystestimates?mod=mw_quote_tab'
	req5 = Request(url5, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded5 = urlopen(req5, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup5 = BeautifulSoup(webpage_coded5, 'html.parser') #Parsing(breaking the code down into relevant info the html code

	#####################################################################################################################################

	#We first get all the necessary info from the dataScraping file
	columnNames, xValues, Buy, Overweight, Hold, Underweight, Sell = Recomendations(soup5)

	#Now we plot all the bars for all the different ratinga from 3m , 1m and current
	for i in range(len(columnNames)):
		#to put one on top of another we must plot the first with a value of the sum of all ratings and reduce it after each bar
		#we chose specific color to make it easier to understand visually
		plt.bar(i + 1, Buy[i] + Overweight[i] + Hold[i] + Underweight[i] + Sell[i], color = (0, 0.5, 0.2), width = 0.3, zorder = 3)
		plt.bar(i + 1, Overweight[i] + Hold[i] + Underweight[i] + Sell[i], color = (0, 0.8, 0.2), width = 0.3, zorder = 3)
		plt.bar(i + 1, Hold[i] + Underweight[i] + Sell[i], color = (0.9, 0.9, 0), width = 0.3, zorder = 3)
		plt.bar(i + 1, Underweight[i] + Sell[i], color = (1, 0.6, 0), width = 0.3, zorder = 4)
		plt.bar(i + 1, Sell[i], color = (0.8, 0, 0), width = 0.3, zorder = 5)

	#we werent able to label before because it was in a for i in range
	#we create empty bars but with the respective labels and colors
	#We also add the values of each rating to give more info	
	plt.bar(0, 0, color = (0, 0.5, 0.2), label = 'Buy   ' + str(Buy), width = 0)	
	plt.bar(0, 0, color = (0, 0.8, 0.2), label = 'Overweight   ' + str(Overweight), width = 0)	
	plt.bar(0, 0, color = (0.9, 0.9, 0), label = 'Hold   ' + str(Hold), width = 0)	
	plt.bar(0, 0, color = (1, 0.6, 0), label = 'Underweight   ' + str(Underweight), width = 0)	
	plt.bar(0, 0, color = (0.8, 0, 0), label = 'Sell   ' + str(Sell), width = 0)	

	#Name the x values with the respective time frames		
	index = np.arange(len(columnNames)) #Gives us an array of evenly spaced numbers in our chosen interval		
	plt.xticks(index + 1, columnNames)

	#We calculate the timeframe with the most amount of ratings and limit the graph to a little above that
	numberOfRatings = mostRatings(Buy, Overweight, Hold, Underweight, Sell, columnNames)
	plt.ylim(0, (1.5 * numberOfRatings) // 1)
	

	plt.legend() #Show labels
	plt.grid(True, 'both', zorder = 0, alpha = 0.5) #show grid, zorder = 0 so that is below all the bars
	plt.suptitle('Analyst Recomendations', weight = 'bold', fontsize = 17) #title in bold and bigger font size
	plt.title('Data from MarketWatch', fontsize = 10)
	plt.xlabel('Timeframes', weight = 'heavy')
	plt.ylabel('Nº of Ratings', weight = 'heavy')

	#Graph bar chart
	plt.show()	



if __name__ == '__main__': main()
