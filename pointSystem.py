#-----------------------------------------------------------------------
# pointSystem.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 14/02/2020
# Version: 1.0
#-----------------------------------------------------------------------

#The objective of this code is to evaluate the information retrieved by webscraping and compare it to different parameters and metrics, 
#ultimately giving it a score

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List
from dataScraping import *

def sumList(list1:List[int], totalList = 0) -> int:
	#we need to add all the elements of the list for a total sum
	for element in list1:
		totalList += element
	return totalList	

def ProfitMarginGrowth(RevenuePast5:List[float], NetIncomePast5:List[float]) -> float:
	#we calculate the profit margins year over year for 
	if len(RevenuePast5) >= 2 and len(NetIncomePast5) >= 2:
		if len(RevenuePast5) == len(NetIncomePast5):
			#first we calculate the profit margin of the first year and then the current year
			ProfitMarginStart = NetIncomePast5[0] / RevenuePast5[0] 
			ProfitMarginEnd = NetIncomePast5[-1] / RevenuePast5[-1]
			#Now we calculate the growth if this in all the years and then use a root with the length of years as the exponent the calculate year of year growth
			#to not get complex numbers we separate the positive and negative cases
			ProfitMarginGrowth = (ProfitMarginEnd * 100 / ProfitMarginStart) - 100
			if ProfitMarginGrowth < 0:
				ProfitMarginGrowth = (-1 * ProfitMarginGrowth) ** (1 / len(RevenuePast5))
				ProfitMarginGrowth = -1 * ProfitMarginGrowth
			else:
				ProfitMarginGrowth ** (1 / len(RevenuePast5))	
			return ProfitMarginGrowth
		else:
			#first we calculate the profit margin of the first year and then the current year
			ProfitMarginStart = NetIncomePast5[0] / RevenuePast5[0] 
			ProfitMarginEnd = NetIncomePast5[-1] / RevenuePast5[-1]	
			#Now we calculate the growth from last year to this year
			ProfitMarginGrowth = (ProfitMarginEnd * 100 / ProfitMarginStart) - 100
			return ProfitMarginGrowth
	#if we dont have at least 2 years of info we cannot calculate the growth
	else:
		return -1

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
			print('Not sufficient Data for Assets and Liabilities')		


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

def future(EPSNextY:float, EPSNext5Y:float, estimateRevision1:float, estimateRevision2:float, AverageTarget:float, LowTarget:float, Buy:List[int], Overweight:List[int], Hold:List[int], Underweight:List[int], Sell:List[int], RevenueGrowthNextY:float, Price:float, pointsEarnedFuture = 0, TotalpointsFuture = 0) -> int:
	#We measure differrent values and see if it meets the established parameters, adding points in affirmative cases
	#2 points if earnings growth is over 10 percent and another 3 if it is over 20 percent
	EPSNextY = float(EPSNextY)
	if EPSNextY != -1:
		if EPSNextY > 10:
			print(11)
			pointsEarnedFuture += 2
		if EPSNextY > 20:
			print(12)
			pointsEarnedFuture += 3
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
			pointsEarnedFuture += 3
		TotalpointsFuture += 5
	else:
		print('Not sufficient Data for EPS Next 5 Years')

	#2 points if only one of them is positive and three if both are 
	if estimateRevision1 > 0 or estimateRevision2 > 0:
		if estimateRevision1 <= 0 or estimateRevision2 <= 0:
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
				pointsEarnedFuture += 3
				print(41)
			TotalpointsFuture += 3
		else:
			print('Not sufficient Data for Average Target')	
		if LowTarget != -1:	
			if Price <= LowTarget:
				pointsEarnedFuture += 2
				print(42)
			TotalpointsFuture += 2
		else:
			print('Not sufficient Data for Low Target')		
	else:
		print('Not sufficient Data for Price')

	#2 points if it is over 10 percent and another three if it is over 15 percent
	if RevenueGrowthNextY != -1:
		if RevenueGrowthNextY > 5:
			print(51)
			pointsEarnedFuture += 2
		if RevenueGrowthNextY > 10:
			print(52)
			pointsEarnedFuture += 2	
		if RevenueGrowthNextY > 15:
			print(53)
			pointsEarnedFuture += 1
		TotalpointsFuture += 5

	#we need to know how many votes of each recommendation there is
	numBuy = sumList(Buy)
	numOverweight = sumList(Overweight)
	numHold = sumList(Hold)
	numUnderweight = sumList(Underweight)
	numSell = sumList(Sell)
	#2 points if total of buy and overweight is bigger than the rest, 3 points if it is bigger than 1.5 times the rest
	if numBuy + numOverweight >= numHold + numSell + numUnderweight:
		pointsEarnedFuture += 2
		print(61)
	if numBuy + numOverweight > 1.5 * (numHold + numSell + numUnderweight):
		pointsEarnedFuture += 3	
		print(62)
	TotalpointsFuture += 5	

	print(pointsEarnedFuture)
	print(TotalpointsFuture)

	return pointsEarnedFuture, TotalpointsFuture	

