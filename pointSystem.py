#-----------------------------------------------------------------------
# pointSystem.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 14/02/2020
# Version: 1.0
#-----------------------------------------------------------------------

#The objective of this code is to retrieve all the necessary information that we need by scraping different
# webpages, so that we can later commence a full stock analysis with this info.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List
from dataScraping import *

def health(DebtEquity:float, LongTermLiabilities:float, NetOperatingCashFlow:float, EBIT:float, InterestExpense:float, TotalCurrentAssets:float, TotalCurrentLiabilities:float, TotalLiabilities:float, GrowthLA:float, TotalEquity:float, ShortTermDebt:float, LongTermDebt:float, TotalDebtReduction:float, GrowthDA:float, TotalAssets:float, TotalpointsHealth = 0, pointsEarnedHealth = 0) -> int:
	#We evaluate each parameter and add points if it meets the criteria
	#2 points if it is below 0.8 and 3 if it is below 0.4
	DebtEquity = float(DebtEquity)
	if DebtEquity == -1:
		#to redefinde Debt/Equity Ratio first we must make sure that total equity is not zero so that we dont have an error
		if TotalEquity != -1:
			DebtEquity = (LongTermDebt + ShortTermDebt) / TotalEquity
	#We check to see if it is correct, redefined or not
	if DebtEquity != -1:
		if DebtEquity <= 0.4:
			pointsEarnedHealth += 5
			print(11)
		elif 0.4 < DebtEquity <= 0.8:
			pointsEarnedHealth += 3
			print(12)
		TotalpointsHealth += 5		
	else:
		print('Not sufficient Data for Debt/Equity Ratio')

	#3 Points if EBIT covers 33% of Interest Expense
	if EBIT != -1:
		#Calculate ratio
		RatioLE = InterestExpense / EBIT
		if RatioLE <= 0.33:
			pointsEarnedHealth += 2
			print(2)
		TotalpointsHealth += 2
	else:
		print('Not sufficient Data for EBIT and Interest Expense')	

	#3 points if free cash flow covers half of total liabilities and 2 points if it covers all if it
	if NetOperatingCashFlow != -1 and LongTermDebt != -1:
		#Calculate ratio
		RatioFD = NetOperatingCashFlow / (LongTermDebt + ShortTermDebt)
		if RatioFD >= 1:
			pointsEarnedHealth += 5
			print(31)
		elif 0.5 <= RatioFD < 1:
			pointsEarnedHealth += 3
			print(32)
		elif 0.25 <= RatioFD < 0.5:
			pointsEarnedHealth += 1
			print(33)	
		TotalpointsHealth += 5
	else:
		print('Not sufficient Data for Net Operating Cash Flow and Total Liabilities')		

	if TotalCurrentAssets != -1 and TotalCurrentLiabilities != -1:
		#Calculate Ratio
		RatioLA = TotalCurrentLiabilities / TotalCurrentAssets	
		if RatioLA < 1:
			pointsEarnedHealth += 3
			print(4)
		TotalpointsHealth += 3
	else:
		print('Not sufficient Data for Total Current Assets and Total Current Liabilities')		

	#3 points if current assets is equal or bigger than long term liabilities and 2 points if it at most 25% smaller
	if TotalCurrentAssets != -1 and LongTermLiabilities != -1:
		#Calculate Ratio
		RatioLA2 = LongTermLiabilities / TotalCurrentAssets
		if RatioLA2 <= 1:
			pointsEarnedHealth += 5
			print(51)
		elif 1 < RatioLA2 <= 1.25:
			pointsEarnedHealth += 2
			print(52)
		TotalpointsHealth += 5	
	else:
		print('Not sufficient Data for Total Current Assets and Long Term Liabilities')	

	#In case that previous two measurements dont work we use another one with similar parameters but less importance
	#2 points if assets cover liabilities and equity	
	if TotalCurrentAssets == -1 or TotalCurrentLiabilities == -1 or LongTermLiabilities == -1:
		if TotalAssets != -1 and TotalLiabilities != -1:
			RatioLA3 = (TotalLiabilities + TotalEquity) / TotalAssets
			if RatioLA3 > 1:
				print(54)
				pointsEarnedHealth += 2
			TotalpointsHealth += 2
		else:
			print('Not sufficient Data for Total Assets and Total Liabilities')		


	#2 points if liabilities/assets ratio has been reduced in the last few years	
	if GrowthLA != -1:
		if GrowthLA < 0:
			pointsEarnedHealth += 2
			print(61)
		TotalpointsHealth += 2
	else:
		#if the LA ratio isnt available we opt for the DA ratio
		#2 points if debt/assets ratio has reduced in the last few years
		if GrowthDA != -1:
			if GrowthDA < 0:
				pointsEarnedHealth += 2
				print(62)
		TotalpointsHealth += 2
		if GrowthDA == 0:
			print('Not sufficient Data for Liabilities/Assets Ratio Growth or Debt/Assets Ratio Growth')

	#3 points if there has been debt reduction over the past 5 yearss
	if TotalDebtReduction != -1:
		if TotalDebtReduction < 0:
			pointsEarnedHealth += 3
			print(7)
		TotalpointsHealth += 3
	else:
		print('Not sufficient Data for Debt Reduction')			
	
	print(pointsEarnedHealth)
	print(TotalpointsHealth)

	return pointsEarnedHealth, TotalpointsHealth	

