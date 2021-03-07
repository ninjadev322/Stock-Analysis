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
		TotalEquity = float(TotalEquity)
		if TotalEquity != -1:
			DebtEquity = (LongTermDebt + ShortTermDebt) / TotalEquity
	#We check to see if it is correct, redefined or not
	if DebtEquity != -1:
		if DebtEquity <= 0.4:
			pointsEarnedHealth += 5
		elif 0.4 < DebtEquity <= 0.8:
			pointsEarnedHealth += 3
		TotalpointsHealth += 5

	#3 Points if EBIT covers 33% of Interest Expense
	if EBIT != -1:
		#Calculate ratio
		if EBIT != 0:
			RatioLE = InterestExpense / EBIT
			if RatioLE <= 0.33:
				pointsEarnedHealth += 2
			TotalpointsHealth += 2
		else:
			TotalpointsHealth += 2	

	#3 points if free cash flow covers half of total liabilities and 2 points if it covers all if it
	if NetOperatingCashFlow != -1 and LongTermDebt != -1:
		#Calculate ratio
		if LongTermDebt + ShortTermDebt != 0:
			RatioFD = NetOperatingCashFlow / (LongTermDebt + ShortTermDebt)
			if RatioFD >= 1:
				pointsEarnedHealth += 5
			elif 0.5 <= RatioFD < 1:
				pointsEarnedHealth += 3
			elif 0.25 <= RatioFD < 0.5:
				pointsEarnedHealth += 1
			TotalpointsHealth += 5
		else:
			pointsEarnedHealth += 5
			TotalpointsHealth += 5	

	if TotalCurrentAssets != -1 and TotalCurrentLiabilities != -1:
		#Calculate Ratio
		RatioLA = TotalCurrentLiabilities / TotalCurrentAssets
		if RatioLA < 1:
			pointsEarnedHealth += 3
		TotalpointsHealth += 3

	#3 points if current assets is equal or bigger than long term liabilities and 2 points if it at most 25% smaller
	if TotalCurrentAssets != -1 and LongTermLiabilities != -1:
		#Calculate Ratio
		RatioLA2 = LongTermLiabilities / TotalCurrentAssets
		if RatioLA2 <= 1:
			pointsEarnedHealth += 5
		elif 1 < RatioLA2 <= 1.25:
			pointsEarnedHealth += 2
		TotalpointsHealth += 5

	#In case that previous two measurements dont work we use another one with similar parameters but less importance
	#2 points if assets cover liabilities and equity
	if TotalCurrentAssets == -1 or TotalCurrentLiabilities == -1 or LongTermLiabilities == -1:
		if TotalAssets != -1 and TotalLiabilities != -1:
			RatioLA3 = (TotalLiabilities + TotalEquity) / TotalAssets
			if RatioLA3 > 1:
				pointsEarnedHealth += 2
			TotalpointsHealth += 2


	#2 points if liabilities/assets ratio has been reduced in the last few years
	if GrowthLA != -1:
		if GrowthLA < 0:
			pointsEarnedHealth += 2
		TotalpointsHealth += 2
	else:
		#if the LA ratio isnt available we opt for the DA ratio
		#2 points if debt/assets ratio has reduced in the last few years
		if GrowthDA != -1:
			if GrowthDA < 0:
				pointsEarnedHealth += 2
		TotalpointsHealth += 2

	#3 points if there has been debt reduction over the past 5 yearss
	if TotalDebtReduction != -1:
		if TotalDebtReduction < 0:
			pointsEarnedHealth += 3
		TotalpointsHealth += 3

	return pointsEarnedHealth, TotalpointsHealth