def past(ROA:float, ROE:float, RevenuePast5:List[float], RevenueGrowthPast5:float, EPSpast5:float, EPSgrowthPast5:float, NetIncomePast5:List[float], pointsEarnedPast = 0, TotalpointsPast = 0)	-> int:
	#We measure differrent values and see if it meets the established parameters, adding points in affirmative cases
	#3 points if EPS growth has been over 10 percent and another 2 points if it is over 20 percent
	if EPSgrowthPast5 != -1:
		if EPSgrowthPast5 > 10:
			print(11)
			pointsEarnedPast += 3
		if EPSgrowthPast5 > 20:
			print(12)
			pointsEarnedPast += 2
		TotalpointsPast += 5
	else:
		print('Not sufficient Data for EPS Past 5 Years')	

	##3 points if Revenue growth has been over 10 percent and another 2 points if it is over 20 percent
	if RevenueGrowthPast5 != -1:
		if RevenueGrowthPast5 > 10:
			print(21)
			pointsEarnedPast += 3
		if RevenueGrowthPast5 > 20:
			print(22)
			pointsEarnedPast += 2
		TotalpointsPast += 5
	else:
		print('Not sufficient Data for EPS Past 5 Years')

	#3 points if it is over 20 percent
	ROE = float(ROE)
	if ROE != -1:
		if ROE >= 20:
			print(3)
			pointsEarnedPast += 3
		TotalpointsPast += 3
	else:
		print('Not sufficient Data for Return On Equity')

	#2 points if it is over 5 percent and another one if it is over 10 percent
	ROA = float(ROA)
	if ROA != -1:
		if ROA >= 5:
			pointsEarnedPast += 2
			print(41)
		if ROA >= 10:
			pointsEarnedPast += 1	
			print(42)
		TotalpointsPast += 3
	else:
		print('Not sufficient Data for Return On Assets') 							

	#using a function to calculate the companies profit margins and its growth over the past years
	ProfitMarginsGrowth = ProfitMarginGrowth(RevenuePast5, NetIncomePast5)	
	#3 points if profit margins have grown in the past 5 years and an  additional point if it has grown substantially
	if ProfitMarginsGrowth != -1:
		if ProfitMarginsGrowth > 0:
			print(51)
			pointsEarnedPast += 3
		if ProfitMarginsGrowth > 10:
			print(52)
			pointsEarnedPast += 1	
		TotalpointsPast += 4	
	else:
		print('Not sufficient Data for Profit Margins')	

	print(pointsEarnedPast)
	print(TotalpointsPast)	

	return pointsEarnedPast, TotalpointsPast

def insiders(InsiderTrans:float, InstitutionTrans:float, pointsEarnedInsiders = 0, TotalpointsInsiders = 0) -> int:
	#We measure differrent values and see if it meets the established parameters, adding points in affirmative cases
	#2 points if there has been positive insider transactions
	InsiderTrans = float(InsiderTrans)
	if InsiderTrans != -1:
		if InsiderTrans > 0:
			print(1)
			pointsEarnedInsiders += 2
		TotalpointsInsiders += 2
	else:
		print('Not sufficient Data for Insider Transactions')

	#5 points if institution transactions have been positive and another three if they have been substantial
	InstitutionTrans = float(InstitutionTrans)
	if InstitutionTrans != -1:
		if InstitutionTrans > 0:
			print(21)
			pointsEarnedInsiders += 5
		if InstitutionTrans > 5:
			print(22)
			pointsEarnedInsiders += 3
		TotalpointsInsiders += 8
	else: 
		print('Not sufficient Data for Institution Transactions')					
			
	print(pointsEarnedInsiders)
	print(TotalpointsInsiders)

	return pointsEarnedInsiders, TotalpointsInsiders