def future(EPSNextY:float, EPSNext5Y:float, estimateRevision1:float, estimateRevision2:float, AverageTarget:float, LowTarget:float, Buy:List[int], Overweight:List[int], Hold:List[int], Underweight:List[int], Sell:List[int], RevenueGrowthNextY:float, Price:float, pointsEarnedFuture = 0, TotalpointsFuture = 0) -> float:
	#We measure differrent values and see if it meets the established parameters, adding points in affirmative cases
	#2 points if earnings growth is over 10 percent and another 3 if it is over 20 percent
	EPSNextY = float(EPSNextY)
	if EPSNextY != -1:
		if EPSNextY > 10:
			print(11)
			pointsEarnedFuture += 2
		if EPSNextY > 20:
			print(12)
			TotalpointsFuture += 3
		TotalpointsFuture += 5
	else:
		print('Not sufficient Data for EPS Next Year')

	#2 points if earnings growth is over 10 percent and another 3 if it is over 20 percent
	EPSNext5Y = float(EPSNext5Y)
	if EPSNext5Y != -1:
		if EPSNext5Y > 10:
			print(21)
			pointsEarnedFuture += 2
		if EPSNext5Y > 20:
			print(22)
			TotalpointsFuture += 3
		TotalpointsFuture += 5
	else:
		print('Not sufficient Data for EPS Next 5 Years')

	#2 points if only one of them is positive and three if both are 
	if estimateRevision1 > 0 or estimateRevision2 > 0:
		if estimateRevision1 <= 0:
			pointsEarnedFuture += 2
			print(31)
		elif estimateRevision2 <= 0:
			pointsEarnedFuture += 2
			print(31)
		else:
			print(32)
			pointsEarnedFuture += 3
	TotalpointsFuture += 3

	#2 points if price is lower than average target by analysts and 3 points if it is lower than low target by analysts
	Price = float(Price)
	if Price != -1:
		if AverageTarget != -1:
			if Price < AverageTarget:
				pointsEarnedFuture += 2
				print(41)
			TotalpointsFuture += 2
		else:
			print('Not sufficient Data for Average Target')	
		if LowTarget != -1:	
			if Price < LowTarget:
				pointsEarnedFuture += 3
				print(42)
			TotalpointsFuture += 3
		else:
			print('Not sufficient Data for Low Target')		
	else:
		print('Not sufficient Data for Price')

	#
	if RevenueGrowthNextY != -1:
		if RevenueGrowthNextY > 10:
			print(51)
			pointsEarnedFuture += 2
		if RevenueGrowthNextY > 15:
			print(52)
			TotalpointsFuture += 3
		TotalpointsFuture += 5


			

	print(pointsEarnedFuture)
	print(TotalpointsFuture)

	return pointsEarnedFuture, TotalpointsFuture				

			