def future(EPSNextY:float, EPSNext5Y:float, estimateRevision1:float, estimateRevision2:float, AverageTarget:float, LowTarget:float, Buy:List[int], Overweight:List[int], Hold:List[int], Underweight:List[int], Sell:List[int], RevenueGrowthNextY:float, Price:float, pointsEarnedFuture = 0, TotalpointsFuture = 0) -> int:
	#We measure differrent values and see if it meets the established parameters, adding points in affirmative cases
	#2 points if earnings growth is over 10 percent and another 3 if it is over 20 percent
	EPSNextY = float(EPSNextY)
	if EPSNextY != -1:
		if EPSNextY > 10:
			pointsEarnedFuture += 2
		if EPSNextY > 20:
			pointsEarnedFuture += 3
		TotalpointsFuture += 5

	#2 points if earnings growth is over 10 percent and another 3 if it is over 20 percent
	EPSNext5Y = float(EPSNext5Y)
	if EPSNext5Y != -1:
		if EPSNext5Y > 10:
			pointsEarnedFuture += 2
		if EPSNext5Y > 20:
			pointsEarnedFuture += 3
		TotalpointsFuture += 5

	#2 points if only one of them is positive and three if both are
	if estimateRevision1 > 0 or estimateRevision2 > 0:
		if estimateRevision1 <= 0 or estimateRevision2 <= 0:
			pointsEarnedFuture += 2
		else:
			pointsEarnedFuture += 3
	TotalpointsFuture += 3

	#2 points if price is lower than average target by analysts and 3 points if it is lower than low target by analysts
	Price = float(Price)
	if Price != -1:
		if AverageTarget != -1:
			if Price < AverageTarget:
				pointsEarnedFuture += 3
			TotalpointsFuture += 3
		if LowTarget != -1:
			if Price <= LowTarget:
				pointsEarnedFuture += 2
			TotalpointsFuture += 2

	#2 points if it is over 10 percent and another three if it is over 15 percent
	if RevenueGrowthNextY != -1:
		if RevenueGrowthNextY > 5:
			pointsEarnedFuture += 2
		if RevenueGrowthNextY > 10:
			pointsEarnedFuture += 2
		if RevenueGrowthNextY > 15:
			pointsEarnedFuture += 1
		TotalpointsFuture += 5

	#we need to know how many votes of each recommendation there is
	if len(Buy) + len(Overweight) + len(Hold) + len(Underweight) + len(Sell) >= 1:
		numBuy = sumList(Buy)
		numOverweight = sumList(Overweight)
		numHold = sumList(Hold)
		numUnderweight = sumList(Underweight)
		numSell = sumList(Sell)
		#2 points if total of buy and overweight is bigger than the rest, 3 points if it is bigger than 1.5 times the rest
		if numBuy + numOverweight >= numHold + numSell + numUnderweight:
			pointsEarnedFuture += 2
		if numBuy + numOverweight > 1.5 * (numHold + numSell + numUnderweight):
			pointsEarnedFuture += 3
		TotalpointsFuture += 5

	return pointsEarnedFuture, TotalpointsFuture

def past(ROA:float, ROE:float, RevenuePast5:List[float], RevenueGrowthPast5:float, EPSpast5:float, EPSgrowthPast5:float, NetIncomePast5:List[float], pointsEarnedPast = 0, TotalpointsPast = 0)	-> int:
	#We measure differrent values and see if it meets the established parameters, adding points in affirmative cases
	#3 points if EPS growth has been over 10 percent and another 2 points if it is over 20 percent
	if EPSgrowthPast5 != -1:
		if EPSgrowthPast5 > 10:
			pointsEarnedPast += 3
		if EPSgrowthPast5 > 20:
			pointsEarnedPast += 2
		TotalpointsPast += 5

	##3 points if Revenue growth has been over 10 percent and another 2 points if it is over 20 percent
	if RevenueGrowthPast5 != -1:
		if RevenueGrowthPast5 > 10:
			pointsEarnedPast += 3
		if RevenueGrowthPast5 > 20:
			pointsEarnedPast += 2
		TotalpointsPast += 5

	#3 points if it is over 20 percent
	ROE = float(ROE)
	if ROE != -1:
		if ROE >= 20:
			pointsEarnedPast += 3
		TotalpointsPast += 3

	#2 points if it is over 5 percent and another one if it is over 10 percent
	ROA = float(ROA)
	if ROA != -1:
		if ROA >= 5:
			pointsEarnedPast += 2
		if ROA >= 10:
			pointsEarnedPast += 1
		TotalpointsPast += 3

	#using a function to calculate the companies profit margins and its growth over the past years
	ProfitMarginsGrowth = ProfitMarginGrowth(RevenuePast5, NetIncomePast5)
	#3 points if profit margins have grown in the past 5 years and an  additional point if it has grown substantially
	if ProfitMarginsGrowth != -1:
		if ProfitMarginsGrowth > 0:
			pointsEarnedPast += 3
		if ProfitMarginsGrowth > 10:
			pointsEarnedPast += 1
		TotalpointsPast += 4

	return pointsEarnedPast, TotalpointsPast