def value(PE:float, PEG:float, PS:float, PB:float, YearHighPercent:float, EBITDA:float, LongTermDebt:float, ShortTermDebt:float, FreeCashFlow:float, MarketCap:float, pointsEarnedValue = 0, TotalpointsValue = 0) -> float:
	#We measure differrent values and see if it meets the established parameters, adding points in affirmative cases
	#3 points if PE ratio is under 20 and another 2 if it is under 15 
	PE = float(PE)
	if PE != -1:
		if PE <= 20:
			print(11)
			pointsEarnedValue += 3
		if PE <= 15:
			print(12)
			pointsEarnedValue += 2
		TotalpointsValue += 5
	else:
		print('Not sufficient Data for Price to Earnings Ratio')

	#3 points if PEG ratio is under 1.3 and another 2 if it is under 1 
	PEG = float(PEG)
	if PEG != -1:
		if PEG <= 1.3:
			print(21)
			pointsEarnedValue += 2
		if PEG <= 1:
			print(22)
			pointsEarnedValue += 1
		TotalpointsValue += 5
	else:
		print('Not sufficient Data for Price to Earnings Growth Ratio')

	#3 points if PS ratio is under 1.8 and another 1 if it is under 1 
	PS = float(PS)
	if PS != -1:
		if PS <= 1.8:
			print(31)
			pointsEarnedValue += 2
		if PS <= 1:
			print(32)	
			pointsEarnedValue += 1
		TotalpointsValue += 3
	else:
		print('Not sufficient Data for Price to Sales Ratio')

	#3 points if PE ratio is under 20 and another 2 if it is under 15 
	PB = float(PB)
	if PB != -1:
		if PB <= 3:
			print(41)
			pointsEarnedValue += 2
		if PB <= 1:
			print(42)
			pointsEarnedValue += 1
		TotalpointsValue += 3
	else:
		print('Not sufficient Data for Price to Book Ratio')

	#3 points if golden ratio is under 15 and another 2 if it is under 10
	if EBITDA != -1 and LongTermDebt != -1 and FreeCashFlow != -1 and MarketCap	!= -1:
		GoldenRatio = (MarketCap + LongTermDebt + ShortTermDebt - FreeCashFlow) / EBITDA
		if GoldenRatio <= 15:
			print(51)
			pointsEarnedValue += 3
		if GoldenRatio <= 10:
			print(52)
			pointsEarnedValue += 2
		TotalpointsValue += 5		 		
	else:
		print('Not sufficient Data for Golden Ratio')

	#2 points if it is more than 10 percent of its 52 week high and another one if it is more than 20 percent off
	YearHighPercent = float(YearHighPercent)
	if YearHighPercent != -1:
		if YearHighPercent <= -10:
			print(61)
			pointsEarnedValue += 2
		if YearHighPercent <= -20:
			print(62)
			pointsEarnedValue += 1
		TotalpointsValue += 3
	else:
		print('Not sufficient Data for 52 Week High')	

	#2 stage discounted cash flow			

	print(pointsEarnedValue)
	print(TotalpointsValue)

	return pointsEarnedValue, TotalpointsValue

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

	RevenuePast5, RevenueGrowthPast5, EBITDA, EBIT, DepreciationAmortization, EPSpast5, EPSgrowthPast5, InterestExpense, NetIncomePast5 = IncomeStatementMW(soup2)
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
	print('Health')
	pointsEarnedHealth, TotalpointsHealth = health(DebtEquity, LongTermLiabilities, NetOperatingCashFlow, EBIT, InterestExpense, TotalCurrentAssets, TotalCurrentLiabilities, TotalLiabilities, GrowthLA, TotalEquity, ShortTermDebt, LongTermDebt, TotalDebtReduction, GrowthDA, TotalAssets)
	print()
	print()
	print()
	print('Future')
	pointsEarnedFuture, TotalpointsFuture = future(EPSNextY, EPSNext5Y, estimateRevision1, estimateRevision2, AverageTarget, LowTarget, Buy, Overweight, Hold, Underweight, Sell, RevenueGrowthNextY, Price)
	print()
	print()
	print()
	print('Past')
	pointsEarnedPast, TotalpointsPast = past(ROA, ROE, RevenuePast5, RevenueGrowthPast5, EPSpast5, EPSgrowthPast5, NetIncomePast5)
	print()
	print()
	print()
	print('Insiders')
	pointsEarnedInsiders, TotalpointsInsiders = insiders(InsiderTrans, InstitutionTrans)
	print()
	print()
	print()
	print('Value')
	pointsEarnedValue, TotalpointsValue = value(PE, PEG, PS, PB, YearHighPercent, EBITDA, LongTermDebt, ShortTermDebt, FreeCashFlow, MarketCap)


if __name__ == '__main__': main()