def  main ():

	Ticker = str(input('Ticker: '))
	url1 = 'http://finviz.com/quote.ashx?t=' + Ticker
	req1 = Request(url1, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded1 = urlopen(req1, timeout = 4).read() #We open the page and read all the raw info
   	#webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup1 = BeautifulSoup(webpage_coded1, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

	url2 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/financials'
	req2 = Request(url2, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded2 = urlopen(req2, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded2 = webpage_coded2.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup2 = BeautifulSoup(webpage_coded2, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

	url3 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/financials/balance-sheet'
	req3 = Request(url3, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded3 = urlopen(req3, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup3 = BeautifulSoup(webpage_coded3, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

	url4 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/financials/cash-flow'
	req4 = Request(url4, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded4 = urlopen(req4, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup4 = BeautifulSoup(webpage_coded4, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ###################################################################################################################################################

	url5 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/analystestimates?mod=mw_quote_tab'
	req5 = Request(url5, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded5 = urlopen(req5, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup5 = BeautifulSoup(webpage_coded5, 'html.parser') #Parsing(breaking the code down into relevant info) the html code
	
	#####################################################################################################################################################

	url6 = 'https://finance.yahoo.com/quote/' + Ticker + '/analysis?p=' + Ticker
	req6 = Request(url6, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded6 = urlopen(req6, timeout = 4).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup6 = BeautifulSoup(webpage_coded6, 'html.parser') #Parsing(breaking the code down into relevant info) the html code


	PE, PEG, PS, PB, MarketCap, DebtEquity, Recom, InsiderTrans, InstitutionTrans, ROA, ROE, AvgVolume, Price, LastChange, PerfWeek, PerfMonth, PerfYear, YearHighPercent, EPSNextY, EPSNext5Y = fundamentalInfoFVZ(soup1)

	RevenuePast5, RevenueGrowthPast5, EBITDA, EBIT, DepreciationAmortization, EPSpast5, EPSgrowthPast5, InterestExpense = IncomeStatementMW(soup2)
	TotalEquity, GrowthLA, GrowthDA, TotalLiabilities, TotalCurrentLiabilities, LongTermLiabilities, TotalAssets, TotalCurrentAssets, LongTermAssets, ShortTermDebt, LongTermDebt = BalanceSheet(soup3)
	FreeCashFlow, TotalDebtReduction, NetOperatingCashFlow = CashFlow(soup4)

	estimateRevision1, estimateRevision2 = EPSRevisions(soup5)
	HighTarget, LowTarget, AverageTarget, NumberOfRatings = PriceTargets(soup5)

	EPSestimates = EPSEstimates(soup5)
	RevenueGrowthNextY = RevenuesEstimates(soup6)

	columnNames, xValues, Buy, Overweight, Hold, Underweight, Sell = Recomendations(soup5)

    ############################################################################################################################################
    ############################################################################################################################################
    ############################################################################################################################################

	pointsEarnedHealth, TotalpointsHealth = health(DebtEquity, LongTermLiabilities, NetOperatingCashFlow, EBIT, InterestExpense, TotalCurrentAssets, TotalCurrentLiabilities, TotalLiabilities, GrowthLA, TotalEquity, ShortTermDebt, LongTermDebt, TotalDebtReduction, GrowthDA, TotalAssets)
	print()
	print()
	print()
	future(EPSNextY, EPSNext5Y, estimateRevision1, estimateRevision2, AverageTarget, LowTarget, Buy, Overweight, Hold, Underweight, Sell, RevenueGrowthNextY, Price)



if __name__ == '__main__': main()