def insiders(InsiderTrans:float, InstitutionTrans:float, pointsEarnedInsiders = 0, TotalpointsInsiders = 0) -> int:
	#We measure differrent values and see if it meets the established parameters, adding points in affirmative cases
	#2 points if there has been positive insider transactions
	InsiderTrans = float(InsiderTrans)
	if InsiderTrans != -1:
		if InsiderTrans > 0:
			pointsEarnedInsiders += 2
		TotalpointsInsiders += 2

	#5 points if institution transactions have been positive and another three if they have been substantial
	InstitutionTrans = float(InstitutionTrans)
	if InstitutionTrans != -1:
		if InstitutionTrans > 0:
			pointsEarnedInsiders += 5
		if InstitutionTrans > 5:
			pointsEarnedInsiders += 3
		TotalpointsInsiders += 8

	return pointsEarnedInsiders, TotalpointsInsiders


def value(PE:float, PEG:float, PS:float, PB:float, YearHighPercent:float, EBITDA:float, LongTermDebt:float, ShortTermDebt:float, FreeCashFlow:float, MarketCap:float, NetIncome:float, pointsEarnedValue = 0, TotalpointsValue = 0) -> float:
	#We measure differrent values and see if it meets the established parameters, adding points in affirmative cases
	#3 points if PE ratio is under 20 and another 2 if it is under 15
	PE = float(PE)
	if PE != -1:
		if PE <= 20:
			pointsEarnedValue += 3
		if PE <= 15:
			pointsEarnedValue += 2
		TotalpointsValue += 5
	else:
		if NetIncome != []:
			if NetIncome[-1] < 0:
				TotalpointsValue += 5	

	#3 points if PEG ratio is under 1.3 and another 2 if it is under 1
	PEG = float(PEG)
	if PEG != -1:
		if PEG <= 1.3:
			pointsEarnedValue += 2
		if PEG <= 1:
			pointsEarnedValue += 1
		TotalpointsValue += 5

	#3 points if PS ratio is under 1.8 and another 1 if it is under 1
	PS = float(PS)
	if PS != -1:
		if PS <= 1.8:
			pointsEarnedValue += 2
		if PS <= 1:
			pointsEarnedValue += 1
		TotalpointsValue += 3

	#3 points if PE ratio is under 20 and another 2 if it is under 15
	PB = float(PB)
	if PB != -1:
		if PB <= 3:
			pointsEarnedValue += 2
		if PB <= 1:
			pointsEarnedValue += 1
		TotalpointsValue += 3

	#3 points if golden ratio is under 15 and another 2 if it is under 10
	if EBITDA != -1 and LongTermDebt != -1 and FreeCashFlow != -1 and MarketCap	!= -1:
		GoldenRatio = (MarketCap + LongTermDebt + ShortTermDebt - FreeCashFlow) / EBITDA
		if GoldenRatio <= 15:
			pointsEarnedValue += 3
		if GoldenRatio <= 10:
			pointsEarnedValue += 2
		TotalpointsValue += 5

	#2 points if it is more than 10 percent of its 52 week high and another one if it is more than 20 percent off
	YearHighPercent = float(YearHighPercent)
	if YearHighPercent != -1:
		if YearHighPercent <= -10:
			pointsEarnedValue += 2
		if YearHighPercent <= -20:
			pointsEarnedValue += 1
		TotalpointsValue += 3

	#2 stage discounted cash flow

	return pointsEarnedValue, TotalpointsValue

